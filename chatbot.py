from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def ask_library_chatbot(question, books):
    """
    AI Library Assistant using TF-IDF and Cosine Similarity
    Works completely offline.
    """

    # Convert books string into a list
    book_lines = [b.strip() for b in books.split("\n") if b.strip()]

    if not book_lines:
        return "No books are available in the library database."

    # Create searchable text
    corpus = book_lines + [question]

    # Convert text to vectors
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(corpus)

    # Compare question with all books
    similarity = cosine_similarity(vectors[-1], vectors[:-1]).flatten()

    # Get top matching books
    top_indices = similarity.argsort()[::-1]

    results = []
    for idx in top_indices:
        if similarity[idx] > 0:
            results.append(book_lines[idx])

    # If no match is found, return books by simple category matching
    if not results:
        q = question.lower()

        if "fiction" in q:
            results = [b for b in book_lines if "fiction" in b.lower()]
        elif "engineering" in q or "engg" in q:
            results = [b for b in book_lines if "engineering" in b.lower() or "general" in b.lower()]
        elif "historical" in q:
            results = [b for b in book_lines if "historical" in b.lower()]
        elif "general" in q:
            results = [b for b in book_lines if "general" in b.lower()]

    if results:
        return "Based on your query, the most relevant books are:\n\n" + "\n".join(results[:5])

    return "Sorry, I could not find any relevant books in the library database."