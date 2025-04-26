import os
import csv
from pathlib import Path

french_dictionary_path: str = "random_scripts/dictionary_extractor/french/output"
spanish_dictionary_path: str = "random_scripts/dictionary_extractor/spanish/output"

dictionary_path: str = spanish_dictionary_path

file_type: str = '.csv'

neutral_list: list = []
feminine_list: list = []
masculine_list: list = []


for filename in os.listdir(path=dictionary_path):
  if filename.endswith(file_type):
    with open(f"{dictionary_path}/{filename}", newline='') as csvfile:
      lines = csv.reader(csvfile, delimiter=',', quotechar='"')
      for line in lines:
        word: str = line[0] #left-most cell in the line of comma separated file
        if line[-1] != '': # it is tags

          tag_str: str = line[-1][1:-1] # the tags without '[' and ']'
          tag_list: list = tag_str.split(",") # converting str tags to a list
          for i in range(len(tag_list)):
            # cleaning each tag: remove single quotes and superfluous spaces
            tag_list[i] = tag_list[i].replace("'", "").strip()
          # placing each word into the appropriate list 
          if 'feminine' in tag_list and 'masculine' in tag_list:
            neutral_list.append(word)
          elif 'feminine' in tag_list:
            feminine_list.append(word)
          elif 'masculine' in tag_list:
            masculine_list.append(word)


def write_list_to_file(name: str, list_of_words: list) -> None:
  # writing each list into a .txt file
  with open(name, 'w') as f:
    for word in list_of_words:
      f.write(f"{word}\n")


path: str = "random_scripts/dictionary_extractor/masculine_feminine_words"
# creating a folder named result
Path(path).mkdir(parents=True, exist_ok=True)

folder_name: str = ""
if dictionary_path == french_dictionary_path:
    folder_name = "french"
elif dictionary_path == spanish_dictionary_path:
    folder_name = "spanish"

Path(path + "/" + folder_name).mkdir(parents=True, exist_ok=True)



# writing each list into a .txt file
write_list_to_file(f'{path}/{folder_name}/neutral.txt', neutral_list)
write_list_to_file(f'{path}/{folder_name}/feminine.txt', feminine_list)
write_list_to_file(f'{path}/{folder_name}/masculine.txt', masculine_list)


# # Printing the actual lists on screen
# print("\n".join(neutral_list))
# print("\n==============\n")
# print("\n".join(feminine_list))
# print("\n==============\n")
# print("\n".join(masculine_list))

print("Neutral list count:", len(neutral_list))
print("Feminine list count:", len(feminine_list))
print("Masculine list count:", len(masculine_list))

