from kipro2.expectations.Expectation import Expectation

class KInduction:

    def __init__(self, charfun, pre, statistics):

        k = 1
        curr = pre
        while True:

            statistics.formula_time.start_timer()
            apply = charfun.apply_expectation(curr, prune_unsat_guards_early=True)
            statistics.formula_time.stop_timer()

            statistics.sat_time.start_timer()
            if Expectation.check_leq(apply, pre):
                statistics.sat_time.stop_timer()
                break
            statistics.sat_time.stop_timer()

            statistics.formula_time.start_timer()
            curr = Expectation.pointwise_minimum(apply, pre)
            statistics.formula_time.stop_timer()
            k = k + 1

        statistics.k = k
        statistics.result = "ind"
        statistics.final_size = len(curr.guard_linexp_pairs)