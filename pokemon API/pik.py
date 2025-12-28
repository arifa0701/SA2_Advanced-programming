import tkinter
from tkinter import *
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
import io

# COLORS 
c0 = "#000000" #black
c1 = "#feffff" #white
c2 = "#f6d743" #YELLOW CARD
c3 = "#403d3d"  #ash

# Type-based colors
type_colors = {
    "fire": "#F08030",
    "water": "#6890F0",
    "electric": "#F8D030",
    "grass": "#78C850",
    "ice": "#98D8D8",
   "ghost": "#764F88",
   "psychic": "#F85888",
   "dragon": "#F85E38"

}

#  API BASE URL 
BASE_URL = "https://pokeapi.co/api/v2/"

#  WINDOW
window = Tk()
window.title("PokeDex Explorer")
window.geometry("750x510")
window.resizable(False, False)
window.configure(bg=c1)

ttk.Separator(window, orient=HORIZONTAL).grid(row=0, columnspan=2, ipadx=375)

# LEFT CARD
main_frame = Frame(window, width=500, height=480, bg=c2)
main_frame.grid(row=1, column=0, padx=5, pady=5)

# Pokemon name
pok_name = Label(main_frame,text="Pokemon Name",anchor="w",font=("Ivy", 22, "bold"),bg=c2,fg=c0)
pok_name.place(x=15, y=15)

# Pokemon type
pok_type = Label(main_frame,text="Type",font=("Ivy", 12),bg=c2,fg=c0)
pok_type.place(x=15, y=55)

# Pokemon image
image_label = Label(main_frame, bg=c2)
image_label.place(x=150, y=90)

# Status section
status_label = Label(main_frame,text="Status",justify=LEFT,font=("Ivy", 10),bg=c2,fg=c0)
status_label.place(x=15, y=300)

# Skills section
skills_label = Label(main_frame,text="Skills",justify=LEFT,font=("Ivy", 10),bg=c2,fg=c0)
skills_label.place(x=280, y=300)

# RIGHT PANEL
right_frame = Frame(window, width=230, height=480, bg=c1)
right_frame.grid(row=1, column=1, padx=5, pady=5)
search_entry = Entry(right_frame, width=18)
search_entry.pack(pady=5)
search_entry.bind("<Return>", lambda event: search_pokemon())

Button(right_frame,text="Search",width=15,command=lambda: search_pokemon()).pack(pady=5)
Label(right_frame,text="Pokémon List",font=("Ivy", 12, "bold"),bg=c1,fg=c0).pack(pady=5)

# Filter by type
type_var = StringVar()
type_var.set("electric")

type_menu = OptionMenu(right_frame,type_var,
   "fire", "water", "electric", "grass",
    "ice", "dragon", "ghost", "psychic"
)
type_menu.pack(pady=5)

Button(right_frame,text="Filter",width=15,command=lambda: filter_by_type()).pack(pady=5)

# Pokemon list container
list_frame = Frame(right_frame, bg=c1)
list_frame.pack(pady=10)

#API FUNCTIONS
def fetch_pokemon(name):
    try:
        url = BASE_URL + f"pokemon/{name.lower()}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None

def fetch_by_type(poke_type):
    try:
        url = BASE_URL + f"type/{poke_type.lower()}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None
    
#SEARCH
def search_pokemon():
    name = search_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Please enter a Pokémon name")
        return

    load_pokemon(name)

#LOAD IMAGE
def load_image(url):
    response = requests.get(url)
    image = Image.open(io.BytesIO(response.content))
    image = image.resize((200, 200))
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo

#LOAD POKEMON
def load_pokemon(name):
    data = fetch_pokemon(name)
    if not data:
        messagebox.showerror("Error", "Pokémon not found")
        return

    pok_name.config(text=data["name"].capitalize())
    pok_type.config(
        text=", ".join(t["type"]["name"] for t in data["types"])
    )

    stats = data["stats"]
    status_label.config(
        text=
        f"Status\n\n"
        f"HP: {stats[0]['base_stat']}\n"
        f"Attack: {stats[1]['base_stat']}\n"
        f"Defense: {stats[2]['base_stat']}\n"
        f"Speed: {stats[5]['base_stat']}"
    )

    skills = [a["ability"]["name"] for a in data["abilities"]]
    skills_label.config(
        text="Skills\n\n" + "\n".join(skills)
    )

    load_image(data["sprites"]["front_default"])

def load_pokemon(name):
    data = fetch_pokemon(name)
    if not data:
        messagebox.showerror("Error", "Pokémon not found")
        return

    pok_name.config(text=data["name"].capitalize())
    
    # Get types
    types = [t["type"]["name"] for t in data["types"]]
    pok_type.config(text=", ".join(types))

    # Change card background based on first type
    color = type_colors.get(types[0], c2)  # default c2 if type not in mapping
    main_frame.config(bg=color)
    pok_name.config(bg=color)
    pok_type.config(bg=color)
    image_label.config(bg=color)
    status_label.config(bg=color)
    skills_label.config(bg=color)

    # Status
    stats = data["stats"]
    status_label.config(
        text=(
            f"Status\n\n"
            f"HP: {stats[0]['base_stat']}\n"
            f"Attack: {stats[1]['base_stat']}\n"
            f"Defense: {stats[2]['base_stat']}\n"
            f"Speed: {stats[5]['base_stat']}"
        )
    )

    # Skills
    skills = [a["ability"]["name"] for a in data["abilities"]]
    skills_label.config(text="Skills\n\n" + "\n".join(skills))

    # Image
    load_image(data["sprites"]["front_default"])


# FILTER BY TYPE
def filter_by_type():
    data = fetch_by_type(type_var.get())
    if not data:
        return

    for widget in list_frame.winfo_children():
        widget.destroy()

    for p in data["pokemon"][:10]:
     Button(list_frame,text=p["pokemon"]["name"].capitalize(),width=20, command=lambda n=p["pokemon"]["name"]: 
            load_pokemon(n)).pack(pady=2)

#DEFAULT LOAD 
load_pokemon("pikachu")
filter_by_type()

window.mainloop()




