import os
import json
import time
import requests
from typing import List, Dict, Any

class Readwise:
    def __init__(self, token: str):
        self.token = token
        self.api_url = "https://readwise.io/api/v2/highlights/"
        self.headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json"
        }
        self.failed_items: List[Dict[str, Any]] = []

    def create_highlights(self, highlights: List[Dict[str, Any]]):
        batch_size = 200
        for i in range(0, len(highlights), batch_size):
            batch = highlights[i:i+batch_size]
            print(f"📦 Uploading batch {i//batch_size + 1} of {(len(highlights) + batch_size - 1) // batch_size}...")
            try:
                resp = requests.post(self.api_url, headers=self.headers, json={"highlights": batch})
                if resp.status_code != 200:
                    print(f"❌ Failed batch {i//batch_size + 1}: HTTP {resp.status_code}")
                    self.failed_items.append({"batch": batch, "response": resp.text})
                    continue
                try:
                    data = resp.json()
                except ValueError:
                    print("❌ Invalid JSON in response")
                    self.failed_items.append({"batch": batch, "response": "Invalid JSON"})
            except Exception as e:
                print(f"❌ Exception in batch {i//batch_size + 1}: {str(e)}")
                self.failed_items.append({"batch": batch, "error": str(e)})
            time.sleep(1)

    def post_zotero_annotations_to_readwise(self, highlights: List[Dict[str, Any]]):
        self.create_highlights(highlights)

    def save_failed_items_to_json(self, path: str = "failed_readwise_highlights.json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.failed_items, f, indent=2, ensure_ascii=False)
        print(f"📄 {len(self.failed_items)} failed highlights saved to {path}")
