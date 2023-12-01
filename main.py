from tkinter import *
from tkinter import messagebox, font, ttk, simpledialog
import random
from fpdf import FPDF


# Declare entry variables as global
name_entry = None
price_entry = None
description_entry = None
category_var = None
frame_visible = True
table = None  # Add a global variable for the table



def reset_frame():
    global frame_screen
    frame_screen.destroy()  # Destroy the existing frame
    frame_screen = Frame(root, width=920, height=536, borderwidth=10, relief="groove")
    frame_screen.place(x=360, y=184)


def add_item():
    global frame_screen, name_entry, price_entry, description_entry, category_var, frame_visible
    reset_frame()  # Reset the frame before creating new widgets
    font.Font(size=20)

    delete_label = Label(frame_screen, text="Add Item", font=("Helvetica", 24))
    delete_label.place(x=100, y=30)
    entry_font = font.Font(size=20)  # Set the desired font size
    name_label = Label(frame_screen, text="Name:")

    name_label.place(x=100, y=80)
    name_entry = Entry(frame_screen, width=40, font=entry_font)  # Set width to 70 characters
    name_entry.place(x=100, y=110, height=58)  # Set height to 58 pixels

    price_label = Label(frame_screen, text="Price:")
    price_label.place(x=100, y=180)
    price_entry = Entry(frame_screen, width=40, font=entry_font)
    price_entry.place(x=100, y=208, height=58)

    description_label = Label(frame_screen, text="Description:")
    description_label.place(x=100, y=276)
    description_entry = Entry(frame_screen, width=40, font=entry_font)
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

    # Other widgets (save button, close button) remain unchanged

    # Save button
    save_button = Button(frame_screen, text="Save", command=save_item)
    save_button.place(x=100, y=440, height=30)
    # Close button
    close_button = Button(frame_screen, text="Close", command=reset_frame)
    close_button.place(x=100, y=480, height=30)


def save_item():
    # Function to handle the "Save" button click
    global name_entry, price_entry, description_entry, category_var
    item_name = name_entry.get()
    item_price = price_entry.get()
    item_description = description_entry.get()
    item_category = category_var.get()

    # Check for empty fields, non-numeric price, and category not selected
    if not item_name or not item_price or not item_price.isdigit() or item_category == "None":
        messagebox.showerror("Error", "Please fill in all fields correctly and select a valid category.")
        return

    # Check if the item name already exists in the catalog
    if is_duplicate_name(item_name):
        messagebox.showerror("Error", "Item name already exists in the catalog. Please choose a different name.")
        return

    item_id = generate_unique_id()
    with open("catalog_data.txt", "a") as file:
        file.write(f"{item_id}, {item_name}, {item_price}, {item_description}, {item_category}\n")

    messagebox.showinfo("Success", f"Item added successfully!\nItem ID: {item_id}")


def is_duplicate_name(new_name):
    try:
        with open("catalog_data.txt", "r") as file:
            existing_names = [line.split(",")[1].strip() for line in file if line.strip() and line.split(",")]
            return new_name in existing_names
    except FileNotFoundError:
        return False


def generate_unique_id():
    try:
        with open("catalog_data.txt", "r") as file:
            existing_ids = {int(line.split(",")[0]) for line in file if line.strip() and line.split(",")}
    except FileNotFoundError:
        existing_ids = set()

    # Generate a new ID until a unique one is found
    new_id = random.randint(1000, 9999)
    while new_id in existing_ids:
        new_id = random.randint(1000, 9999)

    return new_id


def delete():
    global frame_screen, frame_visible
    reset_frame()  # Reset the frame before creating new widgets

    # Create UI for deleting an item
    entry_font = font.Font(size=20)  # Set the desired font size

    delete_label = Label(frame_screen, text="Delete Item", font=("Helvetica", 24))
    delete_label.place(x=100, y=30)

    item_id_label = Label(frame_screen, text="Enter Item ID to delete:")
    item_id_label.place(x=100, y=90)

    item_id_entry = Entry(frame_screen, width=40, font=entry_font)
    item_id_entry.place(x=100, y=120, height=58)

    delete_button = Button(frame_screen, text="Delete", command=lambda: delete_item(item_id_entry.get()))
    delete_button.place(x=100, y=188, height=30)

    # Close button
    close_button = Button(frame_screen, text="Close", command=reset_frame)
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

    entry_font = font.Font(size=20)  # Set the desired font size

    update_label = Label(frame_screen, text="Update Item", font=("Helvetica", 24))
    update_label.place(x=100, y=30)

    item_id_label = Label(frame_screen, text="Enter Item ID to update:")
    item_id_label.place(x=100, y=90)

    item_id_entry = Entry(frame_screen, width=40, font=entry_font)
    item_id_entry.place(x=100, y=120, height=58)

    update_button = Button(frame_screen, text="Update", command=lambda: update_item_ui(item_id_entry.get()))
    update_button.place(x=100, y=188, height=30)

    # Close button
    close_button = Button(frame_screen, text="Close", command=reset_frame)
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
            item_data = line.strip().split(", ")[1:5]  # Extract name, price, description, category
            break

    if found:
        create_update_frame(item_id, item_data)
    else:
        messagebox.showerror("Error", f"No corresponding item found for Item ID: {item_id}")


def create_update_frame(item_id, item_data):
    global frame_screen
    frame_screen.destroy()  # Destroy the existing frame
    frame_screen = Frame(root, width=920, height=536, borderwidth=10, relief="groove")
    frame_screen.place(x=360, y=184)
    entry_font = font.Font(size=20)  # Set the desired font size

    name_label = Label(frame_screen, text="Name:")
    name_label.place(x=100, y=30)
    name_entry = Entry(frame_screen, width=40, font=entry_font)
    name_entry.insert(0, item_data[0])  # Pre-fill with existing name
    name_entry.place(x=100, y=60, height=58)

    price_label = Label(frame_screen, text="Price:")
    price_label.place(x=100, y=130)
    price_entry = Entry(frame_screen, width=40, font=entry_font)
    price_entry.insert(0, item_data[1])  # Pre-fill with existing price
    price_entry.place(x=100, y=158, height=58)

    description_label = Label(frame_screen, text="Description:")
    description_label.place(x=100, y=226)
    description_entry = Entry(frame_screen, width=40, font=entry_font)
    description_entry.insert(0, item_data[2])  # Pre-fill with existing price
    description_entry.place(x=100, y=254, height=58)

    category_label = Label(frame_screen, text="Category:")
    category_label.place(x=100, y=322)
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
    category_var.set(item_data[3].strip())  # Pre-select existing category

    category_dropdown = OptionMenu(frame_screen, category_var, *categories)
    category_dropdown.place(x=100, y=350, height=30)

    # Save button
    save_button = Button(frame_screen, text="Save",
                         command=lambda: save_updated_item(item_id, name_entry.get(), price_entry.get(),
                                                           description_entry.get(), category_var.get()))
    save_button.place(x=100, y=418, height=58)
    # Close button
    close_button = Button(frame_screen, text="Close", command=reset_frame)
    close_button.place(x=250, y=418, height=58)


def save_updated_item(item_id, new_name, new_price, new_description, new_category):
    # Function to handle saving the updated item to the catalog
    try:
        with open("catalog_data.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    updated_data = []
    for line in lines:
        if line.startswith(str(item_id)):
            # Update the name, price, and category if provided
            updated_line = (
                f"{item_id}, {new_name}, {new_price}, {new_description}, "
                f"{line.strip().split(',')[4] if new_category == 'None' else new_category}\n"
            )
            updated_data.append(updated_line)
        else:
            updated_data.append(line)

    with open("catalog_data.txt", "w") as file:
        file.writelines(updated_data)

    messagebox.showinfo("Success", f"Item with Item ID {item_id} updated successfully!")
    reset_frame()  # Close the update frame


def display_items():
    global table, category_var  # Declare category_var as global
    # Reset the frame before creating new widgets
    reset_frame()

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
                               command=lambda: search_and_display_items(search_entry.get(), category_var.get()))
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

    table.configure(yscroll=scrollbar.set)

    # Event handler for resetting column widths
    def reset_column_widths(event):
        for column, width in column_widths.items():
            table.column(column, width=width)

    # Bind the callback function to the cell click event
    def on_cell_click(event):
        region = table.identify("region", event.x, event.y)

        if region == "heading":
            # Clicked on a column heading, not a cell
            return

        item = table.selection()[0]
        item_data = table.item(item, 'values')
        full_description = item_data[3]  # Assuming description is at index 3

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
                data = line.strip().split(", ")
                table.insert('', index=0, values=(data[0], data[1], data[2], data[3], data[4]), tags='myfont')
    except FileNotFoundError:
        messagebox.showerror("Error", "Catalog data file not found.")

    # Store the table globally
    table = table

    # Other widgets (close button)
    close_button = ttk.Button(frame_screen, text="Close", command=reset_frame)
    close_button.place(x=100, y=480, height=30)


def search_and_display_items(search_term, selected_category):
    global table  # Access the global table variable
    table.delete(*table.get_children())  # Clear the existing items in the table

    try:
        with open("catalog_data.txt", "r") as file:
            for line in file:
                data = line.strip().split(", ")
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

    # Set background color for header row
    pdf.set_fill_color(228, 4, 75)

    # Define the column widths based on your requirements
    col_widths = [30, 40, 40, 40, 40]

    # Add column headings to PDF
    for i, col in enumerate(table["columns"]):
        pdf.cell(col_widths[i], 10, str(col), border=1, fill=True, ln=False)

    pdf.ln()

    # Set background colors for data rows
    pdf.set_fill_color(255, 255, 255)
    for row in data:
        for i, col in enumerate(row):
            pdf.cell(col_widths[i], 10, truncate_text(str(col), 15), border=1, fill=True, ln=False)  # Adjust max_length as needed
        pdf.ln(10)  # Leave space between rows

        # Check if there's enough space for another row, if not, add a new page
        if pdf.get_y() + 20 > pdf.h - 15:
            pdf.add_page()

    pdf.output("Avon_Catalog.pdf")
    print("PDF generated successfully.")

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

frame_screen = Frame(root, width=920, height=536, borderwidth=10, relief="groove")
frame_screen.place(x=360, y=184)

add_item_image = PhotoImage(file='addbutton.png')
add_button = Button(root, text="Add Item", image=add_item_image, bg='#FFFFFF', borderwidth=0, command=add_item)
add_button.image = add_item_image
add_button.place(x=19, y=233, anchor='nw')

display_items_image = PhotoImage(file='displaybutton.png')
display_button = Button(root, text="Display Items", image=display_items_image, bg='#FFFFFF', borderwidth=0,
                        command=display_items)
display_button.image = display_items_image
display_button.place(x=19, y=341, anchor='nw')

update_item_image = PhotoImage(file='updatebutton.png')
update_button = Button(root, text="Update Item", image=update_item_image, bg='#FFFFFF', borderwidth=0,
                       command=update_item)
update_button.image = update_item_image
update_button.place(x=19, y=449, anchor='nw')

delete_item_image = PhotoImage(file='deletebutton.png')
delete_button = Button(root, text="Delete Item", image=delete_item_image, bg='#FFFFFF', borderwidth=0, command=delete)
delete_button.image = delete_item_image
delete_button.place(x=19, y=557, anchor='nw')

root.mainloop()
