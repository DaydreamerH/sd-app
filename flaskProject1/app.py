from table import User, Like
from table import Img, Comment
from table import app
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from sqlalchemy.orm import aliased
from flask import request
import os
from table import db
from sqlalchemy import func
from table import bcrypt
from table import CommentInfo
from PIL import Image


key = b'daydreamerhpy114'
iv = b'openliedownaaaaa'

def decryptPassword(ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(base64.b64decode(ciphertext))
    plaintext = unpad(decrypted, AES.block_size).decode('utf-8')
    return plaintext



## 路由
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello ！'


## 注册账户
@app.route('/user/register', methods=['POST'])
def register():
    data = request.get_json()
    data['secret'] = decryptPassword(data['secret'])
    data['secret'] = bcrypt.generate_password_hash(data['secret'])
    user = User(uid=data["uid"], uname=data["uname"], secret=data['secret'])
    db.session.add(user)
    db.session.commit()
    db.session.close()
    return "success"


## 登录
@app.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    c_uid = data['uid']
    c_secret = data['secret']
    c_secret = decryptPassword(c_secret)
    user = User.query.filter_by(uid=c_uid).first()
    db.session.close()
    if bcrypt.check_password_hash(user.secret,c_secret):
        return 'success'
    return 'error'

@app.route('/user/getU_info',methods=['POST'])
def getU_info():
    uid = request.get_json()
    u_info = db.session.query(User.uname, User.sign, User.avatar).filter_by(uid=uid).first()
    u_info = {
        "uname": u_info.uname,
        "avatar": u_info.avatar,
        "sign": u_info.sign
    }
    work_num = db.session.query(Img.iid).filter(Img.uid == uid).count()
    like_num = db.session.query(Like.iid).filter(Like.uid == uid).count()
    be_liked_num = db.session.query(Like.uid, Like.iid).join(Img, Img.iid == Like.iid).filter(Img.uid == uid).count()
    result={
        "work_num": work_num,
        "like_num": like_num,
        "be_liked_num": be_liked_num,
        "u_info":u_info
    }
    return result

## 获取用户信息
@app.route('/user/getInfo', methods=['POST'])
def getInfo():
    data = request.get_json()
    uid = data['uid']
    per_page = data['per_page']

    u_info = db.session.query(User.uname,User.sign,User.avatar).filter_by(uid = uid).first()
    u_info = {
        "uname":u_info.uname,
        "avatar":u_info.avatar,
        "sign":u_info.sign
    }
    work_num = db.session.query(Img.iid).filter(Img.uid == uid).count()
    like_num = db.session.query(Like.iid).filter(Like.uid == uid).count()
    be_liked_num = db.session.query(Like.uid,Like.iid).join(Img,Img.iid == Like.iid).filter(Img.uid==uid).count()

    query = db.session.query(Img.iid, Img.prev_source, Img.title).filter_by(uid=uid).order_by(Img.iid.desc())
    img_list = []
    max_iid = 0
    if len(query.all())!=0:
        max_iid = query.first().iid
        my_list = query.paginate(page=1, per_page=per_page)
        for img in my_list:
            img_dict = {
                "source": img.prev_source,
                "title": img.title,
                "iid": img.iid
            }
            img_list.append(img_dict)
        result = {
            "my_list": img_list,
            "max_iid":max_iid,
            "u_info":u_info,
            "total_pages":my_list.pages,
            "work_num":work_num,
            "like_num":like_num,
            "be_liked_num":be_liked_num
        }
    else:
        result = {
            "my_list": [],
            "max_iid": 0,
            "u_info": u_info,
            "total_pages": 0,
            "work_num": 0,
            "like_num": like_num,
            "be_liked_num": 0
        }
    return result


## 修改信息
@app.route('/user/upInfo', methods=['POST'])
def upInfo():
    data = request.get_json()
    c_uid = data['uid']
    c_secret = data['secret']
    c_secret = decryptPassword(c_secret)
    c_uname = data['uname']
    c_sign = data['sign']
    user = User.query.filter_by(uid=c_uid).first()
    if bcrypt.check_password_hash(user.secret,c_secret)==False:
        return 'error'
    user.uname = c_uname
    user.sign = c_sign
    db.session.commit()
    db.session.close()
    return 'success'


## 上传用户头像
@app.route('/user/upAvatar', methods=['POST'])
def upAvatar():
    # 判断用户
    c_uid = request.form.get('uid')
    c_secret = request.form.get('secret')
    c_secret = decryptPassword(c_secret)
    user = User.query.filter_by(uid=c_uid).first()
    if bcrypt.check_password_hash(user.secret,c_secret)==False:
        return 'error'

    # 取出相应路径
    folder_path = "/home/hupeiyu/apache-tomcat-9.0.78/webapps/upload/" + c_uid + '/avatar/'
    # 不存在则创建
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # 存在则清空其文件
    else:
        for fname in os.listdir(folder_path):
            fp = os.path.join(folder_path, fname)
            if os.path.isfile(fp):
                os.remove(fp)

    avatar = request.files.get('avatar')
    file_name = avatar.filename.replace(" ", "")
    file_path = folder_path + file_name
    url = "http://localhost:8080/upload/" + c_uid + '/avatar/' + file_name
    user.avatar = url
    db.session.commit()
    db.session.close()
    avatar.save(file_path)
    print(url)
    return url


## 上传图像作品
@app.route('/img/upload', methods=['POST'])
def upload_img():
    ## 用户检查
    c_uid = request.form.get('uid')
    c_secret = request.form.get('secret')
    c_secret = decryptPassword(c_secret)
    user = User.query.filter_by(uid=c_uid).first()
    if bcrypt.check_password_hash(user.secret, c_secret) == False:
        return '来骗，来偷袭？'
    ## 处理文件
    img = request.files.get('work')
    folder_path = "/home/hupeiyu/apache-tomcat-9.0.78/webapps/upload/" + c_uid + '/works/'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_name = img.filename.replace(" ", "")
    file_path = folder_path + file_name
    img.save(file_path)
    ## 降低分辨率
    with Image.open(file_path) as img_obj:
        img = Image.open(file_path)
        width = int(img.size[0] * 0.5)
        height = int(img.size[0] * 0.5)
        type = img.format
        out_img = img.resize((width, height), Image.ANTIALIAS)
        folder_path = "/home/hupeiyu/apache-tomcat-9.0.78/webapps/upload/" + c_uid + '/prev-works/'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = folder_path + file_name
        out_img.save(file_path, type)
    ## 上传数据库
    c_title = request.form.get('title')
    c_prompt = request.form.get('prompt')
    c_n_prompt = request.form.get('n_prompt')
    c_tag = request.form.get('tag')
    url = "http://localhost:8080/upload/" + c_uid + '/works/' + file_name
    prev_url="http://localhost:8080/upload/" + c_uid + '/prev-works/' + file_name
    img = Img(uid=c_uid, source=url, title=c_title, tag=c_tag, prompt=c_prompt, n_prompt=c_n_prompt,prev_source = prev_url)
    db.session.add(img)
    db.session.commit()
    db.session.close()
    return 'success'

@app.route('/img/select',methods=['POST'])
def ImgSelect():
    data = request.get_json()
    rule = data['rule']
    img_list = []
    if rule == 'like':
        prev_imgs = ((
            db.session.query(Img.title, Img.prev_source, Img.iid,Img.tag,func.count(Like.iid).label('like_num'),User.uname.label('uname'))
            .outerjoin(Like, Img.iid == Like.iid)
            .group_by(Img.iid)
            .order_by(func.count(Like.iid).desc(),Img.time.desc()))
            .outerjoin(User,User.uid == Img.uid)
            .limit(10)
            .all())
        for img in prev_imgs:
            img_dict = {
                'title': img.title,
                'source': img.prev_source,
                'iid': img.iid,
                'tag': img.tag,
                'like_num':img.like_num,
                'uname':img.uname
            }
            img_list.append(img_dict)
    else :
        page = data['page']
        per_page = data['per_page']
        if page==1:
            query = db.session.query(Img.title, Img.prev_source, Img.iid).order_by(Img.iid.desc())
            iid = query.first().iid
            hot_imgs = (
                    db.session.query(Img.title, Img.prev_source, Img.iid).outerjoin(Like, Img.iid == Like.iid).group_by(Img.iid)
                    .order_by(func.count(Like.iid).desc(), Img.time.desc()).limit(3).all())
        else :
            iid = data['iid']
            query = db.session.query(Img.title, Img.prev_source, Img.iid).filter(Img.iid <= iid).order_by(Img.iid.desc())
        prev_imgs = query.paginate(page=page, per_page=per_page)
        for img in prev_imgs:
            img_dict = {
                'title': img.title,
                'source': img.prev_source,
                'iid': img.iid
            }
            img_list.append(img_dict)
    # if page ==1:
    #     max_iid = db.session.query(Img).order_by(Img.iid.desc()).first().iid
    #     if rule=='time':
    #         per_page = data['per_page']
    #         page = data['page']
    #         query = db.session.query(Img.title, Img.source, Img.iid).order_by(Img.iid.desc())
    #         prev_imgs = query.paginate(page=page, per_page=per_page)
    #         hot_imgs = (
    #             db.session.query(Img.title, Img.source, Img.iid).outerjoin(Like, Img.iid == Like.iid).group_by(Img.iid)
    #             .order_by(func.count(Like.iid).desc(), Img.time.desc()).limit(3).all())
    #     else :
    #         prev_imgs = (db.session.query(Img.title,Img.source,Img.iid).outerjoin(Like,Img.iid == Like.iid).group_by(Img.iid)
    #                 .order_by(func.count(Like.iid).desc(),Img.time.desc())).limit(10).all()
    # else :
    #     iid=data['iid']
    #     if rule == 'time':
    #         query = db.session.query(Img.title, Img.source, Img.iid).filter(Img.iid<=iid).order_by(Img.iid.desc())
    #         prev_imgs = query.paginate(page=page, per_page=per_page)
    #     else:
    #         prev_imgs = (db.session.query(Img.title, Img.source, Img.iid).filter(Img.iid<=iid).outerjoin(Like, Img.iid == Like.iid).group_by(Img.iid)
    #                  .order_by(func.count(Like.iid).desc(), Img.time.desc())).limit(10).all()

    db.session.close()

    result = {
        'prev_imgs': img_list
    }

    if rule == 'time':
        result['total_pages'] = prev_imgs.pages
        result['current_page'] = prev_imgs.page
        result['total'] = prev_imgs.total
        if page == 1:
            hot_list = []
            for img in hot_imgs:
                img_dict = {
                    "title": img.title,
                    "image": img.prev_source,
                    "iid": img.iid
                }
                hot_list.append(img_dict)
            result['hot_imgs'] = hot_list
            result['iid'] = iid
    if 'uid' in data:
        info_num = db.session.query(CommentInfo).filter_by(uid=data['uid']).count()
        result['info_num'] = info_num
    else :
        result['info_num'] = 0
    return result

## 分类查图像
@app.route('/img/select_tag',methods=['POST'])
def ImgSelectTag():
    data = request.get_json()
    tag = data['tag']
    rule = data['rule']
    img_list=[]
    if rule=='like':
        prev_imgs = ((db.session.query(Img.title, Img.prev_source, Img.iid, Img.tag,func.count(Like.iid).label('like_num'), User.uname.label('uname'))
                    .filter_by(tag=tag)
                    .outerjoin(Like, Img.iid == Like.iid)
                    .group_by(Img.iid)
                    .order_by(func.count(Like.iid).desc(), Img.time.desc()))
                    .outerjoin(User, User.uid == Img.uid)
                    .limit(10)
                    .all())
        for img in prev_imgs:
            img_dict = {
                'title': img.title,
                'source': img.prev_source,
                'iid': img.iid,
                'tag': img.tag,
                'like_num': img.like_num,
                'uname': img.uname
            }
            img_list.append(img_dict)
    else :
        page = data['page']
        per_page = data['per_page']
        if page == 1:
            query = db.session.query(Img.title, Img.prev_source, Img.iid).filter_by(tag=tag).order_by(Img.iid.desc())
            iid = db.session.query(Img).order_by(Img.iid.desc()).first().iid
            hot_imgs = (db.session.query(Img.title, Img.prev_source, Img.iid).filter_by(tag=tag).
                        outerjoin(Like, Img.iid == Like.iid).group_by(
                Img.iid).order_by(func.count(Like.iid).desc(), Img.time.desc()).limit(3).all())
        else :
            iid = data['iid']
            query = db.session.query(Img.title, Img.prev_source, Img.iid).filter(Img.tag == tag, Img.iid <= iid).order_by(
                Img.iid.desc())
        prev_imgs = query.paginate(per_page=per_page,page=page)
        for img in prev_imgs:
            img_dict = {
                'title': img.title,
                'source': img.prev_source,
                'iid': img.iid
            }
            img_list.append(img_dict)

    # if page == 1:
    #     if rule=='time':
    #         query = db.session.query(Img.title, Img.source, Img.iid).filter_by(tag = tag).order_by(Img.iid.desc())
    #     else :
    #         query = (db.session.query(Img.title, Img.source, Img.iid).filter_by(tag=tag).outerjoin(Like,
    #             Like.iid == Img.iid).group_by(Img.iid).order_by(func.count(Like.iid).desc(),Img.time.desc()))
    #     hot_imgs = (db.session.query(Img.title, Img.source, Img.iid).filter_by(tag=tag).
    #                 outerjoin(Like,Img.iid == Like.iid).group_by(
    #         Img.iid).order_by(func.count(Like.iid).desc(), Img.time.desc()).limit(3).all())
    #     max_iid = db.session.query(Img).order_by(Img.iid.desc()).first().iid
    #
    # else :
    #     iid = data['iid']
    #     if rule == 'time':
    #         query = db.session.query(Img.title, Img.source, Img.iid).filter(Img.tag==tag,Img.iid<=iid).order_by(Img.iid.desc())
    #     else :
    #         query = (db.session.query(Img.title, Img.source, Img.iid).filter_by(tag=tag).filter(Img.iid<=iid).outerjoin(Like,
    #             Like.iid == Img.iid).group_by(Img.iid).order_by(func.count(Like.iid).desc(), Img.time.desc()))
    result = {
        'prev_imgs': img_list
    }

    if rule=='time':
        result['total_pages'] = prev_imgs.pages
        result['total'] = prev_imgs.total
        result['current_page'] = prev_imgs.page
        if page == 1:
            hot_list = []
            for img in hot_imgs:
                img_dict = {
                    "title": img.title,
                    "image": img.prev_source,
                    "iid": img.iid
                }
                hot_list.append(img_dict)
            result['hot_imgs'] = hot_list
            result['iid'] = iid

    if 'uid' in data:
        info_num = db.session.query(CommentInfo).filter_by(uid=data['uid']).count()
        result['info_num'] = info_num
    db.session.close()
    return result

## 图像详情页展示
@app.route('/img/show',methods=['POST'])
def showImg():
    data = request.get_json()
    uid = data['uid']
    iid = data['iid']
    per_page = data['per_page']
    query1 = db.session.query(Img, User).join(User,Img.uid == User.uid).filter(Img.iid == iid).first()
    like_num = db.session.query(Like).filter_by(iid = iid).count()

    query2 = (db.session.query(Comment, User)
              .join(User, Comment.uid == User.uid)
              .filter(Comment.iid == iid,Comment.pcid==None)
              .order_by(Comment.cid.desc()))
    query2 = query2.paginate(page = 1,per_page = per_page)
    like_state = db.session.query(Like).filter_by(uid = uid,iid = iid).count()
    if query1:
        img, user = query1
        com_list=[]
        if query2:
            for com,user in query2:
                com_dict={
                    "uname":user.uname,
                    "avatar":user.avatar,
                    "uid":user.uid,
                    "time":com.time,
                    "text":com.text,
                    "cid":com.cid
                }
                query3 = (db.session.query(Comment, User)
                          .join(User, Comment.uid == User.uid)
                          .filter(Comment.iid == iid, Comment.pcid == com_dict['cid'])
                          .order_by(Comment.cid.desc())).all()
                if query3:
                    reply_list=[]
                    for reply_com,reply_user in query3:
                        reply_dict={
                            "uname": reply_user.uname,
                            "avatar": reply_user.avatar,
                            "uid": reply_user.uid,
                            "time": reply_com.time,
                            "text": reply_com.text,
                            "cid": reply_com.cid
                        }
                        reply_list.append(reply_dict)
                    com_dict['reply_list'] = reply_list

                com_list.append(com_dict)
        result = {
            "source":img.source,
            "prompt":img.prompt,
            "n_prompt":img.n_prompt,
            "img_time":img.time,
            "tag":img.tag,
            "title":img.title,
            "user_uid":img.uid,
            "painter_uname":user.uname,
            "painter_avatar":user.avatar,
            "painter_sign":user.sign,
            "painter_uid":user.uid,
            "like_num":like_num,
            "com_list":com_list,
            "like_state":like_state,
            "total_compage":query2.pages
        }

        db.session.close()
        return result
    else:
        db.session.close()
        return 'error'

@app.route('/like/insert',methods=['POST'])
def likeInsert():
    data = request.get_json()
    uid = data['uid']
    secret = data['secret']
    secret = decryptPassword(secret)
    iid = data['iid']
    user = User.query.filter_by(uid=uid).first()
    state = db.session.query(Like).filter_by(uid=uid,iid=iid).count()
    if bcrypt.check_password_hash(user.secret,secret)==False or state== 1:
        return '来骗，来偷袭？'
    like = Like(iid = iid,uid = uid)
    db.session.add(like)
    db.session.commit()
    db.session.close()
    return 'success'

@app.route('/like/delete',methods=['POST'])
def likeDel():
    data = request.get_json()
    uid = data['uid']
    secret = data['secret']
    secret = decryptPassword(secret)
    iid = data['iid']
    user = User.query.filter_by(uid=uid).first()
    like = db.session.query(Like).filter_by(uid=uid, iid=iid).first()
    if bcrypt.check_password_hash(user.secret,secret)==False or like == None:
        return '来骗，来偷袭？'
    db.session.delete(like)
    db.session.commit()
    db.session.close()
    return 'success'

@app.route('/comment/insert',methods=['POST'])
def commentInsert():
    data = request.get_json()
    iid = data['iid']
    uid = data['uid']
    secret = data['secret']
    secret = decryptPassword(secret)
    text = data['text']

    user = User.query.filter_by(uid = uid).first()
    if bcrypt.check_password_hash(user.secret,secret)==False:
        return '来骗，来偷袭？'

    if 'pcid' in data:
        pcid = data['pcid']
        comment = Comment(uid=uid,iid=iid,text=text,pcid=pcid)

    else :
        comment = Comment(uid=uid,iid=iid,text=text)
    db.session.add(comment)

    query2 = (db.session
              .query(Comment, User)
              .join(User, Comment.uid == User.uid)
              .filter(Comment.iid == iid,User.uid == uid)
              .order_by(Comment.cid.desc()).first())
    com,user = query2
    com_dict = {
        "uname": user.uname,
        "avatar": user.avatar,
        "uid": user.uid,
        "time": com.time,
        "text": com.text,
        "cid": com.cid
    }
    if 'pcid' in data:
        com_dict['pcid']=pcid

    info_cid = com_dict['cid']
    info_uid = db.session.query(Img.uid).filter_by(iid=iid).scalar()
    info = CommentInfo(uid=info_uid, cid=info_cid)
    db.session.add(info)

    if 'pcid' in data:
        info_uid_again = db.session.query(Comment.uid).filter_by(cid=pcid).scalar()
        if info_uid_again!=info_uid:
            info = CommentInfo(uid=info_uid_again, cid=info_cid)
            db.session.add(info)

    db.session.commit()
    db.session.close()
    return com_dict

@app.route('/comment/select',methods=['POST'])
def commentSelect():
    data = request.get_json()
    iid = data['iid']
    page = data['page']
    per_page = data['per_page']
    if page != 1:
        cid = data['cid']
        query2 = db.session.query(Comment, User).join(User, Comment.uid == User.uid).filter(Comment.iid == iid,
                                                                                            Comment.cid<=cid,Comment.pcid==None).order_by(
        Comment.cid.desc())
    else :
        query2 = db.session.query(Comment, User).join(User, Comment.uid == User.uid).filter(Comment.iid == iid,Comment.pcid==None).order_by(
            Comment.cid.desc())
    coms = query2.paginate(page = page,per_page = per_page)
    com_list = []
    for com,user in coms:
        com_dict = {
            "uname": user.uname,
            "avatar": user.avatar,
            "uid": user.uid,
            "time": com.time,
            "text": com.text,
            "cid": com.cid
        }
        query3 = (db.session.query(Comment, User)
                  .join(User, Comment.uid == User.uid)
                  .filter(Comment.iid == iid, Comment.pcid == com_dict['cid'])
                  .order_by(Comment.cid.desc())).all()
        if query3:
            reply_list = []
            for reply_com, reply_user in query3:
                reply_dict = {
                    "uname": reply_user.uname,
                    "avatar": reply_user.avatar,
                    "uid": reply_user.uid,
                    "time": reply_com.time,
                    "text": reply_com.text,
                    "cid": reply_com.cid
                }
                reply_list.append(reply_dict)
            com_dict['reply_list'] = reply_list
        com_list.append(com_dict)

    comments = {
        'total_pages': coms.pages,
        'total_items': coms.total,
        'current_page': coms.page,
        'com_list': com_list
    }
    db.session.close()
    return comments

@app.route('/img/select_con',methods=['POST'])
def selectCon():
    data = request.get_json()
    page = data['page']
    per_page = data['per_page']
    con = data['con']
    if page == 1:
        query = (db.session.query(Img.title, Img.prev_source, Img.iid)
                 .filter(Img.title.like('%'+con+'%')).order_by(Img.iid.desc()))
        if query.count() == 0:
            result = {
                "img_list": [],
                'total_pages': 0,
                'total_items': 0
            }
            return result
        max_iid = db.session.query(Img).filter(Img.title.like('%'+con+'%')).order_by(Img.iid.desc()).first().iid
    else:
        iid = data['iid']
        query = (db.session.query(Img.title, Img.prev_source, Img.iid)
                 .filter(Img.title.like('%' + con + '%'),Img.iid<=iid).order_by(Img.iid.desc()))
    query = query.paginate(per_page=per_page,page=page)
    img_list=[]
    for img in query:
        img_dict={
            "title": img.title,
            "source": img.prev_source,
            "iid": img.iid
        }
        img_list.append(img_dict)
    result={
        "img_list":img_list,
        'total_pages':query.pages,
        'total_items':query.total
    }
    if page==1:
        result['max_iid'] = max_iid
    db.session.close()

    return result


# @app.route('/com/insert_com',methods=['POST'])
# def comInsertCom():
#     data = request.get_json()
#     iid = data['iid']
#     uid = data['uid']
#     secret = data['secret']
#     secret = decryptPassword(secret)
#     text = data['text']
#     pcid = data['pcid']
#
#     user = User.query().filter_by(uid = uid).first()
#     if bcrypt.check_password_hash(user.secret,secret) == False:
#         return '来骗？来偷袭？'
#     comment = Comment(iid = iid,pcid = pcid,text = text,uid = uid)
#     db.session.add(comment)
#
#     query2 = db.session.query(Comment, User).join(User, Comment.uid == User.uid).filter(Comment.iid == iid,
#                                                                                         User.uid == uid).order_by(
#         Comment.cid.desc()).first()
#     com, user = query2
#     com_dict = {
#         "uname": user.uname,
#         "avatar": user.avatar,
#         "uid": user.uid,
#         "time": com.time,
#         "text": com.text,
#         "cid": com.cid,
#         "pcid":com.pcid
#     }
#     db.session.commit()
#     db.session.close()
#
#     return com_dict

@app.route('/img/select_my',methods=['POST'])
def selectMyImg():
    data = request.get_json()
    uid = data['uid']
    page = data['page']
    per_page = data['per_page']
    get_type = data['get_type']

    if get_type=='own':
        if page==1:
            query = db.session.query(Img.iid,Img.prev_source,Img.title).filter_by(uid=uid).order_by(Img.iid.desc())
            if len(query.all())==0:
                result={
                    "my_list":[],
                    "total_pages":0
                }
                return result
            max_iid = query.first().iid
        else:
            max_iid = data['max_iid']
            query = db.session.query(Img.iid,Img.prev_source,Img.title).filter_by(uid=uid).filter(Img.iid <= max_iid).order_by(Img.iid.desc())
    else:
        if page==1:
            query = db.session.query(Img.iid,Img.prev_source,Img.title).join(Like,Like.iid==Img.iid).filter(Like.uid==uid).order_by(Img.iid.desc())
            if len(query.all())==0:
                result={
                    "my_list":[],
                    "total_pages":0
                }
                return result
            max_iid = query.first().iid
        else:
            max_iid = data['max_iid']
            query = db.session.query(Img.iid,Img.source,Img.title).join(Like,Like.iid==Img.iid).filter(Like.uid==uid,Img.iid<=max_iid).order_by(Img.iid.desc())

    my_list = query.paginate(page=page,per_page=per_page)
    img_list=[]
    for img in my_list:
        img_dict={
            "source":img.prev_source,
            "title":img.title,
            "iid":img.iid
        }
        img_list.append(img_dict)

    result = {
        "my_list":img_list,
        "total_pages":my_list.pages
    }

    if page==1:
        result['max_iid'] = max_iid
    return result

@app.route('/info/get',methods=['POST'])
def GetInfo():
    uid = request.get_data()

    query = (db.session
             .query(Comment.text,Comment.cid,User.uname,User.avatar,Img.title,Img.iid)
             .join(CommentInfo,CommentInfo.cid == Comment.cid)
             .join(User,Comment.uid == User.uid)
             .join(Img,Comment.iid==Img.iid)
             .filter(CommentInfo.uid == uid)
             .all())
    info_list = []
    if query:
        for info in query:
            info_dict = {
                'avatar':info.avatar,
                'uname':info.uname,
                'text':info.text,
                'title':info.title,
                'cid':info.cid,
                'iid':info.iid
            }
            info_list.append(info_dict)
    db.session.close()
    return info_list

@app.route('/info/delete_one',methods=['POST'])
def InfoDeleteOne():
    data = request.get_json()
    uid = data['uid']
    secret = data['secret']
    secret = decryptPassword(secret)
    secret_real = db.session.query(User.secret).filter_by(uid= uid).scalar()
    if bcrypt.check_password_hash(secret_real,secret)==False:
        return '来骗，来偷袭？'
    cid = data['cid']
    info = CommentInfo.query.filter_by(uid=uid,cid=cid).first()
    db.session.delete(info)
    db.session.commit()

    return 'success'

@app.route('/img/delete',methods=['POST'])
def DelImg():
    data = request.get_json()
    uid = data['uid']
    secret = data['secret']
    secret = decryptPassword(secret)
    secret_real = db.session.query(User.secret).filter_by(uid = uid).scalar()

    if bcrypt.check_password_hash(secret_real,secret)==False:
        return '来骗，来偷袭？'

    iid = data['iid']
    img = db.session.query(Img).filter_by(iid=iid,uid=uid).first()

    url = img.source
    file_name = '/'.join(url.split('/')[4:])
    folder_path = "/home/hupeiyu/apache-tomcat-9.0.78/webapps/upload/"
    file_path = folder_path+file_name

    if os.path.exists(file_path):
        os.remove(file_path)
    url = img.prev_source
    file_name = '/'.join(url.split('/')[4:])
    file_path = folder_path+file_name
    if os.path.exists(file_path):
        os.remove(file_path)
    db.session.delete(img)
    db.session.commit()
    return 'success'


if __name__ == '__main__':
    app.run('',port="3689",debug=True)


