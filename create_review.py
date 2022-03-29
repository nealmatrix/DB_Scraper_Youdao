# %%
# import package
import sqlite3 as sl
import pandas as pd
import numpy as np
from IPython.display import display
import time
import os

pd.set_option('display.max_rows', 10)
# from IPython.core.interactiveshell import InteractiveShell
# InteractiveShell.ast_node_interactivity = 'all'

# %%
# Parameter
index_end_last_sat = 4280
num_review = 100

# %%
# Fetch WORDS_COCA table from database
con = sl.connect('words.db')
with con:
    df_COCA = pd.read_sql_query(
        "SELECT * FROM (\
            SELECT * FROM WORDS_COCA WHERE COCA IS NOT NULL ORDER BY COCA, collins_meaning)\
        UNION ALL\
        SELECT * FROM (\
            SELECT * FROM WORDS_COCA WHERE COCA IS NULL AND word <> '-' ORDER BY word, collins_meaning)\
        UNION ALL\
        SELECT * FROM (\
            SELECT * FROM WORDS_COCA WHERE COCA IS NULL AND word = '-' ORDER BY episode);", con)

df_COCA['COCA'] = df_COCA['COCA'].astype('Int64')
df_COCA

# df.to_csv('.//doc//a.csv', index = False)

# %%
# Produce review_all for tomorrow's review
with open(".//doc//reviewed.csv", 'r+') as f:
    reviewed = []
    while True:
        review = f.readline()
        if not review:
            break
        review = review.rstrip('\n')
        reviewed.append(int(review))

    print('num of reviewed: ' + str(len(reviewed)))

    df_noreviews = df_COCA.loc[~df_COCA['id'].isin(reviewed)]

    print('no reviews')
    display(df_noreviews)

    df_today_reviews = df_noreviews[:num_review].reset_index(drop = True)

    print('today reviews')
    display(df_today_reviews)

    filename = time.strftime("%Y-%m-%d %H.%M.%S", time.localtime())
    
    df_today_reviews.to_csv('.//doc//review_all//' + filename + '-review.csv')

    # Write the id of today review words into reviewed.csv
    today_reviews = list(df_today_reviews['id'])
    if len(today_reviews) > 0:
        if len(reviewed) == 0:
            f.write(str(today_reviews[0]))
        else:
            f.write('\n' + str(today_reviews[0]))

        for write in today_reviews[1:]:
            f.write('\n' + str(write))
        
# %%
# Produce week_review & week_review_COCA
con = sl.connect('words.db')
with con:
    df_week = pd.read_sql_query(
        "SELECT * FROM WORDS WHERE id > " + str(index_end_last_sat) + ";", con) 
    
    df_week_COCA = pd.read_sql_query(
        "SELECT * FROM (\
            SELECT * FROM (\
                SELECT * FROM WORDS_COCA WHERE COCA IS NOT NULL ORDER BY COCA, collins_meaning)\
            UNION ALL\
            SELECT * FROM (\
                SELECT * FROM WORDS_COCA WHERE COCA IS NULL AND word <> '-' ORDER BY word, collins_meaning)\
            UNION ALL\
            SELECT * FROM (\
                SELECT * FROM WORDS_COCA WHERE COCA IS NULL AND word = '-' ORDER BY episode))\
        WHERE id > " + str(index_end_last_sat)+ ";", con)
    
df_week_COCA['COCA'] = df_week_COCA['COCA'].astype('Int64')

print("week review:")
display(df_week)
print("week review with COCA")
display(df_week_COCA)

filename = time.strftime("%Y-%m-%d %H.%M.%S", time.localtime())
df_week.to_csv(os.path.join('doc', 'week_review', filename + '.csv'))
df_week_COCA.to_csv(os.path.join('doc', 'week_review', filename + '_COCA.csv'))
# %%
