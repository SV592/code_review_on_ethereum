# GitHub Pull Request Analysis

### **`get_pullrequestdata.py`**
This script uses the GitHub GraphQL API to extract detailed pull request data for a given repository. It gathers metadata such as:
- PR title, number, state, creation/merge times
- Number of reviewers and comments
- Author details
- Associated reviews and comments

The extracted data is saved in a CSV file for further processing.

### **`pull_requests.py`**
This script automates the process of:
- Checking out merged pull requests in a local repository.
- Running static analysis on the merged code using **Slither** to identify vulnerabilities.
- Storing the results of the analysis in JSON files.

---

## Features

### `get_pullrequestdata.py`
- Fetches PR metadata using the GitHub GraphQL API.
- Handles API rate limits gracefully with retries.
- Saves PR data as CSV for easy analysis.

### `pull_requests.py`
- Automates the checkout of merged PRs in a local repository.
- Runs **Slither**, a Solidity static analysis tool, on the code introduced by the PRs.
- Saves vulnerability reports in JSON format for further investigation.

---

## Prerequisites

- Python 3.8+
- Git
- Node.js (for Slither)
- **Slither** Solidity Analyzer:
  ```bash
  npm install -g slither-analyzer
