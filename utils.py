import pandas as pd
from dateutil.relativedelta import relativedelta
from config_903 import DateCols903, EthnicSubcategories
import numpy as np


def format_dates(column):
    # Replace empty strings with NaT and fill NaN values with NaT
    column.replace(r"^\s*$", pd.NaT, regex=True)
    column = column.fillna(pd.NaT)
    try:
        column = pd.to_datetime(column, format="%d/%m/%Y")
        return column
    except:
        raise ValueError(f"Unknown date format in {column.name}, expected dd/mm/YYYY")


def calculate_age_buckets(age):
    # Used to make age buckets matching published data
    if age < 1:
        return "a) Under 1 year"
    elif age < 5:
        return "b) 1 to 4 years"
    elif age < 10:
        return "c) 5 to 9 years"
    elif age < 16:
        return "d) 10 to 16 years"
    elif age >= 16:
        return "e) 16 years and over"
    else:
        return "f) Age error"


def clean_903_table(df: pd.DataFrame, collection_end: pd.Timestamp):
    """
    Clean and transform a 903 data table by applying various data processing operations.
    Performs the following operations on the input dataframe:
    - Removes the 'index' column if present
    - Converts date columns to datetime format based on DateCols903 configuration
    - Maps ethnic categories to their main ethnicity groups
    - Calculates age and age bucket classifications based on date of birth
    Args:
        df (pd.DataFrame): The input dataframe containing raw 903 table data.
        collection_end (pd.Timestamp): The reference date used for age calculations.
    Returns:
        pd.DataFrame: A cleaned dataframe with additional processed columns including:
            - *_dt columns for converted date columns
            - ETHNICITY: Main ethnicity group mappings
            - AGE: Calculated age in years
            - AGE_BUCKETS: Age category classification

    """
    clean_df = df.copy()

    # Drop index column if it exists
    if "index" in clean_df.columns:
        clean_df.drop("index", axis=1, inplace=True)

    # Convert date cols to datetime
    for column in clean_df.columns:
        if column in DateCols903.cols.value:
            clean_df[f"{column}_dt"] = format_dates(clean_df[column])

    # Add ethnicity to main groups col
    if "ETHNIC" in clean_df.columns:
        clean_df["ETHNICITY"] = clean_df["ETHNIC"].apply(
            lambda ethnicity: EthnicSubcategories[ethnicity].value
        )

    # Create age and age buckets cols
    if "DOB_dt" in clean_df.columns:
        clean_df["AGE"] = clean_df["DOB_dt"].apply(
            lambda dob: relativedelta(dt1=collection_end, dt2=dob).normalized().years
        )
        clean_df["AGE_BUCKETS"] = clean_df["AGE"].apply(calculate_age_buckets)

    return clean_df


def group_calculation(df, col_to_group, measure_name):
    df = df.copy()
    grouped = df.groupby([col_to_group]).size()
    grouped = grouped.to_frame("Count").reset_index()
    grouped = grouped.rename(columns={col_to_group: "Value"})

    grouped["Percentage"] = (grouped["Count"] / grouped["Count"].sum()) * 100

    grouped["Measure"] = measure_name

    grouped_ordered = grouped[["Measure", "Value", "Count", "Percentage"]]

    return grouped_ordered


def time_difference(start_col, end_col, business_days=False):
    if business_days:
        time_diff = np.busday_count(
            start_col.values.astype("datetime64[D]"),
            end_col.values.astype("datetime64[D]"),
        )
    else:
        time_diff = end_col - start_col
        time_diff = time_diff / pd.Timedelta(days=1)

    return time_diff.astype("int")


def multiples_same_event(df, event_name):
    df = df.copy()
    multiples = df.groupby(["CHILD"]).size().to_frame("Number of events").reset_index()
    multiples = (
        multiples.groupby("Number of events")
        .size()
        .to_frame("Children with number of events")
        .reset_index()
    )
    multiples["Event type"] = event_name
    multiples = multiples[
        ["Event type", "Number of events", "Children with number of events"]
    ]
    return multiples


def group_calculation_year(df, year_col, col_to_group, measure_name):
    df = df.copy()
    grouped = df.groupby([year_col, col_to_group])
    grouped = grouped.size().to_frame("Count").reset_index()
    grouped = grouped.rename(columns={col_to_group: "Value"})

    grouped["Percentage by year"] = grouped.apply(
        lambda row: (
            row["Count"]
            / grouped.loc[grouped[year_col] == row[year_col]].Count.sum()
            * 100
        ),
        axis=1,
    )

    grouped["Measure"] = measure_name

    grouped = grouped[[year_col, "Measure", "Value", "Count", "Percentage by year"]]

    return grouped


def appears_on_both(df1, df2, measure_name):
    df1 = df1.drop_duplicates(subset=["CHILD"]).copy()
    df2 = df2.drop_duplicates(subset=["CHILD"]).copy()
    merged_df = df1.merge(df2, on=["CHILD"], how="inner")
    merged_df["on_both"] = "Yes"
    df = df1.merge(merged_df[["CHILD", "on_both"]], on="CHILD", how="left")
    df.fillna({"on_both": "No"}, inplace=True)
    output = group_calculation(df, "on_both", measure_name)
    return output
