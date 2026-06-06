# opengem-event-detector

🧪 alpha

Event detection + scenario-pack triggering for OPENGEM. Maps detected events
(news headlines, market-condition crosses, GPR spikes, GDELT theme bursts) to
canonical scenario packs from `opengem-scenarios`.

## Architecture

```
Detectors → Events → Rule engine → Pack triggers
  │
  ├─ MarketThresholdDetector: term spread inverted, VIX > 35, BAA-10y > 400bp
  ├─ GPRSpikeDetector: country GPR > 2 sigma above 12m moving average
  ├─ NewsKeywordDetector: keywords in news headlines mapped to packs
  └─ ManualTrigger: API-driven manual scenario trigger
```

For IOC, we focus on simple, transparent rules. Each detector is independent
and pluggable.

## Why this exists

Per the program-owner direction: the friend's YouTuber workflow is event-driven.
He wakes up, sees Iran-Israel news, and wants OPENGEM to have already run the
Iran-Israel pack overnight so the digest is ready. This package implements the
"wakes up and runs the right pack" logic.
