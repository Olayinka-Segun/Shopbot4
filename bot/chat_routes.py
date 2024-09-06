from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from bot.nlp_module import ChatbotNLP
from auth.models import db, SearchHistory
from scraper.scraper import scrape_all_sites  # Make sure this function exists and is correct

chat_bp = Blueprint('chat_bp', __name__)
chatbot_nlp = ChatbotNLP()  # Initialize the ChatbotNLP class

@chat_bp.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    response = None
    products = []
    
    if request.method == 'POST':
        user_message = request.form.get('message')
        
        if not user_message:
            flash('Message cannot be empty', 'warning')
            return redirect(url_for('chat_bp.chat'))
        
        # Generate a response from the chatbot
        try:
            response = chatbot_nlp.generate_response(user_message)
        except Exception as e:
            response = f"An error occurred while generating the response: {str(e)}"

        # Handle saving search history and searching for products
        intent = chatbot_nlp.classify_intent(user_message)
        if intent == 'product_search':
            query = chatbot_nlp.extract_product_query(user_message)
            if query:
                # Save search history
                try:
                    search_history = SearchHistory(
                        user_id=current_user.id,
                        query=query,
                        search_time=datetime.utcnow(),
                        results=None  # Store actual results if available
                    )
                    db.session.add(search_history)
                    db.session.commit()
                    
                    # Perform the product search
                    products = scrape_all_sites(query)  # Ensure this function returns product data
                except Exception as e:
                    flash(f"An error occurred while saving search history or scraping: {str(e)}", 'danger')

    return render_template('chat.html', response=response, products=products)
