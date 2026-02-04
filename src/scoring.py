from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    stop_words="english"
)


def calculateSubdomainSimilarity(sub1, sub2):
    # vectorizing = converting the text into a vector of numbers
    vectors = vectorizer.fit_transform([sub1.lower(), sub2.lower()])
    # cosine_similarity  calculates the similarity between two vectors
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    return similarity

def calculateScore(mentee, mentor):
    score = 0
    reasons = []
    if mentee["research_domain"].lower() != mentor["research_domain"].lower():
        return 0, "Different research domain"
    
    score += 70
    reasons.append(f"Same domain ({mentee['research_domain']})")
    
    similarity = calculateSubdomainSimilarity(
        mentee["subdomain"],
        mentor["subdomain"]
    )
    
    subScore = int(similarity * 30)
    score += subScore
    
    if similarity >= 0.75:
        reasons.append("Same or very similar subdomain")
    elif similarity >= 0.4:
        reasons.append("Related subdomain")
    else:
        reasons.append("Different subdomain")

    return min(score, 100), ", ".join(reasons)
