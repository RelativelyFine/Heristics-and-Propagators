# =============================
# Student Names: David Courtis
# Group ID: 49
# Date: 2023-02-06
# =============================
# CISC 352 - W23
# cagey_csp.py
# desc: Defines required functions for the Cagey CSP problem
#

# Look for #IMPLEMENT tags in this file.

'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all variables in the given csp. If you are returning an entire grid's worth of variables
they should be arranged in a linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 20/100 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
|n^2-n-1| n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *
import itertools


def instantiate_n_dom_var(cagey_grid):
    n = cagey_grid[0]  # get the size of the grid

    dom = [i for i in range(1, n+1)]  # create the domain of 1 to n

    var_arr = []
    for t in itertools.product(dom, dom):

        # create the var_array
        var_arr.append(Variable('Cell({},{})'.format(t[0], t[1]), dom))

    return (n, dom, var_arr)


def binary_ne_grid(cagey_grid):

    # instantiate the n x n grid with the domain of 1 to n and the var_array
    n, dom, var_arr = instantiate_n_dom_var(cagey_grid)

    cons = []

    # since cagey is n x n, we can just iterate through rows and columns in one go
    for item in range(n):  # item is the row/column number
        for var in range(n):  # var is the cell number in the row/column
            for var2 in range(var+1, n):  # second var, with lower range (to avoid duplicates)

                # row constraint
                cons.append(Constraint("C({})".format(
                    var_arr[item*n+var].name, var_arr[item*n+var2].name), [var_arr[item*n+var], var_arr[item*n+var2]]))

                # column constraint
                cons.append(Constraint("C({})".format(
                    var_arr[var*n+item].name, var_arr[var2*n+item].name), [var_arr[var*n+item], var_arr[var2*n+item]]))

                # add all possible tuples to the constraint
                cons[-1].add_satisfying_tuples([(i, j)
                                               for i in dom for j in dom if i != j])

    csp = CSP("{}x{}-BinaryGrid".format(n, n), var_arr)  # create the csp
    for c in cons:
        csp.add_constraint(c)  # add all constraints to the csp
    return csp, var_arr


def nary_ad_grid(cagey_grid):
    # Note that this implementation is a little simpler than the binary_ne_grid because we need to account for less specific constraints (i.e. all different)
    # Other than that, it is the same as the binary_ne_grid

    # instantiate the n x n grid with the domain of 1 to n and the var_array
    n, dom, var_arr = instantiate_n_dom_var(cagey_grid)

    cons = []

    for item in range(n):  # item is the row/column number

        # row constraint
        cons.append(Constraint("C({})".format(
            [var_arr[item*n+var].name for var in range(n)]), [var_arr[item*n+var] for var in range(n)]))

        # column constraint
        cons.append(Constraint("C({})".format(
            [var_arr[var*n+item].name for var in range(n)]), [var_arr[var*n+item] for var in range(n)]))

        # add all possible tuples to the constraint
        cons[-1].add_satisfying_tuples(list(itertools.permutations(dom, n)))

    csp = CSP("{}x{}-N-naryGrid".format(n, n), var_arr)  # create the csp
    for c in cons:
        csp.add_constraint(c)  # add all constraints to the csp
    return csp, var_arr


def eval(x, y, operator):
    '''Evaluates the expression: x operator y.'''
    if operator == "+":
        return x + y
    elif operator == "*":
        return x * y
    elif operator == "-":
        return x - y
    elif operator == "/":
        return x / y
    else:
        raise Exception("Invalid operator")  # should never happen


def possible_cage(target, operands, operator):
    '''Takes a targer and a list of operands and an operator.
    Returns True if the cage in a cagy grid is possible, False otherwise.'''

    # get all permutations of the operands
    perms = list(itertools.permutations(operands))

    # evaluate the permutations
    for perm in perms:

        # the first operand is our starting point where we evaluate from
        result = perm[0]

        # evaluate the rest of the operands with the base and the operator
        for i in range(1, len(perm)):
            result = eval(result, perm[i], operator)
        if result == target:
            return True
    return False


def cagey_csp_model(cagey_grid):
    """
    Desc: a model of a Cagey grid built using choice (1) binary not-equal
          constraints for the grid, together with Cagey cage constraints.
    Reason: for faster computation in terms of number of constraints
        For n x n grid
            num of binary constraints
            (row + col) n x nC2 + n x nC2 = 2n x nC2
            num of n-ary constraints
            (row + col) n x n! + n x n! = 2n x n!
        which means num of binary < num of n-ary constraints
    """
    # Note: Some if the code is in a more expanded form.
    # I didn't put everything in 1 line because it was easier to read this way. (As much as I wanted to!)

    n = cagey_grid[0]  # n x n grid

    # this is the n x n grid with n-ary constraints
    csp, var_arr = binary_ne_grid(cagey_grid)

    # uncomment below for binary constraints
    # csp, var_arr = binary_ne_grid(cagey_grid)

    # Add cage constraints
    for cage in cagey_grid[1]:
        target = cage[0]
        operator = cage[2]
        dom = ["+", "-", "*", "/", "?"]

        # convert coordinates to index in var_arr
        # this is the list of variables in the cage
        in_cage = [var_arr[(var[0] - 1) * n + (var[1] - 1)] for var in cage[1]]

        # create cage variable
        cage_oper = Variable('Cage_op({}:{}:{})'.format(
            target, operator, in_cage), dom)

        cage_oper.assign(operator)  # assign operator value as given

        # Add cage variable to csp
        csp.add_var(cage_oper)
        varlist = in_cage[:]  # true copy
        varlist.append(cage_oper)
        con = Constraint('Cage({}:{}:{})'.format(
            target, operator, in_cage), varlist)

        # get the CURRENT domains of the variables in the cage
        varDoms = [v.cur_domain() for v in varlist]

        if (operator != "?") or (len(in_cage) == 1):
            # check all possible combinations of the variables in the cage
            # check if the cage is possible for each combination
            # add tuple to the constraint if it is possible
            con.add_satisfying_tuples([t for t in itertools.product(
                *varDoms) if possible_cage(target, t[:-1], t[-1])])

        else:  # if the operator is unknown and there are more than 1 variables in the cage

            # try all possible operators except "?"
            for oper in dom.remove("?"):

                # assign the operator to the last variable in the operator list
                # check all possible combinations of the variables in the cage
                # check if the cage is possible for each combination
                # add tuple to the constraint if it is possible
                # add all possible tuples to the constraint
                con.add_satisfying_tuples([t for t in itertools.product(
                    *(varDoms[:-1]+oper)) if possible_cage(target, t[:-1], t[-1])])

        # Add cage var and constraints to the csp Object
        var_arr.append(cage_oper)
        csp.add_constraint(con)
    return csp, var_arr
