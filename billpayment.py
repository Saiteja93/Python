# This function helps us get input that is only digits or allows 'quit'.
def get_number_or_quit(prompt_message):
    """
    Asks the user for input using 'prompt_message'.
    Keeps asking until the user enters only digits, or types 'quit'.
    Returns the number (as an integer) or the string 'quit'.
    """
    while True: # This loop keeps going until we get valid input or 'quit'
        user_input = input(prompt_message).strip() # Get input and remove extra spaces

        # Check if the user wants to stop
        if user_input.lower() == 'quit': # .lower() makes 'Quit' or 'QUIT' work too
            return 'quit' # Send back 'quit' to signal cancellation

        # Check if the input is made of only digits (0-9)
        if user_input.isdigit():
            return int(user_input) # If it's digits, convert to a whole number and return
        else:
            print("That's not a valid number. Please enter digits only (e.g., 50, 15).")
            # The loop will then run again, asking for input.

# --- Start of the main program ---
print("Hello! We hope you guys like our food :) Please pay your bill.")

# --- Step 1: Get the total bill amount ---
# We use our helper function to get the bill.
# If 'quit' is returned, we stop the whole program.
bill_amount_raw = get_number_or_quit("Enter your total bill amount (e.g., 100): $")
if bill_amount_raw == 'quit':
    print("Bill calculation cancelled. Goodbye!")
    exit() # This stops the program right here
bill_amount = bill_amount_raw # Now we know it's a number, rename for clarity

# Check if the bill amount is reasonable (e.g., not zero or negative)
if bill_amount <= 0:
    print("Bill amount must be greater than zero. Please restart if you wish to calculate a bill.")
    exit() # Stop if the bill is invalid

print(f"Your actual bill is: ${bill_amount:.2f}") # Display bill with 2 decimal places

# --- Step 2: Get the tip percentage ---
tip_percentage_raw = get_number_or_quit("Enter your tip percentage (e.g., 15 for 15%): ")
if tip_percentage_raw == 'quit':
    print("Bill calculation cancelled. Goodbye!")
    exit() # Stop the program
tip_percentage = tip_percentage_raw # Now it's a number

if tip_percentage != 0:
    print("Thank you so much for the tip!")
else:
    print("Thank you!")

# --- Step 3: Calculate the tip and total bill ---
# Remember, tip_percentage is an integer, so direct calculation is fine.
tip_amount = (bill_amount * tip_percentage) / 100
final_bill_total = bill_amount + tip_amount

print(f"Tip amount: ${tip_amount:.2f}") # Show tip amount
print(f"Your total bill (including tip) is: ${final_bill_total:.2f}")

# --- Step 4: Get how many people are splitting the bill ---
split_people_raw = get_number_or_quit("How many people are splitting the bill? (Enter 1 if not splitting): ")
if split_people_raw == 'quit':
    print("Bill calculation cancelled. Goodbye!")
    exit() # Stop the program
split_people = split_people_raw # Now it's a number

# Make sure people splitting is at least 1
if split_people <= 0:
    print("Number of people must be at least 1. We'll use 1 person for calculation.")
    split_people = 1 # Default to 1 if user enters 0 or less

# --- Step 5: Calculate bill per person and display ---
bill_per_person = final_bill_total / split_people

# Always round currency to 2 decimal places
bill_per_person = round(bill_per_person, 2)

if split_people > 1:
    print(f"Each person's share of the bill is: ${bill_per_person:.2f}")
else:
    print(f"Your final bill is: ${bill_per_person:.2f}")

# --- End message ---
print("We are excited to see you guys again!")

