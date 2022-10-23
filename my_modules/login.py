from steam.client import SteamClient
from dota2.client import Dota2Client

client = SteamClient()
dota = Dota2Client(client)

@client.on('loggen_on')
def start_dota():
	dota.launch()

