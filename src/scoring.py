from typing import Tuple

import torch.nn.functional as F
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

tfidf_vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    stop_words="english",
)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def semanticSimilarity(sub1: str, sub2: str) -> float:
    emb1 = embedding_model.encode(sub1, convert_to_tensor=True)
    emb2 = embedding_model.encode(sub2, convert_to_tensor=True)
    return float(F.cosine_similarity(emb1, emb2, dim=0).item())


def tfidfSimilarity(sub1: str, sub2: str) -> float:
    vectors = tfidf_vectorizer.fit_transform([sub1.lower(), sub2.lower()])
    return float(cosine_similarity(vectors[0], vectors[1])[0][0])


def _subdomain_similarity(sub1: str, sub2: str) -> float:
    try:
        return semanticSimilarity(sub1, sub2)
    except Exception:
        return tfidfSimilarity(sub1, sub2)


def _subdomain_reason(similarity: float) -> str:
    if similarity >= 0.75:
        return "Same or very similar subdomain"
    if similarity >= 0.4:
        return "Related subdomain"
    return "Different subdomain"


def calculateScore(mentee, mentor) -> Tuple[int, str]:
    mentee_domain = str(mentee["research_domain"]).lower()
    mentor_domain = str(mentor["research_domain"]).lower()
    if mentee_domain != mentor_domain:
        return 0, "Different research domain"

    similarity = _subdomain_similarity(
        str(mentee["subdomain"]),
        str(mentor["subdomain"]),
    )
    sub_score = int(similarity * 30)
    score = min(70 + sub_score, 100)
    reasons = [
        f"Same domain ({mentee['research_domain']})",
        _subdomain_reason(similarity),
    ]
    return score, " and ".join(reasons)