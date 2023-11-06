if not exist .\songs\ (
    mkdir songs
)

if not exist .\.venv\ (
    python -m venv .\.venv
    .\.venv\Scripts\pip install -r requirements.txt
)

.\.venv\Scripts\python main.py