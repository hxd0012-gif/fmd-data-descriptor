# Vascular function data: documentation and reproducible code

Version 0.1.0-preparation, 25 October 2026.

This repository contains a data dictionary, quality codebook, deterministic recomputation code and entirely synthetic examples for a retrospective vascular function resource. It contains no participant-level records. The local preparation baseline contains 1,814 participants and 2,392 examinations collected within the author-confirmed window 1 August 2000 to 6 June 2016; these are provisional preparation counts, not the size of an approved shared release.

Participant-level data are planned for OMIX controlled access, subject to institutional approval, eligibility review and verification of the access route. No OMIX accession or data DOI has been issued for this project. See [ACCESS.md](ACCESS.md). The code archive DOI is also pending.

## Run the synthetic example

```sh
python recompute.py synthetic_example.csv synthetic_recomputed.csv
python validate.py synthetic_example.csv synthetic_expected.csv
python make_figures.py synthetic_example.csv figures/synthetic_availability
```

Python 3.10 or later is required. Only the optional plotting script requires matplotlib. Synthetic rows are hand-constructed arithmetic examples and are not sampled, perturbed or estimated from patient records. Cases include a missing response diameter, a zero baseline diameter, a censored baseline measurement and an explicit exact-value qualifier.

## Controlled file schema

`examinations.csv` has one row per examination and includes `subject_id`, `record_id`, and `is_index_record`. `derived_measures.csv` contains the same keys and 16 calculated measures. `unresolved_source_fields.csv` preserves source measurements with unresolved units or definitions and their qualifiers. `quality_flags.csv` has one row per recorded issue. Join examination-level tables using both keys. CSV is UTF-8; empty fields indicate missing or withheld values, never zero. Numeric values retain their stored precision.

With authorized data, run `python validate.py examinations.csv derived_measures.csv --extension unresolved_source_fields.csv`. The extension join is explicit and checks exact key agreement. A bound qualifier (`<`, `>`, `≤`, `≥`, `<=`, `>=`) suppresses calculations that require an exact input; `=` denotes an exact value. No imputation, winsorization, cross-visit filling or modeling transformation is applied to the shared master data.

In the long quality table, `variable` refers to the released field when a match exists and `source_variable` preserves the source field token. A blank released field token indicates an issue on a field that is not released. `value_withheld` means the affected released value is missing; `source_issue_recorded` preserves a source problem without asserting that a recomputed released value was withheld. Other statuses distinguish a recorded repair from a review or provenance flag. Every token from the original quality string is retained.

The code recomputes the measures in the prepared dataset. It does not recreate private identity linkage, recover source values or adjudicate source errors. The optional availability plot is an inspectable usage example; it does not claim to reproduce every manuscript figure. Consult [protocol.md](protocol.md) and [data_dictionary.csv](data_dictionary.csv) before analysis.

MIT applies to the code and documentation in this repository. It grants no rights to participant data, which require a separate institutionally approved data-use agreement.
