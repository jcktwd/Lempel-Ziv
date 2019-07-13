import argparse
import os
from compress import compress_lz77, decode_lz77, compress_lzss, decode_lzss
from bits import bits
from itertools import product
from multiprocessing import Pool
from datetime import datetime

def cmd_compress(args):
    assert os.path.isfile(args.input), "Input wasn't a file"
    assert args.symbolSize > 0, "Positive symbol size required"
    assert args.windowSize > 0, "Positive window size required"
    output = args.output if args.output is not None else "{}.lz77".format(args.input)

    directory = os.path.dirname(output)
    if not os.path.exists(directory):
        print("Creating output directory...")
        os.makedirs(directory)

    data = bits()
    with open(args.input, "rb") as file:
        data.fromfile(file)

    if args.lzss:
        encoding = compress_lzss(data, args.symbolSize, args.windowSize, args.maxSearch)
    else:
        encoding = compress_lz77(data, args.symbolSize, args.windowSize, args.maxSearch)

    with open(output, "wb+") as file:
        encoding.tofile(file)

def cmd_test(args):
    pool = Pool(os.cpu_count())
    assert os.path.exists(args.directory), "Directory given does not exist"
    files = os.listdir(args.directory)
    assert len(files) > 0, "Directory doesn't contain any files to compress"
    results = [["Filename", "Filesize (bits)", "Symbol Size", "Window Size", "Search Size", "Compressed Size (bits)", "Compression Time", "Decompression Time"]]
    a = ((b, c, d, e, f, g) for b,c,d,e,f,g in product([args.directory], files, ((2**i)-1 for i in range(1, 14)), (2**i for i in range(2, 7)), ((2**i)-1 for i in range(1, 11)), [True]))
    #a = ((b, c, d, e, f, g) for b,c,d,e,f,g in product([args.directory], files, [1023], [8], [1023], [True]))
    results += pool.starmap(test_file, a)
    with open("./testResults.csv", "w+") as file:
        file.write("\n".join((",".join(str(val) for val in row)) for row in results))
    print("Tests done!")

def test_file(directory, filename, window, symbol, search, _verbose=False):
    data = bits()
    with open(os.path.join(directory, filename), "rb") as file:
        data.fromfile(file)

    if _verbose:
        print("[{} W:{} S:{} L:{}] Starting compression at {}".format(filename,window,symbol,search, datetime.now()))

    comp_start = datetime.now()
    compressed = compress_lz77(data, symbol, window, search)
    comp_end = datetime.now()
    if _verbose:
        print("[{} w{} s{} l{}] Data compressed, took {}, A compression ratio of {}".format(
            filename,window,symbol,search, comp_end - comp_start, len(data)/len(compressed)))
    dec_start=datetime.now()
    decompressed = decode_lz77(compressed)
    dec_end = datetime.now()

    if _verbose:
        print("[{} w{} s{} l{}] Data decompressed, took {}".format(
            filename, window, symbol, search, dec_end - dec_start))
    return filename, len(data), symbol, window, search, len(compressed), (comp_end - comp_start).total_seconds(), (dec_end - dec_start).total_seconds()

def cmd_decompress(args):
    assert os.path.isfile(args.input), "Input wasn't a file"
    output = args.output if args.output is not None else args.input.replace(".lz77", "")

    directory = os.path.dirname(output)
    if not os.path.exists(directory):
        print("Creating output directory...")
        os.makedirs(directory)

    encoding = bits()
    with open(args.input, "rb") as file:
        encoding.fromfile(file)

    if args.lzss:
        data = decode_lzss(encoding)
    else:
        data = decode_lz77(encoding)

    with open(output, "wb+") as file:
        data.tofile(file)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Lempel Ziv 77 (LZ77) Compression Utilities")
    subs = parser.add_subparsers(title="Commands")

    # compression command
    compressParser = subs.add_parser("compress", description="Compress a file using LZ77")
    compressParser.add_argument("-input", required=True, action="store", type=str,
                                help="File address of file to encode")
    compressParser.add_argument("-output", action="store", type=str,
                                help="Specify file to output to, the default behaviour is the input filename with the"
                                     " .lz77 extension")
    compressParser.add_argument("-windowSize", action="store", type=int, default=256,
                                help="Size of the sliding window in number of symbols")
    compressParser.add_argument("-symbolSize", action="store", type=int, default=8,
                                help="The number of bits to be considered a symbol")
    compressParser.add_argument("-maxSearch", action="store", type=int, default=256,
                                help="The maximum number of symbols to be searched for in the window. Smaller than or"
                                     " equal to windowSize")
    compressParser.add_argument("-lzss", action="store_true", help="Use LZSS encoding")
    compressParser.set_defaults(func=cmd_compress)

    # decompression command
    decompressParser = subs.add_parser("decompress", description="Recover a file compressed using this utility")
    decompressParser.add_argument("-input", required=True, action="store", type=str,
                                  help="The input file encoded using this utility.")
    decompressParser.add_argument("-output", action="store", type=str,
                                  help="The file to save to.")
    decompressParser.add_argument("-lzss", action="store_true", help="Use LZSS decoding")
    decompressParser.set_defaults(func=cmd_decompress)

    # test command
    testParser = subs.add_parser("test", description="Run benchmark encoding on a test suite")
    testParser.add_argument("directory", action="store", type=str, help="The directory path containing the test files")
    testParser.add_argument("-verbose", action="store_true", help="Flag for displaying detailed testing progress.")
    testParser.set_defaults(func=cmd_test)

    args = parser.parse_args()
    print(args)
    args.func(args)
