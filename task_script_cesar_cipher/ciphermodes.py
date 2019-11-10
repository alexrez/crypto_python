import os
import json
import random
from itertools import permutations
from itertools import chain


def genkey(args):
    keys = list(range(256))
    random.shuffle(keys)
    key_path = os.path.normpath(os.path.expanduser(args.out))
    with open(key_path, 'w') as key_file:
        key_file.write(json.dumps(keys))
    os.chmod(key_path, 0o600)


def cipher_(keys, in_file, out_file):
    with open(out_file, 'wb') as out_file:
        for key in keys:
            with open(in_file, 'rb') as input_file:
                text_gen = (key[sym] for line in input_file.readlines() for sym in line)

            out_file.write(bytes(list(text_gen)))
        

def enc(args):
    key_path = os.path.normpath(os.path.expanduser(args.key))
    keys = []
    with open(key_path, 'r') as key_file:
        for line in key_file.readlines():
            keys.append(json.loads(line))

    if args.out is None: # default: input.file.enc
        args.out = args.inputfile + '.enc'
    in_path = os.path.normpath(os.path.expanduser(args.inputfile))
    out_path = os.path.normpath(os.path.expanduser(args.out))
    cipher_(keys, in_path, out_path)


def dec(args):
    key_path = os.path.normpath(os.path.expanduser(args.key))
    keys = []
    with open(key_path, 'r') as key_file:
        for line in key_file.readlines():
            cur_keys = [0] * 256
            for i, k in enumerate(json.loads(line)):
                cur_keys[k] = i
            keys.append(cur_keys)

    if args.out is None: # default: если inputfile с '.enc', то удалить это расширение, если без,- то input.file.dec
        ind = args.inputfile.find('.enc')
        if ind != -1:
            args.out = args.inputfile[:ind]
        else:
            args.out = args.inputfile + '.dec'
    in_path = os.path.normpath(os.path.expanduser(args.inputfile))
    out_path = os.path.normpath(os.path.expanduser(args.out))
    cipher_(keys, in_path, out_path)


def frequency(files):
    count = [0] * 256
    for file in files:
        file_path = os.path.normpath(os.path.expanduser(file))
        with open(file_path, 'rb') as f:
            for line in f.readlines():
                for sym in line:
                    count[sym] += 1 
            # sym_gen = (count[sym]++ for line in f.readlines() for sym in line)
            # list(sym_gen)

    all_sym = sum(count)
    if all_sym != 0:
        count = [c / all_sym for c in count]
    return count


def possible_keys(model):
    n = len(model)
    seq = []

    def foo(model, seq):
        if model:
            sym = model[0]
            for perm in permutations(sym):
                seq.append(perm)
                yield from foo(model[1:], seq)
                seq.pop()

        else:
            yield [i for item in seq for i in item]
            
    yield from foo(model, seq)
    

def broke(args):
    model_path = os.path.normpath(os.path.expanduser(args.model))
    with open(model_path, 'r') as model_file:
        freq_model = json.loads(model_file.read())

    freq_encode = frequency([args.inputfile])

    freq_model_dict = dict()
    dict_gen = (freq_model_dict.update({freq: freq_model_dict.get(freq, list())+ [i] }) for i, freq in enumerate(freq_model) if freq != 0)
    list(dict_gen)

    freq_encode_dict = dict()
    dict_gen = (freq_encode_dict.update({freq: freq_encode_dict.get(freq, list())+ [i] }) for i, freq in enumerate(freq_encode) if freq != 0)
    list(dict_gen)

    model_key = [symb[1] for symb in sorted(freq_model_dict.items(), key=lambda freq_symb: freq_symb[0], reverse=True)]
    encode_key = [symb[1] for symb in sorted(freq_encode_dict.items(), key=lambda freq_symb: freq_symb[0], reverse=True)]

    out_path = os.path.normpath(os.path.expanduser(args.out))
    with open(out_path, 'w') as model_file: 
        for m_sym in possible_keys(model_key):
            for e_sym in possible_keys(encode_key):
                broke_keys = [0] * 256
                for m, e in list(zip(m_sym, e_sym)):
                    broke_keys[m] = e
                model_file.write(json.dumps(broke_keys) + os.linesep)


def makemodel(args):
    sym_count = frequency(args.files)
    out_path = os.path.normpath(os.path.expanduser(args.out))
    with open(out_path, 'w') as model_file:
        model_file.write(json.dumps(sym_count))
