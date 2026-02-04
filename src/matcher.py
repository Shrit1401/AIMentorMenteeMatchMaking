from src.scoring import calculateScore

def FindBestMentor(mentee, mentorCSV):
    bestScore = -1
    bestMentor = None
    bestReason = ""
    
    for _, mentor in mentorCSV.iterrows():
        score, reason = calculateScore(mentee, mentor)
        
        if score > bestScore:
            bestScore = score
            bestMentor = mentor["name"]
            bestReason = reason
            
    return bestMentor, bestScore, bestReason
    
def rankTopMentors(mentee, mentorCSV, topK = 3):
    results= []
    
    for _, mentor in mentorCSV.iterrows():
        score, reason = calculateScore(mentee, mentor)
        results.append({
            "mentor": mentor["name"],
            "score": score,
            "reason": reason
        })
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )
    return results[:topK]