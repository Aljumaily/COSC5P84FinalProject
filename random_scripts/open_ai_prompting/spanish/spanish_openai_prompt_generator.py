from openai import OpenAI
from datetime import datetime

my_api_key: str = "INSERT THE API KEY"
input_file_path: str = "random_scripts/open_ai_prompting/spanish/male.txt"
output_file_path: str = f'random_scripts/open_ai_prompting/spanish/female{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'

client: OpenAI = OpenAI(api_key=my_api_key)


def spanish_prompt_generator(word: str):
    prompt: str = f"""
    Task: Find the corresponding feminine version of the masculine word

    Limit responses to **ONLY** the word/answer. Also, masculine singular words are translated to the equivalent feminine singular word. 
    Also, masculine plural words are translated to the equivalent feminine plural word. 
    In case there is no match, then write ZZZZZ as the word.

    Language: Spanish/Español
    Word: hombre
    Answer: mujer

    Language: Spanish/Español
    Word: rey
    Answer: reina

    Language: Spanish/Español
    Word: el 
    Answer: ella
    
    Language: Spanish/Español
    Word: actor
    Answer: actriz

    Language: Spanish/Español
    Word: maestro
    Answer: maestra

    Language: Spanish/Español
    Word: {word}
    Answer:
    """
    return prompt

def get_translated_word(original_word: str) -> str:
    response = client.responses.create(
        model="gpt-4.1",
        input=spanish_prompt_generator(original_word)
    )
    return response.output[0].content[0].text

input_file = open(input_file_path, 'r')
output_file = open(output_file_path, 'w')

words: list = input_file.readlines()

for i, word in enumerate(words):
    # print(word)
    # output_file.write(word)
    translated_word: str = get_translated_word(word)
    output_file.write(translated_word + '\n')
    if i % 100 == 0:
        print(i, "out of", len(words))
    
input_file.close()
output_file.close()

# started 2:30pm
