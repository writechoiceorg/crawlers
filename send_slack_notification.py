import requests
import os
import sys


def send_slack_notification(message, assignee, origin_repo):
    webhook_url = "https://hooks.slack.com/triggers/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"
    print(webhook_url)
    if webhook_url is None:
        print("SLACK_WEBHOOK_URL environment variable is not set.")
        sys.exit(1)
    data = {"Message": message, "Assignee": assignee, "Origin_Repo": origin_repo}
    print(data)
    headers = {"Content-type": "application/json"}
    response = requests.post(webhook_url, json=data, headers=headers)

    print(f"Status code: {response.status_code}")
    print("Response content:", response.content.decode("utf-8"))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: send_slack_notification.py <message> <assignee> <origin_repo>")
        sys.exit(1)

    message = sys.argv[1]
    assignee = sys.argv[2]
    origin_repo = sys.argv[3]
    send_slack_notification(message, assignee, origin_repo)
