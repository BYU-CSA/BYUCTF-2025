import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, url_for

from Models.Recipe import Recipe
from DAOs.Recipe_DAO import RecipeDAO

# Load env and start the flask app
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET')

# Redirect from the main page
@app.route('/', methods=['GET'])
def main_page():
    return redirect(url_for('search'))

# Search Request
@app.route('/search', methods=['GET'])
def search():
    # Get items from the request args in the URL
    recipe_name = request.args.get('recipe_name', '')
    description = request.args.get('description', '')
    tags = request.args.getlist('tags')  # Gets all selected tags

    # Handle the case where the form is submitted without any criteria
    searchDetails = [
        isinstance(recipe_name, str) or recipe_name is None,
        isinstance(description, str) or description is None,
        isinstance(tags, list) or tags is None
    ]
    if not any(searchDetails):
        flash('Please enter search criteria.', 'error')
        return render_template('search.html')

    # Make the search
    recipes:list[Recipe] = RecipeDAO().retrieve_recipes_from_search(recipe_name, description, tags)
    items = []
    for recipe in recipes:
        tup = (recipe, False, False)
        items.append(tup)
    
    # Return the matching items
    return render_template('search.html', items=items)

# listen on port 1337
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337, debug=True)