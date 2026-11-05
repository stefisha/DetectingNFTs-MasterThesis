# Research scope and limitations

## Original research

The master's thesis examines three independent NFT classification problems: image-based analysis, description-based analysis, and collection-domain analysis. It compares several model families within each problem and discusses the value of combining evidence in future applications.

The thesis is a 2023 master's study. The thesis is in the process of being published. No acceptance decision, publication venue, or DOI has been confirmed.

## Limitations discussed in the thesis

Section 6.6, printed pages 66–67, identifies limited scam examples, class imbalance, incomplete NFT attributes, changing fraud behavior, possible dataset bias, and computational constraints. It recommends expanding the data and maintaining contact with the NFT community as fraud techniques evolve.

Description experiments focus on descriptions rather than all NFT metadata. Section 6.2 explains that many other fields were missing or unavailable across records.

## Observations from the archived notebooks

The notebooks are exploratory research artifacts with the following evaluation considerations:

- Some saved results and narrative percentages differ from manuscript tables. See [the provenance record](RESULTS.md).
- The notebooks do not provide collection-disjoint or temporal evaluation manifests. Random item-level splits may contain related examples; the actual degree of overlap is not established here.
- Optional internal domain cross-validation diagnostics reuse preprocessing fitted on the training partition; rigorous CV requires fitting preprocessing separately within each fold.
- Commented alternatives and incomplete saved outputs should be distinguished from executed experiments. The manuscript discusses more alternatives than can be confirmed from every current execution snapshot.
- Historical source labels, domains, and NFT content should not be interpreted as present-day assessments of a project or person.

## Follow-up work

Useful extensions include a documented dataset release with permissions; collection-aware and time-based splits; duplicate analysis; calibration and threshold selection; repeated runs with confidence intervals; broader external validation; and a separately evaluated fusion model. An applied system also needs a review of error costs, abuse resistance, operational monitoring, and human review processes.

## Later application

The author identifies this thesis as the research basis for [MintEye](https://github.com/stefisha/MintEye), a later Solana Radar Hackathon application. That project has its own application code, model artifacts, and runtime. Its deployment or inference behavior is not evidence that the historical thesis scores have been independently reproduced.
