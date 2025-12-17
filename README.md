# PharmProfile Drug-Drug Network

This repository contains two related Python scripts for drug–drug interaction analysis:

- `drug_drug_interact_cic.py`: CLI-friendly pipeline that ingests medication schedules from Excel, builds an XML representation of patient–date–drug relationships, and enumerates drug combinations across multiple time windows. It also supports a DrugBank lookup for a user-provided list of drugs.
- `Interact_Detect.py`: Modernized version of the original `Interact_Detect` script with clearer defaults, input validation, and a `main()` entry point while preserving the legacy outputs (drug XML, combination lists, and DrugBank matches).

## Features
Both scripts share core functionality:

- **Schedule ingestion from Excel**: Reads a worksheet containing date, time, patient identifier, and medication columns and converts each row into a timestamped medication event.
- **XML generation**: Builds a hierarchical `drug.xml` file organized by patient, administration date, and medication, ready for downstream inspection.
- **Time-window combination analysis**: Calculates medication pairs administered to the same patient within 6-hour, same-day (24-hour), and 48-hour windows.
- **DrugBank interaction search**: Optionally scans a DrugBank XML file using a list of drugs of interest and saves matching interaction descriptions.

## Inputs
Both scripts use the same defaults:

- **Excel schedule**: Defaults to `Med_vs_Tiempo.xlsx` with sheet name `Med_vs_Tiempo (5)`. The first four columns must contain date, time, patient ID, and medications (multiple drugs separated by underscores), respectively.
- **DrugBank XML**: Defaults to `drugbank_2.xml`. Only required if you want interaction lookups.
- **Profile list**: Plain-text file (default `lista_med_cic.txt`) with one drug name per line to match against DrugBank.
- **Output directory**: Defaults to the current directory but can be redirected.

## Output artifacts
`drug_drug_interact_cic.py` produces unsorted lists that mirror the historical workflow:

- `drug.xml`: XML tree of patients, timestamps, and administered drugs.
- `combinaciones_6_noSorted.txt`: Unsorted drug pairs within ±6 hours.
- `combinaciones_24h_noSorted.txt`: Unsorted drug pairs given on the same calendar day.
- `combinaciones_48_noSorted.txt`: Unsorted drug pairs exactly 48 hours apart.
- `intreacciones_cic_no_depurado.txt`: Raw same-day drug pairs per patient/date.
- `interacciones_drugbank.txt`: DrugBank interaction matches (only created when both profile list and DrugBank XML are available).

`Interact_Detect.py` emits deduplicated lists by default, aligning with the legacy script names:

- `drug.xml`: XML tree of patients, timestamps, and administered drugs.
- `combinaciones_24h.txt`: Unique drug pairs within the same calendar day.
- `combinaciones_48h.txt`: Unique drug pairs exactly 48 hours apart (includes same-day pairs).
- `combinaciones_6h.txt`: Unique drug pairs within a ±6-hour window.
- `interacciones_drugbank.txt`: DrugBank interaction matches (only created when both profile list and DrugBank XML are available).

## Installation
1. Use Python 3.10+ and create/activate a virtual environment if desired.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   If a requirements file is unavailable, install `openpyxl` directly:
   ```bash
   pip install openpyxl
   ```

## Usage
`drug_drug_interact_cic.py` exposes a CLI with sensible defaults. A typical run with all default paths:
```bash
python drug_drug_interact_cic.py
```

Specify custom files and output locations as needed:
```bash
python drug_drug_interact_cic.py \
    --excel path/to/schedule.xlsx \
    --sheet "Sheet1" \
    --output-dir outputs/ \
    --drugbank path/to/drugbank.xml \
    --profile path/to/drug_list.txt \
    --log-level DEBUG
```

`Interact_Detect.py` provides similar arguments (replace `--log-level` with `--verbose`):
```bash
python Interact_Detect.py \
    --excel path/to/schedule.xlsx \
    --sheet "Sheet1" \
    --output-dir outputs/ \
    --drugbank path/to/drugbank.xml \
    --profile path/to/drug_list.txt \
    --verbose
```

### Expected workflow
1. Prepare the Excel schedule with the required columns (date, time, patient, medications separated by underscores).
2. Run the script to generate `drug.xml` and the combination lists in your chosen output directory.
3. (Optional) Provide a profile list and DrugBank XML to create `interacciones_drugbank.txt` with matched interaction descriptions.

## Logging and robustness
- Logging verbosity is controlled via `--log-level` (for `drug_drug_interact_cic.py`) or `--verbose` (for `Interact_Detect.py`).
- Rows with unparsable dates or times are skipped gracefully with warnings to keep processing moving.
- Missing DrugBank or profile files disable interaction export without stopping the main pipeline.

## Repository structure
```
PharmProfile_drug_drug_network/
├── drug_drug_interact_cic.py   # CLI pipeline with unsorted outputs
├── Interact_Detect.py          # Modernized legacy script with deduplicated outputs
└── Drug_drug_interaction - DatosyGuaros.pdf  # Reference document (Spanish)
```

## Support
For questions about the pipeline or data formats, review the inline docstrings and logging output in `drug_drug_interact_cic.py`. The script is self-contained and can be invoked directly with the commands above.
