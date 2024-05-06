import { createRouter, createWebHistory } from 'vue-router'

//导入组件
import LoginVue from '@/views/Login.vue'
import AdminLayoutVue from '@/views/AdminLayout.vue'

import BookManageVue from '@/views/admin/BookManage.vue'
import RecordManageVue from '@/views/admin/RecordManage.vue'
import UserManageVue from '@/views/admin/UserManage.vue'
import DashboardVue from '@/views/Dashboard.vue'


//定义路由关系
const routes = [
    { path: '/', component: LoginVue },
    { path: '/admin', component: AdminLayoutVue,
        children:[
            {path: '/books', component: BookManageVue},
            {path: '/users', component: UserManageVue},
            {path: '/records', component: RecordManageVue},
            {path: '/dashboard', component: DashboardVue}
        ]
    }
]

//创建路由器
const router = createRouter({
    history: createWebHistory(),
    routes: routes
})

//导出路由
export default router