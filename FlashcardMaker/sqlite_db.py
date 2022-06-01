import sqlite3
import csv
import os
from flashcard import Card
from random import randint

# ------- Citations for sqlite_db.py -------------
# Description: CRUD with SQLite and Python
# Source URL: https://www.sqlitetutorial.net/sqlite-python/insert/


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
    c.execute(
        """CREATE TABLE IF NOT EXISTS cards (
            card_id INTEGER PRIMARY KEY,
            card_term TEXT NOT NULL,
            card_def TEXT NOT NULL)
            """
    )

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
            (new_card.get_term(), new_card.get_definition()),
        )
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
        """SELECT count(name) FROM sqlite_master WHERE type='table' AND name='cards'"""
    )

    if c.fetchone()[0] == 1:
        exist = True
        conn.close()
    return exist


def grab_cards():
    """
    Converts current flashcard deck into a dictionary of key, value pairs.
    Each key is a flashcard term whose value is the its corresponding definition.
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


def generate_card(flashcard_deck):
    key = randint(0, len(flashcard_deck) - 1)
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
    c.execute(
        "UPDATE cards SET card_term = ? WHERE card_id = ?", (
            new_term, old_card_id)
    )
    conn.commit()
    conn.close()
    print("Card updated.")


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
    print("Card definition updated.")


def delete_card(acard_term):
    # Open database and create cursor
    conn = sqlite3.connect("_flashcard.db")
    c = conn.cursor()

    # Select correct card from database
    c.execute("SELECT card_id FROM cards WHERE card_term = ?", (acard_term,))
    old_card_id = c.fetchone()
    old_card_id = old_card_id[0]

    # Execute Delete
    c.execute("DELETE FROM cards WHERE card_id = ?", (old_card_id,))
    conn.commit()
    conn.close()
    print("Card deleted.")


def delete_all_cards():
    # Open database and create cursor
    conn = sqlite3.connect("_flashcard.db")
    c = conn.cursor()

    # Droppimg table if already exists
    c.execute("DROP TABLE IF EXISTS cards")
    print("Your flashcards have been deleted.")

    # Close connection
    conn.close()


def import_cards(file_name="sample.csv"):
    """Imports a CSV file into the _flashcard.db database"""
    cards_dict = grab_cards()
    with open(file_name, encoding="UTF-8-sig", mode="r") as cards_csv:
        cards_reader = csv.reader(
            cards_csv, skipinitialspace=True, delimiter=",")
        try:
            check_columns = len(next(cards_reader))
        except StopIteration as e:
            return "invalid"
        if check_columns != 2:
            return "invalid"
        cards_csv.seek(0)
        cards_tuple = cards_dict.values()
        for card in cards_reader:
            for term in cards_tuple:
                if card[0] == term[0]:
                    return term[0]
        cards_csv.seek(0)
        for card in cards_reader:
            new_card = create_card_manual(card[0], card[1])
            added = add_card(new_card)
    return "successful"


def export_cards(file_name="cards.csv"):
    """Exports existing flashcards as a CSV file"""
    with open(file_name, encoding="UTF-8-sig", mode="w") as cards_csv:
        cards_dict = grab_cards()
        cards_writer = csv.writer(
            cards_csv, delimiter=",", skipinitialspace=True, quotechar="'"
        )
        for card in cards_dict.values():
            cards_writer.writerow([card[0], card[1]])
