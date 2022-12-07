# International Judo Federation (IJF) World Ranking: Scraping, ETL process and PowerBI Dashboard (Project Overview)

Welcome! In this project I want to show a bit of Data Engineering and Data Analysis through the use of the API that contains the World Ranking for the International Judo Federation.

It consists in two parts:

- A Extraction, Transformation and Loading (ETL) of the Data with Python

- A Display of a Power BI Dashboard with GitHub Pages.

## Objetive
The objetive is:

- Create a Python Script that scraps the Data From the World Ranking of the International Judo Federation 

- Transform the Data in order to load it into CSV files that will later feed a Power Bi Dashboard

- Display and Analyse the information from the World Ranking on PowerBI

- Publish the Data in a website through GitHub Pages


## Tools Used
Python:

- Requests (library) - For Scrappin the Data
- Pandas (Library) - for Manipulating the Data in a tabular form

Power BI - For Data Visualization and Analysis

HTML - For Deploying the data on GitHub Pages

## The Data
The IJF is tghe highest entity of Judo in the World. Among all the thing it does, they are in charge of the international competitions that prepare competitors all around the globe fot the Olympic Games. Usually the 32 best competitors in the world ranking get to go to this competition for each different weight category of competition.

The IJF Api returns a JSON object that contains a list with information of each competitor.
The info it contains is:

- **id** - String (Identifier)

- **sum_points** - Numeric (Points in the World Rankinf for competing)

- **place** - Numeric (Position in the World Ranking)

- **place_prev** - Numeric (Position before changing)

- **id_person** - String (Identifier for the competitor)

- **family_name** - String

- **given_name** - String

- **gender** - String

- **timestamp_version** - String

- **id_country** - String (Identifier for country)

- **country_name** - String

- **country_ioc_code** - String (ioc: Internation Olympic Comitee)

- **id_continent** - String (Identifier for continent)

- **id_weight** - String (Identifier for weight category)

- **weight_name** - String (Competition category)

- **score_parts** - list with dictionaries of the competitions the competitor participated

    - **Points** - Numeric (Obtained in the competition)
    - **competition** - Dictionary contains:
        - Competition Id
        - Competition Name
        - Date of the competition
    - **place** - Numeric (Result in the competition)
    - **long_place** - String (Categorical Result in the competition)

## ETL, Visualization and Deploying Process

### ETL with Python

We extract the data with Python using the Requests library. With the Pandas librarie we transform the JSON object into a DataFrame in which each row was a competition in which a competitor participated (normalized in the "score_parts" key of the competitors in the World Ranking). The we loaded the data into 6 different CSV files that would feed out PowerBI Dashboard:

- First a competitors Dimension: **dim_competitors**

- Weight category dimension: **dim_weight_category**

- Country Dimension: **dim_country**

- Continent Dimension: **dim_continent**

- Competitions Dimension: **dim_competition**

- Fact table from each competition a player has been, with his respective points for the World Ranking and result: **fact_tournament_results**

### Visualization on PowerBI

From the created tables, 4 Pages were designed on PowerBI: Two for Countries Analysis, One for Competitors and One particular for Colombian Competitors.

The PowerBI dashboard was published in order to be deployed in a website

### Web Deployment with HTML and GitHub Pages

An index.html document was created with the insertion of the Dashboard from PowerBI Service.

Then it was deployed on GitHub pages.

Link: https://santigarzond.github.io/IJF_WR_Scrap_and_Dashboard/