import streamlit as st
import requests
from riotwatcher import LolWatcher, ApiError
import pandas as pd
import os
import re


key = os.environ.get('RIOT_API_KEY')
watcher = LolWatcher(key)

# AMERICAS = 'americas.api.riotgames.com'
# EUROPE = 'asia.api.riotgames.com'
# ASIA = 'europe.api.riotgames.com'

servers = {
    "EUNE": 'eun1.api.riotgames.com',
    "EUW": 'euw1.api.riotgames.com',
    "NA": 'na1.api.riotgames.com',
    "RU": 'ru.api.riotgames.com'
}
serv = re.compile('(\w+)')
# reg = re.match(serv, servers['EUNE'])[0]
regions = [re.match(serv, i)[0] for i in servers.values()]
region = regions[0]
if region == 'eun1':
    reg = 'eune'
else:
    reg = region

name = 'SunnyJ'
me = watcher.summoner.by_name(region, name)

# Control version of the game:
latest = watcher.data_dragon.versions_for_region(reg)['n']['champion']

# Champion ids to names:
static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')
champ_dict = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict[row['key']] = row['id']


def get_rank(queue):
    stats = watcher.league.by_summoner(region, me['id'])
    flex = {'WR': f"{round(stats[0]['wins'] * 100 / (stats[0]['wins'] + stats[0]['losses']))}%",
            'rank': stats[0]['tier'] + " " + stats[0]['rank'],
            'LP': stats[0]['leaguePoints']}
    solo = {'WR': f"{round(stats[1]['wins'] * 100 / (stats[1]['wins'] + stats[1]['losses']))}%",
            'rank': stats[1]['tier'] + " " + stats[1]['rank'],
            'LP': stats[1]['leaguePoints']}
    if queue == 'flex':
        return flex
    elif queue == 'solo':
        return solo


def get_last_x_matches(x):
    my_matches = watcher.match.matchlist_by_account(region, me['accountId'])
    last_x_matches = my_matches['matches'][:x]
    return last_x_matches


last = get_last_x_matches(20)
match = get_last_x_matches(1)


def map_roles(tup):
    role = ''
    if tup == ("MID", "SOLO"):
        role = 'Mid'
    elif tup == ('TOP', 'SOLO'):
        role = 'Top'
    elif tup == ('JUNGLE', 'NONE'):
        role = 'Jungle'
    elif tup == ('BOTTOM', 'DUO_CARRY'):
        role = 'ADC'
    elif tup == ('BOTTOM', 'DUO_SUPPORT'):
        role = 'Support'
    return role


def get_match_data(match):
    my_data = {}
    match_details = watcher.match.by_id(region, match['gameId'])
    for row in match_details['participants']:
        if row['championId'] == match['champion']:
            my_data['champion'] = row['championId']
            my_data['role'] = map_roles((match['lane'], match['role']))
            my_data['win'] = row['stats']['win']
            my_data['kills'] = row['stats']['kills']
            my_data['deaths'] = row['stats']['deaths']
            my_data['assists'] = row['stats']['assists']
            my_data['totalDamageDealtToChampions'] = row['stats']['totalDamageDealtToChampions']
            my_data['healingUtility'] = row['stats']['totalHeal'] / row['stats']['totalUnitsHealed']
            my_data["timeCCingOthers"] = row['stats']['timeCCingOthers']
            my_data["vision"] = row['stats']['wardsPlaced'] + row['stats']['wardsKilled']
            my_data['goldEarned'] = row['stats']['goldEarned']
            my_data['totalMinionsKilled'] = row['stats']['totalMinionsKilled']
            my_data['item0'] = row['stats']['item0']
            my_data['item1'] = row['stats']['item1']
            my_data['item2'] = row['stats']['item2']
            my_data['item3'] = row['stats']['item3']
            my_data['item4'] = row['stats']['item4']
            my_data['item5'] = row['stats']['item5']
            my_data['item6'] = row['stats']['item6']
    return my_data


def combine_data_for_matches(x):
    last = get_last_x_matches(x)
    games = []
    for game in last:
        my_data_row = get_match_data(game)
        games.append(my_data_row)
    gms = pd.DataFrame(games)
    return gms


sperm = combine_data_for_matches(20)

for champ in sperm['champion']:
    champdf = sperm.loc[sperm['champion'] == champ]
    # print(champdf)

    chp = {}
    wr = champdf['win'].value_counts()
    if len(wr.index) == 2:
        print(champdf)
    # print(wr.loc[wr.index[0]])
    # if len(wr.index) == 2:
    #     chp[champ] = f"{(wr.loc[wr.index[0]] / (wr.loc[wr.index[0]] + wr.loc[wr.index[1]])) * 100}%"
    # elif len(wr.index) == 1:
    #     if wr.index[0] == 'True':
    #         chp[champ] = "100%"
    #     elif wr.index[0] == "False":
    #         chp[champ] = "0%"
    # print(chp)
    # print(type(wr))
    # print(wr['True'] / (wr['True'] + wr['False']))


def get_top_wr_champs(n_games, n_champs):
    combined_data = combine_data_for_matches(n_games)
    for champ in combined_data['champion']:
        champdf = combined_data.loc[combined_data['champion'] == champ]
        wr = champdf['win'].value_counts()
        if len(wr.index) == 2:
            champdf['WR'] = f"{(wr.loc[wr.index[0]] / (wr.loc[wr.index[0]] + wr.loc[wr.index[1]])) * 100}%"
        elif len(wr.index) == 1:
            if wr.index[0] == 'True':
                print("100%")
            elif wr.index[0] == "False":
                print("0%")
        # champdf['WR'] = champdf[]
            pass

    pass
# TODO: top 5 champs by WR in last x games
# TODO: best item builds for those champs
# TODO: spider chart for income, dmg, vision, cc and KDA by position
# TODO: Calculate score for these metrics and plot for each position in last x games

# FUTURE:
# TODO: Current game analysis - winrate for all players, best and worst champs, average kda for last 5 game
