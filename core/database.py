from core.config import *

conn = mysql.connector.connect(
    host= os.getenv('HOST_MYSQL'),
    user=  os.getenv('USER_MYSQL'),
    password=os.getenv('PASS_MYSQL'),
    database= os.getenv('DB_MYSQL')
)
sendSQL = conn.cursor()

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