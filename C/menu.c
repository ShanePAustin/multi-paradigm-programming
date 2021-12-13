#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void askName()
{
	fflush(stdin);
	printf("What is your name?\n");
	char name[10];
	fgets(name,10,stdin);
	printf("Welcome, %s\n",name);
}
 

void displayMenu()
{
	askName();

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
			printf("What would you like to buy");
			// doLiveStorefunction();
		}	
		//  else if (choice == 3){
		// 	askName();
		// }
	}
	printf("Thank you for shopping with C");
}

int main(void){
	displayMenu();
}