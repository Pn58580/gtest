<template>
  <el-card>
    <template #header>
      <div class="flex items-center justify-between">
        <span>环境管理</span>
        <el-button type="primary" @click="createEnv">新增环境</el-button>
      </div>
    </template>

    <el-table :data="envs" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="环境名称" width="140" />
      <el-table-column prop="base_url" label="Base URL" min-width="220" />
      <el-table-column label="操作" width="120">
        <template #default="scope">
          <el-button link type="danger" @click="removeEnv(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { http } from '../api/http'

const loading = ref(false)
const envs = ref<Array<Record<string, unknown>>>([])

const fetchEnvs = async () => {
  loading.value = true
  try {
    const { data } = await http.get('/env/list')
    envs.value = data
  } finally {
    loading.value = false
  }
}

const createEnv = async () => {
  const { value } = await ElMessageBox.prompt('请输入环境名称', '新增环境')
  if (!value) return
  await http.post('/env/create', {
    project_id: 1,
    name: value,
    base_url: 'https://example.com',
    variables_json: '{}'
  })
  ElMessage.success('创建成功')
  await fetchEnvs()
}

const removeEnv = async (id: number) => {
  await http.delete(`/env/${id}`)
  ElMessage.success('删除成功')
  await fetchEnvs()
}

onMounted(fetchEnvs)
</script>
