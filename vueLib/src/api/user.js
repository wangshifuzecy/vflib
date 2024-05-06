import request from '@/utils/request.js'

export const userRegisterService = (data) =>{
    return request.post('/users',data)
}

export const userLoginService = (data) =>{
    return request.post('/users/login',data)
}

export const userInfoService = (userid) =>{
    return request.get(`/users/${userid}`)
}

export const getAllUserService = ()=>{
    return request.get(`/users`)
}

export const removeUserByIdService = (userid)=>{
    return request.delete(`/users/${userid}`)
}

export const updateUserService = (userid, data)=>{
    return request.put(`/users/${userid}`, data)
}