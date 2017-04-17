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

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    
    all_digits = '123456789'
    
    for unit in row_units + column_units + square_units:
        d = dict()
        for digit in all_digits:
            # get all boxes in the unit that have the digit
            boxes_with_digit = ''.join([box for box in unit if digit in values[box]])
            # if a digit is only in 2 boxes:
            if len(boxes_with_digit) == 4:
                # Insert the concatenated boxes names as the key in a dictionary with digit as the value 
                if (boxes_with_digit not in d.keys()): 
                    # print('inserting:', digit, ' in ', boxes_with_digit)
                    d[boxes_with_digit] = digit
                # If the concatenated boxes names are already in the dictionary, we have a twin!
                else:
                    digits = d[boxes_with_digit] + digit
                    # print('updating:', digits, ' in ', boxes_with_digit)

                    for box in unit:
                        if (box in boxes_with_digit):
                            # These 2 boxes must have only these 2 values
                            assign_value(values, box, digits) #values[box] = digits
                            
                        else:
                            # The rest of the boxes cannot have these digits
                            assign_value(values, box, values[box].replace(digits[0], ""))
                            assign_value(values, box, values[box].replace(digits[1], ""))
                            # values[box] = values[box].replace(digits[0], "")
                            # values[box] = values[box].replace(digits[1], "")
    return values
 

def cross(A, B):
    "Cross product of elements in A and elements in B."
        return [s+t for s in A for t in B]

rows = "ABCDEFGHI"
cols = "123456789"
"""
Creating All Boxes
"""
boxes = cross(rows, cols)
"""
Creating Row Units
"""
row_units = [cross(r, cols) for r in rows]
"""
Creating Columns Units
"""
column_units = [cross(rows, c) for c in cols]
diag_units = [[],[]]
"""
Creating Diagonal Units
"""
for index, s in enumerate(rows):
    diag_units[0].append(s+cols[index])
for index, s in enumerate(reversed(rows)):
    diag_units[1].append(s + cols[index])
"""
Creating Square Units
"""
square_units = [cross(rs, cs) for rs in ["ABC", "DEF", "GHI"] for cs in ["123", "456", "789"]]
"""
Creating Enitre Unitlist
"""
unitlist = row_units + column_units + square_units + diag_units
"""
Creating Units and Peers for each box as a dictionary
"""
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

    pass

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
        chars = []
    digits = '123456789'
    for c in grid:
        if c == '.':
            chars.append(digits)
        if c in digits:
            chars.append(c)
    assert len(chars) == 81
    return dict(zip(boxes, chars))
    pass

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
    print
    pass

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit,'')) 
            # values[peer] = values[peer].replace(digit,'')
    return values
    pass

def only_choice(values):
        for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                #values[dplaces[0]] = digit
                values = assign_value(values, dplaces[0], digit)
    return values
    pass

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the naked twins strategy
        values = naked_twins(values) 
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    pass

def search(values):
# First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False:
        return False

    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!

    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    pass

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
