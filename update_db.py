#!/usr/bin/env python3
"""
Script para actualizar la base de datos con la nueva configuración de mesas
"""

from app import app, db, Mesa, Reservacion, HistorialReservacion
from mesas_config import get_mesas_config
from datetime import datetime, time
from sqlalchemy import text

def update_database():
    """Actualiza la base de datos con la nueva configuración de mesas"""
    with app.app_context():
        print("🔄 Actualizando base de datos con nueva configuración...")
        
        # Obtener la nueva configuración de mesas
        mesas_config = get_mesas_config()
        
        # Eliminar todas las mesas existentes
        print("🗑️ Eliminando mesas existentes...")
        Mesa.query.delete()
        
        # Eliminar todas las reservaciones existentes
        print("🗑️ Eliminando reservaciones existentes...")
        Reservacion.query.delete()
        
        # Crear las nuevas mesas según la configuración
        print("➕ Creando nuevas mesas...")
        for area, mesas_area in mesas_config.items():
            print(f"   - Área {area}: {len(mesas_area)} mesas")
            for mesa_config in mesas_area:
                mesa = Mesa(
                    numero=mesa_config['numero'],
                    capacidad=mesa_config['capacidad'],
                    ubicacion=area,
                    posicion_x=mesa_config['posicion_x'],
                    posicion_y=mesa_config['posicion_y'],
                    estado='disponible'
                )
                db.session.add(mesa)
        
        # Crear algunas reservaciones de ejemplo con las nuevas mesas
        print("📅 Creando reservaciones de ejemplo...")
        reservaciones_ejemplo = [
            Reservacion(
                mesa_id=1,  # Mesa 1 del interior
                hora_reservacion=time(19, 0),  # 7:00 PM
                area='interior',
                cantidad_personas=4,
                nombre_reservador='Juan Pérez',
                fecha_reservacion=datetime.now().date()
            ),
            Reservacion(
                mesa_id=16,  # Mesa 16 del jardín
                hora_reservacion=time(20, 30),  # 8:30 PM
                area='jardin',
                cantidad_personas=6,
                nombre_reservador='María García',
                fecha_reservacion=datetime.now().date()
            ),
            Reservacion(
                mesa_id=28,  # Mesa 28 de reservados
                hora_reservacion=time(18, 0),  # 6:00 PM
                area='reservados',
                cantidad_personas=20,
                nombre_reservador='Carlos López',
                fecha_reservacion=datetime.now().date()
            )
        ]
        
        for reservacion in reservaciones_ejemplo:
            db.session.add(reservacion)
        
        # Marcar las mesas reservadas como reservadas
        print("🏷️ Marcando mesas reservadas...")
        mesa1 = Mesa.query.filter_by(numero=1).first()
        mesa16 = Mesa.query.filter_by(numero=16).first()
        mesa28 = Mesa.query.filter_by(numero=28).first()
        
        if mesa1:
            mesa1.estado = 'reservada'
            mesa1.fecha = datetime.now().date()
        if mesa16:
            mesa16.estado = 'reservada'
            mesa16.fecha = datetime.now().date()
        if mesa28:
            mesa28.estado = 'reservada'
            mesa28.fecha = datetime.now().date()
        
        # Commit de todos los cambios
        db.session.commit()
        
        # Verificar la actualización
        total_mesas = Mesa.query.count()
        total_reservaciones = Reservacion.query.count()
        
        print("✅ Base de datos actualizada exitosamente!")
        print(f"📊 Estadísticas:")
        print(f"   - Total de mesas: {total_mesas}")
        print(f"   - Total de reservaciones: {total_reservaciones}")
        
        # Mostrar resumen por área
        for area in ['interior', 'jardin', 'reservados']:
            mesas_area = Mesa.query.filter_by(ubicacion=area).count()
            print(f"   - {area.capitalize()}: {mesas_area} mesas")

def verify_database():
    """Verifica que la base de datos esté correctamente configurada"""
    with app.app_context():
        print("\n🔍 Verificando configuración de la base de datos...")
        
        # Verificar que todas las mesas de la configuración existan en la BD
        mesas_config = get_mesas_config()
        errores = []
        
        for area, mesas_area in mesas_config.items():
            for mesa_config in mesas_area:
                mesa_db = Mesa.query.filter_by(numero=mesa_config['numero']).first()
                if not mesa_db:
                    errores.append(f"Mesa {mesa_config['numero']} no existe en la BD")
                elif mesa_db.ubicacion != area:
                    errores.append(f"Mesa {mesa_config['numero']} tiene ubicación incorrecta")
                elif mesa_db.capacidad != mesa_config['capacidad']:
                    errores.append(f"Mesa {mesa_config['numero']} tiene capacidad incorrecta")
        
        if errores:
            print("❌ Errores encontrados:")
            for error in errores:
                print(f"   - {error}")
            return False
        else:
            print("✅ Configuración verificada correctamente")
            return True

def crear_tabla_historial():
    """Crea la tabla de historial de reservaciones si no existe"""
    with app.app_context():
        # Crear la tabla de historial
        db.create_all()
        print("✅ Tabla de historial de reservaciones creada/verificada exitosamente")

def actualizar_base_datos():
    with app.app_context():
        try:
            # Añadir columna telefono a la tabla reservacion
            db.session.execute(text("""
                ALTER TABLE reservacion 
                ADD COLUMN telefono VARCHAR(20)
            """))
            print("✓ Columna 'telefono' añadida a la tabla reservacion")
            
            # Añadir columna nota a la tabla reservacion
            db.session.execute(text("""
                ALTER TABLE reservacion 
                ADD COLUMN nota TEXT
            """))
            print("✓ Columna 'nota' añadida a la tabla reservacion")
            
            # Añadir columna telefono a la tabla historial_reservacion
            db.session.execute(text("""
                ALTER TABLE historial_reservacion 
                ADD COLUMN telefono VARCHAR(20)
            """))
            print("✓ Columna 'telefono' añadida a la tabla historial_reservacion")
            
            # Añadir columna nota a la tabla historial_reservacion
            db.session.execute(text("""
                ALTER TABLE historial_reservacion 
                ADD COLUMN nota TEXT
            """))
            print("✓ Columna 'nota' añadida a la tabla historial_reservacion")
            
            db.session.commit()
            print("\n✅ Base de datos actualizada exitosamente!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al actualizar la base de datos: {e}")
            print("Es posible que las columnas ya existan.")

if __name__ == '__main__':
    print("🚀 Iniciando actualización de base de datos...")
    print("=" * 50)
    
    try:
        update_database()
        verify_database()
        crear_tabla_historial()
        actualizar_base_datos()
        
        print("\n" + "=" * 50)
        print("✅ Proceso completado exitosamente!")
        print("\n💡 Ahora puedes reiniciar el servidor y los errores 404 deberían desaparecer.")
        
    except Exception as e:
        print(f"❌ Error durante la actualización: {e}")
        db.session.rollback() 