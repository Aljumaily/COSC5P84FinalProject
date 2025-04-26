path: str = "./random_scripts/word_matcher/french/"
female_file_path: str = path + "female_input.txt"
male_file_path: str = path + "male_input.txt"

female_output_file_path: str = path + "female_output.txt"
male_output_file_path: str = path + "male_output.txt"

male_file = open(male_file_path, 'r')
female_file = open(female_file_path, 'r')

female_output_file = open(female_output_file_path, 'w')
male_output_file = open(male_output_file_path, 'w')


with open(male_file_path) as f:
    male_words: list = f.read().splitlines()

with open(female_file_path) as f:
    female_words: list = f.read().splitlines()

# print(male_words)
# print(female_words)
# print(len(male_words), len(female_words))

female_output_list: list = []
male_output_list: list = []

for i in range(len(female_words)):
    if female_words[i] != "ZZZZZ":
        female_output_list.append(female_words[i])
        male_output_list.append(male_words[i])

for i, female_word in enumerate(female_output_list):
    female_output_file.write(female_word)
    if i != len(female_output_list) - 1:
        female_output_file.write("\n")


for i, male_word in enumerate(male_output_list):

    male_output_file.write(male_word)
    if i != len(male_output_list) - 1:
        male_output_file.write("\n")


female_output_file.close()
male_output_file.close()
