#!/usr/bin/env python3
"""
Script para probar la funcionalidad de actualización automática de mesas reservadas
"""

from app import app, db, Mesa, Reservacion
from datetime import datetime
import pytz

# Configurar zona horaria del restaurante
RESTAURANT_TIMEZONE = pytz.timezone('America/Phoenix')

def get_restaurant_now():
    return datetime.now(RESTAURANT_TIMEZONE)

def actualizar_mesas_reservadas():
    """Función para actualizar automáticamente el estado de las mesas cuando llega el día de la reservación"""
    try:
        fecha_actual = get_restaurant_now().date()
        
        # Buscar reservaciones para hoy que tengan mesas en estado disponible
        reservaciones_hoy = Reservacion.query.filter(
            Reservacion.fecha_reservacion == fecha_actual
        ).all()
        
        actualizadas = 0
        for reservacion in reservaciones_hoy:
            mesa = Mesa.query.get(reservacion.mesa_id)
            if mesa and mesa.estado == 'disponible':
                # Cambiar el estado de la mesa a reservada
                mesa.estado = 'reservada'
                mesa.fecha = fecha_actual
                actualizadas += 1
                print(f"  ✓ Mesa {mesa.numero} actualizada a reservada")
        
        if actualizadas > 0:
            db.session.commit()
            return {
                'mensaje': f'Se actualizaron {actualizadas} mesas a estado reservado',
                'actualizadas': actualizadas
            }
        
        return None  # No devolver mensaje si no hay cambios
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Error al actualizar mesas reservadas: {str(e)}'}

def mostrar_estado_mesas():
    """Muestra el estado actual de las mesas"""
    print("\n📊 ESTADO ACTUAL DE LAS MESAS:")
    print("=" * 50)
    
    # Mostrar todas las mesas con sus estados
    mesas = Mesa.query.all()
    for mesa in mesas:
        # Buscar reservación para esta mesa
        reservacion = Reservacion.query.filter_by(mesa_id=mesa.id).first()
        
        if reservacion:
            print(f"Mesa {mesa.numero}: {mesa.estado} - Fecha mesa: {mesa.fecha} - RSV: {reservacion.fecha_reservacion} {reservacion.hora_reservacion} - {reservacion.nombre_reservador}")
        else:
            print(f"Mesa {mesa.numero}: {mesa.estado} - Fecha mesa: {mesa.fecha} - Sin reservación")

if __name__ == "__main__":
    with app.app_context():
        print("🧪 PRUEBA DE ACTUALIZACIÓN AUTOMÁTICA DE MESAS")
        print("=" * 60)
        
        fecha_actual = get_restaurant_now().date()
        print(f"Fecha actual: {fecha_actual}")
        
        # Mostrar estado inicial
        mostrar_estado_mesas()
        
        # Ejecutar actualización
        print(f"\n🔄 Ejecutando actualización automática...")
        resultado = actualizar_mesas_reservadas()
        
        if resultado:
            print(f"✅ {resultado['mensaje']}")
        else:
            print("ℹ️ No hay mesas que actualizar")
        
        # Mostrar estado final
        mostrar_estado_mesas() 