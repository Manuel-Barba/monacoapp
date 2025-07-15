#!/usr/bin/env python3
"""
Script para limpiar reservaciones pasadas y moverlas al historial automáticamente.
Este script libera las mesas que tienen reservaciones de días anteriores y mueve
las reservaciones al historial para mantener el registro.
"""

import sqlite3
from datetime import datetime, timedelta
import pytz

# Configurar zona horaria del restaurante
RESTAURANT_TIMEZONE = pytz.timezone('America/Phoenix')

def get_restaurant_now():
    """Obtiene la fecha y hora actual en la zona horaria del restaurante"""
    return datetime.now(RESTAURANT_TIMEZONE)

def clean_past_reservations():
    """Limpia reservaciones pasadas y las mueve al historial"""
    conn = sqlite3.connect('instance/restaurant.db')
    cursor = conn.cursor()
    
    try:
        # Obtener fecha actual en zona horaria del restaurante
        fecha_actual = get_restaurant_now().date()
        print(f"Fecha actual del restaurante: {fecha_actual}")
        
        # Buscar reservaciones de días pasados
        cursor.execute("""
            SELECT r.id, r.mesa_id, r.hora_reservacion, r.area, r.cantidad_personas, 
                   r.nombre_reservador, r.fecha_reservacion, r.fecha_creacion, m.numero
            FROM reservacion r
            JOIN mesa m ON r.mesa_id = m.id
            WHERE r.fecha_reservacion < ?
            ORDER BY r.fecha_reservacion DESC
        """, (fecha_actual,))
        
        reservaciones_pasadas = cursor.fetchall()
        
        if not reservaciones_pasadas:
            print("No hay reservaciones pasadas para limpiar.")
            return
        
        print(f"Encontradas {len(reservaciones_pasadas)} reservaciones pasadas:")
        
        for reservacion in reservaciones_pasadas:
            (reservacion_id, mesa_id, hora_reservacion, area, cantidad_personas,
             nombre_reservador, fecha_reservacion, fecha_creacion, mesa_numero) = reservacion
            
            print(f"  - Mesa {mesa_numero}: {nombre_reservador} - {fecha_reservacion} {hora_reservacion}")
            
            # 1. Crear registro en el historial
            cursor.execute("""
                INSERT INTO historial_reservacion 
                (reservacion_id_original, mesa_id, mesa_numero, hora_reservacion, area, 
                 cantidad_personas, nombre_reservador, fecha_reservacion, fecha_creacion_original, 
                 fecha_liberacion, motivo_liberacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                reservacion_id, mesa_id, mesa_numero, hora_reservacion, area,
                cantidad_personas, nombre_reservador, fecha_reservacion, fecha_creacion,
                datetime.utcnow(), 'Liberación automática por fecha pasada'
            ))
            
            # 2. Liberar la mesa (cambiar estado a disponible y limpiar fecha)
            cursor.execute("""
                UPDATE mesa 
                SET estado = 'disponible', fecha = NULL 
                WHERE id = ?
            """, (mesa_id,))
            
            # 3. Eliminar la reservación original
            cursor.execute("DELETE FROM reservacion WHERE id = ?", (reservacion_id,))
            
            print(f"    ✓ Liberada mesa {mesa_numero} y movida al historial")
        
        # Confirmar cambios
        conn.commit()
        print(f"\n✅ Se liberaron {len(reservaciones_pasadas)} mesas automáticamente.")
        print("📋 Las reservaciones pasadas se movieron al historial para mantener el registro.")
        
    except Exception as e:
        print(f"❌ Error al limpiar reservaciones: {e}")
        conn.rollback()
    finally:
        conn.close()

def show_current_status():
    """Muestra el estado actual de las mesas y reservaciones"""
    conn = sqlite3.connect('instance/restaurant.db')
    cursor = conn.cursor()
    
    try:
        fecha_actual = get_restaurant_now().date()
        print(f"\n📊 ESTADO ACTUAL (Fecha: {fecha_actual}):")
        print("=" * 50)
        
        # Mesas con reservaciones activas
        cursor.execute("""
            SELECT m.numero, m.estado, m.fecha, r.nombre_reservador, r.hora_reservacion
            FROM mesa m
            LEFT JOIN reservacion r ON m.id = r.mesa_id AND r.fecha_reservacion = m.fecha
            WHERE m.fecha IS NOT NULL
            ORDER BY m.fecha DESC, m.numero
        """)
        
        mesas_con_fecha = cursor.fetchall()
        if mesas_con_fecha:
            print("\n🪑 MESAS CON FECHAS:")
            for mesa in mesas_con_fecha:
                numero, estado, fecha, nombre, hora = mesa
                status_icon = "🔴" if estado == "ocupada" else "🟡"
                print(f"  {status_icon} Mesa {numero}: {estado} - {fecha} {hora or ''} - {nombre or 'Sin reservación'}")
        else:
            print("\n✅ No hay mesas con fechas asignadas")
        
        # Reservaciones activas
        cursor.execute("""
            SELECT COUNT(*) FROM reservacion WHERE fecha_reservacion >= ?
        """, (fecha_actual,))
        
        reservaciones_activas = cursor.fetchone()[0]
        print(f"\n📅 RESERVACIONES ACTIVAS: {reservaciones_activas}")
        
        # Historial de reservaciones
        cursor.execute("SELECT COUNT(*) FROM historial_reservacion")
        historial_count = cursor.fetchone()[0]
        print(f"📋 HISTORIAL DE RESERVACIONES: {historial_count}")
        
    except Exception as e:
        print(f"❌ Error al mostrar estado: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("🧹 LIMPIADOR DE RESERVACIONES PASADAS")
    print("=" * 40)
    
    show_current_status()
    
    print("\n" + "=" * 40)
    clean_past_reservations()
    
    print("\n" + "=" * 40)
    show_current_status() 