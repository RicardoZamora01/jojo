import psycopg2
import requests
from bs4 import BeautifulSoup
from Character import Character
from psycopg2 import IntegrityError
import config

global parts  # global variable to store the parts of JoJo's Bizarre Adventure
parts = [
    "Stardust Crusaders",
    "Diamond is Unbreakable",
    "Vento Aureo",
    "Stone Ocean",
    "Steel Ball Run",
    "JoJolion",
    "The JOJOLands",
]


# Web scraping function to set the data in the database
def get_stand_with_stats_data():
    url = "https://jojowiki.com/Stand_Stats"

    print("Getting data from", url)

    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        response.raise_for_status()

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the stand table on the page
        stand_table = soup.find("table")

        # Finds all table rows in the table body
        stands_list = stand_table.find("tbody").find_all("tr")

        scraped_stands = []
        # Iterate through the stands list
        for stand in stands_list[1:]:
            # Split the text of each row by new line
            split = stand.text.split("\n")
            # Remove the first and last elements of the list since they are empty str
            split = split[1:-1]
            #
            stand_name = split[0]
            if "(" in stand_name and ")" in stand_name:
                # Remove the parentheses from the stand name
                stand_name = stand_name.replace("(", "").replace(")", "")
                split[0] = stand_name
            # Append the tuple to the scraped_stands list
            scraped_stands.append(tuple(split))

        return scraped_stands

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)


def get_stand_no_stats_data():
    url = "https://jojowiki.com/List_of_Stands"
    # Initialize a list to store the stands with no stats
    stands_no_stats = []

    print("Getting data from", url)

    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        response.raise_for_status()

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        tabs = soup.find("section", class_="tabber__section")
        articles = tabs.find_all("article", class_="tabber__panel")

        # Initialize a list to store the filtered articles
        filtered_articles = []

        for article in articles:
            # Check if the "data-title" attribute does not contain "Light Novels" or "Miscellaneous"
            data_title = article.get("data-title")
            if data_title is not None and data_title in parts:
                filtered_articles.append(article)

        stands = []

        # Iterate through the filtered articles and find all the stands in parts 3-9
        for article in filtered_articles:
            data_title = article.get("data-title")
            stand_elements = article.find_all("span", class_="charwhitelink")
            stands.extend(stand_elements)

        # Replace stand elements with the text of the stand
        for i in range(len(stands)):
            stands[i] = stands[i].text

        # Get the stand names from the scraped stands with stats data
        stands_with_stats = get_stand_with_stats_data()

        # Get the stand names from the scraped stands with stats data
        stands_with_stats_list = [stand[0] for stand in stands_with_stats]

        # Iterate through the stands list and append the stand name to the
        # stands_no_stats list if it is not in the stands_with_stats_list
        for stand in stands:
            if stand == "Echoes":
                continue
            if stand not in stands_with_stats_list and (stand,) not in stands_no_stats:
                stands_no_stats.append((stand,))

        return stands_no_stats

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)


# Create Stands table and insert data into it
def set_stands_db():
    # Connect to the PostgreSQL database server
    try:
        # Establish a connection to the ElephantSQL database
        database_url = f"postgres://{config.USERNAME}:{config.PASSWORD}@{config.SERVER_HOST}/{config.DEFAULT_DB}"
        conn = psycopg2.connect(database_url)


        # Create a cursor to execute SQL queries
        cursor = conn.cursor()

        # Create a table (if it doesn't exist)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Stands (
                id SERIAL PRIMARY KEY,
                stand_name VARCHAR(255),
                stand_power VARCHAR(10),
                stand_speed VARCHAR(10),
                stand_range VARCHAR(10),
                stand_durability VARCHAR(10),
                stand_precision VARCHAR(10),
                stand_development_potential VARCHAR(10)

            )
        """
        )

        # Define the scraped data
        stands_data = get_stand_with_stats_data()

        # Insert stands with stats data into the table
        for data_point in stands_data:
            try:
                # Check if the stand_name already exists in the table
                cursor.execute(
                    """
                    SELECT id
                    FROM Stands
                    WHERE stand_name = %s
                    """,
                    (
                        data_point[0],
                    ),  # Assuming stand_name is the first element in data_point
                )
                existing_id = cursor.fetchone()

                if not existing_id:
                    # Insert data into the table if stand_name doesn't exist
                    cursor.execute(
                        """
                        INSERT INTO Stands (stand_name, stand_power, stand_speed, stand_range, stand_durability, stand_precision, stand_development_potential)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        data_point,
                    )
                # else:
                # print(f"Skipping duplicate data: {data_point[0]}")
            except IntegrityError as e:
                # Handle other integrity errors if necessary
                print(f"IntegrityError: {e}")
                conn.rollback()  # Rollback the transaction

        stands_no_stats_data = get_stand_no_stats_data()

        # Insert stands with no stats data into the table where stats are "N/A"
        for data_point in stands_no_stats_data:
            try:
                # Check if the stand_name already exists in the table
                cursor.execute(
                    """
                    SELECT id
                    FROM Stands
                    WHERE stand_name = %s
                    """,
                    (
                        data_point,
                    ),  # Assuming stand_name is the first element in data_point
                )
                existing_id = cursor.fetchone()

                if not existing_id:
                    # Insert data into the table if stand_name doesn't exist
                    cursor.execute(
                        """
                        INSERT INTO Stands (stand_name, stand_power, stand_speed, stand_range, stand_durability, stand_precision, stand_development_potential)
                        VALUES (%s, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A')
                        """,
                        data_point,
                    )
                else:
                    print(f"Skipping duplicate data: {data_point[0]}")

            except IntegrityError as e:
                # Handle other integrity errors if necessary
                print(f"IntegrityError: {e}")
                conn.rollback()  # Rollback the transaction

        # Commit changes and close the connection
        conn.commit()
        conn.close()
        print("Data stored successfully in the database.")
    except Exception as e:
        print(f"Error storing data in the database: {e}")


def get_stand_db_data():
    # Connect to the PostgreSQL database server
    try:
        # Establish a connection to the ElephantSQL database
        database_url = f"postgres://{config.USERNAME}:{config.PASSWORD}@{config.SERVER_HOST}/{config.DEFAULT_DB}"
        conn = psycopg2.connect(database_url)

        # Create a cursor to execute SQL queries
        cursor = conn.cursor()

        # Select all data from the table
        cursor.execute("SELECT stand_name FROM Stands")

        # Fetch all rows from the result set
        stands = cursor.fetchall()

        # Close the connection
        conn.close()

        result_list = [row[0] for row in stands]

        print("Data retrieved successfully from the database.")
        return result_list
    except Exception as e:
        print(f"Error retrieving data from the database: {e}")


# Web scraping function to map stands to characters, works with Jotaro, less characters
def map_stand_to_character(character_link):
    stands = []

    try:
        # Send an HTTP GET request to the URL
        response = requests.get(character_link)

        # Check if the request was successful (status code 200)
        response.raise_for_status()

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Find Stand span element
        stand_span = (
            soup.find("div", id="mw-content-text")
            .find("div", class_="mw-parser-output")
            .find_all("dl")
        )

        stands_db_data = get_stand_db_data()

        for s in stand_span:
            stand = s.find("a").text

            if stand in stands_db_data:
                stands.append(stand)
        return stands

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)


# more elaborate version of map_stand_to_character, works with more characters, but not Jotaro
def map_stand_to_character2(character_link):
    stands = []

    try:
        # Send an HTTP GET request to the URL
        response = requests.get(character_link)

        # Check if the request was successful (status code 200)
        response.raise_for_status()

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        character_stand = soup.find_all("div", class_="abilityname diamond")

        stands_db_data = get_stand_db_data()

        for stand in character_stand:
            stand = stand.find("a").text
            if stand in stands_db_data:
                stands.append(stand)
                
        return stands

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)


def get_character_data(url):
    print("Getting data from", url)

    part = url[url.rfind("Part_") + 5]


    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        response.raise_for_status()

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        parent_div = soup.find("div", class_="diamond2")
        stand_anchors = parent_div.find_all("a")

        characters = []
        visited_links = []
        all_stands = set()

        base_url = "https://jojowiki.com"

        for anchor in stand_anchors:
            if anchor.text:
                character_link = base_url + anchor["href"]

                # DELETE THIS -- TO DO: maybe add none for Mansaku Nijimura's stand
                # if character_link == "https://jojowiki.com/Koichi_Hirose%27s_Mother":
                #     break

                if anchor.text == "Anubis":
                    characters.append(
                        Character(anchor.text, character_link, ["Anubis"])
                    )
                    all_stands.add("Anubis")
                    continue
                if character_link in visited_links:
                    continue

                # print("stand:", map_stand_to_character2(character_link))
                if "Part_3" in url:
                    stands = map_stand_to_character(character_link)
                else:
                    stands = map_stand_to_character2(character_link)

                visited_links.append(character_link)
                all_stands.update(stands)
                character = Character(anchor.text, character_link, stands)
                characters.append(character)

        return characters

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)


def set_characters_to_tuple_data():
    part_three_url = "https://jojowiki.com/Category:Part_3_Characters"
    part_four_url = "https://jojowiki.com/Category:Part_4_Characters"
    part_five_url = "https://jojowiki.com/Category:Part_5_Characters"
    part_six_url = "https://jojowiki.com/Category:Part_6_Characters"
    part_seven_url = "https://jojowiki.com/Category:Part_7_Characters"
    part_eight_url = "https://jojowiki.com/Category:Part_8_Characters"
    part_nine_url = "https://jojowiki.com/Category:Part_9_Characters"

    part_three_characters = get_character_data(part_three_url)
    part_four_characters = get_character_data(part_four_url)
    part_five_characters = get_character_data(part_five_url)
    part_six_characters = get_character_data(part_six_url)
    part_seven_characters = get_character_data(part_seven_url)
    part_eight_characters = get_character_data(part_eight_url)
    part_nine_characters = get_character_data(part_nine_url)

    all_characters = (
        part_three_characters
        + part_four_characters
        + part_five_characters
        + part_six_characters
        + part_seven_characters
        + part_eight_characters
        + part_nine_characters
    )
    tuple_data = []

    for character in all_characters:
        if character.stands != []:
            base_character = (character.name, character.link)
            character_tuple = base_character + tuple(character.stands)

            # if stands are less than 3, add N/A to the tuple

            while len(character_tuple) < 6:
                character_tuple += ("N/A",)

            tuple_data.append(character_tuple)

            # for stand in character.stands:
            #     tuple_data.append((character.name, character.link, stand))
        else:
            tuple_data.append(
                (character.name, character.link, "N/A", "N/A", "N/A", "N/A")
            )

    return tuple_data


# Create Stands table and insert data into it
def set_characters_db():
    # Connect to the PostgreSQL database server
    try:
        # Establish a connection to the ElephantSQL database
        database_url = f"postgres://{config.USERNAME}:{config.PASSWORD}@{config.SERVER_HOST}/{config.DEFAULT_DB}"
        conn = psycopg2.connect(database_url)

        # Create a cursor to execute SQL queries
        cursor = conn.cursor()

        # Create a table (if it doesn't exist)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Characters (
                id SERIAL PRIMARY KEY,
                character_name VARCHAR(255),
                link VARCHAR(255),
                stand_1 VARCHAR(255),
                stand_2 VARCHAR(255),
                stand_3 VARCHAR(255),
                stand_4 VARCHAR(255)
            )
        """
        )

        # Define the scraped data
        characters_data = set_characters_to_tuple_data()

        # Insert stands with stats data into the table
        for data_point in characters_data:
            try:
                # Check if the character_name already exists in the table
                cursor.execute(
                    """
                    SELECT id
                    FROM Characters
                    WHERE character_name = %s
                    """,
                    (
                        data_point[0],
                    ),  # Assuming character_name is the first element in data_point
                )
                existing_id = cursor.fetchone()

                if not existing_id:
                    print("Inserting data:", data_point)
                    # Insert data into the table if character_name doesn't exist
                    cursor.execute(
                        """
                        INSERT INTO Characters (character_name, link, stand_1, stand_2, stand_3, stand_4)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        data_point,
                    )
                else:
                    print(f"Skipping duplicate data: {data_point[0]}")
            except IntegrityError as e:
                # Handle other integrity errors if necessary
                print(f"IntegrityError: {e}")
                conn.rollback()  # Rollback the transaction

        # Commit changes and close the connection
        conn.commit()
        conn.close()
        print("Data stored successfully in the database.")
    except Exception as e:
        print(f"Error storing data in the database: {e}")


set_stands_db()
set_characters_db()
