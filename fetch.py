import requests
import json


def createProblemURL (contestId,problemIndex):
    str = "https://codeforces.com/problemset/problem/{}/{}".format(contestId,problemIndex)
    return str
def getProblems(username,L,R):
    r = requests.get("https://codeforces.com/api/user.status?handle={}&from=1&count=200".format(username))
    if(r.status_code != requests.codes.ok):
        print("Couldnt fetch object!")

    r = json.loads(r.text)
    if(r["status"] != "OK"):
        print("Error fetching data!")
    submissions = r["result"]
    problemNames = []
    problemRatings = []
    problemUrls = []
    for submission in submissions:
        if(submission["verdict"] == "OK" and submission["problem"]["rating"] >= L and submission["problem"]["rating"] <= R):
            
            problem_name = submission["problem"]["name"]
            problem_rating = submission["problem"]["rating"]
            problem_url = createProblemURL(submission["problem"]["contestId"],submission["problem"]["index"])
            problemNames.append(problem_name)
            problemRatings.append(problem_rating)
            problemUrls.append(problem_url)

    return problemNames,problemRatings,problemUrls

print("Enter userame : ")
username = input()
print("Enter the rating range [L,R] : ")
L,R = map(int,(input().split()))
names,ratings,urls = getProblems(username,L,R)