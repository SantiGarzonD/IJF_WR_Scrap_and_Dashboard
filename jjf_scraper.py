import requests
import json
import pandas as pd

page = 0
world_ranking = pd.DataFrame()

while True:
    
    url = f'https://www.ijf.org/internal_api/wrl?category=all&page={page}'

    r = requests.get(url=url)
    
    with open('casa.txt', 'w') as f:
        f.write(r.text)

    try:
        data = r.json()

        data_list = data['feed']

        if len(data_list)==0:
            break

        for competitor in data_list:

            competitor['score_parts'] = list(filter(None, competitor['score_parts']))

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
            ], meta_prefix='competitor.')

        world_ranking = pd.concat([world_ranking, df_aux])
    
    except:
        print('except')
        break

    print(page)
    page += 1
    

    

world_ranking.to_csv('competitor.csv')
print('listo :)')