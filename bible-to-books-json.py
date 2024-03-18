import json
import os

# Load the data from the JSON file
with open('kjv.json', 'r') as f:
    data = json.load(f)

# Create a directory to group verses by book name
dir_path = './first_step'
os.makedirs(dir_path, exist_ok=True)

books = {}
for verse in data['verses']:
    book_name = verse['book_name']
    if book_name not in books:
        books[book_name] = {'verses': []}
    books[book_name]['verses'].append(verse)

print("Executing First Step: Segregate everything for future use")
for book_name, verses in books.items():
    with open(f'{dir_path}/{book_name}.json', 'w') as f:
        json.dump(verses, f)
print("First Step Completed")
print("\n" * 2)

print("Executing Second Step: Make the bible dir")
final_dir_path = './bible'
os.makedirs(final_dir_path, exist_ok=True)

for book_name, verses in books.items():
    book_dir = f'{final_dir_path}/{book_name}'
    os.makedirs(book_dir, exist_ok=True)
    for info in verses['verses']:
        chapter_dir = f'{book_dir}/Chapter_{info["chapter"]}'
        os.makedirs(chapter_dir, exist_ok=True)
        verse_file = f'{chapter_dir}/Verse_{info["verse"]}.txt'
        with open(verse_file, 'w') as f:
            f.write(info['text'])

print("Second Step Completed")