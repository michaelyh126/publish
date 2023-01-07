# -*- coding: utf-8 -*-
import thread
from bottle import route, run,Bottle,request,template
import tool
import test


@route('/message')
def hello():
    return "Today is a beautiful day"

@route('/publish_local')
def publish_local():
    mxd_file_path=request.query.mxd_file_path
    mxd_file_path=str(mxd_file_path)
    try:
        thread.start_new_thread(test.test)
    except:
        print "Error: unable to start thread"
    return '正在发布服务'


if __name__ == '__main__':
    run(host='localhost', port=8029, debug=True)