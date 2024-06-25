import csv
import json
from datetime import datetime

class CotizacionesParser:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.data = {
            "sdtInfoCotizacion": {
                "entidad": "Banco Central del Paraguay",
                "fecha": datetime.now().strftime("%Y-%m-%d"),
                "pizarra": {
                    "pizarraItem": []
                }
            }
        }

    def cargar_datos_desde_csv(self):
        with open(self.csv_file, 'r', encoding='utf-8') as archivo:
            lector_csv = csv.reader(archivo)
            next(lector_csv)  # Saltar encabezado

            for row in lector_csv:
                if len(row) >= 4:
                    moneda = self.limpiar_moneda(row[0].strip())
                    codigo = row[1].strip()
                    me_usd = row[2].strip()
                    guarani_me = row[3].strip()

                    item = {
                        "moneda": moneda,
                        "codigo": codigo,
                        "USD": self.convertir_numero(me_usd),
                        "Guaranies": self.convertir_numero(guarani_me)
                    }

                    self.data["sdtInfoCotizacion"]["pizarra"]["pizarraItem"].append(item)
                else:
                    print(f"Advertencia: fila con número inesperado de celdas: {len(row)}. Saltando fila.")

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

    def limpiar_moneda(self, moneda):
        return moneda.replace("*", "").strip()

    def obtener_datos_json(self):
        return json.dumps(self.data, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    parser = CotizacionesParser('datos.csv')
    parser.cargar_datos_desde_csv()
    datos_json = parser.obtener_datos_json()
    print(datos_json)
