## Context

`jmeter/test-plan.jmx` contains two structural defects introduced during initial authoring:

1. **CSVDataSet path** (`filename`): Currently `${__P(csvPath,test-data/users.csv)}`. When running JMeter CLI from the project root (the documented workflow), the default resolves to `test-data/users.csv`, which does not exist at that working directory. The file lives at `jmeter/test-data/users.csv`. The plan was only executable by manually passing `-JcsvPath=jmeter/test-data/users.csv` at the command line.

2. **ConstantThroughputTimer (CTT) placement**: The CTT element sits inside the ThreadGroup's `<hashTree>` as a sibling of the `HTTPSamplerProxy` (lines 171–182 of the JMX), not inside the sampler's own `<hashTree>`. In JMeter's XML model, a timer placed inside a sampler's `<hashTree>` unambiguously applies to that sampler; as a sibling it applies to the ThreadGroup scope but its per-sampler semantics become ambiguous if additional samplers are added later.

Both issues do not require architectural changes—only targeted XML edits to the `.jmx` and a one-line update to `readme.txt`.

## Goals / Non-Goals

**Goals:**
- Change the `CSVDataSet` default `filename` to `jmeter/test-data/users.csv` so the test executes correctly from the project root with no extra flags.
- Relocate the `ConstantThroughputTimer` inside the `HTTPSamplerProxy`'s `<hashTree>` to make its scope explicit and deterministic.
- Remove the `-JcsvPath` override from the documented CLI command in `readme.txt`.

**Non-Goals:**
- Changing thread count (40), ramp-up (30 s), or duration (120 s) variables.
- Modifying the CTT `throughput` value (1200.0 req/min = 20 TPS) or `calcMode` (1 = all threads in group)—these are already correct.
- Altering any assertions (Status 200, DurationAssertion, Token body assertion).
- Changing the `${__P(csvPath,...)}` property-override mechanism itself; only its default value changes.

## Decisions

### 1. Keep `${__P(csvPath,...)}` pattern, change only the default

**Decision:** Update the default in `${__P(csvPath,jmeter/test-data/users.csv)}` rather than hard-coding a plain string.

**Rationale:** Preserving the property function retains CLI override flexibility (e.g., CI pipelines can still pass `-JcsvPath=...` for alternative data sets). Hard-coding would remove that escape hatch with no benefit.

**Alternative considered:** Replace with a plain string `jmeter/test-data/users.csv`. Rejected because it removes runtime overridability without any gain.

### 2. Move CTT inside the `HTTPSamplerProxy` `<hashTree>`

**Decision:** Cut the `<ConstantThroughputTimer>` element and its following `<hashTree/>` from the ThreadGroup level and paste them inside the `HTTPSamplerProxy`'s `<hashTree>`, after the existing assertions.

**Rationale:** JMeter evaluates timers inside a sampler's `<hashTree>` before each execution of that sampler. This is the canonical placement for a timer targeting a single sampler. With only one sampler in the plan, the runtime behavior is identical today, but the correct placement prevents scope ambiguity if the plan is extended and makes the intent self-documenting in the XML.

**Alternative considered:** Leave the CTT at ThreadGroup level. Rejected because the proposal explicitly identifies this as a defect and the ThreadGroup-level placement makes the CTT's relationship to the sampler implicit rather than structural.

### 3. `calcMode = 1` is retained as-is

**Decision:** Keep `calcMode=1` ("all active threads in current thread group").

**Rationale:** This mode distributes the 1200 req/min cap across all 40 threads, which is the correct behavior to enforce a global >= 20 TPS floor for the thread group. `calcMode=0` (per-thread) would allow each thread to fire at 1200/min independently, producing up to 48000 req/min—not the intent.

## Risks / Trade-offs

- **Path assumption** → The new default `jmeter/test-data/users.csv` is relative to the JMeter working directory. If JMeter is invoked from a directory other than the project root, the path will still not resolve. Mitigation: `readme.txt` will document that the CLI command must be run from the project root.

- **CTT move has no runtime impact today** → Because there is only one sampler in the plan, moving the CTT does not change measured throughput. The risk is cosmetic regression if someone compares JMX snapshots; the diff is intentional and covered by this change record.

- **Property override still works** → Any script or CI job currently passing `-JcsvPath=jmeter/test-data/users.csv` will continue to work after the fix (the property value overrides the now-correct default). No breakage expected.
