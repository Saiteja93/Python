PLACEHOLDER = "name"

with open ("./practice/letter/names.txt") as n:
    names = n.readlines()
   

with open ("./practice/letter/draft_letter.txt") as l:
    letter_content = l.read()

    for name in names:
        stripped_name = name.strip()
        new_letter = letter_content.replace(PLACEHOLDER, stripped_name)
        with open(f"./practice/letter/ready_to_send/letter_for_{stripped_name}.docx" , mode="w") as completed_letter:
            completed_letter.write(new_letter)

    
