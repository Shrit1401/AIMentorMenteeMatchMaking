import os
from src.loadData import loadData
from src.compare import compareMenteeWithMentor
from src.matcher import FindBestMentor

def main():
    menteesCSV, mentorsCSV = loadData()
    results = []
    
    for _, mentee in menteesCSV.iterrows():
        mentor, score, reason = FindBestMentor(mentee, mentorsCSV)
        results.append({
            "menteeName": mentee["name"],
            "MatchedMentor": mentor,
            "Reason": reason,
            "ConfidenceScore": score
        })
    outputCSV = pd.DataFrame(results)
    os.makedirs("output", exist_ok=True)
    outputCSV.to_csv("output/results.csv", index=False)

    print(f"Results saved to output/results.csv")

if __name__ == "__main__":
    import pandas as pd
    main()