"""Reglas de negocio de StockGuard (ejemplo de practica para GitHub Actions).

Este modulo NO forma parte de RapidGo 360: se usa unicamente para aprender
como un workflow de integracion continua valida reglas de negocio con pytest.
"""


def clasificar_stock(stock_actual: int, stock_minimo: int) -> str:
    """Clasifica el nivel de riesgo del inventario de un producto.

    Reglas:
        - stock_actual == 0                  -> AGOTADO
        - stock_actual <= 50 % del minimo    -> CRITICO
        - stock_actual <= minimo             -> BAJO
        - cualquier otro caso                -> NORMAL
    """
    if stock_actual < 0:
        raise ValueError("El stock actual no puede ser negativo")
    if stock_minimo <= 0:
        raise ValueError("El stock minimo debe ser mayor que cero")

    if stock_actual == 0:
        return "AGOTADO"
    if stock_actual <= stock_minimo * 0.5:
        return "CRITICO"
    if stock_actual <= stock_minimo:
        return "BAJO"
    return "NORMAL"
