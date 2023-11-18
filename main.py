from tkinter import *
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import random

class MainUI:
    def __init__(self, root, frame_photo_path, title_logo_path, exit_photo_path, add_item_path, display_items_path, update_item_path, delete_item_path):
        self.root = root
        self.root.overrideredirect(1)
        self.root.wm_attributes("-transparentcolor", "grey")

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set window dimensions
        window_width = 627
        window_height = 459

        # Calculate position for the window to appear in the center
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.root.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')

        # Variables to store offset
        global offset_x, offset_y
        offset_x = 0
        offset_y = 0

        # Photo sidebar
        frame_photo = PhotoImage(file=frame_photo_path)
        frameLabel = Label(root, border=0, bg='grey', image=frame_photo)
        frameLabel.image = frame_photo  # Keep a reference to the image
        frameLabel.pack(fill=BOTH, expand=True)

        # Frame photo bind
        frameLabel.bind("<ButtonPress-1>", self.move_start)
        frameLabel.bind("<B1-Motion>", self.move_app)

        # Logo
        title_logo = PhotoImage(file=title_logo_path)
        titleLabel = Label(root, image=title_logo, border=0, bg='#7D4D47')
        titleLabel.image = title_logo  # Keep a reference to the image
        titleLabel.place(x=52, y=17)

        # Exit button photo
        exit_photo = PhotoImage(file=exit_photo_path)

        # Exit label
        exitLabel = Label(root, image=exit_photo, border=0, bg='#7D4D47')
        exitLabel.image = exit_photo  # Keep a reference to the image
        exitLabel.place(x=564, y=2)

        # Exit bind
        exitLabel.bind("<Button-1>", lambda e: self.exit_click())

        # Add Photo
        add_item = PhotoImage(file=add_item_path)

        # Buttons
        addButton = Button(root, text="Add Item", image=add_item, bg='#FFFFFF', borderwidth=0,
                           command=self.add_item)
        addButton.image = add_item
        addButton.place(x=19, y=78, anchor='nw')

        display_items = PhotoImage(file=display_items_path)
        displayButton = Button(root, text="Display Items", image=display_items, bg='#FFFFFF', borderwidth=0,
                               command=self.display_item)
        displayButton.image = display_items
        displayButton.place(x=179, y=78, anchor='nw')

        update_item = PhotoImage(file=update_item_path)
        updateButton = Button(root, text="Update Item", image=update_item, bg='#FFFFFF', borderwidth=0,
                              command=self.update_item)
        updateButton.image = update_item
        updateButton.place(x=339, y=78, anchor='nw')

        delete_item = PhotoImage(file=delete_item_path)
        deleteButton = Button(root, text="Delete Item", image=delete_item, bg='#FFFFFF', borderwidth=0,
                              command=self.delete_item)
        deleteButton.image = delete_item
        deleteButton.place(x=499, y=78, anchor='nw')

        self.data_file = "catalog_data.txt"
        # Display Items Table
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("ID", "Title", "Category", "Price")

        # Set column headings
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("Title", text="Title", anchor=tk.W)
        self.tree.heading("Category", text="Category", anchor=tk.W)
        self.tree.heading("Price", text="Price", anchor=tk.W)

        # Set column widths
        self.tree.column("#0", stretch=tk.NO, minwidth=0, width=0)
        self.tree.column("ID", stretch=tk.NO, minwidth=0, width=50)
        self.tree.column("Title", stretch=tk.NO, minwidth=0, width=150)
        self.tree.column("Category", stretch=tk.NO, minwidth=0, width=200)
        self.tree.column("Price", stretch=tk.NO, minwidth=0, width=100)

        self.tree.pack(pady=20)

        self.populate_table()  # Populate the table with existing items

    def populate_table(self):
        try:
            with open("catalog_data.txt", "r") as file:
                items = file.readlines()
        except FileNotFoundError:
            items = []

        for item in items:
            parts = item.split(", ")
            if len(parts) >= 5:  # Updated to check for at least 5 parts
                item_id, title, category, price, brand = parts[0], parts[1], parts[2], parts[3], parts[4]
                self.tree.insert("", tk.END, values=(item_id, title, category, price, brand))

    def move_start(self, event):
        global offset_x, offset_y
        offset_x = event.x_root - self.root.winfo_x()
        offset_y = event.y_root - self.root.winfo_y()

    def move_app(self, event):
        self.root.geometry(f'+{event.x_root - offset_x}+{event.y_root - offset_y}')

    def exit_click(self):
        self.root.quit()

    def add_item(self):
        AddItemUI(self.root, self)

    def display_item(self):
        display_ui = DisplayItemUI(self)
        display_ui.show()

    def update_item(self):
        UpdateItemUI(self.root)

    def delete_item(self):
        DeleteItemUI(self.root)

class AddItemUI:
    def __init__(self, root, main_ui):
        self.root = Toplevel(root)
        self.root.title("Add Item")

        self.main_ui = main_ui

        # Item Name
        title_label = tk.Label(self.root, text="Enter Item Name:")
        title_label.pack()

        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack()

        brand_label = tk.Label(self.root, text="Enter Brand:")
        brand_label.pack()

        self.brand_entry = tk.Entry(self.root)
        self.brand_entry.pack()

        price_label = tk.Label(self.root, text="Enter Price:")
        price_label.pack()

        self.price_entry = tk.Entry(self.root)
        self.price_entry.pack()

        category_label = tk.Label(self.root, text="Select Category:")
        category_label.pack()

        categories = ["None", "Apparel and Fashion", "Electronics", "Home and Garden", "Toys and Games",
                      "Beauty and Personal Care", "Sports and Outdoors", "Books and Stationery",
                      "Health and Wellness", "Automotive", "Electrical Appliances", "Office Supplies",
                      "Food and Beverages", "Jewelry and Accessories", "Pet Supplies", "Musical Instruments", "Other"]

        self.category_var = StringVar()
        self.category_var.set(categories[0])  # Set the default category to "None"
        category_dropdown = tk.OptionMenu(self.root, self.category_var, *categories)
        category_dropdown.pack()

        save_button = tk.Button(self.root, text="Save", command=self.try_save_item)
        save_button.pack()

        # Center the window after fully initializing
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2
        self.root.geometry("+%d+%d" % (x, y))

    def try_save_item(self):
        title = self.title_entry.get()
        category = self.category_var.get()
        price = self.price_entry.get()
        brand = self.brand_entry.get()

        error_messages = []

        if not title:
            error_messages.append("Please enter a valid item name.")

        if not price.isdigit():
            error_messages.append("Please enter a valid price (numeric value).")

        if not category or category == "None":
            error_messages.append("Please select a valid category.")

        if error_messages:
            error_message = "\n".join(error_messages)
            messagebox.showerror("Error", error_message)
            return

        price = int(price)

        item_id = self.generate_unique_id()

        with open("catalog_data.txt", "a") as file:
            file.write(f"{item_id}, {title}, {category}, {price}, {brand}\n")

        success_message = f"Item added successfully!\nItem ID: {item_id}\n\n"
        success_message += f"Title: {title}\nCategory: {category}\nPrice: {price}\nBrand: {brand}"

        messagebox.showinfo("Success", success_message)

        self.root.destroy()
        self.main_ui.populate_table()
        root.focus_set()

class DisplayItemUI:
    def __init__(self, main_ui):
        self.main_ui = main_ui

        # Frame for DisplayItemUI
        self.frame = Frame(main_ui.root, bg='#7D4D47')
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Display Items Table in DisplayItemUI
        self.tree = ttk.Treeview(self.frame)
        self.tree["columns"] = ("ID", "Title", "Category", "Price")

        # Set column headings
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("Title", text="Title", anchor=tk.W)
        self.tree.heading("Category", text="Category", anchor=tk.W)
        self.tree.heading("Price", text="Price", anchor=tk.W)

        # Set column widths
        self.tree.column("#0", stretch=tk.NO, minwidth=0, width=0)
        self.tree.column("ID", stretch=tk.NO, minwidth=0, width=50)
        self.tree.column("Title", stretch=tk.NO, minwidth=0, width=150)
        self.tree.column("Category", stretch=tk.NO, minwidth=0, width=200)
        self.tree.column("Price", stretch=tk.NO, minwidth=0, width=100)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.pack(pady=20)

        self.populate_table()  # Populate the table with existing items

        # Return Button
        return_button = tk.Button(self.frame, text="Return", command=self.return_to_main_ui)
        return_button.pack(side="bottom")

    def populate_table(self):
        try:
            with open("catalog_data.txt", "r") as file:
                items = file.readlines()
        except FileNotFoundError:
            items = []

        for item in items:
            parts = item.split(", ")
            if len(parts) >= 4:
                item_id, title, category, price = parts[0], parts[1], parts[2], parts[3]
                self.tree.insert("", tk.END, values=(item_id, title, category, price))

    def show(self):
        # Display the frame
        self.frame.lift()

    def return_to_main_ui(self):
        self.frame.destroy()

class UpdateItemUI:
    def __init__(self, parent, main_ui):
        self.parent = parent
        self.root = Toplevel(self.parent)
        self.root.title("Update Item")
        self.main_ui = main_ui  # Store the reference to the main UI
        # Add UI elements for UpdateItem here

        while True:
            item_id = simpledialog.askstring("Update Item", "Enter Item ID to update:")
            if item_id is None:  # User clicked Cancel
                return  # Return to the main menu

            if item_id.isdigit():
                item_id = int(item_id)
                break
            else:
                messagebox.showerror("Error", "Please enter a valid number for the Item ID.")

        try:
            with open(self.main_ui.data_file, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            lines = []

        found = False
        for line in lines:
            if line.startswith(str(item_id)):
                found = True
                break

        if not found:
            messagebox.showerror("Error", f"No corresponding item found for Item ID: {item_id}")
            return  # Return to the main menu

        new_title = simpledialog.askstring("Update Item", "Enter new title (or leave blank to keep the current):")
        new_description = simpledialog.askstring("Update Item",
                                                 "Enter new description (or leave blank to keep the current):")
        new_price = simpledialog.askstring("Update Item", "Enter new price (or leave blank to keep the current):")

        # Update the item with the new values
        updated_data = []
        for line in lines:
            if line.startswith(str(item_id)):
                # Update title if not blank
                if new_title:
                    line = line.replace(line.split(", ")[1], f"{new_title}")

                # Update description if not blank
                if new_description:
                    line = line.replace(line.split(", ")[2], f"{new_description}")

                # Update price if not blank
                if new_price:
                    line = line.replace(line.split(", ")[3], f"{new_price}\n")

            updated_data.append(line)

        with open(self.main_ui.data_file, "w") as file:
            file.writelines(updated_data)

        messagebox.showinfo("Success", f"Item with Item ID {item_id} updated successfully!")



class DeleteItemUI:
    def __init__(self, main_ui):
        self.main_ui = main_ui  # Store the reference to the main UI
        self.root = Toplevel(self.main_ui.root)
        self.root.title("Delete Item")

        # Add UI elements for DeleteItem here
        label = Label(self.root, text="Delete Item by ID:")
        label.pack(pady=10)

        self.item_id_entry = Entry(self.root)
        self.item_id_entry.pack(pady=10)

        delete_button = Button(self.root, text="Delete", command=self.delete_item)
        delete_button.pack(pady=10)

    def delete_item(self):
        while True:
            item_id = simpledialog.askstring("Delete Item", "Enter Item ID to delete:")

            if item_id is None:  # User clicked Cancel
                return  # Return to the main menu

            if not item_id.isdigit():
                messagebox.showerror("Error", "Please enter a valid number for the Item ID.")
                continue  # Ask the user for input again

            item_id = int(item_id)

            try:
                with open(self.main_ui.data_file, "r") as file:
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
                with open(self.main_ui.data_file, "w") as file:
                    file.writelines(updated_data)

                messagebox.showinfo("Success", f"Item with Item ID {item_id} deleted successfully!")
                break  # Exit the loop if the item is found and deleted
            else:
                retry = messagebox.askretrycancel("Error",
                                                  f"No corresponding item found for Item ID: {item_id}. Try again?")

                if not retry:
                    return  # Return to the main menu


if __name__ == "__main__":
    root = Tk()
    MainUI(root, 'Frame 1.png', 'KATALOG.png', 'exit.png','AddItem.png','DisplayItems.png','UpdateItem.png','DeleteItem.png',)
    root.mainloop()
