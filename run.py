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

# sales = SHEET.worksheet('sales')
# data = sales.get_all_values()
# print(data)
def get_sales_data():   
    ''' Get sales figures input from the user, the loop will repeatedly 
    ask the user to input the correct data string of 6 values '''
    while True:
        print('Please enter sales data from the last market.')
        print('Data should be six numbers, separated by commas.')
        print('Example: 10,20,30,40,50,70\n')

        data_str = input('Please enter your data here:\n')

        sales_data = data_str.split(',')

        if validate_data(sales_data):
            print('Data is Valid!')
            break

    return sales_data

def validate_data(values):
    '''Inside the try, converts all string values into integers. 
       Raises ValueError if striings cannot be converted into int,
       or if there aren't exactly six values.
     '''
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                  f'Exactly 6 values required, you provided {len(values)}'
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False   

    return True

# def update_sales_worksheet(data):
#     ''' Updates sales worksheet ,add 
#     new row with the list data provided'''
#     print('Updating sales worksheet...\n')
#     sales_worksheet = SHEET.worksheet('sales')
#     sales_worksheet.append_row(data)
#     print('Sales worksheet updated successfully.\n') 

def calculate_surplus_data(sales_row):
    ''' Compare sales with stock and calculate the surplus for each item type
    . The surplus defined as the sales figure subtracted from the stock: 
    - Positive surplus indicates waste
    - Negative surplus indcates extra made when stock was sold out.''' 
    print('Calculating surplus data...\n')  
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock,sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data   

# def update_surplus_worksheet(excess):
#     ''' Updates surplus worksheet ,add 
#     new row with the list data provided'''
#     print('Updating surplus data...\n')  
#     surplus_data = SHEET.worksheet('surplus')
#     update_surplus_row = surplus_data.append_row(excess)

def update_worksheet(data,worksheet):
    ''' Receives a list of integers to be inserted into a worksheet
        update the relevant worksheet with the data provided'''
    print(f'Updating {worksheet} worksheet...\n')  
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet} udpated successfully\n')

def get_last_5_entries_sales():
    ''' 
    Collects collumns of data from sales worksheet, collecting
    the last 5 entries for each sandwiche  and returns the data 
    as a list of lists
    '''
    sales = SHEET.worksheet('sales')

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    ''' 
    Calculate the average stock for each item type, adding 10%
    '''
    print('Calculating stock data...\n')
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():
    ''' Run all program functions'''

    data = get_sales_data()    
    sales_data = [int(num) for num in data]   
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, 'stock')

print('Welcome to Love sandwiches Data Automation')
main()
