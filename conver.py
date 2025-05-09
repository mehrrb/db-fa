import pandas as pd

def convert_excel_to_csv():
    try:
        # Reading Excel file
        df = pd.read_excel('test.xlsx')
        
        # Saving as CSV
        df.to_csv('test.csv', index=False, encoding='utf-8')
        print("File successfully converted to CSV!")
        
    except Exception as e:
        print(f"Error converting file: {str(e)}")

if __name__ == "__main__":
    convert_excel_to_csv()