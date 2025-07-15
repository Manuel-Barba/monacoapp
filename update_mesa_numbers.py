#!/usr/bin/env python3
"""
Script para actualizar los números de las mesas en la base de datos
"""

import sqlite3
import os

def update_mesa_numbers():
    """Actualiza los números de las mesas en la base de datos"""
    
    # Mapeo de números antiguos a nuevos para interior
    mesa_mapping = {
        1: 101, 2: 102, 3: 103, 4: 104, 5: 105,
        6: 106, 7: 107, 8: 108, 9: 109,
        10: 201, 11: 202, 12: 203,
        13: 204, 14: 205, 15: 206
    }
    
    # Conectar a la base de datos
    db_path = os.path.join('instance', 'restaurant.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("Actualizando números de mesas en la base de datos...")
        
        # Actualizar cada mesa
        for old_num, new_num in mesa_mapping.items():
            cursor.execute("""
                UPDATE mesa 
                SET numero = ? 
                WHERE numero = ? AND ubicacion = 'interior'
            """, (new_num, old_num))
            
            if cursor.rowcount > 0:
                print(f"Mesa {old_num} → Mesa {new_num} (actualizada)")
            else:
                print(f"Mesa {old_num} → Mesa {new_num} (no encontrada)")
        
        # Confirmar cambios
        conn.commit()
        print(f"\n✅ Se actualizaron {len(mesa_mapping)} mesas del interior")
        
        # Mostrar resumen de mesas actualizadas
        cursor.execute("""
            SELECT numero, capacidad, ubicacion, estado 
            FROM mesa 
            WHERE ubicacion = 'interior' 
            ORDER BY numero
        """)
        
        mesas = cursor.fetchall()
        print("\n📋 Resumen de mesas del interior:")
        for mesa in mesas:
            print(f"  Mesa {mesa[0]} - Capacidad: {mesa[1]} - Estado: {mesa[3]}")
            
    except Exception as e:
        print(f"❌ Error al actualizar las mesas: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    update_mesa_numbers() 