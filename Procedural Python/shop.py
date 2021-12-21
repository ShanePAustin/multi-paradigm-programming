from dataclasses import dataclass, field
from typing import List
import csv

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



def printProduct(p):

    print("\nPRODUCT NAME: {} \nPRODUCT PRICE: €{}".format(p.name, p.price))

def printCustomer(c,s):

    print("------------------------------")
    print("CUSTOMER NAME: {} \nCUSTOMER BUDGET €{}".format(c.name,c.budget))
    print("------------------------------")
    

    totalBill = 0

    for item in c.shoppingList:        

        if checkOrder(s, item.product.name) == None:
            print("********************")
            print("WE DO NOT SELL {}".format(item.product.name))
            print("------------------------------")
        else:

            orderedProduct = checkOrder(s, item.product.name).product
            printProduct(orderedProduct)
            print("\nYou have ordered {} {}".format(int(item.quantity),item.product.name))        

            cost = item.quantity * orderedProduct.price
            # print("The cost to {} will be €{:.2f}".format(c.name, cost))

            totalBill += cost

            print("Total Cost will be €{:.2f}".format(totalBill))
            print("------------------------------")

def printShop(s):

    print('Shop has {:.2f} in cash'.format(s.cash))

    for item in s.stock:
        printProduct(item.product)
        print("The Shop has {} of the above".format(int(item.quantity)))
        print("------------------------------")

def checkOrder(s, name):
        for i in s.stock:
        # for each ProductStock compare product.name with searched string 
            if i.product.name == name:
                # if found return ProductStock
                return i
        # if not found return None
        return None


def createAndStockShop():
    s = Shop()
    with open ('../stock.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')

        first_row=next(csv_reader)
        s.cash=(float(first_row[0]))
        for row in csv_reader:
            p = Product(row[0], float(row[1]))
            ps = ProductStock(p, float(row[2]))
            s.stock.append(ps)

    return s

def custOrder(path):

    with open (path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')

        first_row=next(csv_reader)
        order = Customer(first_row[0], float(first_row[1]))

        for row in csv_reader:
            n = row[0]
            q = float(row[1])
            p = Product(n)
            ps = ProductStock(p, q)
            order.shoppingList.append(ps)

    return order


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
    
    s.cash = cash
    c.budget = budget


    return


def liveShop(path,custName):
    print("\nLive Shop")
    print("*************")

    with open (path, 'w', newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter = ',')

        custBudget = int(input("\nPlease Enter Your Budget: €"))
        c = (custName, custBudget)

        csv_writer.writerow(c)
    
        continueShopping = 0

        while continueShopping != 'n':

            prodName = input("What would you like to order?:")
            
            prodQuantity = int(input("How many would you like?: #"))

            c = (prodName, prodQuantity)

            csv_writer.writerow(c)

            continueShopping = input("y to continue shopping or n to checkout: ")

            if continueShopping == 'n':
                break                

        csv_file.close()

        print("Going to Check Out")
        print("------------------------------")

def updateShop(s):

    with open ('../stock.csv', 'w', newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter = ',')


        cash = []
        cashRounded = round(s.cash, 2)
        cash.append(cashRounded)
        csv_writer.writerow(cash)

        for item in s.stock:
            newStock = (item.product.name, item.product.price, int(item.quantity))
            csv_writer.writerow(newStock)

def updateCustomer(c, path):

    with open (path, 'w', newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter = ',')



        custUpdate = (c.name, round(c.budget,2))
        csv_writer.writerow(custUpdate)

        for item in c.shoppingList:
            newStock = (item.product.name, int(item.quantity))
            csv_writer.writerow(newStock)

def main():

    accounts = ("Anna", "Dominic", "Mary", "Shane")

    while True:

        print ("Please choose an option (0 to Exit)")
        print ("Select (1): to load your existing order: ")
        print ("Select (2): to order from the store: ")
        print ("Select (3): to view what's in stock: ")
        
        choice = input("Choice:")
  
        if choice=="1": 

            print("\nWe have 4 accounts currently:")
            print("Anna:    (Who likes to order what we have)")
            print("Dominic: (Who orders items we don't stock)")
            print("Mary:    (Who likes to order expensive items)")
            print("Shane:   (Who likes to order too much)")

            custName = input("\nAccount Name:")

            if custName in accounts:
            
                print("------------------------------")
                path = "../Customer/{}/order.csv".format(custName)
                order = custOrder(path)
                printCustomer(order, s)
                checkOut(order, s)
                updateShop(s) 
                updateCustomer(order, path)


            else:
                print("UNKNOWN ACCOUNT!")
                main()    
           
        elif choice=="2":

            print("\nWe have 4 accounts currently:")
            print("Anna, Dominic, Mary and Shane")

            custName = input("\nAccount Name:")

            if custName in accounts:        

                path = "../Customer/{}/liveOrder.csv".format(custName)
                print("What would you like to buy\n")
                printShop(s) 
                liveShop(path,custName)
                order= custOrder(path)
                printCustomer(order, s)           
                checkOut(order, s)
                updateShop(s)
            
            print("UNKNOWN ACCOUNT!")                
            main()

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
