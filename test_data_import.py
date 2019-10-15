import unittest
import os
import random
import decimal
import statistics
import datetime
import data_import


class TestDataImport(unittest.TestCase):
    '''
    Unit test for data_import.py
    '''
    def setUp(self):
        file = open('search.csv', 'w')
        file.write('time,value\n')
        file.write('1/29/18 1:29,1.0\n')
        file.write('2/12/18 1:29,2.0\n')
        file.close()
        self.obj = data_import.ImportData('search.csv')
        self.obj._rounded_time.append(datetime.datetime(2018, 1, 29, 1, 29))
        self.obj._rounded_time.append(datetime.datetime(2018, 2, 12, 1, 29))

    def tearDown(self):
        os.remove('search.csv')

    def test_ImportDataClass(self):
        file = './smallData/cgm_small.csv'
        res = data_import.ImportData(file)
        self.assertEqual(len(res._time), len(res._value))

    def test_Init(self):
        file = open('test.csv', 'w')
        file.write('time,value\n')
        file.write('1/29/18 1:29,25\n')
        file.close()
        obj = data_import.ImportData('test.csv')
        self.assertEqual(obj._value[0], 25)
        os.remove('test.csv')

    def test_InitWithHighLow(self):
        file = open('./cgm_small.csv', 'w')
        file.write('time,value\n')
        file.write('1/29/18 1:29,low\n')
        file.write('2/12/18 1:29,high\n')
        file.close()
        obj = data_import.ImportData('cgm_small.csv')
        self.assertEqual(obj._value[0], 40.0)
        self.assertEqual(obj._value[1], 300.0)
        os.remove('cgm_small.csv')

    def test_linear_search_notfound(self):
        timestamp = datetime.datetime(2018, 1, 29, 1, 20)
        res = self.obj.linear_search_value(timestamp)
        self.assertEqual(res, -1)

    def test_linear_search_found(self):
        timestamp = datetime.datetime(2018, 1, 29, 1, 29)
        res = self.obj.linear_search_value(timestamp)
        self.assertEqual(res, [1.0])

    def test_binary_search_notfound(self):
        timestamp = datetime.datetime(2018, 1, 29, 1, 20)
        res = self.obj.linear_search_value(timestamp)
        self.assertEqual(res, -1)

    def test_binary_search_found(self):
        timestamp = datetime.datetime(2018, 1, 29, 1, 29)
        res = self.obj.linear_search_value(timestamp)
        self.assertEqual(res, [1.0])

    def test_print_array_round_to_5(self):
        data = []
        for f in os.listdir('smallData'):
            if '.csv' in f:
                data.append(data_import.ImportData('smallData/' + f))
        data_5 = []
        for i in data:
            data_5.append(data_import.roundTimeArray(i, 5))
        self.assertNotEqual(
            data_import.printArray(data_5,
                                   os.listdir('smallData'),
                                   'out_5', 'cgm_small.csv'), -1)
        self.assertTrue(os.path.exists('out_5.csv'))
        os.remove('out_5.csv')

    def test_print_array_round_to_15(self):
        data = []
        for f in os.listdir('smallData'):
            if '.csv' in f:
                data.append(data_import.ImportData('smallData/' + f))
        data_15 = []
        for i in data:
            data_15.append(data_import.roundTimeArray(i, 15))
        self.assertNotEqual(
            data_import.printArray(data_15,
                                   os.listdir('smallData'),
                                   'out_15', 'cgm_small.csv'), -1)
        self.assertTrue(os.path.exists('out_15.csv'))
        os.remove('out_15.csv')


if __name__ == '__main__':
    unittest.main()
