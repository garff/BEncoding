#
# Class that bencodes a python object.
#
# Bencoding (pronounced b-encoding) is mostly used as a way to save
# an object, representing the meta-data of a torrent file.
# 
# All torrent files follows the structure defined by this
# encoding.
#
# More info about the BitTorrent specification and bencoding (although sparse)
# can be found at: https://www.bittorrent.org/beps/bep_0003.html
#
# Copyright 2020 - madsgarff@hotmail.com

from BDecode import BDecode  
from collections import OrderedDict

# Indicates beginning
INT = 'i'
LIST = 'l'
DICT = 'd'

# Seperates length of string from its value
STRING_SEP = ':'

# End of int, list or dict
THE_END = 'e'

class BEncode:
    """
    Encodes a python object and returns it as a bencoded file torrent
    file.
    """
    def __init__(self, data):
        self._data = data
        
    def _intiation(self) -> bytes:
        """
        Initiates the encoding.

        :return bencoded object
        """
        return self._encode(self._data).encode()

    def _encode(self, data) -> bytes:
        """
        Encodes a python object and returns it

        :return torrent file
        """
        if (type(data) == str):
            return self._encodeStr(data)
        elif (type(data) == int):
            return self._encodeInt(data)
        elif (type(data) == dict or type(data) == OrderedDict):
            return self._encodeDict(data)
        elif (type(data) == list):
            return self._encodeList(data)
        elif data == THE_END:
            return THE_END
        else:
            raise ValueError("Python object had an unexpected format.")
            return None 

    def _encodeStr(self, data) -> str :
        """ 
        Encodes given string and calls the next part of the data 
        recursively.
        
        :return encoded string 
        """ 
        return (str(len(data)) + STRING_SEP + str(data))

    def _encodeInt(self, data) -> str:
        """
        Encodes given int and calls the next part of the data
        recursively.

        :return encoded int
        """
        return (INT + str(data) + THE_END)

    def _encodeDict(self, data) -> dict:
        """
        Encodes given dict and calls the dict recursively to 
        encode the data the dict holds.

        :return encoded dict
        """
        res = ""
        for k,v in data.items():
            res += DICT
            res += self._encodeStr(k)     # key is always string
            res += self._encode(v)   
            res += THE_END
        return res 

    def _encodeList(self, data) -> list:
        """
        Encodes given list and its members.
        
        :return encoded list and members
        """
        res = ""
        res += LIST

        for v in data:
            res += self._encode(v)
        return res

if __name__ == "__main__":
    decoder = BDecode("test.torrent")
    decodedFile = decoder._decode()
    encoder = BEncode(decodedFile)
    print(encoder._intiation())