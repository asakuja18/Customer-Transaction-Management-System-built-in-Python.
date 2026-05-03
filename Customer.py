import csv
import os
import numpy as np

# Lists to store customer data and the corresponding numpy array for efficient data manipulation
CustomerData = []
CustomerDataArray = []

# Function to convert a list of dictionaries into a numpy array
def ConvertToNumpyArray(data):
    keys = data[0].keys()
    valuesList = [[a[i] for i in keys] for a in data]
    array = np.array(valuesList)
    return array

# Function to add a new customer to the Customer list
def AddNewCustomer(CustomerList):
    def GenerateCustomerId():
        if CustomerList:
            return CustomerList[-1]['Customer Id'] + 1
        else:
            return 1

    def NewCustomer(customerName, customerCode="", customerPhone=""):
        customerId = GenerateCustomerId()
        customerDetail = {
            "Customer Id": customerId,
            "Customer Name": customerName,
            "Customer Code": customerCode,
            "Customer Phone": customerPhone
        }
        CustomerList.append(customerDetail)
        CustomerData.append(customerDetail)
        CustomerDataArray = ConvertToNumpyArray(CustomerData)
        print(f"The New Customer ID Generated is {customerId}")

    # Collect customer details from the user
    name = input("Enter the Name(Mandatory)")
    code = input("Enter the PostCode(Optional)")
    phoneNo = input("Enter the Phone Number(Optional)")
    NewCustomer(name, code, phoneNo)
    print(CustomerList)

# Function to search for customers based on a search string
def SearchCustomer(CustomerList):
    output = []

    def FindString(x):
        for customer in CustomerList:
            match (x.lower() in str(customer["Customer Id"]).lower() or
               x.lower() in customer["Customer Name"].lower() or
               x.lower() in customer["Customer Code"].lower() or
               x.lower() in customer["Customer Phone"].lower()):
                case 1:output.append(customer)
                case 0:continue

    stringToSearch = input("Enter the String")
    FindString(stringToSearch)
    print(output)

# Function to delete a customer and their associated transactions
def DeleteCustomer(CustomerList, TransactionList):
    newCustomerList = []
    newTransactionList = []

    def Deletion(x):
        for customer in CustomerList:
            match customer["Customer Id"] == x:
                case 1:continue
                case 0:newCustomerList.append(customer)
        for transaction in TransactionList:
            for customer in CustomerList:
                match int(transaction['Transaction Id']) == int(customer["Customer Id"]):
                    case 1:newTransactionList.append(transaction)
                break

    customerId = int(input('Enter the Customer Id to be Removed'))
    Deletion(customerId)
    print("Customer and Following Transaction Successfully Removed")
    print("************** Updated Customer and Transaction Record **************")
    print(newCustomerList)
    CustomerData = newCustomerList
    CustomerDataArray = ConvertToNumpyArray(CustomerData)
    print(newTransactionList)

import csv

# Function to load customers from a CSV file
def LoadCustomers():
    path = input("Enter the Path of the File")
    prevId = [customer["Customer Id"] for customer in CustomerData]
    try:
        with open(path, mode='r', newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            customers = list(reader)

            for item in customers:
                match int(item['Customer Id']) not in prevId:
                    case 1:CustomerData.append(item)
                    case 0:print("Customer Already Present for id {}".format(item["Customer Id"]))
        print(CustomerData)
    except:
        print("****************************************************************\nError Occurred. Please check the file path and format.")

# Function to save customers to a CSV file
def SaveCustomersToFile():
    try:
        path = input("Enter the File Path")
        match os.path.exists(path):
            case 1:
                choice = int(input("Press 1 for Creating New File\n2. for Overwriting the File\n3. Cancellation of Operation"))
                match choice == 1:
                    case 1:
                        path2 = input("Enter the Location in which you want the New File to be Saved")
                        path = path2
                        mode = "w"
                    case 2:
                        mode = "w"
                    case 3:
                        print("Operation Aborted")
                        return
            case _:
                mode = "w"

        with open(path, mode, newline="") as file:
            columns = ["Customer Id", "Customer Name", "Customer Code", "Customer Phone"]
            writer = csv.DictWriter(file, fieldnames=columns)

            if mode == "w":
                writer.writeheader()

            for customer in CustomerData:
                writer.writerow(customer)

        print("File Created")
        CustomerDataArray = ConvertToNumpyArray(CustomerData)
    except:
        print("*****************************************************************\nError Occurred. Please check the file path and format.")
