# Vendor Reviews

An AI-powered vendor review system. Submit comments about vendors and get AI-generated sentiment analysis and summaries.

## Tech Stack

- **Backend:** FastAPI + SQLAlchemy (SQLite)
- **Frontend:** Streamlit
- **AI:** OpenAI gpt-4o-mini (intake agent + summary agent)

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/soltanrahail/vendor-reviews.git
cd vendor-reviews
```

**2. Create and activate a virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your OpenAI API key**
```bash
cp .env.example .env
```
Then open `.env` and replace `your_key_here` with your key from [platform.openai.com](https://platform.openai.com).

## Running the Project

You need two terminals, both with the virtual environment activated (`source .venv/bin/activate`).

**Terminal 1 — Backend:**
```bash
uvicorn main:app --reload
```

**Terminal 2 — Frontend:**
```bash
streamlit run ui.py
```

Then open **http://localhost:8501** in your browser.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/vendors` | Create a vendor |
| `GET` | `/vendors` | List all vendors |
| `POST` | `/vendors/{vendor_id}/comments` | Add a comment (AI-validated + sentiment tagged) |
| `GET` | `/vendors/{vendor_id}/comments` | Get all comments for a vendor |
| `GET` | `/vendors/{vendor_id}/summary` | Generate AI summary for a vendor |

API docs available at **http://localhost:8000/docs** when the backend is running.
