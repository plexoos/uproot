#!/usr/bin/env python

# Copyright (c) 2017, DIANA-HEP
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import numpy
import struct

class Cursor(object):
    
    def __init__(self, index):
        self.index = index
    
    def skip(self, numbytes):
        self.index += numbytes
        
    def write_fields(self, sink, packer, *args):
        toadd = numpy.frombuffer(struct.pack(packer, *args), dtype=numpy.uint8)
        sink.write(toadd, self.index)
        self.index += len(toadd)
        
    def write_strings(self, sink, toput):
        toadd1 = numpy.frombuffer(struct.pack(">B", len(toput)), dtype=numpy.uint8)
        toadd2 = numpy.frombuffer(toput, dtype=numpy.uint8)
        toadd = numpy.concatenate([toadd1, toadd2])
        sink.write(toadd, self.index)
        self.index += len(toadd)
    
    def write_cstring(self, sink, toput):
        toadd = numpy.frombuffer(toput, dtype=numpy.uint8)
        sink.write(toadd, self.index)
        self.index += len(toadd)
    
    def write_array(self, sink, packer, array):
        buffer = bytearray()
        packer = packer
        for x in array:
            buffer = buffer + struct.pack(packer, x)
        toadd = numpy.frombuffer(buffer, dtype=numpy.uint8)
        sink.write(toadd, self.index)
        self.index += len(toadd)
    
    def write_empty_array(self, sink):
        data = bytearray()
        toadd = numpy.frombuffer(data, dtype=numpy.uint8)
        sink.write(toadd, self.index)
        self.index += len(toadd)
        
    def update_fields(self, sink, packer, *args):
        toadd = numpy.frombuffer(struct.pack(packer, *args), dtype=numpy.uint8)
        sink.write(toadd, self.index)
        
    def update_strings(self, sink, toput):
        toadd1 = numpy.frombuffer(struct.pack(">B", len(toput)), dtype=numpy.uint8)
        toadd2 = numpy.frombuffer(toput, dtype=numpy.uint8)
        toadd = numpy.concatenate([toadd1, toadd2])
        sink.write(toadd, self.index)
    
    def update_cstring(self, sink, toput):
        toadd = numpy.frombuffer(toput, dtype=numpy.uint8)
        sink.write(toadd, self.index)
    
    def update_array(self, sink, packer, array):
        buffer = bytearray()
        packer = packer
        for x in array:
            buffer = buffer + struct.pack(packer, x)
        toadd = numpy.frombuffer(buffer, dtype=numpy.uint8)
        sink.write(toadd, self.index)
    
    def update_empty_array(self, sink):
        data = bytearray()
        toadd = numpy.frombuffer(data, dtype=numpy.uint8)
        sink.write(toadd, self.index)