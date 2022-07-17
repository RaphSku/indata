"""Scatter Plot Matrix with Correlation Coefficients"""

import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from abc import abstractmethod
from plotly.subplots import make_subplots


#################################################################################################
#                                    Interface SPLOM                                            #
#################################################################################################

class IFSPLOM:
    """Interface for the SPLOM classes, SPLOM
    classes are used in order to have a simple visualisation
    of the features and their correlation between each other
    """

    @abstractmethod
    def plot(self): # pragma: no cover
        pass


#################################################################################################
#                                         SPLOM                                                 #
#################################################################################################

class SPLOM:
    """Visualisation of the correlation of the features 
    in form of a Scatter Plot Matrix. A Scatter Plot Matrix
    is quadratic and its dimension is equal to the number of
    features
    
    Methods
    -------
        plot()
            Plots the SPLOM and stores it to a user-defined directory `store_dir`
    """

    def __init__(self, name: str, continuous_data: pd.DataFrame, store_dir: str = "./"):
        """Initialises the SPLOM

        Parameters
        ----------
        name : str
            Name of the SPLOM
        data : pd.DataFrame
            Data of the features which should be plotted against each other
        store_dir : str, default = "./"
            A html file containing an interactive plot is stored to `store_dir`
        """
        self.name            = name
        self.continuous_data = continuous_data
        self.store_dir       = store_dir
        
    
    def plot(self) -> None:
        """Plots the SPLOM and stores the plot inside of `store_dir`"""
        if not os.path.exists(self.store_dir):
            os.mkdir(self.store_dir)
        if not os.path.exists(os.path.join(self.store_dir, "splom")):
            os.mkdir(f"{self.store_dir}/splom")

        dimension = len(self.continuous_data.columns)

        columns   = self.continuous_data.columns.to_numpy()
        labels    = []
        for row in range(dimension):
            for col in range(dimension):
                labels.append(columns[row])
        labels = np.resize(np.array(labels), (dimension, dimension))

        subplot_titles = []
        for row in range(dimension):
            for col in range(dimension):
                subplot_titles.append(f"{labels[row][col]} vs. {labels[col][row]}")

        fig = make_subplots(rows = dimension, cols = dimension, subplot_titles = subplot_titles)
        for row in range(dimension):
            for col in range(dimension):
                fig.add_trace(
                    go.Scatter(x = self.continuous_data[labels[row][col]], y = self.continuous_data[labels[col][row]], mode = 'markers', name = ""),
                    row = int(row + 1), col = int(col + 1)
                )
                fig.update_xaxes(title_text = labels[row][col], row = int(row + 1), col = int(col + 1))
                fig.update_yaxes(title_text = labels[col][row], row = int(row + 1), col = int(col + 1))

        fig.update_layout(
            title_text = "Scatter Plot Matrix",
            showlegend = False
        )
        fig.write_html(f"{self.store_dir}/splom/{self.name}.html")