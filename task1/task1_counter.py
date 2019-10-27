def SymbolCounter(files):
    let_count = dict()
    all_letters = 0
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            dict_gen = (let_count.update({let: let_count.get(let, 0) + 1}) for line in f.readlines() for let in line.lower() if let.isalpha())
            list(dict_gen)

    all_letters = sum(n for n in let_count.values())
    let_count = {let: let_count[let] / all_letters for let in let_count}
    sorted_freq = sorted(let_count.items(), key=lambda key_value: key_value[1], reverse=True)
    return sorted_freq

# files_list = ['voyna-i-mir-tom-1.txt', 'voyna-i-mir-tom-2.txt', 'voyna-i-mir-tom-3.txt', 'voyna-i-mir-tom-4.txt']
# print(SymbolCounter(files_list))