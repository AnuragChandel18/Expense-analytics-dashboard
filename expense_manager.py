from __future__ import annotations

import csv
from pathlib import Path
from datetime import date, datetime
from statistics import median
from typing import Iterable


class ExpenseManager:
    """Business logic and CSV persistence for the expense application."""

    categories = [
        "Food",
        "Transport",
        "Housing",
        "Utilities",
        "Entertainment",
        "Healthcare",
        "Shopping",
        "Education",
        "Other",
    ]

    fieldnames = ["id", "date", "category", "description", "amount"]
    date_format = "%Y-%m-%d"

    def __init__(self, data_file: Path):
        self.data_file = Path(data_file)
        self._ensure_file()

    def _ensure_file(self) -> None:
        if not self.data_file.exists():
            with self.data_file.open("w", newline="", encoding="utf-8") as file:
                csv.DictWriter(file, fieldnames=self.fieldnames).writeheader()

    def load(self) -> "pd.DataFrame":
        import pandas as pd

        self._ensure_file()
        df = pd.read_csv(self.data_file)

        if df.empty:
            return pd.DataFrame(columns=self.fieldnames)

        df["id"] = pd.to_numeric(df["id"], errors="raise").astype(int)
        df["amount"] = pd.to_numeric(df["amount"], errors="raise").astype(float)
        df["date"] = pd.to_datetime(df["date"], format=self.date_format, errors="raise")
        return df

    def _read_rows(self) -> list[dict]:
        self._ensure_file()
        with self.data_file.open(newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))

    def _write_rows(self, rows: Iterable[dict]) -> None:
        temp_file = self.data_file.with_suffix(".tmp")
        with temp_file.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        temp_file.replace(self.data_file)

    def _next_id(self, rows: list[dict]) -> int:
        return max((int(row["id"]) for row in rows), default=0) + 1

    def add_expense(
        self,
        expense_date: date,
        category: str,
        description: str,
        amount: float,
    ) -> None:
        if category not in self.categories:
            raise ValueError("Invalid category.")

        description = description.strip()
        if not description:
            raise ValueError("Description cannot be empty.")
        if len(description) > 120:
            raise ValueError("Description must be 120 characters or fewer.")

        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        rows = self._read_rows()
        rows.append(
            {
                "id": str(self._next_id(rows)),
                "date": expense_date.strftime(self.date_format),
                "category": category,
                "description": description,
                "amount": f"{amount:.2f}",
            }
        )
        self._write_rows(rows)

    def delete_expense(self, expense_id: int) -> bool:
        rows = self._read_rows()
        updated = [row for row in rows if int(row["id"]) != expense_id]

        if len(updated) == len(rows):
            return False

        self._write_rows(updated)
        return True

    def summary(self) -> dict:
        rows = self._read_rows()
        if not rows:
            return {
                "count": 0,
                "total": 0.0,
                "average": 0.0,
                "median": 0.0,
                "min": 0.0,
                "max": 0.0,
            }

        amounts = [float(row["amount"]) for row in rows]
        return {
            "count": len(amounts),
            "total": sum(amounts),
            "average": sum(amounts) / len(amounts),
            "median": median(amounts),
            "min": min(amounts),
            "max": max(amounts),
        }
