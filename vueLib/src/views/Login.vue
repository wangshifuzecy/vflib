<script setup>
import { Place, Cellphone, Postcard, User, Lock } from '@element-plus/icons-vue'
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
//控制注册与登录表单的显示， 默认显示注册
const isRegister = ref(false)
const  registerData = ref({
  userId:'',
  password:'',
  rePassword:'',
  nickname: '',
  username: '',
  addr: '',
  phone: '',
  sex: ''
})

//check password 
const checkRePassword = (rule, value, callback) => {
    if (value === '') {
        callback(new Error('请再次输入密码'))
    } else if (value !== registerData.value.password) {
        callback(new Error('请确保两次密码一致'))
    } else {
        callback()
    }
}

//定义函数,清空数据模型的数据 
// 待完善
const clearRegisterData = ()=>{
    registerData.value={
        userId:'',
        password:'',
        rePassword:''
    }
}

//form input check
const rules={
  addr:[
    {required:true, message:'请输入地址', trigger:'blur'},
  ],
  phone:[
    {required:true, message:'请输入手机号', trigger:'blur'},
  ],
  nickname:[
    {required:true, message:'请输入昵称', trigger:'blur'},
  ],
  username:[
    {required:true, message:'请输入用户名', trigger:'blur'},
  ],
  userId:[
    {required:true, message:'请输入卡号', trigger:'blur'},
  ],
  password:[
    {required:true, message:'请输入密码', trigger:'blur'},
  ],
  rePassword:[
    {validator: checkRePassword, trigger: 'blur' }
  ]
}

import {useTokenStore} from '@/stores/token.js'
import {useRouter} from 'vue-router'
import {userRegisterService,userLoginService } from '@/api/user.js'

const router = useRouter()
const tokenStore = useTokenStore()
const register = async ()=>{
  try{
    let registerForm = {
        pwd: registerData.value.password,
        nickname: registerData.value.nickname,
        username: registerData.value.nickname,
        addr: registerData.value.addr,
        phone: registerData.value.phone,
        role: 'student',
        sex: registerData.value.phone,
        addr: registerData.value.addr,
        balance: 0
    }
    console.log(registerForm);
    let result = await userRegisterService(registerForm)
    // console.log(result);
    ElMessage.success(`id ${result.data.id} user is registered success`)
  }catch{
  }
}

import useUserInfoStore from '@/stores/userInfo.js'
import { userInfoService } from '@/api/user';
const getUserInfo = async (id) => {
    try{
        const userInfoStore = useUserInfoStore();
        let result = await userInfoService(id);
        // console.log(result)
        userInfoStore.setInfo(result.data);
        return [userInfoStore.info.position, userInfoStore.info.username]
    }catch(error){
    }
}
//login api
const login = async ()=>{
  try{
    let loginData = {"id": registerData.value.userId , "pwd": registerData.value.password}
    let result = await userLoginService(loginData)
    tokenStore.setToken(result.data)
    let info = await getUserInfo(registerData.value.userId)
    if(info[0] == 'student'){
      ElMessage.success(`学生 ${info[1]} 登录成功`)
    }else if(info[0] == 'teacher'){
      ElMessage.success(`老师 ${info[1]} 登录成功`)
    }else if(info[0] == 'admin'){
      ElMessage.success(`管理员 ${info[1]} 登录成功`)
      router.push('/admin')
    }
  }catch{
  }
}
</script>

<template>
  <el-row class="login-page">
    <el-col :span="15" class="bg"></el-col>
    <el-col :span="6" :offset="2" class="form">
      <!-- 注册表单 -->
      <el-form ref="form" size="large" autocomplete="off" v-if="isRegister" :model="registerData" :rules="rules">
        <el-form-item>
          <h1>注册</h1>
        </el-form-item>
        <el-form-item prop="nickname" label="昵称">
          <el-input :prefix-icon="User" placeholder="请输入用户昵称" v-model="registerData.nickname"></el-input>
        </el-form-item>
        <el-form-item prop="sex" label="性别">
          <el-radio-group v-model="registerData.sex">
            <el-radio value="男" size="large" border>男</el-radio>
            <el-radio value="女" size="large" border>女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item prop="addr" label="地址">
          <el-input :prefix-icon="Place" placeholder="请输入地址" v-model="registerData.addr"></el-input>
        </el-form-item>
        <el-form-item prop="username" label="姓名">
          <el-input :prefix-icon="User" placeholder="请输入真实姓名" v-model="registerData.username"></el-input>
        </el-form-item>
        <el-form-item prop="phone" label="手机号">
          <el-input :prefix-icon="Cellphone" placeholder="请输入手机号" v-model="registerData.phone"></el-input>
        </el-form-item>
        <el-form-item prop="password" label="密码">
          <el-input :prefix-icon="Lock" type="password" placeholder="请输入密码" v-model="registerData.password"></el-input>
        </el-form-item>
        <el-form-item prop="rePassword" label="确认密码">
          <el-input :prefix-icon="Lock" type="password" placeholder="请再次输入密码" v-model="registerData.rePassword"></el-input>
        </el-form-item>
        <!-- 注册按钮 -->
        <el-form-item>
          <el-button class="button" type="primary" auto-insert-space @click="register">
            注册
          </el-button>
        </el-form-item>
        <el-form-item class="flex">
          <el-link type="info"  style="color:blue" @click="isRegister = false;clearRegisterData()">
            ← 返回 
          </el-link>
        </el-form-item>
      </el-form>
      <!-- 登录表单 -->
      <el-form ref="form" size="large" autocomplete="off" v-else :model="registerData" :rules="rules">
        <el-form-item>
          <h1>登录</h1>
        </el-form-item>
        <el-form-item prop="userId">
          <el-input :prefix-icon="Postcard" placeholder="请输入卡号" v-model="registerData.userId"></el-input>
        </el-form-item>
        <el-form-item>
          <el-input name="password" :prefix-icon="Lock" type="password" placeholder="请输入密码"  v-model="registerData.password"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button class="button" type="primary" auto-insert-space @click="login">登录</el-button>
        </el-form-item>
        <el-form-item class="flex">
          <el-link type="info" @click="isRegister = true;clearRegisterData()" style="color:blue;text-decoration: underline;" >
            注册 →
          </el-link>
        </el-form-item>
        <el-from-item>
          <el-link type="info"  @click="router.push('/')" style="color:blue;text-decoration: underline;">
            游客模式
          </el-link>
        </el-from-item>
      </el-form>
    </el-col>
  </el-row>
</template>

<style lang="scss" scoped>
/* 样式 */
.login-page {
  height: 100vh;
  background-color: #fff;

  .bg {
    background: 
    // url('@/assets/logo2.png') no-repeat 60% center / 240px auto,
      url('@/assets/login_bg.jpg') no-repeat center / cover;
    // border-radius: 0 20px 20px 0;
  }

  .form {
    display: flex;
    flex-direction: column;
    justify-content: center;
    user-select: none;

    .title {
      margin: 0 auto;
    }

    .button {
      width: 100%;
    }

    .flex {
      width: 100%;
      display: flex;
      justify-content: space-between;
    }
  }
}
</style>@/stores/userInfo.js