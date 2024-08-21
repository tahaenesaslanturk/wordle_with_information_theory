import unicodedata

input_file = 'turkce_kelime_listesi.txt'
output_file = 'fiveletter.txt'

five_letter_words = []

with open(input_file, 'r', encoding='utf-8') as infile:
    all_words = infile.readlines()
    for word in all_words:
        word = unicodedata.normalize('NFKC', word)  # Normalize the word
        word = word.strip().replace("I", "ı").replace(" ", "")  # Strip both whitespace and newline characters
        if len(word) == 5:  # Check if the word is exactly 5 characters long
            five_letter_words.append(word.lower().replace("i̇", "i"))

unique = []

for item in five_letter_words:
    if item not in unique:
        unique.append(item)
        if len(item) != 5:
            print(item, len(item))

with open(output_file, 'w', encoding='utf-8') as outfile:
    outfile.writelines(f"{word}\n" for word in unique)  # Write each word on a new line