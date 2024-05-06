import request from '@/utils/request.js'

export const getAllBookService = () =>{
    return request.get('/books')
}

export const hiddenBookService = (id) =>{
    return request.post(`/books/${id}/hidden`)
}

export const removeBookByIdService = (id)=>{
    return request.delete(`/books/${id}`)
}

export const editBookByIdService = (id, data)=>{
    return request.put(`/books/${id}`, data)
}

export const addOneBookService = (data)=>{
    return request.post(`/books`, data)
}
