from typing import Dict, List, Tuple

import pandas as pd

from src.scoring import calculateScore


def findBestMentor(mentee: Dict, mentorsCSV: pd.DataFrame) -> Tuple[str, int, str]:
    bestScore = -1
    bestMentor = ""
    bestReason = ""

    for _, mentor in mentorsCSV.iterrows():
        score, reason = calculateScore(mentee, mentor)
        if score > bestScore:
            bestScore = score
            bestMentor = mentor["name"]
            bestReason = reason

    return bestMentor, bestScore, bestReason


def rankTopMentors(
    mentee: Dict, mentorsCSV: pd.DataFrame, topK: int = 3
) -> List[Dict]:
    ranked = []
    for _, mentor in mentorsCSV.iterrows():
        score, reason = calculateScore(mentee, mentor)
        ranked.append(
            {"mentor": mentor["name"], "score": score, "reason": reason}
        )

    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked[: max(int(topK), 0)]


def FindBestMentor(mentee: Dict, mentorCSV: pd.DataFrame):
    return findBestMentor(mentee, mentorCSV)