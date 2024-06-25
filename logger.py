import logging

# Configuración del logger para actividades
logging.basicConfig(
    filename='actividades.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Configuración del logger para errores
error_logger = logging.getLogger('error_logger')
error_handler = logging.FileHandler(filename='errores.log')
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
error_logger.addHandler(error_handler)
error_logger.setLevel(logging.ERROR)

# Función para registrar una interacción exitosa
def log_interaccion(mensaje):
    logging.info(f' {mensaje}')

# Función para registrar un error
def log_error(mensaje):
    error_logger.error(f' {mensaje}')
