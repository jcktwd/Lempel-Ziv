from bitarray import bitarray
from typing import Sequence

class bits(bitarray):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def fromint(self: 'bits', n_bits: int, val: int):
        """Converts an integer into binary of n bits and appends it to a bitarray.

        :param integer: The integer to append
        :param bits: The number of bits to append
        :param array: The bitarray to append to
        :raises OverflowError: Happens when the number of bits needed to represent integer is more than bits.
        :returns: Returns the appended array.
        """

        val_bits = val.bit_length()
        # Check for overflow error.
        if val_bits > n_bits: raise OverflowError("Integer {} is too big to store in {} bits. {} bits are needed in total.".format(val, n_bits, val_bits))

        # Put in leading zeroes
        self.extend(False for _ in range(n_bits - val_bits))

        # Append integer bits
        for n in range(val_bits - 1, -1, -1): self.append((val >> n) & True)

        return self

    def fromints(self: 'bits', n_bits: int, vals: Sequence[int]):
        """Appends binary format to a set length of each element of an array of integers to a bitarray.

        :param array: The bitarray to append to
        :param bits:  Number of bits appended per integer
        :param integers: A sequence of integers
        :raises OverflowError: Happens when the number of bits needed to represent integer is more than bits.
        :returns: Returns the appended array
        """
        for val in vals: self.fromint(n_bits, val)

        return self

    def sub(self, index: int, length: int):
        return self[index: index + length]

    def toint(self):
        return sum(bit * (2**i) for i, bit in enumerate(reversed(self)))
