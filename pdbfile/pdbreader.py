 #!/usr/bin/python
# coding: utf-8

# Copyright (c) 2016 Mountainstorm
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import unicode_literals, print_function


class PdbReader(object):
    '''An object that can map offsets in an IL stream to source locations and block scopes.'''

    def __init__(self, pdb_stream=None, filename=None):
        '''Allocates an object that can map some kinds of ILocation objects to IPrimarySourceLocation objects. 
        For example, a PDB reader that maps offsets in an IL stream to source locations.'''
        self.sources = None
        '''A collection of all sources in this pdb; PdbSource'''
        self._pdb_function_map = {} # uint -> PdbFunction
        self.version = 0
        '''The version of this PDB; int'''
        self._sig = None
        self.signature = 0
        '''The Guid signature of this pdb.  Should be compared to the corresponding pdb signature in the matching PEFile; guid'''
        self.age = 0
        '''The age of this pdb.  Should be compared to the corresponding pdb age in the matching PEFile; int'''
        if pdb_stream is None:
            with open(filename, 'rb') as fs:
                self.init(fs)
        else:
            self.init(pdb_stream)

    def init(self, pdb_stream):
        (functions,
         self.version,
         self._sig,
         self.age,
         self.signature,
         self.sources) = PdbFile.load_functions(pdb_stream, True)
        for pdb_function in functions:
            self._pdb_function_map[pdb_function.token] = pdb_function

    @property
    def functions(self):
        '''A collection of all functions in this pdb; PdbFunction; list'''
        return self._pdb_function_map.values()

    @classmethod
    def get_pdb_properties(cls, pdb_file):
        '''Gets the properties of a given pdb.  Throws IOException on error'''
        BitAccess bits = BitAccess(512 * 1024)
        with open(pdb_file) as pdb_stream:
            PdbFileHeader header = PdbFileHeader(pdbStream, bits)
            PdbStreamHelper reader = PdbStreamHelper(pdbStream, header.page_size)
            MsfDirectory directory = MsfDirectory(reader, header, bits)

            directory.streams[1].read(reader, bits)

            ver = bits.read_int32()   #  0..3  Version
            sig = bits.read_int32()   #  4..7  Signature
            age = bits.read_int32()   #  8..11 Age
            guid = bits.ReadGuid();   # 12..27 GUID
        return signature, age, sig

    def get_function_From_token(method_token):
        '''Retreives a PdbFunction by its metadata token'''
        return _pdb_function_map.try_get_value(method_token)
