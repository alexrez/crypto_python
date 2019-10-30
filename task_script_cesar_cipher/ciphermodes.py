import os
import json
import random


def genkey(args):
    keys = list(range(256))
    random.shuffle(keys)
    key_path = os.path.normpath(os.path.expanduser(args.out))
    with open(key_path, 'w') as key_file:
        key_file.write(json.dumps(keys))
    os.chmod(key_path, 0o600)


def cipher_(keys, in_file, out_file):
    with open(in_file, 'rb') as input_file:
        text_gen = (keys[sym] for line in input_file.readlines() for sym in line)

    with open(out_file, 'wb') as out_file:
        out_file.write(bytes(list(text_gen)))
        

def enc(args):
    key_path = os.path.normpath(os.path.expanduser(args.key))
    with open(key_path, 'r') as key_file:
        keys = json.loads(key_file.read())

    if args.out is None: # default: input.file.enc
        args.out = args.inputfile + '.enc'
    in_path = os.path.normpath(os.path.expanduser(args.inputfile))
    out_path = os.path.normpath(os.path.expanduser(args.out))
    cipher_(keys, in_path, out_path)
    


def dec(args):
    key_path = os.path.normpath(os.path.expanduser(args.key))
    with open(key_path, 'r') as key_file:
        keys = [0] * 256
        for i, k in enumerate(json.loads(key_file.read())):
            keys[k] = i

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

def broke(args):
    model_path = os.path.normpath(os.path.expanduser(args.model))
    with open(model_path, 'r') as model_file:
        freq_model = json.loads(model_file.read())

    freq_encode = frequency([args.inputfile])

    # [модель] - набор чисел (256 float) p_i (вероятность появления байта i) [0, 1]
    # далее считаем частотность символов (байтов) в зашифрованном файле (p'_i ...), сопоставляем (p_0, p_1, ..., p_n) и (p'_0, p'_1, ..., p'_n)
    # (для этого сортируем оба массива) (одинаковые значения - перебором)
    # в этоге получим восстановленный ключ шифрования - это выход

    out_path = os.path.normpath(os.path.expanduser(args.out))
    with open(out_path, 'w') as model_file:
        model_file.write(json.dumps(broke_keys))
    os.chmod(key_path, 0o600)


def makemodel(args):
    sym_count = frequency(args.files)
    out_path = os.path.normpath(os.path.expanduser(args.out))
    with open(out_path, 'w') as model_file:
        model_file.write(json.dumps(sym_count))
