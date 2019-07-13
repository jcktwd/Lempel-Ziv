Algorithms for Lempel-Ziv Compression (LZ77 and LZSS)

## Compression through LZ77
python main.py compress -input [INPUT] -output [OUTPUT] -windowSize [W] -maxSearch [L] -symbolSize [s]

## Decompression of LZ77
python main.py decompress -input [input] -output [OUTPUT]
You may have to exchange python for python3. This program was written and tested for python 3.5 and above

For LZSS add -lzss flag to commands
You can use -h on any command to get help.