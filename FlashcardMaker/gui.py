from tkinter import *

root = Tk()
root.geometry("500x500")
root.title("Flashcard Maker")


# https://www.semicolonworld.com/question/42826/switch-between-two-frames-in-tkinter


greeting = Label(root, text="Welcome!", font=('Arial', 40, 'bold'))
greeting.pack()

# Function for the Button


def openCreateCardsScreen():
    hideButtons()
    hideAllFrames()
    createCardsFrame.pack(fill="both", expand=1)


def openStudyCardsScreen():
    hideButtons()
    hideAllFrames()
    studyCardsFrame.pack(fill="both", expand=1)


def openViewAllCardsScreen():
    hideButtons()
    hideAllFrames()
    viewAllCardsFrame.pack(fill="both", expand=1)


# Hide All Frames
def hideAllFrames():
    createCardsFrame.pack_forget()
    studyCardsFrame.pack_forget()
    viewAllCardsFrame.pack_forget()

# Hide Buttons


def hideButtons():
    createCard.pack_forget()
    studyCards.pack_forget()
    viewAllCards.pack_forget()
    deleteAllCards.pack_forget()


# Create Flashcard Button Widget
createCard = Button(root, text="Create Flashcards",
                    padx=50, command=openCreateCardsScreen)
createCard.pack()

# Study Flashcard Button Widget
studyCards = Button(root, text="Study Flashcards",
                    padx=50, command=openStudyCardsScreen)
studyCards.pack()

# View Flashcard Button Widget
viewAllCards = Button(root, text="View All Flashcards",
                      padx=50, command=openViewAllCardsScreen)
viewAllCards.pack()

# Delete Deck Button Widget
# Study Flashcard Button Widget
deleteAllCards = Button(root, text="Delete Entire Flashcard Deck",
                        padx=50)
deleteAllCards.pack()


# Create Frames
createCardsFrame = Frame(root, width=500, height=500, bg="red")
studyCardsFrame = Frame(root, width=500, height=500, bg="blue")
viewAllCardsFrame = Frame(root, width=500, height=500, bg="green")

# Runs Application
root.mainloop()
