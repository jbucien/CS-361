import sqlite3
from flashcard import Card
from random import choice

# Reference: https://www.sqlitetutorial.net/sqlite-python/insert/
# '_flashcard.db'


def create_card_manual():
    """Prompts User for Card Term and Definition Input"""
    user_term = input('Enter a flashcard term: ')
    user_def = input('Enter a definition for the term: ')
    if user_term is not None and user_def is not None:
        NewCard = Card(user_term, user_def)
        return NewCard
    else:
        print("Card Not Added.")


def add_card(new_card, db_name):
    """Adds a new user-generated flashcard to the _flashcard.db database"""

    # Open database and create cursor
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Create cards table if it doesn't already exist
    c.execute("""CREATE TABLE IF NOT EXISTS cards (
            card_id INTEGER PRIMARY KEY,
            card_term TEXT NOT NULL,
            card_def TEXT NOT NULL)
            """)

    # Insert Row into flashcard table
    c.execute(
        "INSERT INTO cards (card_term, card_def) VALUES (?, ?)",
        (new_card.get_term(), new_card.get_definition()))

    # Commits the current transaction
    conn.commit()
    print("Your flashcard has been added!")

    conn.close()


def view_all_cards(db_name):
    # Open database and create cursor
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    for row in c.execute("SELECT card_term, card_def FROM cards"):
        print(row)

    # Close database
    conn.close()


def grab_cards(db_name):
    """
    Converts current flashcard deck into a dictionary.
    """
    # Open database and create cursor
    conn = sqlite3.connect(db_name)
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
    # delete_all_cards('_flashcard.db')
    study_deck()
