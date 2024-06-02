import os
import pickle

import click
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error
import mlflow


def load_pickle(filename: str):
    with open(filename, 'rb') as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    '--data_path',
    default='./output',
    help='Location where the processed NYC taxi trip data was saved'
)
@click.option(
    '--tracking_uri',
    default='http://127.0.0.1:5000',
    help='URI to connect to MLFlow'
)
def run_train(data_path: str, tracking_uri: str):

    X_train, y_train = load_pickle(os.path.join(data_path, 'train.pkl'))
    X_val, y_val = load_pickle(os.path.join(data_path, 'val.pkl'))

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment('green-taxi-regression')
    mlflow.sklearn.autolog(log_datasets=False)
    
    with mlflow.start_run():
    
        rf = RandomForestRegressor(max_depth=10, random_state=0)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)
    
        rmse = root_mean_squared_error(y_val, y_pred)


if __name__ == '__main__':
    run_train()
