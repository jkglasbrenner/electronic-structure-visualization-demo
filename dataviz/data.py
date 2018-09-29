# -*- coding: utf-8 -*-

import inspect
import json
from pathlib import Path
from typing import List, Tuple, Union

import pandas as pd
import scipy.constants

module_directory: Path = Path(inspect.getfile(inspect.currentframe())).absolute().parent


def read_dos(dir: str, filename_and_mag_order: List[Tuple[str, str, str]]) -> pd.DataFrame:
    """Read in the density of states data and store in a data frame.

    :param str dir: Directory path to density of states data files.
    :param list filename_and_mag_order: A list of tuples that list and label each file
        to read and process.
    :return: Data frame containing density of states data.
    """
    dir: Path = Path(dir)
    dos: Union[pd.DataFrame, None] = None

    for filename, atoms_per_cell, mag_order in filename_and_mag_order:
        path: Path = dir / filename
        tdos: pd.DataFrame = read_tdos_file(
            path=path,
            atoms_per_cell=int(atoms_per_cell),
            magnetic_order=mag_order
        )

        if dos is None:
            dos = tdos.copy()

        else:
            dos = dos.merge(right=tdos, how="outer")

    return dos


def read_bands(
    dir: str,
    filename_and_e_points_and_mag_order: List[Tuple[str, int, str]],
) -> pd.DataFrame:
    """Read in the bands data and store in a data frame.

    :param str dir: Directory path to bands data files.
    :param list filename_and_e_points_and_mag_order: A list of tuples that lists each file
        to read and process, along with the number energy points per symmetry line and a
        label for the magnetic ordering.
    :return: Data frame containing bands data.
    """
    dir: Path = Path(dir)
    bands: Union[pd.DataFrame, None] = None

    for filename, e_points, mag_order in filename_and_e_points_and_mag_order:
        path: Path = dir / filename
        species_bands: pd.DataFrame = read_bands_file(
            path=path, e_points=int(e_points), magnetic_order=mag_order
        )

        if bands is None:
            bands = species_bands.copy()

        else:
            bands = bands.merge(right=species_bands, how="outer")

    return bands


def load_plotly_settings():
    plotly_settings_path: Path = module_directory / "configurations/plotly_config.json"
    with plotly_settings_path.open(mode="r") as jsonfile:
        plotly_settings = json.load(jsonfile)

    return plotly_settings


def read_tdos_file(path: str, atoms_per_cell: int, magnetic_order: str) -> pd.DataFrame:
    path: Path = Path(path)
    eV_conversion: float = \
        scipy.constants.physical_constants["Hartree energy in eV"][0]
    dos_df: pd.DataFrame = pd.read_table(
        filepath_or_buffer=path, sep="\s+", header=None, names=["energy", "dos"]
    )

    observations_per_spin: int = int(len(dos_df) / 2)

    return dos_df \
        .assign(dos=lambda x: x["dos"] / eV_conversion / atoms_per_cell) \
        .assign(energy=lambda x: x["energy"] * eV_conversion) \
        .assign(spin=observations_per_spin * ["up"] +
                     observations_per_spin * ["down"]) \
        .assign(mag_order=magnetic_order) \
        .loc[:, ["energy", "mag_order", "spin", "dos"]]


def read_bands_file(path: str, e_points: int, magnetic_order: str) -> pd.DataFrame:
    path: Path = Path(path)
    eV_conversion: float = \
        scipy.constants.physical_constants["Hartree energy in eV"][0]
    bands_df: pd.DataFrame = pd.read_table(
        filepath_or_buffer=path, sep="\s+", header=None, names=[
            "kpoint", "energy", "weight_tot", "weight_s", "weight_p", "weight_d",
            "weight_f"
        ]
    )

    observations_per_spin: int = int(len(bands_df) / 2)
    bands_per_spin: int = int(observations_per_spin / e_points)
    band_labels: List[int] = 2 * [
        band_number for band_number in list(range(1, bands_per_spin + 1))
        for _ in range(200)
    ]

    return bands_df \
        .assign(energy=lambda x: x["energy"] * eV_conversion) \
        .assign(spin=observations_per_spin * ["up"] +
                     observations_per_spin * ["down"]) \
        .assign(band=band_labels) \
        .assign(mag_order=magnetic_order) \
        .loc[:, ["kpoint", "band", "spin", "mag_order", "energy", "weight_tot",
                 "weight_s", "weight_p", "weight_d", "weight_f"]]
