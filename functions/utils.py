from core.config import *
from core.libs import *

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