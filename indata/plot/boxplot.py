"""Plotting boxplots"""

import os
import pandas as pd
import plotly.graph_objects as go
from abc import abstractmethod


#################################################################################################
#                             Interface Boxplot Plotter                                         #
#################################################################################################

class IFBoxPlot:
    """Interface for the BoxPlot classes
    Boxplot is plotting data in order to get a better
    feeling about the dispersion in the data
    """

    @abstractmethod
    def plot(self, store_dir: str): # pragma: no cover
        pass


#################################################################################################
#                                   Boxplot Plotter                                             #
#################################################################################################

class BoxPlot(IFBoxPlot):
    """Visualisation of data in form of a boxplot
    
    Methods
    -------
        plot(store_dir: str)
            Plots the boxplot and stores it to a user-defined directory
    """

    def __init__(self, name: str, data: pd.DataFrame):
        """Initialises the BoxPlot

        Parameters
        ----------
        name : str
            Name of the feature
        data : pd.DataFrame
            Data of the feature
        """
        self.name = name
        self.data = data


    def plot(self, store_dir: str) -> None:
        """Plots the boxplot and stores it to a directory

        Parameters
        ----------
        store_dir : str
            A html file containing an interactive plot is stored to `store_dir`
        """
        if not os.path.exists(store_dir):
            os.mkdir(store_dir)
        if not os.path.exists(os.path.join(store_dir, "boxplots")):
            os.mkdir(f"{store_dir}/boxplots")

        fig = go.Figure()
        fig.add_trace(go.Box(x = self.data,
                             name = "",
                             marker_color = "darkblue",
                             boxmean = True))
        fig.update_layout(
            title       = {'font': {'size': 30}, 'text': f"{self.name} - Boxplot"},
            xaxis_title = f"{self.name}",
            xaxis       = {'tickfont': {'size': 15}, 'titlefont': {'size': 25}}
        )
        fig.write_html(f"{store_dir}/boxplots/{self.name}.html")