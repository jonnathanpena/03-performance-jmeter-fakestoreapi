INSTRUCCIONES DE EJECUCION - Performance JMeter (FakeStoreAPI)
==============================================================

REQUISITOS
----------
- Java 21+              (verificar: java -version)
- Apache JMeter 5.6.x   (ver instrucciones de instalacion abajo)
- Conexion a internet   (prueba contra fakestoreapi.com)

VERSIONES CLAVE
---------------
- Apache JMeter : 5.6.3
- Java          : 21 (minimo 11)

INSTALACION DE JMETER (macOS)
-----------------------------
Opcion A - Homebrew (recomendado):
  brew install jmeter

Opcion B - Descarga manual:
  1. Ir a https://jmeter.apache.org/download_jmeter.cgi
  2. Descargar apache-jmeter-5.6.3.zip
  3. Descomprimir: unzip apache-jmeter-5.6.3.zip
  4. Agregar al PATH: export PATH=$PATH:/ruta/apache-jmeter-5.6.3/bin

ESTRUCTURA DEL PROYECTO
-----------------------
jmeter/
  test-plan.jmx           -> Plan de prueba JMeter
  test-data/
    users.csv             -> Usuarios parametrizados (5 usuarios)
reports/
  InformeResultados.md    -> Analisis del Ejercicio 2 (textSummary.txt)
results/                  -> Generado al ejecutar (NO incluir en git)

EJECUCION
---------

1. MODO GRAFICO (abrir JMeter GUI para editar o explorar):
   jmeter -t jmeter/test-plan.jmx

2. MODO NO GRAFICO (ejecucion CLI - RECOMENDADO para CI/CD):
   mkdir -p results/html-report
   jmeter -n \
     -t jmeter/test-plan.jmx \
     -l results/results.jtl \
     -e -o results/html-report/ \
     -j results/jmeter.log

3. Ver reporte HTML generado:
   Abrir: results/html-report/index.html

PARAMETROS CONFIGURABLES
-------------------------
  -JTHREADS=40      -> Numero de usuarios virtuales (default: 40)
  -JRAMP_UP=30      -> Tiempo de rampa en segundos (default: 30)
  -JDURATION=120    -> Duracion de la prueba en segundos (default: 120)

Ejemplo con parametros custom:
  jmeter -n -t jmeter/test-plan.jmx -JTHREADS=50 -JDURATION=180 \
    -l results/results.jtl -e -o results/html-report/

CRITERIOS DE ACEPTACION
-----------------------
  - Throughput     : >= 20 TPS (requests por segundo)
  - Tiempo resp.   : P95 <= 1,500 ms
  - Tasa de error  : < 3% del total de peticiones
  - Assertion      : HTTP 200 + campo "token" en el response body

NOTAS
-----
- El archivo users.csv recicla los 5 usuarios (recycle=true) para
  mantener la carga durante toda la duracion de la prueba.
- Con 40 hilos y el Constant Throughput Timer configurado a 1200 req/min
  (20 TPS minimo) se garantiza el criterio de throughput.
- Para reproducir el analisis del Ejercicio 2, ver: reports/InformeResultados.md
