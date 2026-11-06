"""
Forward Chaining Explorer  --  version 1
An interactive explainer for FORWARD CHAINING (Foundations of AI, 26AI601, Module 2).
Run locally:  streamlit run app.py
"""
import streamlit as st
from fc_core import FCResult, Rule, forward_chain, parse_kb, prove

st.set_page_config(page_title="Forward Chaining Explorer", page_icon="🔗", layout="wide")

# ------------------------------------------------------------------ scenarios
SCENARIOS = {
    "Course access (the lecture example)": dict(
        about="The University AI Assistant is asked: *Can Asha download the lecture notes?* "
              "It starts from what it knows and derives step by step.",
        facts="Student(Asha)\nEnrolled(Asha,AI)",
        rules="R1: Enrolled(Asha,AI) -> HasAccess(Asha,AIMaterials)\n"
              "R2: HasAccess(Asha,AIMaterials) -> CanDownload(Asha,LectureNotes)",
        query="CanDownload(Asha,LectureNotes)"),
    "Eligibility for Advanced AI": dict(
        about="Anyone who completed AI **and** ML is eligible for Advanced AI. "
              "Try un-ticking *Completed(Asha,ML)* and see what happens.",
        facts="Student(Asha)\nCompleted(Asha,AI)\nCompleted(Asha,ML)",
        rules="R1: Completed(Asha,AI) & Completed(Asha,ML) -> Eligible(Asha,AdvancedAI)",
        query="Eligible(Asha,AdvancedAI)"),
    "Campus library (several rules ready at once)": dict(
        about="Two rules are ready at the very start. Watch how the order of the rules decides which "
              "fires first, and why the final answer does not depend on that order.",
        facts="Enrolled(Asha)\nFeesPaid(Asha)\nHasIDCard(Asha)",
        rules="R1: Enrolled(Asha) & FeesPaid(Asha) -> ActiveStudent(Asha)\n"
              "R2: HasIDCard(Asha) -> CanEnterCampus(Asha)\n"
              "R3: ActiveStudent(Asha) & CanEnterCampus(Asha) -> CanUseLibrary(Asha)\n"
              "R4: ActiveStudent(Asha) -> HasPortalAccess(Asha)\n"
              "R5: CanUseLibrary(Asha) & HasPortalAccess(Asha) -> CanBorrowEBooks(Asha)",
        query="CanBorrowEBooks(Asha)"),
}


# ------------------------------------------------------------------ helpers
def _set(key, value):
    st.session_state[key] = value


def _q(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def derivation_dot(result: FCResult, step: int) -> str:
    """Graphviz picture of the knowledge base after `step` firings."""
    newest = result.firings[step - 1].derived if step > 0 else None
    lines = ["digraph G {", "rankdir=LR;", 'node [fontname="Helvetica", fontsize=11];']
    ids = {}

    def fact_node(f):
        if f not in ids:
            ids[f] = f"f{len(ids)}"
            given = f in result.given
            fill = "#E3E6EE" if given else "#CDEBD3"
            extra = ', color="#E08A00", penwidth=3' if f == newest else ""
            if result.query == f:
                extra += ', peripheries=2'
            lines.append(f'{ids[f]} [label={_q(f)}, shape=box, style="rounded,filled", fillcolor="{fill}"{extra}];')
        return ids[f]

    for f in result.given:
        fact_node(f)
    for fr in result.firings[:step]:
        rid = f"r{fr.step}"
        lines.append(f'{rid} [label={_q(fr.rule.name)}, shape=ellipse, style=filled, fillcolor="#FFF3CD", fontsize=10];')
        for p in fr.rule.premises:
            lines.append(f"{fact_node(p)} -> {rid};")
        lines.append(f"{rid} -> {fact_node(fr.derived)};")
    lines.append("}")
    return "\n".join(lines)


def narrate(result: FCResult, step: int) -> str:
    n = len(result.firings)
    if step == 0:
        return (f"**Start.** The knowledge base holds {len(result.given)} given fact(s). "
                "Forward chaining now looks for a rule whose conditions are *all* already known.")
    fr = result.firings[step - 1]
    cond = " and ".join(f"**{p}**" for p in fr.rule.premises)
    text = (f"**Step {step}.** Rule **{fr.rule.name}** says: if {cond}, then **{fr.derived}**. "
            f"Every condition is already known, so **{fr.derived}** is added to the knowledge base.")
    others = [r for r in fr.applicable if r != fr.rule.name]
    if others:
        text += (f" Other rules were ready too ({', '.join(others)}). When several are ready, "
                 "the rule listed first fires first and the others wait for a later step.")
    if step == n:
        text += (" **No rule can add anything new now, so forward chaining stops.** "
                 "Everything the rules can justify from these facts is known: this is called a fixed point.")
    return text


def rule_status(result: FCResult, rules, step: int):
    known = set(result.known[: len(result.given) + step])
    rows = []
    for r in rules:
        missing = [p for p in r.premises if p not in known]
        if r.conclusion in known:
            status = "✔ conclusion already known"
        elif not missing:
            status = "🟢 ready to fire"
        else:
            status = "⏳ waiting for: " + ", ".join(missing)
        rows.append({"Rule": r.name, "If … then …": f"{' & '.join(r.premises)}  →  {r.conclusion}", "Status": status})
    return rows


# ------------------------------------------------------------------ the explorer widget
def render_explorer(key: str, facts, rules, query: str):
    with st.expander("Facts the system starts with (untick a fact to ask “what if we did not know this?”)", expanded=True):
        included = [f for f in facts if st.checkbox(f, value=True, key=f"{key}_fact_{f}")]

    result = forward_chain(included, rules, query or None)
    n = len(result.firings)
    sk, sig_k = f"{key}_step", f"{key}_sig"
    sig = (tuple(included), tuple(rules), query)
    if st.session_state.get(sig_k) != sig:                      # knowledge base changed -> restart
        st.session_state[sig_k] = sig
        st.session_state[sk] = 0
    step = min(st.session_state.get(sk, 0), n)

    c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1.4, 3])
    c1.button("⏮ Reset", key=f"{key}_reset", on_click=_set, args=(sk, 0), disabled=step == 0)
    c2.button("◀ Back", key=f"{key}_back", on_click=_set, args=(sk, step - 1), disabled=step == 0)
    c3.button("▶ Step", key=f"{key}_step_btn", on_click=_set, args=(sk, step + 1), disabled=step >= n, type="primary")
    c4.button("⏭ Run to end", key=f"{key}_end", on_click=_set, args=(sk, n), disabled=step >= n)
    c5.progress(1.0 if n == 0 else step / n, text=f"Step {step} of {n}" if n else "No rule can fire")

    left, right = st.columns([3, 2])
    with left:
        st.markdown(narrate(result, step) if n or step == 0 else "")
        if n == 0:
            st.warning("With these facts no rule can fire, so nothing new is derived. "
                       "Inference is not guessing: a conclusion appears only when the rules justify it.")
        st.graphviz_chart(derivation_dot(result, step), width="stretch")
        st.caption("Grey = given fact · green = derived fact · orange outline = newest · yellow oval = rule that fired · double border = query")
    with right:
        known_now = result.known[: len(result.given) + step]
        st.markdown("**Known facts now**")
        for f in known_now:
            tag = "given" if f in result.given else "derived"
            new = step > 0 and f == result.firings[step - 1].derived
            st.markdown(f"{'🟠' if new else ('⚪' if tag == 'given' else '🟢')} `{f}` — {tag}{' (new)' if new else ''}")
        st.markdown("**Rules: what can fire next?**")
        st.dataframe(rule_status(result, rules, step), hide_index=True, width="stretch")

    if query:
        if query in known_now:
            st.success(f"Query **{query}** is derived. Why? Follow the chain back to given facts:")
            st.code("\n".join(prove(query, result)), language="text")
        elif step == n:
            st.info(f"Query **{query}** was **not derived**. That does not mean it is false. "
                    "It means this knowledge base cannot justify it.")


# ------------------------------------------------------------------ page
st.title("🔗 Forward Chaining Explorer")
st.markdown("*How does an AI system derive new knowledge from what it already knows?*  "
            "Learn the idea, watch it run step by step, then try your own rules.")

tab_idea, tab_watch, tab_try = st.tabs(["1 · The idea", "2 · Watch it work", "3 · Try your own"])

with tab_idea:
    st.header("What problem does it solve?")
    st.markdown(
        "An intelligent agent stores what it knows as **facts** (things that are true) and **rules** "
        "(if these things are true, then this other thing is true). Having knowledge is not enough: the agent must "
        "also **reason**, deriving conclusions that were never written down explicitly.\n\n"
        "**Forward chaining** is the simplest way to reason: *start from the facts and keep applying rules "
        "until nothing new can be learned.* It answers the question **“What can I derive from what I know?”**")
    st.header("A tiny example")
    st.markdown(
        "- **Fact:** Asha is enrolled in AI  →  `Enrolled(Asha,AI)`\n"
        "- **Rule 1:** if enrolled in AI, then has access to the AI materials\n"
        "- **Rule 2:** if has access to the AI materials, then can download the lecture notes\n\n"
        "Nobody told the system that Asha can download the notes. It *derived* it: Fact → Rule 1 → new fact → Rule 2 → new fact.")
    st.header("The four-step loop")
    st.code("repeat:\n"
            "    1. look at the known facts\n"
            "    2. find the rules whose conditions are ALL known (and whose conclusion is new)\n"
            "    3. fire one rule: add its conclusion to the known facts\n"
            "until no rule can fire          # a 'fixed point'", language="text")
    st.header("Three ideas worth remembering")
    st.markdown(
        "1. **It never guesses.** If a condition is missing, the rule does not fire. Not derived does not mean false.\n"
        "2. **It always stops.** Every firing adds a new fact, and there are only finitely many conclusions.\n"
        "3. **Order does not change the final answer.** If several rules are ready, the order only changes the *path*, not what is known at the end.")
    st.header("Where is it used?")
    st.markdown("Rule-based expert systems and production-rule engines (for example CLIPS and Drools), business-rule "
                "checks, and reasoning over knowledge graphs, where new relationships are derived from existing ones.")
    st.info("Ready? Open the next tab and press **▶ Step**.")

with tab_watch:
    name = st.selectbox("Choose a scenario", list(SCENARIOS), key="scenario")
    sc = SCENARIOS[name]
    st.markdown(sc["about"])
    s_facts, s_rules = parse_kb(sc["facts"], sc["rules"])
    render_explorer("ex", s_facts, s_rules, sc["query"])

with tab_try:
    st.markdown("Write your own knowledge base. **Facts:** one per line. **Rules:** `A & B -> C` "
                "(use `&` or `AND` between conditions; optional label like `R1:`). Lines starting with `#` are comments.")
    a, b = st.columns(2)
    t_facts = a.text_area("Facts", "Raining\nHaveUmbrella", height=140, key="custom_facts")
    t_rules = b.text_area("Rules", "R1: Raining & HaveUmbrella -> StayDry\nR2: StayDry -> GoOutside", height=140, key="custom_rules")
    t_query = st.text_input("Query (what do you want to find out?)", "GoOutside", key="custom_query")
    try:
        c_facts, c_rules = parse_kb(t_facts, t_rules)
    except ValueError as e:
        st.error(str(e))
    else:
        if not c_facts:
            st.warning("Add at least one fact to start from.")
        else:
            render_explorer("cx", c_facts, c_rules, t_query.strip())

st.divider()
st.caption("Built for Foundations of Artificial Intelligence (26AI601). Interactive-explainer style inspired by the "
           "Georgia Tech Polo Club of Data Science tools and TensorFlow Playground. Developed with AI assistance; "
           "the algorithm is implemented from scratch in Python. Version 1.")