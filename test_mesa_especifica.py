#!/usr/bin/env python3
"""
Script de prueba para verificar la optimización de actualización de mesa específica
"""

import time
import requests
import json

def test_api_mesa_especifica():
    """Prueba la API optimizada de mesa específica"""
    print("🧪 Probando API optimizada de mesa específica...")
    
    # Probar con diferentes IDs de mesa
    mesa_ids = [1, 16, 28]  # Una mesa de cada área
    
    for mesa_id in mesa_ids:
        start_time = time.time()
        
        try:
            response = requests.get(f'http://localhost:5000/api/mesas/especifica/{mesa_id}')
            end_time = time.time()
            
            if response.status_code == 200:
                mesa = response.json()
                tiempo_respuesta = (end_time - start_time) * 1000
                
                print(f"✅ Mesa {mesa_id}:")
                print(f"   - Tiempo: {tiempo_respuesta:.2f}ms")
                print(f"   - Número: {mesa['numero']}")
                print(f"   - Estado: {mesa['estado']}")
                print(f"   - Ubicación: {mesa['ubicacion']}")
                print(f"   - Capacidad: {mesa['capacidad']}")
                print(f"   - Tamaño: {len(response.content)} bytes")
                
            else:
                print(f"❌ Error en mesa {mesa_id}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error en mesa {mesa_id}: {e}")

def test_comparacion_rendimiento():
    """Compara el rendimiento entre actualizar toda el área vs mesa específica"""
    print("\n🧪 Comparando rendimiento: Área completa vs Mesa específica...")
    
    # Mesa de prueba (interior)
    mesa_id = 1
    area = 'interior'
    
    # Test 1: Obtener toda el área
    print("📊 Test 1: Obtener toda el área interior")
    tiempos_area = []
    for i in range(5):
        start_time = time.time()
        try:
            response = requests.get(f'http://localhost:5000/api/mesas/area/{area}')
            if response.status_code == 200:
                end_time = time.time()
                tiempo = (end_time - start_time) * 1000
                tiempos_area.append(tiempo)
                print(f"   Consulta {i+1}: {tiempo:.2f}ms")
        except:
            pass
    
    # Test 2: Obtener mesa específica
    print("\n📊 Test 2: Obtener mesa específica")
    tiempos_mesa = []
    for i in range(5):
        start_time = time.time()
        try:
            response = requests.get(f'http://localhost:5000/api/mesas/especifica/{mesa_id}')
            if response.status_code == 200:
                end_time = time.time()
                tiempo = (end_time - start_time) * 1000
                tiempos_mesa.append(tiempo)
                print(f"   Consulta {i+1}: {tiempo:.2f}ms")
        except:
            pass
    
    # Comparar resultados
    if tiempos_area and tiempos_mesa:
        promedio_area = sum(tiempos_area) / len(tiempos_area)
        promedio_mesa = sum(tiempos_mesa) / len(tiempos_mesa)
        
        print(f"\n📈 Comparación de rendimiento:")
        print(f"   - Área completa (15 mesas): {promedio_area:.2f}ms promedio")
        print(f"   - Mesa específica (1 mesa): {promedio_mesa:.2f}ms promedio")
        
        if promedio_mesa < promedio_area:
            mejora = ((promedio_area - promedio_mesa) / promedio_area) * 100
            print(f"   - Mejora: {mejora:.1f}% más rápido")
            print(f"   - Eficiencia: ✅ Excelente")
        else:
            print(f"   - Eficiencia: ⚠️ Revisar optimización")

def test_actualizacion_mesa():
    """Prueba la actualización de estado de una mesa"""
    print("\n🧪 Probando actualización de estado de mesa...")
    
    mesa_id = 2  # Mesa de prueba
    
    # Obtener estado inicial
    try:
        response = requests.get(f'http://localhost:5000/api/mesas/especifica/{mesa_id}')
        if response.status_code == 200:
            mesa_inicial = response.json()
            estado_inicial = mesa_inicial['estado']
            print(f"✅ Estado inicial de mesa {mesa_id}: {estado_inicial}")
            
            # Cambiar estado (ocupar)
            print(f"🔄 Cambiando estado a 'ocupada'...")
            response_update = requests.put(f'http://localhost:5000/api/mesas/{mesa_id}', 
                json={'estado': 'ocupada', 'fecha': '2025-07-07'})
            
            if response_update.status_code == 200:
                # Verificar cambio
                response_final = requests.get(f'http://localhost:5000/api/mesas/especifica/{mesa_id}')
                if response_final.status_code == 200:
                    mesa_final = response_final.json()
                    print(f"✅ Estado final de mesa {mesa_id}: {mesa_final['estado']}")
                    
                    if mesa_final['estado'] == 'ocupada':
                        print(f"✅ Actualización exitosa")
                    else:
                        print(f"❌ Error en actualización")
                else:
                    print(f"❌ Error al verificar estado final")
            else:
                print(f"❌ Error al actualizar mesa: {response_update.status_code}")
        else:
            print(f"❌ Error al obtener mesa inicial: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error en prueba de actualización: {e}")

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas de optimización de mesa específica")
    print("=" * 60)
    
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
    test_api_mesa_especifica()
    test_comparacion_rendimiento()
    test_actualizacion_mesa()
    
    print("\n" + "=" * 60)
    print("✅ Pruebas completadas")
    print("\n💡 Beneficios de la optimización:")
    print("   - Actualización más rápida (solo 1 mesa vs área completa)")
    print("   - Menos tráfico de red")
    print("   - Mejor experiencia de usuario")
    print("   - Menor carga en el servidor")

if __name__ == "__main__":
    main() 