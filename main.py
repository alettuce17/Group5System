from tkinter import *
from tkinter import messagebox, font, ttk, simpledialog, filedialog
import random
from fpdf import FPDF
from PIL import Image, ImageTk
import tkinter as tk
import os

# Declare entry variables as global
name_entry = None
price_entry = None
description_entry = None
category_var = None
table = None
image_preview = None
image_path = None
canvas = None
canvas_frame = None
current_info_window = None


def catalog_file_exists():
    return os.path.isfile("catalog_data.txt")

def validate_float(value):
    try:
        if value:
            float(value)
        return True
    except ValueError:
        return False


def reset_frame():
    global frame_screen
    frame_screen.destroy()  # Destroy the existing frame
    frame_screen = Frame(root, width=920, height=536, borderwidth=10, relief="flat")
    frame_screen.place(x=360, y=184)


def add_item():
    global frame_screen, name_entry, price_entry, description_entry, category_var, image_preview, image_path

    reset_frame()  # Reset the frame before creating new widgets
    font.Font(size=20)

    delete_label = Label(frame_screen, text="Add Item", font=("Helvetica", 24))
    delete_label.place(x=100, y=30)
    entry_font = font.Font(size=20)  # Set the desired font size
    name_label = Label(frame_screen, text="Name:")

    name_label.place(x=100, y=80)
    name_entry = ttk.Entry(frame_screen, width=40, font=entry_font)  # Set width to 70 characters
    name_entry.place(x=100, y=110, height=58)  # Set height to 58 pixels

    price_label = Label(frame_screen, text="Price:")
    price_label.place(x=100, y=180)
    price_entry = ttk.Entry(frame_screen, width=40, font=entry_font, validate="key",
                            validatecommand=(frame_screen.register(validate_float), '%P'))
    price_entry.place(x=100, y=208, height=58)

    description_label = Label(frame_screen, text="Description:")
    description_label.place(x=100, y=276)
    description_entry = ttk.Entry(frame_screen, width=40, font=entry_font)
    description_entry.place(x=100, y=304, height=58)

    # Category dropdown using Menubutton
    category_label = Label(frame_screen, text="Category:")
    category_label.place(x=100, y=372)

    categories = [
        "None",
        "Makeup",
        "Fragrance",
        "Skincare",
        "Bath and Body",
        "Intimate Apparel",
        "Accessories",
        "Jewelry",
        "Men's Store",
        "Home & Kitchen",
        "Nutrition",
        "Other"
    ]

    category_var = StringVar()
    category_var.set(categories[0])  # Set default category

    category_menu = Menubutton(frame_screen, textvariable=category_var, indicatoron=True, borderwidth=1,
                               relief="raised", width=30)
    category_menu.place(x=100, y=400, height=30)

    category_menu.menu = Menu(category_menu, tearoff=False)
    category_menu["menu"] = category_menu.menu

    for category in categories:
        category_menu.menu.add_radiobutton(label=category, variable=category_var, value=category)

    # Image selection button
    image_button = ttk.Button(frame_screen, text="Select Image", command=select_image)
    image_button.place(x=257, y=34, height=30)

    # Frame to hold the image preview with border
    image_preview_frame = ttk.Frame(frame_screen, border=2, relief="flat")
    image_preview_frame.place(x=579, y=384, height=126, width=137)

    # Image preview label inside the frame
    image_preview = Label(image_preview_frame)
    image_preview.pack(padx=5, pady=5, fill='both', expand=True)

    # Save button
    save_button = ttk.Button(frame_screen, text="Save", command=save_item)
    save_button.place(x=100, y=440, height=30)
    # Close button
    close_button = ttk.Button(frame_screen, text="Close", command=reset_frame)
    close_button.place(x=100, y=480, height=30)


def select_image():
    global image_path, image_preview
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        image_path = file_path
        update_image_preview()
    else:
        messagebox.showwarning("Warning", "No image selected.")


def update_image_preview(image_preview_frame=None):
    global image_path, image_preview

    if image_path:
        # Open the image file and create a resized thumbnail
        img = Image.open(image_path)
        img.thumbnail((137, 137), Image.BICUBIC)
        photo = ImageTk.PhotoImage(img)

        # Update the image preview label
        if image_preview:
            image_preview.config(image=photo)
            image_preview.image = photo
        else:
            image_preview = Label(image_preview_frame, image=photo)
            image_preview.pack(padx=5, pady=5, fill='both', expand=True)
            image_preview.image = photo
    else:
        messagebox.showwarning("Warning", "No image selected.")


def save_item():
    global name_entry, price_entry, description_entry, category_var, image_path
    item_name = name_entry.get()
    try:
        item_price = float(price_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid numeric value for the price.")
        return
    item_description = description_entry.get()
    item_category = category_var.get()

    # Check if no image is selected
    if image_path is None:
        messagebox.showerror("Error", "Please select an image.")
        return

    # Check for empty fields, non-numeric price, category not selected
    if not (item_price is not None and isinstance(item_price, (int, float))) or item_category == "None":
        messagebox.showerror("Error", "Please fill in all fields correctly.")
        return

    # Check if the item name already exists in the catalog
    if is_duplicate_name(item_name):
        messagebox.showerror("Error", "Item name already exists in the catalog. Please choose a different name.")
        return



    # Replace "|" with "\" in item_name and item_description
    item_name_cleaned = item_name.replace("|", "\\")
    item_description_cleaned = item_description.replace("\n", " ").replace("|", "\\")
    item_id = generate_unique_id()
    # Use pipe "|" as a separator for the data
    data_to_write = f"{item_id}|{item_name_cleaned}|{item_price}|{item_description_cleaned}|{item_category}|{image_path}\n"

    # Append the data to the file
    with open("catalog_data.txt", "a") as file:
        file.write(data_to_write)

    messagebox.showinfo("Success", f"Item added successfully!\nItem ID: {item_id}")



def is_duplicate_name(new_name):
    try:
        with open("catalog_data.txt", "r") as file:
            existing_names = [line.split("|")[1].strip() for line in file if line.strip() and line.split("|")]
            return new_name in existing_names
    except FileNotFoundError:
        return False


def generate_unique_id():
    try:
        with open("catalog_data.txt", "r") as file:
            existing_ids = {int(line.split("|")[0]) for line in file if line.strip() and line.split("|")}
    except FileNotFoundError:
        existing_ids = set()

    # Generate a new ID until a unique one is found
    new_id = random.randint(1000, 9999)
    while new_id in existing_ids:
        new_id = random.randint(1000, 9999)

    return new_id


def delete():
    global frame_screen
    reset_frame()  # Reset the frame before creating new widgets
    if not catalog_file_exists():
        messagebox.showerror("Error", "Catalog file does not exist. Please add some item first.")
        return
        # Check if there is data in the file
    try:
        with open("catalog_data.txt", "r") as file:
            first_line = file.readline()
            if not first_line.strip():
                # File is empty, show a message and return
                messagebox.showinfo("Info", "Catalog file is empty. Please add some items.")
                return
    except FileNotFoundError:
        messagebox.showerror("Error", "Catalog data file not found.")
        return
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return
    # Create UI for deleting an item
    entry_font = font.Font(size=20)  # Set the desired font size

    delete_label = Label(frame_screen, text="Delete Item", font=("Helvetica", 24))
    delete_label.place(x=100, y=30)

    item_id_label = Label(frame_screen, text="Enter Item ID to delete:")
    item_id_label.place(x=100, y=90)

    item_id_entry = ttk.Entry(frame_screen, width=40, font=entry_font)
    item_id_entry.place(x=100, y=120, height=58)

    delete_button = ttk.Button(frame_screen, text="Delete", command=lambda: delete_item(item_id_entry.get()))
    delete_button.place(x=100, y=188, height=30)

    # Close button
    close_button = ttk.Button(frame_screen, text="Close", command=reset_frame)
    close_button.place(x=100, y=228, height=30)


def delete_item(item_id_str):
    if item_id_str is None:
        return  # Return to the main menu

    if not item_id_str.isdigit():
        messagebox.showerror("Error", "Please enter a valid number for the Item ID.")
        return

    item_id = int(item_id_str)

    try:
        with open("catalog_data.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    found = False
    updated_data = []
    for line in lines:
        if line.startswith(str(item_id)):
            found = True
        else:
            updated_data.append(line)

    if found:
        with open("catalog_data.txt", "w") as file:
            file.writelines(updated_data)

        messagebox.showinfo("Success", f"Item with Item ID {item_id} deleted successfully!")
    else:
        messagebox.showerror("Error", f"No corresponding item found for Item ID: {item_id}")


def update_item():
    global frame_screen

    reset_frame()  # Reset the frame before creating new widgets
    if not catalog_file_exists():
        messagebox.showerror("Error", "Catalog file does not exist. Please add some item first")
        return
        # Check if there is data in the file
    try:
        with open("catalog_data.txt", "r") as file:
            first_line = file.readline()
            if not first_line.strip():
                # File is empty, show a message and return
                messagebox.showinfo("Info", "Catalog file is empty. Please add some items.")
                return
    except FileNotFoundError:
        messagebox.showerror("Error", "Catalog data file not found.")
        return
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return
    entry_font = font.Font(size=20)  # Set the desired font size

    update_label = Label(frame_screen, text="Update Item", font=("Helvetica", 24))
    update_label.place(x=100, y=30)

    item_id_label = Label(frame_screen, text="Enter Item ID to update:")
    item_id_label.place(x=100, y=90)

    item_id_entry = ttk.Entry(frame_screen, width=40, font=entry_font)
    item_id_entry.place(x=100, y=120, height=58)

    update_button = ttk.Button(frame_screen, text="Update", command=lambda: update_item_ui(item_id_entry.get()))
    update_button.place(x=100, y=188, height=30)

    # Close button
    close_button = ttk.Button(frame_screen, text="Close", command=reset_frame)
    close_button.place(x=100, y=228, height=30)


def update_item_ui(item_id_str):
    global frame_screen
    if not item_id_str.isdigit():
        messagebox.showerror("Error", "Please enter a valid number for the Item ID.")
        return

    item_id = int(item_id_str)

    try:
        with open("catalog_data.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    found = False
    item_data = []
    for line in lines:
        if line.startswith(str(item_id)):
            found = True
            item_data = line.strip().split("|")[1:6]  # Extract name, price, description, category
            break

    if found:
        create_update_frame(item_id, item_data)
    else:
        messagebox.showerror("Error", f"No corresponding item found for Item ID: {item_id}")


def create_update_frame(item_id, item_data):
    global frame_screen, image_path_entry, image_preview_label

    frame_screen.destroy()  # Destroy the existing frame
    frame_screen = Frame(root, width=920, height=536, borderwidth=10, relief="flat")
    frame_screen.place(x=360, y=184)
    entry_font = font.Font(size=20)  # Set the desired font size

    name_label = Label(frame_screen, text="Name:")
    name_label.place(x=100, y=30)
    name_entry = ttk.Entry(frame_screen, width=40, font=entry_font)
    name_entry.insert(0, item_data[0])  # Pre-fill with existing name
    name_entry.place(x=100, y=60, height=58)

    price_label = Label(frame_screen, text="Price:")
    price_label.place(x=100, y=130)
    price_entry = ttk.Entry(frame_screen, width=40, font=entry_font, validate="key",
                            validatecommand=(frame_screen.register(validate_float), '%P'))
    price_entry.insert(0, item_data[1])  # Pre-fill with existing price
    price_entry.place(x=100, y=158, height=58)

    description_label = Label(frame_screen, text="Description:")
    description_label.place(x=100, y=226)
    description_entry = ttk.Entry(frame_screen, width=40, font=entry_font)
    description_entry.insert(0, item_data[2])  # Pre-fill with existing description
    description_entry.place(x=100, y=254, height=58)

    category_label = Label(frame_screen, text="Category:")
    category_label.place(x=100, y=322)
    categories = [
        "Makeup",
        "Fragrance",
        "Skincare",
        "Bath and Body",
        "Intimate Apparel",
        "Accessories",
        "Jewelry",
        "Men's Store",
        "Home & Kitchen",
        "Nutrition",
        "Other"
    ]
    category_var = StringVar()
    category_var.set(item_data[3].strip())  # Pre-select existing category

    category_dropdown = OptionMenu(frame_screen, category_var, *categories)
    category_dropdown.place(x=100, y=350, height=30, width=150)

    # Image Preview Label
    image_preview_label = Label(frame_screen, text="Image Preview:")
    image_preview_label.place(x=260, y=322)

    # Entry for image path
    image_path_entry = ttk.Entry(frame_screen, width=40, font=entry_font)
    image_path_entry.insert(0, item_data[4] if len(item_data) > 4 else "")  # Pre-fill with existing image path
    image_path_entry.place(x=100, y=480, height=30, width=83)

    # Load and display the image preview
    update_image_preview1(item_data[4] if len(item_data) > 4 else "")  # Initial image preview

    # Load and display the image preview
    image_path = item_data[4] if len(item_data) > 4 else ""
    img = Image.open(image_path)
    img.thumbnail((150, 150), Image.BICUBIC)
    preview_photo = ImageTk.PhotoImage(img)
    image_preview = Label(frame_screen, image=preview_photo)
    image_preview.photo = preview_photo  # To prevent image from being garbage collected
    image_preview.place(x=500, y=428)

    # Button for updating the image
    update_image_button = ttk.Button(frame_screen, text="Update Image", command=update_image_path_button)
    update_image_button.place(x=100, y=400, height=30)

    # Save button
    save_button = ttk.Button(frame_screen, text="Save",
                             command=lambda: save_updated_item(item_id, name_entry.get(), price_entry.get(),
                                                               description_entry.get(), category_var.get(),
                                                               image_path_entry))
    save_button.place(x=100, y=440, height=30, width=83)
    # Close button
    close_button = ttk.Button(frame_screen, text="Close", command=reset_frame)
    close_button.place(x=100, y=480, height=30, width=83)


def update_image_preview1(image_path):
    global frame_screen, image_preview_label

    # Destroy the existing image preview label
    if hasattr(image_preview_label, 'image_preview'):
        image_preview_label.image_preview.destroy()

    # Image Preview Label
    image_preview_label = Label(frame_screen, text="Image Preview:")
    image_preview_label.place(x=260, y=322)

    # Load and display the new image preview
    img = Image.open(image_path)
    img.thumbnail((150, 150), Image.BICUBIC)
    preview_photo = ImageTk.PhotoImage(img)
    image_preview = Label(frame_screen, image=preview_photo)
    image_preview.photo = preview_photo  # To prevent the image from being garbage collected
    image_preview.place(x=500, y=428)
    image_preview_label.image_preview = image_preview


def update_image_path_button():
    global image_path_entry

    # Use a file dialog to get the new image path from the user
    new_image_path = filedialog.askopenfilename(title="Select Image File",
                                                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])

    # Update the entry widget with the selected image path
    image_path_entry.delete(0, tk.END)
    image_path_entry.insert(0, new_image_path)

    # Optionally, you can display a message to inform the user about the update
    update_image_preview1(new_image_path)


def update_image_path(item_id, new_image_path):
    try:
        with open("catalog_data.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    updated_data = []
    for line in lines:
        if line.startswith(str(item_id)):
            # Update the image path
            updated_line = f"{line.strip()}, {new_image_path}\n"
            updated_data.append(updated_line)
        else:
            updated_data.append(line)

    with open("catalog_data.txt", "w") as file:
        file.writelines(updated_data)


def save_updated_item(item_id, new_name, new_price, new_description, new_category, image_path_entry):
    try:
        with open("catalog_data.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    # Check for empty fields, non-numeric price, category not selected
    try:
        new_price = float(new_price)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid numeric value for the price.")
        return

    if not new_price or not isinstance(new_price, (int, float)):
        messagebox.showerror("Error", "Please enter a valid numeric value for the price.")
        return

    # Check if the item name already exists in the catalog, excluding the current item being updated
    if is_duplicate_name(new_name) and new_name != get_item_name_by_id(item_id):
        messagebox.showerror("Error", "Item name already exists in the catalog. Please choose a different name.")
        return

    # Replace "|" with "\" in item_name and item_description
    item_name_cleaned = new_name.replace("|", "\\")
    item_description_cleaned = new_description.replace("\n", " ").replace("|", "\\")

    updated_data = []
    for line in lines:
        if line.startswith(str(item_id)):
            # Extract the existing image path
            existing_image_path = line.strip().split("|")[5]

            # Check if the data is the same as existing data
            if (
                    new_name == line.strip().split("|")[1] and
                    new_price == float(line.strip().split("|")[2]) and
                    new_description == line.strip().split("|")[3] and
                    new_category == line.strip().split("|")[4] and
                    image_path_entry.get() == existing_image_path
            ):
                messagebox.showinfo("Info", "No changes detected. Item not updated.")
                reset_frame()  # Close the update frame
                return

            # Update the name, price, category, and description if provided
            updated_line = (
                f"{item_id}|{item_name_cleaned}|{new_price}|{item_description_cleaned}|{new_category}|{image_path_entry.get()}\n"
            )
            updated_data.append(updated_line)
        else:
            updated_data.append(line)

    with open("catalog_data.txt", "w") as file:
        file.writelines(updated_data)

    messagebox.showinfo("Success", f"Item with Item ID {item_id} updated successfully!")
    reset_frame()  # Close the update frame


def get_item_name_by_id(item_id):
    try:
        with open("catalog_data.txt", "r") as file:
            for line in file:
                data = line.strip().split("|")
                if data[0] == str(item_id):
                    return data[1]
    except FileNotFoundError:
        return None


def display_table():
    global table, category_var  # Declare category_var as global
    # Reset the frame before creating new widgets
    reset_frame()
    if not catalog_file_exists():
        messagebox.showerror("Error", "Catalog file does not exist. Please add some item first")
        return
    try:
        with open("catalog_data.txt", "r") as file:
            first_line = file.readline()
            if not first_line.strip():
                # File is empty, show a message and return
                messagebox.showinfo("Info", "Catalog file is empty. Please add some items.")
                return
    except FileNotFoundError:
        messagebox.showerror("Error", "Catalog data file not found.")
        return

    generate_pdf_image = PhotoImage(file='pdfbutton.png')
    generate_pdf_button = Button(frame_screen, text="Generate PDF", image=generate_pdf_image, bg='#F52D2D',
                                 borderwidth=0,
                                 command=generate_pdf_from_table)
    generate_pdf_button.image = generate_pdf_image
    generate_pdf_button.place(x=855, y=0, anchor='nw')

    # Create search entry, category dropdown, and button
    search_label = ttk.Label(frame_screen, text="Search by Name:")
    search_label.place(x=10, y=10)

    search_entry = ttk.Entry(frame_screen, width=20)
    search_entry.place(x=120, y=10)

    # Category dropdown using Menubutton
    category_label = Label(frame_screen, text="Category:")
    category_label.place(x=350, y=10)

    categories = [
        "All",
        "Makeup",
        "Fragrance",
        "Skincare",
        "Bath and Body",
        "Intimate Apparel",
        "Accessories",
        "Jewelry",
        "Men's Store",
        "Home & Kitchen",
        "Nutrition",
        "Other"
    ]

    category_var = StringVar()
    category_var.set(categories[0])  # Set default category

    category_menu = Menubutton(frame_screen, textvariable=category_var, indicatoron=True, borderwidth=1,
                               relief="raised", width=10)
    category_menu.place(x=420, y=7, height=30)

    category_menu.menu = Menu(category_menu, tearoff=False)
    category_menu["menu"] = category_menu.menu

    for category in categories:
        category_menu.menu.add_radiobutton(label=category, variable=category_var, value=category)

    search_button = ttk.Button(frame_screen, text="Search",
                               command=lambda: search_and_display_table(search_entry.get(), category_var.get()))
    search_button.place(x=550, y=7)

    # Create Treeview widget
    table = ttk.Treeview(frame_screen, columns=('ID', 'Name', 'Price', 'Description', 'Category'), show='headings')
    table.place(x=0, y=40, width=890, height=430)

    # Set column headings
    table.heading('ID', text='ID')
    table.heading('Name', text='Name')
    table.heading('Price', text='Price')
    table.heading('Description', text='Description')
    table.heading('Category', text='Category')

    # Set column widths
    column_widths = {'ID': 50, 'Name': 150, 'Price': 100, 'Description': 100, 'Category': 100}
    for column, width in column_widths.items():
        table.column(column, width=width)

    # Set font size for the entire table
    font_size = 12  # Adjust the font size as needed
    font_style = font.Font(size=font_size)
    table.tag_configure('myfont', font=font_style)

    # Add a vertical scrollbar
    scrollbar = ttk.Scrollbar(frame_screen, orient='vertical', command=table.yview)
    scrollbar.place(x=870, y=50, height=410)
    table.configure(yscrollcommand=scrollbar.set)

    # Event handler for resetting column widths
    def reset_column_widths(event):
        for column, width in column_widths.items():
            table.column(column, width=width)

    # Bind the callback function to the cell click event
    def on_cell_click(event):
        if not table.selection():
            # No item is selected, do nothing
            return

        item = table.selection()[0]
        item_data = table.item(item, 'values')
        full_description = item_data[3] if item_data else ""  # Assuming description is at index 3

        # Deselect the currently selected item
        table.selection_remove(item)

        # Display full description in a pop-up window
        simpledialog.messagebox.showinfo("Full Description", full_description)

    table.bind('<ButtonRelease-1>', on_cell_click)

    # Bind the event handler to the column header
    for column in column_widths.keys():
        table.heading(column, text=column, command=lambda c=column: reset_column_widths(c))
        table.heading(column, anchor="w")

    try:
        with open("catalog_data.txt", "r") as file:
            for line in file:
                data = line.strip().split("|")
                table.insert('', index=0, values=(data[0], data[1], data[2], data[3], data[4]), tags='myfont')
    except FileNotFoundError:
        messagebox.showerror("Error", "Catalog data file not found.")

    # Store the table globally
    table = table
    # Other widgets (close button)
    close_button = ttk.Button(frame_screen, text="Close", command=reset_frame)
    close_button.place(x=100, y=480, height=30)


def search_and_display_table(search_term, selected_category):
    global table  # Access the global table variable
    table.delete(*table.get_children())  # Clear the existing table in the table

    try:
        with open("catalog_data.txt", "r") as file:
            for line in file:
                data = line.strip().split("|")
                if (selected_category == "All" or data[4] == selected_category) and search_term.lower() in data[1].lower():
                    table.insert('', index=0, values=(data[0], data[1], data[2], data[3], data[4]), tags='myfont')
    except FileNotFoundError:
        messagebox.showerror("Error", "Catalog data file not found.")


class PDFWithFooter(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", size=10)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, 'C')


def truncate_text(text, max_length):
    return (text[:max_length] + '...') if len(text) > max_length else text


def generate_pdf_from_table():
    global table  # Access the global table variable

    # Check if the table is empty
    if not table.get_children():
        messagebox.showerror("Error", "Table is empty. Please add items before generating a PDF.")
        return

    # Prompt the user for a PDF file name
    pdf_file_name = simpledialog.askstring("PDF File Name", "Enter a name for the PDF file:")

    # Check if the user provided a name
    if pdf_file_name is None or pdf_file_name.strip() == "":
        messagebox.showerror("Error", "Invalid PDF file name. Please provide a valid name.")
        return

    # Construct the PDF file path
    pdf_file_path = f"{pdf_file_name.strip()}.pdf"

    # Check if the file already exists
    if os.path.exists(pdf_file_path):
        # Ask the user if they want to overwrite the existing file
        response = messagebox.askyesno("File Exists",
                                       f"A file named '{pdf_file_name}' already exists. Do you want to overwrite it?")

        if not response:
            return  # User chose not to overwrite, do nothing

    # Get the table data
    data = []
    for item_id in table.get_children():
        item_data = table.item(item_id)['values']
        truncated_data = [truncate_text(str(col), 30) for col in item_data]  # Adjust max_length as needed
        data.append(truncated_data)

    # Create a PDF document with footer
    pdf = PDFWithFooter()

    # Add the first page
    pdf.add_page()

    # Add Avon logo to the top of the PDF
    avon_logo = "avonlogo.png"  # Adjust the path accordingly
    pdf.image(avon_logo, x=10, y=8, w=30)

    # Set font for the title
    pdf.set_font("Arial", 'B', 16)
    pdf.ln(10)  # Move down to leave space between logo and title
    pdf.cell(0, 10, 'Avon Catalog', ln=True, align='C')

    # Move down to leave space for the table
    pdf.ln(20)

    # Set font for the table content
    pdf.set_font("Arial", size=12)
    pdf.set_font("Arial", size=12)

    # Set background color for header row
    pdf.set_fill_color(228, 4, 75)

    # Define the column widths
    col_widths = [30, 40, 40, 40, 40]

    # Add column headings to PDF
    for i, col in enumerate(table["columns"]):
        pdf.cell(col_widths[i], 10, str(col), border=1, fill=True, ln=False)

    pdf.ln()

    # Set background colors for data rows
    pdf.set_fill_color(255, 255, 255)
    for row in data:
        for i, col in enumerate(row):
            pdf.cell(col_widths[i], 10, truncate_text(str(col), 15), border=1, fill=True,
                     ln=False)  # Adjust max_length as needed
        pdf.ln(10)  # Leave space between rows

        # Check if there's enough space for another row, if not, add a new page
        if pdf.get_y() + 20 > pdf.h - 15:
            pdf.add_page()

    try:
        # Attempt to save the PDF file
        pdf.output(pdf_file_path)
        messagebox.showinfo("Success", f"PDF '{pdf_file_name}' generated successfully.")
    except PermissionError:
        # Handle the case where the file is in use with a dialog box
        error_message = (
            f"The file '{pdf_file_path}' is currently open. "
            f"Please close it before generating a new PDF."
        )
        messagebox.showerror("Permission Error", error_message)


def load_from_file():
    global item_list
    try:
        with open("catalog_data.txt", "r") as file:
            for line in file:
                values = line.strip().split("|")
                if len(values) >= 6:  # Ensure there are at least 6 elements in the list
                    # Assuming the format is: ID, Name, Price, Description, Category, ImagePath
                    item = {
                        'id': values[0],
                        'name': values[1],
                        'price': float(values[2]),  # Convert 'price' to float
                        'description': values[3],
                        'category': values[4],
                        'image_path': values[5].strip()  # Remove leading/trailing spaces from the file path
                    }
                    item_list.append(item)  # Append the item to user_list
                else:
                    print(f"Skipping invalid line: {line}")

            # Update the user interface with the loaded catalog data

    except FileNotFoundError:
        pass


def create_item_boxes():
    global canvas, canvas_frame  # Declare canvas and canvas_frame as global

    # Clear existing item boxes
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    # Create a dictionary to store items by category
    items_by_category = {}

    for item in item_list:
        category = item['category']
        if category not in items_by_category:
            items_by_category[category] = []
        items_by_category[category].append(item)

    # Create a frame with a custom border color
    box_frame = tk.Frame(canvas_frame, relief="solid", highlightbackground="#E4044B")
    box_frame.grid(row=0, column=0, padx=5, pady=5)

    # Iterate through each category and display items
    for category, items in items_by_category.items():
        # Add category title row
        title_row = tk.Frame(box_frame, bd=0, relief="flat", bg="#E4044B")
        title_row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        category_title = ttk.Label(title_row, text=category, font=("Arial", 14, "bold"), foreground="white",
                                   background="#E4044B")
        category_title.pack(side=tk.LEFT, padx=5, pady=5)

        # Add items in a 3 by 3 grid
        items_frame = tk.Frame(box_frame, bd=0, relief="flat", bg="white")
        items_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)

        for i, item in enumerate(items):
            img = Image.open(item['image_path'])
            img.thumbnail((254, 254), Image.BICUBIC)  # Resize to 254 by 254 pixels
            photo = ImageTk.PhotoImage(img)

            # Change the border color here
            item_frame = tk.Frame(items_frame, bd=1, relief="solid", highlightbackground="#e7004c")
            item_frame.grid(row=i // 3, column=i % 3, padx=5, pady=5)

            item_box = tk.Label(item_frame, text=item['name'], image=photo, compound=tk.TOP)
            item_box.photo = photo
            font_size = 14
            item_box['font'] = font.Font(size=font_size)
            item_box.pack()

            # Bind the click event to show_item_info function
            item_box.bind("<Button-1>", lambda event, u=item: show_item_info(u))

    # Configure grid weights for resizing
    box_frame.grid_columnconfigure(0, weight=1)
    box_frame.grid_rowconfigure(1, weight=1)

    # Update the scroll region to include the new item boxes
    canvas.configure(scrollregion=canvas.bbox("all"))

    # Bind mouse wheel event for vertical scrolling
    canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

    # Bind the event to update the scroll region when the canvas_frame size changes
    canvas_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))


def display_items():
    global canvas, item_list, canvas_frame

    # Reset the canvas and frame
    reset_frame()

    # Create a Canvas widget with a vertical scrollbar
    canvas = tk.Canvas(frame_screen, width=884, height=539, bd=2)
    canvas.place(x=0, y=0)
    canvas.grid(row=2, column=0, columnspan=4, sticky='nsew')

    # Scroll Bar
    scrollbar = tk.Scrollbar(frame_screen, command=canvas.yview)
    scrollbar.grid(row=2, column=4, sticky='ns')
    canvas.configure(yscrollcommand=scrollbar.set)

    # Canvas
    canvas_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=canvas_frame, anchor=tk.NW)

    # List to store item data
    item_list = []

    # Load existing item data from file
    load_from_file()

    # Sort items
    item_list.sort(key=lambda x: x['name'].lower())

    # Display existing item data
    create_item_boxes()
    if not item_list:
        # Return a message if there are no items in the catalog
        messagebox.showinfo("No Items", "Catalog file is empty. Please add some items.")
        return
    # Configure grid weights for resizing
    for i in range(4):
        root.grid_columnconfigure(i, weight=1)
    root.grid_rowconfigure(2, weight=1)
    canvas.configure(scrollregion=(0, 0, 500, 500))  # Adjust these values as needed

    # Bind the event to update the scroll region when the canvas_frame size changes
    canvas_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

    # Other widgets (close button)
    close_image = PhotoImage(file="close_button.png")
    close_button = ttk.Button(frame_screen, text="Close", image=close_image, command=reset_frame)
    close_button.image = close_image  # Ensure the image is not garbage collected
    close_button.place(x=845, y=0, height=50, width=50)


def close_current_info_window():
    global current_info_window
    if current_info_window:
        current_info_window.destroy()
        current_info_window = None

def show_item_info(item):
    global current_info_window

    close_current_info_window()  # Close the previous window if it exists

    info_window = tk.Toplevel(root)
    info_window.title("Item Information")
    info_window.resizable(False, False)

    # Load the image and create a resized thumbnail
    img = Image.open(item['image_path'])
    img.thumbnail((254, 254), Image.BICUBIC)
    photo = ImageTk.PhotoImage(img)

    # Create a label with the item's name and thumbnail image
    item_frame = tk.Frame(info_window)
    item_frame.pack(padx=10, pady=10)

    item_box = ttk.Label(item_frame, text=item['name'], image=photo, compound=tk.TOP, font=("Arial", 14))
    item_box.photo = photo
    item_box.pack()

    # Create a frame for the price display
    price_frame = tk.Frame(info_window, bg="#e7004c", padx=10, pady=5, relief="solid", borderwidth=1, bd=1)
    price_frame.pack(pady=5)

    # Display the rounded price
    price_label = ttk.Label(price_frame, text=f"Price: ₱{item['price']:.2f}", font=("Arial", 12),
                            foreground="white", background="#e7004c")
    price_label.pack()

    # Create a scrolled text widget for the description
    description_frame = tk.Frame(info_window, padx=10, pady=5)
    description_frame.pack()

    description_text = tk.Text(description_frame, wrap="word", height=5, width=40)
    description_text.insert(tk.END, item['description'])
    description_text.config(state=tk.DISABLED)
    description_text.pack(side=tk.LEFT, fill=tk.Y)

    # Create a vertical scrollbar for the description
    description_scrollbar = ttk.Scrollbar(description_frame, orient="vertical", command=description_text.yview)
    description_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    description_text["yscrollcommand"] = description_scrollbar.set

    # Display additional information using a Text widget
    additional_info_text = tk.Text(info_window, wrap="word", height=2, width=40)
    additional_info_text.insert(tk.END, f"Category: {item['category']}\nID: {item['id']}")
    additional_info_text.config(state=tk.DISABLED)
    additional_info_text.pack(pady=10)

    # Center the window on the screen
    info_window.update_idletasks()
    width = info_window.winfo_width()
    height = info_window.winfo_height()
    x = (info_window.winfo_screenwidth() - width) // 2
    y = (info_window.winfo_screenheight() - height) // 2
    info_window.geometry(f"{width}x{height}+{x}+{y}")

    # Update the current information window
    current_info_window = info_window
root = Tk()
root.geometry('1280x720')
root.resizable(False, False)
root.title('Avon Catalog Management System')

logo_image = PhotoImage(file='avonlogo.png')
root.iconphoto(True, logo_image)

framePhoto = PhotoImage(file='Frame 1.png')
frame_photo_label = Label(root, border=0, image=framePhoto)
frame_photo_label.pack(fill=BOTH, expand=True)

# Logo
slogan_frame = PhotoImage(file='Group 1.png')
slogan_frame_label = Label(root, image=slogan_frame, border=0, bg='#E4044B')
slogan_frame_label.place(x=0, y=140)

frame_screen = Frame(root, width=920, height=536, borderwidth=10, relief="flat")
frame_screen.place(x=360, y=184)

add_item_image = PhotoImage(file='add_button.png')
add_button = Button(root, text="Add Item", image=add_item_image, bg='#FFFFFF', borderwidth=0,
                    command=add_item)
add_button.image = add_item_image
add_button.place(x=19, y=194, anchor='nw')

display_table_image = PhotoImage(file='display_table_button.png')
display_table_button = Button(root, text="Display table", image=display_table_image, bg='#FFFFFF', borderwidth=0,
                              command=display_table)
display_table_button.image = display_table_image
display_table_button.place(x=19, y=295, anchor='nw')

display_items_image = PhotoImage(file='display_items_button.png')
display_button = Button(root, text="Delete Item", image=display_items_image, bg='#FFFFFF', borderwidth=0,
                        command=display_items)
display_button.image = display_items_image
display_button.place(x=19, y=396, anchor='nw')

delete_item_image = PhotoImage(file='delete_button.png')
delete_button = Button(root, text="Delete Item", image=delete_item_image, bg='#FFFFFF', borderwidth=0,
                       command=delete)
delete_button.image = delete_item_image
delete_button.place(x=19, y=497, anchor='nw')

update_item_image = PhotoImage(file='update_button.png')
update_button = Button(root, text="Update Item", image=update_item_image, bg='#FFFFFF', borderwidth=0,
                       command=update_item)
update_button.image = update_item_image
update_button.place(x=19, y=598, anchor='nw')
root.mainloop()
