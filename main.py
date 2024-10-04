import tabula
import pandas as pd
import os

# Specify the path to the PDF file
pdf_file_path = 'C:/Users/yadne/OneDrive/Desktop/Sr.pdf'  # Correct file path (no URL-style path)

# Check if the PDF file exists
if os.path.exists(pdf_file_path):
    print("File found!")
else:
    print("File not found, please check the path.")
    exit()

# Extract tables from the PDF using Tabula
# pages='all' extracts from all pages; specify a page number if needed
tables = tabula.read_pdf(pdf_file_path, pages='all', multiple_tables=True)

# If tables were found
if tables:
    for index, table in enumerate(tables):
        # Define the output CSV file path
        output_csv_path = f'table_{index + 1}.csv'

        # Save the table as a CSV file
        table.to_csv(output_csv_path, index=False)

        # Notify the user
        print(f"Table {index + 1} has been saved to {output_csv_path}")
else:
    print("No tables found in the PDF.")
