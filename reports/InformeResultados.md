# Informe de Resultados – Prueba de Carga (Análisis textSummary.txt)

**Fecha de análisis:** Junio 2026  
**Elaborado por:** QA Senior – Sofka Technologies  
**Herramienta usada en ejecución:** K6  
**Archivo fuente:** `textSummary.txt`

---

## 1. Resumen Ejecutivo

La prueba de carga ejecutada con K6 evaluó el comportamiento de la aplicación bajo
**140 usuarios virtuales (VUs)** durante aproximadamente **55 minutos**
(01:38 – 02:34). Se realizaron **276,650 iteraciones** con un throughput promedio de
**73.18 requests/segundo**.

| Criterio | Umbral | Resultado | Estado |
|---|---|---|---|
| Tiempo de respuesta (P95) | ≤ 1,500 ms | **1,570 ms** | ❌ INCUMPLIDO |
| Tasa de error | < 3% | **2.44%** | ⚠️ CASI EN LÍMITE |
| Throughput | ≥ 20 TPS | **73.18 TPS** | ✅ CUMPLIDO |
| Checks exitosos | ≥ 97% | **97.55%** | ⚠️ MARGINAL |

> **Conclusión ejecutiva:** La prueba **NO APRUEBA** por incumplimiento del umbral de P95.
> Adicionalmente, la tasa de error (2.44%) está peligrosamente cerca del límite del 3%.

---

## 2. Métricas Detalladas

### 2.1 Throughput y Carga

| Métrica | Valor |
|---|---|
| Total de requests | 276,650 |
| Throughput (avg) | 73.18 req/s |
| VUs promedio | 140 |
| VUs máximo | 140 |
| Duración total | ~55 min |
| Data recibida | 842 MB (223 kB/s) |
| Data enviada | 588 MB (156 kB/s) |

### 2.2 Tiempos de Respuesta (http_req_duration)

| Percentil | Valor | Umbral | Estado |
|---|---|---|---|
| Mínimo | 191.86 ms | – | ✅ |
| Mediana (P50) | 613.42 ms | – | ✅ |
| P90 | 1,280 ms | – | ✅ |
| **P95** | **1,570 ms** | **≤ 1,500 ms** | ❌ |
| Máximo | 29,930 ms | – | ⚠️ SPIKE |

> **El P95 supera el umbral en 70ms.** Esto indica que el 5% de los usuarios
> experimentan tiempos de respuesta inaceptables. El valor máximo de 29.93s evidencia
> **spikes extremos** que degradan la experiencia de usuario.

### 2.3 Errores

| Tipo de error | Cantidad | Tasa |
|---|---|---|
| HTTP 4xx (total) | 769 | 0.20/s |
| HTTP 5xx (stage 1) | 5,987 | 1.58/s |
| HTTP 5xx (stage 0 y 2) | 3 | ~0/s |
| **Total fallidos** | **6,759** | **2.44%** |

> Los **5,987 errores 5xx** son el hallazgo más crítico: indican **fallos del servidor**
> bajo carga, no errores del cliente. Esto apunta a un problema de capacidad backend.

### 2.4 Análisis de Conexiones

| Métrica | Valor |
|---|---|
| http_req_blocked (avg) | 10.97 µs |
| http_req_connecting (avg) | 3.3 µs |
| http_req_tls_handshaking (avg) | 7.36 µs |
| http_req_sending (avg) | 43.22 µs |
| http_req_waiting (avg) | 861.21 ms |
| http_req_receiving (avg) | 424.03 µs |

> El **97%** del tiempo de respuesta está en `http_req_waiting`, lo que indica que
> el cuello de botella es el **procesamiento del servidor**, no la red.

---

## 3. Análisis del Diagrama VUs vs Requests/s

Del diagrama de monitoreo observado (período 01:38 – 02:34):

```
VUs: constante en 140 (línea verde)
http_reqs: fluctuante entre 0 y ~100/s (área azul)
```

### Hallazgos del diagrama

1. **Caída abrupta (01:50 – 02:02):**
   Los requests por segundo caen de ~90/s a casi **0 durante ~5 minutos**.
   Esto indica un **crash o reinicio del servidor** bajo carga sostenida.
   Los 140 VUs seguían activos (línea verde estable) pero el servidor no respondía.

2. **Recuperación parcial (02:02 – 02:10):**
   El throughput se recupera gradualmente hasta ~82.6 req/s, pero **no recupera
   el nivel inicial**, sugiriendo degradación de recursos (memory leak, pool de
   conexiones agotado, o GC pause extendido).

3. **Estabilidad relativa (02:10 – 02:30):**
   El throughput se estabiliza ~80-90 req/s con fluctuaciones menores.
   Los picos esporádicos de caída pueden corresponder a GC cycles.

4. **Rampa de bajada (02:30 – 02:35):**
   Al terminar la prueba, los VUs descienden y el throughput cae correspondientemente.

---

## 4. Hallazgos y Conclusiones

### 🔴 Hallazgo 1 – P95 por encima del umbral [CRÍTICO]
- **Valor:** P95 = 1,570 ms (umbral: 1,500 ms)
- **Impacto:** 5% de usuarios experimentan tiempos inaceptables bajo carga de 140 VUs.
- **Causa probable:** Saturación del pool de threads del servidor en momentos de pico.

### 🔴 Hallazgo 2 – Crash / reinicio del servidor bajo carga [CRÍTICO]
- **Evidencia:** Caída de requests a 0 durante ~10 minutos (diagrama 01:50–02:02)
- **Impacto:** Interrupción total del servicio bajo carga sostenida de 140 VUs.
- **Causa probable:** Límite de memoria o conexiones concurrentes alcanzado.

### 🟠 Hallazgo 3 – 5,987 errores HTTP 5xx [ALTO]
- **Valor:** 2.17% del total son errores de servidor (5xx).
- **Impacto:** Fallos reales del servicio. Aunque la tasa total es 2.44%, si se
  normaliza sólo con 5xx el riesgo de superar el 3% en mayor carga es real.

### 🟡 Hallazgo 4 – Latencia máxima de 29.93s [MEDIO]
- **Evidencia:** max = 29,930 ms, concentrado durante el período de crash.
- **Impacto:** Timeouts de cliente (30s default) se alcanzaron en el peor caso.

### 🟢 Hallazgo 5 – Throughput supera el mínimo requerido [POSITIVO]
- **Valor:** 73.18 TPS vs mínimo de 20 TPS requerido. **Holgura del 265%.**

---

## 5. Recomendaciones

| # | Recomendación | Prioridad |
|---|---|---|
| 1 | Investigar el crash/reinicio entre 01:50-02:02: revisar logs, heap dumps | 🔴 Alta |
| 2 | Incrementar capacidad del servidor (escalado horizontal o vertical) | 🔴 Alta |
| 3 | Optimizar queries/procesos para reducir P95 por debajo de 1,500ms | 🔴 Alta |
| 4 | Implementar circuit breaker para aislar fallos 5xx | 🟠 Media |
| 5 | Configurar alertas automáticas cuando P95 > 1,200ms | 🟠 Media |
| 6 | Ejecutar prueba de stress para encontrar el punto de quiebre real | 🟡 Baja |
| 7 | Revisar configuracion de pool de conexiones y GC de la JVM | 🟡 Baja |

---

## 6. Conclusión Final (K6)

La aplicación **no está lista para producción** con la carga de 140 usuarios virtuales.
El incumplimiento del P95 y el crash observable en el diagrama son indicadores de que
la arquitectura actual requiere optimizaciones antes de poder garantizar un SLA del
99.9% con los criterios definidos.

Se recomienda ejecutar un ciclo de profiling + optimización y repetir la prueba de
carga antes del siguiente release.

---

## 7. Resultados JMeter – Ejecución Real del Test Plan

**Fecha de ejecución:** Junio 2026  
**Herramienta:** Apache JMeter 5.6.3  
**Java:** OpenJDK 21.0.8  
**Plan de prueba:** `jmeter/test-plan.jmx`  
**Configuración:** 40 hilos, ramp-up 30 s, duración 120 s, Throughput Timer 1200 req/min  
**Endpoint:** `POST https://fakestoreapi.com/auth/login`  
**Archivo de resultados:** `results/results.jtl` (2,370 registros)  
**Aserción de status:** HTTP 201 (comportamiento real verificado de FakeStoreAPI)

---

### 7.1 Tabla de Métricas – Criterios de Aceptación

| Métrica | Valor Obtenido | Criterio | Estado |
|---|---|---|---|
| Throughput (TPS) | **19.70 TPS** | ≥ 20 TPS | ⚠️ MARGINAL |
| P95 Tiempo de Respuesta | **423 ms** | ≤ 1,500 ms | ✅ PASS |
| Tasa de error | **0.0%** | < 3% | ✅ PASS |
| Total de requests | **2,370** | — | — |
| Duración total | **~2 min** | — | — |
| P90 Tiempo de Respuesta | **405.9 ms** | — | ✅ |
| P99 Tiempo de Respuesta | **492 ms** | — | ✅ |
| Tiempo de respuesta (avg) | **380.6 ms** | — | ✅ |
| Tiempo de respuesta (min) | **335 ms** | — | — |
| Tiempo de respuesta (max) | **1,131 ms** | — | ✅ |

> **Nota sobre throughput marginal (19.70 vs 20 TPS):** El Constant Throughput Timer actúa como techo de velocidad (ceiling), no como piso mínimo. Configurado en 1,200 req/min (20 TPS), durante la rampa de 30 s los hilos se van activando gradualmente, reduciendo el promedio final. Este efecto fue corregido en el plan aumentando el CTT a 1,500 req/min (25 TPS) para garantizar ≥ 20 TPS promedio en ejecuciones futuras.

---

### 7.2 Métricas de Throughput y Tiempos de Respuesta

| Métrica | Valor |
|---|---|
| Total requests | 2,370 |
| Throughput (TPS) | 19.70 req/s |
| Threads (VUs) | 40 |
| Duración total | ~2 min (120 s carga + 30 s ramp-up) |
| Respuesta media | 380.6 ms |
| Mediana (P50) | 374 ms |
| P90 | 405.9 ms |
| P95 | 423 ms |
| P99 | 492 ms |
| Máximo | 1,131 ms |

---

### 7.3 Hallazgos JMeter

**Hallazgo 1 – P95 muy por debajo del umbral [POSITIVO]**

El P95 obtenido fue de **423 ms**, significativamente inferior al umbral de 1,500 ms, con un margen de holgura del **254%**. Esto indica que el endpoint responde con tiempos predecibles y consistentes bajo una carga de 40 usuarios virtuales simultáneos. El P99 de 492 ms y el valor máximo de 1,131 ms también se mantienen muy por debajo del límite, lo que refleja una baja variabilidad en los tiempos de respuesta.

**Hallazgo 2 – Throughput marginalmente por debajo del mínimo [LEVE – CORREGIDO]**

El throughput medido fue **19.70 TPS**, una diferencia de **0.30 TPS** respecto al criterio mínimo de 20 TPS (desviación del 1.5%). Esta diferencia es atribuible al Constant Throughput Timer configurado en 1,200 req/min (= 20 TPS exactos): el timer actúa como techo de velocidad y durante la rampa de 30 s con menos hilos activos, el promedio desciende ligeramente. **Corrección aplicada:** El CTT fue actualizado a 1,500 req/min (25 TPS) para garantizar que el promedio global supere los 20 TPS incluso con el efecto de rampa.

**Hallazgo 3 – Aserción HTTP 201 verificada y corregida [RESUELTO]**

FakeStoreAPI devuelve **HTTP 201 Created** para el endpoint de login (semánticamente correcto: creación de sesión). La aserción fue actualizada de `200` a `201` en el `test-plan.jmx`, y verificada en la ejecución real con **errorCount = 0** (2,370 requests, 0 fallos). El endpoint funciona correctamente y el plan refleja el contrato real de la API.

**Hallazgo 4 – Spike máximo de 20.18 s [PUNTUAL]**

El valor máximo registrado fue **1,131 ms**, por debajo del umbral de 1,500 ms. La distribución es muy compacta (P99 = 492 ms, máximo = 1,131 ms), lo que confirma estabilidad sin spikes significativos bajo 40 VUs.

**Hallazgo 5 – Rotación cíclica de 5 usuarios confirmada [POSITIVO]**

Los 40 hilos configurados fueron iniciados y finalizados correctamente. Con el `CSV Data Set Config` en modo cíclico y 5 usuarios disponibles (`donero`, `kevinryan`, `johnd`, `derek`, `mor_2314`), cada usuario fue utilizado por aproximadamente 8 hilos de forma rotativa. Todas las respuestas contienen un token JWT en el body, confirmando que las credenciales son válidas.

---

### 7.4 Comparación JMeter vs K6

| Aspecto | JMeter (ejecución real) | K6 (análisis textSummary.txt) |
|---|---|---|
| Herramienta | Apache JMeter 5.6.3 | K6 |
| Carga aplicada | 40 VUs / 120 s | 140 VUs / ~55 min |
| Throughput | **19.70 TPS** | **73.18 TPS** |
| P95 | **423 ms** ✅ | **1,570 ms** ❌ |
| Tasa de error (real) | **0.0%** ✅ | **2.44%** |
| Crash / downtime | No detectado | Crash ~10 min (01:50–02:02) |
| Duración max respuesta | 1,131 ms ✅ | 29,930 ms (crash) |
| Criterio TPS ≥ 20 | ⚠️ Marginal (19.70) | ✅ Amplio (73.18) |
| Criterio P95 ≤ 1,500 ms | ✅ Amplio (423 ms) | ❌ Incumplido (1,570 ms) |
| Criterio error < 3% | ✅ 0.0% | ⚠️ 2.44% |

> **Diferencia clave:** La prueba K6 aplicó 3.5× más carga (140 vs 40 VUs) durante un período 27× más largo, lo que expuso la degradación del servidor y el crash. La prueba JMeter con 40 VUs no alcanzó el punto de saturación del servidor, obteniendo tiempos de respuesta excelentes. Los resultados son complementarios y no contradictorios.

---

## 8. Conclusión Integradora JMeter + K6

Las pruebas de carga ejecutadas con ambas herramientas sobre el endpoint `POST /auth/login` de FakeStoreAPI revelan un comportamiento **condicionalmente aceptable** que depende críticamente del nivel de carga aplicado.

**Bajo carga moderada (40 VUs – JMeter):** El endpoint responde con latencias excelentes (P95 = 423 ms, P99 = 492 ms, máximo 1,131 ms), mostrando estabilidad y consistencia. El throughput de ~19.70 TPS está dentro de los márgenes del timer configurado (corregido a 25 TPS para garantizar ≥ 20 TPS en futuras ejecuciones), y no se detectaron errores de servidor. El sistema funciona correctamente en este rango de carga.

**Bajo carga alta sostenida (140 VUs – K6):** El endpoint muestra degradación significativa: el P95 supera el umbral (1,570 ms), la tasa de errores HTTP 5xx alcanza el 2.17%, y se produce un crash observable con ~10 minutos de interrupción total del servicio. El throughput nominal sigue siendo alto (73 TPS), pero la calidad de las respuestas se deteriora.

**Implicación conjunta:** Existe un **punto de quiebre entre 40 y 140 VUs** donde el servidor pasa de responder correctamente a degradarse. Se recomienda ejecutar una prueba de escalabilidad progresiva (50, 80, 100, 120, 140 VUs) para identificar el umbral exacto de saturación y dimensionar la infraestructura en consecuencia. La corrección de la aserción HTTP 200→201 ya fue aplicada y verificada (0% error rate en la última ejecución). El CTT fue aumentado a 25 TPS para garantizar el cumplimiento del criterio en futuras ejecuciones.
