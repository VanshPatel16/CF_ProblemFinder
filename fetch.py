import requests
import json
import pandas as pd

def createCSV(names,ratings,urls):
    names = pd.Series(names)
    ratings = pd.Series(ratings)
    urls = pd.Series(urls)
    problems = pd.DataFrame({
        'name' : names.values,
        'rating' : ratings.values,
        'url' : urls.values
    })
    print("Shape = " + str(problems.shape))
    problems.to_csv("problems.csv",index=False)

def createProblemURL (contestId,problemIndex):
    str = "https://codeforces.com/problemset/problem/{}/{}".format(contestId,problemIndex)
    return str

def getProblemID (contestId,problemIndex):
    probID = str(contestId) + problemIndex
    return probID

def getUserProblemSet(username,L,R):
    r = requests.get("https://codeforces.com/api/user.status?handle={}".format(username))
    if(r.status_code != requests.codes.ok):
        print("Couldnt fetch object!")

    r = json.loads(r.text)
    if(r["status"] != "OK"):
        print("Error fetching your data!!")
        exit(0)
    
    solved_problems = set()
    submissions = r["result"]
    for submission in submissions:
        if(submission["verdict"] == "OK"):
            # special problems having no rating will not have rating field
            try:
                submission["problem"]["rating"]
            except KeyError:
                continue
        
        if(submission["verdict"] == "OK" and submission["problem"]["rating"] >= L and submission["problem"]["rating"] <= R):
            solved_problems.add(getProblemID(submission["problem"]["contestId"],submission["problem"]["index"]))

    
    return solved_problems

def getProblems(user_list,username,L,R):
    failed_list = []
    solved_problems = getUserProblemSet(username,L,R)
    problems = set()
    for userID in user_list:
        r = requests.get("https://codeforces.com/api/user.status?handle={}".format(userID))
        if(r.status_code != requests.codes.ok):
            print("Couldnt fetch user object! for {}".formate(userID))
            failed_list.append(userID)
            continue

        r = json.loads(r.text)
        if(r["status"] != "OK"):
            failed_list.append(userID)
            continue

        submissions = r["result"]
        for submission in submissions:
            if(submission["verdict"] == "OK"):
                # special problems having no rating will not have rating field
                try:
                    submission["problem"]["rating"]
                except KeyError:
                    continue
            
            if(submission["verdict"] == "OK" and submission["problem"]["rating"] >= L and submission["problem"]["rating"] <= R):
                problemID = getProblemID(submission["problem"]["contestId"],submission["problem"]["index"])
                if problemID in solved_problems:
                    # If the user has already solved the problem do not add it.
                    continue
                problem_name = submission["problem"]["name"]
                problem_rating = submission["problem"]["rating"]
                problem_url = createProblemURL(submission["problem"]["contestId"],submission["problem"]["index"])
                problems.add((problem_name,problem_rating,problem_url))

    problemNames = []
    problemRatings = []
    problemUrls = []
    for n,r,u in problems:
        problemNames.append(n)
        problemRatings.append(r)
        problemUrls.append(u)
    if len(failed_list) > 0 :
        print("Failed userID's : ",end=' ')
        print(failed_list)
    return problemNames,problemRatings,problemUrls

print("Enter your username : ")
username = input()
print("Enter user list : ")
user_list = (input().split())
print("Enter the rating range [L,R] : ")
L,R = map(int,(input().split()))
names,ratings,urls = getProblems(user_list,username,L,R)
createCSV(names,ratings,urls)