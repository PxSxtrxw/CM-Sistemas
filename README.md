# CM-Sistemas

## App de Scraping en Python

### 📅 Martes 24/6/24

Este proyecto tiene como objetivo extraer datos mediante web scraping y alojarlos en un servidor HTTP y en una base de datos desde la página del [Banco Central Paraguayo](https://www.bcp.gov.py/webapps/web/cotizacion/monedas). Los datos recopilados incluyen:

-  Moneda
-  Código
-  Spread
-  Compra
-  Venta

### 🛠️ Librerías Usadas

- BeautifulSoup
- Requests
- Sqlite3
- Datetime
- Subprocess
- Json
- Flask
- Csv
- Logging

### 🗂️ Funcionalidad de cada archivo

#### `server.py`

- **Descripción**: Crea un servidor HTTP en `http://localhost:3000/` que aloja la estructura JSON con los datos mencionados. También ejecuta `scraping.py`.
- **Uso**: Ejecutar `server.py` para iniciar el servidor y realizar el scraping automáticamente.

#### `scraping.py`

- **Descripción**: Envía una solicitud HTTP a los métodos seleccionados, extrae los datos, los convierte en estructura JSON y los guarda en la base de datos `cotizaciones.db`.
- **Uso**: Se ejecuta automáticamente al iniciar `server.py`.

#### `logger.py`

- **Descripción**: Registra todas las actividades en `actividades.log` y los errores en `errores.log` al momento de crear el servidor HTTP.
- **Uso**: Incluido y utilizado en `server.py` para el manejo de logs.

#### `conexiondb.py`

- **Descripción**: Establece la conexión a la base de datos `cotizaciones.db` y guarda los datos recibidos. Se asegura de actualizar los registros si ya existen con valores diferentes.
- **Uso**: Utilizado internamente por `scraping.py`.

#### `metodos.py`

- **Descripción**: Contiene los métodos registrados para [BCP](https://www.bcp.gov.py/webapps/web/cotizacion/monedas), [Maxicambios](https://www.maxicambios.com.py), [Cambios Chaco](https://www.cambioschaco.com.py), [Cambios Alberdi](https://www.cambiosalberdi.com/langes/). Estos métodos son utilizados por `scraping.py`, `conexiondb.py` y `logger.py` para sus operaciones correspondientes.

