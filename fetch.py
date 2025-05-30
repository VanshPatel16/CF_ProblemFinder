import requests
import json
import pandas as pd
import streamlit as st
def createCSV(problems):
    problems.to_csv("problems.csv",index=False)

def getDataFrame(names,ratings,urls):
    df = pd.DataFrame({'Name' : names,'Rating' : ratings,'URL' : urls})
    return df
def createProblemURL (contestId,problemIndex):
    str = "https://codeforces.com/problemset/problem/{}/{}".format(contestId,problemIndex)
    return str

def getProblemID (contestId,problemIndex):
    probID = str(contestId) + problemIndex
    return probID

def getUserProblemSet(username,L,R):
    r = requests.get("https://codeforces.com/api/user.status?handle={}".format(username))
    if(r.status_code != requests.codes.ok):
        st.error("Couldnt fetch object!")

    r = json.loads(r.text)
    if(r["status"] != "OK"):
        st.error("Error fetching your data!!")
        exit(0)
    
    solved_problems = set()
    submissions = r["result"]
    for submission in submissions:
        if(submission["verdict"] == "OK"):
            # special problems having no rating will not have rating field
            try:
                _ = submission["problem"]["rating"]
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
            st.error("Couldnt fetch user object! for {}".format(userID))
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
                    _ = submission["problem"]["rating"]
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

    
    if len(failed_list) > 0 :
        st.error("Failed userID's : ",end=' ')
        st.error(failed_list)
    return zip(*problems) if problems else ([],[],[])


st.title("Welcome to CF Problem Finder!")
st.markdown("""
            Tired of finding problems from codeforces? Does sorting by solve count feelboring to you?
            Do not want the hassle of codeforces user-list ? Then CF Problem Finder is the right tool for you!
            
            
            """)
username = st.text_input("Enter your codeforces username : ")
user_list = st.text_input("Enter the list of users (space seperated): ")
L = st.number_input("Enter the lower bound of rating : ")
R = st.number_input("Enter the upper bound of rating : ")

if st.button("Find Problems"):
    if username and user_list:
        user_list = user_list.strip().split()
        names,ratings,urls = getProblems(user_list,username,L,R)
        df = getDataFrame(names,ratings,urls)
        st.success(f"Found {len(df)} problems")
        st.dataframe(df,)
        createCSV(df)
        st.download_button("Download CSV",data=df.to_csv(index=False),file_name="problems.csv")
    else:
        st.warning("Enter both username and user list!!")


