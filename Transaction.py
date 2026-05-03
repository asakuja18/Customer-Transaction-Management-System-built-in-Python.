import csv
import os
import matplotlib.pyplot as plt
import numpy as np

# We created 'Customer' as a separate module for handling customer-related functionalities.
import Customer as Cust

# Transactions data storage and conversion to numpy array.
TransactionsData = []
TransactionsDataArray = []

def ConvertToNumpyArray(data):
    # Converts list of dictionaries to a numpy array for processing.
    keys = data[0].keys()
    valuesList = [[a[i] for i in keys] for a in data]
    array = np.array(valuesList)
    return array

def AddNewTransaction(CustomersList,TransactionsList):

    def GenerateTransactionId():
        if TransactionsList:
            return TransactionsList[-1]["Transaction Id"] + 1
        else:
            return 1

    def NewTransaction(customerId, date, category, sales):
        customer = next((cust for cust in CustomersList if cust['Customer Id'] == customerId), None)
        if customer:
            transactionId = GenerateTransactionId()
            transaction = {
                "Date": date,
                'Transaction Id': transactionId,
                "Customer Id": customerId,
                "Sales": sales,
                "Category ": category
            }
            TransactionsList.append(transaction)
            TransactionsData.append(transaction)
            print(f"Transaction ID {transactionId} generated for Customer ID {customerId}")
        else:
            return None

    customerId = int(input("Enter the Customer ID"))
    date = input("Enter the Date")
    sales = int(input("Enter the Sales"))
    category = input("Enter the Category")
    NewTransaction(customerId, date,category,sales)
    print(TransactionsList)

def SearchTransactions(TransactionsList):
    outputSales = []

    def FindString1(x):
        for transaction in TransactionsList:
            if (x.lower() in str(transaction["Transaction Id"]).lower() or
               x.lower() in str(transaction["Customer Id"]).lower() or
               x.lower() in transaction["Date"].lower() or
               x.lower() in str(transaction["Sales"]).lower() or
               x.lower() in transaction["Category "].lower()):
                outputSales.append(transaction)
            else:
                continue

    stringToSearch = input("Enter the String")
    FindString1(stringToSearch)
    print(outputSales)

def SearchTransactionsByCustomerId(CustomersList, TransactionsList):
    outputSales = []
    outputTransactions = []

    def FindString2(x):
        for customer in CustomersList:
            if (x.lower() in str(customer["Customer Id"]).lower() or
               x.lower() in customer["Customer Name"].lower() or
               x.lower() in customer["Customer Code"].lower() or
               x.lower() in customer["Customer Phone"].lower()):
                outputSales.append(customer["Customer Id"])
        for transaction in TransactionsList:
            if transaction["Customer Id"] in outputSales:
                outputTransactions.append(transaction)

    stringToSearch = input("Enter the String")
    FindString2(stringToSearch)
    print(outputTransactions)

def RemoveTransaction(TransactionsList):
    newTransactionsList = []

    def Delete(x):
        for transaction in TransactionsList:
            if int(transaction["Transaction Id"]) == int(x):
                continue
            else:
                newTransactionsList.append(transaction)

    transactionId = input('Enter the Transaction Id to be Removed')
    Delete(transactionId)
    print("Transaction Successfully Removed")
    print(newTransactionsList)

def transaction_from_file():
    def NewTransaction(customerId, date, category, sales, transactionId):
        transaction = {
            'Transaction Id': transactionId,
            "Customer Id": customerId,
            "Date": date,
            "Sales": sales,
            "Category ": category
        }
        TransactionsData.append(transaction)
        print(f"Transaction ID {transactionId} generated for Customer ID {customerId}")
        print(f"Final Transaction list: {TransactionsData}")

    path = input("Enter the Path location of the File: ")
    try:
        with open(path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactionId = row["Transaction Id"]
                customerId = int(row['Customer Id'])
                date = row['Date']
                sales = int(row["Sales"])
                category = row['Category']

                existingCustomer = next((cust for cust in TransactionsData if int(cust['Customer Id']) == customerId), None)

                if existingCustomer:
                    newTransactionId = int(max(TransactionsData, key=lambda k: int(k['Transaction Id']))['Transaction Id']) + 1
                    NewTransaction(customerId, date, category, sales, newTransactionId)
                else:
                    NewTransaction(customerId, date, category, sales, transactionId)
    except:
        print("Error Occurred. Please check the file path and format.")

def SaveTransactionsToCSV():
    try:
        path = input("Enter the File Path")
        if os.path.exists(path):
            print("Warning: Content of the file would be lost. Continue?")
            choice = int(input("Press 1 for Creating New File\n2. for Overwriting the File\n3. Cancellation of Operation"))
            if choice == 1:
                path2 = input("Enter the Location in which you want the New File to be Saved")
                path = path2
                mode = "w"
            elif choice == 2:
                mode = "w"
            else:
                print("Operation Aborted")
                return
        else:
            mode = "w"
        with open(path, mode, newline="") as file:
            columns = ["Transaction Id", "Customer Id", "Date", "Sales", "Category "]
            writer = csv.DictWriter(file, fieldnames=columns)

            if mode == "w":
                writer.writeheader()

            for transaction in TransactionsData:
                writer.writerow(transaction)

        print("File Created")
    except:
        print("Error Occurred. Please check the file path and format.")


# Plots and displays the monthly sales and transaction counts from a given transactions list.
def DisplayMonthlySalesAndTransactions(transactions):
    monthlySales = {}
    monthlyTransactions = {}

    for transaction in transactions:
        date = transaction['Date']
        sales = transaction['Sales']
        month = date.split('-')[1]

        if month not in monthlySales:
            monthlySales[month] = 0
            monthlyTransactions[month] = 0

        monthlySales[month] += float(sales)
        monthlyTransactions[month] += 1

    months = list(monthlySales.keys())
    salesValues = list(monthlySales.values())
    transactionNumbers = list(monthlyTransactions.values())

    plt.figure(figsize=(10, 6))
    plt.plot(months, salesValues, marker='o', label='Monthly Sales')
    plt.plot(months, transactionNumbers, marker='o', label='Monthly Transactions')
    plt.xlabel('Month')
    plt.ylabel('Value')
    plt.title('Monthly Sales and Transaction Numbers')
    plt.legend()
    plt.grid(True)
    plt.show()

def ShowMonthlySalesAndTransactions():
    DisplayMonthlySalesAndTransactions(TransactionsData)

def DisplayCustomerMonthlySalesAndTransactions(transactions, customerId):
    monthlySales = {}
    monthlyTransactions = {}
    for transaction in transactions:
        if transaction['Customer Id'] == customerId:
            date = transaction['Date']
            sales = transaction['Sales']
            month = date.split('-')[1]

            if month not in monthlySales:
                monthlySales[month] = 0
                monthlyTransactions[month] = 0

            monthlySales[month] += float(sales)
            monthlyTransactions[month] += 1

    months = list(monthlySales.keys())
    salesValues = list(monthlySales.values())
    transactionNumbers = list(monthlyTransactions.values())

    plt.figure(figsize=(10, 10))
    plt.plot(months, salesValues, marker='o', label='Monthly Sales')
    plt.plot(months, transactionNumbers, marker='o', label='Monthly Transactions')
    plt.xlabel('Month')
    plt.ylabel('Monthly Sales')
    plt.title(f'Monthly Sales and Transactions for Customer ID: {customerId}')
    plt.legend()
    plt.grid(True)
    plt.show()

def ShowCustomerMonthlySalesAndTransactions():
    # User input to retrieve customer ID and call the display function for monthly sales and transactions.
    customerId = int(input("Enter Customer ID: "))
    DisplayCustomerMonthlySalesAndTransactions(TransactionsData, customerId)

def DisplayPostcodeMonthlySalesAndTransactions(postcode,CustomerList):
    monthlySales = {}
    monthlyTransactions = {}

    def DisplayCustomerPostcodeMonthlySalesAndTransactions(transactions, customerId):
        # Plots and displays monthly sales and transactions for all customers in a specified postcode.
        monthlySales = {}
        monthlyTransactions = {}

        for transaction in transactions:
            if transaction['Customer Id'] == customerId:
                date = transaction['Date']
                sales = transaction['Sales']
                month = date.split('-')[1]

                if month not in monthlySales:
                    monthlySales[month] = 0
                    monthlyTransactions[month] = 0

                monthlySales[month] += float(sales)
                monthlyTransactions[month] += 1

        months = list(monthlySales.keys())
        salesValues = list(monthlySales.values())
        transactionNumbers = list(monthlyTransactions.values())

        plt.figure(figsize=(10, 10))
        plt.plot(months, salesValues, marker='o', label='Monthly Sales')
        plt.plot(months, transactionNumbers, marker='o', label='Monthly Transactions')
        plt.xlabel('Month')
        plt.ylabel('Sales Value')
        plt.title('Monthly Sales and Transactions for Customer ID: {}'.format(customerId))
        plt.legend()
        plt.show()

    for customer in CustomerList:
        if customer['Customer Code'] == postcode:
            DisplayCustomerPostcodeMonthlySalesAndTransactions(TransactionsData, customer['Customer Id'])
        else:
            print("No such Customer Code Found")

def ShowPostcodeMonthlySalesAndTransactions(CustomerList):
# User input to retrieve postcode and call the display function for monthly sales and transactions per postcode.
    postCode = input("Enter Post Code")
    DisplayPostcodeMonthlySalesAndTransactions(postCode,CustomerList)
