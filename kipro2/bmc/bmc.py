from kipro2.expectations.Expectation import Expectation
from kipro2.expectations.Guard import Guard
from kipro2.expressions.LinearExpression import LinearExpression
from pysmt.shortcuts import Real
class BMC:

    def __init__(self, charfun, pre, statistics):

        k = 1
        curr = Expectation(charfun.variables, [(Guard.TRUE(charfun.variables), LinearExpression.get_constant_expression(charfun.variables, Real(0)))])
        while True:

            statistics.formula_time.start_timer()
            curr = charfun.apply_expectation(curr, True)
            statistics.formula_time.stop_timer()

            print("Size = %s. check" % len(curr.guard_linexp_pairs))

            statistics.sat_time.start_timer()
            print("leqstart")
            if not Expectation.check_leq(curr, pre, True):
                statistics.sat_time.stop_timer()
                break
            statistics.sat_time.stop_timer()
            print("leqend")
            k = k + 1

        statistics.k = k
        statistics.result = "ref"
        statistics.final_size = len(curr.guard_linexp_pairs)