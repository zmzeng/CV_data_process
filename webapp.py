# -*- coding:utf-8 -*-

import bottle
import json
import subprocess
from xpsProcess import xpsProcess
from FLS980 import FLS980Process

upload_path='/tmp/WebApp/temp'

@bottle.route('/')
def welcome():          
    return bottle.template('welcome')                 

@bottle.route('/xpsProcess')
def xps():
    info = get_app_info('xpsProcess')
    return bottle.template('app', info)

@bottle.post('/xpsProcess')
def xps_upload():
    info = get_app_info('xpsProcess')

    command = 'rm ' + upload_path + '/*'
    subprocess.call(command, shell=True)

    uploadfile = bottle.request.files.get('uploadfile')
    standard_energy_of_Carbon = bottle.request.forms.get('standard_energy_of_Carbon')

    try:
        uploadfile.save(upload_path, overwrite=True)#overwrite参数是指覆盖同名文件
        print('get uploadfile and save...')
        if(standard_energy_of_Carbon == ""):
            test = xpsProcess.xpsProcess('py', upload_path + '/' + uploadfile.filename)
        else:
            test = xpsProcess.xpsProcess('py', upload_path + '/' + uploadfile.filename, float(standard_energy_of_Carbon))
        test.main()

        response_info = []
        response_info.append('------>  ' + 'The file to process is ' + test.file2Process)
        response_info.append('------>  ' + 'The standard energy of C is set to ' + str(test.standardEnergyOfCarbon))
        response_info.append('------>  ' + 'Found atoms: '+ str(test.atoms[1:]))
        response_info.append('------>  ' + 'delta is ' + str(test.delta))
        response_info.append('click here to download output file.')
        info['response_info'] = response_info

        command = 'zip -jJ /tmp/WebApp/temp/' + uploadfile.filename[0:-4] + '.zip /tmp/WebApp/temp/*'
        subprocess.call(command, shell=True)
        print('wrap output files.')

        info['download_link'] = '/output/' + uploadfile.filename[0:-4] + '.zip'
        info['respones_status'] = "success!"

        return bottle.template('app', info)

    except:
        info['respones_status'] = "something wrong with your data file!"
        return bottle.template('app', info)

@bottle.route('/FLS980')
def fls980():
    info = get_app_info('FLS980')
    return bottle.template('app', info)

@bottle.post('/FLS980')
def fls980_upload():
    info = get_app_info('FLS980')
    command = 'rm ' + upload_path + '/*'
    subprocess.call(command, shell=True)

    uploadfile = bottle.request.files.get('uploadfile')

    try:
        uploadfile.save(upload_path, overwrite=True)#overwrite参数是指覆盖同名文件
        print('get uploadfile and save...')
        test = FLS980Process.FLS980Process(upload_path + '/' + uploadfile.filename)
        test.main()

        response_info = []
        response_info.append('all done!')
        response_info.append('click here to download output file.')
        info['response_info'] = response_info
        command = 'zip -jJ /tmp/WebApp/temp/' + uploadfile.filename[0:-4] + '.zip /tmp/WebApp/temp/*'
        subprocess.call(command, shell=True)
        print('wrap output files.')

        info['download_link'] = '/output/' + uploadfile.filename[0:-4] + '.zip'
        info['respones_status'] = "success!"

        return bottle.template('app', info)
    except:
        info['respones_status'] = "something wrong with your data file!"
        return bottle.template('app', info)

@bottle.route('/output/<filename:path>')
def file_download(filename):
    print('download ' + filename)
    return bottle.static_file(filename, root=upload_path, download=filename)

@bottle.route('/static/<filename>')
def get_static(filename):
    path = './' + filename
    filename = filename + '.icon'
    print(path)
    return bootle.static_file(filename, root=path)

def get_app_info(appname):
    path_json_of_appinfo = './' + appname + '/' + appname + '.json'
    with open(path_json_of_appinfo, 'r') as f:
        info = json.load(fp=f)
    return info

if __name__ == "__main__":
    bottle.run(host='127.0.0.1', port=9091, debug=True)
else:
    application = bottle.default_app()
    bottle.debug(True)

