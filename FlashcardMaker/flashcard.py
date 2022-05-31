class Card:
    """simple flashcard class"""

    def __init__(self, term, definition):
        self.term = term
        self.definition = definition

    def __repr__(self):
        return f"Card Term: {self.term}, Card Definition: {self.definition}"

    def get_term(self):
        return self.term

    def get_definition(self):
        return self.definition

    def set_term(self, updated_term):
        self.term = updated_term

    def set_definition(self, updated_definition):
        self.definition = updated_definition


def create_card_manual():
    """Prompts User for Card Term and Definition Input"""
    user_term = input("")
    user_def = input("")
    if user_term is not None and user_def is not None:
        NewCard = Card(user_term, user_def)
    else:
        print("Card Not Added.")
