import os
from src.loadData import loadData
from src.matcher import rankTopMentors

def main():
    menteesCSV, mentorsCSV = loadData()
    results = []

    for _, mentee in menteesCSV.iterrows():
        topMentors = rankTopMentors(mentee, mentorsCSV)
        
        for rank, mentorInfo in enumerate(topMentors, start=1):
            results.append({
                "mentee_name": mentee["name"],
                "rank": rank,
                "mentor_name": mentorInfo["mentor"],
                "confidence_score": mentorInfo["score"],
                "reason": mentorInfo["reason"]
            })
    outputCSV = pd.DataFrame(results)
    os.makedirs("output", exist_ok=True)
    outputCSV.to_csv("output/top3.csv", index=False)

    print(f"Results saved to output/top3.csv")

if __name__ == "__main__":
    import pandas as pd
    main()