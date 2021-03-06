from flask import Blueprint,request,render_template
from flask import current_app
import json
import os
from libs import login_required
upload_app = Blueprint("upload",__name__)


@upload_app.before_request
@login_required
def is_login():
    pass

@upload_app.route("/",methods=['get','post'])
def upload():
    if request.method == "POST":
        file_storage_list = request.files.getlist("file")
        message = {"result":"","error":"","filepath_list":[]}
        for file_storage in file_storage_list:
    # 如果上传文件大于300kb，则失败，我们一定要在一开始就判断不然文件已经被接受了才会有类型之类的参数
            if request.content_length > 300 * 1000:
                message['result']="fail"
                message['error']="上传文件太大"
                return json.dumps(message)
    # 上传类型
            print(file_storage.content_type)
    # 如果上传类型不在允许的类型内，则返回403错误
            if file_storage.content_type not in current_app.config['ALLOW_UPLOAD_TYPE']:
                message['result'] = "fail"
                message['error'] = "上传文件类型不对"
                return json.dumps(message)

    # 上传文件原名
            print(file_storage.filename)
    # 文件域名
            print(file_storage.name)
    # 使用保存
            file_path = os.path.join(get_dir(),create_filename(file_storage.filename))
            print("file_path:",file_path)
            try:
                file_storage.save(file_path)
            except Exception as e:
                message = {"result":"fail","error":str(e)}
                return json.dumps(message)
            # [1:]将.static/相对路径转为/static绝对路径
            print("file_path[1:]",file_path[1:])
            message['filepath_list'].append(file_path[1:])
        message['result'] = "success"
        return json.dumps(message)
    return render_template("upload/jquery_upload.html")

# 从ckeditor上传文件：
@upload_app.route("/ckeditor",methods=['post'])
def ckeditor_upload():
    if request.method == "POST":
        file_storage = request.files.get("upload")
        message = {
            "uploaded":"0",
            "fileName":"",
            "url" : "",
            "error":{
                "message":""
            }
        }
        if request.content_length>300*1000:
            message['upload'] = "0"
            message['error']['message'] = "上传文件太大"
            return json.dumps(message)
        if file_storage.content_type not in current_app.config['ALLOW_UPLOAD_TYPE']:
            message['uploaded'] = "0"
            message['error']['message']="上传文件类型不对"
            return json.dumps(message)
        file_path = os.path.join(get_dir(),create_filename(file_storage.filename))
        try:
            file_storage.save(file_path)
        except Exception as e:
            message={"uploaded":"0","error":str(e)}
            return json.dumps(message)
        message['fileName'] = file_storage.filename
        message['url']=file_path[1:]
        message['loaded']="1"
        return json.dumps(message)


@upload_app.route("/ckeditor/browser",methods=['get'])
def ckeditor_browser():
    images = []
    for dirpath,dirnames,filenames in os.walk("./static/uploads"):
        print(dirpath,dirnames,filenames)
        for file in filenames:
            images.append(os.path.join(dirpath[1:],file))
    return render_template("upload/browser.html",images=images)






def get_dir():
    """
    生成文件存放路径
    """
    from datetime import date
    base_path = "./static/uploads/"
    d = date.today()
    path = os.path.join(base_path,str(d.year),str(d.month),str(d.day))
    print(path)
    if os.path.exists(path) is False:
        try:
            os.makedirs(path)
        except Exception as e:
            path = base_path
            print(e)
    return path

def create_filename(filename):
    import uuid
    ext = os.path.splitext(filename)[1]
    new_file_name = str(uuid.uuid4())+ext
    return new_file_name

