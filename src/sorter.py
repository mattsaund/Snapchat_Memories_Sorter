import os
import shutil
from alive_progress import alive_bar
from pathlib import Path

# Function to get month name from month number
def month_name(month_number):
    month_dict = {
        "01": "1 - January",
        "02": "2 - February",
        "03": "3 - March",
        "04": "4 - April",
        "05": "5 - May",
        "06": "6 - June",
        "07": "7 - July",
        "08": "8 - August",
        "09": "9 - September",
        "10": "10 - October",
        "11": "11 - November",
        "12": "12 - December"
    }
    return month_dict.get(month_number, "Unknown")

# Function to count number of files in memories directory
def number_of_memories(source_dir):
    source = Path(source_dir)
    count = sum(1 for item in source.iterdir() if item.is_file())
    return count

# Function to sort memories into year/month folders
def sort_memories(source_dir, dest_dir):

    num = number_of_memories(source_dir)
    num_processed = 0
    err = 0

    source = Path(source_dir)
    dest = Path(dest_dir)

    # Initialize progress bar
    with alive_bar(num) as bar:

        for item in source.iterdir():

            num_processed += 1

            # Extract date components from filename, full_date_of_item and day_of_item are not used currently, but kept for potential future use
            full_date_of_item = item.name[0:10]
            year_of_item = item.name[0:4]
            month_of_item = item.name[5:7]
            day_of_item = item.name[8:10]

            # Get month name
            month = month_name(month_of_item)

            # Create year and month directories
            if not os.path.exists(dest / year_of_item):
                os.makedirs(dest / year_of_item)
                #print(f"Created directory: {dest / year_of_item}")

            if not os.path.exists(dest / year_of_item / month):
                os.makedirs(dest / year_of_item / month)
                #print(f"Created directory: {dest / year_of_item / month}")

            # Copy picture to the sorted directory
            try:
                shutil.copy(source / item.name, dest / year_of_item / month / item.name)
                #print("Sorting picture number", num)
            except Exception as e:
                #print(f"Error moving file {item.name}: {e}")
                err += 1
                continue
    
            # Update progress bar
            bar()

    print(num_processed, "Snapchat memories processed")
    print("Number of errors", err)


def main():

    # change directories of source and destination here. 
    source_dir = 'memories'
    dest_dir = 'Sorted_Memories'
    
    # Create directories if they don't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print("Creating destination directory dependencies...")
    
    # Sort memories and handle FileNotFoundError
    try:
        sort_memories(source_dir, dest_dir)
        input("press any key to exit...")
    except FileNotFoundError:
        print("memories folder not found. Please drag memories folder into Snapchat_Memories_Sorter folder and try again.")
        input("press any key to exit...")


if __name__ == "__main__":
    main()

