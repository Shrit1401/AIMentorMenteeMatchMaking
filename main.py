import os
import pandas as pd
from src.loadData import loadData
from src.matcher import rankTopMentors

def main():
    menteesCSV, mentorsCSV = loadData()
    results = []
    top3_results = []

    for _, mentee in menteesCSV.iterrows():
        topMentors = rankTopMentors(mentee, mentorsCSV, topK=3)
        best = topMentors[0]
        results.append({
            "mentee_name": mentee["name"],
            "mentor_name": best["mentor"],
            "confidence_score": best["score"],
            "reason": best["reason"]
        })
        for rank, mentorInfo in enumerate(topMentors, start=1):
            top3_results.append({
                "mentee_name": mentee["name"],
                "rank": rank,
                "mentor_name": mentorInfo["mentor"],
                "confidence_score": mentorInfo["score"],
                "reason": mentorInfo["reason"]
            })

    os.makedirs("output", exist_ok=True)
    pd.DataFrame(results).to_csv("output/result.csv", index=False)
    pd.DataFrame(top3_results).to_csv("output/top3.csv", index=False)
    print("Results saved to output/result.csv and output/top3.csv")

if __name__ == "__main__":
    main()