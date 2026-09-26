# Documentation & Coverage Workflow Guidelines

For fast documentation and coverage regeneration in `scarajectory`, use the provided automated scripts and aliases:

1. **Sphinx API Doc Generation:**
   To regenerate all Sphinx `.rst` module and package documentation files:
   ```bash
   cd docs && sphinx_doc ../scarajectory
   ```

2. **Automated Tree & Coverage Updates:**
   Do NOT manually edit directory tree ASCII diagrams or coverage tables in `README.md`, `docs/source/index.rst`, or `docs/source/coverage_table.csv`. Instead, run:
   ```bash
   ./run_coverage.sh
   ```
   This script runs `coverage/ats_coverage.py scarajectory` which automatically runs tests, computes line coverage, and updates `README.md`, `docs/source/index.rst`, and `docs/source/coverage_table.csv`.

3. **Sphinx HTML Build:**
   ```bash
   make -C docs html
   ```
