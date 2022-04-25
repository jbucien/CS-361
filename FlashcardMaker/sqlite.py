import sqlite3
from flashcard import Card
from random import randint
from textwrap import wrap

# Reference: https://www.sqlitetutorial.net/sqlite-python/insert/
# https://www.semicolonworld.com/question/42826/switch-between-two-frames-in-tkinter
# '_flashcard.db'


def create_card_manual(user_term, user_def):
    """Takes a user's term and definition entries and validates them. Creates Card instance if valid."""

    new_card = None
    if user_term is False or user_def is False:
        new_card = None
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


def view_all_cards():
    # Open database and create cursor
    conn = sqlite3.connect("_flashcard.db")
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
    conn = sqlite3.connect("_flashcard.db")
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
    conn = sqlite3.connect("_flashcard.db")
    c = conn.cursor()

    flashcard_deck = {}
    i = 0
    for row in c.execute("SELECT card_term, card_def FROM cards"):
        flashcard_deck[i] = row
        i += 1

    # Close database
    conn.close()

    return flashcard_deck


# Wrap text for definitions (Referenced: https://stackoverflow.com/questions/51131812/wrap-text-inside-row-in-tkinter-treeview)
def wrapping(string, length=10):
    return '\n'.join(wrap(string, length))


def generate_card(flashcard_deck):
    key = randint(0, len(flashcard_deck)-1)
    term = flashcard_deck[key][0]
    definition = flashcard_deck[key][1]
    return (key, term, definition)


def update_term(old_term, new_term):
    # Open database and create cursor
    conn = sqlite3.connect("_flashcard.db")
    c = conn.cursor()

    # Select correct card from database
    c.execute("SELECT card_id FROM cards WHERE card_term = ?", (old_term,))
    old_card_id = c.fetchone()
    old_card_id = old_card_id[0]

    # Execute Edit
    c.execute("UPDATE cards SET card_term = ? WHERE card_id = ?",
              (new_term, old_card_id))
    conn.commit()
    conn.close()
    print('Card updated.')


def update_def(old_def, new_def):
    # Open database and create cursor
    conn = sqlite3.connect("_flashcard.db")
    c = conn.cursor()

    # Select correct card from database
    c.execute("SELECT card_id FROM cards WHERE card_def = ?", (old_def,))
    old_card_id = c.fetchone()
    old_card_id = old_card_id[0]

    # Execute Edit
    c.execute("UPDATE cards SET card_def = ? WHERE card_id = ?",
              (new_def, old_card_id))
    conn.commit()
    conn.close()
    print('Card definition updated.')


def delete_card(acard_term):
    # Open database and create cursor
    conn = sqlite3.connect("_flashcard.db")
    c = conn.cursor()

    # Select correct card from database
    c.execute("SELECT card_id FROM cards WHERE card_term = ?", (acard_term,))
    old_card_id = c.fetchone()
    old_card_id = old_card_id[0]

    # Execute Delete
    c.execute("DELETE FROM cards WHERE card_id = ?",
              (old_card_id,))
    conn.commit()
    conn.close()
    print('Card deleted.')


def delete_all_cards():
    # Open database and create cursor
    conn = sqlite3.connect("_flashcard.db")
    c = conn.cursor()

    # Droppimg table if already exists
    c.execute("DROP TABLE IF EXISTS cards")
    print("Your flashcards have been deleted.")

    # Close connection
    conn.close()


if __name__ == "__main__":
    print(grab_cards())
