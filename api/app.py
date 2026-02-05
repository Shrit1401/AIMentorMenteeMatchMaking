from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from src.loadData import loadMentors
from src.matcher import rankTopMentors

app = FastAPI(title="Mentor Mentee Matchmaking API")
mentorsCSV = loadMentors()

class Mentee(BaseModel):
    name: str
    college: str
    research_domain: str
    subdomain: str

class MatchResponse(BaseModel):
    mentor_name: str
    confidence_score: int
    reason: str

class MenteeMatchResult(BaseModel):
    mentee_name: str
    matches: List[MatchResponse]

@app.post("/match", response_model=List[MenteeMatchResult])
def match_mentees(mentees: List[Mentee]):
    results = []

    for mentee in mentees:
        mentee_dict = mentee.dict()
        top_matches = rankTopMentors(mentee_dict, mentorsCSV)

        formatted_matches = [
            {
                "mentor_name": m["mentor"],
                "confidence_score": m["score"],
                "reason": m["reason"]
            }
            for m in top_matches
        ]

        results.append({
            "mentee_name": mentee.name,
            "matches": formatted_matches
        })

    return results
