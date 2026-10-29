# Vascular function data: documentation and reproducible code

This repository contains schema documentation, quality definitions, reproducible code and entirely synthetic examples. It contains no participant-level records.

## Dataset access

The vascular-function dataset was released by OMIX on **27 October 2026** under [OMIX022554](https://ngdc.cncb.ac.cn/omix/release/OMIX022554), linked to [BioProject PRJCA078013](https://ngdc.cncb.ac.cn/bioproject/browse/PRJCA078013). The resource describes 1,814 participants and 2,392 examinations collected between 1 August 2000 and 6 June 2016. It includes brachial and anterior tibial vascular measurements, related clinical phenotypes and irregular repeat examinations.

Access is **Controlled-access**. Apply through “Request for this Data” on the OMIX record; approved use remains subject to the applicable data-use agreement. There is no unrestricted participant-data download. The retrospective study has ethics approval with a waiver of informed consent, and hospital approval for controlled sharing of the described population. Individual written data-sharing consent is not claimed. See [ACCESS.md](ACCESS.md).

## Version-specific documentation

- [Data structure and usage for the v3 manuscript revision](DATA_USAGE_v3.md): keys and joins, field naming, index/repeat records, units, missing values, censoring and quality-table interpretation.
- [Measurement protocol](protocol.md) and [data dictionary](data_dictionary.csv).

The v3 correction package dated 29 October 2026 is a manuscript-revision package and has **not replaced the released OMIX files**. DATA_USAGE_v3.md describes that revision explicitly. The root code and dictionary remain those of the earlier preparation release unless separately versioned. Do not combine versions by row order or assume that the fixed archive contains the new analyses.

The fixed code release is archived at [10.5281/zenodo.23642711](https://doi.org/10.5281/zenodo.23642711), corresponding to [v0.1.0-preparation](https://github.com/hxd0012-gif/fmd-data-descriptor/releases/tag/v0.1.0-preparation) and commit 63a1bb6263ac6d35b18eb165add60a24cde6c333. Main-branch documentation can be updated; the original tag and fixed archive remain unchanged.

## Run the existing synthetic example

    python recompute.py synthetic_example.csv synthetic_recomputed.csv
    python validate.py synthetic_example.csv synthetic_expected.csv
    python make_figures.py synthetic_example.csv figures/synthetic_availability

Python 3.10 or later is required; the optional existing plotting example requires matplotlib. Synthetic rows are hand-constructed arithmetic examples and are not sampled or perturbed participant records.

With authorized data matching this code version:

    python validate.py examinations.csv derived_measures.csv --extension unresolved_source_fields.csv

This code verifies keys, formulas and missingness; it does not recreate private identity linkage or independently adjudicate source errors. MIT applies to the code/documentation and grants no rights to participant data.
