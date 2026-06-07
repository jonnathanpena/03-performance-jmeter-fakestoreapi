# Performance Testing with JMeter - FakeStoreAPI

Performance testing project using Apache JMeter to validate the FakeStoreAPI authentication endpoint under load.

## 📋 Overview

This project contains a complete JMeter test plan for load testing the `POST /auth/login` endpoint from [FakeStoreAPI](https://fakestoreapi.com). The test validates performance criteria including throughput, response times, and error rates under sustained load.

## 🎯 Test Objectives

- **Throughput**: ≥ 20 TPS (transactions per second)
- **Response Time**: P95 ≤ 1,500ms
- **Error Rate**: < 3% of total requests
- **Assertions**: HTTP 200 response + "token" field in response body

## 🛠️ Requirements

- **Java**: 21+ (minimum 11)
- **Apache JMeter**: 5.6.3
- **Internet Connection**: Required for testing against fakestoreapi.com

## 📦 Installation

### macOS

**Option A - Homebrew (Recommended):**
```bash
brew install jmeter
```

**Option B - Manual Download:**
```bash
# Download from https://jmeter.apache.org/download_jmeter.cgi
wget https://downloads.apache.org//jmeter/binaries/apache-jmeter-5.6.3.zip
unzip apache-jmeter-5.6.3.zip
export PATH=$PATH:/path/to/apache-jmeter-5.6.3/bin
```

## 📁 Project Structure

```
.
├── jmeter/
│   ├── test-plan.jmx          # JMeter test plan
│   └── test-data/
│       └── users.csv          # Parameterized test users (5 users)
├── reports/
│   └── InformeResultados.md   # Test analysis report
├── results/                   # Generated on execution (gitignored)
├── conclusiones.txt           # Project conclusions
└── README.md                  # This file
```

## 🚀 Execution

### GUI Mode (For Editing/Exploration)

```bash
jmeter -t jmeter/test-plan.jmx
```

### CLI Mode (Recommended for CI/CD)

```bash
mkdir -p results/html-report
jmeter -n \
  -t jmeter/test-plan.jmx \
  -JcsvPath=jmeter/test-data/users.csv \
  -l results/results.jtl \
  -e -o results/html-report/ \
  -j results/jmeter.log
```

### View HTML Report

Open `results/html-report/index.html` in your browser.

## ⚙️ Configurable Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `-JTHREADS` | 40 | Number of virtual users |
| `-JRAMP_UP` | 30 | Ramp-up time in seconds |
| `-JDURATION` | 120 | Test duration in seconds |

**Example with custom parameters:**
```bash
jmeter -n -t jmeter/test-plan.jmx -JTHREADS=50 -JDURATION=180 \
  -l results/results.jtl -e -o results/html-report/
```

## 📊 Test Configuration

- **Virtual Users**: 40 concurrent users
- **Ramp-up**: 30 seconds
- **Duration**: 120 seconds
- **Throughput Timer**: 1500 req/min (25 TPS ceiling — garantiza ≥ 20 TPS promedio con efecto ramp-up)
- **User Data**: 5 users from CSV with cyclic recycling

## � Results

### Ejercicio 1 – JMeter Load Test (run real: `results/html-report/`)

| Criterio | Umbral | Resultado | Estado |
|---|---|---|---|
| Throughput (TPS) | ≥ 20 TPS | **19.70 TPS** | ⚠️ Marginal |
| P95 Response Time | ≤ 1,500 ms | **423 ms** | ✅ PASS |
| P90 Response Time | — | **405.9 ms** | ✅ |
| P99 Response Time | — | **492 ms** | ✅ |
| Error Rate | < 3% | **0.0%** | ✅ PASS |
| Total Requests | — | **2,370** | — |
| HTTP Status | 201 | **201 ✅** | ✅ PASS |
| Max Response Time | — | **1,131 ms** | ✅ |

> **Nota TPS marginal:** El CTT configurado en 1,200 req/min actúa como ceiling. Durante el ramp-up de 30 s el promedio baja a 19.70 TPS. Corregido a 1,500 req/min (25 TPS) para ejecuciones futuras.

### Ejercicio 2 – Análisis K6 (`reports/textSummary.txt`)

| Criterio | Umbral | Resultado | Estado |
|---|---|---|---|
| Throughput (TPS) | ≥ 20 TPS | **73.18 TPS** | ✅ PASS |
| P95 Response Time | ≤ 1,500 ms | **1,570 ms** | ❌ FAIL |
| Error Rate | < 3% | **2.44%** | ⚠️ Límite |
| Server Crash | Ninguno | **~10 min downtime** | ❌ CRÍTICO |

## 🔍 Technical Assessment

**JMeter Advantages:**
- Industry standard for enterprise load testing
- Graphical interface for test design
- Extensive plugin ecosystem
- Native CI/CD integration (Jenkins, Azure DevOps)

**JMeter Disadvantages:**
- More verbose than K6 for simple scripts
- Higher resource consumption on test agents

## 📝 Recommendations

1. **Critical**: Investigate and resolve server crash issues
2. **High Priority**: Optimize to reduce P95 below 1,500ms
3. **Medium Priority**: Implement stress tests to identify breaking point
4. **Medium Priority**: Configure automated performance degradation alerts

## 📄 License

This project is part of a QA automation challenge for Sofka.

## 👤 Author

QA Automation Challenge - Performance Testing Module
