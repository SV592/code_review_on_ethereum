import pandas as pd
import requests
import time


# Define function to retry requests when rate limit is reached
def retry_on_rate_limit(request_fn, *args, **kwargs):
    retries = 0
    max_retries = 5
    while True:
        response = request_fn(*args, **kwargs)
        if response.status_code == 200:
            return response
        elif (
            response.status_code == 403
            and "X-RateLimit-Remaining" in response.headers
            and int(response.headers["X-RateLimit-Remaining"]) == 0
        ):
            reset_time = int(response.headers["X-RateLimit-Reset"])
            wait_time = max(reset_time - time.time() + 1, 0)
            print(f"Rate limit reached, waiting for reset ({wait_time} seconds)...")
            time.sleep(wait_time)
        elif response.status_code == 502:
            if retries < max_retries:
                retries += 1
                print(f"Encountered 502 error, retrying in {retries} seconds...")
                time.sleep(retries)
            else:
                print(f"Encountered 502 error {max_retries} times, giving up...")
                return None
        else:
            print(f"Error Code {response.status_code}: {response.text}")
            return None


tokens = [
    # Add Github Tokens here
]

owner = "aave"
name = "aave-v3-core"

# Initialize empty DataFrame
pull_request_df = pd.DataFrame()

# Passing tokens into header frame of the API
headers = {
    "Content-Type": "application/json",
}

# Fetching pull requests using pagination
cursor = None

for token in tokens:
    # Passing token into header frame of the API
    headers["Authorization"] = f"bearer {token}"

    while True:
        # Passing query based on name and owner of a repo
        query = f"""
            {{
             repository(name: "{name}", owner: "{owner}") {{
                pullRequests(first: 100, after: {cursor if cursor else "null"}) {{
                  nodes {{
                    title
                    number
                    state
                    createdAt
                    updatedAt
                    closedAt
                    mergedAt
                    author {{
                      login
                    }}
                    reviews(first: 100) {{
                      totalCount
                      nodes {{
                        state
                        author {{
                          login
                        }}
                      }}
                    }}
                    comments {{
                      totalCount
                    }}
                  }}
                  pageInfo {{
                    endCursor
                    hasNextPage
                  }}
                }}
              }}
            }}
            """

        # Graphql post request with retry_on_rate_limit
        request = retry_on_rate_limit(
            requests.post,
            "https://api.github.com/graphql",
            json={"query": query},
            headers=headers,
            timeout=15,
        )

        if request is not None and request.status_code == 200:
            info = request.json()

            if "errors" in info:
                # Handle errors if any
                print(info["errors"])
                break

            pull_requests = info["data"]["repository"]["pullRequests"]["nodes"]
            for pr in pull_requests:
                pr_title = pr["title"]
                pr_number = pr["number"]
                pr_state = pr["state"]
                pr_created_at = pr["createdAt"]
                pr_updated_at = pr["updatedAt"]
                pr_closed_at = pr["closedAt"]
                pr_merged_at = pr["mergedAt"]
                for pr in pull_requests:
                    # ... other code ...

                    # Check if author is not None before accessing its properties
                    if pr["author"]:
                        pr_author = pr["author"]["login"]
                    else:
                        pr_author = (
                            "Unknown"  # Provide a default value if author is missing
                        )

                    # ... other code ...

                for pr in pull_requests:
                    # ... other code ...

                    # Check if reviews is not None before accessing its properties
                    if pr["reviews"]:
                        pr_reviews_count = pr["reviews"]["totalCount"]
                        pr_reviewers = [
                            review["author"]["login"]
                            for review in pr["reviews"]["nodes"]
                            if review and review["author"]
                        ]
                    else:
                        pr_reviews_count = 0
                        pr_reviewers = []

                    # ... other code ...

                pr_reviewers = [
                    review["author"]["login"] for review in pr["reviews"]["nodes"]
                ]
                pr_comments_count = pr["comments"]["totalCount"]

                pull_request_df = pull_request_df.append(
                    {
                        "PullRequestTitle": pr_title,
                        "PullRequestNumber": pr_number,
                        "PullRequestState": pr_state,
                        "PullRequestCreatedAt": pr_created_at,
                        "PullRequestUpdatedAt": pr_updated_at,
                        "PullRequestClosedAt": pr_closed_at,
                        "PullRequestMergedAt": pr_merged_at,
                        "PullRequestAuthor": pr_author,
                        "PullRequestReviewsCount": pr_reviews_count,
                        "PullRequestReviewers": pr_reviewers,
                        "PullRequestCommentsCount": pr_comments_count,
                    },
                    ignore_index=True,
                )

                print(pr_number)

            if info["data"]["repository"]["pullRequests"]["pageInfo"]["hasNextPage"]:
                cursor = f'"{info["data"]["repository"]["pullRequests"]["pageInfo"]["endCursor"]}"'
            else:
                break

            # Save the data after each API request
            pull_request_df.to_csv("aave_v3.csv", index=False, sep=",")

        else:
            print(name + owner)
            print("Error Code " + str(request.status_code))
            break

    if len(pull_request_df) > 0:
        break

# Save the final data
pull_request_df.to_csv("aave_v3.csv", index=False, sep=",")
