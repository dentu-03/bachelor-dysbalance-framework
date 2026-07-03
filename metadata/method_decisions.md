# Method Decisions

## 2026-07-03: ROCKET-style time-series classifiers

The local Python environment was checked with aeon 1.5.0.

Available classifiers:

- RocketClassifier
- MiniRocketClassifier
- MultiRocketClassifier
- MultiRocketHydraClassifier

Decision:

MultiRocketClassifier will be planned as the primary time-series classification method for the Bachelor thesis framework.

MiniRocketClassifier will remain as a stable baseline, because it was already used successfully in the previous KI-Studienprojekt.

Scientific role:

- MultiRocket: main AI-based time-series model
- MiniRocket: reproducible baseline and comparison method
- Dysbalance scores: explainable deviation layer
- Anomaly detection: personalized abnormality detection layer
