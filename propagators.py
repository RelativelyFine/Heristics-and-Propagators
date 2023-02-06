# =============================
# Student Names: David Courtis
# Group ID: 49
# Date: 2023-02-06
# =============================
# CISC 352 - W23
# propagators.py
# desc: Contains two different propagators, one that uses forward checking and one that uses arc consistency
#


# Look for #IMPLEMENT tags in this file. These tags indicate what has
# to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''


def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check_tuple(vals):
                return False, []
    return True, []


def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable, value pairs and return
       '''

    pruned = []  # list of pruned values

    # if newVar is None we do initial FC enforce processing all constraints
    if newVar:
        constraints = csp.get_cons_with_var(newVar)
    else:
        constraints = csp.get_all_cons()

    # check constraints with only one uninstantiated variable
    for con in constraints:
        if con.get_n_unasgn() == 1:
            var = con.get_unasgn_vars()[0]

            # check all values in the domain of the variable
            for val in var.cur_domain():

                # if the value is not consistent with the constraint
                if not con.check_var_val(var, val):

                    # prune the value
                    if (var, val) not in pruned:
                        pruned.append((var, val))
                        var.prune_value(val)

            # if the domain is empty, this indicates a deadend D:
            if var.cur_domain_size() == 0:
                return False, pruned

    # if no deadend is detected, return True :D
    return True, pruned


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''

    # list of pruned values
    pruned = []

    # the GACQueue holds the constraints to be checked
    GACQueue = []
    if newVar:
        GACQueue = csp.get_cons_with_var(newVar)
    else:
        GACQueue = csp.get_all_cons()

    # a non-empty GACQueue indicates that there are still constraints to be re-/checked
    while GACQueue:

        # get the first constraint from the queue and check all variable domains (the values currently valid) in its scope
        con = GACQueue.pop(0)
        for var in con.get_scope():
            for val in var.cur_domain():

                # if the value is not consistent with the constraint
                if not con.check_var_val(var, val):

                    # prune the value
                    if (var, val) not in pruned:
                        pruned.append((var, val))
                        var.prune_value(val)

                    # if the domain is empty, this indicates a deadend D:
                    if var.cur_domain_size() == 0:
                        return False, pruned

                    # if the domain is not empty, add all constraints containing the variable to the queue
                    # this is done to check if the pruned value is still consistent with the other constraints
                    else:
                        for c in csp.get_cons_with_var(var):
                            if c not in GACQueue:
                                GACQueue.append(c)

    # if no deadend is detected, return True :D
    return True, pruned
