import json

from DAOs.GetConnection import get_db_connection
from Models.Recipe import Recipe

class RecipeDAO():
    def retrieve_recipes_from_search(self, recipe_name: str, recipe_description: str, tags: list) -> list:
        """Retrieves recipes matching the search criteria including tags.\n        
        returns: A list of recipes"""

        conn = get_db_connection()
        cursor = conn.cursor()

        # Start building the query dynamically based on provided inputs
        query = "SELECT * FROM recipe WHERE 1=1"
        params = []

        if recipe_name:
            query += " AND recipe_name LIKE ?"
            params.append('%' + recipe_name + '%')

        if recipe_description:
            query += " AND recipe_description LIKE ?"
            params.append('%' + recipe_description + '%')

        if tags:
            tag_conditions = " OR ".join(["json_extract(tags, '$') LIKE '%\"" + tag + "\"%'" for tag in tags])
            query += " AND (" + tag_conditions + ")"
        
        # Execute with SQLite
        print(query)
        cursor.execute(query, params)

        response = cursor.fetchall()
        conn.close()

        # Convert to Recipe Model Objects and return
        recipe_list = [self.__convert_data_to_recipe__(recipe_data) for recipe_data in response]
        return recipe_list

    def __convert_data_to_recipe__(self, recipe_data) -> Recipe:
        recipe_id, recipe_name, date_created, recipe_image, recipe_description, instructions, tags, user_id = recipe_data
        tags =  json.loads(tags)
        recipe = Recipe (
            recipe_id = recipe_id,
            recipe_name = recipe_name,
            date_created = date_created,
            recipe_image = recipe_image,
            recipe_description = recipe_description,
            instructions = instructions,
            tags = tags,
            user_id = user_id
        )
        return recipe