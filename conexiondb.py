import sqlite3

class BCPDatabase:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.items_no_guardados = 0  

    def conectar(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            print(f'Conexión a la base de datos {self.db_file} establecida correctamente.')
        except sqlite3.Error as e:
            print(f'Error al conectar a la base de datos: {e}')

    def crear_tabla_bcp(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS BCP (
                    moneda TEXT,
                    codigo TEXT,
                    usd NUMERIC,
                    guaranies NUMERIC,
                    CONSTRAINT pk_bcp PRIMARY KEY (moneda, codigo)  -- Definir claves primarias compuestas
                )
            ''')
            self.conn.commit()
            print('Tabla BCP creada correctamente en la base de datos.')
        except sqlite3.Error as e:
            print(f'Error al crear la tabla BCP: {e}')

    def guardar_cotizaciones(self, cotizaciones):
        try:
            cursor = self.conn.cursor()
            items_no_guardados = 0
            for cotizacion in cotizaciones:
                try:
                    cursor.execute('''
                        INSERT INTO BCP (moneda, codigo, usd, guaranies)
                        VALUES (?, ?, ?, ?)
                    ''', cotizacion)
                except sqlite3.IntegrityError:  
                    items_no_guardados += 1
            
            self.conn.commit()
            print(f'Se han guardado {len(cotizaciones) - items_no_guardados} cotizaciones en la tabla BCP.')
            if items_no_guardados > 0:
                print(f'{items_no_guardados} items repetidos no se guardaron.')

            self.items_no_guardados = items_no_guardados  
        except sqlite3.Error as e:
            print(f'Error al insertar cotizaciones: {e}')

    def cerrar_conexion(self):
        if self.conn:
            self.conn.close()
            print(f'Conexión a la base de datos {self.db_file} cerrada.')

if __name__ == "__main__":
    db_file = 'dbBCP.db'
    database = BCPDatabase(db_file)
    database.conectar()
    database.crear_tabla_bcp()