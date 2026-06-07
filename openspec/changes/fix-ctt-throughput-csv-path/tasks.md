## 1. Fix CSVDataSet filename default

- [x] 1.1 Open `jmeter/test-plan.jmx` and locate the `CSVDataSet` element's `filename` `stringProp`
- [x] 1.2 Replace the current value `${__P(csvPath,test-data/users.csv)}` with `${__P(csvPath,jmeter/test-data/users.csv)}`
- [x] 1.3 Save `test-plan.jmx` and confirm the only changed line is the `filename` `stringProp`

## 2. Move ConstantThroughputTimer inside HTTPSamplerProxy hashTree

- [x] 2.1 In `jmeter/test-plan.jmx`, locate the `ConstantThroughputTimer` element and its following `<hashTree/>` at the ThreadGroup level (sibling of `HTTPSamplerProxy`)
- [x] 2.2 Cut the `<ConstantThroughputTimer>` block and its closing `</ConstantThroughputTimer>` tag together with the immediately following `<hashTree/>` line
- [x] 2.3 Paste the cut block inside the `<hashTree>` that is the direct child of the `HTTPSamplerProxy` element, after the last assertion element (`</hashTree>` closing the assertions)
- [x] 2.4 Verify `throughput` is `1200.0` and `calcMode` is `1` remain unchanged after the move
- [x] 2.5 Save `test-plan.jmx` and confirm XML structure is well-formed (no duplicate or mismatched tags)

## 3. Update readme.txt CLI command

- [x] 3.1 Open `readme.txt` and locate the documented JMeter CLI execution command
- [x] 3.2 Remove the `-JcsvPath=jmeter/test-data/users.csv` flag from the command
- [x] 3.3 Confirm the updated command reads `jmeter -n -t jmeter/test-plan.jmx -l results/results.jtl -e -o results/html-report/` and notes it must be run from the project root

## 4. Verify fixes

- [x] 4.1 Run `jmeter -n -t jmeter/test-plan.jmx -l results/results.jtl -e -o results/html-report/` from the project root and confirm JMeter loads `users.csv` without a file-not-found error
- [x] 4.2 Inspect the generated `results/results.jtl` or JMeter console output to confirm all 5 users were parametrized and requests fired
- [x] 4.3 Open the HTML report (`results/html-report/index.html`) and verify throughput is >= 20 TPS and error rate < 3%
