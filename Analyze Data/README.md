# Pull Request Data Analysis

### **`analyzer.py`**
This script:
- Processes pull request data from CSV files.
- Adds calculated columns such as review duration (time to merge/close).
- Generates statistical summaries for PR states, review times, and comments.

### **`statistics.py`**
This script:
- Extracts detailed statistics from the processed PR data.
- Calculates averages for key metrics such as:
  - Time to merge/close PRs.
  - Number of reviewers and comments per PR.
- Outputs insights about the review process for further analysis.

---

## Features

### `analyzer.py`
- Adds a `ReviewDuration` column to indicate how long a PR took to merge or close.
- Converts time durations into seconds for precise calculations.
- Generates intermediate outputs for further exploration.

### `statistics.py`
- Analyzes PR data to calculate averages:
  - Time to merge and close PRs (in hours).
  - Number of unique reviewers and comments per PR.
- Outputs insights for repository-level trends.

---

## Prerequisites

- Python 3.8+
- Pandas library:
  ```bash
  pip install pandas
