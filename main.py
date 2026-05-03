import numpy as np
import Customer as CustomerModule
import Transaction as TransactionModule
import time

# Function to display a message with a typewriter effect
def display_msg(a):
    for i in a:
        print(i,end="")
        time.sleep(0.05)
    check()

msg="Hello! Welcome to Western Wholesale Pvt. ltd.\n....Presenting Our Newly Customised Menu....\nEnter the Following Number to Perform the Task Written\n1.Add New Customer\n2.Add New Transaction\n3.Search Customer\n4.Search Transaction\n5.Search Transaction Based on Customer Details\n6.Delete A Transaction\n7.Delete a Customer\n8.Exit from the Program\n9.Load Customers from CSV File\n10.To save the records in file\n11.Adding new Transactions from File\n12.Save transaction to File\n13.Display Monthly Sales and Transaction\n14.Display Monthly Sales and Transaction on the Basis of Customer Id\n15.Display Monthly Sales and Transactions on the Basis of Customer PostCode"

# Global lists to hold customers and transactions
Customer_list = []
Transaction_list = []
Customer_list_array = []
Transaction_list_array = []


# Function to check the user's menu choice and call the appropriate function
def check():
    global choice
    try:
        choice = int(input("\nEnter any number of your choice or 8 to Exit "))
    except:
        print("Only integers are allowed")
        check()
    match choice:
        case 1:
            CustomerModule.AddNewCustomer(Customer_list)
            #Customer_list_array = CustomerModule.ConvertToNumpyArray(Customer_list)
            check()
        case 2:
            TransactionModule.AddNewTransaction(Customer_list, Transaction_list)
            #Transaction_list_array = TransactionModule.ConvertToNumpyArray(Transaction_list)
            check()
        case 3:
            CustomerModule.SearchCustomer(Customer_list)
            check()
        case 4:
            TransactionModule.SearchTransactions(Transaction_list)
            check()
        case 5:
            TransactionModule.SearchTransactionsByCustomerId(Customer_list, Transaction_list)
            check()
        case 6:
            TransactionModule.RemoveTransaction(Transaction_list)
            #Transaction_list_array = TransactionModule.ConvertToNumpyArray(Transaction_list)
            check()
        case 7:
            CustomerModule.DeleteCustomer(Customer_list, Transaction_list)
            try:
                Customer_list_array = CustomerModule.ConvertToNumpyArray(Customer_list)
                Transaction_list_array = TransactionModule.ConvertToNumpyArray(Transaction_list)
            except:
                print("No Data is Left to Be Converted")
            finally:
                check()
        case 8:
            print("Thanks for using Our Service!!! please Visit Again :) ")
            exit()
        case 9:
            CustomerModule.LoadCustomers()
           # Customer_list_array = CustomerModule.ConvertToNumpyArray(Customer_list)
            check()
        case 10:
            CustomerModule.SaveCustomersToFile()
            check()
        case 11:
            TransactionModule.TransactionsFromFile()
           # Transaction_list_array = TransactionModule.ConvertToNumpyArray(Transaction_list)
            check()
        case 12:
            TransactionModule.SaveTransactionsToCSV()
            check()
        case 13:
            TransactionModule.DisplayMonthlySalesAndTransactions(Transaction_list)
            check()
        case 14:
            Id=int(input("Enter the Id"))
            TransactionModule.DisplayCustomerMonthlySalesAndTransactions(Transaction_list,Id)
            check()
        case 15:
            TransactionModule.ShowPostcodeMonthlySalesAndTransactions(Customer_list)
            check()

# Function to convert a list of dictionaries to a numpy array for better data handling
def ND_array(x):
    y = x[0].keys()
    values_list = [[a[i] for i in y] for a in x]
    array = np.array(values_list)
    return array

# Entry point: Display the welcome message and show the menu
display_msg(msg)
check()
