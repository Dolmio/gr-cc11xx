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
