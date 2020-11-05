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
# Copyright 2020 - madsgarff@hotmail.com

from collections import OrderedDict
import json 

# Indicates beginning
INT = b'i'
LIST = b'l'
DICT = b'd'

# Seperates length of string from its value
STRING_SEP = b':'

# End of int, list or dict
THE_END = b'e'

# Skip the last Byte
LAST_BYTE = 1

class BDecode:
    """
    Decodes a torrent file and returns the meta data to the calling 
    source as an OrderedDirect.
    """
    def __init__(self, byteData):
        self._index = 0
        self._data = None

        with open(byteData, 'rb') as f:
            self._data = f.read()

    def _decode(self):
        """ 
        Decodes a byte data file and returns it.

        :return a decoded file as an OrderedDict.
        """
        byte = self._getNextByte()

        if (byte is None):
            raise EOFError("Unexpected end of file error - " 
                                    + "malformed torrent.")
        elif (byte is THE_END):
            return None 
        elif (byte in b'0123456789'):
            length = self._getStrLength(byte)
            return self._decodeStr(length)
        elif (byte == INT):
            return self._decodeInt()
        elif (byte == DICT):
            return self._decodeDict()
        elif (byte == LIST):
            return self._decodeList()
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
        s = str(self._data[self._index: self._index + int(length)], 'utf-8')
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
        while(self._data[self._index: self._index + 1] != THE_END):
            l.append(self._decode())
        return l

    def _decodeDict(self) -> dict:
        """
        Returns and ordered dict and all its descendents from the 
        bencoded file.

        :return dict with all descendents
        """
        d = OrderedDict()
        while(self._data[self._index: self._index + 1] != THE_END):
            key = self._decode()
            value = self._decode()
            d[key] = value
        return d # returns the final dict 

if __name__ == "__main__":
    decoder = BDecode("test.torrent")
    decodedFile = decoder._decode()
    print(decodedFile)