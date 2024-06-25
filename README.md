# CM-Sistemas
## App de Scraping en Python

### Martes 24/6/24
Proyecto de extraccion de datos con el metodo scraping y alojamiento en un servidor HTTP como asi tambien en una base de datos a la paguina  [Banco Central Paraguayo]([https://www.cambioschaco.com.py](https://www.bcp.gov.py/webapps/web/cotizacion/monedas)) con el objetivo de recopilar los siguientes datos:

- Moneda
- Código
- Spread
- Compra
- Venta

### Librerías Usadas
- BeautifulSoup
- Requests
- Sqlite3
- Datetime
- Subprocess
- Json
- Flask
- Csv

### Funcionalidad de cada archivo
- server.py:
  crea un servidor HTTP con la ruta http://localhost:3000/bcp la cual aloja la estructura json con los datos mencionados anteriormente y a la ves ejecuta otros 2 archivos los cuales son scraping.py y jsonn.py

- scraping.py:
  manda una solicitud HTTP a la paguina [Banco Central Paraguayo]([https://www.cambioschaco.com.py](https://www.bcp.gov.py/webapps/web/cotizacion/monedas)) y extrae los datos anteriormente mencionados y los aloja en un archivo .csv (data.csv) y tambien los guarda en una base de datos (dbBCP.db)

- jsonn.py:
  extrae los datos del archivo data.csv y lo convierte en una estructura json

- logger.py:
  registra todas las actividades (actividades.log) y errores (errores.log) al momento de crearse el servidor HTTP

- conexiondb.py:
  establece la conexion a la base de datos (dbBCP.db) y guarda los datos recividos

- metodos.py:
  por terminar
  
  
  
