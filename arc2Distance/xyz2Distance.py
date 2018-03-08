### Description: this script read in .xyz file generated by Lammps
###              and calculate the distance betweent Zr-Ni for every
###              frame.
### Usage: python xyz2Distance.py file.xyz steptime atom2cal
### steptime - int, default is 2000step/ps 
### atom2cal - element, default is Zr
### example: python xyz2Distance.py md.xyz 1000 Hf
### code by zmzeng12 20180303

#coding :utf-8

import re, math, sys

class xyz2Distance(object):

    def __init__(self, file2Process, step2time=2000, atom2cal='Zr'):
        print('\nThe file to process is ' + file2Process +'\n')
        print('\nstep of time is set to ' + str(step2time) +'\n')
        print('\natom is set to ' + atom2cal +'\n')
        self.file2Process = file2Process;
        self.listOfTime = []
        self.listOfatom2cal = []
        self.listOfNi = []
        self.listOfDistance = []
        self.step2time = step2time # default is 2000step/ps
        self.atom2cal = atom2cal

    # get all Time and Zr, Ni coordinate in list
    def readFile(self):
        print('Read file...'+'\n')
        file = open(self.file2Process, 'r')
        line = file.readline()
        while line:
            if line.find('Timestep')!=-1:
                Timestep = int(line.split()[2])
                # convert timestep to time
                self.listOfTime.append(str(Timestep/int(self.step2time)))
            elif line.find(self.atom2cal)!=-1: 
                self.listOfatom2cal.append(line.split()[1:4])
            elif line.find('Ni')!=-1:
                self.listOfNi.append(line.split()[1:4])
            line = file.readline()
        file.close()
        print('Number of frames:' + str(len(self.listOfNi)) +'\n')
        print('Number of Ni:' + str(len(self.listOfNi)) +'\n')
        print('Number of '+ self.atom2cal + ':' + str(len(self.listOfatom2cal)) +'\n')


    # difine distance Calculator
    def distanceCal(self, atom1, atom2):
        # get distance 
        d1 = math.pow(float(atom2[0]) - float(atom1[0]), 2)
        d2 = math.pow(float(atom2[1]) - float(atom1[1]), 2)
        d3 = math.pow(float(atom2[2]) - float(atom1[2]), 2)
        return str(math.sqrt(d1 + d2 + d3))

    # get the distance between Ni and the first Zr atom
    # There are 12 Zr and 1 Ni atoms in the structure of every time step
    def getDistance(self):
        print('Calculating distance...'+'\n')
        self.listOfDistance.append(self.distanceCal(self.listOfatom2cal[0], self.listOfNi[0]))
        i=1
        while i < len(self.listOfTime):
            distance = self.distanceCal(self.listOfatom2cal[i*12], self.listOfNi[i])
            self.listOfDistance.append(distance)
            i += 1

    # output all data
    def outputData(self):
        file = open(self.file2Process[0:-4] + '_Result.txt', 'w')
        file.write('Time (ps)    Distance (Ni-' + self.atom2cal + ') (A)\n')
        for time, distance in zip(self.listOfTime, self.listOfDistance):
            file.write(time + '    ' + distance + '\n')
        file.close()
        print('all done!')
        print('result is stored in ' + self.file2Process[0:-4] + '_Result.txt \n')

    # conver xyz to distance!
    def convert(self):
        self.readFile()
        self.getDistance()
        self.outputData()

if __name__=='__main__':

    file2Process = sys.argv[1];
    step2time = sys.argv[2];
    atom2cal = sys.argv[3];


    test = xyz2Distance(file2Process, step2time, atom2cal)
    test.convert()
