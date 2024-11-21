import pandas as pd
import ast

df = pd.read_csv("makerdao-dss.csv")

# Count number of MERGED, OPEN, CLOSED pull requests, in column "PullRequestState"
# print(df["PullRequestState"].value_counts())


# Count Average numer of comments per Pull Request
average_num_comments = df["PullRequestCommentsCount"].value_counts()
print(f"Average number of comments: {average_num_comments}")

# Count Average number of Reviewers per Pull Request
# Convert the string representation of arrays to actual lists
# Convert the "PullRequestReviewers" column from strings to lists
df["PullRequestReviewers"] = df["PullRequestReviewers"].apply(ast.literal_eval)

# Remove duplicates from the "PullRequestReviewers" lists
df["PullRequestReviewers"] = df["PullRequestReviewers"].apply(set)

# Calculate the number of unique reviewers for each row and store it in a new column
df["num_unique_reviewers"] = df["PullRequestReviewers"].apply(lambda x: len(x))

# Calculate the average number of unique reviewers for the entire dataset
average_unique_reviewers = df["num_unique_reviewers"].mean()

print(f"Average number of reviewers: {round(average_unique_reviewers)}")


# get the average time to merge
df["createdAt"] = pd.to_datetime(df["PullRequestCreatedAt"])
df["mergedAt"] = pd.to_datetime(df["PullRequestMergedAt"])
df["closedAt"] = pd.to_datetime(df["PullRequestClosedAt"])

# Getting time difference for closed pull requests
df["time_difference_hours_close"] = (
    df["closedAt"] - df["createdAt"]
).dt.total_seconds() / 3600.0

# Getting time difference for merged pull requests
df["time_difference_hours_merge"] = (
    df["mergedAt"] - df["createdAt"]
).dt.total_seconds() / 3600.0


average_time_to_close = df["time_difference_hours_close"].mean()
average_time_to_merge = df["time_difference_hours_merge"].mean()

print(f"Average time to close: {round(average_time_to_close)}")
print(f"Average time to merge: {round(average_time_to_merge)}")
