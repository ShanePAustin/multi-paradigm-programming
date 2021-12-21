#A Procedural Python program for a basic shop that reads in stock and orders from csv
#Multi Paradigm Programming.
#GMIT Data Analytics 2021
#Author: Shane Austin

from dataclasses import dataclass, field
from typing import List
import csv


###########################################################################
#establishing the data classes
@dataclass
class Product:
    name: str
    price: float = 0.0

@dataclass
class ProductStock:
    product: Product
    quantity: int

@dataclass
class Shop:
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)

@dataclass
class Customer:
    name: str = ""
    budget: float = 0.0
    shoppingList: List[ProductStock] = field(default_factory=list)

#########################################################################
#Prints the name and price of a product
def printProduct(p):

    print("\nPRODUCT NAME: {} \nPRODUCT PRICE: €{}".format(p.name, p.price))


#Takes in a customer shopping list and prints:
#Customer Name and Budget
#What they have ordered
def printCustomer(c,s):

    print("------------------------------")
    print("CUSTOMER NAME: {} \nCUSTOMER BUDGET €{}".format(c.name,c.budget))
    print("------------------------------")
    

    totalBill = 0

    for item in c.shoppingList:        
        #Check if item is in stock and inform if not
        if checkOrder(s, item.product.name) == None:
            print("********************")
            print("WE DO NOT SELL {}".format(item.product.name))
            print("------------------------------")
        else:
            #if in stock process the order
            orderedProduct = checkOrder(s, item.product.name).product
            printProduct(orderedProduct)
            #Print the name and quantity of ordered item
            print("\nYou have ordered {} {}".format(int(item.quantity),item.product.name))        

            cost = item.quantity * orderedProduct.price
            print("The cost to {} will be €{:.2f}".format(c.name, cost))
            print("------------------------------")
            
            totalBill += cost

            #Print the price of ordered items
            print("Total Cost will be €{:.2f}".format(totalBill))
            print("------------------------------")

#Takes in Shop stock and prints what's available
def printShop(s):

    print('Shop has {:.2f} in cash'.format(s.cash))

    #loop through stock
    for item in s.stock:

        #print stock item and quantity available
		#calls on printProduct()
        printProduct(item.product)
        print("The Shop has {} of the above".format(int(item.quantity)))
        print("------------------------------")

#function to check stock against order item
def checkOrder(s, name):
        for i in s.stock:
        # for each ProductStock compare product.name with searched string 
            if i.product.name == name:
                # if found return ProductStock
                return i
        # if not found return None
        return None

#reads in the stock.csv
def createAndStockShop():
    s = Shop()

    #open the csv and exit if file does not exist
    with open ('../stock.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')

        #read csv first line "cash"
        first_row=next(csv_reader)
        s.cash=(float(first_row[0]))

        #add the stock looping through the csv
        for row in csv_reader:
            p = Product(row[0], float(row[1]))
            ps = ProductStock(p, float(row[2]))
            s.stock.append(ps)

    return s

#Read in customer specific file path
def custOrder(path):

    with open (path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')

        #Read in the customer "name" and "budget" from the .csv file
        first_row=next(csv_reader)
        order = Customer(first_row[0], float(first_row[1]))

        #Read in the "product name" and "quantity" ordered
        for row in csv_reader:
            n = row[0]
            q = float(row[1])
            p = Product(n)
            ps = ProductStock(p, q)
            order.shoppingList.append(ps)

    return order

#Process the customer order
#Update the shop stock and shop cash
def checkOut(c, s):

    print("\n------------------------------")
    print("Check Out")
    print("*************")

    print("Order Summary\n------------------------------")

    
    cash = float(s.cash)
    budget = float(c.budget)
    startBudget = budget
    totalBill = 0

    for item in c.shoppingList:

        # check if customer's product exists in shop stock 
        stockCheck = checkOrder(s, item.product.name)
        
        # if product not found in shop stock 
        if stockCheck == None:
            print("SORRY WE DO NOT HAVE ANY {} IN THIS SHOP".format (item.product.name))
        else:
            # calculates order value 
            itemPrice = item.quantity * stockCheck.product.price

            # checks if there is enough product in the store
            if item.quantity <= stockCheck.quantity:
                print("This shop has {} {} for €{}" .format(int(item.quantity),item.product.name,stockCheck.product.price)) 
                
                # checks if the client has a sufficient budget to complete the transaction
                if budget >= itemPrice:

                    # Updates shop and customer budget
                    stockCheck.quantity -= item.quantity
                    cash += itemPrice
                    budget -= itemPrice
                    totalBill += itemPrice
   
                elif budget < itemPrice:
                    print("SORRY YOU CANNOT AFFORD A  {} IT WILL BE REMOVER FROM THE BASKET".format(item.product.name))
                    continue

            else:
                print("This shop has {} but stock is low and we only have {} of the {} that you wanted\n".format(item.product.name, int(stockCheck.quantity),int(item.quantity)))
                print("We will add what we have to your order: {} {}\n".format(int(stockCheck.quantity), item.product.name))

                # Updates shop and customer budget
                cash += itemPrice
                budget -= itemPrice
                totalBill += (stockCheck.quantity * stockCheck.product.price)
                stockCheck.quantity = 0
 

    if totalBill < budget:
        print("\nYour total bill is €{:.2f} budget is €{:.2f}\n".format(totalBill, startBudget))
        print("You will have €{:.2f} left in your budget\n\n".format(startBudget - totalBill))
    
    #update values
    s.cash = cash
    c.budget = budget


    return

#Live Shop to create a temp csv for that order from Account name path
def liveShop(path,custName):
    print("\nLive Shop")
    print("*************")

    with open (path, 'w', newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter = ',')

        #Enter the budget customer has for this transaction
        custBudget = int(input("\nPlease Enter Your Budget: €"))
        c = (custName, custBudget)

        csv_writer.writerow(c)
    
        continueShopping = 0

        #Keep adding items to the shop until exit command
        while continueShopping != 'n':

            prodName = input("What would you like to order?:")
            
            prodQuantity = int(input("How many would you like?: #"))

            c = (prodName, prodQuantity)

            csv_writer.writerow(c)

            continueShopping = input("y to continue shopping or n to checkout: ")

            #Break the loop and close the csv
            if continueShopping == 'n':
                break                

        csv_file.close()

        print("Going to Check Out")
        print("------------------------------")

#Function to update the stock csv with new figures
def updateShop(s):

    with open ('../stock.csv', 'w', newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter = ',')

        #assign rounded cash value to a list and write to the csv
        cash = []
        cashRounded = round(s.cash, 2)
        cash.append(cashRounded)
        csv_writer.writerow(cash)

        #loop through the stock to update the csv
        for item in s.stock:
            newStock = (item.product.name, item.product.price, int(item.quantity))
            csv_writer.writerow(newStock)

#Function to update the customer budget
def updateCustomer(c, path):

    with open (path, 'w', newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter = ',')


        #Write the first line of the csv with new budget
        custUpdate = (c.name, round(c.budget,2))
        csv_writer.writerow(custUpdate)

        #rewrite the original customer order
        for item in c.shoppingList:
            newStock = (item.product.name, int(item.quantity))
            csv_writer.writerow(newStock)

#Options menu for the application
#Can run order from csv
#order from live shop
#Print the current stock
def main():

    #list of current viable users
    accounts = ("Anna", "Dominic", "Mary", "Shane")

    while True:

        print ("Please choose an option (0 to Exit)")
        print ("Select (1): to load your existing order: ")
        print ("Select (2): to order from the store: ")
        print ("Select (3): to view what's in stock: ")
        
        choice = input("Choice:")
  
        #option 1 Shop form csv
        if choice=="1": 

            #Letting user know the account conditions
            print("\nWe have 4 accounts currently:")
            print("Anna:    (Who likes to order what we have)")
            print("Dominic: (Who orders items we don't stock)")
            print("Mary:    (Who likes to order expensive items)")
            print("Shane:   (Who likes to order too much)")

            custName = input("\nAccount Name:")

            #continue if account name is in the list
            if custName in accounts:
            
                print("------------------------------")
                #set customer file path
                path = "../Customer/{}/order.csv".format(custName)

                #process the order, checkout
                #and update the CSVs
                order = custOrder(path)
                printCustomer(order, s)
                checkOut(order, s)
                updateShop(s) 
                updateCustomer(order, path)


            else:
                print("UNKNOWN ACCOUNT!")
                main()    

        #option 2 live order
        elif choice=="2":

            print("\nWe have 4 accounts currently:")
            print("Anna, Dominic, Mary and Shane")

            custName = input("\nAccount Name:")

            if custName in accounts:        

                path = "../Customer/{}/liveOrder.csv".format(custName)
                print("What would you like to buy\n")

                #print current stock
                printShop(s) 
                #runn live shop functio
                liveShop(path,custName)

                #process the order, checkout
                #and update the shop CSV
                order= custOrder(path)
                printCustomer(order, s)           
                checkOut(order, s)
                updateShop(s)
            
            print("UNKNOWN ACCOUNT!")                
            main()

        #Option 3 show stock
        elif choice=="3":
            printShop(s)

        elif choice=="0":
            print("Thank you for shopping with Python")
            exit()

        else:
            print("Please choose an option from the menu")
            main() 
            

if __name__ == "__main__":
    s = createAndStockShop()
    main()
