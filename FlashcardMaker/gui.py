from tkinter import *

root = Tk()
root.geometry("500x500")
root.title("Flashcard Maker")


greeting = Label(root, text="Welcome!", font=('Arial', 40, 'bold'))
greeting.grid(row=0, column=0, columnspan=2)

# Function for the Button


def myClick():
    hello = f"Hello, {e.get()}"
    greeting = Label(root, text=hello)
    greeting.pack()


# # Entry (Input Widget)
# e = Entry(root, width=50)
# e.pack()
# # At the 0th box, "Term" is the default text
# e.insert(0, "Term")

# Create Flashcard Button Widget
createCard = Button(root, text="Create Flashcards",
                    padx=50, command=myClick)
createCard.grid(row=1, column=0)

# Study Flashcard Button Widget
studyCards = Button(root, text="Study Flashcards",
                    padx=50, command=myClick)
studyCards.grid(row=2, column=0)

# View Flashcard Button Widget
viewAllCards = Button(root, text="View All Flashcards",
                      padx=50, command=myClick)
viewAllCards.grid(row=3, column=0)

# Delete Deck Button Widget
# Study Flashcard Button Widget
deleteAllCards = Button(root, text="Delete Entire Flashcard Deck",
                        padx=50, command=myClick)
deleteAllCards.grid(row=4, column=1)


# Runs Application
root.mainloop()
