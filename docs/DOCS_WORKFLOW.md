# Documentation & Coverage Automation Workflow

This guide details the automated workflow commands used in `scarajectory` for rapid documentation and coverage generation.

---

## 🚀 Key Commands

### 1. Regenerate Sphinx `.rst` Architecture Files
When new modules, interfaces, or factories are added or deleted, regenerate the Sphinx `.rst` API documentation files from the `docs/` directory:

```bash
cd docs
sphinx_doc ../scarajectory
```

> **Note:** `sphinx_doc` is an environment alias that invokes:
> `sphinx-apidoc -P -f -e -a -o source/ ../scarajectory/ ...`
> with automatic exclusion of tests and internal scripts.

---

### 2. Auto-Update README & Index Architecture Trees and Coverage Tables
To run test coverage, generate coverage metrics, and automatically rebuild:
- Directory trees in `README.md` and `docs/source/index.rst`
- Coverage tables in `README.md` and `docs/source/coverage_table.csv`
- Pylint quality report in `scarajectory.report`

Execute from the repository root:

```bash
./run_coverage.sh
```

---

### 3. Build Sphinx HTML Documentation
To build the HTML documentation from updated `.rst` files:

```bash
make -C docs html
```
The output HTML is located at `docs/build/html/index.html`.
