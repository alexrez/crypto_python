import argparse
import ciphermodes as cm

parser = argparse.ArgumentParser(prog='cesarcipher', usage='%(prog)s mode [options] [param]',
                                 description='Cesar cipher.')

subparsers = parser.add_subparsers(title='mode', description='valid modes', help='additional help')

parser_genkey = subparsers.add_parser('genkey', help='generating key')
parser_genkey.add_argument('-o', '--out', '--out-file', dest='out', default='sec.key',
                           type=str, help='result file with key (default: "sec.key")')
parser_genkey.set_defaults(func=cm.genkey)

parser_enc = subparsers.add_parser('enc', help='encryption')
parser_enc.add_argument('-k', '--key', dest='key', default='sec.key',
                        type=str, help='key-file (default: "sec.key")')
parser_enc.add_argument('inputfile', type=str, help='input file to encode')
parser_enc.add_argument('--out-file', dest='out', type=str,
                        help='encoded file (default: input.file+.enc)')
parser_enc.set_defaults(func=cm.enc)

parser_dec = subparsers.add_parser('dec', help='decryption')
parser_dec.add_argument('-k', '--key', dest='key', default='sec.key', type=str,
                        help='key-file (default: "sec.key")')
parser_dec.add_argument('inputfile', type=str, help='input file to decode')
parser_dec.add_argument('--out-file', dest='out', type=str,
                        help='decoded file (default: input.file or input.file.dec)')
parser_dec.set_defaults(func=cm.dec)

parser_broke = subparsers.add_parser('broke', help='cracking')
parser_broke.add_argument('model', type=str, help='frequency model file')
parser_broke.add_argument('inputfile', type=str, help='file to crack')
parser_broke.add_argument('--out-file', dest='out', type=str, default='broke_sec.key',
                          help='result file with possible variants of keys (default: broke_sec.key)')
parser_broke.set_defaults(func=cm.broke)

parser_makemodel = subparsers.add_parser('makemodel', help='make model')
parser_makemodel.add_argument('files', nargs='+', type=str, help='input for frequency analysis calculation')
parser_makemodel.add_argument('--out-file', dest='out', type=str, default='model.file',
                              help='frequency model file (default: model.file)')
parser_makemodel.set_defaults(func=cm.makemodel)

def run(parser_):
    args = parser_.parse_args()
    # print(args)
    args.func(args)

if __name__ == '__main__':
    run(parser)
