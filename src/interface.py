import cv2
import numpy as np
from tkinter import *
from tkinter import ttk


color_names_hex = {
    "Red": "#eb3b5a",
    "Green": "#20bf6b",
    "Blue": "#2d98da",
    "Yellow": "#fed330",
    "Black": "#000",
    "Pink": "#FDA7DF",
    "Purple": "#8854d0",
    "Orange": "#fd9644",
    "White": "#fff",
    "Aqua": "#2bcbba",
}

thickness_line = {
    "Medium": 5,
    "Thin": 2,
    "Thick": 10
}   

def onFigureChange(event):
    selected_value = type_var.get()
    print("Tipo de dibujo:", selected_value)

def onColorChange(event):
    selected_value = color_var.get()
    print("Color seleccionado:", selected_value)

def onSizeChange(event):
    selected_value = size_var.get()
    print("Tamaño seleccionado:", selected_value)


def cleanAll():
    global canvas
    canvas.delete("all")
    print("Limpio")


def start_paint(event):
    global last_x, last_y, drawing_shape, coordinates
    coordinates = []
    last_x, last_y = event.x, event.y
    coordinates.append((last_x, last_y)) 
    drawing_shape = True

def paint(event):
    global last_x, last_y, drawing_shape
    if drawing_shape:
        x, y = event.x, event.y
        canvas.delete("temp_shape")
        if type_var.get() == "Line":
            canvas.create_line((last_x, last_y, x, y), fill=color_names_hex[color_var.get()], width=thickness_line[size_var.get()], tags="temp_shape")
        elif type_var.get() == "Circle":
            canvas.create_oval((last_x, last_y, x, y), outline=color_names_hex[color_var.get()], width=thickness_line[size_var.get()], tags="temp_shape")
        elif type_var.get() == "Rectangle":
            canvas.create_rectangle((last_x, last_y, x, y), outline=color_names_hex[color_var.get()], width=thickness_line[size_var.get()], tags="temp_shape")
        elif type_var.get() == "Freehand":
            x, y = event.x, event.y
            coordinates.append((x, y))
            canvas.delete("temp_shape")
            for i in range(len(coordinates) - 1):
                canvas.create_line((coordinates[i][0], coordinates[i][1], coordinates[i + 1][0], coordinates[i + 1][1]), fill=color_names_hex[color_var.get()], width=thickness_line[size_var.get()], tags="temp_shape")
        elif type_var.get() == "Borrador":
            x, y = event.x, event.y
            coordinates.append((x, y))
            canvas.delete("temp_shape")
            for i in range(len(coordinates) - 1):
                canvas.create_line((coordinates[i][0], coordinates[i][1], coordinates[i + 1][0], coordinates[i + 1][1]), fill="White", width=40, tags="temp_shape")


def end_paint(event):
    global drawing_shape
    drawing_shape = False
    canvas.itemconfig("temp_shape", tags="")

root = Tk()
root.title("Paint with python 213375") 

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
for i in range(4):
    root.rowconfigure(i, weight=1)
    for j in range(3):
        mainframe.columnconfigure(j, weight=1) 

ttk.Label(mainframe, text="Figura:").grid(column=1, row=1, sticky=W)
type_var = StringVar(value="Freehand")
combobox = ttk.Combobox(mainframe, values=["Freehand","Line", "Circle", "Rectangle", "Borrador"], textvariable=type_var, state='readonly')
combobox.grid(column=2, row=1, sticky=W)
combobox.bind("<<ComboboxSelected>>", onFigureChange)

ttk.Label(mainframe, text="Grosor de línea:").grid(column=1, row=2, sticky=W)
size_values = list(thickness_line.keys())
size_var = StringVar(value=size_values[0])
combobox = ttk.Combobox(mainframe, values=size_values, textvariable=size_var, state='readonly')
combobox.grid(column=2, row=2, sticky=W)
combobox.bind("<<ComboboxSelected>>", onSizeChange)

ttk.Label(mainframe, text="Color:").grid(column=1, row=3, sticky=W)
color_values = list(color_names_hex.keys())
color_var = StringVar(value=color_values[0])
combobox = ttk.Combobox(mainframe, values=color_values, textvariable=color_var, state='readonly')
combobox.grid(column=2, row=3, sticky=W)
combobox.bind("<<ComboboxSelected>>", onColorChange)

ttk.Button(mainframe, text="Limpiar todo", command=cleanAll).grid(column=1, row=4, sticky=W)

canvas = Canvas(mainframe, bg="white", width=500, height=500)
canvas.grid(column=4, row=1, rowspan=3, columnspan=3)
canvas.bind("<Button-1>", start_paint)
canvas.bind("<B1-Motion>", paint)
canvas.bind("<ButtonRelease-1>", end_paint)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=15, pady=5)

window_width = 920
window_height = 580


root.geometry(f"{window_width}x{window_height}")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_coordinate = int((screen_width - window_width) / 2)
y_coordinate = int((screen_height - window_height) / 2)

root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

root.mainloop()
