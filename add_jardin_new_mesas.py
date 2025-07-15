#!/usr/bin/env python3
"""
Script para agregar las nuevas mesas del jardín (401-406) a la base de datos
"""

import sqlite3
import os

def add_jardin_new_mesas():
    """Agrega las nuevas mesas del jardín a la base de datos"""
    
    # Conectar a la base de datos
    db_path = os.path.join('instance', 'restaurant.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("Agregando nuevas mesas del jardín a la base de datos...")
        
        # Nuevas mesas del jardín con posiciones
        nuevas_mesas = [
            (401, 0, 'disponible', 'jardin', 3, 1),
            (402, 0, 'disponible', 'jardin', 3, 2),
            (403, 0, 'disponible', 'jardin', 3, 3),
            (404, 0, 'disponible', 'jardin', 4, 1),
            (405, 0, 'disponible', 'jardin', 4, 2),
            (406, 0, 'disponible', 'jardin', 4, 3)
        ]
        
        # Insertar las nuevas mesas
        for numero, capacidad, estado, ubicacion, pos_x, pos_y in nuevas_mesas:
            cursor.execute('''
                INSERT INTO mesa (numero, capacidad, estado, ubicacion, posicion_x, posicion_y)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (numero, capacidad, estado, ubicacion, pos_x, pos_y))
            print(f"✅ Mesa {numero} agregada al área {ubicacion} en posición ({pos_x}, {pos_y})")
        
        # Confirmar cambios
        conn.commit()
        print(f"\n🎉 Se agregaron {len(nuevas_mesas)} nuevas mesas al jardín")
        
        # Verificar que se agregaron correctamente
        cursor.execute('SELECT numero, capacidad, ubicacion, posicion_x, posicion_y FROM mesa WHERE ubicacion = "jardin" ORDER BY numero')
        mesas_jardin = cursor.fetchall()
        print(f"\n📋 Mesas actuales en jardín: {mesas_jardin}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_jardin_new_mesas() 