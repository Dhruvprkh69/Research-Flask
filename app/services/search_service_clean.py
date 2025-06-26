class SearchService:
    def find_similar_papers(self, concept, category, max_results=5):
        return [
            {"title": f"Placeholder paper about {concept}", "category": category, "score": 0.99}
            for _ in range(max_results)
        ]

    def get_paper_details(self, paper_id):
        return {"title": "Placeholder Paper", "id": paper_id}

    def get_trending_papers(self, category, max_results=5):
        return [
            {"title": f"Trending paper in {category}", "score": 0.95}
            for _ in range(max_results)
        ] 