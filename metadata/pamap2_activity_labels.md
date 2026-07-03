# PAMAP2 Activity Labels

This document records the activity labels used in the PAMAP2 Protocol dataset.

## Label mapping

| ID | Activity |
|---:|---|
| 0 | transient / other activity |
| 1 | lying |
| 2 | sitting |
| 3 | standing |
| 4 | walking |
| 5 | running |
| 6 | cycling |
| 7 | Nordic walking |
| 9 | watching TV |
| 10 | computer work |
| 11 | car driving |
| 12 | ascending stairs |
| 13 | descending stairs |
| 16 | vacuum cleaning |
| 17 | ironing |
| 18 | folding laundry |
| 19 | house cleaning |
| 20 | playing soccer |
| 24 | rope jumping |

## Initial protocol observation

The Protocol subset currently contains the following labels:

- Most subjects: 0, 1, 2, 3, 4, 5, 6, 7, 12, 13, 16, 17, 24
- Some subjects are missing individual activities.
- Subject 109 is very short and contains only labels 0 and 24.

## Methodological note

Label 0 represents transient or undefined activity periods. For supervised activity modeling and clean tensorization, this label should likely be excluded or handled separately.

For dysbalance analysis, the treatment of label 0 must be documented explicitly because it can influence subject-specific reference distributions.
