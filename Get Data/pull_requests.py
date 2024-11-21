import pandas as pd
import subprocess
import os

# Path to the CSV file containing pull request information
csv_file_path = ".\\Repos\\Uniswap-v3core.csv"

# Path to the local Git repository
repo_path = (
    ".\\Users\\23pears\\Desktop\\Grad Work (UoW)\\Classes\\CS854\Project\\v3-core"
)

# Directory to save Slither scan results
scan_results_dir = "results"


def checkout_pull_request(pull_request_number):
    try:
        subprocess.run(
            ["git", "checkout", f"pr/{pull_request_number}"], cwd=repo_path, check=True
        )
        print(f"Pull request {pull_request_number} checked out successfully.")
    except subprocess.CalledProcessError:
        print(f"Error checking out pull request {pull_request_number}.")


def scan_with_slither(output_file):
    try:
        subprocess.run(
            [
                "npx",
                "slither",
                "--exclude",
                "some,contracts,to,exclude",
                "--json",
                output_file,
            ],
            cwd=repo_path,
            check=True,
        )
        print("Slither scan completed successfully.")
    except subprocess.CalledProcessError:
        print("Error running Slither scan.")


def main():
    # Read pull request information from CSV using pandas
    pull_requests_df = pd.read_csv(csv_file_path)

    # Filter merged pull requests
    merged_pull_requests = pull_requests_df[
        pull_requests_df["PullRequestState"] == "MERGED"
    ]

    # Create scan results directory if it doesn't exist
    os.makedirs(scan_results_dir, exist_ok=True)

    for index, row in merged_pull_requests.iterrows():
        pull_request_number = row["PullRequestNumber"]
        print(f"Checking out and scanning pull request {pull_request_number}")

        # Checkout the pull request
        checkout_pull_request(pull_request_number)

        # Create output file path for scan results
        output_file = os.path.join(
            scan_results_dir, f"pr_{pull_request_number}_scan.json"
        )

        # Run Slither scan and save results to output file
        scan_with_slither(output_file)


if __name__ == "__main__":
    main()
