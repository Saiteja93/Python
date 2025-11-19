

PLACEHOLDER = "[Name]"
with open("../Input/Names/names.txt") as file_names:
    names = file_names.readlines()

with open ("../Input/Letters/starting_letter.docx") as letter_file:
    letter_contents = letter_file.read()
    for name in names:
        stripped_name = name.strip()
        new_letter = letter_contents.replace(PLACEHOLDER, stripped_name)
        with open(f"../Output/Ready_to_send/letter_to_{stripped_name}.docx", mode='w') as completed_letter:
            completed_letter.write(new_letter)











