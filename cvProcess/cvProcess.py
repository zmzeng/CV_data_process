# -*- coding: utf-8 -*-
import math
import numpy
import re
import sys

class cvProcess(object):

    def __init__(self, py, file_to_process):
        self.file_to_process = file_to_process
        self.data_raw = []
        self.sample_interval = 0.0
        self.info = []
        self.info.append('------>  ' + 'The file to process is ' + self.file_to_process)

    def read_file(self):
        number_of_headerline = 0
        with open(self.file_to_process, 'r') as file:
            with open(self.file_to_process[:-4] + '_last_round.txt', 'w') as file2:
                line = file.readline()
                while line:
                    if re.search('[-]*?\d*\.\d*, [-]*?\d\.\d*', line):
                        break
                    number_of_headerline = number_of_headerline + 1
                    file2.write(line)
                    line = file.readline()
        self.data_raw = numpy.loadtxt(self.file_to_process, skiprows=number_of_headerline, delimiter=',')
        self.data_raw = self.data_raw.T

    def find_last_round(self):
        self.sample_interval = math.fabs(self.data_raw[0][0] - self.data_raw[0][1])
        v_max = numpy.max(self.data_raw[0])
        index = len(self.data_raw[0]) -1
        index_last_max = []
        try:
            while index > 0 and len(index_last_max) < 2 :
                if v_max == self.data_raw[0][index]:
                    index_last_max.append(index)
                index -= 1
            self.data_raw = self.data_raw[:, index_last_max[1]:index_last_max[0]]
        except IndexError:
            pass
        self.info.append('------>  ' + 'Vpeak = ' + str(v_max))

    def output_data(self):

        numpy.savetxt(self.file_to_process[:-4] + "_last_round.txt", self.data_raw.T)

    def main(self):

        self.read_file()
        self.find_last_round()
        self.output_data()
        for i in self.info:
            print(i)

if __name__=='__main__':

    import os

    def get_file(filepath):
        path_dir = os.listdir(filepath)
        all_dir = []
        for every_dir in path_dir:
            child = os.path.join('%s%s' % (filepath, every_dir))
            all_dir.append(child)
        return all_dir

    allDir = get_file('D:/Code/Git/DataProcessing/cvProcess/test/')
    n = 0
    m = 0
    wrong = []
    for everyDir in allDir: 
        print('process.....' + everyDir)
        m += 1
        try:
            test = cvProcess('py', everyDir)
            test.main()
            print('done!')
            n += 1

        except Exception as e:
            print(e)
            wrong.append(everyDir)
    print('success %s/%s'%(n,m))
    with open('wrong.txt','w') as f:
        for i in wrong:
            f.write(i+'\n')

    # test = cvProcess(*sys.argv)
    # test.main()
