# Knowledge Repository System

A knowledge repository system with document management, search, version control, and tag management.

## Tech Stack
- **Backend:** Python, FastAPI, SQLite, SQLAlchemy
- **Frontend:** Streamlit
- **Version Control:** Git (Ensure Git is installed on your system)

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Backend (FastAPI):**
   ```bash
   uvicorn backend.main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`. You can access the Swagger UI documentation at `http://127.0.0.1:8000/docs`.

3. **Run the Frontend (Streamlit):**
   In a new terminal window, run:
   ```bash
   streamlit run frontend/app.py
   ```
   The frontend UI will be available at `http://localhost:8501`.

## Features
- **Upload Document:** Create documents and upload files (versions) to them.
- **Version Control:** Add new files to existing documents to keep a history of versions.
- **Search:** Search documents by their title or description.
- **Tag Management:** Add or remove descriptive tags to organize documents.
