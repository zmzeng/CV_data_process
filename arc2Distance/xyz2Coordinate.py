# -*- coding: utf-8 -*-

import re, math, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class xyz2Coordinate(object):
    """
    Description: 
        This script read in .xyz file generated by Lammps
        and output the coordinate of the specific atom for every frame.
        The result will be plot and output in file end with _Coordinate.txt.

    Usage: 
            $ python xyz2Coordinate.py file2Process step2time atom

    Args:
        file2Process (str): define which file to process.
        step2time (int, optional): define how much time in a step. default is 2000step/ps.
        atom (str, optional): atom type to ouput, default is Ni.

    Attributes:
        self.file2Process (str): define which file to process.
        self.step2time (int): define how much time in a step. default is 2000step/ps.
        self.atom (str): atom type to ouput, default is Ni.
        self.listOfTime (list)：list of all time data.
        self.listOfatom (list): list of coordinate of atom.

    code by zmzeng12 20180308
    """

    def __init__(self, pyname, file2Process, step2time=2000, atom='Ni'):

        print('\n------>  ' + 'The file to process is ' + file2Process )
        print('------>  ' + 'step of time is set to ' + str(step2time) + ' step/ps')
        print('------>  ' + 'atom is set to ' + atom +'\n')
        self.file2Process = file2Process;
        self.listOfTime = []
        self.listOfatom = []
        self.step2time = int(step2time)
        self.atom = atom

    def readFile(self):
        """read file2Process and put data into related lists.
        """
        file = open(self.file2Process, 'r')
        line = file.readline()
        coordinateX = []
        coordinateY = []
        coordinateZ = []
        while line:
            if line.find('Timestep') != -1:
                Timestep = int(line.split()[2])
                # convert timestep to time
                self.listOfTime.append(Timestep / self.step2time)
            elif line.find(self.atom) != -1: 
                coordinate = [float(i) for i in line.split()[1:4]]
                coordinateX.append(coordinate[0])
                coordinateY.append(coordinate[1])
                coordinateZ.append(coordinate[2])
            line = file.readline()
        self.listOfatom.append(coordinateX)
        self.listOfatom.append(coordinateY)
        self.listOfatom.append(coordinateZ)

        file.close()
        print('\n------>  ' + 'Number of frames:' + str(len(self.listOfTime)) +'\n')
        print('------>  ' + 'Number of '+ self.atom + ':' + str(len(self.listOfatom[0])) +'\n')

    def coordinate2str(self, list):
        str = ''
        for i in list:
            str += str(i) + '   '
        return str 

    def outputData(self):
        file = open(self.file2Process[0:-4] + '_Coordinate.txt', 'w')
        file.write('generated by xyz2Coordinate.py from %s\n' %self.file2Process)
        file.write('Time    Coordinate (%s)\n' % self.atom)
        file.write('ps    A\n')
        for time, x, y, z in zip(self.listOfTime, self.listOfatom[0], self.listOfatom[1], self.listOfatom[2]):
            file.write('%f    %f    %f    %f\n' % (time, x, y, z))
        file.close()
        print('\nall done!')
        print('result is stored in ' + self.file2Process[0:-4] + '_Coordinate.txt \n')

    def plotData(self):
        plt.figure('Coordinate - ' + self.atom)
        plt.plot(self.listOfTime[0: len(self.listOfatom[0])], self.listOfatom[0], label='x')
        plt.plot(self.listOfTime[0: len(self.listOfatom[0])], self.listOfatom[1], label='y')
        plt.plot(self.listOfTime[0: len(self.listOfatom[0])], self.listOfatom[2], label='z')
        plt.legend()
        plt.xlabel('Tims (ps)')
        plt.ylabel('Distance (A)')
        plt.title('Coordinate - ' + self.atom)
        plt.savefig(self.file2Process[0:-4] + '_Coordinate-' + self.atom + '.png')

    # conver xyz to coordinate!
    def main(self):
        self.readFile()
        self.outputData()
        self.plotData()

if __name__=='__main__':

    test = xyz2Coordinate(*sys.argv)
    test.main()

