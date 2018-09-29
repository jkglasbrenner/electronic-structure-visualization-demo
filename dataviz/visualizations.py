# -*- coding: utf-8 -*-

from typing import Dict, List

from IPython.display import clear_output, display
from ipywidgets import interact, interactive, fixed, FloatText, RadioButtons
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.offline as py
from plotly.colors import DEFAULT_PLOTLY_COLORS

import dataviz.data


def visualize_dos_with_plotly(
    df: pd.DataFrame,
    mag_order_list: List[str],
):
    figure: Dict = dataviz.data.load_plotly_settings().get("figure")
    append_plotly_dos_trace(df=df, figure=figure, mag_order=mag_order_list[1])
    append_plotly_dos_frames(df=df, figure=figure, mag_order_list=mag_order_list)
    py.iplot(figure, config={"scrollzoom": False})


def visualize_bands_with_plotly():
    pass


def visualize_dos_with_matplotlib(
    df: pd.DataFrame,
    xmin: float,
    xmax: float,
    mag_order_list: List[str],
    update_function,
    dpi: int = 120,
    style: str = "k-",
):
    xmin: FloatText = FloatText(xmin, description="Energy minimum")
    xmax: FloatText = FloatText(xmax, description="Energy maximum")
    mag_order: RadioButtons = RadioButtons(
        options=mag_order_list,
        description="magnetic order",
    )

    interactive_window: interactive = interactive(
        update_function,
        df=fixed(df),
        xmin=xmin,
        xmax=xmax,
        mag_order=mag_order,
        dpi=dpi,
        style=style,
    )

    return interactive_window


def visualize_bands_with_matplotlib():
    pass


def append_plotly_dos_trace(df: pd.DataFrame, figure: Dict, mag_order: str) -> None:
    energy_up: np.ndarray = df \
        .query(f"mag_order == '{mag_order}' & spin == 'up'") \
        .loc[:, "energy"] \
        .values
    dos_up: np.ndarray = df \
        .query(f"mag_order == '{mag_order}' & spin == 'up'") \
        .loc[:, "dos"] \
        .values

    energy_down: np.ndarray = df \
        .query(f"mag_order == '{mag_order}' & spin == 'down'") \
        .loc[:, "energy"] \
        .values
    dos_down: np.ndarray = df \
        .query(f"mag_order == '{mag_order}' & spin == 'down'") \
        .loc[:, "dos"] \
        .values

    figure["data"].extend([
        {
            "type": 'scatter',
            "x": energy_up,
            "y": dos_up,
            "mode": "lines",
            "line": {
                "color": DEFAULT_PLOTLY_COLORS[0]
            }
        },
        {
            "type": "scatter",
            "x": energy_down,
            "y": dos_down,
            "mode": "lines",
            "line": {
                "color": DEFAULT_PLOTLY_COLORS[0]
            }
        },
    ])


def append_plotly_dos_frames(
    df: pd.DataFrame,
    figure: Dict,
    mag_order_list: List[str],
) -> None:
    for mag_order in mag_order_list:
        energy_up: np.ndarray = df \
            .query(f"mag_order == '{mag_order}' & spin == 'up'") \
            .loc[:, "energy"]
        dos_up: np.ndarray = df \
            .query(f"mag_order == '{mag_order}' & spin == 'up'") \
            .loc[:, "dos"]

        energy_down: np.ndarray = df \
            .query(f"mag_order == '{mag_order}' & spin == 'down'") \
            .loc[:, "energy"]
        dos_down: np.ndarray = df \
            .query(f"mag_order == '{mag_order}' & spin == 'down'") \
            .loc[:, "dos"]

        figure["frames"].append({
            "data": [
                {
                    "x": energy_up,
                    "y": dos_up,
                    "type": "scatter",
                    "mode": "lines",
                },
                {
                    "x": energy_down,
                    "y": dos_down,
                    "type": "scatter",
                    "mode": "lines",
                },
            ],
            "name":
            mag_order,
        })


def update_matplotlib_dos_plot(
    df: pd.DataFrame,
    xmin: float,
    xmax: float,
    mag_order: List[str],
    dpi: int,
    style: str,
):
    energy: pd.DataFrame = df \
        .query(f"mag_order == '{mag_order}' & spin == 'up'") \
        .loc[:, "energy"]
    dos_up: pd.DataFrame = df \
        .query(f"mag_order == '{mag_order}' & spin == 'up'") \
        .loc[:, "dos"]
    dos_down: pd.DataFrame = df \
        .query(f"mag_order == '{mag_order}' & spin == 'down'") \
        .loc[:, "dos"]

    clear_output(wait=True)

    fig, ax = plt.subplots(dpi=dpi)

    ax.plot(energy, dos_up, style, label=f"{mag_order}")
    ax.plot(energy, dos_down, style, label=f"{mag_order}")

    ax.set_xlim([xmin, xmax])

    ax.set_xlabel("Energy (eV)")
    ax.set_ylabel("DOS (states/eV/atom)")
