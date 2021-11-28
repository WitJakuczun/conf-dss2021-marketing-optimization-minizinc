import logging
import json

datasets = {
    "small_dataset" : {
        "pCustomersN": 2,
        "pProductsN": 2,
        "pChannelsN": 2,
        "pMaxBudget": 1.0,
        "pMinHurdleReve": 0.2,

        "pExpectedReve": [  # customers
            [  # products
                [0.45, 0.2],  # channels
                [0.35, 0.3],
            ],
            [
                [0.55, 0.1],
                [0.2, 0.45],
            ],
        ],
        "pChannelCosts": [0.45, 0.2],
        "pProductsMinOffersN": [1, 1],
    }
}

logger = logging.getLogger(__file__)
handler = logging.StreamHandler()
# the formatter determines what our logs will look like
LOG_FMT = '%(levelname)s %(asctime)s %(filename)s %(funcName)s %(lineno)d %(message)s'
formatter = logging.Formatter(LOG_FMT)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    for dataset_name, dataset in datasets.items():
        logger.info(f"Generating {dataset_name} dataset")
        with open(f"{dataset_name}.json", "w") as json_file:
            json.dump(dataset, json_file)
