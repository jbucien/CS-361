import tkinter as tk
from tkinter import END, messagebox
import sqlite3
from sqlite import *

# Reference for using classes to switch frames in Tkinter: https://www.semicolonworld.com/question/42826/switch-between-two-frames-in-tkinter


class FlashcardApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Flashcard Maker")
        self.geometry("500x500")
        self._frame = None
        self.switch_frame(HomePage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class HomePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        welcome_label = tk.Label(self, text="Welcome!")
        create_cards_button = tk.Button(self, text="Create Flashcards",
                                        command=lambda: master.switch_frame(CreateCardsPage))

        # Make sure user has created cards Before they study/view deck
        def check_deck(page):
            deck = check_deck_exists()
            if deck is True:
                master.switch_frame(page)
            else:
                messagebox.showinfo(
                    title="Blank Deck", message="You have not added any flashcards to your deck.")

        study_cards_button = tk.Button(self, text="Study Flashcards",
                                       command=lambda: check_deck(StudyCardsPage))
        view_cards_button = tk.Button(
            self, text="View Flashcards", command=lambda: check_deck(ViewCardsPage))

        # View
        welcome_label.pack(side="top", fill="x", pady=10)
        create_cards_button.pack()
        study_cards_button.pack()
        view_cards_button.pack()


class CreateCardsPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        create_cards_label = tk.Label(self, text="Create Cards")

        term_label = tk.Label(self, text="Enter the Flashcard Term:")
        term_entry = tk.Entry(self)

        def_label = tk.Label(self, text="Enter the Flashcard Entry:")
        def_text = tk.Text(self)

        def create_card_gui():
            term = term_entry.get()
            definition = def_text.get("1.0", END)
            card = create_card_manual(term, definition)
            if card is not None:
                added = add_card(card)
                if added is True:
                    messagebox.showinfo(message="Card added!")
                    another = messagebox.askquestion(
                        message="Do you want to add another card?")
                    if another is True:
                        term_entry.delete(0, END)
                        def_text.delete("1.0", END)
                    else:
                        master.switch_frame(HomePage)
                else:
                    messagebox.showerror(
                        message="Card could not be added. Term is already in the flashcard deck.")
                    term_entry.delete(0, END)
                    def_text.delete("1.0", END)
            else:
                messagebox.showerror(
                    message="Card could not be added. Term and Definition fields cannot be blank.")

        submit_button = tk.Button(
            self, text="Add Card", command=create_card_gui)
        return_button = tk.Button(self, text="Home Page",
                                  command=lambda: master.switch_frame(HomePage))
        create_cards_label.pack(side="top", fill="x", pady=10)
        term_label.pack()
        term_entry.pack()
        def_label.pack()
        def_text.pack()
        submit_button.pack()
        return_button.pack()


class StudyCardsPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        study_cards_label = tk.Label(self, text="Study Cards")
        return_button = tk.Button(self, text="Home Page",
                                  command=lambda: master.switch_frame(HomePage))

        card_display = tk.Frame(self, bg="black", width=400, height=350)

        study_cards_label.pack(side="top", fill="x", pady=10)
        card_display.pack(pady=20, padx=20)
        return_button.pack()


class ViewCardsPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        view_cards_label = tk.Label(self, text="View Cards")
        return_button = tk.Button(self, text="Home Page",
                                  command=lambda: master.switch_frame(HomePage))
        view_cards_label.pack(side="top", fill="x", pady=10)
        return_button.pack()


if __name__ == "__main__":
    my_app = FlashcardApp()
    my_app.mainloop()
