import {request} from './request';
import md5 from 'js-md5';

export function GETBASICINFO(username){
    let param = new URLSearchParams()

    param.append('username', username)
    return request({
        url:'/getbasicinfo',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    })
}
export function READPROJECTINFO(recordID){
    let param = new URLSearchParams()

    param.append('recordID', recordID)
    return request({
        url:'/readprojectinfo',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    })
}
export function GETDETAIL(EXPID,recordID){
    let param = new URLSearchParams()

    param.append('EXPID', EXPID)
    param.append('recordID', recordID)
    return request({
        url:'/getdetail',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    })
}
export function SAVEANDSUB(project,issub,loading){
    let param = new URLSearchParams()
    param.append('project', JSON.stringify(project))
    param.append('issub',issub)
    return request({
        url:'/saveandsub',
        method:'post',
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    },loading)
}