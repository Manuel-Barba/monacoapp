import sqlite3
import os

def add_new_columns():
    db_path = 'instance/restaurant.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada en {db_path}")
        return
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Añadiendo nuevas columnas a la base de datos...")
        
        # Añadir columna telefono a la tabla reservacion
        try:
            cursor.execute("ALTER TABLE reservacion ADD COLUMN telefono VARCHAR(20)")
            print("✓ Columna 'telefono' añadida a la tabla reservacion")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("ℹ️ Columna 'telefono' ya existe en la tabla reservacion")
            else:
                print(f"⚠️ Error al añadir columna telefono: {e}")
        
        # Añadir columna nota a la tabla reservacion
        try:
            cursor.execute("ALTER TABLE reservacion ADD COLUMN nota TEXT")
            print("✓ Columna 'nota' añadida a la tabla reservacion")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("ℹ️ Columna 'nota' ya existe en la tabla reservacion")
            else:
                print(f"⚠️ Error al añadir columna nota: {e}")
        
        # Añadir columna telefono a la tabla historial_reservacion
        try:
            cursor.execute("ALTER TABLE historial_reservacion ADD COLUMN telefono VARCHAR(20)")
            print("✓ Columna 'telefono' añadida a la tabla historial_reservacion")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("ℹ️ Columna 'telefono' ya existe en la tabla historial_reservacion")
            else:
                print(f"⚠️ Error al añadir columna telefono: {e}")
        
        # Añadir columna nota a la tabla historial_reservacion
        try:
            cursor.execute("ALTER TABLE historial_reservacion ADD COLUMN nota TEXT")
            print("✓ Columna 'nota' añadida a la tabla historial_reservacion")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("ℹ️ Columna 'nota' ya existe en la tabla historial_reservacion")
            else:
                print(f"⚠️ Error al añadir columna nota: {e}")
        
        # Confirmar cambios
        conn.commit()
        print("\n✅ Base de datos actualizada exitosamente!")
        
        # Mostrar estructura actualizada
        print("\n📋 Estructura actualizada de las tablas:")
        
        cursor.execute("PRAGMA table_info(reservacion)")
        columns = cursor.fetchall()
        print("\nTabla 'reservacion':")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        cursor.execute("PRAGMA table_info(historial_reservacion)")
        columns = cursor.fetchall()
        print("\nTabla 'historial_reservacion':")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
    except Exception as e:
        print(f"❌ Error al actualizar la base de datos: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_new_columns() 