# -*- coding: utf-8 -*-

import click
import pandas as pd

import dataviz.data as dz_data


@click.group()
def cli():
    """Python scripts used in project."""
    pass


@cli.command()
@click.option(
    "-f", "--infile", nargs=3, type=click.STRING, multiple=True,
    help="A file with the atoms per unit cell and a label to read and process."
)
@click.option(
    "-o", "--output", default="dos.csv", nargs=1,
    type=click.Path(file_okay=True,
                    dir_okay=False), help="Output path to use for saving dos CSV file."
)
@click.argument("path", type=click.Path(exists=True, dir_okay=True, file_okay=False))
def dos2csv(path, output, infile):
    dos_df: pd.DataFrame = dz_data.read_dos(
        dir=path,
        filename_and_mag_order=infile,
    )
    dos_df.to_csv(path_or_buf=output, index=False)


@cli.command()
@click.option(
    "-f", "--infile", nargs=3, type=click.STRING, multiple=True,
    help="A file with energy points per symmetry line and a label to read and process."
)
@click.option(
    "-o", "--output", default="bands.csv", nargs=1,
    type=click.Path(file_okay=True, dir_okay=False),
    help="Output path to use for saving bands CSV file."
)
@click.argument("path", type=click.Path(exists=True, dir_okay=True, file_okay=False))
def bands2csv(path, output, infile):
    bands_df: pd.DataFrame = dz_data.read_bands(
        dir=path,
        filename_and_e_points_and_mag_order=infile,
    )
    bands_df.to_csv(path_or_buf=output, index=False)
