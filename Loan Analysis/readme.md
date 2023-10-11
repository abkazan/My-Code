# Loan analysis	
### TLDR: classes, modules, binary search trees, recursion, and data analysis using the Python Pandas module
In this project, I analyzed every loan application made in Wisconsin in 2020. To do this, I took the following steps:
1. I created a module, loans.py with three classes to represent applicants, loans, and banks
2. I then created anothe module, search.py to represent a binary search tree (BST), with functions to add nodes, lookup values, and print out each value in the tree
3. I then demonstrated the functionality of these modules in a notebook file by analyzing "First Home Bank," provided in the "Banks.json" dataset.
4. I then created a new bank object for "University of Wisconsin Credit Union," and analyzed the speed of adding loans to my BST. I also compared the speed of looking up loans in my BST to that of lookng up loans simply by looping over each loan.
5. Finally, I used pandas to plot the number of loan applicants that identify with multiple racial identities before writing a recursive function to count the leaf nodes, or nodes without any children in my BST.
6. I finished the project by writing a recursive function to find the third largest interest rate in the bank. 

