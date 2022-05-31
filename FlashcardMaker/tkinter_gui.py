import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import ImageTk, Image
import sqlite_db
from time import sleep
import os.path


# ------- Citations for tkinter_gui.py -------------
# Description: Using classes to switch frames in Tkinter
# Source URL: https://www.semicolonworld.com/question/42826/switch-between-two-frames-in-tkinter

# Description: Deleting child widgets from a Tkinter frame
# Source URL: https://youtu.be/A6m7TmjuNzw

# Description: Creating and working with Tkinter Treeview objects
# Source URL: https://www.pythontutorial.net/tkinter/tkinter-treeview/

# Description: Opening File Dialog Boxes with Tkinter
# Source URL: https://www.youtube.com/watch?v=Aim_7fC-inw&t=358s

# Description: Place Images in Tkinter Frame
# Source URL: https://www.tutorialspoint.com/how-to-place-an-image-into-a-frame-in-tkinter


class FlashcardApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Flashcard Maker")
        self.geometry("800x550")
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

        # Initialize Welcome title
        self.welcome_label = tk.Label(
            self, text="Welcome!", font=("Arial", 25), pady=10)

        # Initialize main 5 buttons
        self.create_cards_button = tk.Button(
            self, text="Create Flashcards", command=lambda: master.switch_frame(CreateCardsPage))
        self.study_cards_button = tk.Button(
            self, text="Study Flashcards", command=lambda: self.check_deck(master, StudyCardsPage))
        self.view_cards_button = tk.Button(
            self, text="View Flashcards", command=lambda: self.check_deck(master, ViewCardsPage))
        self.import_cards_button = tk.Button(
            self, text="Import Flashcards", command=lambda: master.switch_frame(ImportCardsPage))
        self.export_cards_button = tk.Button(
            self, text="Export Flashcards", command=lambda: self.check_deck(master, ExportCardsPage))

        # Initialize Layout of Grid
        self.welcome_label.grid(column=0, row=0)
        self.create_cards_button.grid(column=0, row=1, padx=10, pady=5)
        self.study_cards_button.grid(column=0, row=2, padx=10, pady=5)
        self.view_cards_button.grid(column=0, row=3, padx=10, pady=5)
        self.import_cards_button.grid(column=0, row=4, padx=10, pady=5)
        self.export_cards_button.grid(column=0, row=5, padx=10, pady=5)

    def check_deck(self, master, page):
        """
        Checks that the user already has flashcards in their deck when they click to the StudyCardsPage or ViewCardsPage. If their deck is empty, tells user to first go to CreateCardsPage. Else, redirects to the page specified in the page parameter.
        """
        deck = sqlite_db.check_deck_exists()
        if deck is True:
            master.switch_frame(page)
        else:
            messagebox.showinfo(
                title="Blank Deck", message="You have not added any flashcards to your deck.")


class CreateCardsPage(tk.Frame):
    def __init__(self, master):
        # Initialize frame
        tk.Frame.__init__(self, master)

        # Initialize Create Cards Title Label
        self.create_cards_label = tk.Label(
            self, text="Create Cards", font=("Arial", 25), pady=10)

        # Initialize Flashcard Term/Def Labels & Text Fields
        self.term_label = tk.Label(self, text="Enter the Flashcard Term:")
        self.term_entry = tk.Entry(self, width=40)

        self.def_label = tk.Label(self, text="Enter the Flashcard Definition:")
        self.def_text = tk.Text(self, height=20, width=60, bd=5,
                                borderwidth=1, relief="raised", font=("Arial", 12))

        # Initialize Auto-Generate Definition Button/Label
        self.generate_def_button = tk.Button(
            self, text="Auto-Generate Definition", command=self.generate_def, padx=1, pady=1)
        self.generate_def_label = tk.Label(
            self, text="")
        # When user hovers over generate_def_button, displays text telling user what button does.
        self.generate_def_button.bind("<Enter>", self.show_generate_def_label)
        self.generate_def_button.bind("<Leave>", self.hide_generate_def_label)

        # Initialize Submit and Return to Home buttons
        self.submit_button = tk.Button(
            self, text="Add Card", command=self.create_card_gui)
        self.return_button = tk.Button(self, text="Home Page",
                                       command=lambda: master.switch_frame(HomePage))

        # Initialize Grid Layout
        self.create_cards_label.grid(
            column=0, row=0, padx=10, pady=5, columnspan=2)
        self.term_label.grid(column=0, row=1, pady=5, columnspan=2, sticky="W")
        self.term_entry.grid(column=0, row=2, pady=5, columnspan=1, sticky="W")
        self.generate_def_button.grid(column=1, row=2, pady=5, padx=3)
        self.def_label.grid(column=0, row=3, pady=5, columnspan=2, sticky="W")
        self.def_text.grid(column=0, row=4, pady=5, columnspan=2, sticky="W")
        self.submit_button.grid(column=1, row=6, padx=5, pady=5,
                                columnspan=1, sticky="w")
        self.return_button.grid(column=0, row=7, padx=5, pady=5,
                                columnspan=1)

    def generate_def(self):
        """
        Writes user's input term to watchMe.txt. Kyle's microservice reads the text file, saves the term, and scrapes the Oxford Learner Dictionary for that term's first definition. His service then writes the definition to the text file. generate_def() reads the definition and outputs the definition to the Flashcard Definition field.
        Note: Kyle's microservice must be running in a separate process.
        """
        term = self.term_entry.get()
        if not term:
            messagebox.showerror(
                title="Blank Term",
                message=f"Term field cannot be blank.")
            return
        else:
            with open("../../361microservice/watchMe.txt", "w") as file:
                file.write(term)
            sleep(2)
            if os.path.exists(f"../../361microservice/{term}.txt"):
                with open(f"../../361microservice/{term}.txt", "r") as file1:
                    definition = file1.read()

                self.def_text.insert('1.0', definition)
            else:
                messagebox.showerror(
                    title="Could Not Generate Definition",
                    message=f"Cannot find definition for term: {term}")

    def show_generate_def_label(self, event):
        """
        Displays text telling user what the Generate Definition button does whenever the user hovers over the button.
        """
        self.generate_def_label.config(
            text="Import a term's definition from the internet. \n (Single-word terms only.)", fg="#00008B", font=("Arial", 10))
        self.generate_def_label.grid(
            row=1, column=1, sticky="e")

    def hide_generate_def_label(self, event):
        """
        Hides the text telling the user what the Generate Definition button does once the user is no longer hovering over the button.
        """
        self.generate_def_label.config(text="")

    def create_card_gui(self):
        """
        Reads user's input flashcard term and definition. Makes sure both fields are filled, else displays an error message. Also makes sure term is not a duplicate, else displays an error message. Adds valid term/definition to SQlite database. Displays text at bottom of window confirming card added successfully.
        """
        term = self.term_entry.get()
        definition = self.def_text.get("1.0", "end - 1 chars")
        if not term:
            messagebox.showerror(
                title="Blank Card",
                message="Card could not be added. Term field cannot be blank.")
        if not definition:
            messagebox.showerror(
                title="Blank Card",
                message="Card could not be added. Definition field cannot be blank.")
        else:
            card = sqlite_db.create_card_manual(term, definition)
            added = sqlite_db.add_card(card)
            if added:
                added_confirmation = tk.Label(
                    self, text="Card Added", fg="#32CD32")
                added_confirmation.grid(
                    column=0, row=6, pady=5)
                self.term_entry.delete(0, "end")
                self.def_text.delete(1.0, "end")
                added_confirmation.after(
                    4000, lambda: added_confirmation.destroy())
            else:
                messagebox.showerror(
                    message="Card could not be added. Term is already in the flashcard deck.")
                self.term_entry.delete(0, "end")
                self.def_text.delete(1.0, "end")


class StudyCardsPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Initialize Study Cards Title Label/Button
        self.study_cards_label = tk.Label(
            self, text="Study Cards", font=("Arial", 25))

        # Connect to database and get flashcards as dictionary. Initialize empty set of already seen cards.
        self.cards_dict = sqlite_db.grab_cards()
        self.cards_seen = set()

        # Initialize Variables for Displaying Terms/Definitions:
        self.def_var = tk.StringVar(self)
        self.term_var = tk.StringVar(self)

        # Intialize Start Studying and Home Buttons
        self.start_study_button = tk.Button(
            self, text="Start Studying!", command=lambda: self.show_card_display(master))
        # Bind Start Study Button to the user's click so the button disappears
        self.start_study_button.bind(
            "<ButtonRelease-1>", self.forget_study_button)
        self.return_button = tk.Button(self, text="Home Page",
                                       command=lambda: master.switch_frame(HomePage))

        # Initialize Inner Card Display Frame (not shown until user clicks "Start Studying!")
        self.card_display = tk.LabelFrame(
            self, text="Card Deck", padx=50, pady=50, height=300, width=400)

        # Initialize Outer Grid Layout
        self.start_study_button.grid(column=0, row=1, pady=10)
        self.return_button.grid(column=0, row=3, pady=10)
        self.study_cards_label.grid(column=0, row=0, pady=5)

    def clear_inner_frame(self):
        """
        Loops through all child frames in the Inner Card Display Frame and deletes them, so only one term/definition appears at time.
        """
        for child in self.card_display.winfo_children():
            child.destroy()

    def show_card_display(self, master):
        """
        Initializes grid layout for elements in the Inner Card Display Frame and call study(), which prompts the reveal of the first card.
        """
        self.card_display.grid(column=0, row=2, padx=5, pady=5)
        self.card_display.grid_propagate(False)
        self.card_display.grid_rowconfigure(0, weight=2)
        self.card_display.grid_rowconfigure(1, weight=1)
        self.card_display.grid_columnconfigure(0, weight=1)
        self.card_display.grid_columnconfigure(1, weight=1)
        self.study(master)

    def study(self, master):
        """
        Checks if user has already looped through the entire flashcard deck. If so, calls repeat_deck(). Else, displays a random flashcard from the deck, along with Show Definition and Next Card buttons that the user clicks on to iterate through the deck.
        """
        self.clear_inner_frame()
        if len(self.cards_seen) == len(self.cards_dict):
            self.repeat_deck(master)
        else:
            # get flashcard entry in form of (key, term, definition)
            term_tuple = sqlite_db.generate_card(self.cards_dict)
            # if flashcard has already been seen, generate a new one
            while term_tuple[0] in self.cards_seen:
                term_tuple = sqlite_db.generate_card(self.cards_dict)

            # Once a new flashcard is found:
            self.cards_seen.add(term_tuple[0])
            self.term_var.set(f"{term_tuple[1]}")

            # Display Term
            show_term = tk.Label(self.card_display, textvariable=self.term_var)
            show_term.grid(column=0, row=0, columnspan=2)

            # Initialize and Display Show Definition Button
            self.show_def_button(master, term_tuple)
            # Show Next Button
            self.show_next_button(master)

    def show_def_button(self, master, term_tuple):
        """
        Initializes and Displays Show Definition Button.
        """
        show_def_button = tk.Button(
            self.card_display, text="Show Definition", command=lambda: self.show_definition(master, term_tuple))
        show_def_button.grid(
            column=0, row=1, sticky="se", padx=10, pady=10)

    def show_next_button(self, master):
        """
        Initializes and Displays Next Button.
        """
        show_next_button = tk.Button(self.card_display, text="Next Card",
                                     command=lambda: self.study(master))
        show_next_button.grid(
            column=1, row=1, sticky="sw", padx=10, pady=10)

    def show_definition(self, master, term_tuple):
        """
        Called when user clicks the Show Definition button. Displays the definition of the randomly generated flashcard term.
        """
        self.clear_inner_frame()
        self.def_var.set(f"{term_tuple[2]}")
        definition_label = tk.Label(
            self.card_display, textvariable=self.def_var)
        definition_label.grid(column=0, row=0, columnspan=2)
        show_term_button = tk.Button(
            self.card_display, text="Show Term", command=lambda: self.show_term(master, term_tuple))
        show_term_button.grid(
            column=0, row=1, sticky="se", padx=10, pady=10)
        self.show_next_button(master)

    def show_term(self, master, term_tuple):
        """
        Called when user clicks the Show Term button. Displays the term associated with the displayed definition.
        """
        self.clear_inner_frame()
        self.term_var.set(f"{term_tuple[1]}")
        term_label = tk.Label(
            self.card_display, textvariable=self.term_var)
        term_label.grid(column=0, row=0, columnspan=2)
        self.show_def_button(master, term_tuple)
        self.show_next_button(master)

    def repeat_deck(self, master):
        """
        Called if user has completed looping through their entire deck. Asks user if they want to repeat the deck. If so, clears cards_seen cache and restarts deck. Else, returns user to Home Page.
        """
        repeat = messagebox.askyesno(
            title="Completed Deck", message="You have completed studying all your cards! Would you like to play again?")
        if repeat:
            self.cards_seen.clear()
            self.clear_inner_frame()
            self.study(master)
        else:
            master.switch_frame(HomePage)

    def forget_study_button(self, event):
        """
        Erases Start Study Button after it has been clicked once.
        """
        self.start_study_button.forget()


class ViewCardsPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Initialize Title Label
        self.view_cards_label = tk.Label(
            self, text="View Cards", font=("Arial", 25))

        # Connect to database and get flashcards as dictionary
        self.cards_dict = sqlite_db.grab_cards()

        # Create card_display inner frame for Treeview Table
        self.card_display = tk.Frame(self)
        # Create crud_frame inner frame for CRUD operations fields
        self.crud_frame = tk.LabelFrame(self, text="Currently Selected")

        # Create labels/fields for CRUD operations within the crud_frame
        self.selected_term_label = tk.Label(
            self.crud_frame, text="Selected Term")
        self.selected_term_entry = tk.Entry(self.crud_frame, width=40)
        self.selected_def_label = tk.Label(
            self.crud_frame, text="Selected Definition")
        self.selected_def_text = tk.Text(
            self.crud_frame, height=5, width=60, borderwidth=1, relief="raised", font=("Arial", 12))

        # Create Edit and Delete Card Buttons in crud_frame
        self.edit_card_button = tk.Button(
            self.crud_frame, text="Save Changes to Selected Card", command=self.edit_selected)
        self.delete_card_button = tk.Button(
            self.crud_frame, text="Delete Selected Card", command=self.delete_selected)

        # Create Delete All and Home Buttons in outer frame
        self.delete_all_button = tk.Button(
            self, text="Delete ALL Cards", command=self.delete_all)
        self.return_button = tk.Button(self, text="Home Page",
                                       command=lambda: master.switch_frame(HomePage))

        # Render outer frame and treeview
        self.view_cards_label.grid(column=0, row=0, pady=10)
        self.card_display.grid(column=0, row=1, pady=10)
        self.tree = self.initialize_treeview()
        self.fill_treeview()
        self.crud_frame.grid(column=0, row=2, pady=5)
        self.return_button.grid(column=0, row=4, pady=5)
        self.delete_all_button.grid(column=0, row=5, pady=5)

        # Render inner crud_frame grid display
        self.crud_frame.grid_columnconfigure(0, weight=1)
        self.crud_frame.grid_columnconfigure(1, weight=3)
        self.crud_frame.grid_rowconfigure(0, weight=1)
        self.crud_frame.grid_rowconfigure(1, weight=2)
        self.crud_frame.grid_rowconfigure(2, weight=1)
        self.selected_term_label.grid(
            row=0, column=0, padx=10, pady=10, sticky="w")
        self.selected_term_entry.grid(
            row=0, column=1, padx=10, pady=10, sticky="w")
        self.selected_def_label.grid(
            row=1, column=0, padx=10, pady=10, sticky="w")
        self.selected_def_text.grid(
            row=1, column=1, padx=5, pady=5, sticky="w")
        self.edit_card_button.grid(row=2, column=1, padx=5, pady=5)
        self.delete_card_button.grid(row=2, column=0, padx=5, pady=5)

    def initialize_treeview(self):
        """
        Creates a Treeview object "tree", which displays numbered cards terms and definitions within the card_display inner frame.
        """
        tree = ttk.Treeview(self.card_display, columns=(
            '#', 'Term', 'Definition'), show='headings', height=8, selectmode="browse")
        return tree

    def fill_treeview(self):
        """
        Fills tree object with headings/columns and flashcard data
        """
        # Create Headings and Columns
        self.tree.heading('#0', text='')
        self.tree.heading('#', text='#', anchor='e')
        self.tree.heading('Term', text='Term')
        self.tree.heading('Definition', text="Definition")
        self.tree.column('#0', width=0, minwidth=35)
        self.tree.column('#', width=35, minwidth=35, anchor="e")
        self.tree.column('Term', width=300, minwidth=35)
        self.tree.column('Definition', width=300, minwidth=35)
        self.tree.pack(side="left", fill="both", expand=1)

        # Adding table data from cards_dict
        for i in range(len(self.cards_dict)):
            self.tree.insert(parent="", index="end", iid=i,
                             text="Terms", values=(i+1, self.cards_dict[i][0], self.cards_dict[i][1]))
        self.treeview_scrollbar()
        # Bind user's left click to the selected flashcard
        self.tree.bind("<ButtonRelease-1>", self.fill_selected)

    def treeview_scrollbar(self):
        """
        Creates vertical scrollbar if number of flashcards exceeds table height.
        """
        scrollbar = tk.Scrollbar(self.card_display)
        scrollbar.pack(side="right", fill="y")
        self.tree.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

    def fill_selected(self, event):
        """
        When user clicks on flashcard within the Treeview display, selects that flashcard and populates the Selected Term Entry and Selected Def Text fields with that flashcard's information.
        """
        self.selected_term_entry.delete(0, "end")
        self.selected_def_text.delete(1.0, "end")
        selected_row = self.tree.item(self.tree.focus(), 'values')
        self.selected_term_entry.insert(0, selected_row[1])
        self.selected_def_text.insert("1.0", selected_row[2])

    def edit_selected(self):
        """
        Called when user clicks the Edit Selected Card button. Checks if updated term is a duplicate of another term. If so, shows error. Also checks if updated term or definition fields are blank. If so, shows error. Otherwise, the user's updated term/definition input is valid. Updates flashcard entry in dataase and gives confirmation.
        """
        selected_obj = self.tree.selection()[0]
        selected_row = self.tree.item(self.tree.focus(), 'values')
        selected_term = selected_row[1]
        selected_def = selected_row[2]
        new_term = self.selected_term_entry.get()
        new_def = self.selected_def_text.get("1.0", "end-1c")

        repeat = 0
        for i in range(len(self.cards_dict)):
            if new_term == self.cards_dict[i][0]:
                repeat += 1
        if repeat > 1:
            repeated_term = messagebox.showerror(
                title="Duplicate Term", message="Term already in deck. Cannot update.")
        elif not new_term:
            blank_field = messagebox.showerror(
                title="Blank Field", message="Flashcard terms cannot be blank.")
        elif len(new_def) == 1:
            blank_field = messagebox.showerror(
                title="Blank Field", message="Flashcard entries cannot be blank.")
        else:
            sqlite_db.update_term(selected_term, new_term)
            sqlite_db.update_def(selected_def, new_def)
            updated_selected_confirmation = messagebox.showinfo(
                title="Confirmation", message="Selected card updated.")
            self.tree.item(selected_obj, text="", values=(
                selected_row[0], new_term, new_def))

    def delete_selected(self):
        """
        Called when user clicks the Delete Selected Card button. Warns user that delete_selected() cannot be reversed. If user continues, permanently deletes the selected card and gives confirmation. Else, dismisses warning and returns user to main View Flashcards page.
        """
        selected_obj = self.tree.selection()[0]
        selected_row = self.tree.item(self.tree.focus(), 'values')
        selected_term = selected_row[1]
        delete_selected_warning = messagebox.askyesno(
            title="Warning", message="Deleting a flashcard cannot be undone. Do you still want to proceed?")
        if delete_selected_warning:
            sqlite_db.delete_card(selected_term)
            self.tree.delete(selected_obj)
            self.selected_term_entry.delete(0, "end")
            self.selected_def_text.delete("1.0", "end")
            deleted_confirmation = tk.Label(
                self, text="Card Deleted", fg="#32CD32")
            deleted_confirmation.grid(
                column=0, row=3, pady=3)
            deleted_confirmation.after(
                4000, lambda: deleted_confirmation.destroy())

    def delete_all(self):
        """
        Called when user clicks the Delete All button. Gives user a warning that delete_all() cannot be reversed. If user continues, permanently deletes user's entire flashcard deck and gives confirmation. Else, dismisses warning and returns user to main View Flashcards page.
        """
        delete_all_warning = messagebox.askyesno(
            title="Warning", message="You are about to delete ALL of your flashcards. This cannot be undone. Do you still want to proceed?")
        if delete_all_warning:
            self.selected_term_entry.delete(0, "end")
            self.selected_def_text.delete("1.0", "end")
            for line in self.tree.get_children():
                self.tree.delete(line)
            sqlite_db.delete_all_cards()
            deleted = messagebox.showinfo(
                title="Confirmation", message="Your flashcards have been deleted.")


class ImportCardsPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Initialize Import Cards Title Label
        self.import_cards_label = tk.Label(
            self, text="Import Cards from a CSV File", font=("Arial", 25), pady=10)

        # Initialize Instructions
        self.import_cards_instructions = tk.Label(
            self, text="Click on \"Import Now\" to open a file browser. Select a valid .csv file and click \"Open\" to import.", pady=10)
        self.valid_csv = tk.Label(
            self, text="Valid .csv files consist of two comma-separated columns. \n The first column is the flashcard term. \n The second column is the flashcard definition. \n Do not add title headers, i.e. \"Term\", \"Definition\"."
        )

        # Initialize Photo Samples
        self.image_frame1 = tk.LabelFrame(
            self, text="Example 1: Format of text .csv file", font=("Arial", 15), width=400, height=200)
        self.sample_plaintext = ImageTk.PhotoImage(
            Image.open("plaintextcsv.png"))
        self.image1 = tk.Label(self.image_frame1, image=self.sample_plaintext)
        self.image_frame2 = tk.LabelFrame(
            self, text="Example 2: Format of spreadsheet .csv file", font=("Arial", 15), width=400, height=200)
        self.sample_spreadsheet = ImageTk.PhotoImage(
            Image.open("spreadsheetcsv.png"))
        self.image2 = tk.Label(
            self.image_frame2, image=self.sample_spreadsheet)

        # Initialize Buttons
        self.import_now_button = tk.Button(
            self, text="Import Cards Now", command=self.import_file_dialog)
        self.return_button = tk.Button(
            self, text="Home Page", command=lambda: master.switch_frame(HomePage))

        # Render Layout of Grid
        self.import_cards_label.grid(column=0, row=1, padx=10, pady=5)
        self.import_cards_instructions.grid(column=0, row=2, padx=10, pady=5)
        self.valid_csv.grid(column=0, row=3, padx=10, pady=5)
        self.image_frame1.grid(column=0, row=4, padx=10, pady=5)
        self.image_frame2.grid(column=0, row=5, padx=10, pady=5)
        self.import_now_button.grid(column=0, row=6, padx=10, pady=5)
        self.return_button.grid(column=0, row=7, padx=10, pady=5)
        self.image1.pack()
        self.image2.pack()

    def import_file_dialog(self):
        self.filename = filedialog.askopenfilename(
            initialdir="/CS-361/FlashcardMaker", title="Select a CSV File", filetypes=((".csv files", "*.csv"),))
        imported = sqlite_db.import_cards(self.filename)
        if imported == "successful":
            added = messagebox.askyesno(
                title="Confirmation", message="Your flashcards have been added. Go to ViewCards Page?")
            if added:
                self.master.switch_frame(ViewCardsPage)

        elif imported == "invalid":
            added = messagebox.showerror(
                title="Import Error", message="Your flashcards could not be imported. Invalid .csv format.")
        else:
            added = messagebox.showerror(
                title="Import Error", message=f"Your flashcards could not be imported. {imported} is a duplicate term.")


class ExportCardsPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Initialize Export Cards Title Label
        self.export_cards_label = tk.Label(
            self, text="Export Cards to a CSV File", font=("Arial", 25), pady=10)

        # Initialize Instructions
        self.export_cards_instructions = tk.Label(
            self, text="Click on \"Export Now\" to open the file browser. \n Navigate to desired file destination. \n Enter your desired filename and click \"Save\" to export.", pady=10)

        # Initialize Buttons
        self.export_now_button = tk.Button(
            self, text="Export Cards Now", command=self.export_file_dialog)
        self.return_button = tk.Button(self, text="Home Page",
                                       command=lambda: master.switch_frame(HomePage))

        # Render Layout of Grid
        self.export_cards_label.grid(column=0, row=1, padx=10, pady=5)
        self.export_cards_instructions.grid(column=0, row=2, padx=10, pady=5)
        self.export_now_button.grid(column=0, row=3, padx=10, pady=5)
        self.return_button.grid(column=0, row=4, padx=10, pady=5)

    def export_file_dialog(self):
        self.filename = filedialog.asksaveasfilename(
            initialdir="/CS-361/FlashcardMaker", title="Save as a CSV File", filetypes=((".csv files", "*.csv"),))
        sqlite_db.export_cards(self.filename)
        print(self.filename)
        added = messagebox.showinfo(
            title="Confirmation", message=f"Your flashcards have been exported as {self.filename}. ")


if __name__ == "__main__":
    my_app = FlashcardApp()
    my_app.mainloop()
