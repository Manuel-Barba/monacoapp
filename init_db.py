from app import app, db, Mesa, Reservacion
from mesas_config import get_mesas_config
from datetime import datetime, time

def init_database():
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        
        # Verificar si ya existen mesas
        if Mesa.query.first() is None:
            print("🔄 Inicializando base de datos con nueva configuración...")
            
            # Obtener la configuración de mesas
            mesas_config = get_mesas_config()
            
            # Crear las mesas según la configuración
            print("➕ Creando mesas...")
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
            
            # Crear algunas reservaciones de ejemplo
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
            
            db.session.commit()
            
            # Mostrar estadísticas
            total_mesas = Mesa.query.count()
            total_reservaciones = Reservacion.query.count()
            
            print("✅ Base de datos inicializada exitosamente!")
            print(f"📊 Estadísticas:")
            print(f"   - Total de mesas: {total_mesas}")
            print(f"   - Total de reservaciones: {total_reservaciones}")
            
            # Mostrar resumen por área
            for area in ['interior', 'jardin', 'reservados']:
                mesas_area = Mesa.query.filter_by(ubicacion=area).count()
                print(f"   - {area.capitalize()}: {mesas_area} mesas")
        else:
            print("ℹ️ La base de datos ya contiene datos")

if __name__ == '__main__':
    init_database() 