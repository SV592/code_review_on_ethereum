import json
import pandas as pd
import numpy as np
import ast

from datetime import datetime


def add_duration_column(df, file):
    review_duration = []
    for index, row in df.iterrows():
        if row["PullRequestState"] in ["MERGED", "CLOSED"]:
            creationTime = datetime.fromisoformat(row["PullRequestCreatedAt"])
            closingTime = datetime.fromisoformat(row["PullRequestClosedAt"])
            duration = closingTime - creationTime
        else:
            duration = None
        review_duration.append(duration)
    df["ReviewDuration"] = review_duration
    df.to_csv(file, index=False)


def add_duration_columns():
    for file in files:
        df = pd.read_csv(file)
        add_duration_column(df, file)


def convert_to_seconds(duration):
    if not isinstance(duration, str):
        return 0
    seconds = 0
    duration_segs = duration.split()
    duration_days = int(duration_segs[0])
    duration_segs = duration_segs[2].split(":")
    duration_hours = int(duration_segs[0])
    duration_mins = int(duration_segs[1])
    duration_secs = int(duration_segs[2])

    seconds += duration_days * 24 * 60 * 60
    seconds += duration_hours * 60 * 60
    seconds += duration_mins * 60
    seconds += duration_secs

    return seconds


def cal_stats():
    out_df = pd.DataFrame()
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
        df = pd.read_csv(file)
        stat_df = {
            "MERGED": {"num": 0, "time": 0},
            "OPEN": {"num": 0, "time": 0},
            "CLOSED": {"num": 0, "time": 0},
            "num_comments": 0,
            "num_reviewers": 0,
        }
        for index, row in df.iterrows():
            state = row["PullRequestState"]
            duration = convert_to_seconds(row["ReviewDuration"])
            stat_df[state]["num"] += 1
            stat_df[state]["time"] += duration
            stat_df["num_comments"] += row["PullRequestCommentsCount"]
            stat_df["num_reviewers"] += len(
                set(ast.literal_eval(row["PullRequestReviewers"]))
            )

        repo_name = file.split("_")[-1][:-4]
        average_time_to_close = (
            round(stat_df["CLOSED"]["time"] / (stat_df["CLOSED"]["num"] * 3600))
            if stat_df["CLOSED"]["num"] != 0
            else None
        )
        average_time_to_merge = (
            round(stat_df["MERGED"]["time"] / (stat_df["MERGED"]["num"] * 3600))
            if stat_df["MERGED"]["num"] != 0
            else None
        )
        average_num_reviewers = round(stat_df["num_reviewers"] / df.shape[0])
        average_num_comments = round(stat_df["num_comments"] / df.shape[0])
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
        out_df = pd.concat([out_df, df_stat_series.to_frame().T], ignore_index=True)
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

    out_df.to_csv("stats.csv", index=False)


files = [
    "Aave_v3.csv",
    "Compoundfinance-protocol.csv",
    "makerdao-dss.csv",
    "smartcontractkit-chainlink.csv",
    "Uniswap-v3core.csv",
]  # TODO

add_duration_columns()
cal_stats()
