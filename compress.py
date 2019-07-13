from bits import bits
from itertools import groupby
from typing import Sequence

def compress_lz77(data: bits, symbol: int, window: int, max_length: int):
    enc, enc_pos = bits().fromints(8, (symbol, window.bit_length(), max_length.bit_length())), 0
    data.extend(False for i in range((symbol - (len(data) % symbol))))
    while enc_pos * symbol < len(data):
        buffer_start, buffer_end, buffer_size = max(0, enc_pos - window), enc_pos, min(enc_pos, window)
        buffer = list(data.sub(i * symbol, symbol) for i in range(buffer_start, buffer_end))
        distance, length, nextSymbol = 0, 0, data.sub(enc_pos * symbol, symbol)
        matches = [buffer_size - i for i, s in enumerate(buffer) if s == nextSymbol]
        # print(buffer, matches)
        while len(matches) > 0 and length < max_length:
            distance = matches[-1]
            length += 1
            nextSymbol = data.sub((enc_pos + length) * symbol, symbol)
            matches = list(filter(lambda match: match - length > 0 and buffer[-match + length] == nextSymbol , matches))
        enc_pos += length + 1
        # print(nextSymbol)
        enc.fromint(window.bit_length(), distance).fromint(max_length.bit_length(), length)
        enc.extend(nextSymbol)
    return enc

def decode_lz77(data: bits):
    symbol_bits, distance_bits, length_bits = (data.sub(i, 8).toint() for i in range(0, 17, 8))
    # print(f"symbol_bits={symbol_bits} distance_bits={distance_bits} length_bits={length_bits}")
    bits_per = sum((symbol_bits, distance_bits, length_bits))
    dec = bits()
    dec_pos = 24
    # print(data[24:])
    while dec_pos < len(data):
        distance, dec_pos = data.sub(dec_pos, distance_bits).toint(), dec_pos + distance_bits
        length, dec_pos = data.sub(dec_pos, length_bits).toint(), dec_pos + length_bits
        nextSymbol, dec_pos = data.sub(dec_pos, symbol_bits), dec_pos + symbol_bits
        # print(f"Decoding dist={distance}, length={length}, nextSymbol={nextSymbol}")
        dec.extend(dec.sub(len(dec) - ((distance) * symbol_bits), length * symbol_bits))
        dec.extend(nextSymbol)
    # print(-(len(dec) % 8))
    return dec

def compress_lzss(data: bits, symbol: int, window: int, max_length: int):
    enc, enc_pos = bits().fromints(8, (symbol, window.bit_length(), max_length.bit_length())), 0
    data.extend(False for i in range((symbol - (len(data) % symbol))))
    while enc_pos * symbol < len(data):
        buffer_start, buffer_end, buffer_size = max(0, enc_pos - window), enc_pos, min(enc_pos, window)
        buffer = list(data.sub(i * symbol, symbol) for i in range(buffer_start, buffer_end))
        distance, length, nextSymbol = 0, 0, data.sub(enc_pos * symbol, symbol)
        matches = [buffer_size - i for i, s in enumerate(buffer) if s == nextSymbol]
        # print(buffer, matches)
        while len(matches) > 0 and length < max_length:
            distance = matches[-1]
            length += 1
            nextSymbol = data.sub((enc_pos + length) * symbol, symbol)
            matches = list(filter(lambda match: match - length > 0 and buffer[-match + length] == nextSymbol , matches))
        enc_pos += length + 1
        # print(nextSymbol)
        if distance + length > 0:
            enc.append(True)
            enc.fromint(window.bit_length(), distance).fromint(max_length.bit_length(), length)
        else:
            enc.append(False)
        enc.extend(nextSymbol)
    return enc

def decode_lzss(data: bits):
    symbol_bits, distance_bits, length_bits = (data.sub(i, 8).toint() for i in range(0, 17, 8))
    # print(f"symbol_bits={symbol_bits} distance_bits={distance_bits} length_bits={length_bits}")
    bits_per = sum((symbol_bits, distance_bits, length_bits))
    dec = bits()
    dec_pos = 24
    # print(data[24:])
    while dec_pos < len(data):
        flag, dec_pos = data.sub(dec_pos, 1).toint(), dec_pos + 1
        if flag:
            distance, dec_pos = data.sub(dec_pos, distance_bits).toint(), dec_pos + distance_bits
            length, dec_pos = data.sub(dec_pos, length_bits).toint(), dec_pos + length_bits
            dec.extend(dec.sub(len(dec) - ((distance) * symbol_bits), length * symbol_bits))
        nextSymbol, dec_pos = data.sub(dec_pos, symbol_bits), dec_pos + symbol_bits
        # print(f"Decoding dist={distance}, length={length}, nextSymbol={nextSymbol}")
        dec.extend(nextSymbol)
    # print(-(len(dec) % 8))
    return dec

if __name__=="__main__":
    pass