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

## 2026-07-03: First new dataset

Decision:

PAMAP2 will be used as the first newly integrated dataset.

Reason:

PAMAP2 is suitable as the first Bachelor-thesis dataset because it combines physical activity, movement-related sensor data and heart-rate information. It is less complex than longitudinal real-world datasets and therefore well suited for validating the extended parser, tensorization and AI-based time-series pipeline.

Scientific role:

- first new dataset beyond the KI-Studienprojekt
- functional physiological deviation modeling
- activity and load-related time-series patterns
- test case for MultiRocket and personalized dysbalance scores
