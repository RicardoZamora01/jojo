# Import flask and datetime module for showing date and time
import datetime

import psycopg2
from flask import Flask, jsonify
import config

x = datetime.datetime.now()

# Initializing flask app
app = Flask(__name__)





# Route for seeing a data
@app.route("/data")
def get_time():
    # Returning an api for showing in  reactjs
    return {"Name": "geek", "Age": "22", "Date": x, "programming": "python"}


# Route for getting all characters
@app.route("/characters")
def get_characters():
    try:
        # Establish a connection to the ElephantSQL database
        database_url = f"postgres://{config.USERNAME}:{config.PASSWORD}@{config.SERVER_HOST}/{config.DEFAULT_DB}"
        conn = psycopg2.connect(database_url)

        # Create a cursor to execute SQL queries
        cursor = conn.cursor()

        # Query to fetch user profile by user_id
        query = """SELECT Characters.character_name,
                    jsonb_agg(Stands.stand_name) AS stand_names,
                    jsonb_agg(
                        jsonb_build_object(
                            'stand_power', Stands.stand_power,
                            'stand_speed', Stands.stand_speed,
                            'stand_range', Stands.stand_range,
                            'stand_durability', Stands.stand_durability,
                            'stand_precision', Stands.stand_precision,
                            'stand_development_potential', Stands.stand_development_potential
                        )
                    ) AS stand_attributes
                FROM Characters
                CROSS JOIN Stands
                WHERE
                    Characters.stand_1 = Stands.stand_name
                    OR Characters.stand_2 = Stands.stand_name
                    OR Characters.stand_3 = Stands.stand_name
                GROUP BY Characters.character_name;"""
        
        cursor.execute(query)

        # Fetch the data from the database
        data = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Convert the data to a JSON response
        result = jsonify(data)

        return result
    except Exception as e:
        # Handle database connection or query errors
        return jsonify({'error': str(e)})

# Running app
if __name__ == "__main__":
    app.run(debug=True)
