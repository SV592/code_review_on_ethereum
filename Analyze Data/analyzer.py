import json
import pandas as pd
import numpy as np
import ast
from datetime import datetime


# Adds a new column "ReviewDuration" to a DataFrame, which calculates the duration
# between PullRequestCreatedAt and PullRequestClosedAt for merged/closed pull requests.
# Saves the updated DataFrame to the given file.
def add_duration_column(df, file):
    review_duration = []  # List to store the calculated duration for each row
    for index, row in df.iterrows():
        # Calculate duration only for MERGED or CLOSED pull requests
        if row["PullRequestState"] in ["MERGED", "CLOSED"]:
            creationTime = datetime.fromisoformat(row["PullRequestCreatedAt"])
            closingTime = datetime.fromisoformat(row["PullRequestClosedAt"])
            duration = closingTime - creationTime
        else:
            duration = None  # No duration for OPEN pull requests
        review_duration.append(duration)
    df["ReviewDuration"] = review_duration  # Add the calculated durations to the DataFrame
    df.to_csv(file, index=False)  # Save the updated DataFrame back to the file


# Iterates over a list of files, reads each file as a DataFrame,
# and applies the add_duration_column function.
def add_duration_columns():
    for file in files:
        df = pd.read_csv(file)  # Read the CSV file
        add_duration_column(df, file)  # Add the "ReviewDuration" column


# Converts a duration string into seconds for easier calculations.
# Duration format example: "X days, HH:MM:SS"
def convert_to_seconds(duration):
    if not isinstance(duration, str):  # If duration is not a string, return 0
        return 0
    seconds = 0  # Initialize the total seconds
    duration_segs = duration.split()  # Split the duration into segments (days and time)

    # Extract the number of days
    duration_days = int(duration_segs[0]) if len(duration_segs) > 1 else 0

    # Extract the time part (HH:MM:SS)
    duration_segs = duration_segs[-1].split(":")
    duration_hours = int(duration_segs[0])
    duration_mins = int(duration_segs[1])
    duration_secs = int(duration_segs[2])

    # Calculate the total duration in seconds
    seconds += duration_days * 24 * 60 * 60
    seconds += duration_hours * 60 * 60
    seconds += duration_mins * 60
    seconds += duration_secs

    return seconds


# Calculates statistics for each repository file, including the number of pull requests,
# average merge and close times, and reviewer/comment statistics. Outputs the results
# as both a CSV file and printed JSON summaries.
def cal_stats():
    out_df = pd.DataFrame()  # DataFrame to store all repository statistics
    columns = [
        "Repository",
        "Num of Merged PRs",
        "Num of Open PRs",
        "Num of Closed PRs",
        "average_merge_time",
        "average_close_time",
        "average_num_reviewers",
        "average_num_comments",
    ]
    
    for file in files:
        df = pd.read_csv(file)  # Read the CSV file for the repository
        # Dictionary to store pull request statistics for the current repository
        stat_df = {
            "MERGED": {"num": 0, "time": 0},
            "OPEN": {"num": 0, "time": 0},
            "CLOSED": {"num": 0, "time": 0},
            "num_comments": 0,
            "num_reviewers": 0,
        }

        for index, row in df.iterrows():
            state = row["PullRequestState"]  # State of the pull request (MERGED/OPEN/CLOSED)
            duration = convert_to_seconds(row["ReviewDuration"])  # Convert duration to seconds
            stat_df[state]["num"] += 1  # Increment the count for the state
            stat_df[state]["time"] += duration  # Add the duration for the state
            # Add the number of comments
            stat_df["num_comments"] += row["PullRequestCommentsCount"]
            # Count unique reviewers for the pull request
            stat_df["num_reviewers"] += len(set(ast.literal_eval(row["PullRequestReviewers"])))

        # Extract the repository name from the filename
        repo_name = file.split("_")[-1][:-4]
        
        # Calculate average time to close (in hours) for CLOSED pull requests
        average_time_to_close = (
            round(stat_df["CLOSED"]["time"] / (stat_df["CLOSED"]["num"] * 3600))
            if stat_df["CLOSED"]["num"] != 0
            else None
        )
        
        # Calculate average time to merge (in hours) for MERGED pull requests
        average_time_to_merge = (
            round(stat_df["MERGED"]["time"] / (stat_df["MERGED"]["num"] * 3600))
            if stat_df["MERGED"]["num"] != 0
            else None
        )
        
        # Calculate average number of reviewers per pull request
        average_num_reviewers = round(stat_df["num_reviewers"] / df.shape[0])
        
        # Calculate average number of comments per pull request
        average_num_comments = round(stat_df["num_comments"] / df.shape[0])

        # Create a Series for the repository statistics
        df_stat_series = pd.Series(
            [
                repo_name,
                stat_df["MERGED"]["num"],
                stat_df["OPEN"]["num"],
                stat_df["CLOSED"]["num"],
                average_time_to_merge,
                average_time_to_close,
                average_num_reviewers,
                average_num_comments,
            ],
            index=columns,
        )

        # Append the statistics Series to the output DataFrame
        out_df = pd.concat([out_df, df_stat_series.to_frame().T], ignore_index=True)

        # Print repository statistics as JSON for quick inspection
        print(
            json.dumps(
                {
                    "Repo": repo_name,
                    "Pull Requests": {
                        "OPEN": stat_df["OPEN"]["num"],
                        "CLOSED": stat_df["CLOSED"]["num"],
                        "MERGED": stat_df["MERGED"]["num"],
                    },
                    "average_num_reviewers": average_num_reviewers,
                    "average_num_comments": average_num_comments,
                    "average_merge_time": f"{average_time_to_merge} hrs",
                    "average_close_time": f"{average_time_to_close} hrs"
                    if average_time_to_close is not None
                    else "None",
                },
                indent=4,
            )
        )

    # Save all repository statistics to a CSV file
    out_df.to_csv("stats.csv", index=False)


# List of CSV files for repositories
files = [
    "Aave_v3.csv",
    "Compoundfinance-protocol.csv",
    "makerdao-dss.csv",
    "smartcontractkit-chainlink.csv",
    "Uniswap-v3core.csv",
]  # TODO: Add more files as needed

# Add the "ReviewDuration" column to each repository file
add_duration_columns()

# Calculate and output repository statistics
cal_stats()
