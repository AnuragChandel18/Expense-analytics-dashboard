# Expense Analytics Dashboard

A Python-based personal expense tracking and analytics application that combines structured CSV storage with an interactive Streamlit dashboard.

## Why this project?

This project demonstrates more than CRUD operations. It shows how to collect structured data, validate it, transform it with pandas, and turn it into useful business-style spending insights.

## Features

- Add and persist expenses
- Category-based expense tracking
- Date-range filtering
- Category filtering
- Description search
- Total, average and median spending KPIs
- Category spending analysis
- Monthly spending trend
- Top 5 expense analysis
- Transaction-level data table
- CSV persistence
- Input validation
- Atomic CSV replacement during updates

## Tech Stack

- Python
- Streamlit
- Pandas
- CSV
- OOP
- Data validation
- Git/GitHub

## Project Structure

```text
expense-analytics-dashboard/
├── app.py
├── expense_manager.py
├── expenses.csv
├── requirements.txt
├── .gitignore
└── README.md
```

## Run Locally

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the dashboard:

```bash
streamlit run app.py
```

## Data Model

| Column | Description |
|---|---|
| id | Unique expense identifier |
| date | Expense date |
| category | Spending category |
| description | Short description |
| amount | Expense amount in INR |

## Key Analytics

The dashboard calculates:

- Total spend
- Number of transactions
- Average expense
- Median expense
- Category-level spending
- Monthly spending trend
- Highest individual expenses

## What I Learned

- Designing a small Python application using classes and separation of responsibilities
- Validating user input before persistence
- Working with CSV as a lightweight data store
- Using pandas for aggregation and filtering
- Building an interactive data dashboard with Streamlit
- Thinking about data integrity when writing files
- Presenting raw data as decision-useful metrics

## Future Improvements

- SQLite database
- Budget limits and alerts
- Export filtered reports
- Authentication
- Recurring expenses
- More advanced visualizations

## Author

Anurag Singh Chandel
