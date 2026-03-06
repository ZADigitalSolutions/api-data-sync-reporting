import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv


def fetch_json(url: str, headers: dict | None = None) -> list[dict]:
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()
    if isinstance(data, dict):
        return [data]
    return data


def main() -> None:
    load_dotenv()

    base_url = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com").rstrip("/")
    token = os.getenv("API_TOKEN", "").strip()

    headers = {"Authorization": f"Bearer {token}"} if token else None

    out_dir = Path("outputs") / datetime.now().strftime("%Y-%m-%d_%H%M")
    out_dir.mkdir(parents=True, exist_ok=True)

    users = fetch_json(f"{base_url}/users", headers=headers)
    posts = fetch_json(f"{base_url}/posts", headers=headers)

    df_users = pd.DataFrame(users)[["id", "name", "email", "username"]].rename(columns={"id": "user_id"})
    df_posts = pd.DataFrame(posts)[["userId", "id", "title"]].rename(columns={"userId": "user_id", "id": "post_id"})

    report = df_posts.merge(df_users, on="user_id", how="left")
    report["title_len"] = report["title"].astype(str).str.len()

    # Save outputs
    report_csv = out_dir / "report.csv"
    report_xlsx = out_dir / "report.xlsx"

    report.to_csv(report_csv, index=False)

    with pd.ExcelWriter(report_xlsx, engine="openpyxl") as w:
        report.to_excel(w, sheet_name="report", index=False)
        report.groupby("user_id").size().reset_index(name="posts_count").to_excel(w, sheet_name="summary", index=False)

    print(f"Saved:\n- {report_csv}\n- {report_xlsx}")


if __name__ == "__main__":
    main()
