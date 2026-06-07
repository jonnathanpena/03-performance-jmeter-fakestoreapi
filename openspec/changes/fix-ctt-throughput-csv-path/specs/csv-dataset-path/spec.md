## ADDED Requirements

### Requirement: CSVDataSet filename defaults to project-root-relative path
The `CSVDataSet` element in `jmeter/test-plan.jmx` SHALL use `${__P(csvPath,jmeter/test-data/users.csv)}` as its `filename` value, so that the default path resolves correctly when JMeter is invoked from the project root without any additional `-J` properties.

#### Scenario: Test plan runs from project root without extra flags
- **WHEN** JMeter CLI is executed as `jmeter -n -t jmeter/test-plan.jmx -l results/results.jtl -e -o results/html-report/` from the project root
- **THEN** JMeter resolves `users.csv` at `jmeter/test-data/users.csv` and all 5 users are loaded without a file-not-found error

#### Scenario: CLI property override still works
- **WHEN** JMeter CLI is executed with `-JcsvPath=<custom-path>` pointing to an alternative CSV file
- **THEN** the `CSVDataSet` uses the overridden path, ignoring the default value

### Requirement: readme.txt documents CLI command without -JcsvPath workaround
`readme.txt` SHALL document the JMeter CLI execution command without the `-JcsvPath=jmeter/test-data/users.csv` override flag, and SHALL note that the command must be run from the project root.

#### Scenario: Operator follows readme CLI command
- **WHEN** an operator copies the CLI command from `readme.txt` and runs it from the project root
- **THEN** the test plan executes successfully and loads user data without modification or additional flags
