import sys
import csv

# create a Product class, give it a repr method
class Product:

    def __init__(self, name, price=0):
        self.name = name
        self.price = price
    
    def __repr__(self):
        return f'PRODUCT NAME: {self.name}\nPRODUCT PRICE: {self.price}'
# create a ProductStock 
class ProductStock:

    def __init__(self, product, quantity):
        self.product = product # product is a class
        self.quantity = quantity # quantity is a float - a primitive. Methods cannot be invoked on primitives
    # getter method for getting product name
    def name(self):
        return self.product.name
    # getter method for getting product price
    def unit_price(self):
        return self.product.price

    # method for calculate cost   
    def cost(self):
        return self.unit_price() * self.quantity

    # a getter method to get the quantity of a stock item
    def get_quantity(self):
        return self.quantity

    # a setter method to update the quantity of a product for each quantity of stock sold
    def set_quantity(self, saleQty):
        self.quantity -= saleQty

    # a getter method to access the product
    def get_product(self):
        return self

    # a repr method to print the product, uses the product repr method
    def __repr__(self):

        # self.product is an instance of the product a class 
        return "{}\nThe shop has {} of the above \n-------------".format(self.product,int(self.quantity))
 
## Define a customer class
class Customer:
    # define the constructor 
    def __init__(self, path):
        self.shoppingList=[]
             

        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            first_row = next(csv_reader)
            self.name = first_row[0]
            self.budget = float(first_row[1])

            for row in csv_reader:
                n = row[0]
                q = float(row[1])
                p = Product(n)
                ps = ProductStock(p, q)
                self.shoppingList.append(ps)

            return

            
     # a method to calculate customer costs   
    def calculate_costs(self, price_list):
            # each shop_item is a productStock
        for shop_item in price_list:
            # iterate through the customer shopping list 
            for list_item in self.shoppingList:
                # check if the item name matches a shop item
                if (list_item.name() == shop_item.name()):
                    # if so pull out the price
                    list_item.product.price = shop_item.unit_price()
    # a method for calculating item cost
    def order_cost(self):
        cost = 0
        # going through the customer shopping list of productStocks  and getting out the cost
        for list_item in self.shoppingList:
            # get the cost using the ProductStock cost method
            cost += list_item.cost()
        return cost

    def updateCustomer(self, path):

        with open (path, 'w', newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter = ',')



            custUpdate = (self.name, round(self.budget,2))
            csv_writer.writerow(custUpdate)

            for item in self.shoppingList:
                newStock = (item.product.name, int(item.quantity))
                csv_writer.writerow(newStock)

# A repr method returns a state based representation of the class 
    def __repr__(self):

        print("------------------------------")
        print("Customer Name: {} \nCustomer Budget {}".format(self.name,self.budget))
        print("------------------------------")

        # just print the actual customer order from the file first
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

# create a subclass of customer so the live customer can use all the customer functionality
class liveShop:
    def __init__(c, path, custName):
        print("Live Shop")


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

############## ################## Shop class  ####################  ######################  
#  the shop takes a customers basket, checks stock, calculcates cost, updates stock, updates cash
       
class Shop:
    # 
    def __init__(self, path):
        # set up an array to read in the stock to
        self.stock = []
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            first_row = next(csv_reader)
            self.cash = float(first_row[0])

            for row in csv_reader:
                p = Product(row[0], float(row[1]))
                ps = ProductStock(p, float(row[2]))
                self.stock.append(ps)

    # a representation method for the shop
    def __repr__(self):
        str = ""
        str += f'Shop has €{self.cash} in cash\n'
        # loop over the stock items, each item is class ProductStock
        for item in self.stock:
            str += f"{item}\n"
        return str        

      ### def checkOut, takes in a customer 
    def checkOut(self,c):

        print("\n------------------------------")
        print("Check Out")

        print("------------------------------")
        print("Order Summary\n------------------------------")

        cash = float(self.cash)
        budget = float(c.budget)
        startBudget = budget
        totalBill = 0

        # print(cash)
        # print(budget)

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

        # totalBill = (startBudget - budget)

        if totalBill < budget:
            print("\nYour total bill is €{:.2f} budget is €{:.2f}\n".format(totalBill, startBudget))
            # print("\nYour total bill is €{:.2f}\n".format(totalBill))
            print("You will have €{:.2f} left in your budget\n\n".format(startBudget - totalBill))  

        self.cash = cash
        c.budget = budget


        return      

    def checkOrder(s, name):
            for i in s.stock:
            # for each ProductStock compare product.name with searched string 
                if i.product.name == name:
                    # if found return ProductStock
                    return i
            # if not found return None
            return None
 
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
            

    def menu(self):

        accounts = ("Anna", "Dominic", "Mary", "Shane")
        while True:

            print ("Please choose an option (0 to Exit)")
            print ("Select (1): to load your existing order: ")
            print ("Select (2): to order from the store: ")
            print ("Select (3): to view what's in stock: ")

            self.choice = input("Choice:")

            if (self.choice =="1"):    

                print("\nWe have 4 accounts currently:")
                print("Anna:    (Who likes to order what we have)")
                print("Dominic: (Who orders items we don't stock)")
                print("Mary:    (Who likes to order expensive items)")
                print("Shane:   (Who likes to order too much)")
                    
                custName = input("\nAccount Name:")
                print("------------------------------")

                if custName in accounts:
                    path = "../Customer/{}/order.csv".format(custName)

                    c = Customer(path)

                    # call calculate method on the customer with shop stock as input
                    c.calculate_costs(self.stock)
                    # print the customer
                    print(c)
                    # process the order using customer object as input
                    self.checkOut(c)
                    self.updateShop()
                    c.updateCustomer(path)
                    self.menu()
                
                print("UNKNOWN ACCOUNT!")
                self.menu()

            elif (self.choice=="2"):

                print("\nWe have 4 accounts currently:")
                print("Anna, Dominic, Mary and Shane")                

                custName = input("\nAccount Name:")

                if custName in accounts:

                    path = "../Customer/{}/liveOrder.csv".format(custName)
                    print("What would you like to buy\n")
                    print(self)   

                    # create a customer object by calling the live class
                    liveShop(path,custName)
                    c = Customer(path)
                    # call calculate method on the live customer object with shop stock as input
                    c.calculate_costs(self.stock)
                    print(c)
                    # process the order with the customer object as input
                    self.checkOut(c)
                    self.updateShop()
                    self.menu()

                elif (self.choice =="3"):
                    print("------------------------------")
                    
                    print(self)
                    self.menu()        

                print("UNKNOWN ACCOUNT!")
                self.menu()

            elif(self.choice =="0"):
                print("\nThank you for shopping with OOP")
                # to exit straight out of the program as this is part of the shop class
                sys.exit()
            
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