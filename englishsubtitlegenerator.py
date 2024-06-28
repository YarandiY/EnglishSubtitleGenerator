import re

def parse_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    blocks = content.split('\n\n')
    subtitles = []
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            index = lines[0]
            times = lines[1]
            text = ' '.join(lines[2:])
            subtitles.append((index, times, text))
    return subtitles

def parse_translations(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    translations = [line.strip() for line in lines if line.strip()]
    return translations

def create_mapping(subtitles):
    mapping = {}
    current_sentence = ""
    current_indices = []
    sentence_counter = 0
    for i, (index, times, text) in enumerate(subtitles):
        current_sentence += text + " "
        current_indices.append(i)
        if text.endswith('.') or text.endswith('!') or text.endswith('?'):
            mapping[sentence_counter] = current_indices
            current_sentence = ""
            current_indices = []
            sentence_counter += 1
    if current_indices:
        mapping[sentence_counter] = current_indices
    return mapping

def distribute_translation(subtitles, translations, mapping):
    eng_subtitles = [""] * len(subtitles)
    for i, translation in enumerate(translations):
        if i in mapping:
            indices = mapping[i]
            words = translation.split()
            num_blocks = len(indices)
            words_per_block = len(words) // num_blocks
            for j, idx in enumerate(indices):
                start = j * words_per_block
                end = (j + 1) * words_per_block if j < num_blocks - 1 else len(words)
                eng_subtitles[idx] = ' '.join(words[start:end])
    return [(subtitles[i][0], subtitles[i][1], eng_subtitles[i]) for i in range(len(subtitles))]

def create_srt(subtitles, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        for index, times, text in subtitles:
            file.write(f"{index}\n{times}\n{text}\n\n")

# Paths to the input files
persian_srt_path = 'subtitles.srt'
translations_txt_path = 'en-sentences.txt'
output_srt_path = 'english_subtitles.srt'

# Parse the input files
persian_subtitles = parse_srt(persian_srt_path)
english_translations = parse_translations(translations_txt_path)

# Create mapping from sentences to subtitle blocks
sentence_to_blocks_mapping = create_mapping(persian_subtitles)

# Distribute the translations across the subtitle blocks
english_subtitles = distribute_translation(persian_subtitles, english_translations, sentence_to_blocks_mapping)

# Create the new SRT file with English subtitles
create_srt(english_subtitles, output_srt_path)