# -*- coding:utf-8 -*-

import bottle
import json
import subprocess
import sys
from xpsProcess import xpsProcess
from FLS980 import FLS980Process

path_of_temp_file='/tmp/WebApp/temp'

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
    filename = get_upload_file()
    standard_energy_of_Carbon = bottle.request.forms.get('standard_energy_of_Carbon')

    try:
        if(standard_energy_of_Carbon == ""):
            test = xpsProcess.xpsProcess('py', path_of_temp_file + '/' + filename)
        else:
            test = xpsProcess.xpsProcess('py', path_of_temp_file + '/' + filename, float(standard_energy_of_Carbon))
        test.main()
        info['response_info'] = test.response_info
        wrap_result_files(filename, info)
        return bottle.template('app', info)

    except Exception as e:
        print(e)
        info['respones_status'] = "something wrong with your data file!"
        return bottle.template('app', info)

@bottle.route('/FLS980')
def fls980():
    info = get_app_info('FLS980')
    return bottle.template('app', info)

@bottle.post('/FLS980')
def fls980_upload():
    info = get_app_info('FLS980')
    filename = get_upload_file()
    try:
        test = FLS980Process.FLS980Process(path_of_temp_file + '/' + filename)
        test.main()
        info['response_info'] = test.response_info
        wrap_result_files(filename, info)
        return bottle.template('app', info)
    except Exception as e:
        print(e)
        info['respones_status'] = "something wrong with your data file!"
        return bottle.template('app', info)

@bottle.route('/output/<filename:path>')
def file_download(filename):
    print('download ' + filename)
    return bottle.static_file(filename, root=path_of_temp_file, download=filename)

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

def get_upload_file():
    command = 'rm ' + path_of_temp_file + '/*'
    subprocess.call(command, shell=True)
    file_upload = bottle.request.files.get('file_upload')
    try:
        file_upload.save(path_of_temp_file, overwrite=True)
        print('get and save upload file successfully')
        return file_upload.filename
    except Exception as e:
        print(e)
        print('no file is upload.')
        return ''

def wrap_result_files(filename, info):
    command = 'zip -jJ ' + path_of_temp_file + '/' + filename[0:-4] + '.zip ' + path_of_temp_file + '/*'
    subprocess.call(command, shell=True)
    print('wrap output files.')
    info['download_link'] = '/output/' + filename[0:-4] + '.zip'
    info['respones_status'] = "success!"


if __name__ == "__main__":
    bottle.run(host='127.0.0.1', port=9091, debug=True)
else:
    application = bottle.default_app()
    bottle.debug(True)

