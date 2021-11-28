import argparse
import logging
import json

from typing import Sequence
from minizinc import Instance, Model, Solver
from minizinc.result import Status

logger = logging.getLogger(__file__)
handler = logging.StreamHandler()
# the formatter determines what our logs will look like
LOG_FMT = '%(levelname)s %(asctime)s %(filename)s %(funcName)s %(lineno)d %(message)s'
formatter = logging.Formatter(LOG_FMT)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def parse_args(str_args: Sequence[str] = None):
    parser = argparse.ArgumentParser(
        description='Solve marketing optimization problem')
    parser.add_argument('--json', type=str, default="small-dataset-whatif.json",
                        help='Data file (json) to be used.', required=True)
    parser.add_argument('--model', type=str, default="dss-marketing-optimization.mzn",
                        help='Model file to be used.')
    parser.add_argument('--solver', type=str, choices=["gecode"], default="gecode",
                        help='Solver to be used')
    if str_args is not None:
        return parser.parse_args(str_args)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    gecode = Solver.lookup("gecode")

    with open(args.json) as data_file:
        model = Model(args.model)
        model.add_file(args.json, parse_data=True)
        instance = Instance(gecode, model)
        for max_budget in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]:
            with instance.branch() as scenario:
                scenario["pMaxBudget"] = max_budget
                result = scenario.solve()
                if result.status in [Status.SATISFIED, Status.OPTIMAL_SOLUTION]:
                    logger.info("Max budget %.2f ->  %.2f", max_budget, result['objective'])
                else:
                    logger.info("Max budget %.2f -> no solution", max_budget)

        logger.info("Solution for max budget = 3.0")
        with instance.branch() as final:
            final["pMaxBudget"] = 3.0
            result = final.solve()
            logger.info(f"> Optimal margin = {result['objective']}")
            for customer in range(instance["pCustomersN"]):
                for product in range(instance["pProductsN"]):
                    for channel in range(instance["pChannelsN"]):
                        if result["vAssignment"][customer][product][channel] > 0.5:
                            logger.info(f">> Offer product:{product} to customer {customer} using channel {channel}")
