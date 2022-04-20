import sqlite3
from flashcard import Card
from random import choice

# Reference: https://www.sqlitetutorial.net/sqlite-python/insert/
# https://www.semicolonworld.com/question/42826/switch-between-two-frames-in-tkinter
# '_flashcard.db'


def create_card_manual(user_term, user_def):
    """Takes a user's term and definition entries and validates them. Creates Card instance if valid."""

    new_card = None
    if user_term == '' or user_def == '':
        return new_card
    else:
        new_card = Card(user_term, user_def)
        return new_card


def add_card(new_card):
    """Adds a new user-generated flashcard to the _flashcard.db database"""
    added = True

    # Open database and create cursor
    conn = sqlite3.connect("_flashcard.db")
    c = conn.cursor()

    # Create cards table if it doesn't already exist
    c.execute("""CREATE TABLE IF NOT EXISTS cards (
            card_id INTEGER PRIMARY KEY,
            card_term TEXT NOT NULL,
            card_def TEXT NOT NULL)
            """)

    # Check to make sure term isn't repeated
    c.execute("SELECT card_term FROM cards WHERE card_term = ?",
              (new_card.get_term(),))
    result = c.fetchall()
    if len(result) != 0:
        added = False
    else:
        # Insert Row into flashcard table
        c.execute(
            "INSERT INTO cards (card_term, card_def) VALUES (?, ?)",
            (new_card.get_term(), new_card.get_definition()))
        conn.commit()
        added = True
    # Commits the current transaction
    conn.close()
    return added


def view_all_cards(db_name):
    # Open database and create cursor
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    for row in c.execute("SELECT card_term, card_def FROM cards"):
        print(row)

    # Close database
    conn.close()


def check_deck_exists():
    """
    Checks to make sure the cards table exists.
    """
    exist = False

    # Open database and create cursor
    conn = sqlite3.connect('_flashcard.db')
    c = conn.cursor()

    # Check if table 'cards' exists
    c.execute(
        """SELECT count(name) FROM sqlite_master WHERE type='table' AND name='cards'""")

    if c.fetchone()[0] == 1:
        exist = True
        conn.close()
    return exist


def grab_cards():
    """
    Converts current flashcard deck into a dictionary.
    """
    # Open database and create cursor
    conn = sqlite3.connect('_flashcard.db')
    c = conn.cursor()

    flashcard_deck = {}
    i = 0
    for row in c.execute("SELECT card_term, card_def FROM cards"):
        flashcard_deck[i] = row
        i += 1

    # Close database
    conn.close()

    return flashcard_deck


def study_deck():
    flashcard_deck = grab_cards('_flashcard.db')
    total_cards = len(flashcard_deck)
    nums = [num for num in range(0, total_cards)]
    print(nums)
    while nums != []:
        index = choice(nums)

        # Display Card Term
        print(flashcard_deck[index][0])

        # Display Card Definition
        print(flashcard_deck[index][1])

        # Remove Index
        nums.remove(index)

        # Update Status
        print(f"{total_cards - len(nums)} / {total_cards} Cards Completed")

    print("Congratulations!")


def delete_all_cards(db_name):
    # Open database and create cursor
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Doping EMPLOYEE table if already exists
    c.execute("DROP TABLE cards")
    print("Your flashcards have been deleted.")

    # Close connection
    conn.close()


if __name__ == "__main__":
    # newcard = create_card_manual()
    # add_card(newcard, '_flashcard.db')
    # newcard1 = create_card_manual()
    # add_card(newcard1, '_flashcard.db')
    # newcard1 = create_card_manual()
    # add_card(newcard1, '_flashcard.db')
    # study_cards('_flashcard.db')
    # view_all_cards('_flashcard.db')
    delete_all_cards('_flashcard.db')
