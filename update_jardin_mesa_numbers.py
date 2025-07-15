#!/usr/bin/env python3
"""
Script para actualizar los números de las mesas del jardín en la base de datos
"""

import sqlite3
import os

def update_jardin_mesa_numbers():
    """Actualiza los números de las mesas del jardín en la base de datos"""
    
    # Mapeo de números antiguos a nuevos para jardín
    mesa_mapping = {
        16: 301, 17: 302, 18: 303,
        19: 304, 20: 305, 21: 306
    }
    
    # Conectar a la base de datos
    db_path = os.path.join('instance', 'restaurant.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("Actualizando números de mesas del jardín en la base de datos...")
        
        # Primero, eliminar las mesas que ya no existen (22-27)
        mesas_a_eliminar = [22, 23, 24, 25, 26, 27]
        for numero in mesas_a_eliminar:
            cursor.execute("""
                DELETE FROM mesa 
                WHERE numero = ? AND ubicacion = 'jardin'
            """, (numero,))
            
            if cursor.rowcount > 0:
                print(f"Mesa {numero} eliminada")
            else:
                print(f"Mesa {numero} no encontrada para eliminar")
        
        # Actualizar cada mesa con el nuevo número
        for old_num, new_num in mesa_mapping.items():
            cursor.execute("""
                UPDATE mesa 
                SET numero = ? 
                WHERE numero = ? AND ubicacion = 'jardin'
            """, (new_num, old_num))
            
            if cursor.rowcount > 0:
                print(f"Mesa {old_num} → Mesa {new_num} (actualizada)")
            else:
                print(f"Mesa {old_num} → Mesa {new_num} (no encontrada)")
        
        # Confirmar cambios
        conn.commit()
        print(f"\n✅ Se actualizaron {len(mesa_mapping)} mesas del jardín")
        
        # Mostrar resumen de mesas actualizadas
        cursor.execute("""
            SELECT numero, capacidad, ubicacion, estado 
            FROM mesa 
            WHERE ubicacion = 'jardin' 
            ORDER BY numero
        """)
        
        mesas = cursor.fetchall()
        print("\n📋 Resumen de mesas del jardín:")
        for mesa in mesas:
            print(f"  Mesa {mesa[0]} - Capacidad: {mesa[1]} - Estado: {mesa[3]}")
            
    except Exception as e:
        print(f"❌ Error al actualizar las mesas: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    update_jardin_mesa_numbers() 