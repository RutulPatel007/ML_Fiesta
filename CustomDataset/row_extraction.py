def extract_row(input_row_number):
    try:
        # Open output_file.txt and read lines with a more flexible encoding (e.g., 'utf-8' or 'ISO-8859-1')
        with open("output_file_batch2.txt", "r", encoding="utf-8") as output_file:
            lines = output_file.readlines()

        # Check if the row number is within the valid range
        if input_row_number < 1 or input_row_number > len(lines):
            print(f"Invalid row number. Please enter a number between 1 and {len(lines)}.")
            return
        
        # Extract the specific row (1-based indexing)
        row = lines[input_row_number - 1]

        # Write the extracted row to input.txt
        with open("input.txt", "w", encoding="utf-8") as input_file:
            input_file.write(row)
        
        print(f"Row {input_row_number} has been extracted and written to input.txt.")
    
    except FileNotFoundError:
        print("The file output_file.txt does not exist.")
    except UnicodeDecodeError as e:
        print(f"Unicode decode error: {e}. Try using a different encoding.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Input from user for the row number to extract
try:
    row_number = int(input("Enter the row number to extract: "))
    extract_row(row_number)
except ValueError:
    print("Please enter a valid integer for the row number.")
