# -*- coding: utf-8 -*-
# encoding=utf8
import os
from flask import Flask,request
import uuid
import thread
import arcpy
import shutil
from werkzeug.utils import secure_filename
import tool
import sys

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
# app.config['ALLOWED_EXTENSIONS'] = set(['shp','shx','dbf','prj','sbx','fbx','aih','ixs','mxs','atx','xml','cpg'])

# def allowed_file(filename):
#     """
#     判断传入的文件后缀是否合规。不合规返回False
#     :param filename:
#     :return: True or False
#     """
#     return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']



# 创建mxd文件（arcpy未提供创建mxd文件方法，所以从空白mxd文件复制一份成为新的mxd文件）
# mxd_name表示文件名
def create_mxd(mxd_name):
    mxd=mxd_name+'__'+str(uuid.uuid1())+'.mxd'
    shutil.copy('mxd_Dir/blank.mxd','mxd_Dir/'+mxd)
    return mxd

# 重写mxd中的shp文件
# mxd_file为mxd文件的名称
# file_name为shp文件的名称
def rewrite_mxd(mxd_file,file_name):
    mxd = arcpy.mapping.MapDocument('mxd_Dir/'+mxd_file)
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    # 添加shp到mxd
    # lyr_path ='upload/'+file_name
    lyr_path =file_name
    lyr_path=str(lyr_path)
    '''改为当前项目文件夹地址'''
    lyr_path='C:/Users/86139/PycharmProjects/myArcgis/'+lyr_path
    lyr = arcpy.mapping.Layer(lyr_path)
    arcpy.mapping.AddLayer(df, lyr)
    mxd.save()

# 重写mxd中的tif文件
# mxd_file为mxd文件的名称
# file_name为tif文件的名称
# prj_file为prj文件的路径
def rewrite_mxd_tif(mxd_file,file_name,prj_file):
    mxd = arcpy.mapping.MapDocument('mxd_Dir/'+mxd_file)
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    sr=arcpy.SpatialReference(prj_file)
    # 添加tif到mxd
    # raster_path ='upload/'+file_name
    raster_path =file_name
    raster_path=str(raster_path)
    df.spatialReference=sr
    '''改为当前项目文件夹地址'''
    raster_path='C:/Users/86139/PycharmProjects/myArcgis/'+raster_path
    raster_lyr = arcpy.mapping.Layer(raster_path)
    arcpy.mapping.AddLayer(df, raster_lyr)
    mxd.save()


# 保存文件，并把加入uuid的文件名称返回（已废弃）
def save_file(file,path):
    if file is None:
        return {
            'message':"文件上传失败"
        }
    file_name = file.filename
    # file_name=str(file_name)
    suffix = os.path.splitext(file_name)[-1]#获取文件后缀（扩展名）
    name = os.path.splitext(file_name)[0]#获取文件后缀（扩展名）
    basePath = os.path.dirname(__file__)  # 当前文件所在路径print(basePath)
    upload_path = os.path.join(basePath, 'upload')#改到upload目录下# 注意：没有的文件夹一定要先创建，不然会提示没有该路径print(upload_path)
    upload_path = os.path.abspath(upload_path) # 将路径转换为绝对路径print("绝对路径：",upload_path)
    file_name=name+str(uuid.uuid1()) + suffix
    file_path=path
    file.save(file_path)#保存文件
    return file_name

# 通过调用py脚本发布服务（flask与arcpy发布服务同时运行会导致出错，故使用脚本发布服务）
def startpy(mxd_file_path):
    os.system('python create_service.py' + ' ' + mxd_file_path)



@app.route('/')
def hello():
    return 'hello'



#  发布本地的mxd的文件
@app.route('/publish_local')
def publish_local():
    mxd_file_path=request.args.get("mxd_file_path")
    mxd_file_path=str(mxd_file_path)
    try:
        thread.start_new_thread(startpy, (mxd_file_path,))
    except:
        print "Error: unable to start thread"
    return '正在发布服务'


# 远程文件发布服务
@app.route('/publish_by_sendfile',methods=['POST'])
def send_file():
    data = request.values
    mxd_name=data.get('mxd_name')
    mxd_name=str(mxd_name)
    # mxd_name=request.json.get('mxd_name')
    uploaded_files = request.files.getlist("file")
    mxd_file=create_mxd(mxd_name)


    shp_path='upload/'+mxd_name+'_'+str(uuid.uuid1())  # 本次上传的shp和tif文件夹的路径
    os.mkdir(shp_path)
    new_lst=[]
    shp_lst=[]
    tif_lst=[]
    prj_path=''

    filenames = []
    error_filenames = []
    # 存储对应的文件到相应的目录，并找到shp，tif，prj文件
    for file in uploaded_files:
        # if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
        suffix = os.path.splitext(file.filename)[-1]  # 获取文件后缀（扩展名）
        name = file.filename.split('.',1)[0]  # 获取文件后缀（扩展名）
        if name in new_lst:
            path=shp_path+'/'+name+'/'+file.filename
            if suffix=='.shp':
                shp_lst.append(path)
            if suffix=='.prj':
                prj_path=path
            if suffix=='.tif':
                tif_lst.append(path)
            file.save(path)
        else:
            path=shp_path+'/'+name
            os.mkdir(path)
            new_lst.append(name)
            path = shp_path + '/' + name + '/' + file.filename
            if suffix=='.shp':
                shp_lst.append(path)
            if suffix=='.prj':
                prj_path=path
            if suffix=='.tif':
                tif_lst.append(path)
            file.save(path)

        filenames.append(file.filename)
        # else:  # 文件后缀不符合
        #     error_filenames.append(file.filename)

    if error_filenames:  # 有文件上传失败的情况
        result = {
            'code': 200,
            'result': 'failure',
            'message': ",".join(error_filenames)
        }
        return result

# 重写mxd文件
    for path in shp_lst:
        rewrite_mxd(mxd_file,path)
    for path in tif_lst:
        rewrite_mxd_tif(mxd_file,path,prj_path)


    # 发布服务
    try:
        '''改为当前项目文件夹地址'''
        mxd_path='C:/Users/86139/PycharmProjects/myArcgis/mxd_Dir/'+mxd_file
        thread.start_new_thread(startpy, (mxd_path,))
    except:
        print "Error: unable to start thread"
    return {
        'code':200,
        'messsge':"文件正在发布",
    }

# 测试
@app.route('/test',methods=["GET"])
def test():
    t=test.rsplit('/', 1)
    print(str(t[0]))
    return ''

if __name__ == '__main__':
    app.run(port=5555)
