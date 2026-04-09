<template>
  <el-card>
    <template #header>
      <div class="flex items-center justify-between">
        <span>接口用例管理</span>
        <el-button type="primary" @click="createCase">新增用例</el-button>
      </div>
    </template>

    <el-table :data="cases" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="name" label="用例名称" min-width="180" />
      <el-table-column prop="method" label="Method" width="100" />
      <el-table-column prop="path" label="Path" min-width="200" />
      <el-table-column label="操作" width="220">
        <template #default="scope">
          <el-button link type="success" @click="runCase(scope.row.id)">执行</el-button>
          <el-button link type="danger" @click="removeCase(scope.row.id)">删除</el-button>
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
const cases = ref<Array<Record<string, unknown>>>([])

const fetchCases = async () => {
  loading.value = true
  try {
    const { data } = await http.get('/api-case/list')
    cases.value = data
  } finally {
    loading.value = false
  }
}

const createCase = async () => {
  const { value } = await ElMessageBox.prompt('请输入用例名称', '新增接口用例')
  if (!value) return
  await http.post('/api-case/create', {
    project_id: 1,
    name: value,
    method: 'GET',
    path: '/health',
    body: '{}'
  })
  ElMessage.success('创建成功')
  await fetchCases()
}

const runCase = async (id: number) => {
  await http.post(`/api-case/run/${id}`)
  ElMessage.success('执行完成')
}

const removeCase = async (id: number) => {
  await http.delete(`/api-case/${id}`)
  ElMessage.success('删除成功')
  await fetchCases()
}

onMounted(fetchCases)
</script>
