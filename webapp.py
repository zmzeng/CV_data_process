# -*- coding:utf-8 -*-

import bottle
import json
import subprocess
from xpsProcess import xpsProcess
from FLS980 import FLS980Process
from cvProcess import cvProcess

path_of_temp_file='./tmp/'

app = bottle.default_app()

@app.route('/')
def welcome():          
    return bottle.template('index')

@app.route('/xpsProcess')
def xps():
    info = get_app_info('xpsProcess')
    return bottle.template('apps', info)

@app.post('/xpsProcess')
def xps_upload():
    info = get_app_info('xpsProcess')
    standard_energy_of_Carbon = bottle.request.forms.get('standard_energy_of_Carbon')
    filenames = get_upload_file()
    if filenames != []:
        for filename in filenames:
            try:
                info['response_info'].append(filename + ' :')
                if(standard_energy_of_Carbon == ""):
                    test = xpsProcess.xpsProcess('py', path_of_temp_file + '/' + filename)
                else:
                    test = xpsProcess.xpsProcess('py', path_of_temp_file + '/' + filename, float(standard_energy_of_Carbon))
                test.main()
                info['response_info'].extend(test.response_info)
            except Exception as e:
                print(e)
                info['response_info'].append('**something wrong with your data file!**')
        wrap_result_files(filename, info)
    else:
        info['respones_status'] = "no file upload!"

    return bottle.template('apps', info)

@app.route('/FLS980')
def fls980():
    info = get_app_info('FLS980')
    return bottle.template('apps', info)

@app.post('/FLS980')
def fls980_upload():
    info = get_app_info('FLS980')
    filenames = get_upload_file()
    if filenames != []:
        for filename in filenames:
            try:
                info['response_info'].append(filename + ' :')
                test = FLS980Process.FLS980Process(path_of_temp_file + '/' + filename)
                test.main()
                info['response_info'].extend(test.response_info)
            except Exception as e:
                print(e)
                info['response_info'].append('**something wrong with your data file!**')
        wrap_result_files(filenames[0], info)
    else:
        info['respones_status'] = "no file upload!"

    return bottle.template('apps', info)

@app.route('/cvProcess')
def cv():
    info = get_app_info('cvProcess')
    return bottle.template('apps', info)

@app.post('/cvProcess')
def cv_upload():
    info = get_app_info('cvProcess')
    filenames = get_upload_file()
    if filenames != []:
        for filename in filenames:
            try:
                info['response_info'].append(filename + ' :')
                test = cvProcess.cvProcess('py', path_of_temp_file + '/' + filename)
                test.main()
                info['response_info'].extend(test.response_info)   
            except Exception as e:
                print(e)
                info['response_info'].append('**something wrong with your data file!**')
        wrap_result_files(filenames[0], info)
    else:
        info['respones_status'] = "no file upload!"

    return bottle.template('apps', info)

@app.route('/output/<filename:path>')
def file_download(filename):
    print('download ' + filename)
    return bottle.static_file(filename, root=path_of_temp_file, download=filename)

@app.route('/ico/<filename>')
def get_ico(filename):
    path = './' + filename[0:-4]
    filename = filename
    print(path)
    return bottle.static_file(filename, root=path)

@app.route('/static/css/<filename>')
def get_static(filename):
    path = './css'
    return bottle.static_file(filename, root=path)

def get_app_info(appname):
    path_json_of_appinfo = './' + appname + '/' + appname + '.json'
    with open(path_json_of_appinfo, 'r') as f:
        info = json.load(fp=f)
    return info

def get_upload_file():
    command = 'rm ' + path_of_temp_file + '/*'
    subprocess.call(command, shell=True)
    file_upload = bottle.request.files.getall('file_upload')
    filenames = []
    try:
        for file in file_upload:
            file.save(path_of_temp_file, overwrite=True)
            print('get and save upload file successfully：' + file.filename)
            filenames.append(file.filename)
        return filenames
    except BaseException:
        #print(e)
        print('no file is upload.')
        return []

def wrap_result_files(filename, info):
    command = 'zip -jJ ' + path_of_temp_file + '/' + filename[0:-4] + '.zip ' + path_of_temp_file + '/*'
    subprocess.call(command, shell=True)
    print('wrap output files.')
    info['response_info'].append('Click *here* to download.')
    info['download_link'] = '/output/' + filename[0:-4] + '.zip'
    info['respones_status'] = "success!"


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True, reloader=True)

