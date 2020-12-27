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
me = watcher.summoner.by_name('eun1', 'SunnyJ')


def get_last_x_matches(x):
    my_matches = watcher.match.matchlist_by_account(region, me['accountId'])
    last_x_matches = my_matches['matches'][:x+1]
    return last_x_matches


last = get_last_x_matches(20)


# TODO: top 5 champs in last x games
# TODO: best item builds for those champs
# TODO: spider chart for income, dmg, vision, cc and KDA by position
# TODO: Calculate score for these metrics and plot for each position in last x games
# TODO: Current game analysis - winrate for all players, best and worst champs, average kda for last 5 game

