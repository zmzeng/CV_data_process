### Description: this script read in .txt file generated by X-ray photoelectron spectroscopy
###              and revise all data according to the standard energy of Carbon
### Usage: python xpsProcess.py <filename> [standard Energy Of Carbon]
### example: python xpsProcess.py test.txt
### code by zmzeng12 20180314

#coding: utf-8
import re
import sys

class xpsProcess(object):

    def __init__(self, py, file2Process, standardEnergyOfCarbon=284.6):
        self.file2Process = file2Process
        self.standardEnergyOfCarbon = float(standardEnergyOfCarbon)

        print('-------------------\n')
        print('The file to process is ' + self.file2Process )
        print('The standard energy of C is set to ' + str(self.standardEnergyOfCarbon) +'\n')
        print('-------------------\n')
        self.atoms = []
        self.spectrum = []
        self.delta = 0.0

    def readFile(self):
        print('Read file...'+'\n')
        file = open(self.file2Process, 'r')
        line = file.readline()
        while line:
            # every atom data is start with line with 'Region'
            if line.find('Region') != -1 and line:
                line = self.getData(file)
        file.close()
        print('Found atoms: '+ str(self.atoms[1:]) +'\n')
        print('-------------------\n')

    def getData(self, file):
        line = file.readline()
        # use RegExr to match the atom type
        atom = re.search('false\s(.*?)\s7', line).group(1)
        self.atoms.append(atom)
        line = file.readline()
        line = file.readline()
        line = file.readline()
        line = file.readline()
        alldata = []
        # all atom experiment data are stored in self.spectrum
        while line.find('Region') == -1 and line:
            if line.find('Layer') != -1 :
                line = file.readline()
                line = file.readline()
                line = file.readline()
            data = [float(x) for x in line.split('\t')]
            alldata.append(data)
            line = file.readline()
        self.spectrum.append(alldata)
        return line

    # Delta = Esignal - Estandard
    def findDelta(self):
        temp = self.spectrum[self.atoms.index('C')]
        index = 0
        max = 0
        for i in range(0,len(temp)):
            if max < temp[i][1]:
                max = temp[i][1]
                index = i
            i += 1
        energyOfCarbon = temp[index][0]
        self.delta = energyOfCarbon - self.standardEnergyOfCarbon
        print('max position is ' + str(energyOfCarbon))
        print('delta is ' + str(self.delta) +'\n')
        print('-------------------\n')

    # Estandard = Esignal - Delta
    def reviseData(self, data):
        return str(data[0]-self.delta) + '  ' + str(data[1]) + '  ' + str(data[0]) 

    def outputData(self):
        for i in range(0,len(self.atoms)):
            if self.atoms[i] == '':
                self.atoms[i] = 'whole spectrum'
            file = open(self.atoms[i] + '_Result.txt', 'w')
            file.write(self.atoms[i] + ' generated by xpsProcess.exe\n')
            file.write('Energy(revised)  Counts  Energy\n')
            file.write('eV eV \n')
            file.write(self.atoms[i] + ' ' + self.atoms[i] + ' '+ self.atoms[i] + '\n')
            for data in self.spectrum[i]:
                file.write(self.reviseData(data) + '\n')
            file.close()
        print('all done!\n')


    def process(self):
        self.readFile()
        self.findDelta()
        self.outputData()

if __name__=='__main__':

    test = xpsProcess(*sys.argv)
    test.process()


