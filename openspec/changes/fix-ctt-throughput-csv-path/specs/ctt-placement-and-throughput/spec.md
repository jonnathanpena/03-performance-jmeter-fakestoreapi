## ADDED Requirements

### Requirement: ConstantThroughputTimer is placed inside the HTTPSamplerProxy hashTree
The `ConstantThroughputTimer` element in `jmeter/test-plan.jmx` SHALL be located inside the `<hashTree>` that is the direct child of the `HTTPSamplerProxy` element for `POST /auth/login`, not as a sibling of the sampler at the ThreadGroup level.

#### Scenario: CTT is a child of the sampler subtree in JMX XML structure
- **WHEN** the `test-plan.jmx` file is parsed
- **THEN** the `ConstantThroughputTimer` element and its following `<hashTree/>` appear inside the `<hashTree>` that follows the `HTTPSamplerProxy` element, after the existing assertion elements

#### Scenario: CTT scope is deterministic with a single sampler
- **WHEN** JMeter executes the test plan with 40 threads
- **THEN** the CTT unambiguously governs only the `POST /auth/login` sampler, and throughput is capped at 1200 req/min across all active threads

### Requirement: ConstantThroughputTimer enforces >= 20 TPS acceptance criterion
The `ConstantThroughputTimer` SHALL have `throughput` set to `1200.0` (requests per minute) and `calcMode` set to `1` (all active threads in current thread group), enforcing the >= 20 TPS global throughput floor for the ThreadGroup.

#### Scenario: Throughput value matches 20 TPS criterion
- **WHEN** the `test-plan.jmx` file is inspected
- **THEN** the `ConstantThroughputTimer` has `throughput` equal to `1200.0` and `calcMode` equal to `1`

#### Scenario: Per-thread throughput does not exceed intended global cap
- **WHEN** JMeter executes the test plan with 40 active threads
- **THEN** the total request rate across all threads is capped at 1200 req/min (20 TPS), not 1200 req/min per thread
