import pandas as pd

def loadMentees(path="data/mentees.csv"):
    return pd.read_csv(path)

def loadMentors(path="data/mentors.csv"):
    return pd.read_csv(path)

def loadData():
    mentees = loadMentees()
    mentors = loadMentors()
    return mentees, mentors
