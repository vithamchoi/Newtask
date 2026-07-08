# Additional Evidence Corpus Release Reviews

This file adds five further target-user/expert reviews for the Evidence Corpus
paper and release plan.

## EC-DATASETCURATOR-03

**Role:** dataset curator / research data librarian  
**Experience:** 9 years supporting open research datasets  
**Feedback lens:** metadata, repository readiness, citation, and reuse

### Ratings

| Dimension | Rating |
|---|---:|
| Dataset documentation readiness | 3/5 |
| Reuse value | 5/5 |
| Schema clarity | 4/5 |
| Citation/repository readiness | 3/5 |
| Maintenance plan clarity | 2/5 |

### Required Before Release

- DOI-minted repository record.
- `README.md` with quick-start usage.
- `datasheet.md`.
- `schema.md` with examples.
- `CITATION.cff`.
- `LICENSE.txt`.
- `CHANGELOG.md`.
- Release version number and date.
- Contact for corrections.
- Checksums for CSV files.

### Comment

The corpus has strong reuse value, but the release package needs to be treated
as a first-class research artifact. The paper should not only say that the CSV
will be released; it should specify versioning, maintenance, citation, and
expected repository structure.

## EC-LEGALPRIVACY-04

**Role:** legal/privacy scholar  
**Experience:** 14 years in privacy law, platform governance, and consumer
protection research  
**Feedback lens:** legal interpretability and overclaim risk

### Ratings

| Dimension | Rating |
|---|---:|
| Legal relevance | 5/5 |
| Risk of overclaim | 4/5 |
| Usefulness for regulators | 4/5 |
| Need for wording caution | 5/5 |

### Comment

The corpus is valuable because it shows how trained reviewers construct a
policy-evidence warrant for a structured label claim. However, the paper must
avoid implying that a reviewer verdict equals legal non-compliance. A privacy
policy may be vague, incomplete, or inconsistent with a platform label without
the paper being able to determine legal violation.

Recommended wording:

- "reviewer-cited evidence"
- "audit verdict under the study protocol"
- "evidence used to support or question a Data Safety claim"

Avoid:

- "proof of violation"
- "ground truth compliance"
- "illegal disclosure"

### Release Condition

Include a note that the corpus supports research and tool evaluation, not
enforcement action without independent legal analysis.

## EC-LLMBUILDER-05

**Role:** LLM-assisted audit tool builder  
**Experience:** 6 years building retrieval-augmented document review tools  
**Feedback lens:** model evaluation, RAG design, and uncertainty

### Ratings

| Dimension | Rating |
|---|---:|
| Usefulness for evidence retrieval | 5/5 |
| Usefulness for verdict prediction | 3/5 |
| Usefulness for RAG evaluation | 5/5 |
| Need for uncertainty labels | 5/5 |

### Comment

This corpus is excellent for evaluating whether a model can retrieve the same
evidence a human auditor cited. I would not start with verdict prediction. I
would start with claim-conditioned retrieval:

1. parse Data Safety claim;
2. split policy into candidate sentences;
3. retrieve top-K evidence;
4. show evidence to reviewer;
5. optionally produce a calibrated suggestion.

The top-K task is the most realistic HCI use. A model that gets Hit@5 high may
still be useful even if top-1 is imperfect.

### Requested Benchmark Metrics

- Hit@1, Hit@3, Hit@5.
- MRR.
- token IoU.
- evidence coverage by axis.
- negative-class precision/recall if verdict suggestions are included.
- calibration curve for uncertainty.

## EC-PLATFORMPOLICY-06

**Role:** platform policy reviewer / app-store compliance operations  
**Experience:** 7 years in platform policy triage  
**Feedback lens:** operational triage and policy-team usefulness

### Ratings

| Dimension | Rating |
|---|---:|
| Operational usefulness | 4/5 |
| Triage value | 5/5 |
| Risk of direct enforcement use | 4/5 |
| Need for app/category metadata | 5/5 |

### Comment

The corpus is useful for training and evaluating tools that help reviewers
locate relevant policy passages. It should not be used by itself to decide
enforcement outcomes. Platform teams would need:

- app category;
- Data Safety field under review;
- policy excerpt;
- surrounding policy context;
- confidence or disagreement indicators;
- whether the evidence supports contradiction, omission, or ambiguity.

The paper should emphasise reviewer-support tooling. A platform reviewer would
use the corpus to reduce search time, not to automate final decisions.

## EC-REPLICATION-07

**Role:** replication-focused empirical researcher  
**Experience:** 10 years in reproducibility, HCI methods, and computational
social science  
**Feedback lens:** replication package and external validity

### Ratings

| Dimension | Rating |
|---|---:|
| Reproducibility readiness | 3/5 |
| External validity clarity | 4/5 |
| Analysis transparency | 4/5 |
| Need for replication scripts | 5/5 |

### Comment

The paper should include a minimal reproduction path. A reader should be able
to run the scorer and reproduce the main linguistic tables in under one hour.
The package should include:

- raw released CSV;
- scored CSV or scorer script;
- notebook or script for all tables;
- environment file;
- fixed random seed;
- official train/test split;
- README with expected outputs.

### External Validity Note

The corpus is likely specific to Google Play Data Safety, English-language
policies, and the original reviewer pool. That does not weaken the resource,
but it should be explicit. A strong paper would invite replications on iOS App
Privacy labels, EU DSA-style disclosures, and non-English policies.

