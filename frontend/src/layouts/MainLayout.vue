<template>
  <el-container class="min-h-screen">
    <el-aside width="240px" class="bg-#0f172a text-white p-4">
      <div class="font-700 text-18px mb-1">L-Tester Pro</div>
      <div class="text-12px text-#94a3b8 mb-5">{{ userStore.profile?.username }} / {{ userStore.profile?.role }}</div>
      <el-menu
        class="!border-none"
        background-color="#0f172a"
        text-color="#cbd5e1"
        active-text-color="#fff"
        :default-active="activePath"
        router
      >
        <el-menu-item index="/">仪表盘</el-menu-item>
        <el-menu-item index="/projects">项目管理</el-menu-item>
        <el-menu-item index="/runs">执行中心</el-menu-item>
        <el-menu-item v-if="userStore.isAdmin" index="/users">用户管理</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="flex items-center justify-between border-b border-#e5e7eb">
        <div class="font-600">自动化测试平台</div>
        <el-button type="primary" link @click="logout">退出登录</el-button>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

onMounted(() => {
  userStore.fetchProfile()
})

const activePath = computed(() => {
  if (route.path.startsWith('/projects')) return '/projects'
  if (route.path.startsWith('/runs')) return '/runs'
  if (route.path.startsWith('/users')) return '/users'
  return '/'
})

const logout = () => {
  userStore.logout()
  router.push('/login')
}
</script>
