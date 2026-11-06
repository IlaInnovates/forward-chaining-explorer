# Forward Chaining Explorer

An interactive explainer for **forward chaining**, the rule-based inference algorithm from Module 2 (Knowledge Representation and Reasoning) of *Foundations of Artificial Intelligence* (26AI601).
A learner with no background can read the idea, watch the algorithm run step by step, ask "what if we did not know this fact?", and try their own rules.

The algorithm is implemented from scratch in plain Python (`fc_core.py`, standard library only). The website is built with Streamlit (`app.py`).
Interactive-explainer style inspired by the Georgia Tech Polo Club of Data Science tools and TensorFlow Playground. Developed with AI assistance (see the project report for the full iteration log).

## Run it on your computer
```
pip install -r requirements.txt
streamlit run app.py
```

## Run the tests
```
pip install pytest
python -m pytest -q
```




