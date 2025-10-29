import pandas as pd
import os

# Path to the downloaded dataset
dataset_path = r"C:\Users\jeswi\.cache\kagglehub\datasets\mehmettahiraslan\customer-shopping-dataset\versions\2"

print(f"Dataset path: {dataset_path}\n")

# List files
print("Files in directory:")
files = os.listdir(dataset_path)
for file in files:
    print(f"  - {file}")

# Find and load CSV file
csv_files = [f for f in files if f.endswith('.csv')]
if csv_files:
    csv_path = os.path.join(dataset_path, csv_files[0])
    print(f"\nLoading: {csv_files[0]}")
    
    df = pd.read_csv(csv_path)
    
    print(f"\nDataset Shape: {df.shape} (rows, columns)")
    print(f"\nColumns: {df.columns.tolist()}")
    print(f"\nData Types:\n{df.dtypes}")
    print(f"\nFirst 5 rows:\n{df.head()}")
    print(f"\nBasic Statistics:\n{df.describe()}")
    print(f"\nMissing Values:\n{df.isnull().sum()}")
    
    # Check unique values for categorical columns
    print(f"\nUnique values per column:")
    for col in df.columns:
        if df[col].dtype == 'object':
            print(f"  {col}: {df[col].nunique()} unique values")
            if df[col].nunique() < 20:
                print(f"    Values: {df[col].unique()}")
    
    # Save a local copy
    df.to_csv("customer_shopping_data.csv", index=False)
    print(f"\n✓ Data saved to: customer_shopping_data.csv")
else:
    print("No CSV files found!")

