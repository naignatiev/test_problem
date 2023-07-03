import os

import requests
from sklearn.datasets import *
import pandas as pd
import click

from config import Config
from extra_datasets import load_extra


@click.group
def cli():
    pass


@cli.command()
def fill_database():
    """ Upload test and scikit-learn toy datasets"""
    for dataset_f in (load_iris, load_diabetes, load_linnerud, load_wine, load_breast_cancer, load_extra):
        # load_diabetes has no "filename" attr
        filename = get_filename_from_funcname(dataset_f.__name__)

        dataset = dataset_f()
        pd.DataFrame(dataset.data, columns=dataset.feature_names).to_csv(filename, index=False)

        with open(filename, 'rb') as f:
            data = f.read()
        # TODO: avoid try-except block. add ping
        try:
            response = requests.post(f'http://localhost:{Config.PORT}/api/dataset', data=data,
                                     headers={'File-Name': filename, 'Content-Type': 'text/csv'})
            if response.status_code != 200:
                click.echo(click.style(f'Error. response.text: {response.text} Check flask log.', fg='red'))
                return
        except requests.exceptions.ConnectionError:
            click.echo(click.style('API service not responding. Are you sure the service is running?', fg='yellow'))
            return

        os.remove(filename)

    click.echo(click.style('Success!', fg='green'))


def get_filename_from_funcname(funcname: str) -> str:
    return f"{'_'.join(funcname.split('_')[1:])}.csv"


@cli.command()
def drop_database():
    """ Clear all data """
    if input('Are you sure?[y/n]: ') != 'y':
        return
    if os.path.exists('data'):
        for filename in os.listdir('data'):
            os.remove(os.path.join('data', filename))
    # TODO: doesn't work if change SQLALCHEMY_DATABASE_URI in config
    if os.path.exists('instance/data.db'):
        os.remove('instance/data.db')
    click.echo(click.style('Success!', fg='green'))


if __name__ == '__main__':
    cli()
