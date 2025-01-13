import click
from kipro2.parsing.parser import *
import os
from kipro2.utils.Statistics import Statistics
from kipro2.utils.Options import Options
from kipro2.kinduction.kinduction import KInduction
from kipro2.bmc.bmc import BMC
import pickle

logger = logging.getLogger("kipro2")

@click.argument('program', type=click.Path(exists=True))
@click.option('--post', type=click.STRING,
              help="The post-expectation. The postexpectation must be in GNF, i.e., of the form [guard_1]*expr + ... [guard_n]*expr such that the guard_i partition the state space.")
@click.option('--pre',
              type=click.STRING,
              help="Candidate upper bound/preexpectation in GNF.")
@click.option('--debuglog/--nodebuglog',
              default = False,
              help ="Determining the logging mode.")
@click.option('--engine',
               type=click.Choice(['kind', 'bmc']),
               default="kind",
               help = "Whether to use k-induction for verification or BMC for refutation.")
@click.option('--safestatistics',
              type=click.STRING,
              default="",
              help="Candidate upper bound/preexpectation in GNF.")
def _main(program, post, pre, debuglog,engine,safestatistics):

    _setup_logger("log.txt", logging.DEBUG if debuglog else logging.INFO, logging.DEBUG if debuglog else logging.INFO)

    print(engine)
    with open(program, 'r') as program_file:
        program_code = program_file.read()
        filename = os.path.basename(program_file.name)

    # ------------- Set up options and statistics objects ------------
    print(filename)
    options = Options()

    statistics = Statistics(filename, post, pre,engine)
    statistics.program = filename
    options.program_code = program_code
    options.post = post
    options.pre = pre


    # Returns a wp- or an ert-characteristic functional depending on past.
    (pre, charfun) = parse_program_and_postexp_into_charfun(options)

    if not pre.check_non_negativity():
        raise Exception("Preexpectation/Candidate upper bound must be non-negative.")

    logger.debug("pre:")
    logger.debug(str(pre))
    if not pre.check_non_negativity():
        raise Exception("Candidate upper bound/preexpectation can be negatie")

    if engine == "kind":
        KInduction(charfun,pre,statistics)
    else:
        BMC(charfun,pre,statistics)


    statistics.total_time.stop_timer()
    print(statistics)

    if safestatistics != "":
        with open(safestatistics, "wb") as handle:
            pickle.dump(statistics,handle)



def _setup_logger(logfile, cmd_loglevel, file_loglevel):
    logger = logging.getLogger("kipro2")
    logger.setLevel(cmd_loglevel)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(logfile)
    fh.setLevel(file_loglevel)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(cmd_loglevel)
    # create formatter and add it to the handlers
    fileformatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    consoleformatter = logging.Formatter('%(name)s: %(message)s')

    ch.setFormatter(consoleformatter)
    fh.setFormatter(fileformatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)


def pickle_statistics(path, filename, statistics):
    #print(path + "/" + filename)
    with open(path + filename + ".pickle", "wb") as handle:
        pickle.dump(statistics, handle)






main = click.command()(_main)
if __name__ == "__main__":
    main()