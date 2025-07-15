from app import app, db
from sqlalchemy import text

with app.app_context():
    # Eliminar la tabla de reservaciones si existe
    try:
        db.session.execute(text('DROP TABLE IF EXISTS reservacion'))
        db.session.commit()
        print("Tabla de reservaciones eliminada")
    except Exception as e:
        print(f"Error al eliminar tabla de reservaciones: {e}")
    
    # Resetear todas las mesas a disponible
    from app import Mesa
    mesas = Mesa.query.all()
    for mesa in mesas:
        mesa.estado = 'disponible'
        mesa.fecha = None
        mesa.grupo_id = None
    
    db.session.commit()
    print("Todas las mesas han sido reseteadas a disponible")
    
    print("Base de datos limpiada completamente")

if __name__ == '__main__':
    clean_database() 