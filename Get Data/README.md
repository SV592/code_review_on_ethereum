# GitHub Pull Request Analysis

This project includes two scripts, `get_pullrequestdata.py` and `pull_requests.py`, designed to streamline the process of collecting and processing pull request (PR) data from GitHub repositories. These tools extract detailed PR metadata and facilitate the exploration of PR changes locally.

---

## Overview

### **`get_pullrequestdata.py`**
This script uses the GitHub GraphQL API to extract detailed pull request data for a given repository. It gathers metadata such as:
- PR title, number, state, creation/merge times
- Number of reviewers and comments
- Author details
- Associated reviews and comments

The extracted data is saved in a CSV file for further processing.

### **`pull_requests.py`**
This script facilitates:
- Checking out merged pull requests from a local Git repository.
- Preparing the repository state for additional analysis or review.

---

## Features

### `get_pullrequestdata.py`
- Fetches PR metadata using the GitHub GraphQL API.
- Handles API rate limits gracefully with retries.
- Saves PR data as CSV for easy analysis.

### `pull_requests.py`
- Automates the checkout of merged PRs in a local repository.
- Prepares the local repository state for custom analysis.

---

## Prerequisites

- Python 3.8+
- Git
- GitHub API token with `repo` and `read:org` permissions for private repositories.

---

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/github-pr-analysis.git
   cd github-pr-analysis
