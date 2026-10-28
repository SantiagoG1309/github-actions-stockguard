# StockGuard - Practica de GitHub Actions

Repositorio de practica de la guia **Introduccion practica a GitHub Actions**
(Linea de Profundizacion I - Big Data, Ingenieria de Sistemas y Computacion).

Caso de ejemplo: **StockGuard**, control de inventario de supermercados.
El objetivo no es el negocio, sino aprender a ejecutar un workflow de CI,
provocar una falla controlada, corregirla y usar los checks de un Pull Request.

> Este caso NO es parte de RapidGo 360 ni de ninguna de sus variantes.

## Regla de negocio

`clasificar_stock(stock_actual, stock_minimo)` devuelve:

| Condicion | Resultado |
| --- | --- |
| `stock_actual == 0` | `AGOTADO` |
| `stock_actual <= 50 % del minimo` | `CRITICO` |
| `stock_actual <= minimo` | `BAJO` |
| cualquier otro caso | `NORMAL` |
| `stock_actual < 0` o `stock_minimo <= 0` | `ValueError` |

Ejemplo: minimo 20 y 7 unidades disponibles -> `CRITICO`, porque 7 <= 10 (50 % de 20).

## Estructura

```
github-actions-stockguard/
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|-- src/
|   |-- __init__.py
|   `-- inventario.py
|-- tests/
|   `-- test_inventario.py
|-- requirements.txt
`-- README.md
```

## Uso local

```bash
python -m pip install -r requirements.txt
pytest -v
```

## Workflow `CI StockGuard`

Se dispara con `push` a `main`, con `pull_request` hacia `main` y manualmente
con `workflow_dispatch`. Corre en `ubuntu-latest` y ejecuta cinco steps:
checkout, setup de Python 3.12, instalacion de dependencias, validacion de
sintaxis (`compileall`) y `pytest -v`.

## Evidencias

Las evidencias de las ejecuciones (exitosa, fallida intencional, corregida,
Pull Request y ejecucion manual) estan documentadas en
[`docs/EVIDENCIAS.md`](docs/EVIDENCIAS.md).
