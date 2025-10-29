"""
Setup script for Retail Sales Dashboard
This script helps download the dataset and prepare the environment
"""
import kagglehub
import pandas as pd
import os
import sys

def main():
    print("=" * 60)
    print("  Retail Sales Dashboard - Setup")
    print("=" * 60)
    print()
    
    # Check if data already exists
    if os.path.exists('customer_shopping_data.csv'):
        print("✓ Dataset already exists locally: customer_shopping_data.csv")
        df = pd.read_csv('customer_shopping_data.csv')
        print(f"  Records: {len(df):,}")
        print(f"  Columns: {len(df.columns)}")
        print()
        response = input("Do you want to re-download the dataset? (y/n): ")
        if response.lower() != 'y':
            print("\nSetup complete! Run 'streamlit run dashboard.py' to start.")
            return
    
    try:
        print("\nDownloading dataset from Kaggle...")
        print("This may take a few moments...")
        
        # Download dataset
        path = kagglehub.dataset_download("mehmettahiraslan/customer-shopping-dataset")
        print(f"✓ Downloaded to: {path}")
        
        # Find CSV file
        csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
        if not csv_files:
            print("✗ Error: No CSV file found in downloaded dataset")
            sys.exit(1)
        
        # Load and save locally
        csv_path = os.path.join(path, csv_files[0])
        df = pd.read_csv(csv_path)
        df.to_csv('customer_shopping_data.csv', index=False)
        
        print(f"\n✓ Dataset prepared successfully!")
        print(f"  File: customer_shopping_data.csv")
        print(f"  Records: {len(df):,}")
        print(f"  Columns: {len(df.columns)}")
        
        # Show column info
        print(f"\nColumns:")
        for col in df.columns:
            print(f"  - {col}")
        
        print("\n" + "=" * 60)
        print("Setup complete!")
        print("\nTo start the dashboard, run:")
        print("  streamlit run dashboard.py")
        print("\nOr on Windows, double-click:")
        print("  start_dashboard.bat")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error during setup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

