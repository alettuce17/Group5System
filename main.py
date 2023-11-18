from tkinter import *

root = Tk()
root.geometry('627x459')
root.overrideredirect(1)
root.wm_attributes("-transparentcolor", "grey")  # Adjust the alpha value as needed
root.wm_attributes("-topmost", 1)

# Variables to store offset
offset_x = 0
offset_y = 0


def moveStart(event):
    global offset_x, offset_y
    offset_x = event.x_root - root.winfo_x()
    offset_y = event.y_root - root.winfo_y()

def moveApp(event):
    root.geometry(f'+{event.x_root - offset_x}+{event.y_root - offset_y}')

def exitClick():
    root.destroy()

def addItem():
    text.config(text="Item Added!")



# Photo sidebar
framePhoto = PhotoImage(file='Frame 1.png')
frameLabel = Label(root, border=0, bg='grey', image=framePhoto)
frameLabel.pack(fill=BOTH, expand=True)
# Frame photo bind
frameLabel.bind("<ButtonPress-1>", moveStart)
frameLabel.bind("<B1-Motion>", moveApp)
#Logo
titleLogo = PhotoImage(file='KATALOG.png')
titleLabel = Label(root, image=titleLogo, border=0, bg='#7D4D47')
titleLabel.place(x=52, y=17)

# Exit button photo
exitPhoto = PhotoImage(file='exit.png')
# Exit label
exitLabel = Label(root, image=exitPhoto, border=0, bg='#7D4D47')
exitLabel.place(x=564, y=2)

# Exit bind
exitLabel.bind("<Button-1>", lambda e: exitClick())

# Add Item Button
addItemPhoto = PhotoImage(file='AddItem.png')
add_button = Button(root, image=addItemPhoto, bg='#FFFFFF', command=addItem, borderwidth=0 )
add_button.place(x=19, y=78, anchor='nw')  # Set anchor to 'nw' for exact position

text = Label(root, text="")
text.pack(padx=19, pady=78)


# Display Item Button
displayItemPhoto = PhotoImage(file='DisplayItems.png')
displayLabel = Label(root, image=displayItemPhoto, border=0)
displayLabel.place(x=179,y=78)

# Update Item Button
updateItemPhoto = PhotoImage(file='UpdateItem.png')
updateLabel = Label(root, image=updateItemPhoto, border=0, bg='#FFFFFF')
updateLabel.place(x=339,y=78)

# Delete Item Button
deleteItemPhoto = PhotoImage(file='DeleteItem.png')
deleteLabel = Label(root, image=deleteItemPhoto, border=0)
deleteLabel.place(x=499,y=78)

# About GUI Button
aboutGUIPhoto = PhotoImage(file='AboutGUI.png')
aboutGUILabel = Label(root, image=aboutGUIPhoto, border=0)
aboutGUILabel.place(x=576,y=424)

# Set window position to center
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 627
window_height = 459

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')


root.mainloop()
