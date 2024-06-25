import requests
from bs4 import BeautifulSoup
from conexiondb import BCPDatabase  

class CotizacionesExtractor:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.cotizaciones = []

    def extraer_cotizaciones(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"No se pudo obtener la página web: {e}")

        soup = BeautifulSoup(response.text, 'html.parser')
        tabla = soup.find('table', {'id': 'cotizacion-interbancaria'})

        if not tabla:
            raise ValueError("No se pudo encontrar la tabla de cotizaciones en la página web")

        filas = tabla.find_all('tr')

        for fila in filas:
            celdas = fila.find_all('td')
            if len(celdas) >= 4:
                moneda = self.limpiar_texto(celdas[0].get_text(strip=True))
                codigo = self.limpiar_texto(celdas[1].get_text(strip=True))
                me_usd = self.limpiar_texto(celdas[2].get_text(strip=True))
                guarani_me = self.limpiar_texto(celdas[3].get_text(strip=True))
                self.cotizaciones.append((moneda, codigo, me_usd, guarani_me))  # Cambiado a tuplas para ser compatible con SQLite
            else:
                print(f"Advertencia: fila con número inesperado de celdas: {len(celdas)}. Saltando fila.")

    def limpiar_texto(self, texto):
        return texto.replace('\n', '').replace('\r', '')

    def guardar_en_sqlite(self, db_file):
        database = BCPDatabase(db_file)
        database.conectar()
        database.crear_tabla_bcp()
        database.guardar_cotizaciones(self.cotizaciones)
        database.cerrar_conexion()

        print(f'Las cotizaciones se han guardado en la base de datos {db_file}')

# Ejemplo de uso:
if __name__ == "__main__":
    url = "https://www.bcp.gov.py/webapps/web/cotizacion/monedas"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    db_file = 'dbBCP.db'

    extractor = CotizacionesExtractor(url, headers)
    extractor.extraer_cotizaciones()
    extractor.guardar_en_sqlite(db_file)
