To protect short-clause prosody while eliminating real, persistent acoustic artifacts, **recommend permanently removing 9–10 of the long or severely warbled files**, while **retaining 7 critical short-clause files**.

---

### Core Strategy & Analysis

1. **Why Short Clauses (< 3.0s) get flagged artificially**:
   Short utterances suffer from a mathematical artifact in density calculations: dividing by a small duration \\(T\\) (1–2 seconds) inflates the `glitches_per_sec` metric (e.g., 4 micro-jumps in 1.15s = 3.48 glitches/sec). However, their **absolute glitch count is low (4–7)**. Since keeping short clauses is vital to prevent inference slurring, these short files should be retained unless their pitch instability (F0 Std) is extreme.

2. **Why Long Clauses (> 4.0s) should be removed**:
   Longer utterances with high glitch density represent **sustained, non-stop pitch tracking failures** across multi-second phrases (12 to 29 glitch jumps per file). Just **8 long files account for 129 out of 187 total glitches (69% of all corpus glitches!)**. Removing them cleans out the vast majority of corruption without sacrificing short-phrase training examples.

---

### Recommended Removal & Retention Breakdown

#### ❌ Category 1: Permanently Remove — Long & Persistent Glitches (8 Files)
*These long files contain massive glitch counts (12–29 jumps) and do not contribute short-clause training value.*

| File Name | Duration | Glitches | F0 Std | Reason for Removal |
| :--- | :---: | :---: | :---: | :--- |
| **`SN_SN22_55_0022.wav`** | 11.43s | **29** | 15.5 Hz | Longest file, highest absolute glitch count in corpus. |
| **`AN_AN4_99_0012.wav`** | 6.32s | **16** | 15.7 Hz | Sustained pitch glitching across 6 seconds. |
| **`KN_Iti_iti78_0003.wav`** | 5.35s | **16** | 15.4 Hz | Sustained pitch glitching across 5 seconds. |
| **`SN_SN21_1_0013.wav`** | 4.77s | **15** | 17.5 Hz | Heavy glitching throughout utterance. |
| **`KN_Khp_khp7_0011.wav`** | 4.65s | **14** | 17.5 Hz | Heavy glitching throughout utterance. |
| **`AN_AN10_92_0013.wav`** | 5.14s | **14** | 16.8 Hz | Heavy glitching throughout utterance. |
| **`AN_AN3_103_0014.wav`** | 5.12s | **13** | 15.9 Hz | Heavy glitching throughout utterance. |
| **`AN_AN6_63_0099.wav`** | 4.04s | **12** | 18.6 Hz | 12 glitches in 4 seconds. |

---

#### ❌ Category 2: Permanently Remove — Severe Pitch Warble (2 Short Files)
*These short files exhibit extreme F0 instability (>20 Hz Std), indicating true vocal warble rather than minor onset/offset math.*

| File Name | Duration | Glitches | F0 Std | Reason for Removal |
| :--- | :---: | :---: | :---: | :--- |
| **`SN_SN6_2_0029.wav`** | 2.42s | 7 | **24.1 Hz** | Highest F0 instability in the entire outlier set. |
| **`SN_SN44_1_0018.wav`** | 1.99s | 7 | **22.3 Hz** | Severe pitch warble/instability. |

---

#### ✅ Category 3: RETAIN in Training Corpus — Essential Short Clauses (7 Files)
*These short clauses (< 3.2s) have low absolute glitch counts (4–8) and acceptable pitch stability. Retaining them prevents model slurring during inference.*

| File Name | Duration | Glitches | F0 Std | Reason for Retention |
| :--- | :---: | :---: | :---: | :--- |
| **`SN_SN22_80_0030.wav`** | 1.15s | 4 | 17.7 Hz | **Shortest file in outlier report.** Essential short phrase. |
| **`SN_SN21_9_0006.wav`** | 1.85s | 5 | 18.0 Hz | Ultra-short utterance with only 5 glitches. |
| **`AN_AN3_42_0005.wav`** | 1.65s | 6 | 20.4 Hz | Short clause (keep unless listening reveals harsh warble). |
| **`SN_SN21_8_0005.wav`** | 2.06s | 7 | 15.2 Hz | Excellent pitch stability (15.2 Hz std). |
| **`AN_AN5_162_0010.wav`** | 2.36s | 6 | 16.3 Hz | Low absolute glitch count & stable F0. |
| **`SN_SN22_95_0034.wav`** | 2.96s | 8 | 17.4 Hz | Sub-3s clause; essential prosody anchor. |
| **`KN_Iti_iti79_0009.wav`** | 3.14s | 8 | 17.6 Hz | ~3s clause; low absolute glitch count. |

---

### Summary Impact

- **Files Removed**: **10 files** (8 long files + 2 warbled short files).
- **Files Retained**: **7 short-clause files** (preserves short-utterance prosody).
- **Corpus Glitch Reduction**: Removes **143 out of 187 outlier glitches (~76.5% of all outlier glitches eliminated)** while retaining 100% of vital short-phrase coverage!

💡 Would you like me to generate a clean Python script or Bash snippet to automatically filter out those 10 filenames from your training `metadata.csv` file?