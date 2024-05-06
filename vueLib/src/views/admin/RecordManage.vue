<script setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus';
import { getAllBookService } from '@/api/book'
import { getAllRecordService, getRecordByUserService, getRecordByBookService, addRecordService, deleteRecordByIdService } from '@/api/record'
import { getItemNotBorrowService, borrowItemService, getItemByIdService, returnItemByIdService } from '@/api/item';
import { getAllUserService } from '@/api/user';
import { useRouter } from 'vue-router';
import Validator from 'async-validator'
import { MoreFilled, Minus, CirclePlusFilled, Close, Edit, Plus} from '@element-plus/icons-vue';
import { getCurrentTime } from '@/utils/time';

const router = useRouter()
const records = ref([])
const books = ref([])
const users = ref([])
const items = ref([])
const editRecord = ref([])
const addRecordForm = ref<import('element-plus').FormInstance
const editDialogVisible = ref(false)
const addDialogVisible = ref(false)
const selectRecordId = ref([])
const addRule = ref({
    book_id: [
        { required: true, message: '请选择索书号', trigger: 'change' }
    ],
    user_id: [
        { required: true, message: '请选择用户卡号', trigger: 'change' }
    ],
    item_id: [
        { required: true, message: '请选择图书码号定位', trigger: 'change' }
    ]
})
const handleSelectionChange = (selection)=>{
    selectRecordId.value = selection.map(record => {
        return {"id": record.id, "item_id": record.item_id}
    })
    // console.log(selectRecordId)
}
const getAllBook = async()=>{
    try{
        let result = await getAllBookService()
        books.value = result.data
        // console.log(books.value);
    }catch{
    }
}
getAllBook()
const getAllUser = async()=>{
    let result = await getAllUserService()
    users.value = result.data
    // console.log(users.value)
}
getAllUser()
const getAllRecord = async()=>{
    let result = await getAllRecordService()
    records.value = result.data
    // console.log(records.value);
}
getAllRecord()
const defaultAddRecord = {
    "book_id": "",
    "item_id": "",
    "user_id": "",
    "isbn": "",
    "book_name": "",
    "borrow_time": "",
    "return_time": null
}
const addRecord = ref({ ...defaultAddRecord })
const resetAddRecord = ()=>{
    addRecord.value = defaultAddRecord
}

const handleBookIdChange = async ()=>{
    books.value.forEach(ele=>{
        if(ele.id == addRecord.value.book_id){
            addRecord.value.isbn =  ele.isbn
            addRecord.value.book_name =  ele.name
        }
    })
    let result = await getItemNotBorrowService(addRecord.value.book_id)
    items.value =  result.data
    // console.log(items.value);
}

const handleSubmit = async (form) => {
    let allValid = true
    if (!form) return
    await form.validate((valid, fields) => {
        allValid &= valid
    })
    if(allValid){
        addOneRecord(addRecord.value)
        addDialogVisible.value = false
    }
}

const addOneRecord = async(record)=>{
    record.borrow_time = getCurrentTime()
    let recordResult = await addRecordService(record)
    let addedRecord = recordResult.data
    getAllRecord()
    // console.log(addedRecord);
    let itemResult = await borrowItemService(addedRecord)
    // console.log(itemResult);
}

const removeRecordById = async(recordId, itemId)=>{
    ElMessageBox.confirm(
        `确认要删除所选记录吗`,
        '警告',
        {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
        }
    )
        .then(async()=>{
            await returnItemByIdService(itemId)
            await deleteRecordByIdService(recordId)
            getAllRecord()
        })
}

const patchRemoveRecord = async () => {
    ElMessageBox.confirm(
        `确认要删除所选记录吗`,
        '警告',
        {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
        }
    )
        .then(async () => {
            await Promise.all(selectRecordId.value.map(async (ele) => {
                try {
                    await returnItemByIdService(ele.item_id)
                    await deleteRecordByIdService(ele.id)
                } catch (error) {
                }
            }))
            getAllRecord()
        })
}

const beginEdit = (id)=>{
    records.value.forEach(element => {
        if(element.id == id){
            editRecord.value = element
        }
    })
    editDialogVisible.value = true
}

const editRecordById = (id, record)=>{

}
</script>

<template>
    <el-card>
        <template #header >
            <div>
                <span>图书管理</span>
                <div style="float:right;">
                    <el-button :disabled="selectRecordId == undefined || selectRecordId.length == 0" @click="patchRemoveRecord()" :icon="Close" type="danger">批量删除</el-button>
                    <el-button @click="addDialogVisible=true" :icon="Plus" type="primary">添加记录</el-button>
                </div>
            </div>
        </template>

        <el-table :data="records" @selection-change="handleSelectionChange">
            <el-table-column type="selection"></el-table-column>
            <el-table-column label="借阅记录ID" prop="id"></el-table-column>
            <el-table-column label="索书号" prop="book_id"></el-table-column>
            <el-table-column label="书名" prop="book_name"></el-table-column>
            <el-table-column label="用户卡号" prop="user_id"></el-table-column>
            <el-table-column label="图书码号定位" prop="item_id"></el-table-column>
            <el-table-column label="ISBN" prop="isbn"></el-table-column>
            <el-table-column label="借出时间" prop="borrow_time"></el-table-column>
            <el-table-column label="归还时间" prop="return_time"></el-table-column>
                <el-table-column label="编辑/删除" style="display: flex;justify-content: space-between">
                <template #default="scope">
                    <el-button size="small" @click=beginEdit(scope.row.id) :icon="Edit" plain type="primary"></el-button>
                    <el-button size="small" @click="removeRecordById(scope.row.id, scope.row.item_id)" :icon="Close" plain type="danger"></el-button>
                </template>
            </el-table-column>
            <template #empty>
                <el-empty description="没有数据"></el-empty>
            </template>
        </el-table>
    </el-card>

    <el-dialog v-model="editDialogVisible">
        <el-form :model="editRecord" :label-position="right">
            <el-form-item label="借阅记录ID" prop="id">
                <el-input v-model="editRecord.id" disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="索书号" prop="book_id">
                <el-input v-model="editRecord.book_id" disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="用户卡号" prop="user_id">
                <el-input v-model="editRecord.user_id"></el-input>
            </el-form-item>
            <el-form-item label="图书码号定位" prop="item_id">
                <el-input v-model="editRecord.item_id" disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="ISBN" prop="isbn">
                <el-input v-model="editRecord.isbn"></el-input>
            </el-form-item>
            <el-form-item label="书名" prop="book_name">
                <el-input v-model="editRecord.book_name"></el-input>
            </el-form-item>
            <el-form-item label="借出时间" prop="borrow_time">
                <el-input v-model="editRecord.borrow_time"></el-input>
            </el-form-item>
            <el-form-item label="归还时间" prop="return_time">
                <el-input v-model="editRecord.return_time"></el-input>
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="editdialogVisible = flase">取消</el-button> 
            <el-button @click="editRecordById(editRecord.id, editRecord)" type="priamry">提交</el-button>
        </template>
    </el-dialog>

    <el-dialog v-model="addDialogVisible">
        <el-form :model="addRecord" :label-position="'right'" :rules="addRule" ref="addRecordForm"> 
            <el-form-item label="索书号" prop="book_id">
                <el-select v-model="addRecord.book_id" @change="handleBookIdChange" placeholder="请选择索书号">
                    <el-option v-for="book in books" :key="book.id" :label="book.id + book.name" :value="book.id"/>
                </el-select>
            </el-form-item>
            <el-form-item label="用户卡号" prop="user_id">
                <el-select v-model="addRecord.user_id" placeholder="请选择用户">
                    <el-option v-for="user in users" :key="user.id" :label="user.id + user.username" :value="user.id"/>
                </el-select>
            </el-form-item>
            <el-form-item label="图书码号定位" prop="item_id" >
                <el-select v-model="addRecord.item_id" placeholder="请在选择索书号后选择对应副本">
                    <el-option v-for="item in items" :key="item.id" :label="item.id + item.name" :value="item.id"/>
                </el-select>
            </el-form-item>
            <el-form-item label="ISBN" prop="isbn">
                <el-input v-model="addRecord.isbn" disabled="true" placeholder="请先选择索书号"/>
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="addDialogVisible = false;resetAddRecord()">取消</el-button> 
            <el-button @click="handleSubmit(addRecordForm)" type="priamry">提交</el-button>
        </template>
    </el-dialog>
</template>