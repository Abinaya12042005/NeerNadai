# 💧 Chennai Smart Water Watch
### AI-Powered Area-Wise Water Wastage Monitor + RAG Chatbot
Built for the **1M1B AI for Sustainability Virtual Internship** (with IBM SkillsBuild & AICTE)
**SDG Alignment:** SDG 6 — Clean Water and Sanitation

---

## What this project does
- **Live dashboard**: shows water usage (litres/person/day) for 4 Chennai zones, flags each as Low/Medium/High **wastage risk** using a trained ML model.
- **RAG chatbot**: ask questions like *"which area wastes the most water?"* or *"how do I save water at home?"* — answered using real project data + verified water-conservation facts (Retrieval-Augmented Generation), generated with **IBM Granite** (free via Hugging Face).
- Built entirely with **free, open-source tools** — no paid subscriptions.

---

## STEP 1 — Get the real dataset from Kaggle

This project ships with **synthetic sample data** so you can run it today. Before final submission, swap in the real dataset:

1. Go to: https://www.kaggle.com/datasets/sudalairajkumar/chennai-water-management
2. Click **Download** (or use the Kaggle API — see below).
3. You'll get `chennai_reservoir_levels.csv` and `chennai_reservoir_rainfall.csv`.
4. Replace the files inside `data/` with these real ones (**same filenames**).

**Using the Kaggle API instead (faster):**
```bash
pip install kaggle
# Get your API token: kaggle.com -> Account -> "Create New API Token" -> saves kaggle.json
mkdir -p ~/.kaggle && mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

kaggle datasets download -d sudalairajkumar/chennai-water-management -p data/ --unzip
```

> Note: the real Kaggle dataset gives reservoir levels (not per-person LPCD directly). Re-run `python model_train.py` after swapping data — the `area_wise_consumption.csv` (LPCD/wastage numbers) is derived by `data/generate_sample_data.py`. If you want the model trained on the *real* reservoir trends instead of the synthetic LPCD numbers, tell me and I'll adjust `model_train.py` to use reservoir draw-down rate as the wastage signal instead — either is a valid, defensible approach for the submission.

---

## STEP 2 — Set up your environment

```bash
# 1. Clone or open the project folder, then create a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
```

---

## STEP 3 — Build the data, knowledge base, and model (run once)

```bash
python data/generate_sample_data.py     # skip this if you already placed the real Kaggle CSVs
python build_knowledge_base.py          # creates the chatbot's knowledge base from your data
python model_train.py                   # trains the RandomForest wastage-risk model
```

---

## STEP 4 — (Optional but recommended) Enable full AI-generated chatbot answers

The chatbot **works immediately with zero setup** (it falls back to showing the most relevant knowledge-base facts). To get full natural-language answers from **IBM Granite**:

1. Create a free Hugging Face account: https://huggingface.co/join
2. Get a free token: https://huggingface.co/settings/tokens (role: "Read")
3. Set it as an environment variable before running the app:
```bash
export HF_TOKEN="hf_your_token_here"      # Windows (PowerShell): $env:HF_TOKEN="hf_your_token_here"
```

---

## STEP 5 — Run the website

```bash
python app.py
```
Open your browser at **http://127.0.0.1:5000** — dashboard + chatbot both live on the same page.

**"Real-time" note (be upfront about this in your submission):** the dashboard re-reads `data/area_wise_consumption.csv` on every page load — so it updates instantly the moment new data is added, without restarting the server. For a live demo, you can write a small script that appends a new row every few seconds to simulate a live sensor feed (happy to build that if you want it for your demo video — it's an honest, transparent way to show "real-time" behavior, which also satisfies the guideline's **Responsible AI — Transparency** requirement).

---

## STEP 6 — Push the project to GitHub

```bash
cd smart-water-watch
git init
git add .
git commit -m "Initial commit: Chennai Smart Water Watch - AI water wastage dashboard + RAG chatbot"

# Create a new EMPTY repo on github.com first (don't add a README there), then:
git remote add origin https://github.com/YOUR-USERNAME/chennai-smart-water-watch.git
git branch -M main
git push -u origin main
```

Add this GitHub link in your 1M1B submission form under "Links to GitHub, videos, presentations or prototypes."

**Important:** `.gitignore` already excludes `*.pkl` (trained model files) and `venv/` to keep the repo light. If you want the trained model included in the repo too (so reviewers don't have to re-run `model_train.py`), just remove `*.pkl` from `.gitignore` before committing.

---

## STEP 7 — Record your demo video
1. Screen-record: open the site → show the dashboard/area cards → ask the chatbot 2-3 questions → briefly show the code (app.py, rag_chatbot.py, model_train.py) in your editor.
2. Keep it under 3-4 minutes — walk through: **problem → AI solution → demo → impact**.
3. Upload to YouTube (unlisted) or Google Drive, and add the link to the submission form.

---

## Project structure
```
smart-water-watch/
├── app.py                       # Flask app (dashboard + chatbot API)
├── rag_chatbot.py                # RAG engine (FAISS + sentence-transformers + IBM Granite)
├── build_knowledge_base.py       # Generates chatbot's knowledge base
├── model_train.py                # Trains the RandomForest wastage-risk model
├── data/
│   ├── generate_sample_data.py
│   ├── chennai_reservoir_levels.csv     <- replace with real Kaggle file
│   ├── chennai_reservoir_rainfall.csv   <- replace with real Kaggle file
│   └── area_wise_consumption.csv
├── knowledge_base/                # auto-generated .txt files the chatbot searches
├── model/                          # saved wastage_model.pkl (after training)
├── templates/index.html
├── static/style.css
├── requirements.txt
└── README.md
```

## Submission checklist (from the 1M1B guideline doc)
- [x] Problem statement — area-wise water wastage in Chennai (SDG 6)
- [x] AI elements — RandomForest (ML prediction) + RAG (retrieval + IBM Granite generation)
- [x] Technologies Used field — mention: **RAG, IBM Granite (via Hugging Face), scikit-learn, Flask**
- [x] Responsible AI section — see `knowledge_base/project_info.txt` (fairness, transparency, privacy notes) — reuse this text in your PPT
- [ ] GitHub link — do Step 6 above
- [ ] Screenshots/demo video — do Step 7 above
- [ ] PPT — see the `Chennai_Smart_Water_Watch.pptx` file provided alongside this project
