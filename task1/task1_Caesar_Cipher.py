# реализуем шифр Цезаря
# для каждой буквы подсчитываем число ее вхождений (для ВСЕХ 26 букв алфавита)
def CaesarCipherEncoder(text, key):
    global alphabet
    return ''.join(alphabet[(ord(letter) - ord('a') + key) % len(alphabet)] for letter in text)

def CaesarCipherDecoder(text, key):
    global alphabet
    return ''.join(alphabet[(ord(letter) - ord('a') - key) % len(alphabet)] for letter in text)

def counter(text):
    cs_counter = dict()
    for letter in text:
        cs_counter[letter] = cs_counter.setdefault(letter, 0) + 1
    return cs_counter

alphabet = [chr(ord('a') + i) for i in range(26)]

s = input('Enter string to be encrypted:\n').lower()
key = int(input('Enter key:\n'))

cs = CaesarCipherEncoder(s, key)
print('Caesar cipher encoded string => {}'.format(cs))

letter_count = counter(cs)
print('Letter counter:\n{}'.format(letter_count))

plain_text = CaesarCipherDecoder(cs, key)
print('Caesar cipher decoded string => {}'.format(plain_text))