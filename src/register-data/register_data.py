# Import libraries

import argparse
import glob
import os
import pandas as pd
import logging
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.entities import Data


# define functions
def main(args):
    data = Data(
        path=args.data_path,
        type=AssetTypes.URI_FOLDER,
        description="MLOps diabetes data",
        name="diabetes-mlops-dataset"
    )
    ml_client = MLClient.from_config(DefaultAzureCredential())
    ml_client.data.create_or_update(data)

    logging.debug(args.data_path)


def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--data_path", dest='data_path',
                        type=str)

    # parse args
    args = parser.parse_args()

    # return args
    return args

# run script
if __name__ == "__main__":
    # add space in logs
    print("\n\n")
    print("*" * 60)

    # parse args
    args = parse_args()

    # run main function
    main(args)

    # add space in logs
    print("*" * 60)
    print("\n\n")
