import pandas as pd
from pathlib import Path
import numpy as np

# --------------------------------------------------
# Project paths
# --------------------------------------------------
import warnings

warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    module="openpyxl"
)
project_root = Path(__file__).resolve().parent.parent

metadata_file = (
    project_root
    / "metadata"
    / "processed_files.txt"
)

output_file = (
    project_root
    / "data"
    / "processed"
    / "scada_data.parquet"
)

# --------------------------------------------------
# Source folder containing monthly folders
# --------------------------------------------------

source_folder = Path(
    r"D:\Neha Outlook\JGEL\Parikshit Paliwal - LOGs\LTT LOGs\FY 2026-27"
)

# --------------------------------------------------
# Read already processed files
# --------------------------------------------------

if metadata_file.exists():
    with open(metadata_file, "r") as f:
        processed_files = set(
            line.strip()
            for line in f
        )
else:
    processed_files = set()

# --------------------------------------------------
# Find all Excel files
# --------------------------------------------------

all_excel_files = list(
    source_folder.rglob("*.xlsx")
)

# --------------------------------------------------
# Keep only new files
# --------------------------------------------------

excel_files = [
    file
    for file in all_excel_files
    if str(file) not in processed_files
]

print(f"{len(excel_files)} new files found")

# --------------------------------------------------
# Exit if no new files
# --------------------------------------------------

if len(excel_files) == 0:
    print("No new files found.")
    exit()

# --------------------------------------------------
# Read files
# --------------------------------------------------

all_data = []

for file in excel_files:

    try:

        df = pd.read_excel(file)

        df["File_Name"] = file.name

        all_data.append(df)

        print(f"Loaded {file.name}")

    except Exception as e:

        print(f"Error reading {file.name}: {e}")

# --------------------------------------------------
# Combine new data
# --------------------------------------------------

combined_df = pd.concat(
    all_data,
    ignore_index=True
)

# --------------------------------------------------
# Convert Timestamp
# --------------------------------------------------

combined_df["Timestamp"] = pd.to_datetime(
    combined_df["Timestamp"],
    errors="coerce"
)
combined_df = combined_df.dropna(
    subset=["Timestamp"]
)

# --------------------------------------------------
# Extract Turbine_ID
# --------------------------------------------------

combined_df["Turbine_ID"] = (
    combined_df["File_Name"]
    .str.split("_")
    .str[0]
)

# --------------------------------------------------
# Append existing parquet if present
# --------------------------------------------------

if output_file.exists():

    old_df = pd.read_parquet(output_file)

    combined_df = pd.concat(
        [old_df, combined_df],
        ignore_index=True
    )

    print("Existing parquet loaded")

# --------------------------------------------------
# Remove duplicates
# --------------------------------------------------

combined_df.drop_duplicates(
    inplace=True
)

combined_df["YearMonth"] = (combined_df["Timestamp"].dt.strftime("%Y_%m"))

print(combined_df.shape)

# --------------------------------------------------
# Save parquet
# --------------------------------------------------
combined_df.replace(["N.V.", "NV", "N/A",  "-", ""], np.nan, inplace=True)

for month in combined_df["YearMonth"].unique():

    month_df = combined_df[
        combined_df["YearMonth"] == month
    ]

    month_file = (
        project_root
        / "data"
        / "processed"
        / f"{month}.parquet"
    )

    # If month already exists, append old data
    if month_file.exists():

        old_df = pd.read_parquet(
            month_file
        )

        month_df = pd.concat(
            [old_df, month_df],
            ignore_index=True
        )

        month_df.drop_duplicates(
            inplace=True
        )

    month_df.to_parquet(
        month_file,
        index=False
    )

    print(
        f"Saved {month_file.name}"
    )

print("Parquet file updated successfully")

# --------------------------------------------------
# Update processed files list
# --------------------------------------------------

with open(metadata_file, "a") as f:

    for file in excel_files:

        f.write(str(file) + "\n")

print("Processed files list updated")
