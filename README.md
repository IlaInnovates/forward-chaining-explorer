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

## Files
| File | Purpose |
|---|---|
| `fc_core.py` | The algorithm: facts, rules, forward chaining loop, proof explanation, knowledge-base parser |
| `app.py` | The website (3 tabs: The idea, Watch it work, Try your own) |
| `test_fc_core.py` | 19 tests, including a comparison against brute-force truth-table entailment |
| `test_app.py` | 5 headless tests of the website |
| `requirements.txt` | Dependencies for hosting |

## Publish it (public URL)
Both options are free. Checked November 2026; menus change, so follow the on-screen text if a step looks different.

**Option A: Streamlit Community Cloud**
1. Create a free GitHub account and a **public** repository (for example `forward-chaining-explorer`). Upload `app.py`, `fc_core.py`, `requirements.txt` and `README.md` (the test files and `.gitignore` are optional).
2. Go to share.streamlit.io and sign in with GitHub. In your workspace click **Create app**, answer "Yup, I have an app", then enter the repository, branch (`main`) and main file path (`app.py`). In the **App URL** field you can choose a memorable subdomain (6 to 63 characters). Click **Deploy**.
3. Your address is `https://<your-subdomain>.streamlit.app`. An app deployed from a public repository is public by default. To check, open the app, click **Share**, and make sure "This app is public and searchable" is selected.
4. To update the app later, push the changed files to GitHub; it redeploys automatically.
5. Free apps go to sleep after a period without visitors and show a "wake it back up" button. Open your link yourself shortly before you submit.

**Option B: Hugging Face Spaces**
1. Create a free account, then **New Space**: choose the **Streamlit** SDK, free **CPU basic** hardware, and **Public**.
2. Upload the same files. Replace the Space's `README.md` with the contents of `hf_space_README.md` (it holds the configuration header with `sdk: streamlit` and `app_file: app.py`).
3. Your address is `https://huggingface.co/spaces/<your-username>/<space-name>`. Free CPU Spaces are paused after 48 hours without visitors and restart when someone opens them.

**Tip:** deploy to both and put both links in the report, with the GitHub repository link as a third item.
