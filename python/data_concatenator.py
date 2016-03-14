import numpy
from gnuradio import gr
import pmt

class data_concatenator(gr.basic_block):
    def __init__(self, data_to_concat=[0xff]):
        gr.basic_block.__init__(self,
            name="data-concatenator",
            in_sig=[],
            out_sig=[])
        self.message_port_register_out(pmt.intern('out'))
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.data_to_concat = data_to_concat

    def handle_msg(self, msg_pmt):
        data = pmt.to_python(pmt.cdr(msg_pmt))
        concatenated =  numpy.concatenate((data, numpy.array(self.data_to_concat)))
        self.message_port_pub(pmt.intern('out'), pmt.cons(pmt.PMT_NIL, pmt.to_pmt(concatenated.astype(numpy.uint8))))