<script setup>
import {
    Management,
    Promotion,
    UserFilled,
    User,
    Crop,
    EditPen,
    SwitchButton,
    CaretBottom,
    ShoppingCart,
    Document,
    Search,
    Collection,
    Notebook
} from '@element-plus/icons-vue'
import {ref} from 'vue'
const searchString = ref('')
import { useRouter } from 'vue-router'
const router = useRouter()
import { ElMessage, ElMessageBox } from 'element-plus';


</script>

<template>
    <el-container class="layout-container">
        <el-aside width="200px">
            <div class="el-aside__logo"></div>
            <el-menu active-text-color="orange" text-color="#233233" router>
                <el-menu-item index="dashboard">
                    <el-icon>
                        <Document/>
                    </el-icon>
                    <span class="menu-text">展示板</span>
                </el-menu-item>
                <el-menu-item index="books">
                    <el-icon>
                        <Notebook/>
                    </el-icon>
                    <span class="menu-text">图书管理</span>
                </el-menu-item>
                <el-menu-item index="users">
                    <el-icon>
                        <User/>
                    </el-icon>
                    <span class="menu-text">读者管理</span>
                </el-menu-item>
                <el-menu-item index="records">
                    <el-icon>
                        <Collection/>
                    </el-icon>
                    <span class="menu-text">借阅管理</span>
                </el-menu-item>
            </el-menu>
        </el-aside>
        <el-container>
        <!-- 右侧区域-->
            <el-header>
            </el-header>
        <!-- 右侧中间区域-->
            <el-main>
                <router-view></router-view>
            </el-main>
        <!-- 右侧底部区域-->
            <el-footer>
                Library Management System ©2024 Created by csu  
            </el-footer>
        </el-container>
    </el-container>
</template>

<style lang="scss" scoped>
.layout-container {
    height: 100vh;
    .menu-text{
        font-size: 22px;
    }

    .el-aside {
        background-color: #fff;

        &__logo {
            height: 120px;
            background: url('@/assets/logo.png') no-repeat center / 120px auto;
        }
    }

    .el-header {
        background-color: #fff;
        display: flex;
        align-items: center;
        justify-content: space-between;

        .el-dropdown__box {
            display: flex;
            align-items: center;

            .el-icon {
                color: #999;
                margin-left: 10px;
            }

            &:active,
            &:focus {
                outline: none;
            }
        }
    }

    .el-footer {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        color: #666;
    }
}
</style>