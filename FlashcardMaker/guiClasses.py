import tkinter as tk
from tkinter import messagebox, ttk

from sqlite import *


# Reference for using classes to switch frames in Tkinter: https://www.semicolonworld.com/question/42826/switch-between-two-frames-in-tkinter


class FlashcardApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Flashcard Maker")
        self.geometry("700x550")
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

        # Declare Title Label and Create Cards Button
        welcome_label = tk.Label(
            self, text="Welcome!", font=("Arial", 25), pady=10)
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
        welcome_label.grid(column=0, row=0)
        create_cards_button.grid(column=0, row=1, padx=10, pady=5)
        study_cards_button.grid(column=0, row=2, padx=10, pady=5)
        view_cards_button.grid(column=0, row=3, padx=10, pady=5)


class CreateCardsPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        create_cards_label = tk.Label(
            self, text="Create Cards", font=("Arial", 25), pady=10)

        term_label = tk.Label(self, text="Enter the Flashcard Term:")
        term_entry = tk.Entry(self, width=40)

        def_label = tk.Label(self, text="Enter the Flashcard Entry:")
        def_text = tk.Text(self, height=20, width=60, bd=5,
                           borderwidth=1, relief="raised", font=("Arial", 12))

        def generate_def():
            pass

        generate_def_button = tk.Button(
            self, text="Auto-Generate Definition", command=generate_def)

        def create_card_gui():
            term = term_entry.get()
            definition = def_text.get(1.0, "end")
            if not term or not definition:
                messagebox.showerror(
                    title="Blank Card",
                    message="Card could not be added. Term and Definition fields cannot be blank.")
            else:
                card = create_card_manual(term, definition)
                added = add_card(card)
                if added:
                    added_confirmation = tk.Label(
                        self, text="Card Added", fg="#32CD32")
                    added_confirmation.grid(
                        column=0, row=5, pady=5, columnspan=2)
                    term_entry.delete(0, "end")
                    def_text.delete(1.0, "end")
                    added_confirmation.after(
                        4000, lambda: added_confirmation.destroy())
                else:
                    messagebox.showerror(
                        message="Card could not be added. Term is already in the flashcard deck.")
                    term_entry.delete(0, "end")
                    def_text.delete(1.0, "end")

        submit_button = tk.Button(
            self, text="Add Card", command=create_card_gui)
        return_button = tk.Button(self, text="Home Page",
                                  command=lambda: master.switch_frame(HomePage))
        create_cards_label.grid(column=0, row=0, padx=10, pady=5, columnspan=2)
        term_label.grid(column=0, row=1, pady=5, columnspan=2, sticky="W")
        term_entry.grid(column=0, row=2, pady=5, columnspan=1, sticky="W")
        generate_def_button.grid(column=1, row=2, pady=5, padx=3)
        def_label.grid(column=0, row=3, pady=5, columnspan=2, sticky="W")
        def_text.grid(column=0, row=4, pady=5, columnspan=2, sticky="W")
        submit_button.grid(column=1, row=6, padx=5, pady=5,
                           columnspan=1, sticky="w")
        return_button.grid(column=0, row=7, padx=5, pady=5,
                           columnspan=1)


class StudyCardsPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Variables for Displaying Terms/Definitions:
        def_variable = tk.StringVar(self)
        term_variable = tk.StringVar(self)

        # Connect to database and get flashcards as dictionary
        cards_dict = grab_cards()
        card_nums = set()

        # Study Cards Title Label/Button
        study_cards_label = tk.Label(
            self, text="Study Cards", font=("Arial", 25))
        study_cards_label.grid(column=0, row=0, pady=5)

        # Initialize Card Display Frame (not shown until user clicks "Start Studying!")
        card_display = tk.LabelFrame(
            self, text="Card Deck", padx=50, pady=50, height=300, width=400)

        # Clear Inner Frame Function
        def clear_inner_frame():
            # reference https://www.youtube.com/watch?v=A6m7TmjuNzw
            # Loops through all child frames and deletes them
            for child in card_display.winfo_children():
                child.destroy()

        # Start study: reveal card term/definition
        def start_study():
            clear_inner_frame()
            if len(card_nums) == len(cards_dict):
                repeat_deck()
            else:
                term_tuple = generate_card(cards_dict)
                while term_tuple[0] in card_nums:
                    term_tuple = generate_card(cards_dict)
                card_nums.add(term_tuple[0])
                term_variable.set(f"{term_tuple[1]}")
                show_term = tk.Label(card_display, textvariable=term_variable)
                show_term.grid(column=0, row=0, columnspan=2)
                show_def_button = tk.Button(
                    card_display, text="Show Definition", command=lambda: show_definition(term_tuple))
                show_def_button.grid(
                    column=0, row=1, sticky="se", padx=10, pady=10)
                show_next_button = tk.Button(card_display, text="Next Card",
                                             command=start_study)
                show_next_button.grid(
                    column=1, row=1, sticky="sw", padx=10, pady=10)

        # Asks User if they want to repeat their deck
        def repeat_deck():
            repeat = messagebox.askyesno(
                title="Completed Deck", message="You have completed studying all your cards! Would you like to play again?")
            if repeat:
                card_nums.clear()
                clear_inner_frame()
                start_study()
            else:
                master.switch_frame(HomePage)

        # Show Definition
        def show_definition(term_tuple):
            clear_inner_frame()
            def_variable.set(f"{term_tuple[2]}")
            definition_label = tk.Label(
                card_display, textvariable=def_variable)
            definition_label.grid(column=0, row=0, columnspan=2)
            show_term_button = tk.Button(
                card_display, text="Show Term", command=lambda: show_term(term_tuple))
            show_term_button.grid(
                column=0, row=1, sticky="se", padx=10, pady=10)
            show_next_button = tk.Button(card_display, text="Next Card",
                                         command=start_study)
            show_next_button.grid(
                column=1, row=1,  sticky="sw", padx=10, pady=10)

        # Show Term
        def show_term(term_tuple):
            clear_inner_frame()
            term_variable.set(f"{term_tuple[1]}")
            term_label = tk.Label(
                card_display, textvariable=term_variable)
            term_label.grid(column=0, row=0, columnspan=2)
            show_def_button = tk.Button(
                card_display, text="Show Definition", command=lambda: show_definition(term_tuple))
            show_def_button.grid(
                column=0, row=1, sticky="se", padx=10, pady=10)
            show_next_button = tk.Button(card_display, text="Next Card",
                                         command=start_study)
            show_next_button.grid(
                column=1, row=1,  sticky="sw", padx=10, pady=10)

        # Reveal the Display Frame
        def show_card_display():
            card_display.grid(column=0, row=2, padx=5, pady=5)
            card_display.grid_propagate(False)
            card_display.grid_rowconfigure(0, weight=2)
            card_display.grid_rowconfigure(1, weight=1)
            card_display.grid_columnconfigure(0, weight=1)
            card_display.grid_columnconfigure(1, weight=1)
            start_study()

        # Start Studying Button
        start_study_button = tk.Button(
            self, text="Start Studying!", command=show_card_display)
        start_study_button.grid(column=0, row=1, pady=10)

        # Erase Study Button After It is Clicked
        def forget_study_button(event):
            start_study_button.forget()
            return
        start_study_button.bind("<ButtonRelease-1>", forget_study_button)

        # Return to Home Button
        return_button = tk.Button(self, text="Home Page",
                                  command=lambda: master.switch_frame(HomePage))
        return_button.grid(column=0, row=3, pady=10)


class ViewCardsPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Page Title
        view_cards_label = tk.Label(
            self, text="View Cards", font=("Arial", 25))
        view_cards_label.pack(side="top", fill="x", pady=10)

        # Connect to database and get flashcards as dictionary
        cards_dict = grab_cards()

        # Create Inner Frame to Display Table
        card_display = tk.Frame(self)
        card_display.pack()

        # Create a Table on Top of this Card_Display Frame
        # Referenced: https://www.pythontutorial.net/tkinter/tkinter-treeview/
        tree = ttk.Treeview(card_display, columns=(
            '#', 'Term', 'Definition'), show='headings', height=8, selectmode="browse")
        tree.heading('#0', text='')
        tree.heading('#', text='#', anchor='e')
        tree.heading('Term', text='Term')
        tree.heading('Definition', text="Definition")
        tree.column('#0', width=0, minwidth=35)
        tree.column('#', width=35, minwidth=35, anchor="e")
        tree.column('Term', width=300, minwidth=35)
        tree.column('Definition', width=300, minwidth=35)
        tree.pack(side="left", fill="both", expand=1)

        # Adding Data to Table
        for i in range(len(cards_dict)):
            tree.insert(parent="", index="end", iid=i,
                        text="Terms", values=(i+1, cards_dict[i][0], cards_dict[i][1]))

        # Creating Table Scrollbar
        scrollbar = tk.Scrollbar(card_display)
        scrollbar.pack(side="right", fill="y")
        tree.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)

        # Edit/Delete Selected Card Fields
        crud_frame = tk.LabelFrame(self, text="Currently Selected")
        crud_frame.pack(fill="both", expand="yes", padx=20, pady=20)
        crud_frame.grid_columnconfigure(0, weight=1)
        crud_frame.grid_columnconfigure(1, weight=3)
        crud_frame.grid_rowconfigure(0, weight=1)
        crud_frame.grid_rowconfigure(1, weight=2)
        crud_frame.grid_rowconfigure(2, weight=1)

        selected_term_label = tk.Label(crud_frame, text="Selected Term")
        selected_term_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        selected_term_entry = tk.Entry(crud_frame, width=40)
        selected_term_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        selected_def_label = tk.Label(crud_frame, text="Selected Definition")
        selected_def_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        selected_def_text = tk.Text(
            crud_frame, height=5, width=60, borderwidth=1, relief="raised", font=("Arial", 12))
        selected_def_text.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Binding Single Click to Selected Treeview Object
        def fill_selected(event):
            selected_term_entry.delete(0, "end")
            selected_def_text.delete(1.0, "end")
            selected_row = tree.item(tree.focus(), 'values')
            selected_term_entry.insert(0, selected_row[1])
            selected_def_text.insert("1.0", selected_row[2])
            return
        tree.bind("<ButtonRelease-1>", fill_selected)

        # Edit Card Function
        def edit_selected():
            selected_obj = tree.selection()[0]
            selected_row = tree.item(tree.focus(), 'values')
            selected_term = selected_row[1]
            selected_def = selected_row[2]
            new_term = selected_term_entry.get()

            index = 0
            repeat = False
            for i in range(len(cards_dict)):
                if new_term == cards_dict[i][0]:
                    repeat = True
                    break
            if repeat:
                repeated_term = messagebox.showwarning(
                    title="Duplicate Term", message="Term already in deck. Cannot update.")

            new_def = selected_def_text.get("1.0", "end")
            update_term(selected_term, new_term)
            update_def(selected_def, new_def)
            updated_selected_confirmation = messagebox.showinfo(
                title="Confirmation", message="Selected card updated.")
            tree.item(selected_obj, text="", values=(
                selected_row[0], new_term, new_def))

        # Edit Button
        edit_card_button = tk.Button(
            crud_frame, text="Save Changes to Selected Card", command=edit_selected)
        edit_card_button.grid(row=2, column=1, padx=5, pady=5)

        # Delete Card Function
        def delete_selected():
            selected_obj = tree.selection()[0]
            selected_row = tree.item(tree.focus(), 'values')
            selected_term = selected_row[1]
            delete_selected_warning = messagebox.askyesno(
                title="Warning", message="You are about to delete the selected flashcard. This cannot be undone. Do you still want to proceed?")
            if delete_selected_warning:
                delete_card(selected_term)
                tree.delete(selected_obj)
                delete_selected_confirmation = messagebox.showinfo(
                    title="Confirmation", message="Selected card deleted.")
                selected_term_entry.delete(0, "end")
                selected_def_text.delete("1.0", "end")
        # Delete Card Button
        delete_card_button = tk.Button(
            crud_frame, text="Delete Selected Card", command=delete_selected)
        delete_card_button.grid(row=2, column=0, padx=5, pady=5)

        # Delete All Function
        def delete_all():
            delete_all_warning = messagebox.askyesno(
                title="Warning", message="You are about to delete ALL of your flashcards. This cannot be undone. Do you still want to proceed?")
            if delete_all_warning:
                selected_term_entry.delete(0, "end")
                selected_def_text.delete("1.0", "end")
                for line in tree.get_children():
                    tree.delete(line)
                delete_all_cards()
                deleted = messagebox.showinfo(
                    title="Confirmation", message="Your flashcards have been deleted.")

        # Delete All Button
        delete_all_button = tk.Button(
            self, text="Delete ALL Cards", command=delete_all)
        delete_all_button.pack(pady=10)

        # Return to Home Button
        return_button = tk.Button(self, text="Home Page",
                                  command=lambda: master.switch_frame(HomePage))
        return_button.pack(pady=10)


if __name__ == "__main__":
    my_app = FlashcardApp()
    my_app.mainloop()
