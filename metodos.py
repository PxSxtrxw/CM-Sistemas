import requests

class URLFetcher:
    def __init__(self, metodo):
        self.metodos = {
            'bcp': {
                'url': "https://www.bcp.gov.py/webapps/web/cotizacion/monedas",
                'entidad': "Banco Central del Paraguay"
            },
            'cambioschaco': {
                'url': "https://www.cambioschaco.com.py",
                'entidad': "Cambios Chaco Sociedad Anonima (Asuncion)"
            },
            'cambiosalberdi': {
                'url': "https://www.cambiosalberdi.com/langes/index.php#sectionCotizacion",
                'entidad': "Cambios Alberdi S:A Confianza y Solidez (Asuncion)"
            },
            'maxicambios': {
                'url': "https://www.maxicambios.com.py",
                'entidad': "Maxicambios"
            }
        }

        metodo_info = self.metodos.get(metodo)
        if not metodo_info:
            raise ValueError(f"El método {metodo} no es soportado.")
        
        self.url = metodo_info['url']
        self.entidad = metodo_info['entidad']

    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.text
        else:
            return None

    @classmethod
    def registrar_metodo(cls, metodo, url, entidad):
        cls.metodos[metodo] = {
            'url': url,
            'entidad': entidad
        }
