#include <stdio.h>
#include <string.h>
#include <stdlib.h>

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

void printCustomer(struct Customer c, struct Shop s)
{
    printf("------------\n");
    printf("Customer Name: %s\nCustomer Budget: %.2f\n", c.name, c.budget);

    double sum = 0;

    for(int i = 0; i < c.index; i++)
    {
 		int shopQuant = s.stock[i].quantity;
		int cusQuant = c.shoppingList[i].quantity;  


        printProduct(c.shoppingList[i].product);

        printf("QUANTITY: %d\n\n", c.shoppingList[i].quantity);

        printf("%s Orders %d of above product\n", c.name, c.shoppingList[i].quantity);
        double cost = c.shoppingList[i].quantity * c.shoppingList[i].product.price;
        printf("The cost to %s will be $%.2f\n", c.name, cost);
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



// void createAndStockShop()
// {
//     FILE *fp = fopen("stock.csv", "r");
//     if(fp == NULL) {
//     perror("Unable to open file!");
//     exit(1);
//     }

//     char chunk[128];

//     while(fgets(chunk, sizeof(chunk), fp) != NULL) {
//     fputs(chunk, stdout);
// }  
// }

void askName()
{
	fflush(stdin);
	printf("What is your name?\n\n");
	char name[10];
	fgets(name,10,stdin);
	printf("Welcome, %s\n",name);
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



			// docsvfunction();
		} else if (choice == 2){
			printf("What would you like to buy \n");
            	struct Shop shop = createAndStockShop();
	            printShop(shop);
			// doLiveStorefunction();
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