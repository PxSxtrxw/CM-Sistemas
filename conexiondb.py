import sqlite3
from datetime import datetime

class CommonDatabase:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.items_no_guardados = 0
        self.items_actualizados = 0

    def conectar(self):
        self.conn = sqlite3.connect(self.db_file)
        self.crear_tabla_unica()

    def cerrar_conexion(self):
        if self.conn:
            self.conn.close()

    def crear_tabla_unica(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS cotizaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entidad TEXT,
            moneda TEXT,
            codigo TEXT,
            compra REAL,
            venta REAL,
            spread REAL,
            fecha_actualizacion TEXT,
            UNIQUE(entidad, moneda, codigo)  -- Agrega una restricción de unicidad
        )
        ''')
        self.conn.commit()

    def cotizacion_existe(self, moneda, codigo, entidad):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT 1 FROM cotizaciones WHERE moneda = ? AND codigo = ? AND entidad = ?
        ''', (moneda, codigo, entidad))
        return cursor.fetchone() is not None

    def guardar_cotizaciones(self, cotizaciones, entidad):
        cursor = self.conn.cursor()
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")

        for cotizacion in cotizaciones:
            moneda = cotizacion[0]
            codigo = cotizacion[1]
            compra = cotizacion[2]
            venta = cotizacion[3]
            spread = cotizacion[4]

            if self.cotizacion_existe(moneda, codigo, entidad):
                try:
                    cursor.execute('''
                        UPDATE cotizaciones
                        SET compra = ?,
                            venta = ?,
                            spread = ?,
                            fecha_actualizacion = ?
                        WHERE moneda = ? AND codigo = ? AND entidad = ?
                    ''', (compra, venta, spread, fecha_actual, moneda, codigo, entidad))
                    self.conn.commit()
                    self.items_actualizados += 1
                except sqlite3.Error as e:
                    self.items_no_guardados += 1
                    print(f"Error al actualizar la cotización para {moneda} ({codigo}) de la entidad {entidad}. No se actualiza.")
                    print(str(e))
            else:
                try:
                    cursor.execute('''
                        INSERT INTO cotizaciones (entidad, moneda, codigo, compra, venta, spread, fecha_actualizacion)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (entidad, moneda, codigo, compra, venta, spread, fecha_actual))
                    self.conn.commit()
                    self.items_actualizados += 1
                except sqlite3.IntegrityError:
                    self.items_no_guardados += 1
                    print(f"Error al guardar la cotización para {moneda} ({codigo}) de la entidad {entidad}. No se guarda.")

