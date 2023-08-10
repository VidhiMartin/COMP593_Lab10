"""
Description:
  Graphical user interface that displays the official artwork for a
  user-specified Pokemon, which can be set as the desktop background image.

Usage:
  python poke_image_viewer.py
"""
from tkinter import *
from tkinter import ttk
import os
import ctypes
from PIL import Image, ImageTk
from poke_api import get_pokemon_info, get_pokemon_names, download_pokemon_artwork
from image_lib import set_desktop_background_image

# Get the script and images directory
script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, 'images')

# Create the images directory if it does not exist
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

# For the icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('COMP593.PokeImageViewer')

# Create the main window
root = Tk()
root.title("Pokemon Viewer")
root.geometry('600x500')
icon_image_path = os.path.join(script_dir, 'poke_ball.ico')
icon_image = Image.open(icon_image_path)
icon_image = icon_image.convert("RGBA")
icon_photo = ImageTk.PhotoImage(icon_image)
root.iconphoto(True, icon_photo)

# Create frames
content_frame = Frame(root)
content_frame.place(anchor=CENTER)

image_label = Label(root, image=icon_photo)
image_label.place(anchor=CENTER)
image_label.grid(row=0, column=3, padx=10, pady=10, columnspan=1, sticky = NSEW)

top_frame = Frame(root)
top_frame.place(anchor=CENTER)
top_frame.grid(row=1, column=3, padx=10, pady=10, columnspan=1, sticky = NSEW)

bottom_frame = Frame(root)
bottom_frame.place(anchor=CENTER)
bottom_frame.grid(row=2, column=3, padx=10, pady=10, columnspan=1, sticky = NSEW)

# Fetch the list of Pokémon names from the URL
pokemon_names = get_pokemon_names()

selected_pokemon = StringVar()
pokemon_combobox = ttk.Combobox(top_frame, textvariable=selected_pokemon, values= pokemon_names)
pokemon_combobox.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky='ew')
pokemon_combobox.set('Select a Pokemon')

def combobox_selected(event):
    selected_pokemon_name = selected_pokemon.get()
    if selected_pokemon_name != "Select a Pokemon":
        pokemon_info = get_pokemon_info(selected_pokemon_name)
        if pokemon_info:
            artwork_filename = os.path.join(images_dir, f"{selected_pokemon_name}_artwork.png")
            download_pokemon_artwork(selected_pokemon_name, artwork_filename)

            image_data = Image.open(artwork_filename)
            image_data.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(image_data)

            image_label.config(image=photo)
            image_label.image = photo

            set_as_desktop_button.config(state=ACTIVE)

pokemon_combobox.bind("<<ComboboxSelected>>", combobox_selected)

def set_as_desktop_image():
    selected_pokemon_name = selected_pokemon.get()
    if selected_pokemon_name:
        artwork_filename = os.path.join(images_dir, f"{selected_pokemon_name}_artwork.png")
        if set_desktop_background_image(artwork_filename):
            print("Desktop background set successfully.")
        else:
            print("Failed to set desktop background.")

set_as_desktop_button = Button(bottom_frame, text="Set as Desktop Image", state=ACTIVE, command=set_as_desktop_image)
set_as_desktop_button.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky = NSEW)

root.mainloop()