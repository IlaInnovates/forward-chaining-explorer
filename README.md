Forward Chaining Explorer
An interactive explainer for forward chaining, the rule-based inference algorithm from Module 2 (Knowledge Representation and Reasoning) of Foundations of Artificial Intelligence (26AI601).
A learner with no background can read the idea, watch the algorithm run step by step, ask "what if we did not know this fact?", and try their own rules.
The algorithm is implemented from scratch in plain Python (`fc_core.py`, standard library only). The website is built with Streamlit (`app.py`).
Interactive-explainer style inspired by the Georgia Tech Polo Club of Data Science tools and TensorFlow Playground. Developed with AI assistance (see the project report for the full iteration log).
Run it on your computer
```
pip install -r requirements.txt
streamlit run app.py
```
Run the tests
```
pip install pytest
python -m pytest -q
```
Files
File	Purpose	Needed to publish?
`app.py`	The website (3 tabs: The idea, Watch it work, Try your own)	Yes
`fc_core.py`	The algorithm: facts, rules, forward chaining loop, proof explanation, knowledge-base parser	Yes
`requirements.txt`	Dependencies for hosting	Yes
`README.md`	This file	Yes
`Dockerfile`	Only for Hugging Face Spaces (Docker SDK)	Hugging Face only
`hf_space_README.md`	Configuration header for the Hugging Face Space's README	Hugging Face only
`test_fc_core.py`	22 tests, including a comparison against brute-force truth-table entailment	Optional
`test_app.py`	7 headless tests of the website	Optional
Troubleshooting
`ModuleNotFoundError: No module named 'customtkinter'` (or any other module that this project does not use): Streamlit is running a different `app.py`. Open the terminal inside the unzipped `forward-chaining-explainer` folder (type `dir` and check that `fc_core.py` is listed), then run `streamlit run app.py` again.
`No module named 'fc_core'`: `fc_core.py` is missing from the folder (or from your GitHub repository). It must sit next to `app.py`.
Publish it (public URL)
Both options are free. Checked November 2026; menus change, so follow the on-screen text if a step looks different.
Option A: Streamlit Community Cloud
Create a free GitHub account and a public repository (for example `forward-chaining-explorer`). Upload `app.py`, `fc_core.py`, `requirements.txt` and `README.md` (the test files and `.gitignore` are optional).
Go to share.streamlit.io and sign in with GitHub. In your workspace click Create app, answer "Yup, I have an app", then enter the repository, branch (`main`) and main file path (`app.py`). In the App URL field you can choose a memorable subdomain (6 to 63 characters). Click Deploy.
Your address is `https://<your-subdomain>.streamlit.app`. An app deployed from a public repository is public by default. To check, open the app, click Share, and make sure "This app is public and searchable" is selected.
To update the app later, push the changed files to GitHub; it redeploys automatically.
Free apps go to sleep after a period without visitors and show a "wake it back up" button. Open your link yourself shortly before you submit.
Option B: Hugging Face Spaces (Docker)
Hugging Face's documentation says its built-in Streamlit option is deprecated and that Streamlit apps should use the Docker SDK, so this project includes a `Dockerfile`.
Create a free account at huggingface.co (sign up with an email address and confirm the email).
Open New Space and fill in: a Space name, SDK Docker (choose the blank template), hardware CPU basic (free), and visibility Public. Click Create Space.
In the Space's Files tab, upload `Dockerfile`, `app.py`, `fc_core.py` and `requirements.txt`. Then open the Space's `README.md`, edit it, and replace its contents with the contents of `hf_space_README.md` (it sets `sdk: docker` and `app_port: 8501`).
The Space shows Building, then Running (the first build takes a few minutes). Your address is `https://huggingface.co/spaces/<your-username>/<space-name>`.
If the build fails, open the Logs tab, copy the error, and send it to your assistant.
Free CPU Spaces are paused after 48 hours without visitors and restart when someone opens them.
Tip: deploy to both and put both links in the report, with the GitHub repository link as a third item.
