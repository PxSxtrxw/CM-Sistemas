import sys
import json
from datetime import datetime
from bs4 import BeautifulSoup
from metodos import URLFetcher
from conexiondb import CommonDatabase
import requests


#CLASE BCP
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
                compra = self.convertir_numero(self.limpiar_texto(celdas[3].get_text(strip=True)))
                venta = self.convertir_numero(self.limpiar_texto(celdas[3].get_text(strip=True)))
                spread = venta - compra if compra is not None and venta is not None else None
                self.cotizaciones.append((moneda, codigo, compra, venta, spread))
            else:
                print(f"Advertencia: fila con número inesperado de celdas: {len(celdas)}. Saltando fila.")

    def limpiar_texto(self, texto):
        return texto.replace('\n', '').replace('\r', '').replace('*', '').strip()

    
    def guardar_en_sqlite(self, db_file):
        entidad = "Banco Central del Paraguay"
        database = CommonDatabase(db_file)
        database.conectar()
        database.guardar_cotizaciones(self.cotizaciones, entidad)
        database.cerrar_conexion()
        print(f'Las cotizaciones se han guardado en la base de datos {db_file}')

        stats = {
            "items_no_guardados": database.items_no_guardados,
            "items_actualizados": database.items_actualizados
        }
        with open('stats_bcp.json', 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=4, ensure_ascii=False)
        print(f'Estadísticas guardadas en stats_bcp.json')


    def guardar_en_json(self, json_file):
        data = {
            "sdtInfoCotizacion": {
                "entidad": "Banco Central del Paraguay",
                "fecha": datetime.now().strftime("%Y-%m-%d"),
                "pizarra": {
                    "pizarraItem": []
                }
            }
        }
        
        for cotizacion in self.cotizaciones:
            item = {
                "moneda": cotizacion[0],
                "codigo": cotizacion[1],
                "compra": cotizacion[3],
                "venta": cotizacion[3],
                "spread": cotizacion[4]
            }
            data["sdtInfoCotizacion"]["pizarra"]["pizarraItem"].append(item)

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f'Las cotizaciones se han guardado en el archivo JSON {json_file}')

    def convertir_numero(self, numero):
        if ',' in numero and '.' in numero:
            numero = numero.replace('.', '').replace(',', '.')
        elif ',' in numero:
            numero = numero.replace(',', '.')
        elif '.' in numero:
            pass
        try:
            return float(numero)
        except ValueError:
            return None



class CambiosChacoExtractor:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.cotizaciones = []

    def extraer_cotizaciones(self):
        try:
            fetcher = URLFetcher('cambioschaco')
            self.url = fetcher.url  # Obtener la URL correcta desde URLFetcher
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"No se pudo obtener la página web: {e}")

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='table table-hover cotiz-tabla')

        if not table:
            raise ValueError("No se pudo encontrar la tabla de cotizaciones en la página web")

        rows = table.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                nombre_moneda = cols[0].text.strip()
                compra = cols[1].text.strip()
                venta = cols[2].text.strip()

                codigo_moneda = self.obtener_codigo_moneda(nombre_moneda)

                try:
                    # Convertir compra y venta manteniendo comas como decimales y puntos como miles
                    compra_num = self.convertir_numero(compra)
                    venta_num = self.convertir_numero(venta)
                except ValueError:
                    continue

                spread = venta_num - compra_num

                self.cotizaciones.append((nombre_moneda, codigo_moneda, compra_num, venta_num, spread))

    def convertir_numero(self, valor):
        # Reemplazar puntos por comas para decimales y comas por puntos para miles
        valor = valor.replace('.', '').replace(',', '.')
        return float(valor)

    def obtener_codigo_moneda(self, nombre_moneda):
        nombre_moneda = nombre_moneda.lower().strip()

        if "dólar americano" in nombre_moneda or "us dollar" in nombre_moneda:
            return "USD"
        elif "real" in nombre_moneda or "brazilian" in nombre_moneda:
            return "BRL"
        elif "peso argentino" in nombre_moneda or "argentine peso" in nombre_moneda:
            return "ARS"
        elif "euro" in nombre_moneda:
            return "EUR"
        elif "peso chileno" in nombre_moneda or "chilean peso" in nombre_moneda:
            return "CLP"
        elif "peso uruguayo" in nombre_moneda or "uruguayan peso" in nombre_moneda:
            return "UYU"
        elif "peso colombiano" in nombre_moneda or "colombian peso" in nombre_moneda:
            return "COP"
        elif "peso mexicano" in nombre_moneda or "mexican peso" in nombre_moneda:
            return "MXN"
        elif "boliviano" in nombre_moneda or "bolivian boliviano" in nombre_moneda:
            return "BOB"
        elif "nuevo sol peruano" in nombre_moneda or "peruvian nuevo sol" in nombre_moneda:
            return "PEN"
        elif "dólar canadiense" in nombre_moneda or "canadian dollar" in nombre_moneda:
            return "CAD"
        elif "dólar australiano" in nombre_moneda or "australian dollar" in nombre_moneda:
            return "AUD"
        elif "corona noruega" in nombre_moneda or "norwegian krone" in nombre_moneda:
            return "NOK"
        elif "corona danesa" in nombre_moneda or "danish krone" in nombre_moneda:
            return "DKK"
        elif "corona sueca" in nombre_moneda or "swedish krona" in nombre_moneda:
            return "SEK"
        elif "libra esterlina" in nombre_moneda or "british pound sterling" in nombre_moneda:
            return "GBP"
        elif "franco suizo" in nombre_moneda or "swiss franc" in nombre_moneda:
            return "CHF"
        elif "yen japonés" in nombre_moneda or "japanese yen" in nombre_moneda:
            return "JPY"
        elif "dinar kuwaiti" in nombre_moneda or "kuwaiti dinar" in nombre_moneda:
            return "KWD"
        elif "shekel israelí" in nombre_moneda or "israeli new sheqel" in nombre_moneda:
            return "ILS"
        elif "rand sudafricano" in nombre_moneda or "south african rand" in nombre_moneda:
            return "ZAR"
        elif "rublo ruso" in nombre_moneda or "russian ruble" in nombre_moneda:
            return "RUB"
        else:
            return "DESCONOCIDO"

    def guardar_en_sqlite(self, db_file):
        entidad = "Cambios Chaco Sociedad Anonima"
        database = CommonDatabase(db_file)
        database.conectar()
        database.guardar_cotizaciones(self.cotizaciones, entidad)
        database.cerrar_conexion()
        print(f'Las cotizaciones se han guardado en la base de datos {db_file}')

        stats = {
            "items_no_guardados": database.items_no_guardados,
            "items_actualizados": database.items_actualizados
        }
        with open('stats_bcp.json', 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=4, ensure_ascii=False)
        print(f'Estadísticas guardadas en stats_bcp.json')

    def guardar_en_json(self, json_file):
        data = {
            "sdtInfoCotizacion": {
                "entidad": "Cambios Chaco Sociedad Anonima",
                "fecha": datetime.now().strftime("%Y-%m-%d"),
                "pizarra": {
                    "pizarraItem": []
                }
            }
        }
        
        for cotizacion in self.cotizaciones:
            item = {
                "moneda": cotizacion[0],
                "codigo": cotizacion[1],
                "compra": cotizacion[2],
                "venta": cotizacion[3],
                "spread": cotizacion[4]
            }
            data["sdtInfoCotizacion"]["pizarra"]["pizarraItem"].append(item)

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f'Las cotizaciones se han guardado en el archivo JSON {json_file}')





class CambiosAlberdiExtractor:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.cotizaciones = []

    def extraer_cotizaciones(self):
        try:
            fetcher = URLFetcher('cambiosalberdi')
            self.url = fetcher.url  # Obtener la URL correcta desde URLFetcher
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"No se pudo obtener la página web: {e}")

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='table')

        if not table:
            raise ValueError("No se pudo encontrar la tabla de cotizaciones en la página web")

        rows = table.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                nombre_moneda = cols[0].text.strip()
                compra = cols[1].text.strip()
                venta = cols[2].text.strip()

                codigo_moneda = self.obtener_codigo_moneda(nombre_moneda)

                try:
                    # Convertir compra y venta manteniendo comas como decimales y puntos como miles
                    compra_num = self.convertir_numero(compra)
                    venta_num = self.convertir_numero(venta)
                except ValueError:
                    continue

                spread = venta_num - compra_num

                self.cotizaciones.append((nombre_moneda, codigo_moneda, compra_num, venta_num, spread))

    def convertir_numero(self, valor):
        # Reemplazar comas por puntos para decimales y puntos por nada para miles
        valor = valor.replace(',', '.').replace('.', '')
        return float(valor)

    def obtener_codigo_moneda(self, nombre_moneda):
        if "Dólar Americano" in nombre_moneda:
            return "USD"
        elif "Real Brasileño" in nombre_moneda:
            return "BRL"
        elif "EURO" in nombre_moneda:
            return "EUR"
        elif "Peso Argentino" in nombre_moneda:
            return "ARS"
        elif "Dólar Americano x Real Brasileño" in nombre_moneda:
            return "USD_BRL"
        elif "Dólar Americano x EURO" in nombre_moneda:
            return "USD_EUR"
        elif "Dólar Americano x Peso Argentino" in nombre_moneda:
            return "USD_ARS"
        elif "Dólar Cheque" in nombre_moneda:
            return "USD"
        elif "Yen Japones" in nombre_moneda:
            return "JPY"
        elif "Libra Esterlina" in nombre_moneda:
            return "GBP"
        elif "Dólar Canadiense" in nombre_moneda:
            return "CAD"
        elif "Peso Chileno" in nombre_moneda:
            return "CLP"
        elif "Peso Uruguayo" in nombre_moneda:
            return "UYU"
        elif "Franco Suizo" in nombre_moneda:
            return "CHF"
        else:
            return "DESCONOCIDO"

    def guardar_en_sqlite(self, db_file):
        entidad = "Cambios Alberdi Sociedad Anonima"
        database = CommonDatabase(db_file)
        database.conectar()
        database.guardar_cotizaciones(self.cotizaciones, entidad)
        database.cerrar_conexion()
        print(f'Las cotizaciones se han guardado en la base de datos {db_file}')

        stats = {
            "items_no_guardados": database.items_no_guardados,
            "items_actualizados": database.items_actualizados
        }
        with open('stats_bcp.json', 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=4, ensure_ascii=False)
        print(f'Estadísticas guardadas en stats_bcp.json')


    def guardar_en_json(self, json_file):
        data = {
            "sdtInfoCotizacion": {
                "entidad": "Cambios Alberdi Sociedad Anonima",
                "fecha": datetime.now().strftime("%Y-%m-%d"),
                "pizarra": {
                    "pizarraItem": []
                }
            }
        }
        
        for cotizacion in self.cotizaciones:
            item = {
                "moneda": cotizacion[0],
                "codigo": cotizacion[1],
                "compra": cotizacion[2],
                "venta": cotizacion[3],
                "spread": cotizacion[4]
            }
            data["sdtInfoCotizacion"]["pizarra"]["pizarraItem"].append(item)

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f'Las cotizaciones se han guardado en el archivo JSON {json_file}')






# CLASE MAXICAMBIO
class MaxicambiosExtractor:
    def __init__(self, url):
        self.url = url
        self.cotizaciones = []

    def extraer_cotizaciones(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"No se pudo obtener la página web: {e}")

        soup = BeautifulSoup(response.content, 'html.parser')
        cotizaciones = soup.find_all('div', class_='cotizDivSmall')

        seen_currencies = set()

        for cotizacion in cotizaciones:
            nombre_moneda_tag = cotizacion.find('p', class_='ng-tns-c4-0')
            if nombre_moneda_tag:
                currency_name = nombre_moneda_tag.text.strip()

                if currency_name in seen_currencies:
                    continue

                seen_currencies.add(currency_name)

                compra_tag = cotizacion.find('p', string='Compra')
                venta_tag = cotizacion.find('p', string='Venta')

                if compra_tag and venta_tag:
                    compra_value = compra_tag.find_next('p', class_='ng-tns-c4-0').text.strip()
                    venta_value = venta_tag.find_next('p', class_='ng-tns-c4-0').text.strip()

                    try:
                        compra_value = float(compra_value.replace(',', '.'))
                        venta_value = float(venta_value.replace(',', '.'))
                    except ValueError:
                        continue

                    codigo_moneda = self.obtener_codigo_moneda(currency_name)

                    self.cotizaciones.append((
                        currency_name,
                        codigo_moneda,
                        compra_value,
                        venta_value,
                        self.calcular_spread(compra_value, venta_value)
                    ))

    def obtener_codigo_moneda(self, nombre_moneda):
        monedas = {
            "Dólar": "USD",
            "Peso Arg": "ARS",
            "Real": "BRL",
            "Peso Uru": "UYU",
            "Euro": "EUR",
            "Libra": "GBP",
            "Yen": "JPY",
            "Peso Chi": "CLP",
            "Rand": "ZAR",
            "Dólar Ca..": "CAD",
            "Dólar Au..": "AUD",
            "Franco": "CHF",
            "Peso Mex": "MXN",
            "Sol": "PEN",
            "Peso Bol": "BOB",
            "Peso Col": "COP",
            "Peso": "ARS",
            "Dólar x Euro": "USD_EUR",
            "Peso x Dólar": "ARS_USD",
            "Real x Dólar": "BRL_USD",
        }
        return monedas.get(nombre_moneda, "DESCONOCIDO")

    def calcular_spread(self, compra, venta):
        try:
            return venta - compra
        except TypeError:
            return None

    def guardar_en_sqlite(self, db_file):
        entidad = "Maxicambios"
        database = CommonDatabase(db_file)
        database.conectar()
        database.guardar_cotizaciones(self.cotizaciones, entidad)
        database.cerrar_conexion()
        print(f'Las cotizaciones se han guardado en la base de datos {db_file}')

        stats = {
            "items_no_guardados": database.items_no_guardados,
            "items_actualizados": database.items_actualizados
        }
        with open('stats_bcp.json', 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=4, ensure_ascii=False)
        print(f'Estadísticas guardadas en stats_bcp.json')


    def guardar_en_json(self, json_file):
        data = {
            "sdtInfoCotizacion": {
                "entidad": "Maxicambios",
                "fecha": datetime.now().strftime("%Y-%m-%d"),
                "pizarra": {
                    "pizarraItem": []
                }
            }
        }

        for cotizacion in self.cotizaciones:
            item = {
                "moneda": cotizacion[0],
                "codigo": cotizacion[1],
                "compra": cotizacion[2],
                "venta": cotizacion[3],
                "spread": cotizacion[4]
            }
            data["sdtInfoCotizacion"]["pizarra"]["pizarraItem"].append(item)

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f'Las cotizaciones se han guardado en el archivo JSON {json_file}')

        

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scraping.py <método>")
        sys.exit(1)

    metodo = sys.argv[1].lower()  # Convertir a minúsculas
    fetcher = URLFetcher(metodo)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    db_file = 'cotizaciones.db'  # Nombre único para la base de datos
    json_file = f'cotizaciones_{metodo}.json' 

    if metodo == "bcp":
        extractor = CotizacionesExtractor(fetcher.url, headers)
        tabla = 'bcp'
        stats_file = 'stats_bcp.json'
    elif metodo == "cambioschaco":
        extractor = CambiosChacoExtractor(fetcher.url, headers)
        tabla = 'cambioschaco'
        stats_file = 'stats_cambioschaco.json'
    elif metodo == "cambiosalberdi":
        extractor = CambiosAlberdiExtractor(fetcher.url, headers)
        tabla = 'cambiosalberdi'
        stats_file = 'stats_cambiosalberdi.json'
    elif metodo == "maxicambios":
        extractor = MaxicambiosExtractor(fetcher.url)
        tabla = 'maxicambios'
        stats_file = 'stats_maxicambios.json'
    else:
        raise ValueError("Método no soportado. Por favor, elige 'bcp', 'cambioschaco', 'cambiosalberdi' o 'maxicambios'.")

    extractor.extraer_cotizaciones()  # Asegúrate de llamar al método correcto
    extractor.guardar_en_sqlite(db_file)  # Utiliza el método adecuado para guardar en SQLite con el nombre de la tabla
    extractor.guardar_en_json(json_file)  # Utiliza el método adecuado para guardar en JSON
    print(f'Cotizaciones extraídas y guardadas correctamente para {metodo}')