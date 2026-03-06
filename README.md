# api-data-sync-reporting

Sync data from REST APIs and generate clean CSV/Excel reports with Python (automation + scheduling-ready outputs).

## What it does
- Pulls data from REST API endpoints
- Normalizes fields into tables
- Joins datasets (example: posts + users)
- Produces:
  - `report.csv`
  - `report.xlsx` (report + summary sheet)
- Outputs are saved under `outputs/<timestamp>/`

## Quick start
### 1) Install
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
