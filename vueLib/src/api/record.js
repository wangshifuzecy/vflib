import request from '@/utils/request.js'

export const getAllRecordService = () =>{
    return request.get('/records')
}

export const getRecordByBookService = (id)=>{
    return request.get(`/records/book_id/${id}`)
}

export const getRecordByUserService = (id)=>{
    return request.get(`/records/user_id/${id}`)
}

export const getRecordByItemService = (id)=>{
    return request.get(`/records/item_id/${id}`)
}

export const getRecordByIdService = (id)=>{
    return request.get(`/records/id/${id}`)
}

export const deleteRecordByIdService = (id)=>{
    return request.delete(`/records/id/${id}`)
}

export const addRecordService = (data)=>{
    return request.post(`/records`, data)
}