# This is a sample Python script.
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url = 'https://www.smogon.com/stats/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
hrefs = [a['href'] for a in soup.find_all('a', href=True)]
latest_url = hrefs[-1]

# can also be 1695
usage_constructor_url = 'gen9ou-1500.txt'

# must be 1500
moveset_constructor_url = 'moveset/gen9ou-1500.txt'

usage_url = url + latest_url + usage_constructor_url
moveset_url = url + latest_url + moveset_constructor_url

moveset_page_blocks = ['Usage', 'Abilities', 'Items', 'Spreads', 'Moves', 'Teammates', 'Checks & Counters']


# this function stores all usage data in a dict or df; values are either "df" or "dict"
def fetch_usage_data(value):
    usage_response_raw = requests.get(usage_url)
    usage_response_delimited = usage_response_raw.text.split('+')

    # create the table of usage table index values
    index_table_delimit_value = 8
    usage_index = [item.strip() for item in usage_response_delimited[index_table_delimit_value].split('|')][1:8]
    print(usage_index)
    # ['Rank', 'Pokemon', 'Usage %', 'Raw', '%', 'Real', '%'], pre-trim 0 is ','

    # store usage values
    usage_table_delimit_value = 16
    usage_stat_array = np.array(
        [item.strip() for item in usage_response_delimited[usage_table_delimit_value].split('|')])
    usage_stat_matrix = [usage_stat_array[i::8] for i in range(1, 8)]

    if value == "dict":
        # create a dictionary of usage data
        #        usage_dict = {}
        #        for i in range(0, len(usage_stat_matrix)-1):
        #            usage_dict[usage_stat_matrix[1][i]] = [usage_stat_matrix[j][i] for j in range(0, 6)]
        usage_dict = {usage_stat_matrix[1][i]: [usage_stat_matrix[j][i] for j in range(0, 6)] for i in
                      range(0, len(usage_stat_matrix) - 1)}
        return usage_dict

    if value == "df":
        df = pd.DataFrame.from_records(usage_stat_matrix, index=usage_index)
        return df

    return


def text_to_array(list_file, array_type=''):
    index_start = 1

    if array_type == 'Usage':
        index_start = 0

    list_to_return = [item.splitlines() for item in list_file]

    for row in list_to_return:
        for i in range(len(row)):
            row[i] = row[i].strip()

    return list_to_return[index_start:]

def transpose(lst):
    return lst(map(lst, zip(*lst)))


# this function returns a dictionary of moveset data for pokemon, the key is the name, and there is another
# dictionary that will contain a list of values: [4Usage, 6Abilities, 8Items, 10Spreads, 12Moves, 14Teammates,
# 16Checks & Counters]
def fetch_moveset_data():
    print(moveset_url)
    moveset_response_raw = requests.get(moveset_url)
    moveset_response_delimited = moveset_response_raw.text.split('+')

    data_array = []

    for i in range(0, 7):
        data_array.append([item.replace("|", "").strip() for item in moveset_response_delimited[(i + 1) * 2::18]])

    # various array construction
    pk_names = data_array[0]
    moveset_data_array = [text_to_array(data_array[i], 'Usage') for i in range(1, 7)]
    moveset_data_array = [[row[i] for row in moveset_data_array] for i in range(len(moveset_data_array[0]))]

    # major dictionary to be populated with all the arrays of data
    moveset_dict = {pk_names[i]: moveset_data_array[i][:] for i in range(len(pk_names))}

    return moveset_dict


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    usage_df = fetch_usage_data('df')
    moveset_dict = fetch_moveset_data()
    # pokedex = movesets are populated now i need to populate pokemon with their stats

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
