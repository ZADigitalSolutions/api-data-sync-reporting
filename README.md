# api-data-sync-reporting

Sync data from REST APIs and generate clean CSV/Excel reports with Python (automation + scheduling-ready outputs).

## What this project does
- Fetches data from one or more REST API endpoints
- Normalizes/cleans the data into tabular form
- Optionally joins multiple datasets (example: `users` + `posts`)
- Exports:
  - `report.csv`
  - `report.xlsx` (includes a `report` sheet + optional `summary` sheet)
- Writes outputs into timestamped folders: `outputs/YYYY-MM-DD_HHMMSS/`

---

## Repo layout (suggested)
```
api-data-sync-reporting/
├─ api_sync_report.py
├─ requirements.txt
├─ .env.example
├─ README.md
└─ outputs/
```

---

## Quick start
### 1) Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Configure environment variables (optional)
Create a `.env` file based on `.env.example`.

`.env.example`
```bash
API_BASE_URL=https://jsonplaceholder.typicode.com
API_TOKEN=
REQUEST_TIMEOUT_SECONDS=20
OUTPUT_DIR=outputs
EXPORT_XLSX=1
EXPORT_CSV=1
```

**Notes**
- If the API doesn’t require auth, leave `API_TOKEN` empty.
- `EXPORT_XLSX` / `EXPORT_CSV`: use `1` to enable, `0` to disable.

### 4) Run
```bash
python api_sync_report.py
```

Outputs will appear under:
```
outputs/YYYY-MM-DD_HHMMSS/report.csv
outputs/YYYY-MM-DD_HHMMSS/report.xlsx
```

---

## Default demo API
By default, the config points to:
- `https://jsonplaceholder.typicode.com` (no token required)

Typical endpoints used in demos:
- `/users`
- `/posts`

---

## Customizing for your API
### A) Change base URL
Set:
- `API_BASE_URL=https://your-api.com`

### B) Add / change endpoints
Open `api_sync_report.py` and update the endpoints list (example):
```python
ENDPOINTS = {
  "users": "/users",
  "posts": "/posts",
}
```

### C) Field mapping / renaming
If you want stable column names, add a mapping step, e.g.:
```python
RENAME = {"id": "user_id", "name": "full_name"}
df = df.rename(columns=RENAME)
```

### D) Joining datasets
Example join (posts -> users):
```python
df = posts.merge(users, left_on="userId", right_on="id", how="left")
```

---

## Scheduling (cron example)
To run every day at 9:00 AM server time:
```bash
crontab -e
```

Add:
```bash
0 9 * * * cd /path/to/api-data-sync-reporting && /path/to/api-data-sync-reporting/.venv/bin/python api_sync_report.py >> cron.log 2>&1
```

---

## Output format details
### CSV
- UTF-8 encoded
- Good for pipelines and quick checks

### Excel (.xlsx)
- One main sheet: `report`
- Optional summary sheet: `summary` (counts, totals, basic metrics)
- Great for clients who want “ready-to-open” reports

---

## Security & best practices
- Do **NOT** commit `.env` (keep secrets local)
- Prefer API tokens with least-privilege access
- If you need headers:
  - Use `Authorization: Bearer <token>` (common pattern)

---

## Troubleshooting
### SSL / network issues
- Increase `REQUEST_TIMEOUT_SECONDS`
- Verify the base URL is reachable

### Empty report
- Confirm the endpoint returns JSON
- Check if pagination is required (you may need to loop pages)

### Excel export missing
- Ensure `openpyxl` is installed via `requirements.txt`
- Ensure `EXPORT_XLSX=1`

---

## License
MIT (recommended for public repos).
