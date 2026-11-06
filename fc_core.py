"""
fc_core.py -- Forward chaining, implemented from the base (standard library only).

Lecture idea (Module 2, Knowledge Representation): a knowledge base holds FACTS and RULES.
Forward chaining repeatedly
    1. looks at the known facts,
    2. finds rules whose conditions are all satisfied by those facts,
    3. fires one rule, adding its conclusion to the knowledge,
    4. repeats until no new conclusion can be derived.
"Forward chaining asks: what can I derive from what I know?"

Version 1 handles propositional (ground) rules: premise1 & premise2 -> conclusion.
Every atom is an opaque string such as "Enrolled(Asha,AI)".
"""
from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class Rule:
    name: str
    premises: Tuple[str, ...]
    conclusion: str

    def __str__(self) -> str:
        return f"{self.name}: {' & '.join(self.premises)} -> {self.conclusion}"


@dataclass
class Firing:
    """One match-fire cycle, recorded for the step-by-step explainer."""
    step: int                              # 1-based
    rule: Rule                             # the rule that fired
    derived: str                           # the new fact it added
    applicable: List[str]                  # names of ALL rules that could fire at this moment
    blocked: Dict[str, List[str]]          # rule name -> premises still missing (rules that could not fire)
    known_before: Tuple[str, ...]          # facts known just before this step


@dataclass
class FCResult:
    given: List[str]                       # initial facts (duplicates removed, order kept)
    firings: List[Firing]
    known: List[str]                       # given facts followed by derived facts, in order of discovery
    provenance: Dict[str, Firing]          # derived fact -> the firing that produced it
    query: Optional[str] = None
    query_derived: Optional[bool] = None
    stopped_early: bool = False


# ------------------------------------------------------------------ the algorithm
def forward_chain(facts: Sequence[str], rules: Sequence[Rule],
                  query: Optional[str] = None, stop_at_query: bool = False) -> FCResult:
    """Run forward chaining to a fixed point (or until the query is derived).

    Conflict resolution: when several rules are applicable, the one listed first fires first.
    A rule only fires if it would add something new, so every firing derives a new fact and the
    loop must stop after at most len(rules) firings.
    """
    given = list(dict.fromkeys(facts))                 # drop duplicates, keep order
    known_list = list(given)
    known = set(known_list)
    firings: List[Firing] = []
    provenance: Dict[str, Firing] = {}
    stopped_early = False

    if query is not None and stop_at_query and query in known:
        stopped_early = True
    else:
        while True:
            applicable: List[Rule] = []
            blocked: Dict[str, List[str]] = {}
            for r in rules:
                if r.conclusion in known:
                    continue                           # would add nothing new
                missing = [p for p in r.premises if p not in known]
                if missing:
                    blocked[r.name] = missing
                else:
                    applicable.append(r)
            if not applicable:
                break                                  # fixed point: nothing more can be derived
            chosen = applicable[0]
            f = Firing(len(firings) + 1, chosen, chosen.conclusion,
                       [r.name for r in applicable], blocked, tuple(known_list))
            firings.append(f)
            provenance[chosen.conclusion] = f
            known.add(chosen.conclusion)
            known_list.append(chosen.conclusion)
            if query is not None and stop_at_query and chosen.conclusion == query:
                stopped_early = True
                break

    return FCResult(given, firings, known_list, provenance, query,
                    None if query is None else query in known, stopped_early)


def prove(fact: str, result: FCResult) -> List[str]:
    """Plain-language derivation of `fact` (why is it known?), as indented lines."""
    lines: List[str] = []

    def walk(f: str, depth: int) -> None:
        pad = "    " * depth
        if f in result.given:
            lines.append(f"{pad}{f}   [given fact]")
            return
        fr = result.provenance.get(f)
        if fr is None:
            lines.append(f"{pad}{f}   [NOT derivable]")
            return
        lines.append(f"{pad}{f}   [derived by {fr.rule.name}: {' & '.join(fr.rule.premises)} -> {fr.rule.conclusion}]")
        for p in fr.rule.premises:
            walk(p, depth + 1)

    walk(fact, 0)
    return lines


# ------------------------------------------------------------------ parsing the knowledge base text
_AND = re.compile(r"\s*(?:&|∧|\^|\bAND\b|\band\b)\s*")
_ARROW = re.compile(r"\s*(?:->|→|=>)\s*")


def parse_kb(facts_text: str, rules_text: str) -> Tuple[List[str], List[Rule]]:
    """Facts: one per line. Rules: 'A & B -> C' per line, optional 'R1:' label. '#' starts a comment."""
    facts: List[str] = []
    for n, raw in enumerate(facts_text.splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if _ARROW.search(line):
            raise ValueError(f"Facts line {n}: '{line}' looks like a rule. Put rules in the rules box.")
        facts.append(line)
    facts = list(dict.fromkeys(facts))                 # the same fact typed twice counts once

    parsed = []                                        # (line number, explicit name or None, premises, conclusion)
    for n, raw in enumerate(rules_text.splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        name = None
        m = re.match(r"^([A-Za-z_][\w]*)\s*:\s*(.+)$", line)
        if m:
            name, line = m.group(1), m.group(2)
        parts = _ARROW.split(line)
        if len(parts) != 2:
            raise ValueError(f"Rules line {n}: write a rule as  A & B -> C  (exactly one arrow).")
        left, right = parts[0].strip(), parts[1].strip()
        premises = tuple(p.strip() for p in _AND.split(left) if p.strip())
        if not premises:
            raise ValueError(f"Rules line {n}: a rule needs at least one condition before the arrow.")
        if not right or _AND.search(right):
            raise ValueError(f"Rules line {n}: a rule must have exactly one conclusion after the arrow.")
        parsed.append((n, name, premises, right))

    explicit = [p[1] for p in parsed if p[1]]
    for n, name, _, _ in parsed:
        if name and explicit.count(name) > 1:
            raise ValueError(f"Rules line {n}: the rule name '{name}' is already used.")
    used, rules = set(explicit), []
    for position, (n, name, premises, right) in enumerate(parsed, 1):
        if not name:                                   # automatic name = rule position, skipping names already taken
            k = position
            while f"R{k}" in used:
                k += 1
            name = f"R{k}"
            used.add(name)
        rules.append(Rule(name, premises, right))
    return facts, rules
