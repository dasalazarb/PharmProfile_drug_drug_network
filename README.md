# PharmProfile Drug-Drug Network

This repository contains a single Python script, `drug_drug_interact_cic.py`, that ingests medication schedules from Excel, constructs an XML representation of patient–date–drug relationships, and enumerates drug combinations across multiple time windows. It also supports a basic lookup of interactions in a DrugBank XML export for a user-provided list of drugs.

## Features
- **Schedule ingestion from Excel**: Reads a worksheet containing date, time, patient identifier, and medication columns and converts each row into a timestamped medication event.
- **XML generation**: Builds a hierarchical `drug.xml` file organized by patient, administration date, and medication, ready for downstream inspection.
- **Time-window combination analysis**: Calculates medication pairs administered to the same patient within 6-hour, same-day (24-hour), and 48-hour windows.
- **DrugBank interaction search**: Optionally scans a DrugBank XML file using a list of drugs of interest and saves matching interaction descriptions.

## Inputs
- **Excel schedule**: Defaults to `Med_vs_Tiempo.xlsx` with sheet name `Med_vs_Tiempo (5)`. The first four columns must contain date, time, patient ID, and medications (multiple drugs separated by underscores), respectively.
- **DrugBank XML**: Defaults to `drugbank_2.xml`. Only required if you want interaction lookups.
- **Profile list**: Plain-text file (default `lista_med_cic.txt`) with one drug name per line to match against DrugBank.
- **Output directory**: Defaults to the current directory but can be redirected.

## Output artifacts
Running the script produces several files inside the chosen output directory:
- `drug.xml`: XML tree of patients, timestamps, and administered drugs.
- `combinaciones_6_noSorted.txt`: Unsorted drug pairs within ±6 hours.
- `combinaciones_24h_noSorted.txt`: Unsorted drug pairs given on the same calendar day.
- `combinaciones_48_noSorted.txt`: Unsorted drug pairs exactly 48 hours apart.
- `intreacciones_cic_no_depurado.txt`: Raw same-day drug pairs per patient/date.
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
The script exposes a CLI with sensible defaults. A typical run with all default paths:
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

### Expected workflow
1. Prepare the Excel schedule with the required columns (date, time, patient, medications separated by underscores).
2. Run the script to generate `drug.xml` and the combination lists in your chosen output directory.
3. (Optional) Provide a profile list and DrugBank XML to create `interacciones_drugbank.txt` with matched interaction descriptions.

## Logging and robustness
- Logging verbosity is controlled via `--log-level` (DEBUG, INFO, WARNING, ERROR, CRITICAL).
- Rows with unparsable dates or times are skipped gracefully with warnings to keep processing moving.
- Missing DrugBank or profile files disable interaction export without stopping the main pipeline.

## Repository structure
```
PharmProfile_drug_drug_network/
├── drug_drug_interact_cic.py   # Main script with all processing logic
├── Interact_Detect/            # Supporting assets (if provided)
└── Drug_drug_interaction - DatosyGuaros.pdf  # Reference document (Spanish)
```

## Support
For questions about the pipeline or data formats, review the inline docstrings and logging output in `drug_drug_interact_cic.py`. The script is self-contained and can be invoked directly with the commands above.
