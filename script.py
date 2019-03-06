import pandas as pd
import numpy as np

# Setting up pandas so that it displays all columns instead of collapsing them
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)

# 1 explore data
ad_clicks = pd.read_csv('ad_clicks.csv')
# print(ad_clicks.head())

# 2 Get df with views per utm source
views_per_utm_source = ad_clicks\
                        .groupby('utm_source')\
                        .user_id\
                        .count()\
                        .reset_index()\
                        .rename(columns={'user_id': 'views'})
# print(views_per_utm_source)

# '~' is a NOT operator. isnull() tests whether or not the value of ad_click_timestamp is null
# 3 in this case a timestamp that is not Null indicates an ad click
ad_clicks['is_click'] = ~ad_clicks\
                            .ad_click_timestamp\
                            .isnull()
# print(ad_clicks.head())

# Group clicks by utm resource
clicks_by_source = ad_clicks\
                    .groupby(['utm_source', 'is_click'])\
                    .user_id\
                    .count()\
                    .reset_index()\
                    .rename(columns={'user_id': 'count'})
# print(clicks_by_source.head())

# Pivot  into a more readable table. Columns are True or False for clicks. Rows are utm_sources.
clicks_pivot = clicks_by_source\
                    .pivot(columns='is_click', index='utm_source', values='count')
# print(clicks_pivot)

# add column with percentage
clicks_pivot['percent_clicked'] = round(clicks_pivot[True]
                                        / (clicks_pivot[True]+clicks_pivot[False])
                                        , 2)
# print(clicks_pivot)

# 4 prints size of A and B group
ab_count = ad_clicks\
            .groupby('experimental_group')\
            .user_id.count()\
            .reset_index()
# print(ab_count)

# 5
ab_count_is_click = ad_clicks\
                        .groupby(['experimental_group', 'is_click'])\
                        .user_id\
                        .count()\
                        .reset_index()
# print(ab_count_is_click)

ab_count_is_click_pivot = ab_count_is_click.pivot(columns='is_click', index='experimental_group', values='user_id')
ab_count_is_click_pivot['percent_clicked'] = round(ab_count_is_click_pivot[True] /
                                                   (ab_count_is_click_pivot[False] +
                                                    ab_count_is_click_pivot[True]
                                                    ),
                                                   2)
# print(ab_count_is_click_pivot)

# 6
a_clicks = ad_clicks[ad_clicks['experimental_group'] == 'A'].reset_index(drop=True)
b_clicks = ad_clicks[ad_clicks['experimental_group'] == 'B'].reset_index(drop=True)
# print(a_clicks.head())
# print(b_clicks.head())
a_clicks_is_click_day = a_clicks\
                            .groupby(['is_click', 'day'])\
                            .user_id\
                            .count()\
                            .reset_index()
a_clicks_is_click_day_pivot = a_clicks_is_click_day\
                                .pivot(
                                    columns='is_click',
                                    index='day',
                                    values='user_id'
                                )\
                                .reset_index()
a_clicks_is_click_day_pivot['percent_clicked'] = round(a_clicks_is_click_day_pivot[True] /
                                                       (a_clicks_is_click_day_pivot[True] +
                                                        a_clicks_is_click_day_pivot[False]
                                                        )
                                                       , 2)
b_clicks_is_click_day = b_clicks.groupby(['is_click', 'day']).user_id.count().reset_index()
b_clicks_is_click_day_pivot = b_clicks_is_click_day\
                                .pivot(
                                    columns='is_click',
                                    index='day',
                                    values='user_id'
                                )\
                                .reset_index()
b_clicks_is_click_day_pivot['percent_clicked'] = round(b_clicks_is_click_day_pivot[True] /
                                                       (b_clicks_is_click_day_pivot[True] +
                                                        b_clicks_is_click_day_pivot[False]
                                                        ),
                                                       2)
print(a_clicks_is_click_day_pivot)
print(b_clicks_is_click_day_pivot)
