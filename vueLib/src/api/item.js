import request from '@/utils/request.js'

export const getAllItemService = () =>{
    return request.get('/items')
}

export const getItemByBookIdService = (bookId) =>{
    return request.get(`/items/book_id/${bookId}`)
}

export const getItemByIdService = (itemId) =>{
    return request.get(`/items/id/${itemId}`)
}

export const getItemNotBorrowService = (bookId)=>{
    return request.get(`/items/not_borrow/book_id/${bookId}`)
}

export const borrowItemService = (data)=>{
    return request.post(`/items/borrow`, data)
}

export const returnItemByIdService = (itemId)=>{
    return request.post(`/items/return/id/${itemId}`)
}