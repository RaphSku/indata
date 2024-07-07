# ARCHIVED

[![Apache 2.0 License][license-shield]][license-url]
![example workflow](https://github.com/RaphSku/indata/actions/workflows/ci.yml/badge.svg)
[![InData CD](https://github.com/RaphSku/indata/actions/workflows/cd.yml/badge.svg)](https://github.com/RaphSku/indata/actions/workflows/cd.yml)

# indata
InData is a concise project which enables the user to generate data quality reports with ease. Data exploration and data visualisation tools are also provided for convenience.

### How to install it
```bash 
pip install indata
```

### How it is organised
```bash
.
└── indata/
    ├── dataio
    ├── table
    ├── plot
    └── utils
```

### How to use it

#### dataio
Provides you with everything you need in order to define the data source
```python
dataset = indata.dataio.DataSet("./data.csv")
```
and get it loaded
```python
dataloader = indata.dataio.DataLoader(dataset)
```

#### table
After you have defined your data source and constructed out of it a loader, you can start creating a data quality report
```python
analytics_table = indata.table.DataQualityTable(dataloader)
```
Now, if you want, you can have a look at the columns and what data type they have
```python
analytics_table.print_header_infos()
```
Define which columns you want to investigate and which columns are continous and which are categorical. With these information, you can kick-off the creation of the data quality report
```python
continuous_features  = ["Popularity", "Vote_Count", "Vote_Average"]
categorical_features = ["Release_Date", "Title", "Overview", "Original_Language", "Genre", "Poster_Url"]

dqt_cont, dqt_catg = analytics_table.create_table(continuous_features = continuous_features,
                                                  categorical_features = categorical_features,
                                                  store_json_dir = "./dqt")
```
In the folder `./dqt` you will find two json files, one for the categorical features and one for the continous features. Each file represents a data quality report for the respective group of features.

### Advanced Usage
#### Transformer
If you have looked into what the different packages have to offer, you will notice that the `DataLoader` accepts another optional parameter called `transformer` which is an instance of the `indata.dataio.Transformer` class. A transformer acts on the dataframe and transforms the columns according to a defined transformer function. For instance, you can define the following Transformer
```python
transformer = indata.dataio.Transformer(columns = ["column1"], funcs = indata.dataio.impute_median)
dataloader  = indata.dataio.DataLoader(dataset)
dataloader.read_csv(transformer = transformer)
```
which will impute the missing values with the median.

#### Plotting
Currently, there are 3 supported plots: **boxplots**, **distribution plots** and **SPLOMS**. Let's see how fast we can create plots out of our data. All you need to get started is a dataframe with some data in it.

##### Boxplots
```python
boxplot = indata.plot.BoxPlot(name = "Some nice Boxplot", data = df["column1"], store_dir = "./")
boxplot.plot()
```
This will create a boxplot for `column1` and will create a directory `plots/boxplots/` at `store_dir` which will hold the `.html` files. These you can open and interactively explore the boxplot.

##### Distribution Plots
Distribution plots come in two flavours, a distribution plotter for categorical features and one for continous features. The distribution plotter expect two additional parameters, one is the data quality report and a `label_hash`. The data quality report is needed because statistics are extracted from it and plotted inside of the visualisation to enrich it with further details. And `label_hash` is only used for the categorical distribution plotter, you do not need to bother what it does, just use the utility function as you can see below
```python
cdist      = indata.plot.ContinuousDistributionPlotter(name = "Some Feature", data = data["feature1"], dqt = cqt,
                                                       store_dir = "./")
cdist.plot()

label_hash = indata.utils.count.Categories.count(data = df["feature2"]
cat_dist   = indata.plot.CategoricalDistributionPlotter(name = "Some other Feature", data = df["feature2"], dqt = cat_qt, label_hash = label_hash,
                                                        store_dir = "./")
cat_dist.plot()
```

##### SPLOM
SPLOM stands for scatterplot matrix and is essentially a matrix of plots where each feature gets plotted against each other. This is useful if you want to investigate linear relationships between the features with just one glance. You can create a SPLOM as simple as running
```python
splom = indata.plot.SPLOM(name = "SPLOM", continuous_data = data[["feature1", "feature2", "feature3"]], 
                          store_dir = "./")
```

### Results
In this case, I want to show some results which I got when using this library on a movie dataset which contains different movie titles and their popularity.

We get the following data quality report for the continuous features of that dataset:
```json
{
    "Count": {
        "Popularity": 9827,
        "Vote_Count": 9827,
        "Vote_Average": 9827
    },
    "Miss. %": {
        "Popularity": 0.1016570093,
        "Vote_Count": 0.1016570093,
        "Vote_Average": 0.1016570093
    },
    "Card.": {
        "Popularity": 8160,
        "Vote_Count": 3267,
        "Vote_Average": 75
    },
    "Min": {
        "Popularity": 7.1,
        "Vote_Count": 7.1,
        "Vote_Average": 7.1
    },
    "1st Qrt.": {
        "Popularity": 16.1275,
        "Vote_Count": 16.1275,
        "Vote_Average": 16.1275
    },
    "mean": {
        "Popularity": 40.3205699603,
        "Vote_Count": 40.3205699603,
        "Vote_Average": 40.3205699603
    },
    "median": {
        "Popularity": 21.191,
        "Vote_Count": 21.191,
        "Vote_Average": 21.191
    },
    "3rd Qrt.": {
        "Popularity": 35.1745,
        "Vote_Count": 35.1745,
        "Vote_Average": 35.1745
    },
    "Max": {
        "Popularity": 5083.954,
        "Vote_Count": 5083.954,
        "Vote_Average": 5083.954
    },
    "Std. Dev.": {
        "Popularity": 108.8743077303,
        "Vote_Count": 108.8743077303,
        "Vote_Average": 108.8743077303
    }
}
```

And a data quality report for the categorical features:
```json
{
    "Count": {
        "Release_Date": 9837,
        "Title": 9828,
        "Overview": 9828,
        "Original_Language": 9827,
        "Genre": 9826,
        "Poster_Url": 9826
    },
    "Miss. %": {
        "Release_Date": 0.0,
        "Title": 0.0914913083,
        "Overview": 0.0914913083,
        "Original_Language": 0.1016570093,
        "Genre": 0.1118227102,
        "Poster_Url": 0.1118227102
    },
    "Card.": {
        "Release_Date": 5903,
        "Title": 9514,
        "Overview": 9823,
        "Original_Language": 44,
        "Genre": 2337,
        "Poster_Url": 9826
    },
    "Mode": {
        "Release_Date": "2022-03-10",
        "Title": "Beauty and the Beast",
        "Overview": "Dr. Raichi is one of the only survivors of the Tuffles, a race that once lived on Planet Plant before the coming of the Saiyans. The Saiyans not only massacred the entire Tuffle race, but also stole their technology and conquered the planet, renaming it Planet Vegeta in honor of their king. Raichi managed to escape with a capsule and found refuge on the Dark Planet, a world at the end of the universe. His only wish is to eradicate the last remaining Saiyans.",
        "Original_Language": "en",
        "Genre": "Drama",
        "Poster_Url": "https:\/\/image.tmdb.org\/t\/p\/original\/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg"
    },
    "Mode Freq.": {
        "Release_Date": 16,
        "Title": 4,
        "Overview": 2,
        "Original_Language": 7569,
        "Genre": 466,
        "Poster_Url": 1
    },
    "Mode Freq. %": {
        "Release_Date": 0.1626512148,
        "Title": 0.0407000407,
        "Overview": 0.0203500204,
        "Original_Language": 77.0224890608,
        "Genre": 4.7425198453,
        "Poster_Url": 0.0101770812
    },
    "2nd Mode": {
        "Release_Date": "2022-03-09",
        "Title": "Alice in Wonderland",
        "Overview": "Wilbur the pig is scared of the end of the season, because he knows that come that time, he will end up on the dinner table. He hatches a plan with Charlotte, a spider that lives in his pen, to ensure that this will never happen.",
        "Original_Language": "ja",
        "Genre": "Comedy",
        "Poster_Url": "https:\/\/image.tmdb.org\/t\/p\/original\/deOzvJHnSSl8FI1HEJjPGgOsS9U.jpg"
    },
    "2nd Mode Freq.": {
        "Release_Date": 15,
        "Title": 4,
        "Overview": 2,
        "Original_Language": 645,
        "Genre": 403,
        "Poster_Url": 1
    },
    "2nd Mode Freq. %": {
        "Release_Date": 0.1524855139,
        "Title": 0.0407000407,
        "Overview": 0.0203500204,
        "Original_Language": 6.5635494047,
        "Genre": 4.1013637289,
        "Poster_Url": 0.0101770812
    }
}
```


  
[contributors-url]: https://github.com/RaphSku
[license-url]: https://github.com/RaphSku/indata/blob/main/LICENSE

[license-shield]: https://img.shields.io/badge/License-Apache%202.0-orange
