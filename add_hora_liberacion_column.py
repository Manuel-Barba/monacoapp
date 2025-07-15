#!/usr/bin/env python3
"""
Script para agregar la columna hora_liberacion a la tabla HistorialReservacion
"""

import sqlite3
import os

def add_hora_liberacion_column():
    """Agrega la columna hora_liberacion a la tabla HistorialReservacion"""
    
    # Ruta de la base de datos
    db_path = os.path.join('instance', 'restaurant.db')
    
    if not os.path.exists(db_path):
        print("Error: No se encontró la base de datos en instance/restaurant.db")
        return False
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info(historial_reservacion)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'hora_liberacion' in columns:
            print("La columna hora_liberacion ya existe en la tabla historial_reservacion")
            return True
        
        # Agregar la columna hora_liberacion
        cursor.execute("""
            ALTER TABLE historial_reservacion 
            ADD COLUMN hora_liberacion TIME
        """)
        
        # Confirmar cambios
        conn.commit()
        print("Columna hora_liberacion agregada exitosamente a la tabla historial_reservacion")
        
        # Verificar que la columna se agregó correctamente
        cursor.execute("PRAGMA table_info(historial_reservacion)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'hora_liberacion' in columns:
            print("Verificación exitosa: la columna hora_liberacion está presente")
            return True
        else:
            print("Error: La columna no se agregó correctamente")
            return False
            
    except sqlite3.Error as e:
        print(f"Error de SQLite: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("Agregando columna hora_liberacion a la tabla HistorialReservacion...")
    success = add_hora_liberacion_column()
    
    if success:
        print("✅ Operación completada exitosamente")
    else:
        print("❌ Error en la operación") 