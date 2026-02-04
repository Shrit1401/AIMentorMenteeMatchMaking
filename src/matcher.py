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
    