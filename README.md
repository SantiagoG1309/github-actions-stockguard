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

### Alerta de sobrestock (mejora propia)

`detectar_sobrestock(stock_actual, stock_maximo)` compara el stock con la
capacidad maxima de bodega:

| Condicion | Resultado |
| --- | --- |
| `stock_actual > stock_maximo` | `SOBRESTOCK` |
| `stock_actual == stock_maximo` | `AL_LIMITE` |
| en cualquier otro caso | `DISPONIBLE` |
| `stock_actual < 0` o `stock_maximo <= 0` | `ValueError` |

`porcentaje_inventario(stock_actual, stock_maximo)` devuelve el porcentaje de
ocupacion redondeado a dos decimales (por ejemplo, 45 de 180 -> `25.0`).

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

## Evidencias y analisis

- Documento de evidencias y respuestas de analisis: [`docs/EVIDENCIAS.md`](docs/EVIDENCIAS.md)
- Logs completos de cada ejecucion: [`docs/evidencias/`](docs/evidencias/)
- Estado del CI: [Actions - CI StockGuard](https://github.com/SantiagoG1309/github-actions-stockguard/actions/workflows/ci.yml)
