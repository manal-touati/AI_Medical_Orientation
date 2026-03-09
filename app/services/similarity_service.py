from sklearn.metrics.pairwise import cosine_similarity


class SimilarityService:
    @staticmethod
    def compute_similarity(user_vector, reference_vectors):
        return cosine_similarity([user_vector], reference_vectors)[0]