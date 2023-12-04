────────────────────────────────────────────
◆ The Avon Catalog Management System ◆
────────────────────────────────────────────
◆ Introduction

The Avon Catalog Management System is a simple Python program designed to help you efficiently manage your catalog of items.
With a user-friendly graphical user interface (GUI) built using the Tkinter library,
you'll be able to effortlessly add, delete, update, and display items in your catalog.

Enjoy managing your catalog effortlessly with the Avon Catalog Management System!

────────────────────────────────────────────────────────────────────────────────────────
◆◆◆ Important Notes

◆ The data will be saved in a text file named "catalog_data.txt" separated by pipe '|' if the user put pipe it will be replaced by backslash "\" to make the data not messy.

◆ The user can also generate pdf files of the current table. The table can be sorted in categories as well as the name that the user may input in the search bar. But it will not make any changes to the data inside the text file.

◆ Any item that is deleted will not be restored

◆ The user is required to fill all the data entry that the add item provides.

◆ Open the "main.exe" file to run the program

────────────────────────────────────────────────────────────────────────────────────────
◆ Guides

...Add Item...

	To add items to your catalog, simply provide the image, name, price, description, and category of the item.
	Once you've entered all the necessary information, click on the "Save" button to add it to your catalog.

...Display Table...

	Easily visualize all the items you've added to your catalog in a neat table format.
	You can also search for items by name or category using the search bar located above the displayed items.

...Display Items...

	View all items in a compact and organized manner. Simply click on an item to display more detailed information.

...Delete Item...

	If you wish to remove an item from your catalog, locate the ID of the item you want to delete.
	You can find the item ID in the Item ID column of the "Display Table".
	Enter the ID in the designated field and proceed to delete it.

...Update Item...

	To update an item, enter the ID of the item desired to be updated.
	A form similar from the "Add Item" will appear.
	You can find the item ID in the Item ID column of the "Display Table".
	Enter the ID in the designated field and proceed to update it.

◆ Libraries Used

The program uses the following libraries:

Tkinter: for creating the GUI
messagebox: for displaying error messages and information dialogs
font: for setting the font size of GUI elements
ttk: for creating themed GUI elements
simpledialog: for displaying a dialog box to get user input
filedialog: for opening a file dialog to select an image file
random: for generating unique item IDs
fpdf: for generating PDF files
PIL: for image processing


◆ Functions

...The program consists of several functions:...

catalog_file_exists(): checks if the catalog data file exists
reset_frame(): resets the frame by destroying the existing frame and creating a new one
add_item(): creates a form for adding a new item to the catalog
select_image(): opens a file dialog to select an image file for an item
update_image_preview(): updates the image preview label with the selected image
save_item(): saves the new item to the catalog data file
is_duplicate_name(): checks if an item name already exists in the catalog
generate_unique_id(): generates a unique item ID
delete(): creates a form for deleting an item from the catalog
delete_item(): deletes an item from the catalog data file
update_item(): creates a form for updating an item in the catalog
update_item_ui(): creates a form with pre-filled fields for updating an item
create_update_frame(): creates a form for updating an item with pre-filled fields
update_image_path(): updates the image path of an item in the catalog data file
save_updated_item(): saves the updated item to the catalog data file
get_item_name_by_id(): retrieves the name of an item by its ID
display_table(): displays the catalog data in a table format
search_and_display_table(): searches for items by name and category and displays the results in the table
PDFWithFooter(): a subclass of FPDF that adds a footer to each page of the generated PDF
truncate_text(): truncates a text string to a specified maximum length
generate_pdf_from_table(): generates a PDF file from the table data
load_from_file(): loads existing item data from the catalog data file
create_item_boxes(): creates item boxes for displaying items in a grid layout
display_items(): displays the items in the catalog using item boxes
show_item_info(): displays additional information about an item in a separate window

◆ Credits

...Team Kahit Ano...

Bronia, Irvin
Bombales, Rena
Daria, Jomel
Floresca, Karl
Molleno, Vincent
Ocol, John Michael
Samson, Rogie
San Juan, Regie
Valencia, Dexter
