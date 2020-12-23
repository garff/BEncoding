#
# Class that decodes a bencoded file as an OrderedDict (python object).
#
# Bencoding (pronounced b-encoding) is mostly used as a way to save
# an object, representing the meta-data of a torrent file, as a bencoded
# torrent file. All torrent files follows the structure defined by this
# encoding.
#
# More info about the BitTorrent specification and bencoding (although sparse)
# can be found at: https://www.bittorrent.org/beps/bep_0003.html
#
# Copyright 2020 - mads@garff.dk

from collections import OrderedDict
import struct

# Indicates beginning
INT = b'i'
LIST = b'l'
DICT = b'd'

# Seperates length of string from its value
STRING_SEP = b':'

# End of int, list or dict
THE_END = b'e'

class Bdecode:
    """
    Decodes a torrent file and returns the meta data to the calling 
    source as an OrderedDirect.
    """
    def __init__(self, filename):
        self._index = 0
        self._data = None

        with open(filename, 'rb') as f:
            self._data = f.read()

    def decode(self):
        """ 
        Decodes a byte data file and returns it.

        :return a decoded file as an OrderedDict.
        """
        byte = self._getNextByte()

        if (byte is None):
            raise EOFError("Unexpected end of file error - " 
                                    + "malformed torrent.")
        elif (byte == INT):
            return self._decodeInt()
        elif (byte == LIST):
            return self._decodeList()
        elif (byte == DICT):
            return self._decodeDict()
        elif (byte == THE_END):
            return None 
        elif (byte in b'0123456789'):
            length = self._getStrLength(byte)
            return self._decodeStr(length)
        else:
            raise ValueError("Byte had unexpected format.")

    def _getNextByte(self) -> bytes:
        """
        Returns the next byte from the bencoded file.

        :return byte 
        """
        b = None
        if (self._index + 1 <= len(self._data)):
            b = self._data[self._index: self._index + 1]
            self._index += 1

        return b

    def _getStrLength(self, byte):
        """
        Reads the int value corresponding to the next string length

        :return string length
        """
        l = ""
        while(byte != STRING_SEP):
            l += byte.decode('utf-8')
            byte = self._getNextByte()

        return int(l)

    def _decodeStr(self, length) -> str:
        """
        Returns the next string from the bencoded file.

        :return the string 
        """
        s = self._data[self._index: self._index + int(length)]
        self._index += int(length) 

        return s

    def _decodeInt(self) -> int:
        """
        Returns an integer from the bencoded file.

        :return the int 
        """
        b = self._getNextByte()
        i = ""
        while (b != THE_END):
            i += b.decode('utf-8')
            b = self._getNextByte()

        return int(i)

    def _decodeList(self) -> list:
        """ 
        Returns a list and all its entries from the bencoded file.

        :return list with entries
        """
        l = []
        while(struct.pack("B", self._data[self._index]) != THE_END):
            l.append(self.decode())
        self._getNextByte() # removes THE_END of list 
        return l

    def _decodeDict(self) -> dict:
        """
        Returns and ordered dict and all its descendents from the 
        bencoded file.

        :return dict with all descendents
        """
        d = OrderedDict()
        while(self._data[self._index: self._index + 1] != THE_END):
            key = self.decode()
            value = self.decode()
            d[key] = value
        return d # returns the final dict 
