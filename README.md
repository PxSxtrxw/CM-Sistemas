# CM-Sistemas
## App de Scraping en Python

### 📅 Martes 24/6/24
Este proyecto tiene como objetivo extraer datos mediante web scraping y alojarlos en un servidor HTTP y en una base de datos desde la página del [Banco Central Paraguayo](https://www.bcp.gov.py/webapps/web/cotizacion/monedas). Los datos recopilados incluyen:

- Moneda
- Código
- Spread
- Compra
- Venta

### 🛠️ Librerías Usadas
- BeautifulSoup
- Requests
- Sqlite3
- Datetime
- Subprocess
- Json
- Flask
- Csv

### 🗂️ Funcionalidad de cada archivo

#### `server.py`
- **Descripción**: Crea un servidor HTTP en `http://localhost:3000/bcp` que aloja la estructura JSON con los datos mencionados. También ejecuta `scraping.py` y `jsonn.py`.
- **Uso**: Ejecutar `server.py` para iniciar el servidor y realizar el scraping automáticamente.

#### `scraping.py`
- **Descripción**: Envía una solicitud HTTP a la página del [Banco Central Paraguayo](https://www.bcp.gov.py/webapps/web/cotizacion/monedas), extrae los datos y los guarda en `data.csv` y en la base de datos `dbBCP.db`.
- **Uso**: Se ejecuta automáticamente al iniciar `server.py`.

#### `jsonn.py`
- **Descripción**: Convierte los datos del archivo `data.csv` en una estructura JSON.
- **Uso**: Se ejecuta automáticamente al iniciar `server.py`.

#### `logger.py`
- **Descripción**: Registra todas las actividades en `actividades.log` y los errores en `errores.log` al momento de crear el servidor HTTP.
- **Uso**: Incluido y utilizado en `server.py` para el manejo de logs.

#### `conexiondb.py`
- **Descripción**: Establece la conexión a la base de datos `dbBCP.db` y guarda los datos recibidos.
- **Uso**: Utilizado internamente por `scraping.py`.

#### `metodos.py`
- **Estado**: Por terminar
- **Descripción**: Contendrá métodos adicionales para el manejo y procesamiento de datos.
