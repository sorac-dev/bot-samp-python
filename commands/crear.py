from core.config import *
from functions.clases import *

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
    if ctx.author.id == 352897123014148096:
        embed = discord.Embed(title="Verificacion (Cuentas) | GreenZone Roleplay")
        embed.add_field(name="Informacion", value="Vincula y verifica la cuenta del servidor con la de nuestro discord.")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1114178012397719552/1115847426046185482/DA7GnGE.png")
        await ctx.respond("**[!]** Dialogo de verificacion creada correctamente", ephemeral=True)
        await ctx.send(embeds=[embed], view=verificarBoton())