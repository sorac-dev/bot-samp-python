import hashlib
import string
import discord
import asyncio
import os
from dotenv import load_dotenv
from samp_client.client import SampClient
import mysql.connector
import random

#=============================#
#          Configuracion      #
#=============================#
load_dotenv()
bot_token = os.getenv('TOKEN')
server_ip = os.getenv('SERVER_IP')
server_port = os.getenv('SERVER_PORT')
botname = os.getenv('BOT_NAME')

owner_id = 352897123014148096

#=============================#
#          Cargando bot       #
#=============================#
bot = discord.Bot()

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
#=============================#
#          Conexion MySQL     #
#=============================#
conn = mysql.connector.connect(
    host= os.getenv('HOST_MYSQL'),
    user=  os.getenv('USER_MYSQL'),
    password=os.getenv('PASS_MYSQL'),
    database= os.getenv('DB_MYSQL')
)
sendSQL = conn.cursor()
#=============================#
#           Funciones         #
#=============================#
def obtenerUsername(user_id):
    query = "SELECT Username FROM usuarios WHERE ID = %s"
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]
    else:
        return "Usuario desconocido"
def obtenerUserID(user_name):
    query = "SELECT ID FROM usuarios WHERE Username = %s"
    cursor = conn.cursor()
    cursor.execute(query, (user_name,))
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]
    else:
        return "Usuario desconocido"
#Encriptador de contraseñás
def EncriptarPassword(data):
    #Esto es algo adicional, que se le combina con la contraseñá del usuario, debe ser igual al de tu Gamemode Zone (WZ)
    token_sha256 = "gz.rp@!28"
    #Aqui unimos la contraseñá y el token unico (El token debe ser unico por lo tanto no debe ser mostrado a nadie)
    encriptacion_reforzada = data + token_sha256
    #Comienza la encriptacion de la contraseñá
    sha256_hash = hashlib.sha256()
    
    #Ya encriptada, pone todo en mayusculas
    sha256_hash.update(encriptacion_reforzada.encode('utf-8'))
    return sha256_hash.hexdigest().upper()

# Función para generar un token único
def generate_token():
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(32))
    return token
def verificar_tiempo(tiempo):
    if not isinstance(tiempo, int):
        return "En 'tiempo' debes ingresar un dato numérico."
    
    if tiempo < 0:
        return "El tiempo debe ser mayor o igual a 0"
    
    if tiempo >= 1441:
        return "El tiempo de muteo/sancion no debe ser superior a 1 día. (1 día = 1440 minutos)"
    
    return None

#=============================#
#       Roles de moderacion   #
#=============================#
SUPERMODS = [1144847700773326938, 1144847700773326938]
MODS = [1144847700773326938, 1144847700773326938]
#=============================#
#       Clases del bot        #
#=============================#
class verificarForm(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Nombre_Apellido"))
        self.add_item(discord.ui.InputText(label="Contraseña"))

    async def callback(self, interaction: discord.Interaction):
        usuario = self.children[0].value
        clave = EncriptarPassword(self.children[1].value)
        
        #Comenzamos con las consultas, para saber si existe el usuario ingresado
        sql = "SELECT ID,Username,Password,DiscordID FROM usuarios WHERE Username = %s"
        sendSQL.execute(sql, (usuario,))
        result = sendSQL.fetchone()

        if result:
            if clave == result[2]: #Verificamos que la contraseña sea igual a la ingresada
                if result[3] == 0: #Verificamos que aun no tenga vinculado algun discord
                    try:
                        role_id = 1144847820424228914 # ID del rol "Usuario"
                        role = discord.utils.get(interaction.guild.roles, id=role_id)
                        if role in interaction.user.roles:
                            await interaction.respond(f"**[!]** {usuario}, ya estas verificado en el servidor de discord.", ephemeral=True)
                            return
                        
                        #Add rol
                        await interaction.user.add_roles(role)
                        #Update name
                        await interaction.user.edit(nick=usuario)

                         # Actualizar el token como usado (vinculado = 1)
                        query = "UPDATE usuarios SET DiscordID = %s WHERE Username = %s"
                        sendSQL.execute(query, (interaction.user.id, usuario,))
                        conn.commit()

                        embed = discord.Embed(title=f"Verificacion | {botname}")
                        embed.add_field(name="Estado verificacion", value="Usted se verifico correctamente")
                        await interaction.response.send_message(embeds=[embed], ephemeral=True)
                    except discord.errors.Forbidden as e:
                        await interaction.response.send_message(f"**[!]** No tengo los permisos suficientes :(", ephemeral=True)
                        print(e)
                else:
                    embed = discord.Embed(title=f"Verificacion | {botname}")
                    embed.add_field(name="Estado verificacion", value="La cuenta ingresada ya esta vinculada")
                    await interaction.response.send_message(embeds=[embed], ephemeral=True)
            else:
                embed = discord.Embed(title=f"Verificacion | {botname}")
                embed.add_field(name="Estado verificacion", value="La contraseña del usuario, no es correcta")
                await interaction.response.send_message(embeds=[embed], ephemeral=True)
        else:
            embed = discord.Embed(title=f"Verificacion | {botname}")
            embed.add_field(name="Estado verificacion", value="El usuario ingresado no existe")
            await interaction.response.send_message(embeds=[embed], ephemeral=True)

class verificarBoton(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    @discord.ui.button(label="🔗 Vincular cuenta", style=discord.ButtonStyle.blurple, custom_id="verificar")
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(verificarForm(title=f"Verificar | {botname}"))

#=============================#
#       Comandos del bots
#=============================#
help = bot.create_group("ayuda", "¿Que tipo de ayuda necesitas?")
@help.command(name = "version", description = "Enterate de la version base actual de nuestro servidor SA-MP.")
async def version(ctx):
    await ctx.respond("Actualmente nos encontramos en la fase **Alpha de desarrollo**, en la cual estamos trabajando en la implementación de características básicas y realizando pruebas. Durante esta etapa, estamos enfocados en establecer una base sólida y recopilar comentarios valiosos para mejorar y perfeccionar nuestro proyecto. Agradecemos tu paciencia y apoyo mientras avanzamos hacia versiones más estables y completas en el futuro.", ephemeral=True)

@help.command(name = "servidor", description = "Enterate del estado actual de nuestro servidor y de su IP.")
async def servidor(ctx):
    with SampClient(address=server_ip, port=server_port) as client:
        info = client.get_server_info()
        embed = discord.Embed(
        description=f"🔌 **IP**: {server_ip}:{server_port}",
        color=0x009cff,
        )
        embed.add_field(name="👥 Jugadores:", value=f"{info.players}/{info.max_players}")
        embed.add_field(name="🌐 Lenguaje:", value=info.language)
        embed.set_author(name=info.hostname)
        embed.set_thumbnail(url="https://i.imgur.com/9hMHjwy.png")
        embed.set_footer(text=f"🛠 {info.gamemode}")
        await ctx.respond(embed=embed, ephemeral=True)
@help.command(name = "novedades", description = "Enterate de las actualizaciones de nuestro bot.")
async def novedades(ctx):
    embed = discord.Embed(
    color=0x009cff,
    )
    embed.add_field(name="🔌 Actualizaciones & novedades de nuestro bot",
                value="""\n\n
                        > Novedades generales del Bot
                        **+** Se creó el bot\n
                         **+** Se agregó el comando */ayuda servidor*, para saber el estado de nuestro servidor SA-MP.\n
                         **+** Se agregó el comando */ayuda version*, para saber el estado de la versión del servidor.\n
                         **+** Se agregó el comando */ping*, para saber la latencia del bot.\n
                         **+** Se agregó el comando */verificar "token"*, para validar y vincular las cuentas de discord y del servidor SA-MP.\n
                         > Novedades administrativas del Bot
                         **+** Se agrego el comando */crear embed*, para añadir embeds personalizados.\n
                         **+** Se agrego el comando */crear token "Nombre_Apellido", para crear token de un usuario desde canal discord especifico.*\n
                         """)
    embed.set_author(name=botname)
    embed.set_thumbnail(url="https://i.imgur.com/9hMHjwy.png")
    embed.set_footer(text=botname)
    await ctx.respond(embed=embed, ephemeral=True)

@help.command(description="Revisa el ping de nuestro bot.") # this decorator makes a slash command
async def ping(ctx): # a slash command will be created with the name "ping"
    await ctx.respond(f"Pong! Nuestro ping es {bot.latency}", ephemeral=True)

crear = bot.create_group("crear", "¿Necesitas crear alguna configuración?")
@crear.command(name = "embed", description = "Crear embed")
async def embed(ctx, titulo, descripcion, color_embed: str, contentenido,banner_url):
    
    if any(role.id in MODS or role.position > MODS.position for role in ctx.author.roles):

        # Convertir el color de cadena a valor hexadecimal
        try:
            color_embed = int(color_embed, 16)
        except ValueError:
            await ctx.respond("Color inválido. Por favor, ingresa un color válido en formato hexadecimal.", ephemeral=True)
            return
        
        embed = discord.Embed(
            title=titulo,
            description=descripcion,
            color= color_embed,
        )

        # Añadir un campo al Embed con el contenido proporcionado
        embed.add_field(name='Contenido', value=contentenido, inline=False)

        # Añadir un footer personalizado al Embed
        embed.set_image(url=f"{banner_url}")
        embed.set_footer(text=botname)

        # Enviar el Embed al canal
        await ctx.send(embed=embed)
        await ctx.respond("Creaste el embed correctamente.", ephemeral=True)
    else:
        await ctx.respond("No estas autorizado para usar este comando.", ephemeral=True)
@crear.command(name="verificacion", description="Crea el dialogo de verificacion")
async def verificacion(ctx):
    if ctx.author.id == owner_id:
        embed = discord.Embed(title="Verificacion (Cuentas) | GreenZone Roleplay")
        embed.add_field(name="Informacion", value="Vincula y verifica la cuenta del servidor con la de nuestro discord.")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1114178012397719552/1115847426046185482/DA7GnGE.png")
        await ctx.respond("**[!]** Dialogo de verificacion creada correctamente", ephemeral=True)
        await ctx.send(embeds=[embed], view=verificarBoton())

@bot.slash_command(name="sancionar", description="Sanciona a un jugador.")
async def sancionar(ctx: discord.ApplicationContext, nombre_apellido, tiempo: int, razon: str):
    if isinstance(ctx.author.roles, (list, tuple)):
        if any(role.id in SUPERMODS for role in ctx.author.roles):
            sql = "SELECT ID, Username, TiempoJail, Online FROM usuarios WHERE Username = %s"
            sendSQL.execute(sql, (nombre_apellido,))
            result = sendSQL.fetchone()

            emisor = ctx.author.display_name
            tipo = 1

            tiempo_status = verificar_tiempo(tiempo)
            if tiempo_status:
                await ctx.respond(tiempo_status, ephemeral=True)
                return
            
            if not result:
                await ctx.respond("Este jugador no existe.", ephemeral=True)
                return

            if result[3] <= 0:
                await ctx.respond("El jugador no está conectado.", ephemeral=True)
                return

            if result[2] > 0:
                await ctx.respond("Este jugador ya fue sancionado.", ephemeral=True)
                return

            # Pasamos todas las validacione, procedemos a insertar.
            query = "INSERT INTO acciones_web (EmisorName, ReceptorName, Accion, Parametro, Tiempo) VALUES (%s, %s, %s, %s, %s)"
            sendSQL.execute(query, (emisor, nombre_apellido, tipo, razon, tiempo,))
            conn.commit()

            print(f"{emisor} sancionó a {nombre_apellido} por {tiempo} minuto/s. Razón: {razon}")
            await ctx.respond(f"**[!]** *{emisor}* sanciono a **{nombre_apellido}** por **{tiempo} minuto/s** por **{razon}**.")

        else:
            await ctx.respond("No estas autorizado para usar este comando.", ephemeral=True)
    else:
        print(f"there is no roles {ctx.author.roles}")
@bot.slash_command(name="banear", description="Banea a un jugador online")
async def banear(ctx: discord.ApplicationContext, nombre_apellido, razon: str):
    if isinstance(ctx.author.roles, (list, tuple)):
        if any(role.id in SUPERMODS for role in ctx.author.roles):
            #Comenzamos con las consultas, para saber si existe el usuario ingresado
            sql = "SELECT ID,Username,Baneado,Online,Admin FROM usuarios WHERE Username = %s"
            sendSQL.execute(sql, (nombre_apellido,))
            result = sendSQL.fetchone()
            
            emisor = ctx.author.display_name
            tipo = 2
            
            if not result:
                await ctx.respond("Este jugador no existe.", ephemeral=True)
                return

            if result[3] == 0:
                await ctx.respond("El jugador no está conectado.", ephemeral=True)
                return
            
            if result[4] > 0:
                await ctx.respond("No puedes banear a un jugador que pertenece al equipo.", ephemeral=True)
                return

            if result[2] == 1:
                await ctx.respond("Este jugador ya fue baneado.", ephemeral=True)
                return

            # Pasamos todas las validacione, procedemos a insertar.
            query = "INSERT INTO acciones_web (EmisorName, ReceptorName, Accion, Parametro) VALUES (%s, %s, %s, %s)"
            sendSQL.execute(query, (emisor, nombre_apellido, tipo, razon,))
            conn.commit()

            print(f"{emisor} baneo a {nombre_apellido} por {razon}.")
            await ctx.respond(f"**[!]** *{emisor}* baneo a **{nombre_apellido}** por **{razon}**.")

        else:
            await ctx.respond("No estas autorizado para usar este comando.", ephemeral=True)
    else:
        print(f"there is no roles {ctx.author.roles}")

@bot.slash_command(name="mutear", description="Mutea a un jugador")
async def mutear(ctx: discord.ApplicationContext, nombre_apellido, tiempo: int, razon: str):
    if isinstance(ctx.author.roles, (list, tuple)):
        if any(role.id in SUPERMODS for role in ctx.author.roles):
            #Comenzamos con las consultas, para saber si existe el usuario ingresado
            sql = "SELECT ID,Username,NMute,Online FROM usuarios WHERE Username = %s"
            sendSQL.execute(sql, (nombre_apellido,))
            result = sendSQL.fetchone()
            
            emisor = ctx.author.display_name
            tipo = 3

            tiempo_status = verificar_tiempo(tiempo)
            if tiempo_status:
                await ctx.respond(tiempo_status, ephemeral=True)
                return
            
            if not result:
                await ctx.respond("Este jugador no existe.", ephemeral=True)
                return

            if result[3] <= 0:
                await ctx.respond("El jugador no está conectado.", ephemeral=True)
                return

            if result[2] >= 1:
                await ctx.respond("Este jugador ya fue muteado.", ephemeral=True)
                return

            # Pasamos todas las validacione, procedemos a insertar.
            query = "INSERT INTO acciones_web (EmisorName, ReceptorName, Accion, Parametro, Tiempo) VALUES (%s, %s, %s, %s, %s)"
            sendSQL.execute(query, (emisor, nombre_apellido, tipo, razon, tiempo,))
            conn.commit()

            print(f"{emisor} muteó a {nombre_apellido} por {tiempo} minuto/s por {razon}.")
            await ctx.respond(f"**[!]** *{emisor}* muteo de Twitter a **{nombre_apellido}** por **{tiempo} minuto/s** por **{razon}**.")

        else:
            await ctx.respond("No estas autorizado para usar este comando.", ephemeral=True)
    else:
        print(f"there is no roles {ctx.author.roles}")
@bot.slash_command(name="supermute", description="Mutea a un jugador y borra el log del chat")
async def mutear(ctx: discord.ApplicationContext, nombre_apellido, tiempo: int, razon:str):
    if isinstance(ctx.author.roles, (list, tuple)):
        if any(role.id in SUPERMODS for role in ctx.author.roles):
            #Comenzamos con las consultas, para saber si existe el usuario ingresado
            sql = "SELECT ID,Username,NMute,Online FROM usuarios WHERE Username = %s"
            sendSQL.execute(sql, (nombre_apellido,))
            result = sendSQL.fetchone()
            
            emisor = ctx.author.display_name
            tipo = 4

            tiempo_status = verificar_tiempo(tiempo)
            if tiempo_status:
                await ctx.respond(tiempo_status, ephemeral=True)
                return
            
            if not result:
                await ctx.respond("Este jugador no existe.", ephemeral=True)
                return

            if result[3] <= 0:
                await ctx.respond("El jugador no está conectado.", ephemeral=True)
                return

            if result[2] >= 1:
                await ctx.respond("Este jugador ya fue muteado.", ephemeral=True)
                return

            # Pasamos todas las validacione, procedemos a insertar.
            query = "INSERT INTO acciones_web (EmisorName, ReceptorName, Accion, Parametro, Tiempo) VALUES (%s, %s, %s, %s, %s)"
            sendSQL.execute(query, (emisor, nombre_apellido, tipo, razon, tiempo,))
            conn.commit()

            print(f"{emisor} muteó a {nombre_apellido} por {tiempo} minuto/s por {razon}.")
            await ctx.respond(f"**[!]** *{emisor}* muteo de Twitter a **{nombre_apellido}** por **{tiempo} minuto/s** por **{razon}**.")

        else:
            await ctx.respond("No estas autorizado para usar este comando.", ephemeral=True)
    else:
        print(f"there is no roles {ctx.author.roles}")
@bot.slash_command(name="mutetw", description="Mutear de twitter a un jugador.")
async def mutear(ctx: discord.ApplicationContext, nombre_apellido, tiempo: int, razon: str):
    if isinstance(ctx.author.roles, (list, tuple)):
        if any(role.id in SUPERMODS for role in ctx.author.roles):
            #Comenzamos con las consultas, para saber si existe el usuario ingresado
            sql = "SELECT ID,Username,AMute,Online,Numero FROM usuarios WHERE Username = %s"
            sendSQL.execute(sql, (nombre_apellido,))
            result = sendSQL.fetchone()
            
            emisor = ctx.author.display_name
            tipo = 5

            tiempo_status = verificar_tiempo(tiempo)
            if tiempo_status:
                await ctx.respond(tiempo_status, ephemeral=True)
                return
            
            if not result:
                await ctx.respond("Este jugador no existe.", ephemeral=True)
                return

            if result[3] <= 0:
                await ctx.respond("El jugador no está conectado.", ephemeral=True)
                return

            if result[2] >= 1:
                await ctx.respond("Este jugador ya fue muteado.", ephemeral=True)
                return
            if result[4] <= 0:
                await ctx.respond("El jugador no tiene twitter o no tiene numero de telefono.", ephemeral=True)
                return

            # Pasamos todas las validacione, procedemos a insertar.
            query = "INSERT INTO acciones_web (EmisorName, ReceptorName, Accion, Parametro, Tiempo) VALUES (%s, %s, %s, %s, %s)"
            sendSQL.execute(query, (emisor, nombre_apellido, tipo, razon, tiempo,))
            conn.commit()

            print(f"{emisor} muteó a {nombre_apellido} por {tiempo} minuto/s por {razon}.")
            await ctx.respond(f"**[!]** *{emisor}* muteo de Twitter a **{nombre_apellido}** por **{tiempo} minuto/s** por **{razon}**.")

        else:
            await ctx.respond("No estas autorizado para usar este comando.", ephemeral=True)
    else:
        print(f"there is no roles {ctx.author.roles}")
bot.run(bot_token)
