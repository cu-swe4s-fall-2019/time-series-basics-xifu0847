import csv
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import copy
import datetime
import os
import math
import time


class ImportData:
    def __init__(self, data_csv):
        self._time = []
        self._value = []
        self._rounded_time_list = []
        self._rounded_time = []
        self._data_csv = data_csv

        # open file, create a reader from csv.DictReader,
        # and read input times and values
        with open(self._data_csv) as f:
            csv_data = csv.DictReader(f)
            for row in csv_data:
                if not ('time' in row.keys() and 'value' in row.keys()):
                    raise ValueError('The csv does not have either'
                                     'time or value column')

                num = None
                if row['time'] == 'NaN':
                    print('Found a NaN value input, skip it')
                    continue
                if not (row['value'] == 'low' or row['value'] == 'high'):
                    try:
                        num = float(row['value'])
                    except ValueError as e:
                        print('Find a bad value input')
                        continue
                if row['time'] == '':
                    print('Time column is not in good format')
                    continue

                timestamp = datetime.datetime.strptime(row['time'],
                                                       '%m/%d/%y %H:%M')
                self._time.append(timestamp)
                if 'cgm_small' in self._data_csv:
                    if row['value'] == 'low':
                        print('replacing low by 40')
                        self._value.append(40)
                    elif row['value'] == 'high':
                        print('replacing high by 300')
                        self._value.append(300)
                    else:
                        if num is not None:
                            self._value.append(num)
                else:
                    if num is not None:
                        self._value.append(num)

        if 'basal' in self._data_csv:
            self._time.reverse()
            self._value.reverse()

    def linear_search_value(self, key_time):
        # return list of value(s) associated with key_time
        # if none, return -1 and error message
        res = []
        for i in range(len(self._rounded_time)):
            if self._rounded_time[i] == key_time:
                res.append(self._value[i])
        if len(res) == 0:
            print('No corresponding result found')
            return -1
        return res

    def binary_search_value(self, key_time):
        # optional extra credit
        # return list of value(s) associated with key_time
        # if none, return -1 and error message
        res = []
        left = 0
        right = len(self._rounded_time) - 1
        pivot = -1
        while left <= right:
            mid = (right - left) // 2 + left
            if self._rounded_time[mid] == key_time:
                pivot = mid
                break
            elif self._rounded_time[mid] > key_time:
                right = mid - 1
            else:
                left = mid + 1

        if pivot == -1:
            print('No corresponding result found')
            return -1

        res.append(self._value[pivot])
        head = pivot
        while (head > 0 and
               self._rounded_time[head - 1] == self._rounded_time[head]):
            res.append(self._value[head - 1])
            head = head - 1
        tail = pivot
        while (tail < len(self._rounded_time) - 2 and
               self._rounded_time[tail + 1] == self._rounded_time[tail]):
            res.append(self._value[tail + 1])
            tail = tail + 1
        return res

    # Return 'sum' or 'average' for different calculate rules
    # defined for different csv files.
    # Return None if the input is invalid.
    def GetCalMethod(self):
        if ('activity' in self._data_csv or 'bolus' in self._data_csv or
                'meal' in self._data_csv):
            return 'sum'
        elif ('smbg' in self._data_csv or 'hr' in self._data_csv or
              'cgm' in self._data_csv or 'basal' in self._data_csv):
            return 'average'
        return None


def roundTimeArray(data, res):
    # Inputs: data (ImportData Object) and res (rounding resoultion)
    # objective:
    # create a list of datetime entries and associated values
    # with the times rounded to the nearest rounding resolution (res)
    # ensure no duplicated times
    # handle duplicated values for a single timestamp based on instructions in
    # the assignment
    # return: iterable zip object of the two lists
    # note: you can create additional variables to help with this task
    # which are not returned
    obj = copy.deepcopy(data)
    method = obj.GetCalMethod()
    if method is None:
        raise ValueError('Double check the name of input csv file')
    for time in obj._time:
        next_diff = res - time.minute % res
        pre_diff = time.minute % res
        if next_diff < pre_diff:
            time = time + datetime.timedelta(minutes=next_diff)
        else:
            time = time - datetime.timedelta(minutes=pre_diff)
        obj._rounded_time.append(time)

        if time not in obj._rounded_time_list:
            obj._rounded_time_list.append(time)
    temp_result = []
    for i in range(len(obj._rounded_time_list)):
        search_result = obj.binary_search_value(obj._rounded_time_list[i])
        temp_result.append(search_result)
    result = []

    for i in range(len(temp_result)):
        if method == 'sum':
            result.append(sum(temp_result[i]))
        elif method == 'average':
            result.append(sum(temp_result[i]) / len(temp_result[i]))
    return zip(obj._rounded_time_list, result)


def printArray(data_list, annotation_list, base_name, key_file):
    """
    Arguments
    --------
    data_list: list of data which is generated by roundTimeArray
    annotation_list: list of csv names
    base_name: output csv file name
    key_file: which file should we use as primary key
    Returns
    --------
    """
    pri_data = None
    pri_anno = None
    sec_data = []
    sec_anno = []
    if os.path.exists(base_name + '.csv'):
        raise NameError('File already exist')
    if key_file not in annotation_list:
        raise ValueError('Please double check your sort key')

    for i in range(len(annotation_list)):
        if (annotation_list[i] == key_file):
            pri_anno = annotation_list[i]
            pri_data = data_list[i]
        else:
            sec_anno.append(annotation_list[i])
            sec_data.append(data_list[i])

    header = ['time', key_file] + sec_anno
    with open(base_name + '.csv', mode='w') as f:
        file_writer = csv.writer(f, delimiter=',')
        file_writer.writerow(header)

        for time1, value1 in pri_data:
            sec_list = []
            for data in sec_data:
                res = 0
                for time2, value2 in data:
                    s1 = time1.strftime("%D/%Y %H:%M")
                    s2 = time2.strftime("%D/%Y %H:%M")
                    if s1 == s2:
                        res = value2
                        break
                sec_list.append(res)
            file_writer.writerow([time1, value1] + sec_list)
    return 0


if __name__ == '__main__':
    # adding arguments
    parser = argparse.ArgumentParser(
        description='A class to import, combine and print data from a folder.',
        prog='dataImport')

    parser.add_argument('--folder_name', type=str, help='Name of the folder')

    parser.add_argument('--output_file', type=str, help='Name of Output file')

    parser.add_argument('--sort_key', type=str, help='File to sort on')

    parser.add_argument('--number_of_files', type=int,
                        help="Number of Files", required=False)

    args = parser.parse_args()

    # pull all the folders in the file
    if not os.path.isdir(args.folder_name):
        raise FileNotFoundError('Directory not found')

    files_lst = [f for f in listdir(args.folder_name)]  # list the folders
    print(files_lst)

    # import all the files into a list of ImportData objects (in a loop!)
    data_lst = []
    for csv_file in files_lst:
        data_lst.append(ImportData(args.folder_name + '/' + csv_file))

    # create two new lists of zip objects
    # do this in a loop, where you loop through the data_lst
    start_time = time.time()
    data_5 = []  # a list with time rounded to 5min
    for data in data_lst:
        data_5.append(roundTimeArray(data, 5))
    data_15 = []  # a list with time rounded to 15min
    for data in data_lst:
        data_15.append(roundTimeArray(data, 15))
    end_time = time.time()
    print(end_time - start_time)

    # print to a csv file
    printArray(data_5, files_lst, args.output_file+'_5', args.sort_key)
    printArray(data_15, files_lst, args.output_file+'_15', args.sort_key)
