## Why

The JMeter test plan (`test-plan.jmx`) has two defects that cause incorrect behavior when executed from the project root via CLI: the `CSVDataSet` default path is relative to `test-data/users.csv` instead of `jmeter/test-data/users.csv`, causing JMeter to fail to find the users file unless a `-JcsvPath` override is passed manually; and the `ConstantThroughputTimer` (CTT) is placed outside the HTTP sampler's `<hashTree>`, making its scope ambiguous and potentially unreliable for enforcing the >= 20 TPS criterion.

## What Changes

- Fix `CSVDataSet` default `filename` from `test-data/users.csv` to `jmeter/test-data/users.csv` so the test runs correctly from the project root without requiring the `-JcsvPath` property override.
- Move the `ConstantThroughputTimer` inside the HTTP sampler's `<hashTree>` so it unambiguously applies per-request to `POST /auth/login`, and verify `calcMode` and `throughput` values match the >= 20 TPS criterion (1200 req/min).
- Update `readme.txt` to remove the `-JcsvPath` workaround from the documented CLI command, since the path will now be correct by default.

## Capabilities

### New Capabilities

- `csv-dataset-path`: Ensures the `CSVDataSet` filename resolves correctly from the project root, removing the need for a manual path override property at runtime.
- `ctt-placement-and-throughput`: Corrects the scope and placement of the `ConstantThroughputTimer` inside the HTTP sampler subtree and validates the throughput value enforces the >= 20 TPS acceptance criterion.

### Modified Capabilities

## Impact

- `jmeter/test-plan.jmx`: Two element modifications (CSVDataSet `filename` default value; CTT `<hashTree>` placement).
- `readme.txt`: Remove `-JcsvPath=jmeter/test-data/users.csv` from the recommended CLI command.
