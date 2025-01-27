#_______________________________________________________________All Imports
import tkinter as tk
import random
import sys

from tkinter import Tk, ttk, Canvas, Entry, Button, PhotoImage
from PIL import Image, ImageDraw, ImageTk, ImageFont
from pathlib import Path

# import databank
from _databank import word_list

#_______________________________________________________________Path (Images/Fonts)
def resource_path(relative_path: str) -> Path:
    try:
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS  
        else:
            base_path = Path(__file__).resolve().parent
        return Path(base_path) / relative_path
    except Exception as e:
        print(f"Failed to determine resource path: {e}")
        return None

ASSETS_PATH = resource_path("assets")  

#_______________________________________________________________Fonts
font_path = resource_path("assets/fonts/MiriamLibre-Regular.ttf")  
font_regular = ImageFont.truetype(font_path, 30)

font_path = resource_path("assets/fonts/MiriamLibre-Bold.ttf")  
font_bold = ImageFont.truetype(font_path, 30)

#_______________________________________________________________Base Window
root = Tk()
root.geometry("1100x750")  
root.title("Whiskerman")  
root.iconbitmap(resource_path("assets/images/icon.ico"))  

#_______________________________________________________________Base - Rounded Rectangles
canvas = tk.Canvas(
    root, 
    bg="#092648", 
    height=750, 
    width=1100, 
    bd=0,
    highlightthickness=0, 
    relief="ridge"
)

canvas.place(x=0, y=0)

def create_rounded_rectangle_image(width, height, radius, fill_color):
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        [(0, 0), (width, height)], 
        radius=radius, 
        fill=fill_color
    )
    return ImageTk.PhotoImage(image)

# Spacing, sizes & colors
grid_spacing = 15 
rect_sizes = [(709, 555), (341, 113), (341, 428), (573, 151), (477, 151)]
colors = ["#191919", "#191919", "#191919", "#191919", "#191919"]

# Calculating positioning for rectangles
total_width_first_row = rect_sizes[0][0] + rect_sizes[1][0] + grid_spacing
total_width_second_row = rect_sizes[3][0] + rect_sizes[4][0] + grid_spacing
first_row_start_x = (1100 - total_width_first_row) // 2
second_row_start_x = (1100 - total_width_second_row) // 2
first_row_start_y = 15
second_row_start_y = rect_sizes[0][1] + grid_spacing + 15

rect_positions = [
    (first_row_start_x, first_row_start_y),
    (first_row_start_x + rect_sizes[0][0] + grid_spacing, first_row_start_y),
    (first_row_start_x + rect_sizes[0][0] + grid_spacing, first_row_start_y + rect_sizes[1][1] + grid_spacing),
    (second_row_start_x, second_row_start_y),
    (second_row_start_x + rect_sizes[3][0] + grid_spacing, second_row_start_y)
]

rectangle_references = []

# Actually creating rectangles
for i, (pos, size, color) in enumerate(zip(rect_positions, rect_sizes, colors)):
    rect = create_rounded_rectangle_image(size[0], size[1], 5, color)
    rectangle_references.append(rect)
    canvas.create_image(pos[0], pos[1], image=rect, anchor="nw")

#_______________________________________________________________Images for Hangman
hangman_images = []
for i in range(11):  # Assuming 11 stages of the hangman images
    image_path = resource_path(f"assets/images/Whiskerman{i}.png")
    hangman_images.append(PhotoImage(file=image_path))

# Set initial image state
image_index = 0
hangman_image = canvas.create_image(
    370,
    292,
    image=hangman_images[image_index]
)

#_______________________________________________________________Guessing Word
word_to_guess = random.choice(word_list).upper()  
updated_word_to_guess = "_ " * len(word_to_guess)    
guessed_letter = set() 
win = []
lose = []                              

#_______________________________________________________________Update Word & Image
# GANZES WORT ÜBERPRÜFEN EINFÜGEN!!
def check_and_update(user_input):
    global updated_word_to_guess, guessed_letter, image_index, hangman_image, win, lose
    
    incorrect_guess = True
    for i, letter in enumerate(word_to_guess):
        if letter == user_input and letter not in guessed_letter:
            guessed_letter.add(letter)
            updated_word_to_guess = "".join(
                [char if char in guessed_letter else "_" for char in word_to_guess]
            )
            incorrect_guess = False

    # Update word display
    displayed_word = " ".join(updated_word_to_guess.upper())
    canvas.itemconfig(word_text_word_to_guess, text=displayed_word)

    if incorrect_guess:  # Wrong guess
        if image_index < 10:  # Maximum index is 10
            image_index += 1
            canvas.itemconfig(hangman_image, image=hangman_images[image_index])

    if updated_word_to_guess == word_to_guess:
        win = canvas.create_text(
            910,
            200,
            width=350,
            anchor="center",
            text=f"You guessed right! The word was \"{word_to_guess.upper()}\"!",
            fill="#A2BBA3",
            font=(font_regular, 20)
        )

    if image_index == 10:
        lose = canvas.create_text(
            910,
            200,
            width=350,
            anchor="center",
            text=f"You lost! The right word was \"{word_to_guess.upper()}\".",
            fill="#CB3654",
            font=(font_regular, 20)
        )


#_______________________________________________________________Letters
def on_letter_click(letter, button):
    check_and_update(letter)
    disable_button_with_fade(button)  

# Alphabet for Buttons
alphabet = [                                      
    {"x": 767.0, "y": 295.0, "text": "A"},
    {"x": 817.0, "y": 295.0, "text": "B"},
    {"x": 867.0, "y": 295.0, "text": "C"},
    {"x": 917.0, "y": 295.0, "text": "D"},
    {"x": 967.0, "y": 295.0, "text": "E"},
    {"x": 1017.0, "y": 295.0, "text": "F"},
    {"x": 767.0, "y": 345.0, "text": "G"},
    {"x": 817.0, "y": 345.0, "text": "H"},
    {"x": 867.0, "y": 345.0, "text": "I"},
    {"x": 917.0, "y": 345.0, "text": "J"},
    {"x": 967.0, "y": 345.0, "text": "K"},
    {"x": 1017.0, "y": 345.0, "text": "L"},
    {"x": 767.0, "y": 395.0, "text": "M"},
    {"x": 817.0, "y": 395.0, "text": "N"},
    {"x": 867.0, "y": 395.0, "text": "O"},
    {"x": 917.0, "y": 395.0, "text": "P"},
    {"x": 967.0, "y": 395.0, "text": "Q"},
    {"x": 1017.0, "y": 395.0, "text": "R"},
    {"x": 767.0, "y": 445.0, "text": "S"},
    {"x": 817.0, "y": 445.0, "text": "T"},
    {"x": 867.0, "y": 445.0, "text": "U"},
    {"x": 917.0, "y": 445.0, "text": "V"},
    {"x": 967.0, "y": 445.0, "text": "W"},
    {"x": 1017.0, "y": 445.0, "text": "X"},
    {"x": 767.0, "y": 495.0, "text": "Y"},
    {"x": 817.0, "y": 495.0, "text": "Z"},
]

# Fade effect function for the button
def fade_button(button, start_color, end_color, steps=20, delay=5):
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(rgb_color):
        return f"#{''.join(f'{v:02x}' for v in rgb_color)}"

    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)
    step = [(end_rgb[i] - start_rgb[i]) / steps for i in range(3)]

    def update_color(step_index=0):
        if step_index <= steps:
            current_rgb = [int(start_rgb[i] + step[i] * step_index) for i in range(3)]
            current_color = rgb_to_hex(current_rgb)
            button.config(bg=current_color)
            button.after(delay, update_color, step_index + 1)
        else:
            button.config(state="disabled", fg="#B0B0B0", bg=end_color)  # Disable the button

    update_color()

# Function to disable the button with fade effect
def disable_button_with_fade(button):
    fade_button(button, start_color="#31498C", end_color="#303030")

button_list = []

# Creating buttons for each letter
for letter in alphabet:     
    button_guess = Button(
        root,
        borderwidth=0,
        highlightthickness=0,
        text=letter["text"],
        fg="#000000",
        font=(font_bold, 30 * -1),
    )
    
    button_guess.config(command=lambda letter=letter, button=button_guess: on_letter_click(letter["text"], button))
    
    button_guess.place(
        x=letter["x"],
        y=letter["y"],
        width=40.0,
        height=43.0
    )

    button_list.append(button_guess)



#_______________________________________________________________Input Field & Enter-Button
#_______________________________________Input Field
user_input = Entry(
    root,
    font=(font_regular, 26 * -1),
    bg="#FFFFFF",
    fg="#000000"
)
user_input.place(
    x=635, 
    y=615, 
    width=420, 
    height=50
)

#_______________________________________Enter-Button
def evaluate_input(event=None):
    user_input_text = user_input.get().upper()
    user_input.delete(0, tk.END)

    if len(user_input_text) == 1 and user_input_text.isalpha():
        check_and_update(user_input_text)

user_input.bind('<Return>', evaluate_input)        


button_guess = Button(
    root,
    text="Guess",
    fg="#FFFFFF",
    bg="#31498C",
    font=(font_regular, 14),
    command=evaluate_input,
    activebackground="#21315D",  
    activeforeground="#ffffff"
)

button_guess.place(
    x=635, 
    y=678, 
    width=125, 
    height=30
)



#_______________________________________________________________Create Textelement  _ _ _ _ _

rect_x = 200.0  
rect_y = 570.0  
rect_width = 210.0  
rect_height = 190.0 

rect_center_x = rect_x + rect_width / 2
rect_center_y = rect_y + rect_height / 2

word_text_word_to_guess = canvas.create_text(
    rect_center_x,
    rect_center_y,
    anchor = "center",
    text = updated_word_to_guess,
    fill = "#ffffff",
    font = (font_bold, 20)
)



#_______________________________________________________________Restart Game
def reset_buttons():
    for button in button_list:
        button.config(state="normal", bg="#ffffff", fg="#000000")


def restart_game():
    global word_to_guess, updated_word_to_guess, guessed_letter, image_index

    word_to_guess = random.choice(word_list).upper()
    updated_word_to_guess = "_ " * len(word_to_guess)
    guessed_letter.clear()
    image_index = 0

    # Reset displayed word
    canvas.itemconfig(word_text_word_to_guess, text=" ".join(updated_word_to_guess))

    # Reset hangman image
    canvas.itemconfig(hangman_image, image=hangman_images[image_index])

    # Reset text
    canvas.delete(win, lose)

    # Reset letters
    reset_buttons()

#_________________________________________________Restart-Button
image_restart = Image.open(resource_path("assets/images/restart.png"))  
photo_restart = ImageTk.PhotoImage(image_restart)

button_restart = tk.Button(
    root,
    image=photo_restart, 
    bg="#191919", 
    bd=0, 
    highlightthickness=0,
    activebackground="#191919",  
    activeforeground="#6C6C6C",
    command=restart_game
)

button_restart.pack(pady=20)

button_restart.place (
    x = 1000.0,
    y = 35.0,
    width = 50.0,
    height = 46.0
)

word_text_restart = canvas.create_text(
    1025,
    95,
    anchor = "center",
    text = "Restart",
    fill = "#ffffff",
    font = (font_regular, 18 * -1)
)


#_______________________________________________________________Main Loop
root.resizable(False, False)
root.mainloop()
