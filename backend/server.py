# Import flask and config
import config
import psycopg2
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS, cross_origin

# Initializing flask app
app = Flask(__name__, static_folder="../jojo-frontend/build", static_url_path="/")
cors = CORS(app)

@app.route("/characters")
@cross_origin()
def get_characters():
    try:
        search_query = request.args.get("search", "")  # Retrieve search query parameter

        # Establish a connection to the ElephantSQL database
        database_url = f"postgres://{config.USERNAME}:{config.PASSWORD}@{config.SERVER_HOST}/{config.DEFAULT_DB}"
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()

        if search_query:
            # Query with search functionality
            query = f"""SELECT Characters.character_name,
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
                            (Characters.stand_1 = Stands.stand_name
                            OR Characters.stand_2 = Stands.stand_name
                            OR Characters.stand_3 = Stands.stand_name)
                            AND Characters.character_name ILIKE %s
                        GROUP BY Characters.character_name;"""
            cursor.execute(query, ("%" + search_query + "%",))
        else:
            # Query to fetch all characters if no search query provided
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

        data = cursor.fetchall()
        cursor.close()
        conn.close()

        result = jsonify(data)
        return result
    except Exception as e:
        # Handle database connection or query issues
        return jsonify({"error": str(e)})

@app.route("/")
def serve():
    return send_from_directory(app.static_folder, 'index.html')

# Running app
if __name__ == "__main__":
    app.run(debug=True)
