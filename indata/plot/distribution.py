"""All plotter which visualise distributions of features"""

import os
import pandas as pd
import plotly.graph_objects as go
from abc import abstractmethod


#################################################################################################
#                                 Interface DistributionPlotter                                 #
#################################################################################################

class IFDistributionPlotter:
    """ Interface for the DistributionPlotters """

    @abstractmethod
    def plot(self, store_dir: str): # pragma: no cover
        pass


#################################################################################################
#                                 ContinuousDistributionPlotter                                 #
#################################################################################################

class ContinuousDistributionPlotter(IFDistributionPlotter):
    """Plots distribution of a continuous feature in form of a histogram
    and add marks for important values like mean and median

    Methods
    -------
        plot(store_dir: str)
            Plotting a histogram of a continuous feature
    """

    def __init__(self, name: str, data: pd.DataFrame, dqt: pd.DataFrame):
        """Initialises the ContinuousDistributionPlotter

        Parameters
        ----------
            name : str
                Name of the feature which will be plotted
            data : pd.DataFrame
                Column of a dataframe which represents the data of the feature
            dqt : pd.DataFrame
                The data quality table from which information like mean and median
                are extracted
        """
        self.name = name
        self.data = data
        self.dqt  = dqt


    def plot(self, store_dir: str) -> None:
        """Plotting a histogram of a continuous feature

        Parameters
        ----------
        store_dir : str
            A html file containing an interactive plot is stored to `store_dir`
        """
        if not os.path.exists(store_dir):
            os.mkdir(store_dir)
        if not os.path.exists(os.path.join(store_dir, "continuous")):
            os.mkdir(f"{store_dir}/continuous")

        first_quantile = self.dqt["1st Qrt."][self.name]
        mean           = self.dqt["mean"][self.name]
        median         = self.dqt["median"][self.name]
        third_quantile = self.dqt["3rd Qrt."][self.name]

        fig = go.Figure(data = [go.Histogram(x = self.data)])
        fig.add_vline(x = first_quantile, line_dash = "dash", line_color = "red", annotation_text = "1st Q.")
        fig.add_vline(x = mean, line_dash = "dash", line_color = "orange", annotation_text = "mean")
        fig.add_vline(x = median, line_dash = "dash", line_color = "yellow", annotation_text = "median")
        fig.add_vline(x = third_quantile, line_dash = "dash", line_color = "green", annotation_text = "3rd Q.")
        fig.update_layout(
            title       = {'font': {'size': 30}, 'text': f"{self.name} - Distribution"},
            xaxis_title = f"{self.name.lower()}",
            yaxis_title = "frequency/a.u.",
            xaxis       = {'tickfont': {'size': 15}, 'titlefont': {'size': 25}},
            yaxis       = {'tickfont': {'size': 15}, 'titlefont': {'size': 25}}
        )
        fig.write_html(f"{store_dir}/continuous/{self.name}.html")


#################################################################################################
#                                 CategoricalDistributionPlotter                                #
#################################################################################################

class CategoricalDistributionPlotter(IFDistributionPlotter):
    """Plots the distribution of a categorical feature in form of a bar plot

    Methods
    -------
        plot(store_dir: str)
            Stores the plot to the `store_dir` directory
    """
    def __init__(self, name: str, data: pd.DataFrame, label_hash: dict, dqt: pd.DataFrame = None):
        """Initialises the CategoricalDistributionPlotter

        Parameters
        ----------
        name : str
            Name of the categorical feature
        data : pd.DataFrame
            Data of the categorical feature
        label_hash : dict
            Hashes the observed distinct categories to its frequencies
        dqt : pd.DataFrame, optional
            Data quality table associated with the categorical feature, defaults to None
        """
        self.name       = name
        self.data       = data
        self.dqt        = dqt
        self.label_hash = label_hash


    def plot(self, store_dir: str) -> None:
        """Plots the categorical feature as a bar plot, the distinct categories
        are plotted on the x-axis and their respective frequencies on the y-axis

        Parameters
        ----------
        store_dir : str
            A html file containing an interactive plot is stored to `store_dir`
        """
        if not os.path.exists(store_dir):
            os.mkdir(store_dir)
        if not os.path.exists(os.path.join(store_dir, "categorical")):
            os.mkdir(f"{store_dir}/categorical")

        fig = go.Figure(data = [go.Bar(x = list(self.label_hash.keys()), y = list(self.label_hash.values()))])
        fig.update_layout(
            title       = {'font': {'size': 30}, 'text': f"{self.name} - Distribution"},
            xaxis_title = f"{self.name.lower()}",
            yaxis_title = "frequency/a.u.",
            xaxis       = {'tickfont': {'size': 15}, 'titlefont': {'size': 25}},
            yaxis       = {'tickfont': {'size': 15}, 'titlefont': {'size': 25}}
        )
        fig.write_html(f"{store_dir}/categorical/{self.name}.html")