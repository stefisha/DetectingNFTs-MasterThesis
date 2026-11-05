# Data documentation

## Availability

The original research datasets are no longer available. Historical experiment reproduction is therefore unavailable. The notebooks expect previously prepared image directories and CSV files. Data acquisition scripts, exact source snapshots, licenses for every item, and split manifests are not supplied.

Do not infer dataset redistribution rights from the code's MIT license. NFT artwork, marketplace records, and third-party datasets retain their own terms and ownership.

## Sources described in the thesis

The manuscript describes Phantom blocklists for scam-labeled examples, marketplace data including Tensor for legitimate-labeled examples, and an OpenSea collection dataset from Kaggle for additional domain information. The labels reflect the sources and selection process used in the research; they are not independently adjudicated ground truth.

## Expected inputs

| Study | Expected inputs | Important fields or layout |
| --- | --- | --- |
| Images | `Images_scam/` and `Images_legit/` directories | Files readable by Pillow; RGB conversion and resizing to 128 × 128 are performed in the notebook |
| Descriptions | `nft_data_legit.csv`, `scam_nft_data_full.csv` | Inspect the notebook's preprocessing cells for the source description field and retained rows |
| Domains | `final_blocklist_domains.csv`, `final_legit_domains.csv` | Scam CSV uses `url`; legitimate CSV uses `Unique Domains`, renamed to `url` |

Future runs use `NFT_DATA_ROOT`, defaulting to `data/` relative to the notebook's working directory:

```text
data/
  Images/Images_scam/
  Images/Images_legit/
  Metadata/nft_data_legit.csv
  Metadata/scam_nft_data_full.csv
  Domains/final_blocklist_domains.csv
  Domains/final_legit_domains.csv
```

For local Jupyter, set the environment variable before starting the kernel, for example `export NFT_DATA_ROOT=/path/to/data`. In Colab, mount your own Drive and set `%env NFT_DATA_ROOT=/content/drive/MyDrive/path/to/data` before the data-loading cell. The original Drive layout used `/content/drive/MyDrive/Master/Project/` as its root.

Only supply data you are authorized to use. Replacement datasets cannot recover the historical thesis experiments. Do not commit private datasets or access credentials.

## Manuscript counts and notebook snapshots

| Modality | Thesis collection counts | Available notebook evidence |
| --- | --- | --- |
| Images | 1,082 scam-labeled and 1,796 legitimate-labeled images; section 4.1.1, printed page 22 | Cells 3 and 7 record 1,082 and 1,762 images, totaling 2,844; cell 9 records train/validation/test counts of 1,990/427/427 |
| Metadata | 2,722 scam-labeled and 10,007 legitimate-labeled records; section 4.1.2, printed page 23 | Preprocessing may remove or transform records; the repository does not include an immutable processed-data manifest |
| Domains | 1,637 scam-labeled and 823 legitimate-labeled addresses; section 4.1.3, printed page 23 | Domain cell 8 displays a combined series of 2,451 rows; the manuscript collection total is 2,460 |

Differences between collection counts and saved notebook counts are recorded rather than assigned an unverified cause. Do not use one count as an interchangeable substitute for the other.

## Information needed for a reproducible dataset release

A future release should record source identifiers, collection dates, labeling rules, exclusions, duplicate handling, collection grouping, class counts before and after processing, item-level train/validation/test assignments, checksums, and redistribution permissions. Sensitive information and harmful URLs should be handled appropriately; examples displayed by the notebooks should not be interpreted as current assertions about a site's ownership or safety.
