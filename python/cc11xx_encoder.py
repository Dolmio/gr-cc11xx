#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr
import pmt
import cc11xx_packet
class cc11xx_encoder(gr.basic_block):
    def __init__(self, preamble=[0x20, 0x20, 0x20, 0x20, 0x20, 0x20], syncword=[0x35, 0x2E, 0x35, 0x2E], crc=True, whitening=True):
        gr.basic_block.__init__(self,
            name="cc11xx-encoder",
            in_sig=[],
            out_sig=[])
        self.message_port_register_out(pmt.intern('out'))
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

        self.syncword = syncword
        self.preamble = preamble
        self.crc = crc
        self.whitening = whitening

    def handle_msg(self, msg_pmt):
        msg_list = pmt.to_python(pmt.cdr(msg_pmt))
        #when msg_list comes from pad source it is numpy.ndarray
        #we prefer giving non numpy objects to packet create
        if isinstance(msg_list, numpy.ndarray):
             msg_list =  msg_list.tolist()
        packet_buffer = cc11xx_packet.create(msg_list, preamble= self.preamble, syncword=self.syncword, crc=self.crc, whitening=self.whitening)
        packet_arr = numpy.frombuffer(packet_buffer, dtype='uint8')
        self.message_port_pub(pmt.intern('out'), pmt.cons(pmt.PMT_NIL, pmt.to_pmt(packet_arr)))
