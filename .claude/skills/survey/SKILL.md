---
description: Create and edit Qualtrics surveys using the markdown spec and converter. Use when the user wants to build, modify, or convert a survey.
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
---

# Qualtrics Survey Assistant

You are helping the user create or edit a Qualtrics survey using the markdown-to-QSF converter in this repository. The converter (`convert.py`) takes a `.md` file and produces a `.qsf` file ready to import into Qualtrics via **Create Project → Import a QSF File**.

$ARGUMENTS

## Your workflow

1. Identify the survey file to work on — check for `.md` files in the project (excluding README, SURVEY_SPEC, QSF_FORMAT, and example files).
2. Read `SURVEY_SPEC.md` for the full markdown syntax reference before making any edits.
3. Make the requested changes to the survey `.md` file.
4. Run the converter and fix any warnings before reporting back:
   ```bash
   source .venv/bin/activate && python src/convert.py your_survey.md
   ```
5. Regenerate the flow diagram:
   ```bash
   source .venv/bin/activate && python src/visualize.py your_survey.md
   ```
6. Elicit the behavioral model by asking the user these questions in one message:
   - What is the expected % split across screener branches (e.g. current / former / non-adopter)?
   - For each `[mc-multi]` question, how many choices do you expect the average respondent to select?
   - For each `[matrix]` scale, what is the expected mean response and which groups (if any) do you expect to score higher or lower?
   - Are there directional hypotheses linking constructs (e.g. "higher threat severity → higher adoption intent")?
   - Any other prior assumptions about the data (e.g. floor/ceiling effects, expected dropout points)?
7. Once the user answers, write their responses to `behavioral_model.yaml` next to the survey `.md` file using this structure:
   ```yaml
   # Behavioral model — pre-registration priors
   # Generated from survey: <survey filename>

   branches:
     <branch_name>: <expected proportion, e.g. 0.40>

   multi_select:
     <question_label>:
       mean_selections: <number>
       most_common: [<choice>, ...]

   scales:
     <question_label>:
       expected_mean: <1–7>
       group_differences: "<free text hypothesis>"

   hypotheses:
     - "<directional hypothesis>"

   notes: "<anything else>"
   ```
   Leave any field blank rather than inventing values the user did not provide.

## Key syntax rules

**Question heading:**
```
## Question text [type]* @label
```
- `*` makes it required
- `@label` lets other directives reference this question by name instead of counting QIDs manually

**Block heading:**
```
# Block Name
branch-if: @label/choice_number Selected
loop-from: @label
```

**Question-level directives** (placed immediately after the heading):
```
show-if: @label/choice_number Selected
carry-from: @label
```

**Choice annotations** (inline on bullet points):
```
- Option text [VARNAME=N]   ← recode value and variable name
- Other [+text]             ← enables inline text entry field
```

**Skip logic** (after choices):
```
skip-if: choice_number Selected → ENDOFBLOCK
skip-if: choice_number Selected → ENDOFSURVEY
skip-if: choice_number Selected → @label
```

## Question types

| Syntax | Description |
|--------|-------------|
| `[mc]` | Single-answer radio |
| `[mc-multi]` | Multi-answer checkboxes |
| `[mc-dropdown]` | Dropdown |
| `[rank]` | Drag-and-drop rank order |
| `[text]` | Single-line text entry |
| `[text-essay]` | Multi-line text entry |
| `[matrix]` | Likert matrix (one answer per row) — requires `scale:` line |
| `[matrix-multi]` | Likert matrix (multiple answers per row) |
| `[description]` | Descriptive text block (no input) |

## Label system

Assign a label to any question and reference it anywhere a `QIDn` is expected:

```markdown
## Are you subscribed? [mc]* @subscribed
- Yes
- No
skip-if: 1 Selected → ENDOFBLOCK

# Current Users
branch-if: @subscribed/1 Selected
```

## Loop & Merge

Repeats once per selected choice in the source question. Use `${lm://Field/1}` to pipe the current choice label into question text.

```markdown
## Who concerns you? [mc-multi]* @threat_actors
- Scammers
- Identity thieves

# Threat Details
loop-from: @threat_actors

## How would <strong>${lm://Field/1}</strong> harm you? [mc-multi]
- Phishing
- Physical harm
```

## Carry forward + Rank

```markdown
## Which concerns you most? [mc]*
carry-from: @threat_actors

## Rank your concerns [rank]*
carry-from: @threat_actors
```

## Current limitations

- Single condition only in branch/display/skip logic (no AND/OR)
- Loop blocks cannot be combined with `branch-if:`
- No choice randomization or scoring
