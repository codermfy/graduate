# coding: utf-8
import pymysql
from flask import Flask,request,jsonify,json,session,make_response,Response,render_template
from flask_cors import CORS,cross_origin
from random import Random
import hashlib
import os
import uuid
import datetime
import time

db = pymysql.connect("127.0.0.1","root","ma1272006711","graduate")
cursor = db.cursor()
ipv4='http://192.168.3.31:8000'
app = Flask(__name__,static_url_path='/',static_folder='./../../design for graduate/code/dist', template_folder='./../../design for graduate/code/dist')
CORS(app, resources=r'/*')
app.secret_key = '\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'
# 获取随机token
def get_token():
    length_r = 32
    token = ''
    chars = '0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(length_r):
        token += chars[random.randint(0, length)]
    return token
def check_token(token):
    if token==session['token']:
        return True
    return False
# md5加密
def md5val(key):
    input_name = hashlib.md5()
    input_name.update(key.encode("utf-8"))
    return input_name.hexdigest()
def textencode(txt):
    return (txt.replace("\"", "'")).replace(ipv4, 'http:address')
def textuncode(txt):
    return (txt.replace('http:address', ipv4)).replace("\'", "\"")
# 学生登录
def login_st(username,password,isforget=False):
    if not isforget:
        cursor.execute('select * from students where STID="'+username+'" and Password="'+password+'" AND isused=1')
    else:
        cursor.execute('select * from students where STID="'+username+'" and CardNo="'+password+'" AND isused=1')
    result = cursor.fetchall()
    if result:
        session['name']=result[0][1]
        return True
    else:
        return False
# 老师登录
def login_te(username,password,isforget=False):
    if not isforget:
        cursor.execute('select * from teachers where TEID="'+username+'" and Password="'+password+'" AND isused=1')
    else:
        cursor.execute('select * from teachers where TEID="'+username+'" and CardNo="'+password+'" AND isused=1')
    result = cursor.fetchall()
    if result:
        session['name']=result[0][1]
        return True
    else:
        return False
# 管理员登录
def login_ad(username,password,isforget=False):
    if not isforget:
        cursor.execute('select * from admins where Account="'+username+'" and Password="'+password+'" AND isused=1')
    else:
        cursor.execute('select * from admins where Account="'+username+'" and CardNo="'+password+'" AND isused=1')
    result = cursor.fetchall()
    if result:
        session['name']=result[0][3]
        session['username']=result[0][1]
        return True
    else:
        return False
def resetPwd(username,cardcode,type):
    sql=''
    newpwd=md5val(str(cardcode)[-6:])
    if type=="student":
        sql='update students set Password="'+newpwd+'" where STID="'+username+'"'
    elif type=="teacher":
        sql='update teachers set Password="'+newpwd+'" where TEID="'+username+'"'
    else:
        sql='update admins set Password="'+newpwd+'" where Account="'+username+'"'
    try:
        cursor.execute(sql)
        db.commit()
        return 'success'
    except Exception as e:
        db.rollback()
        return 'fail'
def ad_resetPwd(username,type):
    sql=''
    if type=="student":
        sql='select CardNo from students where STID="'+username+'"'
    elif type=="teacher":
        sql='select CardNo from teachers where TEID="'+username+'"'
    else:
        sql='select CardNo from admins where Account="'+username+'"'
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        cardcode=result[0][0]
        return resetPwd(username,cardcode,type)
    else:
        return 'No user'
def deluser(username,type):
    sql=''
    if type=="student":
        sql='update students set isused=0 where STID="'+username+'"'
    elif type=="teacher":
        sql='update admins set isused=0 where TEID="'+username+'"'
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            db.rollback()
            return 'fail'
        sql='update classes set TEID="" where TEID="'+username+'"'
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            db.rollback()
            return 'fail'
        sql='update teachers set isused=0 where TEID="'+username+'"'
    elif type=='admin':
        sql='update admins set isused=0 where Account="'+username+'"'
    elif type=='class':
        sql='update students set ClassNo=null where ClassNo="'+username+'"'
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            db.rollback()
            return 'fail'
        sql='update classes set isused=0 where ClassNo="'+username+'"'
    elif type=='exdemo':
        sql='update exdemos set isused=0 where ID='+username+''
    elif type=='exgood':
        admin=session['username']
        sql='update exgoods set isused=0,charge="'+admin+'" where ID='+username+''
    elif type=='project':
        sql='update experiments set isused=0 where EXPID='+username+''
    try:
        cursor.execute(sql)
        db.commit()
        return 'success'
    except Exception as e:
        db.rollback()
        return 'fail'
def editpassword(username,password,type):
    sql=''
    newpwd=md5val(password)
    if type=="student":
        sql='update students set Password="'+newpwd+'" where STID="'+username+'"'
    elif type=="teacher":
        sql='update teachers set Password="'+newpwd+'" where TEID="'+username+'"'
    else:
        sql='update admins set Password="'+newpwd+'" where Account="'+username+'"'
    try:
        cursor.execute(sql)
        db.commit()
        return 'success'
    except Exception as e:
        db.rollback()
        return 'fail'
def searchresult(query,querytype,usertype):
    sql=''
    res=[]
    i=1
    # 管理员搜索
    if usertype=='admin':
        if query=='':
            sql='select * from admins where isused=1'
        else:
            if querytype=='queryall':
                sql='select * from admins where (Account like "%'+query+'%" or Name like "%'+query+'%" or Phonenum like "%'+query+'%" or TEID like "%'+query+'%") and isused=1'
            elif querytype=="username":
                sql='select * from admins where Account="'+query+'" and isused=1'
            elif querytype=="name":
                sql='select * from admins where Name="'+query+'" and isused=1'
            elif querytype=="phonenum":
                sql='select * from admins where Phonenum="'+query+'" and isused=1'
            elif querytype=="TEID":
                sql='select * from admins where TEID="'+query+'" and isused=1'
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            for item in result:
                temp={}
                temp['currentid']=i
                i=i+1
                temp['username']=item[1]
                temp['name']=item[3]
                temp['phonenum']=item[4]
                temp['TEID']=item[5]
                res.append(temp)
    # 老师搜索
    elif usertype=='teacher':
        if query=='':
            sql='select * from teachers where isused=1'
        else:
            if querytype=='queryall':
                sql='select * from teachers where (TEname like "%'+query+'%" or Phonenum like "%'+query+'%" or TEID like "%'+query+'%") and isused=1'
            elif querytype=="name":
                sql='select * from teachers where TEname="'+query+'" and isused=1'
            elif querytype=="phonenum":
                sql='select * from teachers where Phonenum="'+query+'" and isused=1'
            elif querytype=="TEID":
                sql='select * from teachers where TEID="'+query+'" and isused=1'
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            for item in result:
                temp={}
                temp['currentid']=i
                i=i+1
                temp['TEID']=item[0]
                temp['name']=item[1]
                temp['phonenum']=item[3]
                temp['teacher']=item[1]+'---'+item[0]
                temp['cardno']=item[4]
                res.append(temp)
    # 学生搜索
    elif usertype=='student':
        if query=='':
            sql='select * from students where isused=1'
        else:
            if querytype=='queryall':
                sql='select * from students where (STname like "%'+query+'%" or ClassNo like "%'+query+'%" or STID like "%'+query+'%") and isused=1'
            elif querytype=="name":
                sql='select * from students where STname="'+query+'" and isused=1'
            elif querytype=="classno":
                sql='select * from students where ClassNo="'+query+'" and isused=1'
            elif querytype=="STID":
                sql='select * from students where STID="'+query+'" and isused=1'
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            for item in result:
                temp={}
                temp['currentid']=i
                i=i+1
                temp['STID']=item[0]
                temp['name']=item[1]
                temp['classno']=item[2]
                temp['cardno']=item[4]
                res.append(temp)
    # 班级搜索
    elif usertype=='class':
        if query=='':
            sql='select a.ClassNo,a.ClassNum,b.TEID,b.TEname from classes a left join teachers b on a.TEID=b.TEID where a.isused=1 order by a.ClassNo'
        else:
            if querytype=='queryall':
                sql='select a.ClassNo,a.ClassNum,b.TEID,b.TEname from classes a left join teachers b on a.TEID=b.TEID where (b.TEID like "%'+query+'%" or b.TEname like "%'+query+'%" or a.ClassNo like "%'+query+'%") and a.isused=1 order by a.ClassNo'
            elif querytype=="classno":
                sql='select a.ClassNo,a.ClassNum,b.TEID,b.TEname from classes a left join teachers b on a.TEID=b.TEID where a.ClassNo='+query+' and a.isused=1 order by a.ClassNo'
            elif querytype=="teacher":
                sql='select a.ClassNo,a.ClassNum,b.TEID,b.TEname from classes a left join teachers b on a.TEID=b.TEID where (b.TEID="'+query+'" or b.TEname="'+query+'") and a.isused=1 order by a.ClassNo'
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            for item in result:
                temp={}
                temp['currentid']=i
                i=i+1
                temp['classno']=item[0]
                temp['teacher']='' if item[2]==None else item[3]+'---'+item[2]
                temp['peoplenum']=getpeoplenum(item[0])
                res.append(temp)
    # 实验演示搜索
    elif usertype=='exdemo':
        if query=='':
            sql='select * from exdemos where isused=1'
        else:
            if querytype=='queryall':
                sql='select ID,title from exdemos where (ID like "%'+query+'%" or title like "%'+query+'%") and isused=1'
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            for item in result:
                temp={}
                temp['itemid']=item[0]
                temp['title']=item[1]
                res.append(temp)
    # 物品报修搜索
    elif usertype=='exgood':
        typedic={'1':'实验仪器','2':'化学药品','3':'其他'}
        result=None
        if query=='':
            sql='select * from exgoods a left join teachers b on a.TEID=b.TEID where a.isdone=0 and a.isused=1 order by a.ID desc'
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                for item in result:
                    temp={}
                    temp['fixid']=item[0]
                    temp['goodsname']=item[1]
                    temp['goodstype']=typedic.get(str(item[2]))
                    temp['goodsnum']=item[3]
                    temp['teacher']=item[11]+'---'+item[10]
                    temp['isdone']=1 if item[7]==b'\x01' else 0
                    temp['goodsdesc']=item[4]
                    temp['cost']=item[6] if item[6]!=None else ''
                    # admin=searchresult(item[8],'username','admin')
                    # temp['charge']=admin[0]['name']+'---'+admin[0]['TEID']
                    # temp['charge']=item[10]
                    res.append(temp)
            sql='select * from exgoods a left join teachers b on a.TEID=b.TEID where a.isdone=1 and a.isused=1 order by a.ID desc'
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                for item in result:
                    temp={}
                    temp['fixid']=item[0]
                    temp['goodsname']=item[1]
                    temp['goodstype']=typedic.get(str(item[2]))
                    temp['goodsnum']=item[3]
                    temp['teacher']=item[11]+'---'+item[10]
                    temp['isdone']=1 if item[7]==b'\x01' else 0
                    temp['goodsdesc']=item[4]
                    temp['cost']=item[6] if item[6]!=None else ''
                    # admin=searchresult(item[8],'username','admin')
                    # temp['charge']=admin[0]['name']+'---'+admin[0]['TEID']
                    # temp['charge']=admin
                    # temp['charge']=item[10]
                    res.append(temp)
        else:
            if querytype=='queryall':
                sql='select * from exgoods a left join teachers b on a.TEID=b.TEID where a.ID='+query+' and a.isused=1'
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    for item in result:
                        temp={}
                        temp['fixid']=item[0]
                        temp['goodsname']=item[1]
                        temp['goodstype']=typedic.get(str(item[2]))
                        temp['goodsnum']=item[3]
                        temp['teacher']=item[11]+'---'+item[10]
                        temp['isdone']=1 if item[7]==b'\x01' else 0
                        temp['goodsdesc']=item[4]
                        temp['cost']=item[6] if item[6]!=None else ''
                        # admin=searchresult(item[8],'username','admin')
                        # temp['charge']=admin[0]['name']+'---'+admin[0]['TEID']
                        # temp['charge']=admin
                        # temp['charge']=item[10]
                        res.append(temp)
            elif querytype=="TEID":
                sql='select * from exgoods a left join teachers b on a.TEID=b.TEID where a.TEID="'+query+'"  order by a.ID desc'
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    for item in result:
                        temp={}
                        temp['fixid']=item[0]
                        temp['goodsname']=item[1]
                        temp['goodstype']=typedic.get(str(item[2]))
                        temp['goodsnum']=item[3]
                        temp['teacher']=item[11]+'---'+item[10]
                        temp['isdone']=1 if item[7]==b'\x01' else 0
                        temp['goodsdesc']=item[4]
                        temp['cost']=item[6] if item[6]!=None else ''
                        temp['isused']='1' if item[9]==b'\x01' else '0'
                        if item[8]!=None:
                            admin=searchresult(item[8],'username','admin')
                            temp['charge']=admin[0]['name']+'---'+admin[0]['TEID']
                        else:
                            temp['charge']=''
                        # temp['charge']=admin
                        # temp['charge']=item[10]
                        res.append(temp)
            elif querytype=="isdone":
                sql='select * from exgoods a left join teachers b on a.TEID=b.TEID where a.TEID="'+query+'" and a.isused=1 and isdone=1 order by a.ID desc'
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    for item in result:
                        temp={}
                        temp['fixid']=item[0]
                        temp['goodsname']=item[1]
                        temp['goodstype']=typedic.get(str(item[2]))
                        temp['goodsnum']=item[3]
                        temp['teacher']=item[11]+'---'+item[10]
                        temp['isdone']=1 if item[7]==b'\x01' else 0
                        temp['goodsdesc']=item[4]
                        temp['cost']=item[6] if item[6]!=None else ''
                        temp['isused']='1'
                        if item[8]!=None:
                            admin=searchresult(item[8],'username','admin')
                            temp['charge']=admin[0]['name']+'---'+admin[0]['TEID']
                        else:
                            temp['charge']=''
                        # temp['charge']=admin
                        # temp['charge']=item[10]
                        res.append(temp)
            elif querytype=="waitdone":
                sql='select * from exgoods a left join teachers b on a.TEID=b.TEID where a.TEID="'+query+'" and a.isused=1 and isdone=0 order by a.ID desc'
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    for item in result:
                        temp={}
                        temp['fixid']=item[0]
                        temp['goodsname']=item[1]
                        temp['goodstype']=typedic.get(str(item[2]))
                        temp['goodsnum']=item[3]
                        temp['teacher']=item[11]+'---'+item[10]
                        temp['isdone']=1 if item[7]==b'\x01' else 0
                        temp['goodsdesc']=item[4]
                        temp['cost']=item[6] if item[6]!=None else ''
                        temp['isused']='1'
                        if item[8]!=None:
                            admin=searchresult(item[8],'username','admin')
                            temp['charge']=admin[0]['name']+'---'+admin[0]['TEID']
                        else:
                            temp['charge']=''
                        # temp['charge']=admin
                        # temp['charge']=item[10]
                        res.append(temp)
            elif querytype=="dontdone":
                sql='select * from exgoods a left join teachers b on a.TEID=b.TEID where a.TEID="'+query+'" and a.isused=0 order by a.ID desc'
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    for item in result:
                        temp={}
                        temp['fixid']=item[0]
                        temp['goodsname']=item[1]
                        temp['goodstype']=typedic.get(str(item[2]))
                        temp['goodsnum']=item[3]
                        temp['teacher']=item[11]+'---'+item[10]
                        temp['isdone']=1 if item[7]==b'\x01' else 0
                        temp['goodsdesc']=item[4]
                        temp['cost']=item[6] if item[6]!=None else ''
                        temp['isused']='0'
                        if item[8]!=None:
                            admin=searchresult(item[8],'username','admin')
                            temp['charge']=admin[0]['name']+'---'+admin[0]['TEID']
                        else:
                            temp['charge']=''
                        # temp['charge']=admin
                        # temp['charge']=item[10]
                        res.append(temp)
    return res
def getpeoplenum(classno):
    classno=str(classno)
    cursor.execute('select count(*) from students where ClassNo='+classno+' and isused=1')
    result = cursor.fetchall()
    if result:
        return result[0][0]
    return 0
def getuserinfo(username,usertype):
    res={}
    if usertype=='admin':
        cursor.execute('select * from admins where Account="'+username+'" and isused=1')
        result = cursor.fetchall()
        if result:
            res['username']=result[0][1]
            res['name']=result[0][3]
            res['phonenum']=result[0][4]
            res['TEID']=result[0][5]
    elif usertype=='student':
        cursor.execute('select * from students where STID="'+username+'" and isused=1')
        result = cursor.fetchall()
        if result:
            res['classno']=result[0][2]
            res['name']=result[0][1]
            res['STID']=result[0][0]
    elif usertype=='teacher':
        cursor.execute('select * from teachers where TEID="'+username+'" and isused=1')
        result = cursor.fetchall()
        if result:
            res['phonenum']=result[0][3]
            res['name']=result[0][1]
            res['TEID']=result[0][0]
    elif usertype=="class":
        cursor.execute('select b.TEID,b.TEname from classes a left join teachers b on a.TEID=b.TEID where a.ClassNo='+username+' and a.isused=1')
        result = cursor.fetchall()
        if result:
            res['teacher']='' if result[0][0]==None else result[0][1]+'---'+result[0][0]
    elif usertype=="exdemo":
        cursor.execute('select * from exdemos where ID='+username+' and isused=1')
        result = cursor.fetchall()
        if result:
            res['title']=result[0][1]
            res['steps']=result[0][2]
    return res
def setuserinfo(username,content,usertype):
    sql=''
    if usertype=="admin":
        sql='update admins set Phonenum="'+content+'" where Account="'+username+'" '
    elif usertype=='student':
        sql='update students set ClassNo="'+content+'" where STID="'+username+'" '
    elif usertype=='teacher':
        sql='update teachers set Phonenum="'+content+'" where TEID="'+username+'" '
    elif usertype=='class':
        if teacher_exist(content):
            sql='update classes set TEID="'+content+'" where ClassNo='+username+' '
        else:
            return "no teacher"
    try:
        cursor.execute(sql)
        db.commit()
        return 'success'
    except Exception as e:
        db.rollback()
        return 'fail'
def admin_username_exist(username):
    cursor.execute('select * from admins where Account="'+username+'" and isused=1')
    result = cursor.fetchall()
    if result:
        return True
    else:
        return False
def admin_teacher_exist(TEID):
    cursor.execute('select * from admins where TEID="'+TEID+'" and isused=1')
    result = cursor.fetchall()
    if result:
        return True
    else:
        return False
def teacher_exist(TEID):
    cursor.execute('select * from teachers where TEID="'+TEID+'" and isused=1')
    result = cursor.fetchall()
    if result:
        return True
    else:
        return False
def teacher_cardno_exist(cardno):
    cursor.execute('select * from teachers where CardNo="'+cardno+'" and isused=1')
    result = cursor.fetchall()
    if result:
        return True
    else:
        return False
def student_exist(STID):
    cursor.execute('select * from students where STID="'+STID+'" and isused=1')
    result = cursor.fetchall()
    if result:
        return True
    else:
        return False
def student_cardno_exist(cardno):
    cursor.execute('select * from students where CardNo="'+cardno+'" and isused=1')
    result = cursor.fetchall()
    if result:
        return True
    else:
        return False
def class_exist(classno):
    cursor.execute('select * from classes where ClassNo='+classno+' and isused=1')
    result = cursor.fetchall()
    if result:
        return True
    else:
        return False
def insert_admin(username,password,TEID):
    cursor.execute('select * from teachers where TEID="'+TEID+'" and isused=1')
    result = cursor.fetchall()
    name=result[0][1]
    phonenum=result[0][3]
    teid=result[0][0]
    cardno=result[0][4]
    try:
        cursor.execute('insert admins (Account,Password,Name,Phonenum,TEID,CardNo) values ("'+username+'","'+password+'","'+name+'","'+phonenum+'","'+teid+'","'+cardno+'")')
        db.commit()
        return 'success'
    except Exception as e:
        db.rollback()
        return 'fail'
def insert_teacher(TEID,name,phonenum,cardno):
    pwd=md5val(str(cardno)[-6:])
    try:
        cursor.execute('insert teachers (TEID,TEname,Password,Phonenum,CardNo) values ("'+TEID+'","'+name+'","'+pwd+'","'+phonenum+'","'+cardno+'")')
        db.commit()
        return 'success'
    except Exception as e:
        db.rollback()
        return 'fail'
def insert_student(STID,name,classno,cardno):
    pwd=md5val(str(cardno)[-6:])
    try:
        cursor.execute('insert students (STID,STname,ClassNo,Password,CardNo) values ("'+STID+'","'+name+'",'+classno+',"'+pwd+'","'+cardno+'")')
        db.commit()
        return 'success'
    except Exception as e:
        db.rollback()
        return 'fail'
def insert_class(classno,TEID):
    try:
        cursor.execute('insert classes (ClassNo,TEID) values ('+classno+',"'+TEID+'")')
        db.commit()
        return 'success'
    except Exception as e:
        db.rollback()
        return 'fail'
def multi_insert(userlist,usertype):
    userlist=json.loads(userlist)
    sql=''
    n=0
    if usertype=="teacher":
        sql="insert into teachers (TEID,TEname,Password,Phonenum,CardNo) values "
        for item in userlist:
            TEID=str(item['TEID'])
            name=item['name']
            cardno=item['cardno']
            phonenum=str(item['phonenum'])
            pwd=md5val(str(cardno)[-6:])
            if n==0:
                sql+='("'+TEID+'","'+name+'","'+pwd+'","'+phonenum+'","'+cardno+'")'
            else:
                sql+=',("'+TEID+'","'+name+'","'+pwd+'","'+phonenum+'","'+cardno+'")'
            n+=1
    elif usertype=="student":
        sql="insert into students (STID,STname,ClassNo,Password,CardNo) values "
        for item in userlist:
            STID=str(item['STID'])
            name=item['name']
            cardno=item['cardno']
            classno=str(item['classno'])
            pwd=md5val(str(cardno)[-6:])
            if n==0:
                sql+='("'+STID+'","'+name+'",'+classno+',"'+pwd+'","'+cardno+'")'
            else:
                 sql+=',("'+STID+'","'+name+'",'+classno+',"'+pwd+'","'+cardno+'")'
            n+=1
    try:
        cursor.execute(sql)
        db.commit()
        return 'success'
    except Exception as e:
        db.rollback()
        return 'fail'
def finished_good(ID,cost,charge):
    try:
        cursor.execute('update exgoods set cost="'+cost+'" , isdone=1 , charge="'+charge+'" where ID='+ID+'')
        db.commit()
        return 'success'
    except Exception as e:
        db.rollback()
        return 'fail'
# -------------------------------------路由功能-----------------------------------------------------
# @app.route('/')
# def index():
#     return render_template('index.html')
@app.route('/login',methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        session['token']=None
        type=0
        session['name']=None
        session['username']=None
        if len(username)==13 and username.isdigit():
            if login_st(username,password):
                session['token']=get_token()
                type=1
        if len(username)==10 and username.isdigit():
            if login_te(username,password):
                session['token']=get_token()
                type=2
        if not username.isdigit():
            if login_ad(username,password):
                session['token']=get_token()
                type=3
        temp={}
        temp['token']=session['token']
        temp['type']=type
        temp['name']=session['name']
        result=[]
        result.append(temp)
        return jsonify(result)

@app.route('/forget',methods=['POST'])
def forget():
    if request.method == 'POST':
        cardcode=request.form.get('cardcode')
        username=request.form.get('username')
        temp={}
        result=[]
        if len(username)==13 and username.isdigit():
            if login_st(username,cardcode,True):
                temp['message']=resetPwd(username,cardcode,'student')
                result.append(temp)
                return jsonify(result)
        if len(username)==10 and username.isdigit():
            if login_te(username,cardcode,True):
                temp['message']=resetPwd(username,cardcode,'teacher')
                result.append(temp)
                return jsonify(result)
        if not username.isdigit():
            if login_ad(username,cardcode,True):
                temp['message']=resetPwd(username,cardcode,'admin')
                result.append(temp)
                return jsonify(result)
        temp['message']='wrong'
        result.append(temp)
        return jsonify(result)
@app.route('/reset',methods=['POST'])
def reset():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            username=request.form.get('username')
            if len(username)==13 and username.isdigit():
                result['status']=ad_resetPwd(username,'student')
            if len(username)==10 and username.isdigit():
                result['status']=ad_resetPwd(username,'teacher')
            if not username.isdigit():
                result['status']=ad_resetPwd(username,'admin')
            return jsonify(result)
        else:
            result['status']='Invalid_operation'
            return jsonify(result)
@app.route('/delsome',methods=['POST'])
def delsome():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            username=request.form.get('username')
            type=request.form.get('type')
            result['status']=deluser(username,type)
            return jsonify(result)
        else:
            result['status']='Invalid_operation'
            return jsonify(result)
@app.route('/editpwd',methods=['POST'])
def editpwd():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            username=request.form.get('username')
            password=request.form.get('new_password')
            usertype=request.form.get('type')
            result['status']=editpassword(username,password,usertype)
            return jsonify(result)
        else:
            result['status']='Invalid_operation'
            return jsonify(result)
@app.route('/search',methods=['POST'])
def search():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            query=request.form.get('query')
            querytype=request.form.get('querytype')
            usertype=request.form.get('usertype')
            result['data']=searchresult(query,querytype,usertype)
            return jsonify(result)
        else:
            result['status']='Invalid_operation'
            return jsonify(result)
@app.route('/getinfo',methods=['POST'])
def getinfo():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            username=request.form.get('username')
            usertype=request.form.get('usertype')
            result['data']=getuserinfo(username,usertype)
            return jsonify(result)
        else:
            result['status']='Invalid_operation'
            return jsonify(result)
@app.route('/setinfo',methods=['POST'])
def setinfo():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            username=request.form.get('username')
            content=request.form.get('content')
            usertype=request.form.get('usertype')
            result['status']=setuserinfo(username,content,usertype)
            return jsonify(result)
        else:
            result['status']='Invalid_operation'
            return jsonify(result)
@app.route('/addadmin',methods=['POST'])
def addadmin():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            username=request.form.get('username')
            password=request.form.get('password')
            TEID=request.form.get('TEID')
            if teacher_exist(TEID):
                if not admin_username_exist(username):
                    if not admin_teacher_exist(TEID):
                        result['status']=insert_admin(username,password,TEID)
                    else:
                        result['status']="has signed"
                else:
                    result['status']="has account"
            else:
                result['status']="no teacher"
            return jsonify(result)
        else:
            result['status']='Invalid_operation'
            return jsonify(result)
@app.route('/addteacher',methods=['POST'])
def addteacher():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            TEID=request.form.get('TEID')
            name=request.form.get('name')
            phonenum=request.form.get('phonenum')
            cardno=request.form.get('cardno')
            if not teacher_exist(TEID):
                if not teacher_cardno_exist(cardno):
                    result['status']=insert_teacher(TEID,name,phonenum,cardno)
                else:
                    result['status']="has signed"
            else:
                result['status']="has TEID"
            return jsonify(result)
        else:
            result['status']='Invalid_operation'
            return jsonify(result)
@app.route('/multiadd',methods=['POST'])
def multiadd():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            userlist=request.form.get('userlist')
            usertype=request.form.get('usertype')
            
            result['status']=multi_insert(userlist,usertype)
            return jsonify(result)
        else:
            result['status']='Invalid_operation'
            return jsonify(result)
@app.route('/addstudent',methods=['POST'])
def addstudent():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            STID=request.form.get('STID')
            name=request.form.get('name')
            classno=request.form.get('classno')
            cardno=request.form.get('cardno')
            if not student_exist(STID):
                if not student_cardno_exist(cardno):
                    result['status']=insert_student(STID,name,classno,cardno)
                else:
                    result['status']="has signed"
            else:
                result['status']="has STID"
            return jsonify(result)
        else:
            result['status']='Invalid_operation'
            return jsonify(result)
@app.route('/addclass',methods=['POST'])
def addclass():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            TEID=request.form.get('TEID')
            classno=request.form.get('classno')
            if not class_exist(classno):
                if teacher_exist(TEID):
                    result['status']=insert_class(classno,TEID)
                else:
                    result['status']="no teacher"
            else:
                result['status']="has classno"
            return jsonify(result)
        else:
            result['status']='Invalid_operation'
            return jsonify(result)
@app.route('/hasfixed',methods=['POST'])
def hasfixed():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            ID=request.form.get('ID')
            cost=request.form.get('cost')
            charge=request.form.get('charge')
            result['status']=finished_good(ID,cost,charge)
            return jsonify(result)
        else:
            result['status']='Invalid_operation'
            return jsonify(result)
@app.route('/hasgoodfix',methods=['GET'])
def hasgoodfix():
    if request.method == 'GET':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            cursor.execute('select * from exgoods where isdone=0 and isused=1')
            res = cursor.fetchall()
            if res:
                result['status']=True
            else:
                result['status']=False
            return jsonify(result)
        else:
            result['status']='Invalid_operation'
            return jsonify(result)
# ----------------------上传图片\文件------------
@app.route('/upload-img',methods=['POST'])
def uploadimg():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            result['data']=[]
            result['errno']=0
            for i in request.files:
                fname=request.files[i+''].filename
                fkzm=fname[fname.find('.'):]
                file=request.files[i+''].stream.read()
                savename=str(uuid.uuid1())+fkzm
                path="./images/"+savename
                with open(path,'wb') as f:
                    f.write(file)
                    f.close()
                temp={}
                temp['url']=ipv4+path[1:]
                result['data'].append(temp)
            return result
        else:
            result['status']='Invalid_operation'
            return jsonify(result)
@app.route('/upload-file',methods=['POST'])
def uploadfile():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            result['data']=[]
            for i in request.files:
                fname=request.files[i+''].filename
                fkzm=fname[fname.find('.'):]
                file=request.files[i+''].stream.read()
                savename=str(uuid.uuid1())+fkzm
                path="./files/"+savename
                with open(path,'wb') as f:
                    f.write(file)
                    f.close()
                temp={}
                temp['name']=fname
                temp['url']=path[1:]
                result['data'].append(temp)
            return result
        else:
            result['data']=[]
            result['status']='Invalid_operation'
            return jsonify(result)
@app.route('/upload-video',methods=['POST'])
def uploadvideo():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            result['data']=[]
            result['errno']=0
            for i in request.files:
                fname=request.files[i+''].filename
                fkzm=fname[fname.find('.'):]
                file=request.files[i+''].stream.read()
                savename=str(uuid.uuid1())+fkzm
                path="./videos/"+savename
                with open(path,'wb') as f:
                    f.write(file)
                    f.close()
                temp={}
                temp['url']=ipv4+path[1:]
                result['data'].append(temp)
            return result
        else:
            result['status']='Invalid_operation'
            return jsonify(result)
# ----------------------教师端------------
def getclasslist(username):
    res=[]
    cursor.execute('select ClassNo from classes where TEID="'+username+'" and isused=1 ')
    result = cursor.fetchall()
    if result:
        for item in result:
            res.append(item[0])
        return res
    else:
        return res
def searchprojectlist(querytype,username,projecttype):
    sql=''
    res=[]
    if projecttype=='teacherproject':
        if querytype=='all':
            sql='select * from experiments where TEID="'+username+'" and isused=1 order by EXPID desc'
        else:
            sql='select * from experiments where TEID="'+username+'" and ClassNo='+querytype+' and isused=1 order by EXPID desc'    
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            for item in result:
                temp={}
                temp['EXPID']=item[0]
                temp['title']=item[2]
                temp['start']=item[6].strftime('%Y-%m-%d %H:%M:%S')
                temp['end']=item[7].strftime('%Y-%m-%d %H:%M:%S')
                temp['issub']=6 if item[12]==b'\x01' else 5
                temp['classno']=item[8]
                temp['totalnum']=getpeoplenum(item[8])
                temp['subnum']=getsubmitpeople(item[0])
                res.append(temp)
    elif projecttype=='studentproject':
        if querytype=='all':
            sql='select b.recordID,b.EXPID,a.title,a.startTime,a.endTime,b.isread,b.issub,b.isdone from experiments a left join exrecords b on a.EXPID=b.EXPID where b.STID="'+username+'" and a.isused=1 and a.issubmit=1 order by b.EXPID desc'
        elif querytype=='finished':
            sql='select b.recordID,b.EXPID,a.title,a.startTime,a.endTime,b.isread,b.issub,b.isdone from experiments a left join exrecords b on a.EXPID=b.EXPID where b.STID="'+username+'" and a.isused=1 and a.issubmit=1 and b.issub=1 and b.isdone=1 order by b.EXPID desc'
        elif querytype=='waitcorrect':
            sql='select b.recordID,b.EXPID,a.title,a.startTime,a.endTime,b.isread,b.issub,b.isdone from experiments a left join exrecords b on a.EXPID=b.EXPID where b.STID="'+username+'" and a.isused=1 and a.issubmit=1 and b.issub=1 and b.isdone=0 order by b.EXPID desc'
        else:
            sql='select b.recordID,b.EXPID,a.title,a.startTime,a.endTime,b.isread,b.issub,b.isdone from experiments a left join exrecords b on a.EXPID=b.EXPID where b.STID="'+username+'" and a.isused=1 and a.issubmit=1 and b.issub=0 order by b.EXPID desc'
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            for item in result:
                temp={}
                temp['recordID']=item[0]
                temp['EXPID']=item[1]
                temp['title']=item[2]
                temp['start']=item[3].strftime('%Y-%m-%d %H:%M:%S')
                temp['end']=item[4].strftime('%Y-%m-%d %H:%M:%S')
                temp['isread']=1 if item[5]==b'\x01' else 0
                status=-1
                if temp['end']<datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') and item[6]!=b'\x01':
                    status=4
                else:
                    if item[6]!=b'\x01':
                        status=1
                    elif item[6]==b'\x01' and item[7]!=b'\x01':
                        status=2
                    elif item[6]==b'\x01' and item[7]==b'\x01':
                        status=3
                temp['status']=status
                res.append(temp)
    return res
def getsubmitpeople(EXPID):
    EXPID=str(EXPID)
    cursor.execute('select count(*) from exrecords where EXPID='+EXPID+' and issub=1')
    result=cursor.fetchall()
    if result:
        return result[0][0]
    return 0
def getbasinfo(username):
    res={}
    cursor.execute('select a.ClassNo,a.TEID from classes a left join students b on b.ClassNo=a.ClassNo where b.STID="'+username+'" and a.isused=1 ')
    result=cursor.fetchall()
    if result:
        res['classno']=result[0][0]
        res['teacher']=getteachername(result[0][1])
    else:
        res['classno']=''
        res['teacher']=''
    return res
def getteachername(TEID):
    cursor.execute('select TEname from teachers where TEID="'+TEID+'" and isused=1 ')
    result=cursor.fetchall()
    if result:
        return result[0][0]
    return ''
@app.route('/getclassnolist',methods=['POST'])
def getclassnolist():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            username=request.form.get('username')
            result['data']=getclasslist(username)
            return result
        else:
            result['data']=[]
            result['status']='Invalid_operation'
            return jsonify(result)
@app.route('/searchproject',methods=['POST'])
def searchproject():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            username=request.form.get('username')
            querytype=request.form.get('querytype')
            projecttype=request.form.get('projecttype')
            result['data']=searchprojectlist(querytype,username,projecttype)
            return result
        else:
            result['data']=[]
            result['status']='Invalid_operation'
            return jsonify(result)
@app.route('/getbasicinfo',methods=['POST'])
def getbasicinfo():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            username=request.form.get('username')
          
            result['data']=getbasinfo(username)
            return result
        else:
            result['data']={}
            result['status']='Invalid_operation'
            return jsonify(result)

def saveexperiment(project,username,ispub):
    sql1=''
    sql2=''
    n=0
    title=project['title']
    content=textencode(project['content'])
    start=project['start']
    end=project['end']
    files=project['files']
    filename=''
    fileaddr=''
    classnolist=project['classnolist']
    for i in range(len(files)):
        if i !=0:
            filename+=';;'
            fileaddr+=';;'
        filename+=files[i]['name']
        fileaddr+=files[i]['url']
    if ispub=='true':
        for classno in classnolist:
            sql1='insert into experiments (TEID,title,content,filename,fileaddr,startTime,endTime,ClassNo,issubmit) values '
            sql1+='("'+username+'","'+title+'","'+content+'","'+filename+'","'+fileaddr+'","'+start+'","'+end+'",'+str(classno)+',1)'
            try:
                cursor.execute(sql1)
                db.commit()
                cursor.execute('select @@IDENTITY from experiments')
                result=cursor.fetchall()
                EXPID=result[0][0]
                index=0
                sql2='insert into exrecords (EXPID,ClassNo,STID,isread,issub,isdone) values '
                peoplelist=getpeopleofclass(str(classno))
                for STID in peoplelist:
                    if index==0:
                        sql2+='("'+str(EXPID)+'",'+str(classno)+',"'+STID+'",0,0,0)'
                    else:
                        sql2+=',("'+str(EXPID)+'",'+str(classno)+',"'+STID+'",0,0,0)'
                    index+=1
                cursor.execute(sql2)
                db.commit()
            except Exception as e:
                print(sql1)
                print(e)
                db.rollback()
                return 'fail'
        return 'success'
    else:
        sql1+='insert into experiments (TEID,title,content,filename,fileaddr,startTime,endTime,ClassNo,issubmit) values '
        for classno in classnolist:
            if n==0:
                sql1+='("'+username+'","'+title+'","'+content+'","'+filename+'","'+fileaddr+'","'+start+'","'+end+'",'+str(classno)+',0)'
            else:
                sql1+=',("'+username+'","'+title+'","'+content+'","'+filename+'","'+fileaddr+'","'+start+'","'+end+'",'+str(classno)+',0)'
            n+=1
        try:
            cursor.execute(sql1)
            db.commit()
            return 'success'
        except Exception as e:
            db.rollback()
            return 'fail'
    
    
    
def getpeopleofclass(classno):
    res=[]
    cursor.execute('select STID from students where ClassNo='+classno+' and isused=1 ')
    result = cursor.fetchall()
    if result:
        for i in result:
            res.append(i[0])
    return res
def getprojectinfo_teacher(EXPID):
    res={}
    cursor.execute('select * from experiments where EXPID='+EXPID+' and isused=1 ')
    result = cursor.fetchall()
    if result:
        res['EXPID']=result[0][0]
        res['title']=result[0][2]
        res['content']=textuncode(result[0][3])
        res['start']=result[0][6].strftime('%Y-%m-%d %H:%M:%S')
        res['end']=result[0][7].strftime('%Y-%m-%d %H:%M:%S')
        res['classno']=result[0][8]
        res['issub']=1 if result[0][12]==b'\x01' else 0
        files=[]
        filename=result[0][4].split(";;") if result[0][4]!='' else []
        fileaddr=result[0][5].split(";;") if result[0][5]!='' else []
        for i in range(len(filename)):
            temp={}
            temp['name']=filename[i]
            temp['url']=fileaddr[i]
            files.append(temp)
        res['files']=files
        res['anscontent']=textuncode(result[0][9]) if result[0][9]!=None else ''
        ansfilename=result[0][10].split(";;") if result[0][10]!=None and result[0][10]!='' else []
        ansfileaddr=result[0][11].split(";;") if result[0][11]!=None and result[0][11]!='' else []
        ansfiles=[]
        for i in range(len(ansfilename)):
            temp={}
            temp['name']=ansfilename[i]
            temp['url']=ansfileaddr[i]
            ansfiles.append(temp)
        res['ansfiles']=ansfiles
        return res
    return res

def getprojectinfo_student(recordID):
    res={}
    cursor.execute('select * from exrecords where recordID='+recordID+' ')
    result = cursor.fetchall()
    if result:
        for item in result:
            temp={}
            temp['recordID']=item[0]
            temp['report']=textuncode(item[4]) if item[4]!=None else ''
            filename=item[5].split(";;") if item[5]!=None and item[5]!='' else []
            fileaddr=item[6].split(";;") if item[6]!=None and item[6]!='' else []
            files=[]
            for i in range(len(filename)):
                file={}
                file['name']=filename[i]
                file['url']=fileaddr[i]
                files.append(file)
            temp['files']=files
            temp['grade']='' if item[7]==None else item[7]
            temp['isread']=1 if item[8]==b'\x01' else 0
            temp['subtime']=item[9].strftime('%Y-%m-%d %H:%M:%S') if item[9]!=None else ''
            temp['piyu']=item[11] if item[11]!=None else ''
            res=temp
        return res
    return res
@app.route('/saveproject',methods=['POST'])
def saveproject():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            username=request.form.get('username')
            project=json.loads(request.form.get('project'))
            ispub=request.form.get('ispub')
            result['status']=saveexperiment(project,username,ispub)
            return result
        else:
            result['status']='Invalid_operation'
            return jsonify(result)

def updateinfo_project(project):
    EXPID=str(project['EXPID'])
    title=project['title']
    content=textencode(project['content'])
    start=project['start']
    end=project['end']
    files=project['files']
    filename=''
    fileaddr=''
    for i in range(len(files)):
        if i !=0:
            filename+=';;'
            fileaddr+=';;'
        filename+=files[i]['name']
        fileaddr+=files[i]['url']
    anscontent=textencode(project['anscontent'])
    ansfiles=project['ansfiles']
    ansfilename=''
    ansfileaddr=''
    for i in range(len(ansfiles)):
        if i !=0:
            ansfilename+=';;'
            ansfileaddr+=';;'
        ansfilename+=ansfiles[i]['name']
        ansfileaddr+=ansfiles[i]['url']
    try:
        cursor.execute('update experiments set title="'+title+'", content="'+content+'",startTime="'+start+'",endTime="'+end+'",filename="'+filename+'",fileaddr="'+fileaddr+'",anscontent="'+anscontent+'",ansfilename="'+ansfilename+'",ansfileaddr="'+ansfileaddr+'" where EXPID='+EXPID+'')
        db.commit()
        return 'success'
    except Exception as e:
        print(e)
        db.rollback()
        return 'fail'

@app.route('/getprojectinfo',methods=['POST'])
def getprojectinfo():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            EXPID=str(request.form.get('EXPID'))
            
            result['project']=getprojectinfo_teacher(EXPID)
            return result
        else:
            result['status']='Invalid_operation'
            return jsonify(result)

@app.route('/updateprojectinfo',methods=['POST'])
def updateprojectinfo():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            project=json.loads(request.form.get('project'))
            
            result['status']=updateinfo_project(project)
            return result
        else:
            result['status']='Invalid_operation'
            return jsonify(result)

def updateandpub_project(project):
    EXPID=str(project['EXPID'])
    title=project['title']
    content=textencode(project['content'])
    start=project['start']
    end=project['end']
    files=project['files']
    classno=project['classno']
    filename=''
    fileaddr=''
    for i in range(len(files)):
        if i !=0:
            filename+=';;'
            fileaddr+=';;'
        filename+=files[i]['name']
        fileaddr+=files[i]['url']
    try:
        cursor.execute('update experiments set title="'+title+'", content="'+content+'",startTime="'+start+'",endTime="'+end+'",filename="'+filename+'",fileaddr="'+fileaddr+'",issubmit=1 where EXPID='+EXPID+'')
        db.commit()
        index=0
        sql2='insert into exrecords (EXPID,ClassNo,STID,isread,issub,isdone) values '
        peoplelist=getpeopleofclass(str(classno))
        for STID in peoplelist:
            if index==0:
                sql2+='("'+EXPID+'",'+str(classno)+',"'+STID+'",0,0,0)'
            else:
                sql2+=',("'+EXPID+'",'+str(classno)+',"'+STID+'",0,0,0)'
            index+=1
        cursor.execute(sql2)
        db.commit()
        return 'success'
    except Exception as e:
        print(e)
        db.rollback()
        return 'fail'
@app.route('/updateandpub',methods=['POST'])
def updateandpub():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            project=json.loads(request.form.get('project'))
            
            result['status']=updateandpub_project(project)
            return result
        else:
            result['status']='Invalid_operation'
            return jsonify(result)

@app.route('/delproject',methods=['POST'])
def delproject():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            EXPID=str(request.form.get('EXPID'))
            
            result['status']=deluser(EXPID,'project')
            return result
        else:
            result['status']='Invalid_operation'
            return jsonify(result)

def getsubmitlist(EXPID,querytype):
    res=[]
    sql=''
    if querytype=='all':
        sql='select a.recordID,a.STID,a.report,a.filename,a.fileaddr,a.grade,a.subTime,a.issub,a.isdone,a.piyu,b.STname from exrecords a left join students b on a.STID=b.STID where a.EXPID='+EXPID+' and b.isused=1 '
    elif querytype=='finished':
        sql='select a.recordID,a.STID,a.report,a.filename,a.fileaddr,a.grade,a.subTime,a.issub,a.isdone,a.piyu,b.STname from exrecords a left join students b on a.STID=b.STID where a.EXPID='+EXPID+' and b.isused=1 and a.issub=1 and a.isdone=1 '
    elif querytype=='waitcorrect':
        sql='select a.recordID,a.STID,a.report,a.filename,a.fileaddr,a.grade,a.subTime,a.issub,a.isdone,a.piyu,b.STname from exrecords a left join students b on a.STID=b.STID where a.EXPID='+EXPID+' and b.isused=1 and a.issub=1 and a.isdone=0 '
    elif querytype=='unfinished':
        sql='select a.recordID,a.STID,a.report,a.filename,a.fileaddr,a.grade,a.subTime,a.issub,a.isdone,a.piyu,b.STname from exrecords a left join students b on a.STID=b.STID where a.EXPID='+EXPID+' and b.isused=1 and a.issub=0'
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        for item in result:
            temp={}
            temp['recordID']=item[0]
            temp['STID']=item[1]
            temp['report']=textuncode(item[2]) if item[2]!=None else ''
            filename=item[3].split(";;") if item[3]!=None and item[3]!='' else []
            fileaddr=item[4].split(";;") if item[4]!=None and item[4]!='' else []
            files=[]
            for i in range(len(filename)):
                file={}
                file['name']=filename[i]
                file['url']=fileaddr[i]
                files.append(file)
            temp['files']=files
            temp['grade']='' if item[5]==None else item[5]
            temp['subtime']=item[6].strftime('%Y-%m-%d %H:%M:%S') if item[6]!=None else ''
            temp['name']=item[10]
            temp['piyu']=item[9] if item[9]!=None else ''
            temp['status']='0' if item[7]!=b'\x01' else ("1" if item[8]!=b'\x01' else '2')
            res.append(temp)
    return res

@app.route('/searchsubmitlist',methods=['POST'])
def searchsubmitlist():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            EXPID=str(request.form.get('EXPID'))
            querytype=request.form.get('querytype')
            result['submitlist']=getsubmitlist(EXPID,querytype)
            return result
        else:
            result['status']='Invalid_operation'
            return jsonify(result)

def updategradeandpiyu(project):
    grade=str(project['grade'])
    recordID=str(project['recordID'])
    piyu=project['piyu']
    try:
        cursor.execute('update exrecords set grade='+grade+',piyu="'+piyu+'",isdone=1 where recordID='+recordID+' ')
        db.commit()
        return 'success'
    except Exception as e:
        print(e)
        db.rollback()
        return 'fail'

@app.route('/submitgrade',methods=['POST'])
def submitgrade():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            project=json.loads(request.form.get('project'))
            result['status']=updategradeandpiyu(project)
            return result
        else:
            result['status']='Invalid_operation'
            return jsonify(result)

def projectisread(recordID):
    try:
        cursor.execute('update exrecords set isread=1 where recordID='+recordID+' ')
        db.commit()
        return 'success'
    except Exception as e:
        print(e)
        db.rollback()
        return 'fail'

@app.route('/readprojectinfo',methods=['POST'])
def readprojectinfo():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            recordID=str(request.form.get('recordID'))
            projectisread(recordID)
            return result
        else:
            result['status']='Invalid_operation'
            return jsonify(result)
@app.route('/getdetail',methods=['POST'])
def getdetail():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            result['TEproject']={}
            result['STproject']={}
            recordID=str(request.form.get('recordID'))
            EXPID=str(request.form.get('EXPID'))
            result['TEproject']=getprojectinfo_teacher(EXPID)
            result['STproject']=getprojectinfo_student(recordID)
            return result
        else:
            result['status']='Invalid_operation'
            return jsonify(result)

def saveprojectandsubmit(project,issub):
    sql=''
    recordID=str(project['recordID'])
    report=textencode(project['report'])
    subtime=project['subtime']
    files=project['files']
    filename=''
    fileaddr=''
    for i in range(len(files)):
        if i!=0:
            filename+=';;'
            fileaddr+=';;'
        filename+=files[i]['name']
        fileaddr+=files[i]['url']
    if issub=="true":
        sql='update exrecords set report="'+report+'",filename="'+filename+'",fileaddr="'+fileaddr+'",subTime="'+subtime+'",issub=1 where recordID='+recordID+''
    else:
        sql='update exrecords set report="'+report+'",filename="'+filename+'",fileaddr="'+fileaddr+'",subTime="'+subtime+'",issub=0 where recordID='+recordID+''
    try:
        cursor.execute(sql)
        db.commit()
        return 'success'
    except Exception as e:
        print(e)
        db.rollback()
        return 'fail'
@app.route('/saveandsub',methods=['POST'])
def saveandsub():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
           
            project=json.loads(request.form.get('project'))
            issub=request.form.get('issub')
            result['status']=saveprojectandsubmit(project,issub)
            return result
        else:
            result['status']='Invalid_operation'
            return jsonify(result)

def delfix(fixid):
    try:
        cursor.execute('delete from exgoods where ID = '+fixid+' ')
        db.commit()
        return 'success'
    except Exception as e:
        print(e)
        db.rollback()
        return 'fail'

@app.route('/delfixrecord',methods=['POST'])
def delfixrecord():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            fixid=str(request.form.get('fixid'))
            result['status']=delfix(fixid)
            return result
        else:
            result['status']='Invalid_operation'
            return jsonify(result)

def addfix(fixrecord,username):
    goodsname=fixrecord['goodsname']
    goodstype=fixrecord['goodstype']
    goodsnum=fixrecord['goodsnum']
    goodsdesc=fixrecord['goodsdesc']
    TEID=username
    try:
        sql="insert into exgoods (goodsname,goodstype,goodsnum,goodsdesc,TEID,isdone,isused) values (%s,%s,%s,%s,%s,%s,%s)"
        val=(goodsname,int(goodstype),goodsnum,goodsdesc,TEID,0,1)
        cursor.execute(sql,val)
        db.commit()
        return 'success'
    except Exception as e:
        print(e)
        db.rollback()
        return 'fail'

@app.route('/addfixrecord',methods=['POST'])
def addfixrecord():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            fixrecord=json.loads(request.form.get('fixrecord'))
            username=str(request.form.get('username'))
            result['status']=addfix(fixrecord,username)
            return result
        else:
            result['status']='Invalid_operation'
            return jsonify(result)

def add_exdemo(exdemo):
    title=exdemo['title']
    steps=textencode(exdemo['steps'])
    files=exdemo['files']
    videourl=textencode(exdemo['videourl'])
    filename=""
    fileaddr=""
    for i in range(len(files)):
        if i!=0:
            filename+=";;"
            fileaddr+=";;"
        filename+=files[i]['name']
        fileaddr+=files[i]["url"]
    try:
        sql="insert into exdemos (title,steps,filename,fileaddr,videourl,isused) values (%s,%s,%s,%s,%s,%s)"
        val=(title,steps,filename,fileaddr,videourl,1)
        cursor.execute(sql,val)
        db.commit()
        return 'success'
    except Exception as e:
        print(e)
        db.rollback()
        return 'fail'

@app.route('/addexdemo',methods=['POST'])
def addexdemo():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            exdemo=json.loads(request.form.get('exdemo'))
            result['status']=add_exdemo(exdemo)
            return result
        else:
            result['status']='Invalid_operation'
            return jsonify(result)

def get_exdemo(itemid):
    res={}
    cursor.execute('select * from exdemos where ID='+itemid+'')
    result=cursor.fetchall()
    if result:
        res['itemid']=result[0][0]
        res['title']=result[0][1]
        res['steps']=textuncode(result[0][2])
        res['videourl']=textuncode(result[0][5])
        files=[]
        filename=result[0][3].split(";;") if result[0][3]!='' else []
        fileaddr=result[0][4].split(";;") if result[0][4]!='' else []
        for i in range(len(filename)):
            temp={}
            temp['name']=filename[i]
            temp['url']=fileaddr[i]
            files.append(temp)
        res['files']=files
    return res
@app.route('/getexdemo',methods=['POST'])
def getexdemo():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            itemid=str(request.form.get('itemid'))
            result['data']=get_exdemo(itemid)
            return result
        else:
            result['status']='Invalid_operation'
            return jsonify(result)

def edit_exdemo(exdemo):
    itemid=exdemo['itemid']
    title=exdemo['title']
    steps=textencode(exdemo['steps'])
    files=exdemo['files']
    videourl=textuncode(exdemo['videourl'])
    filename=""
    fileaddr=""
    for i in range(len(files)):
        if i!=0:
            filename+=";;"
            fileaddr+=";;"
        filename+=files[i]['name']
        fileaddr+=files[i]["url"]
    try:
        sql="update  exdemos set title=%s,steps=%s,filename=%s,fileaddr=%s,videourl=%s where ID=%s"
        val=(title,steps,filename,fileaddr,videourl,itemid)
        cursor.execute(sql,val)
        db.commit()
        return 'success'
    except Exception as e:
        print(e)
        db.rollback()
        return 'fail'

@app.route('/editexdemo',methods=['POST'])
def editexdemo():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            exdemo=json.loads(request.form.get('exdemo'))
            result['status']=edit_exdemo(exdemo)
            return result
        else:
            result['status']='Invalid_operation'
            return jsonify(result)
def getdata(querytype,queryrole,username):
    sql=''
    res=[]
    if queryrole=="class":
        sql='select * from experiments where TEID="'+username+'" and ClassNo='+querytype+' and isused=1 order by EXPID desc'    
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            for item in result:
                temp={}
                temp['EXPID']=item[0]
                temp['title']=item[2]
                studentlist=getsubmitlist(str(temp['EXPID']),'all')
                sumgrade=0
                for i in studentlist:
                    if i['grade']!='':
                        sumgrade+=i['grade']
                temp['totalnum']=getpeoplenum(item[8])
                temp['subnum']=getsubmitpeople(item[0])
                temp['averagegrade']=round(sumgrade/temp['subnum'],1) if temp['subnum']!=0 else 0
                temp['submitlv']=round(temp['subnum']/temp['totalnum']*100,1) if temp['totalnum']!=0 else 0
                res.append(temp)
    else:
        classnolist=getclasslist(username)
        if querytype=="all":
            for classno in classnolist:
                res.extend(searchresult(str(classno),'classno','student'))
        else:
            res.extend(searchresult(querytype,'classno','student'))   
        for item in res:
            temp=getgradeandsubmitlv(item['STID'])
            totalnum=len(temp['grades'])
            subnum=len(temp['issub'])
            sumgrade=0
            for i in temp['grades']:
                sumgrade+=i
            item['averagegrade']=round(sumgrade/subnum,1) if subnum!=0 else 0
            item['submitlv']=str(round(subnum/totalnum*100,1))+'%' if totalnum!=0 else str(0)+'%'
        res.sort(key=lambda x:x['averagegrade'],reverse=True)
    return res
def getgradeandsubmitlv(STID):
    res={}
    res['titles']=[]
    res['grades']=[]
    res['issub']=[]
    sql='select b.title,a.grade,a.issub from exrecords a left join experiments b on a.EXPID=b.EXPID where a.STID="'+STID+'" and b.isused=1 '    
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        for item in result:
            res['titles'].append(item[0])
            if item[1]==None:
                res['grades'].append(0),
            else:
                res['grades'].append(int(item[1]))
            if item[2]==b'\x01':
                res['issub'].append(1)
    return res
@app.route('/getstatistics',methods=['POST'])
def getstatistics():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            querytype=str(request.form.get('querytype'))
            queryrole=request.form.get('queryrole')
            username=request.form.get('username')
            result['data']=getdata(querytype,queryrole,username)
            return result
        else:
            result['data']=[]
            result['status']='Invalid_operation'
            return jsonify(result)

@app.route('/getallrecord',methods=['POST'])
def getallrecord():
    if request.method == 'POST':
        result={}
        if 'Authorzation' in request.headers.keys() and check_token(request.headers['Authorzation']):
            STID=request.form.get('STID')
            result['data']=getgradeandsubmitlv(STID)
            return result
        else:
            result['data']={}
            result['status']='Invalid_operation'
            return jsonify(result)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
    
    
