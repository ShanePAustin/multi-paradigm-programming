//A C program for a basic shop that reads in stock and orders from csv
//Multi Paradigm Programming.
//GMIT Data Analytics 2021
//Author: Shane Austin
////////////////////////////////////////////////////////////////////////////////


#include <stdio.h>
#include <string.h>
#include <stdlib.h>

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
#include <stddef.h>
#include <errno.h>

//function for getline
//https://dev.w3.org/libwww/Library/src/vms/getline.c
int getline(char **lineptr, size_t *n, FILE *stream)
{
static char line[256];
char *ptr;
unsigned int len;

   if (lineptr == NULL || n == NULL)
   {
      errno = EINVAL;
      return -1;
   }

   if (ferror (stream))
      return -1;

   if (feof(stream))
      return -1;
     
   fgets(line,256,stream);

   ptr = strchr(line,'\n');   
   if (ptr)
      *ptr = '\0';

   len = strlen(line);
   
   if ((len+1) < 256)
   {
      ptr = realloc(*lineptr, 256);
      if (ptr == NULL)
         return(-1);
      *lineptr = ptr;
      *n = 256;
   }

   strcpy(*lineptr,line); 
   return(len);
}

////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////

//Product struct: variables - name and price
struct Product {

    char* name;
    double price;

};

//Product Stock struct: variables - Product(struct) and quantity
struct ProductStock {
    struct Product product;
    int quantity;

};

//Shop struct: variables - cash Product Stock(struct) and  stock index
struct Shop {
    double cash;
    struct ProductStock stock[20];
    int index;     

};

//Customer struct: variables - name, budget
//porducts shopping list and index 
struct Customer {
    char* name;
    double budget;
    struct ProductStock shoppingList[10];
    int index; 
      
};

//Prints the name and price of a product
void printProduct(struct Product p)
{

    printf("%s: e%.2f\n", p.name, p.price);
    printf("------------\n");
}



//Takes in a customer shopping list and prints:
//Customer Name and Budget
//What they have ordered
void printCustomer(struct Customer* c)
{
		printf("------------\n");
		printf("Customer Name: %s\nCustomer Budget: %.2f\n", c->name, c->budget);

		double sum = 0;
		//loop through shopping List
		for(int i = 0; i < (c->index -1); i++)

			{
				//Print the name and quantity of ordered item
				printf("------------\n");        
				printf("You have ordered %d %s \n",c->shoppingList[i].quantity,c->shoppingList[i].product.name);

				//Print the price of ordered items
				double cost = c->shoppingList[i].quantity * c->shoppingList[i].product.price;
				printf("The cost will be e%.2f\n", cost);
			}
}



//Takes in Shop stock and prints what's available
void printShop(struct Shop s)
{
		printf("Shop has %.2f in cash\n", s.cash);

		//loop through shop stock
		for (int i = 0; i < s.index -1; i++)

			{
				//print stock item and quantity available
				//calls on printProduct()
				printProduct(s.stock[i].product);
				printf("The shop has %d of the above\n", s.stock[i].quantity);
				printf("------------\n");
			}
}

//reads in the stock.csv
struct Shop createAndStockShop()
{    
		FILE * fp;
		char * line = NULL;
		size_t len = 0;
		ssize_t read;

		//open the csv and exit if file does not exist
		fp = fopen("../stock.csv", "r");
		if (fp == NULL)
			exit(EXIT_FAILURE);

		//read csv first line "cash"
		read = getline(&line, &len, fp);	
		float cash = atof(line);
		//open shop with cash taken from first line of file
		struct Shop shop = { cash };

		//add the stock looping through the csv
		while ((read = getline(&line, &len, fp)) !=-1){

			char *n = strtok(line,",");
			char *p = strtok(NULL, ",");
			char *q = strtok(NULL, ","); 
			int quantity = atoi(q);
			double price = atof(p);
			char *name = malloc(sizeof(char) * 50);
			strcpy(name, n);
			struct Product product = { name, price};
			struct ProductStock stockItem = {product, quantity};
			shop.stock[shop.index++] = stockItem;       
		}

		return shop;

}

// Read in customer specific file path
struct Customer custOrder(char* path)
{
		FILE * fp;
		char * line = NULL;
		size_t len = 0;
		size_t read;

		fp = fopen(path, "r");
		if (fp == NULL)
			exit(EXIT_FAILURE);

		// Read in the customer "name" and "budget" from the .csv file
		read = getline(&line, &len, fp);
		char * n = strtok(line, ",");
		char * b = strtok(NULL, ",");
		char * name = malloc(sizeof(char) * 50);
		strcpy(name, n);
		double budget = atof(b);

		struct Customer customerOrder = { name, budget };

		// Read in the "product name" and "quantity 
		// the customer requires from the .csv file
		while ((read = getline(&line, &len, fp)) != -1) {

				char * n = strtok(line, ",");
				char * q = strtok(NULL, ",");
				char * name = malloc(sizeof(char) * 50);
				strcpy(name, n);
				int quantity = atoi(q);
				struct Product product = { name };
				struct ProductStock customerItem = { product, quantity };
				customerOrder.shoppingList[customerOrder.index++] = customerItem;
		}
		return customerOrder;
}

// Process the customer order
// Update the shop stock and shop cash
struct Shop checkOut(struct Customer* c, struct Shop* s) {

	// keeps record of product prices to bill
	double totalBill = 0;

	printf("\n\n-----------------------------------");
	printf("\nOrder Summary\n-----------------------------------\n");
	
	// loop goes through shopping list
	for (int i=0; i<c->index-1; i++){

		short stockCheck = 0;
		char *list = malloc(sizeof(char) * 25);
		strcpy(list, c->shoppingList[i].product.name);
		
		// this loop looks at the shop stock
		for (int j=0; j < s->index-1; j++){
			
			char *shop = malloc(sizeof(char) * 25);
			strcpy(shop, s->stock[j].product.name);
			
			// does the item exist
			if (strstr(list, shop) != NULL){
				
				stockCheck=1;
				printf("This shop has: "); 
				
				// check stock level
				int orderAmt = c->shoppingList[i].quantity;
				int shopAmt = s->stock[j].quantity;
				double price = s->stock[j].product.price;
				
				// means stock to fill the order is available 
				if (orderAmt<=shopAmt){

					printf("%i %s for e%.2f\n\n",orderAmt, shop, price);
					// take away shopping list amount from shop stock

					if (c->budget > price){

					s->stock[j].quantity-=orderAmt;
					// add total bill to shop cash
					s->cash += (s->stock[j].product.price * orderAmt);
					// add order value to total bill 
					totalBill += (orderAmt * price);
				}
					else {printf("You can't afford\n");
					continue;
			}
					
		}
					
				
				// if not enough stock to fulfill order
				else {

					// remove what items are not in stock
					printf("%s but stock is low and we only have %i of the %i %s that you wanted\n", shop, shopAmt, orderAmt, shop);
					printf("We will add what we have to your order: %i %s for e%.2f (missing %i %s)\n\n", shopAmt, shop, price, orderAmt-shopAmt, shop);

					// check out what's available
					s->stock[j].quantity -= shopAmt;
					s->cash += (s->stock[j].product.price * shopAmt);
					totalBill += (shopAmt * price);
				}
			}
			
			// loop ends meaning we are at end of list
			if (j == s->index-1 & !stockCheck) {
				printf("Sorry we don't have any %s in this shop\n\n", list);
				
		}
	}
}		
	

	if (totalBill > c->budget){

		double shortAmount = 0;
		// Find the amount the customer is short by deducting the customer budget from the total order cost
		shortAmount = (c->budget - totalBill);  
		printf("\nSORRY YOUR BUDGET DOES NOT COVER THE COST OF THE PRODUCTS YOU WISH TO PURCHASE!");
		printf("\nYOU ARE SHORT BY e%.2f \n", shortAmount);

	}
		if (totalBill < c->budget){
		// gives total bill and remaining budget of customer
		printf("\nYour total bill is e%4.2f budget is %4.2f\n", totalBill, c->budget);
		printf("You will have e%4.2f left in your budget\n\n", c->budget - totalBill);
	
		}

		c->budget - totalBill;
						
	return *s;
}


//Live Shop to create a temp csv for that order
void liveShop(struct Shop s)
{
    struct Shop shop = createAndStockShop();

		char* path = (char*) malloc(10 * sizeof(char));
		char* custName = (char*) malloc(10 * sizeof(char));

        printf("\nWe have 4 accounts currently:");
        printf("\nAnna, Dominic, Mary and Shane");
		printf("\nAccount Name: ");
        scanf("%s", &custName);

		//set account name to the customers folder and order file
        sprintf(path, "../Customer/%s/liveOrder.csv",&custName);

        FILE *fpw;
    
		fpw = fopen(path, "w");

		if (fpw == NULL)
			exit(EXIT_FAILURE);

		char* custBudget = (char*) malloc(10 * sizeof(char));

		//Enter the budget customer has for this transaction
		printf("\nPlease Enter Your Budget: e");
		scanf("%s", &custBudget);

		fprintf(fpw, "%s, %s\n", &custName, &custBudget);

		int continueShopping = 1;

		char * prodName = (char*) malloc(10 * sizeof(char));
		char * prodQuantity = (char*) malloc(10 * sizeof(char));

			//Keep adding items to the shop until exit command
			while (continueShopping == 1) {

				printf("\nWhat would you like to order?: ");
				scanf("%s", &prodName);

				printf("\nHow many would you like?: #");
				scanf("%s", &prodQuantity);
				
				fprintf(fpw, "%s, %s\n", &prodName, &prodQuantity);

				printf("\n1 to continue shopping or 0 to checkout: ");
				scanf("%d", &continueShopping);                

				// If exiting the shop. Process the order &
				// update the shop stock and balance
				if (continueShopping == 0) {

                    fclose(fpw);
                                                         			
					struct Customer customerLiveOrder = custOrder(path);
					printf("\nGoing to Check Out\n");
					printf("\n------------------------------");
					checkOut(&customerLiveOrder, &shop);
					
				}
			}
		}

//Function to update the stock csv with new figures
void updateShop(struct Shop s)
{
	// Open the stock.csv in write mode.
	FILE * fp;
	char *filename = "../stock.csv"; 
	fp = fopen(filename,"w+");
	if (fp == NULL)
	{
		fprintf(stderr, "Could not open %s: %s\n", filename, strerror(errno));
		exit(EXIT_FAILURE);
	}

	// Update cash.
	fprintf(fp,"%.2f\n", s.cash);

	// Loop to update stock.
	for (int i=0; i< s.index-1; i++)
	{
		fprintf(fp, "%s,%.2f,%i\n",s.stock[i].product.name,s.stock[i].product.price,s.stock[i].quantity);	
	}
	fclose(fp);	
	return;
}

//Options menu for the application
//Can run order from csv
//order from live shop
//Print the current stock
void displayMenu()
{
    struct Shop shop = createAndStockShop();
	int choice = -1;	

	while (choice != 0){		
		
		fflush(stdin);
		printf("\nPlease choose an option (0 to Exit) ");
		printf("\nSelect (1): to load your existing order: ");
		printf("\nSelect (2): to order from the store: ");
        printf("\nSelect (3): to view what's in stock: ");
		scanf("%d", &choice);

		if (choice == 1)
		{

        printf("\nWe have 4 accounts currently:");
        printf("\nAnna:    (Who likes to order what we have)");
        printf("\nDominic: (Who orders items we don't stock)");
        printf("\nMary:    (Who likes to order expensive items)");
        printf("\nShane:   (Who likes to order too much)");

			char* path = (char*) malloc(10 * sizeof(char));
			char* custName = (char*) malloc(10 * sizeof(char));
			printf("\nAccount Name: ");
			scanf("%s", &custName);

			//Assign the path for the correct customer
			sprintf(path, "../Customer/%s/order.csv",&custName);

			//Print the order, checkout and update the csv
			struct Customer customerOrder = custOrder(path);
			printCustomer(&customerOrder);
			checkOut(&customerOrder, &shop);
			updateShop(shop);

		} 

        else if (choice == 2){

			printf("What would you like to buy \n");            	

			//Print the current shop, do live shop and update csv
	        printShop(shop);
            liveShop(shop);
			updateShop(shop);
		}	

		else if (choice == 3){
            
			printShop(shop);
		}
	}

	printf("Thank you for shopping with C");
}


int main(void)
{
	struct Shop shop = createAndStockShop();
    displayMenu();

    return 0;

}

