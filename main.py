from core.config import *
from core.database import *
from functions.utils import *
from functions.clases import *
from commands.ayuda import *
from commands.crear import *
from commands.moderacion_samp import *

#=============================#
#          Cargando bot       #
#=============================#
async def update_player_count():
    while True:
        with SampClient(address='s1.fenixzone.com', port='7777') as client:
            info = client.get_server_info()
            jugando = info.players
            
            # Actualizar el estado del bot
            await bot.change_presence(activity=discord.Game(name=f"{botname} con {jugando} jugadores"))

        await asyncio.sleep(60)
        
@bot.event
async def on_ready():
    #El bot esta jugando, actualmente el nombre del bot o servidor.
    bot.loop.create_task(update_player_count())

    bot.add_view(verificarBoton())
    
    print("#=============================================#")
    print(f" {bot.user} ha sido iniciado correctamente!")
    print(f" Botname: {botname}")
    print(" Desarrollado por: Sorac")
    print("#=============================================#")
    print("Conectado a Discord como:")
    print(f" Nombre: {bot.user.name}")
    print(f" ID: {bot.user.id}")
    print("#=============================================#")

bot.run(bot_token)
