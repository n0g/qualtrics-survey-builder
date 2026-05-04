# Markdown Survey Specification

This document defines the markdown format accepted by `convert.py`.

---

## File Structure

```
---
title: My Survey Title
language: EN
description: Optional description
---

# Block Name

## Question text [type]
- Choice 1
- Choice 2

---

# Another Block

## Another question [type]
```

---

## Frontmatter

YAML block at the top of the file (required for title, optional otherwise).

| Key | Default | Description |
|-----|---------|-------------|
| `title` | `Untitled Survey` | Survey name shown in Qualtrics |
| `language` | `EN` | Language code |
| `description` | `""` | Survey description (metadata only) |

---

## Blocks

Level-1 headings (`#`) define blocks (pages in Qualtrics). If no `#` headings are used, all questions go into a single default block.

```markdown
# Demographics

## Question 1 [mc]
...

# Feedback

## Question 2 [text]
```

---

## Questions

Level-2 headings (`##`) define questions. The type is specified in `[brackets]` at the end.

```markdown
## Question text here [type]
```

Add `*` after the type to make the question required:

```markdown
## What is your name? [text]*
```

---

## Question Types

### `[mc]` — Multiple Choice, Single Answer

Choices are listed as bullet points.

```markdown
## What is your age? [mc]
- Under 18
- 18–24
- 25–34
- 35–44
- 45 or older
```

### `[mc-multi]` — Multiple Choice, Multiple Answers

```markdown
## Which platforms do you use? [mc-multi]
- iOS
- Android
- Web
- Desktop
```

### `[mc-dropdown]` — Multiple Choice, Dropdown

```markdown
## Select your country [mc-dropdown]
- United States
- Germany
- Japan
- Other
```

### `[text]` — Single-Line Text Entry

No bullet points needed.

```markdown
## What is your email address? [text]
```

### `[text-essay]` — Multi-Line / Essay Text Entry

```markdown
## Please describe your experience [text-essay]
```

### `[matrix]` — Matrix / Likert Scale (single answer per row)

Specify the scale (columns) with a `scale:` line (comma-separated), then list rows as bullet points.

```markdown
## Rate the following features [matrix]
scale: Poor, Fair, Good, Excellent
- Ease of use
- Visual design
- Performance
- Documentation
```

### `[matrix-multi]` — Matrix, Multiple Answers per Row

Same syntax as `[matrix]`.

```markdown
## Which of the following apply? [matrix-multi]
scale: Never, Sometimes, Often, Always
- I use the mobile app
- I use the desktop app
- I use the API
```

### `[description]` — Descriptive Text (no input)

The question text is displayed as instructions. No choices.

```markdown
## Please read the following instructions carefully [description]
```

---

## Page Breaks

A `---` line inside a block inserts a page break between questions.

```markdown
# Block 1

## Question 1 [mc]
- Yes
- No

---

## Question 2 [text]
```

---

## Full Example

```markdown
---
title: Product Feedback Survey
language: EN
---

# About You

## How old are you? [mc]
- Under 18
- 18–24
- 25–34
- 35–44
- 45 or older

## What is your job role? [mc]
- Engineer
- Designer
- Manager
- Other

---

## How long have you used our product? [mc]
- Less than 1 month
- 1–6 months
- 6–12 months
- More than 1 year

# Product Experience

## Please rate the following aspects of our product [matrix]
scale: Very Poor, Poor, Neutral, Good, Excellent
- Ease of use
- Visual design
- Performance
- Documentation
- Customer support

## Which features do you use regularly? [mc-multi]
- Dashboard
- Reports
- Integrations
- API
- Mobile app

## What is the most important improvement we could make? [text-essay]

## Overall, how satisfied are you with our product? [mc]*
- Very dissatisfied
- Dissatisfied
- Neutral
- Satisfied
- Very satisfied
```

---

## Limitations

- Display logic / skip logic is not supported yet
- Scoring is not supported
- Choice randomization is not supported
- Multi-language questions are not supported
- Rich text in question text is not supported
