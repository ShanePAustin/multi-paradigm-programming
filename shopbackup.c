#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
#include <stddef.h>
#include <errno.h>


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
struct Product {
    char* name;
    double price;

};

struct ProductStock {
    struct Product product;
    int quantity;

};

struct Shop {
    double cash;
    struct ProductStock stock[20];
    int index;     

};

struct Customer {
    char* name;
    double budget;
    struct ProductStock shoppingList[10];
    int index; 
      
};

void printProduct(struct Product p)
{
    // printf("------------\n");
    printf("%s: $%.2f\n", p.name, p.price);
    //printf("------------\n");
}

void printCustomer(struct Customer c)//, struct Shop s
{
    printf("------------\n");
    printf("Customer Name: %s\nCustomer Budget: %.2f\n", c.name, c.budget);

    double sum = 0;

    for(int i = 0; i < c.index; i++)
    {
 		//int shopQuant = s.stock[i].quantity;
		// int custQuant = c.shoppingList[i].quantity;  


        printProduct(c.shoppingList[i].product);

        printf("QUANTITY: %d\n\n", c.shoppingList[i].quantity);

        // printf("%s Orders %d of above product\n", c.name, c.shoppingList[i].quantity);
        // double cost = c.shoppingList[i].quantity * c.shoppingList[i].product.price;
        // printf("The cost to %s will be $%.2f\n", c.name, cost);
    }
}

void printShop(struct Shop s)
{
	//printf("Shop has %.2f in cash\n", s.cash);
	for (int i = 0; i < s.index; i++)
	{
		//printf("------------\n");
        printProduct(s.stock[i].product);
		printf("The shop has %d of the above\n", s.stock[i].quantity);
        printf("------------\n");
	}
}

struct Shop createAndStockShop()
{    
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    fp = fopen("../stock.csv", "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);

    read = getline(&line, &len, fp);
    float cash = atof(line);
    //printf("cash in shop is %.2f\n", cash);
    
    struct Shop shop = { cash };

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

struct Customer custOrder()
{
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    size_t read;

	// char * customerFile;
	// char str1[50] = "../";
	// customerFile = strcat(str1, filename);

	fp = fopen("order1.csv", "r");
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

void liveShop()
{

		char* url = (char*) malloc(10 * sizeof(char));
		char* custName = (char*) malloc(10 * sizeof(char));
		printf("\nPlease Enter Your First Name: ");
        scanf("%s", &custName);

        sprintf(url, "../Customer/%s/liveOrder.csv",&custName);

         FILE *fpw;
    
		fpw = fopen(url, "w");

		if (fpw == NULL)
			exit(EXIT_FAILURE);

		char* custBudget = (char*) malloc(10 * sizeof(char));
		printf("\nPlease Enter Your Budget: $");
		scanf("%s", &custBudget);

		fprintf(fpw, "%s, %s\n", &custName, &custBudget);

			int continueShopping = 1;

			char * prodName = (char*) malloc(10 * sizeof(char));
			char * prodQuantity = (char*) malloc(10 * sizeof(char));

			while (continueShopping == 1) {
				printf("\nPlease Enter Product Name: ");
				scanf("%s", &prodName);

				printf("\nPlease Enter Requried Quantity: #");
				scanf("%s", &prodQuantity);
				
				fprintf(fpw, "%s, %s\n", &prodName, &prodQuantity);

				printf("\nEnter 1 to continue shopping or 0 to stop: ");
				scanf("%d", &continueShopping);                

				// If exiting the shop. Process the order &
				// update the shop stock and balance
				if (continueShopping == 0) {

                    //fpw2 = fopen("../%s/liveOrder.csv", "w"), custName;


                    //char* filename = "/%s/liveOrder.csv", custName;
                    fclose(fpw);
                    //fclose(fpw2);

                                                         
					
					//struct Customer customerLiveOrder = customerOrderList(filename);
					printf("\nProcessing Customer Order\n");
					printf("\n------------------------------");
					//processingOrder(&customerLiveOrder, &shop);
				}
			}
		}


void displayMenu()
{
	//askName();

	int choice = -1;	

	while (choice != 0){		
		
		fflush(stdin);
		printf("\nPlease choose an option (0 to Exit) ");
		printf("\nSelect (1): to load your existing order ");
		printf("\nSelect (2): to order from the store ");
		scanf("%d", &choice);

		if (choice == 1)
		{
			printf("The user pressed 1, load in csv\n");
            struct Customer customerOrder = custOrder();
            printCustomer(customerOrder);

		} else if (choice == 2){
			printf("What would you like to buy \n");
            	struct Shop shop = createAndStockShop();

	            printShop(shop);
                liveShop();
		}	
		//  else if (choice == 3){
		// 	askName();
		// }
	}
	printf("Thank you for shopping with C");
}


int main(void)
{
    displayMenu();
    // struct Customer shane = {"Shane", 100.0};

    // struct Product coke = {"Can Coke",1.10};
    // struct Product bread = {"Bread", 0.7};


    // printProduct(coke);

    // struct ProductStock cokeStock = { coke, 20};
    // struct ProductStock breadStock = { bread, 2};
    // shane.shoppingList[shane.index++] = cokeStock;
    // shane.shoppingList[shane.index++] = breadStock;

    // printCustomer(shane);

	// struct Shop shop = createAndStockShop();
	// printShop(shop);


    // printf("The shop has %d of the product %s\n", cokeStock.quantity, cokeStock.product.name);

    return 0;

}


// struct Customer custOrder()
// {
// 	FILE * fp;
//     char * line = NULL;
//     size_t len = 0;
//     ssize_t read;

//     fp = fopen("order1.csv", "r");
//     if (fp == NULL)
//         exit(EXIT_FAILURE);
	
// 	read = getline(&line, &len, fp);
//     char *a = strtok(line, ",");
//     char *b = strtok(NULL, ",");
//     char *custName = malloc(sizeof(char) * 50);
//     double custBudget = atof(b);
//     strcpy(custName, a); 
// 	struct Customer customer = { custName, custBudget};
	
//     while ((read = getline(&line, &len, fp)) != -1) {
// 		// TODO process remaining lines
// 	}        
// 	return customer;
// }   

// int main(void) 
// {
//     struct Customer customer = custOrder();
// 	printf("Customer name is: %s and they have: %.2f for their budget\n", customer.name, customer.budget);
//     return 0;
// }