from unittest.mock import patch
import unittest

import cwl_client.interface as i_face


class TestInterface(unittest.TestCase):
    def test_no_retry(self):
        with patch('builtins.print'):
            with patch('builtins.input', side_effect=['1']):
                self.assertTrue(i_face.ask_true_or_false('msg'))
            with patch('builtins.input', side_effect=['2']):
                self.assertFalse(i_face.ask_true_or_false('msg'))

    def test_retry(self):
        with patch('builtins.print'):
            with patch('builtins.input', side_effect=['a', '', '0', '-1', 'e3\n', '1']):
                self.assertTrue((i_face.ask_true_or_false('msg')))

    # def test_select_from_dict(self):
    #     dict_for_testcase = {1: 'swing', 2: 'scalping', 3: 'other'}
    #     with patch('builtins.print'):
    #         for key, val in dict_for_testcase.items():
    #             with patch('cwl_client.interface.prompt_inputting_decimal', return_value=key):
    #                 result = i_face.select_from_dict(dict_for_testcase)
    #                 self.assertEqual(result, val, '選択したkeyに対応するvalを得る')


if __name__ == '__main__':
    unittest.main()
