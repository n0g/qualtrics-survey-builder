# QSF File Format Reference

Qualtrics Survey Format (QSF) is a proprietary JSON file. Qualtrics does not publish an official spec; this document is reverse-engineered from the [ctesta01 gist](https://gist.github.com/ctesta01/d4255959dace01431fb90618d1e8c241) and the [sumtxt/qsf R package](https://github.com/sumtxt/qsf).

**Confidence levels:** ✅ Confirmed from source code · ⚠️ Inferred / best-guess · ❓ Unknown

---

## Top-Level Structure

```json
{
  "SurveyEntry": { ... },
  "SurveyElements": [ ... ]
}
```

---

## SurveyEntry ✅

```json
{
  "SurveyID": "SV_xxxxxxxxxxxxxxx",
  "SurveyName": "My Survey",
  "SurveyDescription": "",
  "SurveyOwnerID": "UR_xxxxxxxxxxxxxxx",
  "SurveyBrandID": "qualtricssurvey",
  "DivisionID": null,
  "SurveyLanguage": "EN",
  "SurveyActiveResponseSet": "RS_xxxxxxxxxxxxxxx",
  "SurveyStatus": "Inactive",
  "SurveyStartDate": "0000-00-00 00:00:00",
  "SurveyExpirationDate": "0000-00-00 00:00:00",
  "SurveyCreationDate": "2026-05-01 12:00:00",
  "CreatorID": "UR_xxxxxxxxxxxxxxx",
  "LastModified": "2026-05-01 12:00:00",
  "LastAccessed": "0000-00-00 00:00:00",
  "LastActivated": "0000-00-00 00:00:00",
  "Deleted": null
}
```

**ID formats:**
- `SurveyID`: `SV_` + 15 alphanumeric chars
- `SurveyOwnerID` / `CreatorID`: `UR_` + 15 alphanumeric chars
- `SurveyActiveResponseSet`: `RS_` + 15 alphanumeric chars

---

## SurveyElements Array

Contains the following element types identified by the `Element` field. Each element follows this envelope:

```json
{
  "SurveyID": "SV_xxx",
  "Element": "<type>",
  "PrimaryAttribute": "...",
  "SecondaryAttribute": null,
  "TertiaryAttribute": null,
  "Payload": { ... }
}
```

### Known element types

| Element | Description | Payload type |
|---------|-------------|--------------|
| `BL` | Survey Blocks (pages) | Array of block objects |
| `FL` | Survey Flow | Object with `Flow` array |
| `SO` | Survey Options | Object |
| `SQ` | Survey Question | Object (one per question) |
| `RS` | Response Set | `null` |
| `PROJ` | Project metadata | Object |
| `STAT` | Survey statistics ⚠️ | Object |
| `QC` | Question count ⚠️ | `null` |
| `SCO` | Scoring ⚠️ | Object |

---

## BL — Survey Blocks ✅

```json
{
  "Element": "BL",
  "PrimaryAttribute": "Survey Blocks",
  "Payload": [
    {
      "Type": "Trash",
      "Description": "Trash / Unused Questions",
      "ID": "BL_TRASH",
      "BlockElements": []
    },
    {
      "Type": "Standard",
      "SubType": "",
      "Description": "Block name",
      "ID": "BL_xxxxxxxxxxxxxxx",
      "BlockElements": [
        { "Type": "Question", "QuestionID": "QID1" },
        { "Type": "Page Break" },
        { "Type": "Question", "QuestionID": "QID2" }
      ]
    }
  ]
}
```

- **Block ID format:** `BL_` + 15 alphanumeric chars (from R package `make_qid()`) ✅
- Trash block is required ⚠️
- `BlockElements` accepts `"Question"` and `"Page Break"` type entries ✅

---

## FL — Survey Flow ✅

```json
{
  "Element": "FL",
  "PrimaryAttribute": "Survey Flow",
  "Payload": {
    "Flow": [
      { "Type": "Block", "ID": "BL_xxx", "FlowID": "FL_2" },
      { "Type": "EndOfSurvey", "FlowID": "FL_3" }
    ],
    "Properties": { "Count": 3 },
    "FlowID": "FL_1",
    "Type": "Root"
  }
}
```

- Root flow has `FlowID: "FL_1"` and `Type: "Root"` ⚠️
- Each block entry gets a sequential `FlowID` ⚠️
- `EndOfSurvey` must be the last flow entry ⚠️
- `Properties.Count` = total number of FL entries including root ⚠️

---

## SO — Survey Options ⚠️

```json
{
  "Element": "SO",
  "PrimaryAttribute": "Survey Options",
  "Payload": {
    "BackButton": "false",
    "SaveAndContinue": "true",
    "SurveyProtection": "PublicSurvey",
    "BallotBoxStuffingPrevention": "false",
    "NoIndex": "Yes",
    "SecureResponseFiles": "true",
    "SurveyExpiration": "None",
    "SurveyTermination": "DefaultMessage",
    "Header": "",
    "Footer": "",
    "ProgressBarDisplay": "None",
    "PartialData": "+4 weeks",
    "ValidationMessage": "",
    "PreviousButton": "",
    "NextButton": "",
    "SurveyTitle": "My Survey",
    "SkinLibrary": "qualtrics",
    "SkinType": "templated",
    "Skin": { "brandingId": null, "templateId": "*base" },
    "NewScoring": 0
  }
}
```

Note: boolean-like values are strings (`"true"` / `"false"`), not JSON booleans. ✅

---

## SQ — Survey Question ✅

```json
{
  "Element": "SQ",
  "PrimaryAttribute": "QID1",
  "SecondaryAttribute": "First 99 chars of question text",
  "Payload": {
    "QuestionText": "Full question text",
    "DataExportTag": "Q1",
    "QuestionID": "QID1",
    "QuestionType": "MC",
    "Selector": "SAVR",
    "SubSelector": "TX",
    "Configuration": {
      "QuestionDescriptionOption": "UseText"
    },
    "QuestionDescription": "First 99 chars of question text",
    "Choices": {
      "1": { "Display": "Option A" },
      "2": { "Display": "Option B" }
    },
    "ChoiceOrder": [1, 2],
    "Validation": {
      "Settings": {
        "ForceResponse": "OFF",
        "ForceResponseType": "OFF",
        "Type": "None"
      }
    },
    "Language": []
  }
}
```

- `QuestionID` format: `QID` + integer (e.g. `QID1`, `QID2`) ✅
- `DataExportTag` defaults to `Q` + integer ✅
- `Language` is an empty array for single-language surveys ✅

### Question Types & Selectors

| Markdown type | QuestionType | Selector | SubSelector |
|---------------|-------------|----------|-------------|
| `mc` | `MC` | `SAVR` | `TX` |
| `mc-multi` | `MC` | `MAVR` | `TX` |
| `mc-dropdown` | `MC` | `DL` | `TX` |
| `text` | `TE` | `SL` | — |
| `text-essay` | `TE` | `ESTB` | — ⚠️ |
| `matrix` | `Matrix` | `Likert` | `SingleAnswer` |
| `matrix-multi` | `Matrix` | `Likert` | `MultipleAnswer` |
| `description` | `DB` | `TB` | — |

**Selector codes:**
- `SAVR` = Single Answer Vertical Radio ✅
- `SAHR` = Single Answer Horizontal Radio ⚠️
- `MAVR` = Multiple Answer Vertical (checkboxes) ✅
- `MAHR` = Multiple Answer Horizontal ⚠️
- `DL` = Dropdown List ⚠️
- `SL` = Single Line text entry ✅
- `ESTB` = Essay Text Box ⚠️ (may be `ML` or `MLT`)
- `Likert` = Matrix/Likert selector ✅
- `TB` = Text / Descriptive block ✅
- `TX` = Sub-selector for text responses ✅

### Matrix Question Payload ✅

```json
{
  "QuestionType": "Matrix",
  "Selector": "Likert",
  "SubSelector": "SingleAnswer",
  "Choices": {
    "1": { "Display": "Row 1" },
    "2": { "Display": "Row 2" }
  },
  "ChoiceOrder": [1, 2],
  "Answers": {
    "1": { "Display": "Scale point 1" },
    "2": { "Display": "Scale point 2" }
  },
  "AnswerOrder": [1, 2]
}
```

Note: For Matrix, `Choices` = rows (statements), `Answers` = columns (scale) ✅

---

## RS — Response Set ⚠️

```json
{
  "Element": "RS",
  "PrimaryAttribute": "RS_xxxxxxxxxxxxxxx",
  "SecondaryAttribute": "Default Response Set",
  "Payload": null
}
```

---

## PROJ — Project Metadata ⚠️

```json
{
  "Element": "PROJ",
  "PrimaryAttribute": "ProjectCategory",
  "TertiaryAttribute": "1.1.0",
  "Payload": {
    "ProjectCategory": "CORE",
    "SchemaVersion": "1.1.0"
  }
}
```

---

## QC — Question Count ⚠️

```json
{
  "Element": "QC",
  "PrimaryAttribute": "Survey Question Count",
  "SecondaryAttribute": "5",
  "Payload": null
}
```

`SecondaryAttribute` is the total question count as a string.

---

## Known Unknowns

- ❓ Exact validation for essay text entry selector (`ESTB` vs `ML` vs `MLT`)
- ❓ Whether the Trash block is strictly required or optional
- ❓ Exact `STAT` element structure
- ❓ Whether `SCO` element is required for import
- ❓ Required vs optional fields in `SurveyEntry`
- ❓ Display logic / skip logic structure (`add_skiplogic.R` exists in R package)
- ❓ Randomization of choices
- ❓ Multi-language survey structure
