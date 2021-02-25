from flask import request, render_template, Blueprint
import logging

from my_lol_api.LOLService import LOLService
from my_lol_api.Player import Player

logger = logging.getLogger(__file__)

lol_api = Blueprint('lol_api', __name__)

lol = LOLService()


@lol_api.route('/', methods=['GET'])
def home():
    servers = lol.servers
    return render_template('index.html', servers=servers)


@lol_api.route(f'/player', methods=['POST'])
def get_player_by_summoner_name():
    server = request.values.get('server').lower()
    summoner_data = lol.get_summoner_data(request.values)
    summoner_data['server'] = server
    player = Player.from_summoner_data(summoner_data)
    icon = lol.get_icon(player)
    return render_template('player.html', icon=icon, name=player.name, lvl=player.lvl)

