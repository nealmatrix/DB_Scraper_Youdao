# %%
import requests
from bs4 import BeautifulSoup
import argparse
import pandas as pd
import sqlite3 as sl

# %%
# Command Parameter
parser = argparse.ArgumentParser()
parser.add_argument('-w', '--word', default = "test", help = 'input word', type = str)
parser.add_argument('-p', '--pron', default = "", help = 'Add pron', type = str)
parser.add_argument('-t', '--type', default = 1, help = 'input word type index in collins', type = int)
parser.add_argument('-i', '--index', default = 1, help = 'index of the meaning', type = int)
parser.add_argument('-m', '--meaning', default = '', help = 'Add the meaning of the word')
parser.add_argument('-ex', '--example', default = '', help = 'Add the example of the word')
parser.add_argument('-exi', '--example_index_list', nargs = '+', default = [1], help = 'the example index of the word in Youdao I want to choose')

parser.add_argument('-e', '--episode', choices = [
    'DHS01E01',     # Desperate housewifves
    'DHS01E02',
    'DHS01E03',
    'DHS01E04',
    'DHS01E05',
    'DHS01E06',
    'DHS01E07',    
    'DHS01E08',

    'FS01E05',      # Friends
    'FS01E06',
    'FS01E07',
    
    'HTGAWMS01E01', # How to get away with murder
    'LF',           # Lucifer
    'LTN',          # Light the night
    
    'DM',           # Despicable Me
    'JW',           # Jurassic World
    'LDR',          # Love death + robots
    'MR',           # Mechanic: resurrection

    'POE',          # Path of exile
    'MC',           # Minecraft
    'HS',           # Hearthstone
    'D3',           # Diablo 3 

    'NCE',          # New Concept English

    'CS',           # Computer Science

    'Other',        # Other words in my life
    'Pron',         # Pronunciation correction
    'Youdao',       # Words in Youdao collins meaning or example
    'Name',         # Male first name, Female first name, last name
    'Place'         # Place name 
    ], default = 'DHS01E01', help = 'Show the episode the word shows up')


args = parser.parse_args()

word = args.word
add_pron = args.pron
word_type = args.type
collins_idx = args.index
add_meaning = args.meaning
add_example = args.example
example_index_list = args.example_index_list
episode = args.episode

# %%
# Search COCA frequency in real time, shwon in terminal
def searchCOCA(word):
    try:
        con = sl.connect('words.db')
        df = pd.read_sql_query(
            "SELECT * FROM COCA60000 WHERE word = '" + 
            word.replace("'", "''") + "';" , con)

        print("\n" + str(df["id"][0]))
        
    except IndexError:
        print("\n" + "not found in COCA60000")

    finally:
        if (con):
            con.close()

# %%
# Scrape info from Youdao
def scrapeFromYoudao(word, word_type, collins_idx, add_meaning):
    url = "http://dict.youdao.com/w/" + word + "/#keyfrom=dict2.top"
    results = requests.get(url)
    soup = BeautifulSoup(results.text, "html.parser")

    # Find pronounce
    if not add_pron:
        pron = soup.find_all('span', class_ = 'pronounce')
        pron_us = pron[1].get_text(' ', strip = True) if len(pron) > 1 else '-'
    else:
        pron_us = add_pron
    print("\n" + pron_us)

    # Find the collins meaning and example
    collins = soup.find('div', attrs = {'id': 'collinsResult'})

    if collins and not(add_meaning) and not(add_example):
        # If the word has more than one 词性
        collins = collins.select('.wt-container:nth-child(' + str(word_type) + ')')

        # collins_item: the meaning we need including meaning and examples 
        collins_item = collins[0].select('li:nth-child(' + str(collins_idx) + ') > .collinsMajorTrans')
        collins_meaning = str(word_type) + '.' + collins_item[0].get_text(' ', strip = True)

        collins_example_div = collins[0].select('li:nth-child(' + str(collins_idx) + ') .examples')
        if collins_example_div:
            collins_example = ''
            for example_index in example_index_list:
                collins_example += collins_example_div[int(example_index) - 1].get_text('\n', strip = True) + '\n'
            collins_example = collins_example[: -1]
        else:
            collins_example = '-'
    else:
        collins_meaning = add_meaning if add_meaning else '-'
        collins_example = add_example if add_example else '-'

    print ("\n" + collins_meaning)
    print ("\n" + collins_example)
    print ("\n" + episode)

    return pron_us, collins_meaning, collins_example

# %%
# Store data into the sqlite database
def WriteIntoDB(word, pron_us, collins_meaning, collins_example, episode):
    con = sl.connect('words.db')

    print( 
            "INSERT INTO WORDS (word, pron_us, collins_meaning, collins_example, episode) VALUES('" +
            word.replace("'", "''") + "','" +
            pron_us.replace("'", "''") + "','" +
            collins_meaning.replace("'", "''") + "','" +
            collins_example.replace("'", "''") + "','" +
            episode + "');"
        )

    with con:
        con.execute(
            "INSERT INTO WORDS (word, pron_us, collins_meaning, collins_example, episode) VALUES('" +
            word.replace("'","''") + "','" +
            pron_us.replace("'", "''") + "','" +
            collins_meaning.replace("'", "''") + "','" + # 转译字符串中有'的情况
            collins_example.replace("'", "''") + "','" +
            episode + "');"
            )


    print("\nInsert into database DONE")

# %%
def get_words_unique(words):
    seen = set()
    seen_add = seen.add
    return [x for x in words if not (x in seen or seen_add(x))]

# %%
if __name__ == "__main__":
    searchCOCA(word)
    pron_us, collins_meaning, collins_example = scrapeFromYoudao(word, word_type, collins_idx, add_meaning)

    # Double check
    yOrN = input('\nContent Checked, Y or N?\n')

    if yOrN.upper() == 'Y':
        WriteIntoDB(word, pron_us, collins_meaning, collins_example, episode)

    else:
        print("Cancel")


