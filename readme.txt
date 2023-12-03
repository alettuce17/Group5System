readme

The Avon Catalog Management System is a Python program that allows users to manage a catalog of items. The program provides a graphical user interface (GUI) built using the Tkinter library. Users can add, delete, update, and display items in the catalog.

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

The program consists of several functions:

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