import subprocess
import json
from flask import Flask, Response
from logger import log_interaccion, log_error

app = Flask(__name__)

def ejecutar_scraping(metodo):
    try:
        subprocess.run(['python', 'scraping.py', metodo], check=True, stdout=subprocess.PIPE)
        log_interaccion(f"-----------------------------------------------------------------------")
        log_interaccion(f"Scraping completado para el metodo {metodo} y JSON creado.")
    except subprocess.CalledProcessError as e:
        log_error(f"Error al ejecutar scraping.py para el metodo {metodo}: {e}")

def registrar_estadisticas(metodo):
    try:
        with open(f'stats_{metodo}.json', 'r', encoding='utf-8') as file:
            stats = json.load(file)
            items_no_guardados = stats.get("items_no_guardados", 0)
            items_actualizados = stats.get("items_actualizados", 0)
            log_interaccion(f"{items_actualizados} cotizaciones fueron actualizadas para el metodo {metodo}.")
    except Exception as e:
        log_error(f"Error al registrar las estadísticas para el metodo {metodo}: {e}")

def contar_cotizaciones(metodo):
    try:
        json_file = f'cotizaciones_{metodo}.json'
        with open(json_file, 'r', encoding='utf-8') as file:
            datos_json = json.load(file)
            num_cotizaciones = len(datos_json["sdtInfoCotizacion"]["pizarra"]["pizarraItem"])
            log_interaccion(f"{num_cotizaciones} cotizaciones procesadas en total para el metodo {metodo}.")
    except Exception as e:
        log_error(f"Error al contar las cotizaciones para el metodo {metodo}: {e}")

@app.route('/<metodo>', methods=['GET'])
def obtener_cotizaciones(metodo):
    metodos_validos = ['bcp', 'cambioschaco', 'cambiosalberdi', 'maxicambios']
    
    if metodo not in metodos_validos:
        log_error(f"Metodo no soportado: {metodo}")
        return Response(response=json.dumps({"error": "Metodo no soportado"}), status=400, mimetype="application/json")
    
    ejecutar_scraping(metodo)
    registrar_estadisticas(metodo)
    contar_cotizaciones(metodo)
    
    try:
        json_file = f'cotizaciones_{metodo}.json'
        with open(json_file, 'r', encoding='utf-8') as file:
            datos_json = file.read()
        log_interaccion(f"Se han obtenido las cotizaciones correctamente para el metodo {metodo}.")
        log_interaccion(f"-----------------------------------------------------------------------")

        response = Response(response=datos_json, status=200, mimetype="application/json")
        return response
    
    except Exception as e:
        log_error(f"Error al obtener las cotizaciones para el metodo {metodo}: {e}")
        return Response(status=500)

if __name__ == '__main__':
    host = 'localhost'
    port = 3000

    log_interaccion(f'Servidor en ejecucion en: http://{host}:{port}/')

    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    app.run(host=host, port=port, debug=False)
