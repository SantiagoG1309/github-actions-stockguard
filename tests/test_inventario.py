import pytest

from src.inventario import (
    clasificar_stock,
    detectar_sobrestock,
    porcentaje_inventario,
)


def test_stock_agotado():
    assert clasificar_stock(0, 20) == "AGOTADO"


def test_stock_critico():
    assert clasificar_stock(7, 20) == "CRITICO"


def test_stock_bajo():
    assert clasificar_stock(15, 20) == "BAJO"


def test_stock_normal():
    assert clasificar_stock(30, 20) == "NORMAL"


def test_stock_invalido():
    with pytest.raises(ValueError):
        clasificar_stock(-2, 20)


def test_sobrestock_detectado():
    assert detectar_sobrestock(120, 100) == "SOBRESTOCK"


def test_sobrestock_en_el_limite():
    assert detectar_sobrestock(100, 100) == "AL_LIMITE"


def test_sobrestock_normal():
    assert detectar_sobrestock(40, 100) == "DISPONIBLE"


def test_sobrestock_invalido():
    with pytest.raises(ValueError):
        detectar_sobrestock(10, 0)


def test_porcentaje_inventario():
    assert porcentaje_inventario(45, 180) == 25.0


def test_porcentaje_inventario_invalido():
    with pytest.raises(ValueError):
        porcentaje_inventario(-5, 100)
