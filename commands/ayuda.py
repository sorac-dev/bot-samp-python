from core.config import *

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

