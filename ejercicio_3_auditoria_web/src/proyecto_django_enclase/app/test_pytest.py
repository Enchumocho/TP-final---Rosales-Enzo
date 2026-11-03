import pytest
from .views import calcular_emisiones_carbono, obtener_metricas_consumo


def test_calculo_nominal():
    """Valida la exactitud numérica del cálculo ante valores nominales estándar."""
    resultado = calcular_emisiones_carbono(100, 0.4)
    # Aserción directa de pytest
    assert resultado == 40.0
    #assert resultado == 50.0  # <--- MODIFICACIÓN PARA FORZAR FALLO sacar "#" en caso de usar

def test_factor_personalizado():
    """Valida el cálculo utilizando un factor de emisión específico."""
    resultado = calcular_emisiones_carbono(200, 0.5)
    assert resultado == 100.0


def test_consumo_negativo_excepcion():
    """Verifica la correcta elevación de ValueError ante consumos negativos."""
    # pytest.raises gestiona el contexto de la excepción esperada
    with pytest.raises(ValueError):
        calcular_emisiones_carbono(-50)


def test_obtener_metricas_consumo():
    """Valida el procesamiento global y la identificación de la planta crítica."""
    registros_prueba = [
        {"planta": "Planta Alfa", "consumo_kwh": 200},
        {"planta": "Planta Beta", "consumo_kwh": 500}
    ]
    metricas = obtener_metricas_consumo(registros_prueba)
    assert metricas["total_emisiones"] == 280.0
    assert metricas["planta_mayor_consumo"] == "Planta Beta"