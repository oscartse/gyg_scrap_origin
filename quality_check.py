import pandas as pd
import numpy as np
import pprint
import requests
import pandas as pd
from lxml import etree


def country_check(path):
    df = pd.read_csv(path)
    df.drop(df.loc[df['count'] == 'no_count'].index, inplace=True)

    for link in df['request_url'].values:
        req = requests.request('POST', link)
        root = etree.HTML(req.content)
        checker = root.xpath('//div[@class="vertical-activity-card-container "]//text()')
        if checker:
            pass
        else:
            df.drop(df.loc[df['request_url'] == link].index, inplace=True)
    df.to_csv(path)


def diagnosis(prev_path, curr_path, file_loca):
    df_prev = pd.read_csv(prev_path)
    df_new = pd.read_csv(curr_path)
    if df_prev['count'].sum() != df_new['count'].sum():
        if len(df_prev['country']) == len(df_new['country']):
            df1 = df_prev[['country', 'count']]
            df2 = df_new[['country', 'count']]
            pair_comparing = pd.merge(df1, df2, on='country', how='inner')
            pair_comparing['difference'] = pair_comparing['count_y'] - pair_comparing['count_x']
            diagnosis = pair_comparing[pair_comparing['difference'] != 0]
            diagnosis.to_csv(file_loca + '/gyg_diagnosis.csv')
        else:
            df1 = df_prev[['country', 'count']]
            df2 = df_new[['country', 'count']]
            pair_comparing = pd.merge(df1, df2, on='country', how='inner')
            pair_comparing['difference'] = pair_comparing['count_y'] - pair_comparing['count_x']
            diagnosis = pair_comparing[pair_comparing['difference'] != 0]
            new_country = list(set(df_new['country'])-set(df_prev['country'].values))
            for country in new_country:
                diagnosis.concat(df2[df2['country'] == country])
            diagnosis.to_csv(file_loca + '/gyg_diagnosis.csv')


def main():
    path = "your_path"
    country_check(path)
    pass


if __name__ == '__main__':
    main()
