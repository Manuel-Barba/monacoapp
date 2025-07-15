# Configuración estática de todas las mesas del restaurante
# Este archivo define la estructura fija de las mesas para optimizar la carga

MESAS_CONFIG = {
    'interior': [
        # Columna 1: Mesas 101, 102, 103, 104, 105
        {'numero': 101, 'capacidad': 4, 'posicion_x': 1, 'posicion_y': 1},
        {'numero': 102, 'capacidad': 4, 'posicion_x': 1, 'posicion_y': 2},
        {'numero': 103, 'capacidad': 4, 'posicion_x': 1, 'posicion_y': 3},
        {'numero': 104, 'capacidad': 4, 'posicion_x': 1, 'posicion_y': 4},
        {'numero': 105, 'capacidad': 4, 'posicion_x': 1, 'posicion_y': 5},
        # Columna 2: Mesas 106, 107, 108, 109
        {'numero': 106, 'capacidad': 4, 'posicion_x': 2, 'posicion_y': 1},
        {'numero': 107, 'capacidad': 4, 'posicion_x': 2, 'posicion_y': 2},
        {'numero': 108, 'capacidad': 4, 'posicion_x': 2, 'posicion_y': 3},
        {'numero': 109, 'capacidad': 4, 'posicion_x': 2, 'posicion_y': 4},
        # Columna 3: Mesas 201, 202, 203
        {'numero': 201, 'capacidad': 6, 'posicion_x': 3, 'posicion_y': 1},
        {'numero': 202, 'capacidad': 4, 'posicion_x': 3, 'posicion_y': 2},
        {'numero': 203, 'capacidad': 4, 'posicion_x': 3, 'posicion_y': 3},
        # Columna 4: Mesas 204, 205, 206
        {'numero': 204, 'capacidad': 6, 'posicion_x': 4, 'posicion_y': 1},
        {'numero': 205, 'capacidad': 4, 'posicion_x': 4, 'posicion_y': 2},
        {'numero': 206, 'capacidad': 4, 'posicion_x': 4, 'posicion_y': 3}
    ],
    'jardin': [
        # Columna 1: Mesas 301, 302, 303
        {'numero': 301, 'capacidad': 4, 'posicion_x': 1, 'posicion_y': 1},
        {'numero': 302, 'capacidad': 4, 'posicion_x': 1, 'posicion_y': 2},
        {'numero': 303, 'capacidad': 6, 'posicion_x': 1, 'posicion_y': 3},
        # Columna 2: Mesas 304, 305, 306
        {'numero': 304, 'capacidad': 4, 'posicion_x': 2, 'posicion_y': 1},
        {'numero': 305, 'capacidad': 4, 'posicion_x': 2, 'posicion_y': 2},
        {'numero': 306, 'capacidad': 6, 'posicion_x': 2, 'posicion_y': 3},
        # Columna 3: Mesas 401, 402, 403
        {'numero': 401, 'capacidad': 0, 'posicion_x': 3, 'posicion_y': 1},
        {'numero': 402, 'capacidad': 0, 'posicion_x': 3, 'posicion_y': 2},
        {'numero': 403, 'capacidad': 0, 'posicion_x': 3, 'posicion_y': 3},
        # Columna 4: Mesas 404, 405, 406
        {'numero': 404, 'capacidad': 0, 'posicion_x': 4, 'posicion_y': 1},
        {'numero': 405, 'capacidad': 0, 'posicion_x': 4, 'posicion_y': 2},
        {'numero': 406, 'capacidad': 0, 'posicion_x': 4, 'posicion_y': 3}
    ],
    'reservados': [
        {'numero': 28, 'capacidad': 25, 'posicion_x': 1, 'posicion_y': 1}
    ]
}

# Configuración de layout por área
LAYOUT_CONFIG = {
    'interior': {
        'grid_columns': 4,
        'grid_rows': 5,
        'css_class': 'interior-layout'
    },
    'jardin': {
        'grid_columns': 4,
        'grid_rows': 3,
        'css_class': 'jardin-layout'
    },
    'reservados': {
        'grid_columns': 1,
        'grid_rows': 1,
        'css_class': 'reservados-layout'
    }
}

def get_mesas_config():
    """Retorna la configuración completa de todas las mesas"""
    return MESAS_CONFIG

def get_layout_config():
    """Retorna la configuración de layout por área"""
    return LAYOUT_CONFIG

def get_mesas_por_area(area):
    """Retorna la configuración de mesas para un área específica"""
    return MESAS_CONFIG.get(area, [])

def get_mesa_config(numero):
    """Retorna la configuración de una mesa específica por número"""
    for area, mesas in MESAS_CONFIG.items():
        for mesa in mesas:
            if mesa['numero'] == numero:
                return {**mesa, 'ubicacion': area}
    return None

def get_total_mesas():
    """Retorna el total de mesas en el restaurante"""
    total = 0
    for area, mesas in MESAS_CONFIG.items():
        total += len(mesas)
    return total

def get_mesas_disponibles_por_area(area):
    """Retorna solo las mesas disponibles para un área (sin estado de BD)"""
    return MESAS_CONFIG.get(area, [])

def get_mesa_ids_por_area(area):
    """Retorna los números de mesa para un área específica"""
    return [mesa['numero'] for mesa in MESAS_CONFIG.get(area, [])] 