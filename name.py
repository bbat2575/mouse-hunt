'''
Name Checker (Child-Friendly Feature)
'''

# Checks if name is between 1 and 9 characters long (inclusive)
def is_valid_length(name: str) -> bool:
    result = len(name) >= 1 and len(name) <= 9
    return result

# Checks if name starts with a letter
def is_valid_start(name: str) -> bool:
    result = name[0].isalpha()
    return result

# Checks if name is one word (no spaces)
def is_one_word(name: str) -> bool:
    result = name.find(' ') == -1
    return result

# Checks if name is valid using all the other functions
def is_valid_name(name: str) -> bool:
    result = is_valid_length(name) and is_valid_start(name) and is_one_word(name) and not is_profanity(name)
    return result

# Checks for profanities in the name
def is_profanity(word: str, database='/home/files/list.txt', records='/home/files/history.txt') -> bool:
    profanity = False
    if type(word) == str:
        word = word.lower().strip()

    try:
        # Using keywords 'with' and 'as' ensures the file will be closed
        with open(database) as data:
            ls_names = data.readlines()

        i = 0
        total_names = len(ls_names)      
        
        while i < total_names:
            if word == ls_names[i].strip():
                profanity = True
                break
            i += 1
    except FileNotFoundError:
        print("Check directory of database!")

    # If word is a profanity, append it to history.txt if the file exists, otherwise create it
    if profanity:
        try:
            with open(records, 'a') as rec:
                rec.write(word + '\n')
        except FileNotFoundError:
            with open(records, 'w') as rec:
                rec.write(word + '\n')

    return profanity

# Counts the occurences of a word contained in a file
def count_occurrence(word: str, file_records="/home/files/history.txt", start_flag=True) -> int:
    # Check for string type
    if type(word) != str:
        print("First argument must be a string object!")
        return 0
    # Check for empty string
    elif not word.strip():
        print("Must have at least one character in the string!")
        return 0
    else:
        word = word.lower().strip()

    try:
        with open(file_records) as rec:
            ls_names = rec.readlines()
        
        count = 0
        i = 0
        total_names = len(ls_names)

        # if start_flag = True -> check for same first alphabetical character as word
        if start_flag:
            while i < total_names:
                if word[0] == ls_names[i][0].lower().strip():
                    count += 1
                i += 1
            return count
        # else if start_flag = False -> check for same word as word
        else:
            while i < total_names:
                if word == ls_names[i].lower().strip():
                    count += 1
                i += 1
            return count

    except FileNotFoundError:
        print("File records not found!")
        return 0

# Generate a name using a file
def generate_name(word: str, src="/home/files/animals.txt", past="/home/files/names.txt") -> str:
    # Check for string type
    if type(word) != str:
        print("First argument must be a string object!")
        return "Bob"
    # Check for empty string
    elif not word.strip():
        print("Must have at least one character in the string!")
        return "Bob"
    else:
        word = word.lower().strip()

    try:
        with open(src) as source:
            ls_names = source.readlines()
        with open(past) as old:
            old_names = old.readlines()
        
        i = 0
        total_names = len(ls_names)
        total_old_names = len(old_names)
        
        # Create an empty list to store tuples with the following 2 entries: 
        # - Names from animals.txt with same first letter as word
        # - The number of times that name occurs in names.txt
        similar = []
        while i < total_names:
            check = ls_names[i].lower().strip()
            if word[0] == check[0]:
                # If first letter is the same, find how many times the word occurs in names.txt
                occur_count = count_occurrence(check, file_records=past, start_flag=False)
                # Append the name and occurrence count to the list
                similar.append((check, occur_count))
            i += 1

        # Need to find the least occurring word from list similar
        # by comparing the number of times they occur in names.txt
        i = 1
        least_occurring = similar[0][0]
        while i < len(similar):
            if similar[i][1] < similar[i-1][1]:
                least_occurring = similar[i][0]
            i += 1
        
        # Append the name to names.txt if the file exists, otherwise create it
        try:
            with open(past, 'a') as old:
                old.write(least_occurring + '\n')
        except FileNotFoundError:
            with open(past, 'w') as old:
                old.write(least_occurring + '\n')

        return least_occurring

    except FileNotFoundError:
        print("Source file is not found!")
        return "Bob"


def main():
    while True:
        name = input("Check name: ")
        
        # If user inputs "s" program terminates
        if name.lower().strip() == "s":
            break
        # If name is not valid generate a new one
        elif not is_valid_name(name):
            new_name = generate_name(name)
            print(f"Your new name is: {new_name}")
        # Name is valid
        else:
            print(f"{name} is a valid name!")


if __name__ == "__main__":
    main()
