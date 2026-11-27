# PromptLens — AI Security Detection & Evaluation Lab

**PromptLens** is an experimental machine-learning application for identifying potentially malicious prompts, including instruction-override and prompt-injection attempts. It began as a hands-on AI security learning project and developed into a deployed classifier with model benchmarking, failure analysis, and a second training-data experiment.

**Live app:** https://promptlens-ai-security-lab.streamlit.app/  
**Repository:** https://github.com/mubarak-byte/promptlens-ai-security-lab

> **Research prototype, not a security control.** PromptLens can misclassify harmless text and miss malicious instructions. Its scores are not calibrated probabilities, and its benchmark results do not establish reliable performance in production.

## What the app does

Enter a prompt in the Streamlit interface to receive:

- A **Benign** or **Potentially Malicious** prediction.
- A LinearSVC **decision score**: positive favors the malicious class; negative favors the benign class.
- Clearly labeled **validation metrics** for the deployed experimental v2 model.

PromptLens classifies text; it does **not** run or execute the submitted prompt against an LLM or measure whether a prompt injection would succeed.

## Approach

The project uses a **TF-IDF + Linear Support Vector Classifier (LinearSVC)** pipeline. The initial benchmark compared three classifiers trained using the same word-level TF-IDF representation:

| Classifier | Validation F1 (malicious class) |
| --- | ---: |
| Logistic Regression | 94.69% |
| Multinomial Naive Bayes | 94.30% |
| **LinearSVC** | **96.07%** |

LinearSVC was selected for the first deployed version based on validation performance.

### Original dataset

The initial model was trained using the **`core`** configuration of [NeurAlchemy's Prompt-injection-dataset](https://huggingface.co/datasets/neuralchemy/Prompt-injection-dataset):

| Split | Examples |
| --- | ---: |
| Train | 4,391 |
| Validation | 941 |
| Held-out test | 942 |
| **Total** | **6,274** |

Labels: `0` = benign; `1` = malicious. The dataset includes a range of prompt categories. Some labels, particularly those involving harmful-content requests rather than explicit instruction overrides, require careful interpretation against a precise threat model.

## Evaluation results

### V1 — original word-level LinearSVC

| Metric | Validation | Held-out test |
| --- | ---: | ---: |
| True positives | 525 | 539 |
| False positives | 34 | 33 |
| True negatives | 373 | 357 |
| False negatives | 9 | 13 |
| Malicious precision | 93.92% | 94.23% |
| Malicious recall | 98.31% | 97.64% |
| Malicious F1 | 96.07% | 95.91% |
| Accuracy | 95.43% | 95.12% |

The held-out test was used for the original v1 final evaluation, not for selecting the v2 modifications.

### Why investigate v2?

After deployment, v1 incorrectly flagged ordinary inputs such as greetings and general questions as malicious. In a small **exploratory, manually constructed** challenge set, it flagged **14 of 30 benign prompts** (46.67% false-positive rate). In a separate set of **30 synthetic instruction-override examples**, it detected all 30. These small challenge sets were used for diagnosis, **not** as representative production benchmarks or untouched final v2 tests.

A training-data audit found that, using a narrow beginning-of-message greeting pattern, **0 benign** training examples and **22 malicious** training examples matched. This suggested that benign conversational coverage might be inadequate; it did not prove that greeting words caused the false positives.

### V2 — benign conversational augmentation (experimental)

We gathered candidate ordinary-language prompts from [AllenAI's WildChat-1M](https://huggingface.co/datasets/allenai/WildChat-1M), then filtered for possible language mismatches, duplicates, sensitive information, suspicious instructions, and known overlaps. **644 additional examples** were provisionally selected as benign and used to retrain the same word-level TF-IDF + LinearSVC architecture.

**The added examples were automatically screened and were not all manually verified.** This creates a residual label-quality and privacy risk and limits the strength of conclusions.

| Validation metric | V1 | V2 (experimental) |
| --- | ---: | ---: |
| Training examples | 4,391 | 5,035 |
| True positives | 525 | 512 |
| False positives | 34 | **24** |
| True negatives | 373 | **383** |
| False negatives | **9** | 22 |
| False-positive rate (benign class) | 8.35% | **5.90%** |
| Malicious recall | **98.31%** | 95.88% |
| Malicious F1 | **96.07%** | 95.70% |

V2 reduced validation false positives by **10 cases (29.4%)**, but missed **13 additional malicious-labeled examples**. It should **not** be described as unambiguously better than v1. On previously examined greetings and general questions, some predictions improved while others remained incorrect. **No fresh independent final test has yet been reported for v2.**

Other experiments included threshold adjustment, balanced class weights, character-level TF-IDF, and feature-contribution analysis. These helped diagnose behavior but did not eliminate the generalization issue.

## Run the application locally

Clone the repository and install the app dependencies in a virtual environment:

```bash
git clone https://github.com/mubarak-byte/promptlens-ai-security-lab.git
cd promptlens-ai-security-lab
python -m venv .venv
```

Activate the environment (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies and launch:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The application loads `promptlens_v2_filtered.joblib` from the repository root. A compatible scikit-learn environment is necessary to load the serialized model. Only load `joblib`/pickle artifacts from sources you trust.

## Limitations and research lessons

- **False positives:** Harmless everyday language may be flagged as malicious.
- **False negatives:** Some malicious-labeled prompts are missed, including after benign augmentation.
- **Dataset generalization:** Performance on one dataset split does not guarantee similar performance on independent conversations or new attack strategies.
- **Threat-model ambiguity:** Harmful-content requests, jailbreaks, and prompt injection are related but not interchangeable categories.
- **Decision scores:** LinearSVC margin scores are **not probabilities** or calibrated confidence values.
- **V2 data quality:** WildChat additions were provisionally screened, not exhaustively hand-labeled.
- **Reproducibility scope:** The repository includes the deployed model artifact and application. Full reproduction of the v2 data selection requires the complete preparation procedure and its reviewed data manifest.

**Takeaway:** Better coverage of normal conversations reduced false alarms on validation, but there was a measurable loss in malicious recall. PromptLens is a learning and experimentation project, not a production-ready prompt-injection defense.

## Data attribution

- [NeurAlchemy — Prompt-injection-dataset](https://huggingface.co/datasets/neuralchemy/Prompt-injection-dataset), published under **Apache-2.0**.
- [AllenAI — WildChat-1M](https://huggingface.co/datasets/allenai/WildChat-1M), published under **ODC-BY**. WildChat was used as a source of candidate benign conversations. Refer to the upstream dataset card for licensing, attribution, and privacy considerations.

## Project status

**PromptLens v2 — Experimental release.** The next learning project is a neural network built from scratch, followed by adversarial-robustness experiments.
