from gnuradio import gr, gr_unittest, digital, blocks
import cc11xx_swig as cc11xx
import numpy as np
import pmt
import cc11xx_encoder
import time
class qa_cc11xx_deframer_bb (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def encode_decode_test(self, payload_str="TEST", whitening=False, encode_crc=False, decode_crc=False):
        preamble = "01010101"
        sync1 = 0x2
        sync2 = 0x3
        sync_length = 2
        payload = [ord(c) for c in payload_str]

        strobe = blocks.message_strobe(pmt.cons(pmt.PMT_NIL, pmt.to_pmt(payload)), 200)
        encoder = cc11xx_encoder.cc11xx_encoder(preamble=[int(preamble, 2)], syncword=[sync1, sync2], whitening=whitening, crc=encode_crc)
        pdu_to_stream = blocks.pdu_to_tagged_stream(blocks.byte_t, "packet_len")
        debug = blocks.message_debug()
        self.tb.msg_connect(strobe, "strobe", encoder, "in")
        self.tb.msg_connect(encoder, "out", pdu_to_stream, "pdus")

        unpack = blocks.packed_to_unpacked_bb(1, 0)

        acc_code_block =  digital.correlate_access_code_tag_bb(preamble, 0, "preamble")
        deframer = cc11xx.cc11xx_deframer_bb(sync1 ,sync2, whitening, decode_crc, sync_length)

        self.tb.connect(pdu_to_stream,unpack)
        self.tb.connect(unpack, acc_code_block)
        self.tb.connect(acc_code_block, deframer)
        self.tb.msg_connect((deframer, 'out'), (debug, 'store'))
        self.tb.start()
        time.sleep(1)
        self.tb.stop()
        #Please get rid of this sleep if you know how!
        time.sleep(0.1)
        self.tb.stop()

        result_data = [i for i in pmt.to_python(pmt.cdr(debug.get_message(0)))]
        self.assertEqual(payload, result_data)

    def test_encode_decode_without_whitening (self):
        self.encode_decode_test(payload_str="TEST", whitening=False)

    def test_encode_decode_with_long_payload (self):
        self.encode_decode_test(payload_str="T" * 255, whitening=False)

    def test_encode_decode_with_whitening (self):
        self.encode_decode_test(payload_str="TEST", whitening=True)

    def test_encode_decode_with_crc_in_encode (self):
        self.encode_decode_test(payload_str="TEST", whitening=False, encode_crc=True)

if __name__ == '__main__':
    gr_unittest.main ()
