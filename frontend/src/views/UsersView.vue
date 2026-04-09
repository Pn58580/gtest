<template>
  <el-card>
    <template #header>
      <div class="font-600">用户管理（管理员）</div>
    </template>
    <el-table :data="users" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="role" label="角色" width="120" />
    </el-table>
  </el-card>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { http } from '../api/http'

interface UserItem {
  id: number
  username: string
  role: string
}

const loading = ref(false)
const users = ref<UserItem[]>([])

const fetchUsers = async () => {
  loading.value = true
  try {
    const { data } = await http.get<UserItem[]>('/system/users')
    users.value = data
  } catch {
    ElMessage.error('你没有权限查看用户列表')
  } finally {
    loading.value = false
  }
}

onMounted(fetchUsers)
</script>
