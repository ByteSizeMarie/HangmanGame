# Abschlussprojekt - Hangman © 2024 by Marie Sterzer is licensed under CC BY-NC-SA 4.0 

# Standard-Import
import tkinter as tk                              # GUI 
import random                                     # wichtig für Zufallswörter
import sys                                        # wichtig für Restart

# Lokal
from words import word_list

# Path
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage

OUTPUT_PATH = Path(__file__).resolve().parent     # Path(__file__) = Pfad zur aktuellen Datei, resolve() = vollständiger Pfad ohne Links, parent = Pfad zum Verzeichnis
ASSETS_PATH = OUTPUT_PATH / "assets"              # OUTPUT_PATH = Übergeordneter ordner mit Pfad zu Unterordnern
                                                  # relative Pfade wegen Lesbarkeit auf versch. Geräten

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


################ Basis - Fenster
root = Tk()
root.geometry("600x450")                          # bestimmt Größe des Fensters
root.title("Galgenmännchen")                      # ändert Name des Fensters
root.iconbitmap(relative_to_assets("sign.ico"))   # ändert Icon des Fensters

canvas = Canvas(                                  # erstellt ein Canvas-Widget (Canvas-Widget = grafisches Element zur Erstellung von benutzerdefinierten Oberflächen )
    root, bg = "#38618A",                         # bg = background-Farbe
    height = 450, 
    width = 600,
    bd = 0,                                       # bd = borderwidth
    highlightthickness = 0,                       # Dicke der Umrandung (Highlight) um das Widget fest.
    relief = "ridge"                              # ohne 3D-Effekt, ohne rahmen, auch möglich : raised, sunken, groove, ridge, solid
)

canvas.place(x = 0, y = 0)                        # Platzierung innerhalb eines übergeordneten Widgets an bestimmter Position, x = horizontal, y = vertical

canvas.create_rectangle (                         # erstellt Rechteck
    5.0,                                          # ohne externe x oder y Achse, Position im Bezug zur linken oberen Ecke 
    5.0,
    595.0,
    445.0,
    fill = "#D9D9D9",                             # Färbung
    outline = ""                                  # Rahmenlinie
)

################ Alphabet
canvas.create_text(                               # erstellt Textelement
    350.0,           
    100.0,
    anchor = "nw",                                #  Verankerung oder Ausrichtung eines gezeichneten Objekts innerhalb eines Canvas, nw = nordwest
    text = "Bereits verwendete Buchstaben:",
    fill = "#616161",
    font = ("Inter Medium", 14 * -1)              # Schriftart & -größe, * -1 = Schriftgröße in Pixel 
)

image_letters_bckg = PhotoImage(file=relative_to_assets("letters.png")) 

canvas.create_image(
    455.0,
    220.0,
    image=image_letters_bckg                      # Bild einfügen 
)

alphabet = [                                      # Liste mit Alphabet und individueller Koordinaten, Einrückung zur besseren Visualisierung
    {"x": 378.0, "y": 130.0, "text": "A"},
      {"x": 415.0, "y": 130.0, "text": "B"},
       {"x": 450.0, "y": 130.0, "text": "C"},
        {"x": 485.0, "y": 130.0, "text": "D"},
         {"x": 518.0, "y": 130.0, "text": "E"},

    {"x": 380.0, "y": 160.0, "text": "F"},
      {"x": 414.0, "y": 160.0, "text": "G"},
       {"x": 450.0, "y": 160.0, "text": "H"},
        {"x": 487.0, "y": 160.0, "text": "I"},
         {"x": 518.0, "y": 160.0, "text": "J"},

    {"x": 378.0, "y": 190.0, "text": "K"},
      {"x": 415.0, "y": 190.0, "text": "L"},
        {"x": 449.0, "y": 190.0, "text": "M"},
          {"x": 485.0, "y": 190.0, "text": "N"},
           {"x": 516.0, "y": 190.0, "text": "O"},

    {"x": 378.0, "y": 222.0, "text": "P"},
      {"x": 413.0, "y": 222.0, "text": "Q"},
        {"x": 450.0, "y": 222.0, "text": "R"},
          {"x": 485.0, "y": 222.0, "text": "S"},
           {"x": 518.0, "y": 222.0, "text": "T"},

    {"x": 378.0, "y": 255.0, "text": "U"},
      {"x": 415.0, "y": 255.0, "text": "V"},
        {"x": 448.0, "y": 255.0, "text": "W"},
          {"x": 483.0, "y": 255.0, "text": "X"},
            {"x": 518.0, "y": 255.0, "text": "Y"},

    {"x": 378.0, "y": 287.0, "text": "Z"},
      {"x": 415.0, "y": 289.0, "text": "Ä"},
        {"x": 450.0, "y": 289.0, "text": "Ö"},
          {"x": 485.0, "y": 289.0, "text": "Ü"},
]

for letter in alphabet:                            # Automatisches erstellen der Buchstaben mit zuvor definierter Liste "alphabet"
    canvas.create_text(
        letter["x"],                               # Variable letter nimmt x oder y Wert entgegen     
        letter["y"],
        anchor = "nw",    
        text = letter["text"],                     # Variable letter nimmt Text entgegen
        fill = "#ffffff",
        font = ("Inter Medium", 20 * -1)
    )

################ Galgenmännchen
hangman_images = [PhotoImage(file = relative_to_assets(f"hangman{i}.png")) for i in range(10, -1, -1)] 
# ↑erstellt Liste mit allen Hangman-Bildern, List Comprehension(Einzeiler) &  range() = umgekehrte Reihenfolge
image_index = 0                                    # Initialer Index (Startwert) für das Hangman-Bild
hangman_image = None                               # keine Wertzuweisung, da später im Code aktualisiert wird

hangman_image = canvas.create_image(               # Zuweisung Funktion canvas.create zu Variable hangman_image
    170,
    218,
    image = hangman_images[image_index]            # Variable image bekommt Element von Liste, das an Stelle von image_index steht
)

################ User Eingabefeld
canvas.create_text(
    350.0,            
    340.0,
    anchor = "nw",    
    text = "Fang an zu raten!",
    fill = "#616161",
    font = ("Inter Medium", 14 * -1)
)

user_input = Entry(                                 # erstellt Eingabefeld
    bd = 1,
    bg = "#FFFFFF",
    fg = "#2d475a",
    highlightthickness=0,
    font = ("Inter Medium", 18 * -1)
)

user_input.place(
    x = 350.0,
    y = 360.0,
    width = 150.0,
    height = 25.0
)


################ Enter / Enter-Button
def evaluate_input(event = None):                   # event = None??
    user_input_text = str(user_input.get())         # Inhalt des user_inputs wird als text abgerufen und in Variable gespeichert
    check_and_update(user_input_text)               # user_input_text als Parameter übergeben zur Überprüfung von Aktualisierung
    user_input.delete(0, "end")                     # leeren von Eingabefeld für nächste Eingabe


user_input.bind('<Return>', evaluate_input)         #.bind = Funktion oder Ereignis mit einem bestimmten Widget verknüpfen, hier Enter-Taste = Aufruf evaluate_input
root.bind('<Return>', evaluate_input)

button_guess = Button(                              # erstellt Button zur Eingabe
    borderwidth = 0,
    highlightthickness = 0,

    text = "GUESS",
    fg = "#616161",
    font = ("Inter Medium", 10 * -1),
    command = evaluate_input
)
button_guess.pack()

button_guess.place(
    x = 505.0,
    y = 360.0,
    width = 40.0,
    height = 25.0
)

################ Buchstaben einfügen und durchstreichen, Bild aktualisieren, Gewinn & Lose-Nachricht
word_to_guess = random.choice(word_list)             # würfelt random Wort aus word_list
updated_word_to_guess = "_ " * len(word_to_guess)    # Wort durch Unterstriche ersetzen
crossed_letters = []                                 # leere Liste um alle duchgestrichen Buchstaben zu speichern
guessed_positions = []                               # leere Liste um Position von geratenen Buchstaben zu verfolgen
guessed_letter = set()                               # leere Set um geratene Buchstaben zu speichern                                                                                   


def check_and_update(user_input):                    # definiert Funktion die Parameter user_input erwartet
    global updated_word_to_guess, guessed_letter, image_index, hangman_image, output_won, output_lost # außerhalb definierte Variablen die innerhalb geändert werden
    
    letter = " " # behebt fhelermeldung
    ####### Ganzes Wort richtig geraten
    if user_input == word_to_guess:                  # wenn True ...
        updated_word_to_guess = user_input           # ... dann aktualisiert in updated_word_to_guess
        guessed_letter = set(word_to_guess)          # ... Menge der guessed_letters mit den Buchstaben des zu erratenden Wort befüllen, wichtig für durchstreichen
        
    else:
        incorrect_guess = True                                                                          # True = Nutzer hat falsch geraten
        for letter in user_input:                                                                       # Für jeden Buchstaben in der Benutzereingabe
            if letter in word_to_guess and letter not in guessed_letter:                                # Buchstabe im zu erratenden Wort enthalten und noch nicht geraten
                guessed_letter.add(letter)                                                              # Buchstabe als geraten markieren
                temp_word = [letter if letter in guessed_letter else "_" for letter in word_to_guess]   # geratene Buchstaben oder Platzhalter für nicht geratene
                updated_word_to_guess = "".join(temp_word)                                              # aktualisieren des updated_word_to_guess mit temp_word
                incorrect_guess = False                                                                 # False = Nutzer hat richtig geraten

        ####### Ausgabe: Gewonnen
        if updated_word_to_guess == word_to_guess: 
            output_won = canvas.create_text(
                35,
                50,
                anchor="nw",
                text = f"Glückwunsch! Du hast das Wort \"{word_to_guess.upper()}\" richtig erraten!",   # upper() um Wort in Großbuchstaben anzuzeigen
                fill = "#38618A",
                font = ("Inter Medium", 18 * -1)
            )
    
        ####### Erneute Eingabe von gleichem falschen Buchstaben # Bild aktualisieren
        if incorrect_guess and letter not in word_to_guess:     # ... wenn incorrect_guess und der Buchstabe nicht im zu erratenden Wort enthalten  
            if image_index < 10 and hangman_image is not None:  # ... und wenn der Bildindex kleiner als 10 ist und das Hangman-Bild existiert
                canvas.delete(hangman_image)                    # ... wird das aktuelle Bild gelöscht ...
                image_index += 1                                # ... und der Index erhöht ...
                hangman_image = canvas.create_image(            # ... und Neues erstellt
                    170,
                    218,
                    image=hangman_images[image_index]
                )
        
        ####### Ausgabe: Verloren
        if image_index >= 10:   
            output_lost = canvas.create_text(
                35,
                50,
                anchor = "nw",
                text = f"Keine Versuche mehr übrig! Das Wort war \"{word_to_guess.upper()}\".",
                fill = "#38618A",
                font = ("Inter Medium", 18 * -1)
            ) 
          
    ####### Ausgabe des aktualisierten Wortes
    displayed_word = " ".join(updated_word_to_guess.upper()) # Umwandlung in Großbuchstaben und zufügen von Leerzeichen
    canvas.itemconfig(word_text, text=displayed_word)        # angezeigter Unterstrich wird durch den Inhalt von displayed_word ersetzt
    
    ####### Durchstreichen der Buchstaben
    for input_letter in user_input.upper():
        if len(input_letter) == 1:                           # ... wenn Eingabe einzelner Buchstabe ...
            for letter in alphabet:                          # ... und Buchstabe im Alphabet ...
                if input_letter == letter["text"]:           # ... und Buchstabe im angegebenen Wort ...
                    crossed_letter_id = canvas.create_text(  # ... dann wird er durchgestrichen und in Liste gespeichert
                        letter["x"],
                        letter["y"],
                        anchor = "nw",
                        text = "X",
                        fill = "#d00000",
                        font = ("Inter Medium", 26 * -1)
                    )
                    crossed_letters.append(crossed_letter_id)


####### Erstellen des Textelements _ _ _ _ _
word_text = canvas.create_text(
    50.0,
    365.0,
    anchor = "nw",
    text = updated_word_to_guess,
    fill = "#616161",
    font = ("Inter Medium", 18 * -1)
)



################ Funktionen zurücksetzen
def restart_game():                                          # setzt alles zurück um erneut zu spielen
    global word_to_guess, updated_word_to_guess, guessed_positions, guessed_letter, image_index, hangman_image
    ####### Zurücksetzen der Variablen
    word_to_guess = random.choice(word_list)
    updated_word_to_guess = "_ " * len(word_to_guess)
    guessed_positions = []
    guessed_letter = set()
    image_index = 0
    
    ######## Löschen des alten Hangman-Bildes
    if hangman_image is not None:
        canvas.delete(hangman_image)
    
    ######## Neues Hangman-Bild erstellen
    hangman_image = canvas.create_image(
        170, 
        218,
        image = hangman_images[image_index]
    )
    
    ######## Zurücksetzen des angezeigten Wortes
    displayed_word = " ".join(updated_word_to_guess.upper())
    canvas.itemconfig(word_text, text=displayed_word)

    ######## Alphabet zurücksetzen
    for crossed_letter_id in crossed_letters:
        canvas.delete(crossed_letter_id)

    ######## Ausgabe Gewonnen zurücksetzen
    def remove_output_won():
        global output_won
        if "output_won" in globals():
            canvas.delete(output_won)

    if restart_game:
        remove_output_won()
        
    ######## Ausgabe Verloren zurücksetzen
    def remove_output_lost():
        global output_lost
        if "output_lost" in globals():
            canvas.delete(output_lost)

    if restart_game:
        remove_output_lost()


################ Restart Button
button_image_restart = PhotoImage (
    file = relative_to_assets("button-restart.png")
)  

button_restart = Button (
    image = button_image_restart,
    borderwidth = 0,
    highlightthickness = 0,
    relief = "flat",    
    command = restart_game                                  # oben definierte Funktion aufrufen
)
button_restart.pack()

button_restart.place (
    x = 525.0,
    y = 5.0,
    width = 44.0,
    height = 44.0
)

################ Exit-Button
def root_exit():
    root.destroy()


button_image_exit = PhotoImage (
    file = relative_to_assets("button-exit.png")  
)

button_exit = Button(
    image = button_image_exit,
    borderwidth = 0,
    highlightthickness = 0,
    relief = "flat",    
    command = root_exit
)

button_exit.pack()

button_exit.place(
    x = 565.0,
    y = 5.0,
    width = 27.0,
    height = 44.0
)

################ Öffnet Fenster
root.resizable(False, False)                                # Fenstergröße kann nicht angepasst werden
root.mainloop()