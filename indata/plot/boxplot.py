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
    def plot(self): # pragma: no cover
        pass


#################################################################################################
#                                   Boxplot Plotter                                             #
#################################################################################################

class BoxPlot(IFBoxPlot):
    """Visualisation of data in form of a boxplot
    
    Methods
    -------
        plot()
            Plots the boxplot and stores it to a user-defined directory `store_dir`
    """

    def __init__(self, name: str, data: pd.DataFrame, store_dir: str = "./"):
        """Initialises the BoxPlot

        Parameters
        ----------
        name : str
            Name of the feature
        data : pd.DataFrame
            Data of the feature
        store_dir : str, default = "./"
            A html file containing an interactive plot is stored to `store_dir`
        """
        self.name      = name
        self.data      = data
        self.store_dir = store_dir


    def plot(self) -> None:
        """Plots the boxplot and stores it to a directory"""
        if not os.path.exists(self.store_dir):
            os.mkdir(self.store_dir)
        if not os.path.exists(os.path.join(self.store_dir, "boxplots")):
            os.mkdir(f"{self.store_dir}/boxplots")

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
        fig.write_html(f"{self.store_dir}/boxplots/{self.name}.html")