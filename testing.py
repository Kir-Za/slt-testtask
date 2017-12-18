import os
import unittest
from config import TEST_DATABASE, app
from utils import check_ip, create_rack, get_detail_rack_info, remove_rack, create_and_add_server, \
    remove_server, move_to_del


class FlaskrTestCase(unittest.TestCase):
    """
    Тест критически важных функций
    """
    def setUp(self):
        app.testing = True
        app.config['DATABASE'] = TEST_DATABASE

    def test_create_rack(self):
        first_rack = create_rack('newline', 10)
        info = get_detail_rack_info(1)
        first_out = remove_rack(1)
        self.assertEqual(first_rack, 1)
        self.assertEqual([info.get('id', None), info.get('volume', None)], [1, 10])
        self.assertEqual(first_out, 1)

    def test_create_server(self):
        first_rack = create_rack('newline', 10)
        first_server = create_and_add_server(first_rack, '111.111.111.111', 128)
        second_server = create_and_add_server(first_rack, 'asdf.111.111.111', 128)
        self.assertEqual(first_server, 1)
        self.assertFalse(second_server)

    def test_check_ip(self):
        first_rack = create_rack('newline', 10)
        create_and_add_server(first_rack, '111.111.111.111', 128)
        good_ip = check_ip('222.222.222.222')
        self.assertEqual(good_ip, '222.222.222.222')
        with self.assertRaises(AttributeError):
            check_ip('222.222.222.asdfs')
        with self.assertRaises(AttributeError):
            check_ip('111.111.111.111')

    def test_remove_server(self):
        first_rack = create_rack('newline', 10)
        first_server = create_and_add_server(first_rack, '111.111.111.111', 128)
        bat_try = remove_server(first_server)
        del_serv = move_to_del(first_server)
        good_try = remove_server(first_server)
        self.assertEqual(bat_try, None)
        self.assertTrue(del_serv)
        self.assertTrue(good_try)

    def tearDown(self):
        try:
            os.remove(TEST_DATABASE)
        except Exception:
            pass

if __name__ == '__main__':
    unittest.main()
