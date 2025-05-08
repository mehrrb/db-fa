import pandas as pd

def convert_excel_to_csv():
    try:
        # خواندن فایل Excel
        df = pd.read_excel('test.xlsx')
        
        # ذخیره به صورت CSV
        df.to_csv('test.csv', index=False, encoding='utf-8')
        print("فایل با موفقیت به CSV تبدیل شد!")
        
    except Exception as e:
        print(f"خطا در تبدیل فایل: {str(e)}")

if __name__ == "__main__":
    convert_excel_to_csv()