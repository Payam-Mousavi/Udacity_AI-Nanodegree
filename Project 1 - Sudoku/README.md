# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: First, all instances of the naked-twins are found (and put in a list) using 
the following algorithm: Iterating through all boxes, for each box, I look at 
its peers, and if I find a box which has a value of length 2 and the value is 
the same as the box's value, I append the box to the naked-twins list (if it's
not already there from previous iterations). Secondly, to remove the digits 
based on the naked-twins list, iterating through the unitlist, all the twins 
within the unit are found. Ignoring twins that exist in the main list but are 
not actually twins for the current unit, the two digits in the twins are removed 
from all other boxes in the units (even if they belong to the main list of twins). 
I originally hadn't accounted for the fact that there could be multiple pairs 
of twins in each unit! I fixed that problem once I got feedback through the 
online system. I also learned that removing items from a list in a loop is not
a good idea! I was able to use .append() instead to create a list of object 
I want to remove and then removed them. Please note that, I'm fairly new to 
Python so I am sure I haven't implemented the algorithm in the most efficient
manner.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Using the sudoko solver developed over the quizzes, the only modification 
required is to update the list of constraints. This includes:
1) the units: Two additional units containing the two diagonals are added,
2) The peers: for each box along the two diagonals, other elements in each 
    diagonal are added to its peers list, 
3) Similar to (1), the unitlist is modified to include the new units.
Once this is done, the original solver using the functions, Eliminate(.), 
only_choice(.), reduce_puzzle(.), and search(.) are used to solve the sudoku 
as before. In a sense, the additional constraints make the problem easier as
there are fewer choices available for each box, so the tree-search will 
converge faster. Also note, that the naked_twins function can in principal be
used in the diagonal sudoku solver. In that case, we will have two additional
units from which you could remove the naked twins from the corresponding boxes.
However, while I verified that the naked_twins function worked for the regular
sudoku, I chose not to include it in the solver for the diagonal sudoku.  

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

