from core.libs import *
from core.config import *
from functions.clases import *
from functions.utils import *

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