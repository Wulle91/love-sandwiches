# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures inpit form the user
    Run a while loop to collect a valid string of data from user via the terminal, 
    witch has to be a string of 6 numbers separated by commas. The loop will 
    repeatedly request data until it is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10, 20, 30, 40, 50, 60\n")
        
        data_str = input("Enter your data here: ")
        
        sales_data = data_str.split(',')
        
        if validate_data(sales_data):
            print('Data is valid!')
            break
    return sales_data

def validate_data(values):
    """
    Inside the try, converts all strins into integers.
    Raises ValueError if strings cannot be converten into int, 
    or if there aren't exactly 6 values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(f"Exactly 6 values required, you provided {len(values)}")
    except ValueError as e:
        print(f'Invalid data {e} please try again.\n')
        return False
    return True


def update_worksheet(data, worksheet):
    """
    Recives a list if integers to be inserted intp a worksheet
    Update the relevant worksheet with data provided
    """
    print(f'Calculate {worksheet} worksheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet} worksheet updated successfully.\n')
    
    
def calculate_sulpurs_data(sales_row):
    """
    Compare sales with stocks and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock_
     - Positve surplus indicates waste
     - Negatuve surplus indicates extra made when stock was sold out.
    """
    print('calculatind surplus data...\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data
   
def get_last_5_enteries_sales():
    """
    Collects collumns of data frpm sales worksheet, collesting the last 5 
    enteries for each sandwich and returns the data as a list of lists 
    """
    sales = SHEET.worksheet('sales')
    
    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)[-5:]
        columns.append(column)
    pprint(columns)
   
def main():    
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_sulpurs_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    
print('Welcome to Love Sandiches Data Automation')
#main()
get_last_5_enteries_sales()