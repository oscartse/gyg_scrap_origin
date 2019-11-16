import requests
import pandas as pd
from lxml import etree


def country_check(path):
    df = pd.read_csv(path)
    for link in df['request_url'].values:
        req = requests.request('POST', link)
        root = etree.HTML(req.content)
        checker = root.xpath('//div[@class="vertical-activity-card-container "]//text()')
        if checker:
            pass
        else:
            df.drop(df.loc[df['request_url'] == link].index, inplace=True)
    df.to_csv(path)
