from pysmt.shortcuts import Solver, Not, get_env, And, to_smtlib, Equals, Min, Int, Or, Max,is_sat as pis_sat
from pysmt.logics import QF_UFLIRA
from pysmt.logics import QF_LRA
from pysmt.solvers.z3 import Z3Model
import z3
import logging

logger = logging.getLogger("kipro2")
#solver = Solver("z3", QF_UFLIRA)
solver = Solver("z3", QF_UFLIRA)
#solver = Solver("cvc4")

pysmt_to_z3_variables = dict()

def get_model(formulas):

    #return z3_check_sat_minimizing_var(formulas, "diff")
    #print(pis_sat(And([form for form in formulas])))
    if solver.solve(formulas):
        model = solver.get_model()
        #solver.reset_assertions()
        return model
    else:
        #solver.reset_assertions()
        return None


def is_sat(formulas):
    return solver.solve(formulas)
    # solver.add_assertion(formula)
    #
    # if solver.solve():
    #     solver.reset_assertions()
    #     return True
    # else:
    #     solver.reset_assertions()
    #     return False


def is_valid(formula):
    solver.add_assertion(Not(formula))

    if not solver.solve():
        solver.reset_assertions()
        return True
    else:
        solver.reset_assertions()
        return False





def get_smtlib_string(formula):

    #res = "(set-logic QF_UFLIRA) "
    res = "" # TODO: set logid?
    # produce variable declarations
    for symb in get_env().formula_manager.get_all_symbols():
        if symb.get_type().is_real_type():
            res += "(declare-const %s %s) " % (symb, "Real")

        elif symb.get_type().is_int_type():
            res += "(declare-const %s %s) " % (symb, "Int")

        else:
            raise Exception("unhandled type : %s" % symb.get_type())

    return res + (" (assert " + to_smtlib(formula) + ")")



