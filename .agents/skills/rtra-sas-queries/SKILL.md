---
name: rtra-sas-queries
description: Write, validate, debug, and interpret Statistics Canada Real Time Remote Access (RTRA) SAS queries. Use for RTRA requests, returned logs, output CSVs, or survey microdata tabulations.
---

# RTRA SAS Queries

Use this skill when writing or revising a Statistics Canada Real Time Remote
Access (RTRA) SAS program, diagnosing an RTRA return, or interpreting RTRA
output. Treat the returned log and the official RTRA data catalogue as the
source of truth. Do not guess a dataset name, variable type, weight, or
release rule.

## Required context

Establish these facts before writing a submission:

1. Survey and exact RTRA source dataset.
2. Time period and whether it is a calendar year, year to date, or pooled
   multi-month estimate.
3. Target population and exclusions.
4. Analysis variables, grouping variables, survey weight, and their types.
5. Requested outputs and their intended interpretation.

Use these sources in order:

1. The official RTRA data catalogue:
   `https://www.statcan.gc.ca/en/microdata/rtra/data`
2. The survey's current RTRA record layout and documentation.
3. A known successful RTRA program for the same survey and source.
4. The returned RTRA log, when debugging.

The log overrides assumptions. Do not repeat a failed pattern after the log
has identified it.

## Designing the query

Keep the program in this order:

1. Header: state purpose, source, time window, population, outputs, and
   definitions.
2. Base data step: read only required source variables, then filter the
   population and time period.
3. Derived variables: convert character values explicitly and calculate any
   derived measure.
4. Classification: create labels or subsets without duplicating observations
   within an input dataset.
5. One RTRA macro call per distinct result.

Use short, unique output names. RTRA output names are limited to 20
characters. The submission file name must begin with the survey tag required
by the source dataset.

### Generic mean template

Adapt all names and filters to the survey documentation.

```sas
data work.base;
     set RTRAdata.SURVEYTAG
          (keep = ID YEAR MONTH GROUPVAR ANALYSISVAR);

     if YEAR = 'YYYY';
     if POPULATION_CONDITION;

     analysis_value = input(ANALYSISVAR, 8.2);
run;

%RTRAMean(
     InputDataset = work.base,
     OutputName = output_name,
     ClassVarList = GROUPVAR,
     AnalysisVarList = analysis_value,
     UserWeight = WEIGHTVAR);
```

Use the actual source variable types. For example, a numeric provincial code
must not be quoted, while a character provincial code must be quoted.

SAS does not support chained mathematical comparisons. Write an age range as
`15 <= AGE and AGE <= 24`, not `15 <= AGE <= 24`.

## Separate sources and periods

Do not combine periods that reside in different RTRA source datasets. Write
separate submissions when the data catalogue assigns different source
datasets, even if the variables have the same names.

Label pooled results precisely:

- `January-December 2025` for a completed calendar year.
- `January-August 2026 year to date` for an incomplete current year.
- `June-August 2026 pooled estimate` for a three-month pooled microdata
  estimate.

Do not call an annualized weekly measure an observed annual wage. State:
`annualized weekly earnings = weekly earnings * 52`.

## LFS profile

Reconfirm the current catalogue before each use. The catalogue checked in
September 2026 lists:

| Time span | LFS RTRA source |
|---|---|
| 2021-2025 | `RTRAdata.LFS202125` |
| 2026-2030 | `RTRAdata.LFS202630` |

For the current LFS wage structure:

- `SYEAR` and `SMTH` are character variables.
- `PROV` is character. Alberta is `PROV = '48'`.
- `LFSSTAT in ('1', '2')` selects currently employed people.
- `HRLYEARN` and `WKLYEARN` are usual main-job earnings variables.
- `NAICS_5 =: '0311'` selects Food manufacturing. The leading zero matters.
- Convert earnings before estimation, for example:

```sas
hourly_wage = input(HRLYEARN, 8.2);
weekly_wage = input(WKLYEARN, 8.2);
if not missing(weekly_wage) then annualized_wage = weekly_wage * 52;
```

For this LFS source, preserve `ID` in the source `keep=` list and specify
`FINALWT` only through `UserWeight = FINALWT` in the RTRA macro. Do not add
`FINALWT` to the source `keep=` list unless the current documentation or
returned log explicitly says it is available there.

## RTRA macro safeguards

Before submission, check every macro input:

- IDs are unique within that input dataset.
- The same respondent is not deliberately stacked into all-industry and
  industry-subset records. Create distinct subset datasets instead.
- Each class variable has more than one distinct value.
- Output names are unique and 20 characters or fewer.
- The number of macro calls complies with the RTRA program limit.

For a true one-group total, do not use a constant label such as
`location = 'Alberta'` as the only class variable. RTRA rejects a class
variable with one unique value. Instead, use a natural multi-value grouping
such as month:

```sas
%RTRAMean(
     InputDataset = work.alberta_wages,
     OutputName = ab_all_wages,
     ClassVarList = SMTH,
     AnalysisVarList = hourly_wage weekly_wage annualized_wage,
     UserWeight = FINALWT);
```

This returns monthly rows and a blank `SMTH` row. The blank row is the pooled
total across the selected Alberta data. Confirm this interpretation against
the returned output before reporting it.

## Reading output correctly

RTRA typically includes an overall total row with a blank class value. That
row is the total for the program's input universe, not automatically a
provincial or national result.

For example, if a program retains Alberta economic regions plus selected
CMAs outside Alberta, the blank total is the combined selected universe. It
is not an Alberta total. Filter explicitly to the province to produce a
provincial estimate.

Keep unavailable estimates unavailable:

- A missing row means no released row was returned.
- A row with a weighted count but blank estimates is an unreleased or
  suppressed estimate.
- Do not impute, calculate from other groups, or label either case as zero.

## Debugging returned logs

Use the error text to make the smallest correct revision.

| Returned issue | Correct response |
|---|---|
| Source dataset not found | Check the catalogue, source name, and required filename tag. |
| Variable unavailable in `keep=` | Remove it from `keep=` or use the documented source variable. |
| Duplicate IDs | Split overlapping all-industry and subgroup data into separate macro inputs. |
| Output name too long | Shorten it to 20 characters or fewer. |
| Insufficient unique class values | Remove the constant class variable; use a natural multi-value class such as month if a total row is needed. |
| Character-to-numeric conversion note | Correct the comparison type, for example `PROV = '48'` for character `PROV`. |
| Blank released estimate | Report it as suppressed or unreleased; do not alter the microdata filter merely to force a value. |

After revision, re-read the complete returned log. A successful data step
does not prove the RTRA macro completed. Confirm a success message for every
requested macro call and confirm the expected CSV or SAS output files exist.

## Final validation checklist

Before handing a program to the user:

1. Verify the source dataset against the official catalogue.
2. Verify the program filename begins with the RTRA survey tag.
3. Compare variable names, types, and codes against the record layout.
4. Check the population definition against the request.
5. Check date filters and label incomplete years as year to date.
6. Check each macro input for unique IDs and valid class variables.
7. Check output names, macro count, and expected output files.
8. After return, read the log and inspect every output CSV for missing or
   suppressed groups before preparing a presentation table.
