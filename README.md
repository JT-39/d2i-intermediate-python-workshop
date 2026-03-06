# D2I Intermidiate Python Workshop

## End-to-End Data Workflow in Python

This repository contains course material demonstrating a **real-world, end-to-end data workflow** in Python.

The course covers:
- Ingesting data from SQL databases and flat files  
- Cleaning, transforming, and calculating metrics  
- Formatting and exporting outputs for downstream tools (e.g. Power BI)  
- Light dashboarding in Python  

By the end of the course, you will have a **single, production-style Python script** that runs from data extraction to final output in one click.

A strong emphasis is placed on:
- Writing reusable and well-structured Python code  
- Organising code across modules and scripts  
- Testing data pipelines and calculations  
- Professional syntax, formatting, and best practices  

This course builds on beginner-level Python and focuses on writing code suitable for real analytics and data engineering workflows.

## Session 1

Using this repo:

https://github.com/data-to-insight/ERN-sessions/tree/main/intermediate_python

Two databases:

- `903_database.db`
- `gravity.db`

Code to setup a database from an Excel file:

```python
import pandas as pd
import sqlite3


# Run this to make the 903 database file
db = sqlite3.connect("903_database.db")
dfs = pd.read_excel("/workspaces/ERN-sessions/data/903_xlsx.xlsx", sheet_name=None)
for table, df in dfs.items():
    df.to_sql(table, db)
db.commit()
db.close()
 ```

 Notes can be found with Will's repo https://github.com/data-to-insight/ERN-sessions/tree/main/intermediate_python, inside the relevant `.ipynb` file.