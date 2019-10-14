def SymbolCounter(files):
    letter_counter = dict()
    all_letters = 0
    for file in files:
        f = open(file, 'r', encoding='utf-8')

        for line in f.readlines():
            all_letters += len(line) - 1
            for letter in line.lower():
                if(letter.isalpha()):
                    letter_counter[letter] = letter_counter.setdefault(letter, 0) + 1

    letter_freq = {letter: letter_counter[letter] / all_letters for letter in letter_counter}
    sorted_freq = sorted(letter_freq.items(), key=lambda key_value: key_value[1], reverse=True)
    return sorted_freq

# files_list = ['voyna-i-mir-tom-1.txt', 'voyna-i-mir-tom-2.txt', 'voyna-i-mir-tom-3.txt', 'voyna-i-mir-tom-4.txt']
# print(SymbolCounter(files_list))