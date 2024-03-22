
from core.database import *
from functions.utils import *

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
                        role_id = 1144847820424228914  # ID del rol "Usuario"
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