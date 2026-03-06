import pandas as pd
from dateutil.relativedelta import relativedelta
from config_903 import DateCols903, EthnicSubcategories

def format_dates(column):
    # Replace empty strings with NaT and fill NaN values with NaT
    column.replace(r"^\s*$", pd.NaT, regex=True)
    column=column.fillna(pd.NaT)
    try:
        column = pd.to_datetime(column, format="%d/%m/%Y")
        return column
    except:
        raise ValueError(
            f"Unknown date format in {column.name}, expected dd/mm/YYYY"
        )

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
        clean_df["AGE_BUCKETS"] = clean_df['AGE'].apply(calculate_age_buckets)

    return clean_df