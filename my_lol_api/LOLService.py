import os
from riotwatcher import LolWatcher, ApiError
import re


class LOLService:
    def __init__(self):
        self.key = os.environ.get('key')
        self.watcher = LolWatcher(self.key)
        self.servers = {'BR1': 'Brazil',
                        'EUN1': 'Europe East',
                        'EUW1': 'Europe West',
                        'JP1': 'Japan',
                        'KR': 'Korea',
                        'LA1': 'Latin America North',
                        'LA2': 'Latin America South',
                        'NA1': 'North America',
                        'OC1': 'Oceania',
                        'TR1': 'Turkey',
                        'RU': 'Russia'}

    def map_server_for_versioning(self, player):
        server = player.server
        if server == 'eun1':
            s = 'eune'
        elif server == 'la1':
            s = 'lan'
        elif server == 'la2':
            s = 'las'
        elif server == 'oc1':
            s = 'oce'
        else:
            s = server

        return s

    def map_url_to_server(self, server):
        return self.servers[server]

    def get_summoner_data(self, request):
        server = request.get('server').lower()
        summoner = request.get('summoner')
        response = self.watcher.summoner.by_name(server, summoner)
        return response

    def get_icon(self, player):
        server = self.map_server_for_versioning(player)
        version = self.watcher.data_dragon.versions_for_region(server)
        profile_icon = self.watcher.data_dragon.profile_icons(version['n']['profileicon'])
        ic = profile_icon['data'][str(player.icon)]['image']['full']
        cdn = version['cdn']
        v = version['v']
        return f'{cdn}/{v}/img/profileicon/{ic}'
        # return cdn

    def get_current_season(self):
        pass




