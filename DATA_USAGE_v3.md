# Data structure and use: 29 October 2026 revision (v3)

This document describes the manuscript revision dataset v3. It contains schema and usage information, not participant records.

## Repository and version

The controlled dataset [OMIX022554](https://ngdc.cncb.ac.cn/omix/release/OMIX022554), linked to [PRJCA078013](https://ngdc.cncb.ac.cn/bioproject/browse/PRJCA078013), was released on 27 October 2026. The public page lists four controlled files and a “Request for this Data” application link. Released does not mean unrestricted download.

The v3 correction package dated 29 October 2026 has not replaced those released files. The existing fixed code archive [10.5281/zenodo.23642711](https://doi.org/10.5281/zenodo.23642711) remains the earlier v0.1.0-preparation release. A manuscript analysis must identify its input version and hashes; v3 results must not be reproduced by silently combining old and new files.

## Examination tables and keys

The resource has 1,814 participants and 2,392 examinations. Three wide tables have the same complete examination-key set:

| File | Rows | Columns | Role |
|---|---:|---:|---|
| examinations.csv | 2,392 | 115 | Direct and recorded values, timing and index flag |
| derived_measures.csv | 2,392 | 19 | Two keys and 17 recalculated measures |
| unresolved_source_fields.csv | 2,392 | 14 | Two keys and preserved source fields/qualifiers |

Join these tables on subject_id and record_id together. record_id is unique within each wide table. subject_id identifies repeated examinations from the same individual. Validate one-to-one key agreement before joining; do not join by row order.

is_index_record=1 identifies the 1,814 index examinations corresponding to sheet1. is_index_record=0 identifies 578 additional examinations in 349 participants, corresponding to sheet2. Index means the earliest reliably dated observed examination; if all dates are unavailable, the selected index record is flagged accordingly. It does not mean first-ever clinical contact.

The v3 dictionary contains 144 unique examination-level fields: 143 workbook fields plus is_index_record. Repeated keys across files are counted once. The earlier 143-field dictionary described the previous 142-field workbook plus that flag; v3 adds albumin_globulin_ratio_calc. Issue-table fields are not included in the 144-field count.

## Quality tables

quality_flags.csv contains 5,842 issue rows involving 1,788 examinations and 1,400 participants. variable, source_variable, issue_code and status describe the field, source token, issue and processing state. One examination can have multiple issue rows. Therefore, row count is neither examination count nor participant count.

Aggregate or filter issue rows before joining them to examination tables, and check that the join does not multiply examinations. value_withheld means the affected released value is missing; source_repair_recorded records a repair; review_or_provenance_flag marks review/provenance; source_issue_recorded preserves a source issue without asserting that the current recalculated value was withheld. Consult qc_codebook.csv for each issue. Absence of a flag does not establish measurement accuracy.

statistical_review_flags.csv contains 1,624 outer-3-IQR flags involving 861 examinations. These values remain in the main data. Such a flag is not an error diagnosis and does not invalidate an entire examination.

## Field names, units and timing

Names encode site, measurement stage and unit, for example brachial_d0_cm, tibial_d1_cm and creatinine_umol_l. The suffix _calc denotes a recalculated measure, _qualifier a comparison operator, and _source a preserved source definition requiring care.

visit_sequence is the within-person organizational order. visit_timing distinguishes dated/undated index examinations, later dated examinations, same-day extra readings and undated extra records. days_from_index stores observed relative day intervals. index_period is a five-year bin for the index date and cannot date every later examination. source_file_count and source_copy_count describe provenance coverage and collapsed source copies, not independent observations.

lipoprotein_a_mg_l is expressed in mg/L, as specified by the original column heading. Correcting its unit description did not change values. Units and definitions of unresolved source fields must be checked before transformation; do not assume that an ambiguously defined GFR field is indexed to body surface area or that urine albumin concentration is an albumin/creatinine ratio.

## Missing values and censoring

UTF-8 CSV empty fields indicate missing or withheld values, never zero. Numeric values retain their stored precision. A main numeric field must be interpreted with its corresponding qualifier: <, >, ≤, ≥, <= or >= indicates a bound; = denotes an exact value. A blank qualifier does not imply the main value is present.

No imputation, winsorization or cross-visit filling is introduced by exporting CSV, XLSX or XLS. Derivation code does not substitute a censoring bound for an exact input. Published statistical examples use pairwise exact complete observations for correlations and model-specific complete cases for regression.

## Recalculation and interpretation

Each vascular response is recalculated from its own examination: FMD = 100 × (D1 − D0)/D0; NID = 100 × (D2 − D0)/D0. Both sites retain separate D0, D1 and D2. D0 is the examination baseline and D2 follows sublingual nitroglycerin 0.5 mg. Full formulas and input requirements are in the dictionary and revision code.

Negative vascular responses are retained when computable. Operational curation limits are review rules, not clinical normal ranges. Definite source errors are corrected with provenance; unresolved suspicious values are withheld rather than guessed. Source/identity-level audit material remains restricted.

The repeat example uses one earliest–latest complete pair on distinct dates per participant (293 pairs). It is not a fixed follow-up schedule, intervention comparison or reliability experiment. Clinical-event outcomes and fully validated medication exposures are unavailable. Technical validation is exploratory and does not prove causality, vascular-bed superiority or clinical benefit.

## Access

Participant-level files require approved controlled access and applicable data-use agreements. Scientific/data-access contact: Liangdi Xie (ldxield@163.com). Public code and schema documentation grant no rights to participant records.
