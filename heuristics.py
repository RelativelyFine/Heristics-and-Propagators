# =============================
# Student Names: David Courtis
# Group ID: 49
# Date: 2023-02-06
# =============================
# CISC 352 - W23
# heuristics.py
# desc: Contains two different heuristics, one that uses minimum remaining values and one that uses degree heuristic
#


# Look for #IMPLEMENT tags in this file. These tags indicate what has
# to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''


def ord_dh(csp):
    '''A variable ordering heuristic that chooses the next variable to be assigned according to the Degree
    heuristic (DH). ord dh returns the variable that is involved in the largest number of constraints,
    which have other unassigned variables.'''

    # gets all unassigned variables in the csp
    # for each unassigned variable, get the number of constraints it is involved in
    # return the variable with the most constraints
    # this uses a lambda function where v is the variable and the length of the constraints it is involved in is returned

    return max(csp.get_all_unasgn_vars(), key=lambda v: len(csp.get_cons_with_var(v)))


def ord_mrv(csp):
    '''A variable ordering heuristic that chooses the next variable to be assigned according to the Minimum-
    Remaining-Value (MRV) heuristic. ord mrv returns the variable with the most constrained current
    domain (i.e., the variable with the fewest legal values remaining).'''

    # gets all variables in the csp
    # for each variable, get the number of values in its domain
    # return the variable with the least values in its domain
    # this uses a lambda function where v is the variable and the length of its domain is returned

    return min(csp.get_all_vars(), key=lambda v: len(v.cur_domain()))
