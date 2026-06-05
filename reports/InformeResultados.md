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

## 6. Conclusión Final

La aplicación **no está lista para producción** con la carga de 140 usuarios virtuales.
El incumplimiento del P95 y el crash observable en el diagrama son indicadores de que
la arquitectura actual requiere optimizaciones antes de poder garantizar un SLA del
99.9% con los criterios definidos.

Se recomienda ejecutar un ciclo de profiling + optimización y repetir la prueba de
carga antes del siguiente release.
