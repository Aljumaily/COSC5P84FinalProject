
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import nltk
import regex as re
from tqdm import tqdm
from collections import defaultdict
import random
from models.other_utils import load_file_to_list, get_intervals


def la_le_swapper(i: int, swapped_sent: list):
    # check if there is a 'la' or 'le' before the current token (within the previous four token)
    if i > 4:
        for j in range(1, 5):
            index = i - j
            if swapped_sent[index] == "la":
                swapped_sent[index] = "le"
                return  # Exit after the first swap
            elif swapped_sent[index] == "La":
                swapped_sent[index] = "Le"
                return  # Exit after the first swap
            elif swapped_sent[index] == "le":
                swapped_sent[index] = "la"
                return  # Exit after the first swap
            elif swapped_sent[index] == "Le":
                swapped_sent[index] = "La"
                return  # Exit after the first swap

def remove_extra_spaces_smart(text):
    """Removes multiple spaces but tries to preserve single spaces around digits and periods where appropriate."""
    # Remove space before apostrophe
    text = re.sub(r"\s+(['\u2019])\s+", lambda m: m.group().strip(), text)
    text = re.sub(r"\s+([,.«»])", r"\1 ", text)
    text = re.sub(r'\s{2,}', ' ', text).strip()
    return text


def main():
    random.seed(1)

    pat = re.compile(r"""(?:l'|qu'|d'|j'|t'|s')\w+| # Handle common French contractions at the beginning of words
                                \w+(?:-\w+)*|       # Match words with optional internal hyphens
                                \p{L}+|             # Match Unicode letters (including accented ones)
                                \p{N}+|             # Match Unicode numbers
                                [\p{S}\p{P}]+|      # Match one or more Unicode symbols or punctuation marks
                                \s+                 # Match whitespace
                                """, re.VERBOSE)

    langauge: str = 'fr'
    input_path = f'data/{langauge}/data.txt'
    output_path = f'data/{langauge}/gender_swapped_data.txt'
    
    male_words = load_file_to_list(f'data/{langauge}/male.txt')
    female_words = load_file_to_list(f'data/{langauge}/female.txt')

    assert len(male_words) == len(female_words)
    male2female, female2male = defaultdict(list), defaultdict(list)
    for male_word, female_word in zip(male_words, female_words):
        
        male2female[male_word].append(female_word)
        female2male[female_word].append(male_word)

    sents = load_file_to_list(input_path)


    # by frequency
    count = {}
    all_tokens = [tok.strip().lower() for sent in sents for tok in re.findall(pat, sent)]
    for attribute in list(set(male_words + female_words)):
        count[attribute] = all_tokens.count(attribute) + 1 # smoothing
    male_weights = {}
    for male_word in male_words:
        female_words_list = male2female[male_word]
        weights = [count[i] for i in female_words_list]
        add =  sum(weights)
        weights = [count/add for count in weights]
        male_weights[male_word] = weights
    
    female_weights = {}
    for female_word in female_words:
        male_words_list = female2male[female_word]
        weights = [count[i] for i in male_words_list]
        add =  sum(weights)
        weights = [count/add for count in weights]
        female_weights[female_word] = weights
    

    # print(count)

    gender_swapped_sents = []
    for sent in tqdm(sents):
        toks = [tok.strip() for tok in re.findall(pat, sent)]
        # this is to make sure the transformed text has the same tokenization as original text
        intervals = get_intervals(sent, toks)
        swapped_sent = []
        for i, tok in enumerate(toks):
            
                # print(toks[i-3], toks[i-2], toks[i-1], toks[i])
            if tok.lower() in male_words:
                swapped_list = male2female[tok.lower()]
                
                swapped = random.choices(swapped_list, weights=male_weights[tok.lower()], k=1)[0]

                if tok[0] != tok.lower()[0]:
                    swapped = swapped.capitalize()
                
                swapped_sent.append(swapped)
                la_le_swapper(i, swapped_sent)
            elif tok.lower() in female_words:
                swapped_list = female2male[tok.lower()]

                swapped = random.choices(swapped_list, weights=female_weights[tok.lower()], k=1)[0]
                if len(tok) > 0 and tok[0] != tok.lower()[0]: # MAYSARA ADDED 'len(tok) > 0 and' 
                    swapped = swapped.capitalize()
                swapped_sent.append(swapped)
                la_le_swapper(i, swapped_sent)
            else:
                swapped_sent.append(tok)
                la_le_swapper(i, swapped_sent)
        assert len(toks) == len(swapped_sent)

        # add white spaces
        new_sent = ''
        for i in range(len(toks)):
            if intervals[i] == 0:# MAYSARA ADDED 
                new_sent = new_sent + ' ' + swapped_sent[i] # MAYSARA ADDED 
            else:# MAYSARA ADDED 
                new_sent = new_sent + ' ' * intervals[i] + swapped_sent[i]
        gender_swapped_sents.append(new_sent)
        # gender_swapped_sents.append(' '.join(swapped_sent))

    #TODO: add name swapping
    
    with open(output_path, 'w') as f:
        for sent in gender_swapped_sents:
            f.write(remove_extra_spaces_smart(sent))# MAYSARA ADDED 
            f.write('\n')

if __name__ == '__main__':
    main()