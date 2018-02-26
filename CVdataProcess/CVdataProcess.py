# ### CVdataProcess

# #### Description: 
# When perform cyclic voltammetry method, usually the experiment will go many repeat cycle. But only the data of first or the last cycle is what we need.
# This script will read in all the data files(.txt) in `D:/auto/` and output data of the first cycle and last cycle.

# #### Usage:
# 1. put all your data file in `D:/auto`
# 2. `python CVdataProcess.py`

# *code by zmzeng12 20110110*


# coding:utf-8
import os


# 遍历指定目录，返回目录下的所有文件名
def get_file(filepath):
    path_dir = os.listdir(filepath)
    all_dir = []
    for every_dir in path_dir:
        child = os.path.join('%s%s' % (filepath, every_dir))
        all_dir.append(child)
    return all_dir  # .decode('gbk')  # .decode('gbk')是解决中文显示乱码问题

#筛选掉非数据文件和处理后的输出文件
def filter_dir(allDir):
    output_dir = []
    for everyDir in allDir:
        if everyDir.find('cycle') == -1 and everyDir.find('.txt') != -1:
            f = open(everyDir, 'r')
            lines = f.readlines()
            for line in lines:
                if line.find('Cyclic Voltammetry\n') != -1:
                    output_dir.append(everyDir)
    return output_dir


# 读取文件内容并处理
def process_file(filename):
    f = open(filename, 'r')  # r 代表read
    # 定义output文件名
    filename_output = os.path.join('%s%s' % (filename, '_first cycle.txt'))
    f_output = open(filename_output, 'w')
    line = f.readline()  # 调用文件的 readline()方法
    # 获取段数，并讲info信息写入output文件
    while line.find('Potential/V, Current/A') != 0:
        if line.find('Segment =') == 0:
            segment_num = line.split()[2]
            print 'Segment : %s' % segment_num
        f_output.write('%s' % line)
        line = f.readline()
    # 补写Potential/V, Current/A以及后面的空行
    f_output.write('%s' % line)
    line = f.readline()
    f_output.write('%s' % line)
    # 从第一行数据获取初始电压
    line = f.readline()
    InitE = (line.split(',')[0])
    print 'Init E : %s' % InitE
    # 输出第一圈
    f_output.write(line)
    line = f.readline()
    while line.find(InitE) == -1:
        f_output.write(line)
        line = f.readline()
    f_output.close()
    # 找到最后一圈的位置
    i = 2
    while not i > int(segment_num) / 2 - 1:
        line = f.readline()
        if line.find(InitE) == 0 or line.find('-' + InitE) == 0:
            i += 1
    # 把最后一圈的数据都写入output文件
    filename_output = os.path.join('%s%s' % (filename, '_last cycle.txt'))
    f_output = open(filename_output, 'w')
    while 1:
        if not line:
            break
        f_output.write('%s' % line)
        line = f.readline()

    f.close()
    f_output.close()


if __name__ == '__main__':

    print 'Please put cv data(.txt files) in D:/auto/%s' \
          'Press Enter to continue' % os.linesep
    raw_input()
    # 指定存放cv txt数据位置
    try:
        allDir = get_file('D:\\auto\\')
    except StandardError:
        print 'can\'t get files'
    # 遍历文件夹中的文件，并进行筛选
    filtered_Dir = filter_dir(allDir)
    print filtered_Dir
    # 遍历筛选后的列表，并处理和输出
    for everyDir in filtered_Dir:       
        print 'processing %s' % everyDir
        try:
            process_file(everyDir)
        except StandardError:
            print 'The file is not a cv data'
            continue
    print '%sAll done!%s' \
          'Press Enter to exit' % (os.linesep, os.linesep)
    raw_input()
