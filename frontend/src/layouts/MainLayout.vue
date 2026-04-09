<template>
  <el-container class="min-h-screen">
    <el-aside width="220px" class="bg-#0f172a text-white p-4">L-Tester Pro</el-aside>
    <el-container>
      <el-header class="flex items-center justify-end border-b border-#e5e7eb">
        <el-button type="primary" link @click="logout">退出登录</el-button>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

const logout = () => {
  userStore.logout()
  router.push('/login')
}
</script>
