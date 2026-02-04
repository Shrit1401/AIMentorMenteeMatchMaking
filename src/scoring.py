from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sentence_transformers import SentenceTransformer, util


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
tfidf_vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    stop_words="english"
)


vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    stop_words="english"
)

def semantic_similarity(sub1, sub2):
    emb1 = embedding_model.encode(sub1, convert_to_tensor=True)
    emb2 = embedding_model.encode(sub2, convert_to_tensor=True)
    similarity = util.cos_sim(emb1, emb2).item()
    return similarity

def tfidf_similarity(sub1, sub2):
    vectors = tfidf_vectorizer.fit_transform([sub1.lower(), sub2.lower()])
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    return similarity


def calculateScore(mentee, mentor):
    if mentee["research_domain"].lower() != mentor["research_domain"].lower():
        
        return 0, "Different research domain"
    score = 70
    reasons = [f"Same domain ({mentee['research_domain']})"]
    
    if mentee["research_domain"].lower() != mentor["research_domain"].lower():
        return 0, "Different research domain"
    
    try:
        similarity = semantic_similarity(
            mentee["subdomain"],
            mentor["subdomain"]
        )
        similarity_source = "semantic"
    except Exception:
        similarity = tfidf_similarity(
            mentee["subdomain"],
            mentor["subdomain"]
        )
        similarity_source = "tfidf"

    sub_score = int(similarity * 30)
    score += sub_score

    
    subScore = int(similarity * 30)
    score += subScore
    
    if similarity >= 0.75:
        reasons.append("Same or very similar subdomain")
    elif similarity >= 0.4:
        reasons.append("Related subdomain")
    else:
        reasons.append("Different subdomain")

    reasons.append(f"Similarity via {similarity_source}")

    return min(score, 100), ", ".join(reasons)

