from flask import Flask, request, send_file
from cryptography.fernet import Fernet
import logging
import psycopg2
import os

app = Flask(__name__)

# Configuración de los Logs
logging.basicConfig(filename='registro_eventos.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Gestión de la Llave Maestra
def obtener_clave():
    # Lee la llave del archivo local para no perder los datos al reiniciar
    if os.path.exists("secret.key"):
        with open("secret.key", "rb") as archivo:
            return archivo.read()
    else:
        clave_nueva = Fernet.generate_key()
        with open("secret.key", "wb") as archivo:
            archivo.write(clave_nueva)
        return clave_nueva

cifrador = Fernet(obtener_clave())

# Conexión a la Base de Datos PostgreSQL
def obtener_conexion():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "base_de_datos"),
        database=os.environ.get("DB_NAME", "registro_usuarios"),
        user=os.environ.get("DB_USER", "admin_rayan"),
        # La contraseña real debe ir en el docker-compose o .env, no aquí
        password=os.environ.get("DB_PASSWORD", "contrasena_falsa_por_defecto")
    )

# Crear la tabla automáticamente al arrancar
def inicializar_bd():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                correo_cifrado TEXT NOT NULL
            )
        """)
        conexion.commit()
        cursor.close()
        conexion.close()
        print("Base de datos lista y conectada.")
    except Exception as e:
        logging.error(f"Error conectando a la BD: {e}")

inicializar_bd()

@app.route('/')
def inicio():
    return send_file('../frontend/index.html')

@app.route('/api/registro', methods=['POST'])
def registrar():
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')

    if not nombre or not correo:
        logging.warning(f"Error: Faltan datos desde IP {request.remote_addr}")
        return "ERROR: Faltan datos", 400

    # CIFRADO AES
    correo_cifrado = cifrador.encrypt(correo.encode()).decode()

    # Guardar en PostgreSQL
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, correo_cifrado) VALUES (%s, %s)",
            (nombre, correo_cifrado)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        logging.info(f"Registro OK y guardado en BD - Usuario: {nombre}")
    except Exception as e:
        logging.error(f"Error guardando en BD: {e}")
        return "ERROR INTERNO DEL SERVIDOR", 500
    
    return f"""
    <div style='font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background-color: #f0f2f5; color: #1c1e21; padding: 40px; text-align: center; height: 100vh; margin: 0; display: flex; flex-direction: column; justify-content: center; align-items: center;'>
        <div style='background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 500px;'>
            <h2 style='margin-top: 0; color: #1877f2;'>Registro completado</h2>
            <p>Usuario <b>{nombre}</b> validado e insertado en la base de datos.</p>
            <hr style='border: 1px solid #dddfe2; margin: 20px 0;'>
            <p style='font-size: 14px; color: #606770;'>Cifrado AES aplicado:</p>
            <p style='background: #f0f2f5; padding: 10px; border-radius: 4px; font-family: monospace; word-break: break-all; font-size: 12px;'>{correo_cifrado[:60]}...</p>
        </div>
    </div>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

