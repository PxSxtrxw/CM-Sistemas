import subprocess
from flask import Flask, Response
from jsonn import CotizacionesParser
from logger import log_interaccion, log_error

app = Flask(__name__)

def ejecutar_scraping():
    try:
        subprocess.run(['python', 'scraping.py'], check=True, stdout=subprocess.PIPE)
        log_interaccion("Scraping completado.")
    except subprocess.CalledProcessError as e:
        log_error(f"Error al ejecutar scraping.py: {e}")

def ejecutar_jsonn():
    try:
        subprocess.run(['python', 'jsonn.py'], check=True, stdout=subprocess.PIPE)
        log_interaccion("JSON creado correctamente.")
    except subprocess.CalledProcessError as e:
        log_error(f"Error al ejecutar jsonn.py: {e}")

def contar_cotizaciones():
    try:
        parser = CotizacionesParser('datos.csv')
        parser.cargar_datos_desde_csv()
        datos_json = parser.obtener_datos_json()
        num_cotizaciones = len(parser.data["sdtInfoCotizacion"]["pizarra"]["pizarraItem"])
        log_interaccion(f"{num_cotizaciones} cotizaciones guardadas correctamente.")

    except Exception as e:
        log_error(f"Error al contar las cotizaciones: {e}")

@app.route('/bcp', methods=['GET'])
def obtener_cotizaciones():
    try:
        parser = CotizacionesParser('datos.csv')
        parser.cargar_datos_desde_csv()
        datos_json = parser.obtener_datos_json()
        log_interaccion("Se han obtenido las cotizaciones correctamente.")
        
        response = Response(response=datos_json, status=200, mimetype="application/json")
        return response
    
    except Exception as e:
        log_error(f"Error al obtener las cotizaciones: {e}")
        return Response(status=500)

if __name__ == '__main__':
    ejecutar_scraping()
    ejecutar_jsonn()
    contar_cotizaciones()

    host = 'localhost'
    port = 3000

    log_interaccion(f'Servidor en ejecucion: http://{host}:{port}/bcp')
    
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    app.run(host=host, port=port, debug=False)
