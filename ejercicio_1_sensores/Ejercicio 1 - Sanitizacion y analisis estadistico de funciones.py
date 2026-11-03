"""
===============================================================================
EJERCICIO 1: Sanitización y Análisis Estadístico de Sensores
EcoTech Solutions - Trabajo práctico integrador FESAT 2026
===============================================================================

El módulo procesa flujos de datos heterogéneos y crudos en formato de diccionario
en memoria, normalizando los registros individuales y generando un reporte 
consolidado con alertas térmicas.
"""


# =============================================================================
# PASO 1.1: DISEÑAR LA FUNCIÓN DE NORMALIZACIÓN (limpiar_registro_sensor)
# =============================================================================

def limpiar_registro_sensor(registro_raw):
    """
    Toma un diccionario con datos crudos ("sucios") de un sensor y retorna
    un nuevo diccionario perfectamente estandarizado bajo reglas estrictas de negocio.
    
    :param registro_raw: dict con información heterogénea y posible ruido.
    :return: dict limpio y estructurado.
    """
    # Inicialización de una estructura de diccionario vacía para no mutar los datos originales
    registro_limpio = {}
    
    # --- 1. Sanitización del Identificador (sensor_id) ---
    # Extraemos el valor asociado a la clave y aplicamos .strip() para remover espacios al inicio y final
    sensor_id_raw = registro_raw.get("sensor_id", "")
    registro_limpio["sensor_id"] = str(sensor_id_raw).strip()
    
    # --- 2. Estandarización de la Temperatura (temperatura) ---
    temp_raw = registro_raw.get("temperatura", 0.0)
    
    # Bifurcación por tipo de dato: Evaluamos si ya es numérico (int o float)
    if isinstance(temp_raw, (int, float)):
        registro_limpio["temperatura"] = float(temp_raw)
    else:
        # Limpieza de cadenas: Si viene como texto (ej. "24.5C", "31.2°c"), purgamos los caracteres no numéricos
        temp_str = str(temp_raw).lower()
        for char_remplazo in ['c', 'f', '°', ' ']:
            temp_str = temp_str.replace(char_remplazo, '')
        
        # Control de fallos distributivos (try-except): 
        # Si la cadena está corrupta y falla la conversión, asignamos por defecto 0.0
        try:
            registro_limpio["temperatura"] = float(temp_str)
        except ValueError:
            registro_limpio["temperatura"] = 0.0

    # --- 3. Tratamiento del Atributo de Ubicación (ubicacion) ---
    ubicacion_raw = registro_raw.get("ubicacion", "")
    
    # Validación condicional: Para ver si contiene texto real y no está constituido solo por espacios vacíos
    if isinstance(ubicacion_raw, str) and ubicacion_raw.strip():
        registro_limpio["ubicacion"] = ubicacion_raw.strip()
    else:
        # Valor por defecto seguro ante campos vacíos o ausentes
        registro_limpio["ubicacion"] = "Área No Asignada"
        
    # --- 4. Retorno de Datos ---
    return registro_limpio


# =============================================================================
# PASO 1.2: DISEÑAR LA FUNCIÓN DE MAPEO ESTADÍSTICO (generar_resumen_sensores)
# =============================================================================

def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    """
    Procesa una colección de registros sanitizados y un umbral límite para 
    retornar una tupla con la lista de alertas y el promedio térmico global.
    
    :param lista_sensores_limpios: list de diccionarios ya sanitizados.
    :param umbral_temperatura: float que define el límite de temperatura para alertas.
    :return: tupla (lista_sensores_alerta, promedio_temperatura).
    """
    # Cláusula de Guarda (Validación de seguridad inicial):
    # Si la lista está vacía, retornamos de forma anticipada para prevenir ZeroDivisionError.
    if not lista_sensores_limpios:
        return [], 0.0
    
    acumulador_temp = 0.0
    lista_sensores_alerta = []
    total_sensores = len(lista_sensores_limpios)
    
    # Ciclo de procesamiento y acumulación
    for sensor in lista_sensores_limpios:
        temp = sensor.get("temperatura", 0.0)
        acumulador_temp += temp
        
        # Evaluación del umbral de alerta: Comprueba si supera de manera estricta el umbral
        if temp > umbral_temperatura:
            lista_sensores_alerta.append(sensor.get("sensor_id"))
            
    # Cálculo del promedio métrico global y redondeo a 2 decimales con round()
    promedio_temperatura = round(acumulador_temp / total_sensores, 2)
    
    # Retorno estructurado como tupla inmutable exacta
    return lista_sensores_alerta, promedio_temperatura


# =============================================================================
# BLOQUE DE DEMOSTRACIÓN Y PRUEBAS DEL EJERCICIO 1 (DATOS EN MEMORIA)
# =============================================================================

if __name__ == "__main__":
    print("=========================================================")
    print(" DEMOSTRACIÓN DEL EJERCICIO 1: SANITIZACIÓN Y ESTADÍSTICA")
    print("=========================================================\n")

    # Declaración de una lista con diccionarios de prueba en memoria 
    # (emulando casos de error reales: espacios, sufijos y ubicación vacía) (se planteo en la guía)
    registros_crudos = [
        {"sensor_id": " SENSOR-001", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002 ", "temperatura": "35.0 c", "ubicacion": ""},
        {"sensor_id": "SENSOR-003", "temperatura": "19.8°F", "ubicacion": "Planta Sur"},
        {"sensor_id": "SENSOR-004", "temperatura": "corrupto_err", "ubicacion": "   "}
    ]

    # Umbral de temperatura establecido para las pruebas de alerta
    UMBRAL_ALERTA = 25.0

    print("1. Registros crudos originales (en memoria):")
    for r in registros_crudos:
        print(f"   -> {r}")

    # Normalización de la colección utilizando comprensión de listas
    sensores_limpios = [limpiar_registro_sensor(reg) for reg in registros_crudos]

    print("\n2. Registros normalizados (sanitizados):")
    for s in sensores_limpios:
        print(f"   -> ID: {s['sensor_id']} | Temp: {s['temperatura']}°C | Ubicación: {s['ubicacion']}")

    # Invocación de la función de mapeo estadístico
    alertas, promedio_global = generar_resumen_sensores(sensores_limpios, UMBRAL_ALERTA)

    print("\n3. Reporte consolidado estadístico:")
    print(f"   * Umbral de alerta configurado: {UMBRAL_ALERTA}°C")
    print(f"   * Dispositivos en elerta: {alertas}")
    print(f"   * Promedio térmico global de la planta: {promedio_global}°C")