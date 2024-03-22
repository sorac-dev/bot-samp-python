from core.libs import *

bot = discord.Bot()

#Cargar archivo .env
load_dotenv()
bot_token = os.getenv('TOKEN')
server_ip = os.getenv('SERVER_IP')
server_port = os.getenv('SERVER_PORT')
botname = os.getenv('BOT_NAME')

#=============================#
#       Roles de moderacion   #
#=============================#
SUPERMODS = [1144847700773326938, 1144847700773326938]
MODS = [1144847700773326938, 1144847700773326938]

