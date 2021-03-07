import {request} from './request';
import md5 from 'js-md5';

export function GETCLASSLIST(username){
    let param = new URLSearchParams()
    param.append('username', username)
    return request({
        url:'/getclassnolist',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    })
}
export function SEARCHPROJECT(querytype,username,projecttype,loading=false){
    let param = new URLSearchParams()
    param.append('querytype', querytype)

    param.append('projecttype', projecttype)
    param.append('username', username)
    return request({
        url:'/searchproject',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    },loading)
}

export function SAVEANDPUB(project,username,ispub=false,loading=false){
    let param = new URLSearchParams()
    param.append('project', JSON.stringify(project))
    param.append('username', username)
    param.append('ispub',ispub)
    return request({
        url:'/saveproject',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    },loading)
}
export function GETPROJECTINFO(EXPID){
    let param = new URLSearchParams()
    param.append('EXPID',EXPID)
    return request({
        url:'/getprojectinfo',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    })
}
export function UPDATEPROJECTINFO(project,loading=false){
    let param = new URLSearchParams()
    param.append('project', JSON.stringify(project))
    return request({
        url:'/updateprojectinfo',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    },loading)
}
export function UPDATEANDPUB(project,loading=false){
    let param = new URLSearchParams()
    param.append('project', JSON.stringify(project))
    return request({
        url:'/updateandpub',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    },loading)
}

export function DELPROJECT(EXPID){
    let param = new URLSearchParams()
    param.append('EXPID',EXPID)
    return request({
        url:'/delproject',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    })
}

export function SEARCHSUBMITLIST(EXPID,querytype){
    let param = new URLSearchParams()
    param.append('EXPID',EXPID)
    param.append('querytype',querytype)
    return request({
        url:'/searchsubmitlist',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    })
}

export function SUBMITGRADE(project,loading=false){
    let param = new URLSearchParams()
    param.append('project', JSON.stringify(project))
    return request({
        url:'/submitgrade',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    },loading)
}
export function DELFIX(fixid){
    let param = new URLSearchParams()
    param.append('fixid',fixid)
    return request({
        url:'/delfixrecord',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    })
}
export function ADDFIX(fixrecord,username,loading=false){
    let param = new URLSearchParams()
    param.append('fixrecord', JSON.stringify(fixrecord))
    param.append('username',username)
    return request({
        url:'/addfixrecord',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    },loading)
}

export function GETSTATISTICS(querytype,queryrole,username,loading=false){
    let param = new URLSearchParams()
    param.append('querytype', querytype)
    param.append('queryrole',queryrole)
    param.append('username',username)
    return request({
        url:'/getstatistics',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    },loading)
}

export function GETALLRECORDS(STID){
    let param = new URLSearchParams()
    param.append('STID', STID)
    return request({
        url:'/getallrecord',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    })
}