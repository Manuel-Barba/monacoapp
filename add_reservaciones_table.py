from app import app, db, Reservacion
from datetime import datetime, time

def add_reservaciones_table():
    with app.app_context():
        # Crear la tabla de reservaciones
        db.create_all()
        
        # Verificar si ya existen reservaciones
        if Reservacion.query.first() is None:
            # Crear algunas reservaciones de ejemplo
            reservaciones_ejemplo = [
                Reservacion(
                    mesa_id=1,
                    hora_reservacion=time(19, 0),  # 7:00 PM
                    area='Interior',
                    cantidad_personas=4,
                    nombre_reservador='Juan Pérez',
                    fecha_reservacion=datetime.now().date()
                ),
                Reservacion(
                    mesa_id=17,
                    hora_reservacion=time(20, 30),  # 8:30 PM
                    area='jardin',
                    cantidad_personas=6,
                    nombre_reservador='María García',
                    fecha_reservacion=datetime.now().date()
                ),
                Reservacion(
                    mesa_id=41,
                    hora_reservacion=time(18, 0),  # 6:00 PM
                    area='reservados',
                    cantidad_personas=8,
                    nombre_reservador='Carlos López',
                    fecha_reservacion=datetime.now().date()
                )
            ]
            
            for reservacion in reservaciones_ejemplo:
                db.session.add(reservacion)
            
            # Marcar las mesas reservadas como reservadas
            from app import Mesa
            mesa1 = Mesa.query.filter_by(numero=1).first()
            mesa17 = Mesa.query.filter_by(numero=17).first()
            mesa41 = Mesa.query.filter_by(numero=41).first()
            
            if mesa1:
                mesa1.estado = 'reservada'
                mesa1.fecha = datetime.now().date()
            if mesa17:
                mesa17.estado = 'reservada'
                mesa17.fecha = datetime.now().date()
            if mesa41:
                mesa41.estado = 'reservada'
                mesa41.fecha = datetime.now().date()
            
            db.session.commit()
            print("Tabla de reservaciones creada con datos de ejemplo")
        else:
            print("La tabla de reservaciones ya contiene datos")

if __name__ == '__main__':
    add_reservaciones_table() 