#include <stdio.h>
#include <string.h>
#include <stdlib.h>

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



struct Product {
    char* name;
    double price;

};

struct ProductStock {
    struct Product product;
    int quantity;

};

struct Customer {
    char* name;
	double budget;
    struct ProductStock shoppingList[10];
    int index; 
}; 

struct Customer custOrder()
{
	FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    fp = fopen("liveOrder.csv", "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);
	
	read = getline(&line, &len, fp);
    char *a = strtok(line, ",");
    char *b = strtok(NULL, ",");
    char *custName = malloc(sizeof(char) * 50);
    double custBudget = atof(b);
    strcpy(custName, a); 
	struct Customer customer = { custName, custBudget};
	
    while ((read = getline(&line, &len, fp)) != -1) {
		// TODO process remaining lines
        char *n = strtok(line,",");
        char *p = strtok(NULL, ",");
        char *q = strtok(NULL, ","); 
        int quantity = atoi(q);
        double price = atof(p);
        char *name = malloc(sizeof(char) * 50);
        strcpy(name, n);
        struct Product product = { name, price};
        struct ProductStock customerItem = {product, quantity};
        customer.shoppingList[customer.index++] = customerItem;       
    }        
	       
	return customer;
}   


void printCustomer(struct Customer* c)
{

	printf("\n------------------------------\n");
	printf("CUSTOMER NAME: %s \nCUSTOMER BUDGET: €%.2f\n", c->name, c->budget);
	printf("\n------------------------------");
	printf("\nCUSTOMER ORDER:\n");

	for(int i = 0; i < c->index; i++)
	{
		printf("PRODUCT NAME: %s \nQUANTITY REQUIRED: %d\n", c->shoppingList[i].product.name, c->shoppingList[i].quantity);
		printf("\n------------------------------\n");
	}
}

int main(void) 
{

    struct Customer customer = custOrder();
        printCustomer(custOrder);

}