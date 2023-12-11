import pandas as pd
import requests
import json
import time
from datetime import datetime
import os
from settings import TOKEN, FIRST_FILE_INDEX, LAST_FILE_INDEX, NEXT_INDEX_TO_OBSERVE

if __name__ == "__main__":
    first_file_index = FIRST_FILE_INDEX
    last_file_index = LAST_FILE_INDEX

    file_paths = [os.path.join("data", "tssb_data_3M", f"file-{index}.jsonl") for index in range(first_file_index, last_file_index+1)]

    data_list = []

    for file_path in file_paths:
        with open(file_path, 'r') as file:
            for line in file:
                data_dict = json.loads(line)
                data_list.append(data_dict)

    df = pd.DataFrame(data_list)

    del data_list, file_paths

    print("Data loaded successfully.")

    # Enter your personal token.
    token = TOKEN

    # The limit of GitHub API requests per hour.
    github_limit = 1000

    dataset_size = df.shape[0]
    numberof_partitions = dataset_size // github_limit + 1
    partitions_boundaries = [github_limit * (i) for i in range(numberof_partitions)] 
    partitions_boundaries += [partitions_boundaries[-1] + dataset_size % github_limit]

    #Make it with os
    extracted_data_path = os.path.join("data", "commits")

    for baundary_index in range(NEXT_INDEX_TO_OBSERVE, numberof_partitions):
        commits = []
        errors = []
        
        for data_index in range(partitions_boundaries[baundary_index], partitions_boundaries[baundary_index + 1]):
            username, reponame = df["project_url"][data_index].split('/')[-2:]
            commit_sha = df["commit_sha"][data_index]

            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json"
            }

            commit_url = f"https://api.github.com/repos/{username}/{reponame}/commits/{commit_sha}"
            commit_response = requests.get(commit_url, headers=headers)

            while "API rate limit exceeded" in commit_response.text:
                commit_response = requests.get(commit_url, headers=headers)

                print("Hourly limit exceeded. Next attempt in five minute.")

                time.sleep(300)

            if commit_response.status_code == 200:
                commit_details = commit_response.json()
                commits.append({
                    "username": username,
                    "reponame": reponame,
                    "commit_sha": commit_sha,
                    "likely_bug": bool(df["likely_bug"][data_index]),
                    "before": df["before"][data_index],
                    "after": df["after"][data_index],
                    "message": commit_details["commit"]["message"],
                    "sstub_pattern": df["sstub_pattern"][data_index]
                })

            else:
                print("Error:", commit_response.status_code, commit_response.text, username, reponame, commit_sha)

                errors.append({
                    "username": username,
                    "reponame": reponame,
                    "commit_sha": commit_sha,
                    "response_code": commit_response.status_code,
                    "response_text": commit_response.text
                })
        
        with open(os.path.join(extracted_data_path, ("commits_" + str(baundary_index) + ".json")), "w") as file:
            json.dump(commits, file)
        
        with open(os.path.join(extracted_data_path, ("errors_" + str(baundary_index) + ".json")), "w") as file:
            json.dump(errors, file)

        print("Last Index Observed: " + str(baundary_index) + " | Time: " + str(datetime.now()))

    del partitions_boundaries, commits, errors