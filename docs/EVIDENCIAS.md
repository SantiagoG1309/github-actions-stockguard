# Evidencias y analisis - GitHub Actions con StockGuard

**Estudiante:** Kevin Santiago Garcia Ospina
**Repositorio:** https://github.com/SantiagoG1309/github-actions-stockguard
**Guias:** Introduccion practica a GitHub Actions - CI con Python, pytest y Pull Requests
(Linea de Profundizacion I - Big Data)

Los logs completos de cada ejecucion estan en esta misma carpeta (`docs/evidencias/`),
descargados con `gh run view <id> --log`. Los enlaces abren la ejecucion en GitHub.

---

## 1. Resumen de ejecuciones

| # | Run ID | Commit | Evento | Resultado | Que lo determino |
| --- | --- | --- | --- | --- | --- |
| 0 | [40765037544](https://github.com/SantiagoG1309/github-actions-stockguard/actions/runs/40765037544) | `e341ea1` | `push` a main | ❌ failure | Step **Ejecutar pruebas**: `ModuleNotFoundError: No module named 'src'` |
| 1 | [40765171667](https://github.com/SantiagoG1309/github-actions-stockguard/actions/runs/40765171667) | `9e6b89c` | `push` a main | ✅ success | Los 5 steps en verde (5 pruebas PASSED) |
| 2 | [40765302518](https://github.com/SantiagoG1309/github-actions-stockguard/actions/runs/40765302518) | `55700b2` | `push` a main | ❌ failure (intencional) | Step **Ejecutar pruebas**: `1 failed, 4 passed` |
| 3 | [40765420201](https://github.com/SantiagoG1309/github-actions-stockguard/actions/runs/40765420201) | `21a197d` | `push` a main | ✅ success | Restaurada la prueba correcta (5 PASSED) |
| 4 | [40765715202](https://github.com/SantiagoG1309/github-actions-stockguard/actions/runs/40765715202) | `8d7bd97` | `pull_request` -> main | ✅ success | Check `validar-python` del PR #2 (11 PASSED) |
| 5 | [40765822218](https://github.com/SantiagoG1309/github-actions-stockguard/actions/runs/40765822218) | `ad3ef33` | `workflow_dispatch` | ✅ success | Ejecucion manual desde la pestana Actions |
| 6 | [40765935201](https://github.com/SantiagoG1309/github-actions-stockguard/actions/runs/40765935201) | `a3c2d57` | `push` a main (merge del PR #2) | ✅ success | Integracion del PR ya validado |

- **Workflow:** `CI StockGuard` (`ci.yml`)
- **Job:** `validar-python` sobre `ubuntu-latest`, Python 3.12
- **Steps:** Descargar repositorio -> Configurar Python -> Instalar dependencias -> Validar sintaxis -> Ejecutar pruebas
- **Pull Request:** https://github.com/SantiagoG1309/github-actions-stockguard/pull/2 (merged)
- **Issue de origen:** https://github.com/SantiagoG1309/github-actions-stockguard/issues/1
- **Rama de la mejora:** `feature/alerta-sobrestock` (commit `8d7bd97`)

> **Hallazgo real del paso 1 (run 0).** La primera ejecucion fallo aunque en local
> las 5 pruebas pasaban. En el runner el step es `pytest -v` (comando directo), asi que
> la raiz del repositorio **no** se agrega a `sys.path`; en local yo habia usado
> `python -m pytest`, que si agrega el directorio actual. Se corrigio agregando
> `pytest.ini` con `pythonpath = .` (commit `9e6b89c`). Es exactamente el caso
> "pasa local pero falla en GitHub" de la seccion 19 de la guia.

---

## 2. Evidencias exigidas (seccion 18)

| Evidencia | Donde esta |
| --- | --- |
| Ejecucion exitosa con nombre del workflow y steps | Run [40765171667](https://github.com/SantiagoG1309/github-actions-stockguard/actions/runs/40765171667) + `run-01-exitoso.log` |
| Ejecucion fallida causada intencionalmente | Run [40765302518](https://github.com/SantiagoG1309/github-actions-stockguard/actions/runs/40765302518) + `run-02-fallido.log` |
| Ejecucion posterior corregida | Run [40765420201](https://github.com/SantiagoG1309/github-actions-stockguard/actions/runs/40765420201) + `run-03-corregido.log` |
| Pull Request mostrando los checks | [PR #2](https://github.com/SantiagoG1309/github-actions-stockguard/pull/2) + `run-04-pull-request.log` |
| Ejecucion manual (`workflow_dispatch`) | Run [40765822218](https://github.com/SantiagoG1309/github-actions-stockguard/actions/runs/40765822218) + `run-05-manual-workflow-dispatch.log` |
| Commit/PR con regla y pruebas propias | Commit `8d7bd97` / [PR #2](https://github.com/SantiagoG1309/github-actions-stockguard/pull/2) |

Si se necesitan capturas de pantalla, se pueden tomar directamente de esos enlaces:
Actions > CI StockGuard > run > job `validar-python` > cada step.

### Capturas incluidas en `docs/evidencias/`

| Captura | Que muestra |
| --- | --- |
| `captura-01-ejecucion-exitosa.png` | Run #4 (push, `21a197d`): workflow `CI StockGuard`, job `validar-python` en verde, disparado por push |
| `captura-02-ejecucion-fallida.png` | Run #3 (push, `55700b2`): mismo workflow en rojo tras el cambio intencional |
| `captura-03-job-fallido-steps.png` | Detalle del job fallido: los 4 primeros steps en verde y **Ejecutar pruebas** en rojo |
| `captura-04-job-exitoso-steps.png` | Detalle del job exitoso: los 5 steps en verde |
| `captura-05-pull-request-checks.png` | PR #2 merged con su commit y el check asociado |
| `captura-05b-pull-request-checks-detalle.png` | Pestana Checks del PR: `CI StockGuard` disparado por `pull_request` |
| `captura-06-ejecucion-manual.png` | Run disparado con `workflow_dispatch` (ejecucion manual) |

### Proteccion de rama aplicada

Para que la condicion "si falla un check no se puede mergear" no dependa de la
disciplina del equipo, se configuro en `main`:

- **Required status check:** `validar-python` (strict: la rama debe estar actualizada).
- Force push y borrado de `main` bloqueados.

Verificacion:

```bash
gh api repos/SantiagoG1309/github-actions-stockguard/branches/main/protection
# -> required_status_checks.contexts = ["validar-python"], strict = true
```

---

## 3. Preguntas de analisis (seccion 17)

### 1. Una ejecucion exitosa y una fallida: que cambio y que step decidio

- **Exitosa:** run `40765420201`, commit `21a197d` ("fix(test): restaurar la expectativa
  correcta de stock critico"). El step **Ejecutar pruebas** termino con `5 passed`.
- **Fallida:** run `40765302518`, commit `55700b2` ("test: provocar fallo controlado de CI"),
  donde `test_stock_critico` esperaba `NORMAL` para `clasificar_stock(7, 20)`.

En ambos casos el step que decidio el resultado fue **Ejecutar pruebas**; los cuatro
anteriores (checkout, setup-python, dependencias y `compileall`) terminaron bien en las dos.

### 2. Por que `pytest` local no reemplaza `pytest` en Actions

Porque el runner es un entorno **limpio y distinto**: sistema operativo Linux, Python
recien instalado, sin mis dependencias ni mis archivos locales, y solo con lo que quedo
commiteado. Lo comprobe en el run `40765037544`: localmente las pruebas pasaban y en
GitHub fallo con `ModuleNotFoundError: No module named 'src'`, porque el step usa
`pytest -v` y no `python -m pytest` (diferencia de `sys.path`). Ademas el runner no
tiene estado previo: si una dependencia no esta en `requirements.txt`, falla ahi aunque
en mi equipo funcione. CI valida "el repositorio tal como lo recibe otra persona".

### 3. Riesgo de hacer merge a main sin esperar los checks

Se integra codigo no verificado y main deja de ser una base confiable: cualquier
companero que haga `pull` hereda el fallo y sus propias ejecuciones empiezan a fallar
por algo que no escribio. Ademas se pierde el rastro: sin el check asociado al PR es
mas dificil saber que cambio rompio que, y en la entrega del proyecto el equipo puede
llegar a la demo con main roto. Con el check en el PR, el error se ve **antes** de
tocar main y queda ligado al commit que lo causo.

### 4. Linea esencial del error en la ejecucion fallida

```
E       AssertionError: assert 'CRITICO' == 'NORMAL'
```

Con esa linea (y el resumen `1 failed, 4 passed`) pude diagnosticar que la funcion
devolvia `CRITICO` y la prueba esperaba `NORMAL`: el fallo estaba en la **expectativa
de la prueba**, no en la logica de negocio, porque las otras cuatro pruebas seguian
pasando. Sin el `-v` de pytest no habria visto cual prueba fallo ni el valor real.

### 5. Diferencia entre un step con `uses:` y uno con `run:`

- `uses:` invoca una **action reutilizable** publicada y versionada
  (`actions/checkout@v6`, `actions/setup-python@v5`). No escribo el codigo: le paso
  parametros con `with:` y GitHub resuelve la implementacion.
- `run:` ejecuta **comandos de shell** en el runner (`pip install`, `compileall`,
  `pytest`). Depende del shell del runner (aqui `bash`) y de que las herramientas ya
  esten instaladas o se instalen antes.

En resumen: `uses:` reutiliza logica empaquetada; `run:` ejecuta lo que yo escribo.

### 6. Que aporta `${{ github.actor }}` en `run-name`

Es el usuario de GitHub que disparo la ejecucion (por push, por PR o manualmente).
Por eso mis ejecuciones aparecen como "CI ejecutado por SantiagoG1309". En un equipo
de tres personas permite ver **quien** ejecuto cada verificacion sin abrir los logs, y
en la ejecucion manual (`workflow_dispatch`) sirve como evidencia de participacion
individual, tal como plantea la guia para el proyecto final.

### 7. Si el workflow pasa pero la aplicacion falla en Docker, Actions "no sirve"?

No. Actions esta verificando una **porcion** del sistema: que el codigo Python compile,
que las dependencias declaradas se instalen y que las reglas de negocio se cumplan en
pruebas unitarias. No verifica integracion real: Kafka, Spark, Airflow, volumenes,
redes, variables de entorno, orden de arranque de contenedores ni datos reales. Un check
verde significa "no rompiste lo que estaba cubierto", no "el sistema completo funciona".
La validacion de integracion sigue siendo local (o en un job mas costoso aparte).

### 8. Tres checks propuestos para mi variante de RapidGo 360

> Propuesta a validar con el equipo; la regla concreta depende de la variante asignada.
> Se muestra el caso "inventario / fulfillment", que es el que practique aqui.

| Check | Regla que verifica | Error concreto que evita |
| --- | --- | --- |
| 1. Pruebas de la regla de negocio | `detectar_stockout(stock, demanda)` clasifica bien el caso normal, el limite y el invalido | Que un cambio en los umbrales genere alertas falsas o silencie un stockout real |
| 2. Contrato del evento JSON | Validar que el evento que produce el producer tenga los campos y tipos esperados (`producto_id`, `stock`, `timestamp`) | Que el consumer o Spark falle en ejecucion por un campo faltante o mal tipado |
| 3. Estructura y sintaxis del proyecto | `compileall` sobre las carpetas Python + `docker compose config --quiet` | Que se suba un archivo con error de sintaxis o un `compose.yml` invalido que nadie nota hasta la demo |

### 9. Cual check deberia implementarse primero y por que

El **1** (pruebas de la regla de negocio) junto con `compileall`. Es el mas barato
(segundos, sin servicios externos), da retroalimentacion inmediata en cada push y
protege la decision central del proyecto. Ademas, sin sintaxis valida ni reglas
correctas, los otros checks no aportan: primero hay que garantizar que el nucleo del
sistema es correcto y despues ampliar la cobertura.

### 10. Que prueba seria demasiado costosa o fragil para cada push

Levantar el stack completo Kafka + Spark + Airflow y esperar a que un Producer envie
datos varios minutos: consume muchos minutos, depende de servicios externos y es
propensa a fallos intermitentes (falsos negativos) que harian perder confianza en el
check. Alternativa: validar en cada push solo lo estatico (`compileall`,
`docker compose config --quiet`, pruebas unitarias) y dejar la prueba de integracion
para `workflow_dispatch` o para un job programado (`schedule`) antes de la entrega,
con un conjunto de datos pequeno y tiempo limite.

---

## 4. Transferencia al Proyecto Final RapidGo 360 (seccion 16)

Esta practica **no** se copia al proyecto: la funcion `clasificar_stock` y sus pruebas
pertenecen solo a StockGuard. Lo que se traslada es el mecanismo y las decisiones:

1. **Regla propia de la variante:** una funcion pura, sin Kafka, que reciba datos y
   devuelva una clasificacion (por ejemplo `clasificar_cumplimiento`,
   `clasificar_temperatura`, `clasificar_servicio` o `evaluar_mantenimiento`).
2. **Tres casos minimo:** normal, limite e invalido/alerta, igual que aqui
   (`NORMAL`, `AL_LIMITE`/`CRITICO`, `ValueError`).
3. **Carpetas para `compileall`:** las que contengan codigo Python del equipo
   (`src/`, `producer/`, `consumer/`, `dags/`), excluyendo entornos virtuales.
4. **Archivos a comprobar:** `requirements.txt` presente, `docker-compose.yml` valido
   con `docker compose config --quiet`, y el esquema del evento JSON.
5. **Condicion que impide el merge:** el check `validar-python` en rojo (sintaxis o
   pruebas fallidas) bloquea el PR a `main`; se configura como *required status check*
   en la proteccion de la rama.

Flujo de trabajo adoptado:

```
Issue -> Branch -> Codigo + pruebas -> Pull Request -> GitHub Actions -> Review -> Merge
```

---

## 5. Conclusion

GitHub Actions no es "un YAML para cumplir": es la forma de convertir las reglas de
calidad del equipo en verificaciones repetibles. En esta practica lo comprobe en los
dos sentidos: un cambio de una sola linea en una prueba puso el workflow en rojo
(`1 failed, 4 passed`) y el mismo mecanismo, al corregirlo, lo devolvio a verde. El
valor real aparece en el Pull Request: el check corre antes del merge y deja evidencia
de que la integracion no rompio lo que ya funcionaba.
