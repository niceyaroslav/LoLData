import os
from riotwatcher import LolWatcher, ApiError
from my_lol_api.LOLService import LOLService

req = {"accountId": "deK5u33uGh_PyOd1RxXOTEqpqoNg1sYmN9MfJGDq60uEnQ",
       "id": "HXjALHJ4kS0f_ge5nnkOIwlFBTQmf9tVEgmdbJTJISd5PdE",
       "name": "SunnyJ",
       "profileIconId": 4419,
       "puuid": "ny4N7ojH39UjqpNZVog34i0WNOu8qp3osYRsF8CekJTjURF5Wh7EFw5rdjqn3CUNPPFeo5S-LudgcQ",
       "revisionDate": 1614031824000,
       "summonerLevel": 271}

schema = {"accountId": "account_id",
          "id": "id",
          "name": "name",
          "profileIconId": 'icon',
          "puuid": "puuid",
          "summonerLevel": 'lvl',
          'server': 'server'}


class Player:

    def __init__(self):
        self.account_id = ''
        self.id = ''
        self.name = ''
        self.icon = int()
        self.puuid = ''
        self.lvl = int()
        self.server = ''

    @staticmethod
    def from_summoner_data(summoner_data):
        player = Player()
        for i, k in schema.items():
            setattr(player, k, summoner_data[i])
        return player

    # def get_match_list(self, request):
    #     server = request.get('server').lower()
    #     response = self.get_summoner_data(request)
    #     matches = self.watcher.match.matchlist_by_account(server, response['accountId'])
    #     return matches

    def get_last_x_matches(self, x):
        pass