from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.sql import func
from auth.models import User, SearchHistory, Product
import numpy as np

# Collaborative Filtering
def collaborative_filtering(user_id):
    # Find other users with search history
    similar_users = User.query.join(SearchHistory).filter(SearchHistory.user_id != user_id).all()
    
    # Collect products that similar users have interacted with
    recommended_products = []
    for user in similar_users:
        user_searches = SearchHistory.query.filter_by(user_id=user.id).all()
        
        for search in user_searches:
            # Assuming 'results' field is JSON or a list of product IDs
            product_ids = search.results  # Ensure this is a list of product IDs
            if isinstance(product_ids, list):
                products = Product.query.filter(Product.id.in_(product_ids)).all()
                recommended_products.extend(products)

    # Filter duplicates and return top 5 unique products
    unique_products = list({product.id: product for product in recommended_products}.values())
    return unique_products[:5]  # Return top 5 recommendations

# Content-Based Filtering
def content_based_filtering(user_id):
    # Get user's search history
    user_history = SearchHistory.query.filter_by(user_id=user_id).all()
    
    if not user_history:
        return []  # Return empty if no search history
    
    queries = [history.query for history in user_history]

    # TF-IDF vectorization of the product titles and user queries
    vectorizer = TfidfVectorizer(stop_words='english')
    all_products = Product.query.all()
    
    if not all_products:
        return []  # Return empty if no products available
    
    all_titles = [product.title for product in all_products]

    # Fit-transform with user queries and all product titles
    vectors = vectorizer.fit_transform(queries + all_titles)

    # Calculate cosine similarity between user queries and product titles
    user_vector = vectors[:len(queries)]
    product_vectors = vectors[len(queries):]
    similarity_scores = cosine_similarity(user_vector, product_vectors)

    # Average similarity scores across all user queries
    avg_similarity_scores = np.mean(similarity_scores, axis=0)

    # Find top products based on similarity scores
    top_indices = avg_similarity_scores.argsort()[-5:][::-1]  # Get top 5 indices, reversed for descending order
    top_products = [all_products[i] for i in top_indices]

    return top_products

# Helper function to format recommendations
def format_recommendations(recommendations):
    if not recommendations:
        return "No recommendations available at this time."

    formatted_results = "Top Recommendations:\n"
    for product in recommendations:
        formatted_results += f"Product: {product.title}\nPrice: {product.price}\nRating: {product.rating}\nLink: {product.link}\n\n"
    
    return formatted_results
