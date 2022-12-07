# Import libreries
import requests # For connecting with the IJF API
import pandas as pd # For maninpulating the data in a tabular way

# Create a loop and a starting value for it
page = 0

# Create the object that will be containing the data
world_ranking = pd.DataFrame()

# Loop
while True:
    
    # IFJ API URL
    url = f'https://www.ijf.org/internal_api/wrl?category=all&page={page}'

    # We set the request of the API
    # The API extracts the info in batches of 100 competitors per page
    r = requests.get(url=url)
    
    # Try to read the data requested from the API as a JSON object
    # If it returns an error, the While Loop will break
    try:
        # Read the request as a JSON
        data = r.json()

        # We extract the list that contains each of the competitor from the "feed" key
        data_list = data['feed']

        # Another break in case the API does not return an error
        if len(data_list)==0:
            break

        # Now we iterate through each competitor in the list
        # for deleting Null values in the "score_parts" list for each competitor
        # (If we don't do this the it raises an erroer when normalizing in Pandas)
        for competitor in data_list:

            competitor['score_parts'] = list(filter(None, competitor['score_parts']))

        # Now we add the info into an auxiliar Pandas DataFrame
        # We will extract the info of each competition the competitor have competed.
        # That's why we use the "score_parts" as the Path to normalize
        df_aux = pd.json_normalize(data_list, 'score_parts',[
            'id',
            'sum_points',
            "place",
            "place_prev",
            "id_person",
            "family_name",
            "given_name",
            "gender",
            "timestamp_version",
            "id_country",
            "country_name",
            "country_ioc_code",
            "id_continent",
            "id_weight",
            "weight_name"
            ], # We keep columns that are not on "score_parts"
             meta_prefix='competitor.') # We add them a prefix

        # We concat the info we just extracted into the worl_ranking DF
        world_ranking = pd.concat([world_ranking, df_aux])
    
    except:
        print('except')
        break
    
    # I print the Page we just iterate through in order to
    # keep track of how many pages we connected
    print(page)
    page += 1    

# Save that DF on a csv File
world_ranking.to_csv('competitor.csv')

# -------------------------------------

# Let's create the tables that will feed my PowerBI Dashboard

# First a competitors Dimension
dim_competitors = world_ranking[[
            'competitor.id',
            'competitor.sum_points',
            "competitor.place",
            "competitor.place_prev",
            "competitor.id_person",
            "competitor.family_name",
            "competitor.given_name",
            "competitor.gender",
            "competitor.timestamp_version",
            "competitor.id_country",
            "competitor.id_weight",]].drop_duplicates(
                subset=['competitor.id']
                )

# Weight category dimension
dim_weight_category = world_ranking[
    ['competitor.id_weight',
     'competitor.weight_name',
     'competitor.gender']
     ].drop_duplicates().sort_values(
        ['competitor.id_weight']
        ).reset_index(drop=True)

# Country Dimension
dim_country = world_ranking[
    ['competitor.id_country',
    'competitor.country_name',
    'competitor.country_ioc_code',
    'competitor.id_continent']
    ].drop_duplicates().sort_values('competitor.id_country').reset_index(drop=True)

# Continent Dimension
dim_continent = dim_country[
    ['competitor.id_continent']].drop_duplicates(
        'competitor.id_continent'
        ).sort_values('competitor.id_continent').assign(
            continent_name =  [
                'ijf',
                'Africa',
                'Asia',
                'Europe',
                'Oceania',
                'America']).reset_index(drop=True)

# Competitions Dimension
dim_competition = world_ranking[
    ['competition.id',
    'competition.name',
    'competition.date_from']].drop_duplicates().sort_values(
        'competition.date_from'
        ).reset_index(drop=True)

# Fact table from each competition a player has been,
# with his respective points for the World Ranking
# and result
fact_tournament_results = world_ranking[
    ['points',
    'place',
    'long_place',
    'competition.id',
    'competitor.id']]

# We export the data that will feed our PowerBI Dashboard
dim_competitors.to_csv('data/dim_competitors.csv', index=False)
dim_competition.to_csv('data/dim_competition.csv', index=False)
dim_continent.to_csv('data/dim_continent.csv', index=False)
dim_country.to_csv('data/dim_country.csv', index=False)
dim_weight_category.to_csv('data/dim_weight_category.csv', index=False)
fact_tournament_results.to_csv('data/fact_tournament_results.csv', index=False)
# THE END
print('Ready :)')