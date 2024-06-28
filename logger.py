import logging

# Configuración del logger para actividades
actividad_logger = logging.getLogger('actividad_logger')
actividad_handler = logging.FileHandler('actividades.log')
actividad_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
actividad_logger.addHandler(actividad_handler)
actividad_logger.setLevel(logging.INFO)

# Configuración del logger para errores
error_logger = logging.getLogger('error_logger')
error_handler = logging.FileHandler('errores.log')
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
error_logger.addHandler(error_handler)
error_logger.setLevel(logging.ERROR)

# Función para registrar una interacción exitosa
def log_interaccion(mensaje):
    actividad_logger.info(f'{mensaje}')

# Función para registrar un error
def log_error(mensaje):
    error_logger.error(f'{mensaje}')
