<script setup>
import { ref } from 'vue'
import { ElMessage,ElMessageBox } from 'element-plus';
import { getAllBookService, addOneBookService, hiddenBookService, editBookByIdService, removeBookByIdService} from '@/api/book';
import { getAllItemService, getItemByBookIdService } from '@/api/item';
import { useRouter } from 'vue-router';
import { MoreFilled, Minus, CirclePlusFilled, Close, Edit, Plus} from '@element-plus/icons-vue';

const router = useRouter()
const books = ref([])
const items = ref([])
const itemDialogVisible = ref(false)
const editDialogVisible = ref(false)
const addDialogVisible = ref(false)
const selectBookId = ref()
const defaultAddBook = {
    "author": "余华",
    "category": "小说",
    "img": "cover_image.jpg",
    "info": "cn",
    "isbn": "9787508654004",
    "name": "活着",
    "pages": 208,
    "price": 39.8,
    "publish_time": "2012-09-01",
    "publisher": "csu"
//---
//   "author": "",
//   "category": "",
//   "img": "",
//   "info": "",
//   "isbn": "",
//   "name": "",
//   "pages": 0,
//   "price": 0,
//   "publish_time": "",
//   "publisher": ""
}
const addBook = ref({ ...defaultAddBook })
const editBook = ref([])

const getAllBook = async()=>{
    try{
        let result = await getAllBookService()
        books.value = result.data
        // console.log(books.value);
    }catch{
    }
}
getAllBook()

const hiddenBook = async(id)=>{
    let result = await hiddenBookService(id)
}

const removeBookById = (id)=>{
    ElMessageBox.confirm(
        `确认要删除id为${id}的图书吗`,
        '警告',
        {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
        }
    )
        .then(async () => {
            try {
                let result = await removeBookByIdService(id)
                if (result.status == 0) {
                    books.value = books.value.filter(book => book.id != id)
                }
            } catch {
            }
        })
}

const beginEdit = (id)=>{
    editDialogVisible.value = true
    books.value.forEach(element => {
        if(element.id == id){
            editBook.value = element
        }
    });
}

const editBookById = async(id, editBook)=>{
    try{
        let result = await editBookByIdService(id, editBook)
        ElMessage.success(' 修改成功')
    }catch{
    }
}

const addOneBook = async(addBook)=>{
    try{
        let result = await addOneBookService(addBook)
        if(result.status == 0){
            ElMessage.success(' 添加成功')
            console.log(result.data);
            books.value.push(result.data)
        }
        addDialogVisible.value = false
    }catch{
    }
}

const resetAddBook = ()=>{
    addBook.value = defaultAddBook
}

const handleSelectionChange = (selection)=>{
    selectBookId.value = selection.map(book => book.id)
    // console.log(selectBookId)
}

const patchRemoveBook = async ()=>{
    ElMessageBox.confirm(
        `确认要删除所选图书吗`,
        '警告',
        {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
        }
    )
        .then(async () => {
            await Promise.all(selectBookId.value.map(async (ele) => {
                try {
                    let result = await removeBookByIdService(ele);
                } catch (error) {
                }
            }))
            getAllBook()
        })
}

const checkBorrow = async (id)=>{
    try{
        let result = await getItemByBookIdService(id)
        items.value = result.data
        itemDialogVisible.value = true
    }catch{
    }
}
</script>

<template>
    <el-card class="page-container" >
        <template #header >
            <div>
                <span>图书管理</span>
                <div style="float:right;">
                    <el-button :disabled="selectBookId == undefined || selectBookId.length == 0" @click="patchRemoveBook()" :icon="Close" type="danger">批量删除</el-button>
                    <el-button @click="addDialogVisible=true" :icon="Plus" type="primary">添加图书</el-button>
                </div>
            </div>
        </template>

        <el-table :data="books" style="" @selection-change="handleSelectionChange">
            <el-table-column type="selection"></el-table-column>
            <el-table-column label="id" prop="id"></el-table-column>
            <el-table-column label="书名" prop="name"></el-table-column>
            <el-table-column label="ISBN" prop="isbn"></el-table-column>
            <el-table-column label="作者" prop="author"></el-table-column>
            <el-table-column label="出版时间" prop="publish_time"></el-table-column>
            <el-table-column label="是否隐藏" prop="is_hidden">
                <template #default="scope">
                    <el-switch v-model="scope.row.is_hidden" @change="hiddenBook(scope.row.id)"></el-switch>
                </template>
            </el-table-column>
            <el-table-column label="编辑/删除/查看借阅详情" style="display: flex;justify-content: space-between">
                <template #default="scope">
                    <el-button size="small" @click=beginEdit(scope.row.id) :icon="Edit" plain type="primary"></el-button>
                    <el-button size="small" @click=removeBookById(scope.row.id) :icon="Close" plain type="danger"></el-button>
                    <el-button size="small" @click=checkBorrow(scope.row.id) :icon="MoreFilled" plain ></el-button>
                </template>
            </el-table-column>
            <template #empty>
                <el-empty description="没有数据"></el-empty>
            </template>
        </el-table>
    </el-card>

    <el-dialog v-model="editDialogVisible">
        <el-form :model="editBook" :label-position="'right'">
            <el-form-item label="ID" prop="id">
                <el-input disabled="true" v-model="editBook.id"></el-input>
            </el-form-item>
            <el-form-item label="作者" prop="author">
                <el-input v-model="editBook.author"></el-input>
            </el-form-item>
            <el-form-item label="类别" prop="category">
                <el-input v-model="editBook.category"></el-input>
            </el-form-item>
            <el-form-item label="简介" prop="info">
                <el-input v-model="editBook.info"></el-input>
            </el-form-item>
            <el-form-item label="ISBN" prop="isbn">
                <el-input v-model="editBook.isbn"></el-input>
            </el-form-item>
            <el-form-item label="价格" prop="price">
                <el-input v-model="editBook.price"></el-input>
            </el-form-item>
            <el-form-item label="图片" prop="img">
                <el-input v-model="editBook.img"></el-input>
            </el-form-item>
            <el-form-item label="出版社" prop="publisher">
                <el-input v-model="editBook.publisher"></el-input>
            </el-form-item>
            <el-form-item label="出版时间" prop="publish_time">
                <el-input v-model="editBook.publish_time"></el-input>
            </el-form-item>
            <el-form-item label="页数" prop="pages">
                <el-input v-model="editBook.pages"></el-input>
            </el-form-item>
            <el-form-item label="借出次数" prop="borrow_times">
                <el-input v-model="editBook.borrow_times"></el-input>
            </el-form-item>
            <el-form-item label="读者想读计数" prop="want">
                <el-input v-model="editBook.want"></el-input>
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="editDialogVisible = flase">取消</el-button> 
            <el-button @click="editBookById(editBook.id, editBook)" type="priamry">提交</el-button>
        </template>
    </el-dialog>

    <el-dialog v-model="addDialogVisible">
        <el-form :model="addBook" :label-position="'right'">
            <el-form-item label="作者" prop="author">
                <el-input v-model="addBook.author"></el-input>
            </el-form-item>
            <el-form-item label="类别" prop="category">
                <el-input v-model="addBook.category"></el-input>
            </el-form-item>
            <el-form-item label="简介" prop="info">
                <el-input v-model="addBook.info"></el-input>
            </el-form-item>
            <el-form-item label="ISBN" prop="isbn">
                <el-input v-model="addBook.isbn"></el-input>
            </el-form-item>
            <el-form-item label="价格" prop="price">
                <el-input v-model="addBook.price"></el-input>
            </el-form-item>
            <el-form-item label="图片" prop="img">
                <el-input v-model="addBook.img"></el-input>
            </el-form-item>
            <el-form-item label="出版时间" prop="publish_time">
                <el-input v-model="addBook.publish_time"></el-input>
            </el-form-item>
            <el-form-item label="出版社" prop="publisher">
                <el-input v-model="addBook.publisher"></el-input>
            </el-form-item>
            <el-form-item label="页数" prop="pages">
                <el-input v-model="addBook.pages"></el-input>
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="addDialogVisible = false;resetAddBook()">取消</el-button> 
            <el-button @click="addOneBook(addBook);getAllBook()" type="priamry">提交</el-button>
        </template>
    </el-dialog>

    <el-dialog v-model="itemDialogVisible">
        <el-table :data="items" style="">
            <el-table-column label="码号定位" prop="id"></el-table-column>
            <el-table-column label="借阅情况" prop="is_borrowed">
                <template #default="scope">
                    {{  scope.row.is_borrowed ? "借出" : "入藏"}}
                </template>
            </el-table-column>
            <el-table-column label="借阅记录ID" prop="record_id">
                <template #default="scope">
                    {{  scope.row.record_id || ""}}
                </template>
            </el-table-column>
            <template #empty>
                <el-empty description="没有数据"></el-empty>
            </template>
        </el-table>
    </el-dialog>
</template>