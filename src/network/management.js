import {request} from './request';
import md5 from 'js-md5';

export function RESETPWD(username){
    let param = new URLSearchParams()
    param.append('username', username)
    return request({
        url:'/reset',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    })
}
export function DEL(username,type){
    let param = new URLSearchParams()
    param.append('username', username)
    param.append('type', type)
    return request({
        url:'/delsome',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    })
}
export function EDITPWD(username,password,type){
    let param = new URLSearchParams()
    param.append('username', username)
    param.append('new_password', password)
    param.append('type', type)
    return request({
        url:'/editpwd',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    })
}
export function SEARCH(query,querytype,usertype,loading=false){
    let param = new URLSearchParams()
    param.append('query', query)
    param.append('querytype', querytype)
    param.append('usertype', usertype)
    return request({
        url:'/search',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    },loading)
}
export function GETINFO(username,usertype){
    let param = new URLSearchParams()
    param.append('username', username)
    param.append('usertype', usertype)
    return request({
        url:'/getinfo',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    })
}
export function SETINFO(username,content,usertype){
    let param = new URLSearchParams()
    param.append('username', username)
    param.append('content', content)
    param.append('usertype', usertype)
    return request({
        url:'/setinfo',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    })
}

export function ADDADMIN(username,password,TEID,loading=false){
    let param = new URLSearchParams()
    param.append('username', username)
    param.append('password', md5(password))
    param.append('TEID', TEID)
    return request({
        url:'/addadmin',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    },loading)
}
export function ADDTEACHER(TEID,name,phonenum,cardno,loading=false){
    let param = new URLSearchParams()
    param.append('TEID', TEID)
    param.append('name', name)
    param.append('phonenum', phonenum)
    param.append('cardno', cardno)
    return request({
        url:'/addteacher',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    },loading)
}
export function ADDBYFILE(userlist,usertype,loading=false){
    let param = new URLSearchParams()
    param.append('userlist', JSON.stringify(userlist))
    param.append('usertype', usertype)
    return request({
        url:'/multiadd',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    },loading)
}
export function ADDSTUDENT(STID,name,classno,cardno,loading=false){
    let param = new URLSearchParams()
    param.append('STID', STID)
    param.append('name', name)
    param.append('classno', classno)
    param.append('cardno', cardno)
    return request({
        url:'/addstudent',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    },loading)
}
export function ADDCLASS(classno,TEID,loading=false){
    let param = new URLSearchParams()
    param.append('classno', classno)
    param.append('TEID', TEID)
    return request({
        url:'/addclass',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    },loading)
}
export function HASFINISHED(ID,cost,charge,loading=false){
    let param = new URLSearchParams()
    param.append('ID', ID)
    param.append('cost', cost)
    param.append('charge', charge)
    return request({
        url:'/hasfixed',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    },loading)
}
export function HASNEWFIX(){
    return request({
        url:'/hasgoodfix',
        method:'get',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    })
}
export function ADDEXDEMO(exdemo,loading=false){
    let param = new URLSearchParams()
    param.append('exdemo', JSON.stringify(exdemo))
    return request({
        url:'/addexdemo',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    },loading)
}
export function EDITEXDEMO(exdemo,loading=false){
    let param = new URLSearchParams()
    param.append('exdemo', JSON.stringify(exdemo))
    return request({
        url:'/editexdemo',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    },loading)
}
export function GETEXDEMO(itemid,loading=false){
    let param = new URLSearchParams()
    param.append('itemid', itemid)
    return request({
        url:'/getexdemo',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    },loading)
}