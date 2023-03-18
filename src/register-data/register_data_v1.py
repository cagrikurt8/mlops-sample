# Import libraries

import argparse
import logging
from azureml.core import Workspace, Dataset


# define functions
def main(args):
    ml_client = Workspace(subscription_id=args.subscription_id,
                          resource_group="AI-ML_RG",
                          workspace_name="ml-workspace")

    data_folder = Dataset.File.from_files(path=args.data_path)
    data_folder.register(workspace=ml_client,
                         name="diabetes-mlops-folder",
                         create_new_version=True)


def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--data_path", dest='data_path',
                        type=str)
    
    parser.add_argument("--subscription_id", dest='data_path',
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
