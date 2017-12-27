'''
Diagonal Sudoku solver + naked_twins functions created for Udacity AI-nanodegree
Author: Payam Mousavi
Date:April 26, 2017
--------------------------------NOTE:------------------------------------------
The following code was taken mostly from the Udacity AI program. The following 
were added:
    1) naked_twins() function that's an additional strategy for reducing the puzzle,
    2) The capability to solve 'diagonal' sudoku was added.

Also, minor modifications were made to the other functions to facilitate 
visualization.
'''
#------------------------------------------------------------------------------
#                           Preliminary definitions
#------------------------------------------------------------------------------
from collections import Counter

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]
    pass
  
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
# Made a copy of the original unitlist to be used by naked_twins function:
unitlist_naked = unitlist[:]

#------------------------------------------------------------------------------
#                       Diagonal Sudoku modifications
#------------------------------------------------------------------------------
# Comment this section out to solve a normal sudoku.

# Modifying unitlist:
diag1 = list()
diag2 = list()
# First diagonal:
for i in range(9):
    diag1.append(unitlist[i][i])
    diag2.append(unitlist[9-1-i][i])
    
# Modifying the unitlist:
unitlist.append(diag1)
unitlist.append(diag2)

# Modifying peers dictionary:
for box in diag1:
    for box2 in diag1:
        if box2!=box:
            peers[box].add(box2)
for box in diag2:
    for box2 in diag2:
        if box2!=box:
            peers[box].add(box2)
            
# Modifying units:
for box in diag1:
    units[box].append(diag1)
for box in diag2:
    units[box].append(diag2)
#------------------------------------------------------------------------------    
#                   End of Diagonal Sudoku modification
#------------------------------------------------------------------------------    

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

#------------------------------------------------------------------------------
#                          End of preliminary definitions
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#                               naked_twins function
#------------------------------------------------------------------------------
def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    
    # Find all instances of naked twins
    naked_twins_list = list()
    for box in boxes:
        for peer in peers[box]:
            if (len(values[peer])==2) and (values[peer]==values[box]) and (peer not in naked_twins_list):
                naked_twins_list.append(peer)
                
    # Eliminate the naked twins as possibilities for their peers
    
    # For each unit, remove the twins not belonging to that unit:
    for unit in unitlist_naked:
        twins_value_list = list()
        unit_twins = [twins for twins in unit if twins in naked_twins_list]
        unit_twins_values = [values[x] for x in unit_twins]
        b = [k for (k,v) in Counter(unit_twins_values).items() if v<2]
        if len(b)!=0:
            remove_list = list()
            for i in range(len(b)):
                remove_list.append(unit_twins[unit_twins_values.index(b[i])])
            for l in remove_list:    
                unit_twins.remove(l)
        # Remove twin digits from all units with those digits: 
        if len(unit_twins)>0:
            for box in unit_twins:
                twins_value_list.append(values[box])
            twins_values = ''.join([twins_value_list for twins_value_list,n in Counter(twins_value_list).items() if n>1])
            for i in range(9):
                if len(values[unit[i]])>1 and (unit[i] not in unit_twins):
                    remove_values = ''.join(list(set(twins_values).intersection(values[unit[i]])))
                    values[unit[i]] = ''.join(c for c in values[unit[i]] if c not in remove_values)
    return values
    pass
#------------------------------------------------------------------------------
#                               grid_values function
#------------------------------------------------------------------------------
def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))
    pass

#------------------------------------------------------------------------------
#                               display function
#------------------------------------------------------------------------------
def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return
    pass

#------------------------------------------------------------------------------
#                               eliminate function
#------------------------------------------------------------------------------
def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values,peer,values[peer].replace(digit,''))
    return values
    pass

#------------------------------------------------------------------------------
#                           only_choice function
#------------------------------------------------------------------------------
def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values,dplaces[0],digit)
    return values
    pass

#------------------------------------------------------------------------------
#                           reduce_puzzle function
#------------------------------------------------------------------------------
def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    pass

#------------------------------------------------------------------------------
#                               search function
#------------------------------------------------------------------------------
def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        assign_value(new_sudoku,s,value)
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    pass

#------------------------------------------------------------------------------
#                               solve function
#------------------------------------------------------------------------------
def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values


#------------------------------------------------------------------------------
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
