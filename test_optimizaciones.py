#!/usr/bin/env python3
"""
Script de prueba para verificar las optimizaciones de carga de mesas
"""

import time
import requests
import json
from datetime import datetime

def test_api_mesas():
    """Prueba la API optimizada de mesas"""
    print("🧪 Probando API optimizada de mesas...")
    
    # Medir tiempo de respuesta
    start_time = time.time()
    
    try:
        response = requests.get('http://localhost:5000/api/mesas')
        end_time = time.time()
        
        if response.status_code == 200:
            mesas = response.json()
            tiempo_respuesta = (end_time - start_time) * 1000  # Convertir a ms
            
            print(f"✅ API /api/mesas:")
            print(f"   - Tiempo de respuesta: {tiempo_respuesta:.2f}ms")
            print(f"   - Total de mesas: {len(mesas)}")
            print(f"   - Tamaño de respuesta: {len(response.content)} bytes")
            
            # Verificar estructura de datos
            if mesas and len(mesas) > 0:
                mesa_ejemplo = mesas[0]
                campos_requeridos = ['id', 'numero', 'capacidad', 'estado', 'ubicacion', 'posicion_x', 'posicion_y']
                campos_presentes = all(campo in mesa_ejemplo for campo in campos_requeridos)
                
                if campos_presentes:
                    print(f"   - Estructura de datos: ✅ Correcta")
                else:
                    print(f"   - Estructura de datos: ❌ Faltan campos")
            
            return True, tiempo_respuesta
            
        else:
            print(f"❌ Error en API: {response.status_code}")
            return False, 0
            
    except Exception as e:
        print(f"❌ Error al conectar con API: {e}")
        return False, 0

def test_api_mesas_por_area():
    """Prueba la API optimizada de mesas por área"""
    print("\n🧪 Probando API optimizada de mesas por área...")
    
    areas = ['interior', 'jardin', 'reservados']
    resultados = {}
    
    for area in areas:
        start_time = time.time()
        
        try:
            response = requests.get(f'http://localhost:5000/api/mesas/area/{area}')
            end_time = time.time()
            
            if response.status_code == 200:
                mesas = response.json()
                tiempo_respuesta = (end_time - start_time) * 1000
                
                print(f"✅ Área {area}:")
                print(f"   - Tiempo: {tiempo_respuesta:.2f}ms")
                print(f"   - Mesas: {len(mesas)}")
                print(f"   - Tamaño: {len(response.content)} bytes")
                
                resultados[area] = {
                    'tiempo': tiempo_respuesta,
                    'mesas': len(mesas),
                    'tamaño': len(response.content)
                }
            else:
                print(f"❌ Error en área {area}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error en área {area}: {e}")
    
    return resultados

def test_configuracion_estatica():
    """Prueba la configuración estática de mesas"""
    print("\n🧪 Probando configuración estática...")
    
    try:
        from mesas_config import get_mesas_config, get_total_mesas, get_layout_config
        
        # Obtener configuración
        config = get_mesas_config()
        total_mesas = get_total_mesas()
        layout_config = get_layout_config()
        
        print(f"✅ Configuración estática:")
        print(f"   - Total de mesas configuradas: {total_mesas}")
        print(f"   - Áreas disponibles: {list(config.keys())}")
        
        for area, mesas in config.items():
            print(f"   - {area.capitalize()}: {len(mesas)} mesas")
        
        print(f"   - Configuración de layout: {list(layout_config.keys())}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error al importar configuración: {e}")
        return False
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def test_rendimiento_comparativo():
    """Prueba de rendimiento comparativo"""
    print("\n🧪 Prueba de rendimiento comparativo...")
    
    # Realizar múltiples consultas para medir consistencia
    tiempos = []
    
    for i in range(5):
        start_time = time.time()
        try:
            response = requests.get('http://localhost:5000/api/mesas')
            if response.status_code == 200:
                end_time = time.time()
                tiempo = (end_time - start_time) * 1000
                tiempos.append(tiempo)
                print(f"   Consulta {i+1}: {tiempo:.2f}ms")
        except:
            pass
    
    if tiempos:
        tiempo_promedio = sum(tiempos) / len(tiempos)
        tiempo_min = min(tiempos)
        tiempo_max = max(tiempos)
        
        print(f"\n📊 Estadísticas de rendimiento:")
        print(f"   - Promedio: {tiempo_promedio:.2f}ms")
        print(f"   - Mínimo: {tiempo_min:.2f}ms")
        print(f"   - Máximo: {tiempo_max:.2f}ms")
        print(f"   - Variabilidad: {((tiempo_max - tiempo_min) / tiempo_promedio * 100):.1f}%")
        
        # Evaluar rendimiento
        if tiempo_promedio < 1000:  # Menos de 1 segundo
            print(f"   - Rendimiento: ✅ Excelente")
        elif tiempo_promedio < 2000:  # Menos de 2 segundos
            print(f"   - Rendimiento: ✅ Bueno")
        else:
            print(f"   - Rendimiento: ⚠️ Necesita optimización")

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas de optimizaciones de mesas")
    print("=" * 50)
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get('http://localhost:5000/')
        if response.status_code != 200:
            print("❌ El servidor no está respondiendo correctamente")
            return
    except:
        print("❌ No se puede conectar al servidor. Asegúrate de que esté corriendo en localhost:5000")
        return
    
    # Ejecutar pruebas
    test_configuracion_estatica()
    test_api_mesas()
    test_api_mesas_por_area()
    test_rendimiento_comparativo()
    
    print("\n" + "=" * 50)
    print("✅ Pruebas completadas")
    print("\n💡 Para ver las optimizaciones en acción:")
    print("   1. Abre http://localhost:5000 en tu navegador")
    print("   2. Abre las herramientas de desarrollador (F12)")
    print("   3. Ve a la pestaña Console")
    print("   4. Observa los logs de tiempo de carga")

if __name__ == "__main__":
    main() 