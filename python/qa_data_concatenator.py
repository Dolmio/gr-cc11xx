from gnuradio import gr, gr_unittest, blocks
import pmt
from data_concatenator import data_concatenator
import numpy
import time
class qa_data_concatenator_bb (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def concat_test (self, data_to_concat):
        payload = [0x00]
        strobe = blocks.message_strobe(pmt.cons(pmt.PMT_NIL, pmt.to_pmt(payload)), 200)
        concatenator = data_concatenator(data_to_concat=data_to_concat)
        debug = blocks.message_debug()
        self.tb.msg_connect(strobe, "strobe", concatenator, "in")
        self.tb.msg_connect(concatenator, "out", debug, "store")

        self.tb.start()
        time.sleep(1)
        self.tb.stop()
        #Please get rid of this sleep if you know how!
        time.sleep(0.1)
        self.tb.stop()

        result_data = pmt.to_python(pmt.cdr(debug.get_message(0)))
        self.assertEqual(payload + data_to_concat , result_data.tolist())

    def test_concat_with_data(self):
        self.concat_test(data_to_concat=[0xff, 0xff])
    
    
    def test_concat_with_empty_data(self):
        self.concat_test(data_to_concat=[])

if __name__ == '__main__':
    gr_unittest.main ()
