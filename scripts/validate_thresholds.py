import csv
import os
import statistics
import sys

THROUGHPUT_THRESHOLD = 20     # TPS mínimo aceptable
P95_THRESHOLD = 1500          # ms máximo aceptable en P95
ERROR_RATE_THRESHOLD = 3.0    # % máximo aceptable de error rate


def parse_jtl(filepath):
    if not os.path.isfile(filepath):
        print(f"ERROR: Archivo no encontrado: {filepath}")
        sys.exit(1)

    elapsed_values = []
    success_values = []
    timestamps = []

    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            elapsed_values.append(int(row['elapsed']))
            success_values.append(row['success'].strip().lower() == 'true')
            timestamps.append(int(row['timeStamp']))

    if not elapsed_values:
        print("ERROR: El archivo JTL no contiene filas de datos.")
        sys.exit(1)

    return elapsed_values, success_values, timestamps


def calculate_throughput(timestamps, total_requests):
    duration_ms = max(timestamps) - min(timestamps)
    if duration_ms == 0:
        return float('inf')
    duration_seconds = duration_ms / 1000.0
    return total_requests / duration_seconds


def calculate_p95(elapsed_values):
    return statistics.quantiles(elapsed_values, n=100)[94]


def calculate_error_rate(success_values):
    failed = sum(1 for s in success_values if not s)
    return (failed / len(success_values)) * 100


def main():
    if len(sys.argv) < 2:
        print("Uso: validate_thresholds.py <ruta_al_results.jtl>")
        sys.exit(1)

    filepath = sys.argv[1]
    elapsed_values, success_values, timestamps = parse_jtl(filepath)

    total_requests = len(elapsed_values)
    throughput = calculate_throughput(timestamps, total_requests)
    p95 = calculate_p95(elapsed_values)
    error_rate = calculate_error_rate(success_values)

    failures = []

    print("=" * 55)
    print("  Reporte de Validación de Umbrales de Performance")
    print("=" * 55)

    tps_status = "PASS" if throughput >= THROUGHPUT_THRESHOLD else "FAIL"
    print(f"Throughput  : {throughput:.2f} TPS  (umbral: >= {THROUGHPUT_THRESHOLD} TPS)  [{tps_status}]")
    if throughput < THROUGHPUT_THRESHOLD:
        failures.append(f"Throughput {throughput:.2f} TPS < {THROUGHPUT_THRESHOLD} TPS")

    p95_status = "PASS" if p95 <= P95_THRESHOLD else "FAIL"
    print(f"P95 Latencia: {p95:.0f} ms    (umbral: <= {P95_THRESHOLD} ms)  [{p95_status}]")
    if p95 > P95_THRESHOLD:
        failures.append(f"P95 {p95:.0f} ms > {P95_THRESHOLD} ms")

    er_status = "PASS" if error_rate < ERROR_RATE_THRESHOLD else "FAIL"
    print(f"Error Rate  : {error_rate:.2f}%    (umbral: <  {ERROR_RATE_THRESHOLD}%)   [{er_status}]")
    if error_rate >= ERROR_RATE_THRESHOLD:
        failures.append(f"Error rate {error_rate:.2f}% >= {ERROR_RATE_THRESHOLD}%")

    print("=" * 55)
    print(f"Total de requests: {total_requests}")

    if failures:
        print("\nUmbrales INCUMPLIDOS:")
        for f in failures:
            print(f"  - {f}")
        print("\nResultado: FAIL")
        sys.exit(1)
    else:
        print("\nResultado: PASS — Todos los umbrales cumplidos.")
        sys.exit(0)


if __name__ == "__main__":
    main()
