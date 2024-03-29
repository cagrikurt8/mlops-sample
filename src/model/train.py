# Import libraries

import argparse
import glob
import os
import mlflow

import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score


# define functions
def main(args):
    # TO DO: enable autologging
    mlflow.sklearn.autolog(log_input_examples=True,
                           registered_model_name="mlops-model")

    # read data
    df = get_csvs_df(args.training_data)
    
    # split data
    X_train, X_test, y_train, y_test = split_data(df)

    # train model
    model = train_model(args.reg_rate, X_train, X_test, y_train, y_test)
    mlflow.sklearn.save_model(model, args.model_output)


def get_csvs_df(path):
    if not os.path.exists(path):
        raise RuntimeError(f"Cannot use non-existent path provided: {path}")
    csv_files = glob.glob(f"{path}/*.csv")
    if not csv_files:
        raise RuntimeError(f"No CSV files found in provided data path: {path}")
    return pd.concat((pd.read_csv(f) for f in csv_files), sort=False)


# TO DO: add function to split data

def split_data(df):
    X, y = df.drop("Diabetic", axis=1).values, df["Diabetic"].values
    
    return train_test_split(X, y, test_size=0.3, random_state=0)


def train_model(reg_rate, X_train, X_test, y_train, y_test):
    # train model
    
    model = LogisticRegression(C=1/reg_rate, solver="liblinear")
    pipeline = make_pipeline(StandardScaler(), model)
    pipeline.fit(X_train, y_train)
    y_hat = pipeline.predict(X_test)
    accuracy_score(y_test, y_hat)
    y_scores = pipeline.predict_proba(X_test)
    roc_auc_score(y_test,y_scores[:,1])

    return model
    

def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--training_data", dest='training_data',
                        type=str)
    parser.add_argument("--reg_rate", dest='reg_rate',
                        type=float, default=0.01)
    parser.add_argument("--model_output", dest='model_output',
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
