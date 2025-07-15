#!/usr/bin/env python3
"""
Script de prueba para verificar la zona horaria del restaurante
"""

import pytz
from datetime import datetime

# Configurar zona horaria del restaurante (GMT-7)
RESTAURANT_TIMEZONE = pytz.timezone('America/Phoenix')  # GMT-7 (sin horario de verano)

def get_restaurant_now():
    """Obtiene la fecha y hora actual en la zona horaria del restaurante"""
    return datetime.now(RESTAURANT_TIMEZONE)

if __name__ == "__main__":
    print("=== PRUEBA DE ZONA HORARIA ===")
    print(f"Zona horaria configurada: {RESTAURANT_TIMEZONE}")
    
    # Fecha y hora actual en UTC
    utc_now = datetime.utcnow()
    print(f"Fecha/hora UTC: {utc_now}")
    
    # Fecha y hora actual en la zona horaria del restaurante
    restaurant_now = get_restaurant_now()
    print(f"Fecha/hora restaurante: {restaurant_now}")
    
    # Fecha actual del restaurante
    restaurant_date = restaurant_now.date()
    print(f"Fecha actual restaurante: {restaurant_date}")
    
    # Verificar offset
    offset = restaurant_now.utcoffset()
    print(f"Offset de zona horaria: {offset}")
    
    print("\n=== COMPARACIÓN ===")
    print(f"¿Es la misma fecha que UTC? {utc_now.date() == restaurant_date}")
    print(f"Diferencia en horas: {offset.total_seconds() / 3600}")
    
    print("\n=== INFORMACIÓN ADICIONAL ===")
    print(f"Nombre de la zona: {RESTAURANT_TIMEZONE.zone}")
    print(f"¿Tiene horario de verano? {restaurant_now.dst() != None}") 