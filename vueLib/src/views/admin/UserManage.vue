<script setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus';
import { getAllUserService, updateUserService, userRegisterService, removeUserByIdService } from '@/api/user';
import { getRecordByUserService, getRecordByBookService } from '@/api/record'
import { useRouter } from 'vue-router';
import { MoreFilled, Minus, CirclePlusFilled, Close, Edit, Plus} from '@element-plus/icons-vue';

const users = ref([])
const selectUserId = ref()
const addDialogVisible = ref(false)
const editDialogVisible = ref(false)
const recordDialogVisible = ref(false)
const records = ref([])
const editUser = ref()
const defaultAddUser = {
    "nickname": "hello",
    "username": "王某",
    "position": "student",
    "sex": "男",
    "addr": "ST.STAIN",
    "phone": "13901391270",
    "balance": 0
    //----------------
    // "nickname": "",
    // "username": "",
    // "position": "student",
    // "sex": "男",
    // "addr": "",
    // "phone": "",
    // "balance": 0
}
const addUser = ref({ ...defaultAddUser })
const resetAddUser = ()=>{
    addUser.value = defaultAddUser
}


const getAllUser = async()=>{
    let result = await getAllUserService()
    users.value = result.data
    // console.log(users.value)
}
getAllUser()

const handleSelectionChange = (selection)=>{
    selectUserId.value = selection.map(book => book.id)
    console.log(selectUserId);
}

const beginEdit = (id)=>{
    editDialogVisible.value = true
    users.value.forEach(element => {
        if(element.id == id){
            editUser.value = element
        }
    });
}

const removeUserById = async(id)=>{
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
                let result = await removeUserByIdService(id)
                console.log(result)
                if (result.status == 0) {
                    users.value = users.value.filter(user => user.id != id)
                }
            } catch {
            }
        })
}

const editUserById = async(id, data)=>{
    let result = await updateUserService(id, data)
    ElMessage.success(' 修改成功')
    editDialogVisible.value = false
}

const checkBorrow = async (id)=>{
    let result = await getRecordByUserService(id)
    records.value = result.data
    recordDialogVisible.value = true
}

const patchRemoveBook = async () => {
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
            await Promise.all(selectUserId.value.map(async (ele) => {
                try {
                    let result = await removeUserByIdService(ele);
                } catch (error) {
                }
            }))
            getAllUser()
        })
}

const addOneUser = async()=>{
    let result = await userRegisterService(addUser.value)
    if(result.status == 0){
        ElMessage.success(`用户注册成功, id为${result.data.id}`)
    }
    addDialogVisible.value = false
    getAllUser()
}

</script>

<template>
    <el-card>
        <template #header>
            <div>
                <span> 用户管理 </span>
                <div style="float:right">
                    <el-button  :disabled="selectUserId == undefined || selectUserId.length == 0"
                        @click="patchRemoveBook()" :icon="Close" type="danger">批量删除</el-button>
                    <el-button  @click="addDialogVisible = true" :icon="Plus"
                        type="primary">添加用户</el-button>
                </div>
            </div>
        </template>
        <el-table :data="users" style="" @selection-change="handleSelectionChange">
            <el-table-column type="selection"></el-table-column>
            <el-table-column label="ID" prop="id"></el-table-column>
            <el-table-column label="昵称" prop="nickname"></el-table-column>
            <el-table-column label="真实姓名" prop="username" width="120px"></el-table-column>
            <el-table-column label="职位" width="80px">
                <template #default="scope">
                    {{ scope.row.position === "student" ? "学生" : "老师" }}
                </template>
            </el-table-column>
            <el-table-column label="性别" prop="sex" width="60px"></el-table-column>
            <el-table-column label="地址" prop="addr"></el-table-column>
            <el-table-column label="手机号" prop="phone"></el-table-column>
            <el-table-column label="余额" prop="balance"></el-table-column>
            <el-table-column label="编辑/删除/查看借阅详情" style="display: flex;justify-content: space-between">
                <template #default="scope">
                    <el-button size="small" @click=beginEdit(scope.row.id) :icon="Edit" plain
                        type="primary"></el-button>
                    <el-button size="small" @click=removeUserById(scope.row.id) :icon="Close" plain
                        type="danger"></el-button>
                    <el-button size="small" @click=checkBorrow(scope.row.id) :icon="MoreFilled" plain></el-button>
                </template>
            </el-table-column>
            <template #empty>
                <el-empty description="没有数据"></el-empty>
            </template>
        </el-table>
    </el-card>

    <el-dialog v-model="addDialogVisible">
        <el-form :model="addUser" :label-position="'right'">
            <el-form-item label="昵称" prop="nickname">
                <el-input v-model="addUser.nickname"></el-input>
            </el-form-item>
            <el-form-item label="用户名" prop="username">
                <el-input v-model="addUser.username"></el-input>
            </el-form-item>
            <el-form-item label="职位" prop="position">
                <el-select v-model="addUser.position">
                    <el-option label="学生" value="student"/>
                    <el-option label="教师" value="teacher"/>
                </el-select>
            </el-form-item>
            <el-form-item label="性别" prop="sex">
                <el-select v-model="addUser.sex">
                    <el-option label="男" value="男"/>
                    <el-option label="女" value="女"/>
                </el-select>
            </el-form-item>
            <el-form-item label="地址" prop="addr">
                <el-input v-model="addUser.addr"></el-input> 
            </el-form-item>
            <el-form-item label="手机号" prop="phone">
                <el-input v-model="addUser.phone"></el-input> 
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="addDialogVisible = flase;resetAddUser()">取消</el-button> 
            <el-button @click="addOneUser(addUser);" type="priamry">提交</el-button>
        </template>
    </el-dialog>

    <el-dialog v-model="editDialogVisible">
        <el-form :model="editUser" :label-position="'right'">
            <el-form-item label="ID" prop="id">
                <el-input v-model="editUser.id" disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="昵称" prop="nickname">
                <el-input v-model="editUser.nickname"></el-input>
            </el-form-item>
            <el-form-item label="用户名" prop="username">
                <el-input v-model="editUser.username"></el-input>
            </el-form-item>
            <el-form-item label="职位" prop="position">
                <el-select v-model="editUser.position">
                    <el-option label="学生" value="student"/>
                    <el-option label="教师" value="teacher"/>
                </el-select>
            </el-form-item>
            <el-form-item label="性别" prop="sex">
                <el-select v-model="editUser.sex">
                    <el-option label="男" value="男"/>
                    <el-option label="女" value="女"/>
                </el-select>
            </el-form-item>
            <el-form-item label="地址" prop="editr">
                <el-input v-model="editUser.addr"></el-input> 
            </el-form-item>
            <el-form-item label="手机号" prop="phone">
                <el-input v-model="editUser.phone"></el-input> 
            </el-form-item>
            <el-form-item label="余额" prop="balance">
                <el-input v-model="editUser.balance"></el-input> 
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="editDialogVisible = flase">取消</el-button> 
            <el-button @click="editUserById(editUser.id, editUser);" type="priamry">提交</el-button>
        </template>
    </el-dialog>

    <el-dialog v-model="recordDialogVisible">
        <el-table :data="records" style="">
            <el-table-column label="借阅记录ID" prop="id"></el-table-column>
            <el-table-column label="索书号" prop="book_id"></el-table-column>
            <el-table-column label="ISBN" prop="isbn"></el-table-column>
            <el-table-column label="借出时间" prop="borrow_time"></el-table-column>
            <el-table-column label="归还时间" prop="return_time"></el-table-column>
            <template #empty>
                <el-empty description="没有数据"></el-empty>
            </template>
        </el-table>
    </el-dialog>
</template>