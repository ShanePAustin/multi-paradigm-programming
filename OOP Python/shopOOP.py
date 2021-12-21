#A Object Orientated Python program for a basic shop that reads in stock and orders from csv
#Multi Paradigm Programming.
#GMIT Data Analytics 2021
#Author: Shane Austin

import csv

#Create a Product class
#product name and price
class Product:

    def __init__(self, name, price=0):
        self.name = name
        self.price = price
    
    def __repr__(self):
        return f'PRODUCT NAME: {self.name}\nPRODUCT PRICE: {self.price}'

#Create a ProductStock class
#Link to product and set quantity
class ProductStock:

    def __init__(self, product, quantity):
        self.product = product 
        self.quantity = quantity

    #Function to get product name
    def name(self):
        return self.product.name

    #Function to get product price
    def unitPrice(self):
        return self.product.price

    #Function to get calculate cost   
    def cost(self):
        return self.unitPrice() * self.quantity

    #repr function to print the product
    def __repr__(self):

        return "{}\nThe shop has {} of the above \n-------------".format(self.product,int(self.quantity))
 
## Define a customer class
class Customer:
 
    def __init__(self, path):
        self.shoppingList=[]
             
        #Read in customer specific file path
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            #Read in the customer "name" and "budget" from the .csv file
            first_row = next(csv_reader)
            self.name = first_row[0]
            self.budget = float(first_row[1])

            #Read in the "product name" and "quantity" ordered
            for row in csv_reader:
                n = row[0]
                q = float(row[1])
                p = Product(n)
                ps = ProductStock(p, q)
                self.shoppingList.append(ps)

            return

            
    #Function to calculate customer costs   
    def calculate_costs(self, priceList):
            # each shopItem is a productStock
        for shopItem in priceList:
            # iterate through the customer shopping list 
            for listItem in self.shoppingList:
                # check if the item name matches a shop item
                if (listItem.name() == shopItem.name()):
                    # if so pull out the price
                    listItem.product.price = shopItem.unitPrice()

    #Function for calculating item cost
    def order_cost(self):
        cost = 0
        #Loop through the customer shopping list
        for listItem in self.shoppingList:
            #Get the cost
            cost += listItem.cost()
        return cost

    #Function to update the customer budget
    def updateCustomer(self, path):

        with open (path, 'w', newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter = ',')

            #Write the first line of the csv with new budget
            custUpdate = (self.name, round(self.budget,2))
            csv_writer.writerow(custUpdate)

            #rewrite the original customer order
            for item in self.shoppingList:
                newStock = (item.product.name, int(item.quantity))
                csv_writer.writerow(newStock)

    #Takes in a customer shopping list and prints:
    #Customer Name and Budget
    #What they have ordered             
    def __repr__(self):


        print("------------------------------")
        print("Customer Name: {} \nCustomer Budget {}".format(self.name,self.budget))
        print("------------------------------")

 
        for item in self.shoppingList:
            print(item.product)
            print("You have ordered {} {}\n".format(int(item.quantity),item.product.name))
            
            cost = item.quantity * item.product.price

            print("The cost to {} will be €{}".format(self.name, cost))
            print("------------------------------")  

            totalBill = self.order_cost()

            out = ""
            out += ("Total Cost will be {:.2f}".format(totalBill))          
                
        return out

#LiveShop class to create a temp csv for that order from Account name path
class liveShop:
    def __init__(c, path, custName):
        print("Live Shop")


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


#Shop class for stock and order processing       
class Shop:
     
    def __init__(self, path):
        #Set up an array to read in the stock to
        self.stock = []
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            #read csv first line "cash"
            first_row = next(csv_reader)
            self.cash = float(first_row[0])

            #add the stock looping through the csv
            for row in csv_reader:
                p = Product(row[0], float(row[1]))
                ps = ProductStock(p, float(row[2]))
                self.stock.append(ps)

    # repr for the shop
    def __repr__(self):
        str = ""
        str += f'Shop has €{self.cash} in cash\n'
        # loop over the stock items, each item is class ProductStock
        for item in self.stock:
            str += f"{item}\n"
        return str        

    #Process the customer order
    def checkOut(self,c):

        print("\n------------------------------")
        print("Check Out")
        print("*************")
        
        print("Order Summary\n------------------------------")

        cash = float(self.cash)
        budget = float(c.budget)
        startBudget = budget
        totalBill = 0

        for item in c.shoppingList:

            # check if customer's product exists in shop stock 
            stockCheck = self.checkOrder(item.product.name)
            
            # if product not found in shop stock 
            if stockCheck == None:
                print("Sorry we don't have any {} in this shop".format (item.product.name))
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
                        print("Sorry you cannot afford a {} it will be remove from the order".format(item.product.name))
                        continue

                else:
                    print("This shop has {} but stock is low and we only have {} of the {} that you wanted\n".format(item.product.name, int(stockCheck.quantity),int(item.quantity)))
                    print("We will add what we have to your order: {} {}\n".format(int(stockCheck.quantity), item.product.name))
                    cash += itemPrice
                    budget -= itemPrice
                    totalBill += (stockCheck.quantity * stockCheck.product.price)
                    stockCheck.quantity = 0

 

        if totalBill < budget:
            print("\nYour total bill is €{:.2f} budget is €{:.2f}\n".format(totalBill, startBudget))
            print("You will have €{:.2f} left in your budget\n\n".format(startBudget - totalBill))  

        self.cash = cash
        c.budget = budget

        return      

    #function to check stock against order item
    def checkOrder(s, name):
            for i in s.stock:
            # for each ProductStock compare product.name with searched string 
                if i.product.name == name:
                    # if found return ProductStock
                    return i
            # if not found return None
            return None

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
            

    #Options menu for the application
    #Can run order from csv
    #order from live shop
    #Print the current stock
    def menu(self):

        #list of current viable users
        accounts = ("Anna", "Dominic", "Mary", "Shane")
        while True:

            print ("Please choose an option (0 to Exit)")
            print ("Select (1): to load your existing order: ")
            print ("Select (2): to order from the store: ")
            print ("Select (3): to view what's in stock: ")

            self.choice = input("Choice:")

            #option 1 Shop form csv
            if (self.choice =="1"):    

                print("\nWe have 4 accounts currently:")
                print("Anna:    (Who likes to order what we have)")
                print("Dominic: (Who orders items we don't stock)")
                print("Mary:    (Who likes to order expensive items)")
                print("Shane:   (Who likes to order too much)")
                    
                custName = input("\nAccount Name:")
                print("------------------------------")

                #continue if account name is in the list
                if custName in accounts:
                    path = "../Customer/{}/order.csv".format(custName)

                    c = Customer(path)

                    # call calculate method on the customer with shop stock as input
                    c.calculate_costs(self.stock)
                    #print the customer
                    print(c)

                    #process the order, checkout
                    #and update the CSVs
                    self.checkOut(c)
                    self.updateShop()
                    c.updateCustomer(path)
                    self.menu()
                
                print("UNKNOWN ACCOUNT!")
                self.menu()

            #option 2 live order
            elif (self.choice=="2"):

                print("\nWe have 4 accounts currently:")
                print("Anna, Dominic, Mary and Shane")                

                custName = input("\nAccount Name:")

                if custName in accounts:

                    path = "../Customer/{}/liveOrder.csv".format(custName)
                    print("What would you like to buy\n")
                    print(self)   

                    
                    liveShop(path,custName)
                    c = Customer(path)
                    
                    c.calculate_costs(self.stock)
                    print(c)
                    
                    #process the order, checkout
                    #and update the shop CSV                    
                    self.checkOut(c)
                    self.updateShop()
                    self.menu()

                print("UNKNOWN ACCOUNT!")
                self.menu()


            #Option 3 show stock
            elif (self.choice =="3"):
                print("------------------------------")
                    
                print(self)
                self.menu()      


            elif(self.choice =="0"):
                print("\nThank you for shopping with OOP")
                
                exit()
            
            else:
                print("Please choose an option from the menu")
                self.menu()


# the main method just creates a shop object 
def main():
    s = Shop("../stock.csv")
    s.menu()
        
if __name__ == "__main__":

    # call the main method
    main() 