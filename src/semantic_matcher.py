from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_match(resume_text, jd_text):

    emb1 = model.encode([resume_text])
    emb2 = model.encode([jd_text])

    similarity = cosine_similarity(emb1, emb2)

    return float(similarity[0][0])