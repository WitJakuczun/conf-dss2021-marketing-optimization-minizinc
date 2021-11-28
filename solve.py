import argparse
import logging
import json

from typing import Sequence
from minizinc import Instance, Model, Solver

logger = logging.getLogger(__file__)
handler = logging.StreamHandler()
# the formatter determines what our logs will look like
LOG_FMT = '%(levelname)s %(asctime)s %(filename)s %(funcName)s %(lineno)d %(message)s'
formatter = logging.Formatter(LOG_FMT)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def parse_args(str_args : Sequence[str]=None):
    parser = argparse.ArgumentParser(description='Solve marketing optimization problem')
    parser.add_argument('--json', type=str, default="dss-marketing-optimization.json",
                       help='Data file (json) to be used.', required=True)
    parser.add_argument('--model', type=str, default="dss-marketing-optimization.mzn",
                       help='Model file to be used.')
    parser.add_argument('--solver', type=str, choices=["gecode"], default="gecode",
                       help='Solver to be used')
    if str_args is not None:
        return parser.parse_args(str_args)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args(["--json", "small_data.json"])
    gecode = Solver.lookup("gecode")

    model = Model(args.model)

    with open(args.json) as data_file:
        model.add_file(args.json, parse_data=True)
        instance = Instance(gecode, model)
        result = instance.solve()
        logger.info("Solution objective: %.2f", result['objective'])

        for customer in range(instance["pCustomersN"]):
            for product in range(instance["pProductsN"]):
                for channel in range(instance["pChannelsN"]):
                    if result["vAssignment"][customer][product][channel] > 0.5:
                        logger.info(f"Offer product:{product} to customer {customer} using channel {channel}")
