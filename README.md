[![Author][contributors-shield]][contributors-url]
[![Apache 2.0 License][license-shield]][license-url]
![Version][version-shield]
![example workflow](https://github.com/RaphSku/indata/actions/workflows/ci.yml/badge.svg)
[![InData CD](https://github.com/RaphSku/indata/actions/workflows/cd.yml/badge.svg)](https://github.com/RaphSku/indata/actions/workflows/cd.yml)

# indata
InData is a concise project which enables the user to generate data quality reports with ease and also other data exploration and data visualization tools are available

### Goal
InData should primarily enable the fast generation of data quality reports for continous and categorical features. Additionally, data visualisation tools are integrated which can help to find patterns faster in data.

### How to install it
1. `pip install indata`

### How to use it
If you want to have more insight into how this library works, then I would advise you to look at the numerous unit tests and see how it is used there.
For quick starters, you will have to undertake the following steps in order to use this library:

1. You have to specify where your data is via

```python
dataset    = load.DataSet("./data.csv")
```

2. Then you have to load the data into the Dataloader

```python
dataloader = load.DataLoader(dataset)
```

3. Now you can create an instance of a DataQualityTable

```python
analytics_table = dqt.DataQualityTable(dataloader)
```

4. (optional) You can have a look at the columns and their specifications

```python 
analytics_table.print_header_infos()
```

5. Define which columns in your data refer to continuous and which to categorical features

```python 
continuous_features  = ["Popularity", "Vote_Count", "Vote_Average"]
categorical_features = ["Release_Date", "Title", "Overview", "Original_Language", "Genre", "Poster_Url"]
```

6. Now you are ready to create the data quality report/table for the continuous and categorical features. If you only want the respective table for either categorical features or continuous features, then just pass an empty list to this method:

```python
dqt_cont, dqt_catg = analytics_table.create_table(continuous_features = continuous_features,
                                                  categorical_features = categorical_features,
                                                  store_json_dir = "./dqt")
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

Furthermore, when using the visualisation tools from this package, then these plots will be stored as `html` files in the directory you specified, it is stored as html files such that you can inspect the plot in more detail, thus it is an interactive plot.
  
[contributors-url]: https://github.com/RaphSku
[license-url]: https://github.com/RaphSku/indata/blob/main/LICENSE

[contributors-shield]: https://img.shields.io/badge/Author-RaphSku-orange?style=plastic&labelColor=black
[license-shield]: https://img.shields.io/badge/License-Apache%202.0-informational?style=plastic&labelColor=black
[version-shield]: https://img.shields.io/badge/Version-1.0.0-red?style=plastic&labelColor=black
