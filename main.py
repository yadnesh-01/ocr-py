import cv2
import numpy as np
import pandas as pd
import os
import pytesseract
import tabula
import datetime

# Specify the path to the PDF or image document
file_path = 'C:/Users/yadne/OneDrive/Desktop/try.png'  # Change this to your desired input file path


# Function to extract text using Tesseract
def extract_text(image):
    return pytesseract.image_to_string(image)


# Function to detect and extract tables from an image
def extract_table(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))

    horizontal_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel)
    vertical_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel)
    table_mask = cv2.add(horizontal_lines, vertical_lines)

    contours, _ = cv2.findContours(table_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    table_data = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cell = image[y:y + h, x:x + w]
        cell_text = pytesseract.image_to_string(cell, config='--psm 7').strip()

        row_index = len(table_data) - 1
        if row_index < 0 or x < table_data[row_index][-1][0]:
            table_data.append([])
        table_data[-1].append((x, cell_text))

    sorted_table_data = []
    for row in table_data:
        sorted_row = [text for _, text in sorted(row, key=lambda x: x[0])]
        sorted_table_data.append(sorted_row)

    return sorted_table_data


# Function to generate a unique filename
def generate_unique_filename(base_filename):
    if not os.path.exists(base_filename):
        return base_filename
    else:
        # Get the file name and extension
        name, ext = os.path.splitext(base_filename)
        # Append timestamp or incrementing number to create a unique filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{name}_{timestamp}{ext}"
        return unique_filename


# Function to save extracted data to CSV
def save_to_csv(table_data, text_data):
    base_filename = 'extracted_data.csv'
    unique_filename = generate_unique_filename(base_filename)

    df_table = pd.DataFrame(table_data)
    df_text = pd.DataFrame([{'Extracted Text': text_data}])
    result = pd.concat([df_text, df_table], ignore_index=True)

    result.to_csv(unique_filename, index=False)
    print(f"Data saved to {unique_filename}")


# Function to extract tables from PDF using Tabula
def process_pdf(file_path):
    try:
        tables = tabula.read_pdf(file_path, pages='all', multiple_tables=True)

        if tables:
            for index, table in enumerate(tables):
                output_csv_path = generate_unique_filename(f'table_{index + 1}.csv')
                table.to_csv(output_csv_path, index=False)
                print(f"Table {index + 1} has been saved to {output_csv_path}")
        else:
            print("No tables found in the PDF.")
    except Exception as e:
        print(f"An error occurred while processing the PDF: {e}")


# Main processing function for documents (PDF or image)
def process_document(file_path):
    if file_path.lower().endswith('.pdf'):
        process_pdf(file_path)
    else:
        if os.path.exists(file_path):
            print("File found! Processing...")
            image = cv2.imread(file_path)
            extracted_text = extract_text(image)
            extracted_table = extract_table(image)
            save_to_csv(extracted_table, extracted_text)
        else:
            print("File not found, please check the path.")


# Check if file exists and process it
if os.path.exists(file_path):
    process_document(file_path)
else:
    print("File not found, please check the path.")
