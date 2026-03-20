import pandas as pd
from sqlalchemy import (
    create_engine,
    inspect,
    text,
    select,
    MetaData,
    Table,
)
from utils import (
    clean_903_table,
    group_calculation,
    time_difference,
    multiples_same_event,
    group_calculation_year,
    appears_on_both,
)
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

# Initialise session variables
filepath = "/workspaces/d2i-intermediate-python-workshop/data/903_database.db"

# User to select year of data they want to return
collection_year = 2014
collection_end = datetime(collection_year, 3, 31)

# Read in 903 data from SQL db
engine_903 = create_engine(f"sqlite+pysqlite:///{filepath}")
connection = engine_903.connect()
inspection = inspect(engine_903)

table_names = inspection.get_table_names()

# Uncomment to check database connection
# print(table_names)

metadata_903 = MetaData()

dfs = {}
for table in table_names:
    current_table = Table(table, metadata_903, autoload_with=engine_903)
    with engine_903.connect() as con:
        stmt = select(current_table)
        result = con.execute(stmt).fetchall()
    dfs[table] = pd.DataFrame(result)

# Uncomment to check reading of tables as dfs
# print(dfs.keys())
# print(dfs.values())

# Clean all tables in 903
for key, df in dfs.items():
    dfs[key] = clean_903_table(df, collection_end)

# print(dfs["header"])

# Session 3
"""
Calculating, transforming, and groupbys
"""
# If we are prepping data for Power BI/Excel we want to organise our data differently to prep for Python.
# For external dashboarding products we want everything calculated already so we can easily slice it
# and keep the dashboard nice and lightweight, not performing any calculations

# We need an empty dict to store our measures in:
measures_dict = {}

# Calculate groupbys
# We'll need a reusable function here that can groupby a value in a colum (e.g. ethnicity) that outputs
# in the way we want so we can reuse it every time we want to group by something

# Total CYP in header by ethnicity
# Let's do it for ethnicity then turn it into a function - let's get a count and a percent

# grouped = dfs['header'].groupby(['ETHNICITY']).size()
# grouped = grouped.to_frame('Header - Ethnicities - Count').reset_index()
# grouped = grouped.rename(columns={'ETHNICITY':'Ethnicities'})

# grouped['Header - Ethnicities - Percentage'] =  (grouped['Header - Ethnicities - Count'] / grouped['Header - Ethnicities - Count'].sum() ) * 100

# print(grouped)
# print(grouped['Header - Ethnicities - Percentage'].sum())
# Let's make the function in utils.py
measures_dict["Header by ethnicity"] = group_calculation(
    dfs["header"], "ETHNICITY", "Header - Ethnicities"
)

# Let's show now how easy it is to do the same using our age buckets
measures_dict["Header by age"] = group_calculation(
    dfs["header"], "AGE_BUCKETS", "Header - Age"
)


# Now let's see why we did it like this for our final outputs.
# We won't keep this in but we will use it later
output_table = pd.concat([measures_dict["Header by ethnicity"], measures_dict["Header by age"]])

# Calculate time periods
# Whether we want exact numbers of buckets, we need a way to calculate time periods (e.g. time children have)
# been in a placement. It's good to have contingency for business days in there too as many CS
# measures_dict take note of business days

# Same premise, make it as a normal calculation then turn it into a function
# dfs["missing"]["MISSING_DURATION"] = dfs["missing"].apply(
#     lambda x: relativedelta(x["MIS_START_dt"], x["MIS_END_dt"]).normalized().days, axis=1
# )

# dfs["missing"]['MISSING_DURATION2'] = dfs["missing"]["MIS_END_dt"] - dfs["missing"]["MIS_START_dt"]

# or for working days:
# We need to convert these to np datetime 64s rather than pd datetimes for this calculation
# dfs["missing"]['MISSING_DURATION3'] = np.busday_count(dfs["missing"]["MIS_START_dt"].values.astype('datetime64[D]'), dfs["missing"]["MIS_END_dt"].values.astype('datetime64[D]'))

dfs["missing"]["MISSING_DURATION"] = time_difference(
    dfs["missing"]["MIS_START_dt"], dfs["missing"]["MIS_END_dt"]
)

# We might also think about making some type of function that groups this by numbers of days.
# That will depend on what we are looking at, however, for instance we might want under and over
# 45 days for assessments, but that would make no sense for placement lengths.
# We could .apply() a function like the one for age buckets in each different instance for this
# print(dfs["missing"])

measures_dict["Multiple episodes"] = multiples_same_event(
    dfs["episodes"], event_name="Number of episodes"
)

dfs["episodes"]["DECOM_YEAR"] = dfs["episodes"]["DECOM_dt"].dt.year

measures_dict["Episodes starting per year"] = group_calculation(
    dfs["episodes"], "DECOM_YEAR", "Episodes starting per year"
)

measures_dict["Placements by year"] = group_calculation_year(
    dfs["episodes"], "DECOM_YEAR", "PLACE", "Placements by year"
)

measures_dict["CYP with episodes who have been missing"] = appears_on_both(
    dfs["episodes"], dfs["missing"], "CYP with episodes who have been missing"
)
print(measures_dict["Header by ethnicity"])
