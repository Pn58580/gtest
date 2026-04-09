<template>
  <el-card>
    <template #header>
      <div class="flex items-center justify-between">
        <span>接口用例管理</span>
        <el-button type="primary" @click="openCreate">新增用例</el-button>
      </div>
    </template>

    <el-table :data="cases" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="name" label="用例名称" min-width="160" />
      <el-table-column prop="method" label="Method" width="90" />
      <el-table-column prop="path" label="Path" min-width="180" />
      <el-table-column prop="expected_status" label="期望状态码" width="120" />
      <el-table-column prop="expected_keyword" label="期望关键字" width="140" />
      <el-table-column label="操作" width="220">
        <template #default="scope">
          <el-button link type="success" @click="runCase(scope.row.id)">执行</el-button>
          <el-button link type="danger" @click="removeCase(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>

  <el-dialog v-model="visible" title="新增接口用例" width="540px">
    <el-form :model="form" label-width="96px">
      <el-form-item label="名称"><el-input v-model="form.name" /></el-form-item>
      <el-form-item label="Method">
        <el-select v-model="form.method" style="width: 100%">
          <el-option label="GET" value="GET" />
          <el-option label="POST" value="POST" />
          <el-option label="PUT" value="PUT" />
          <el-option label="DELETE" value="DELETE" />
        </el-select>
      </el-form-item>
      <el-form-item label="Path"><el-input v-model="form.path" /></el-form-item>
      <el-form-item label="Body"><el-input v-model="form.body" type="textarea" :rows="3" /></el-form-item>
      <el-form-item label="期望状态码"><el-input-number v-model="form.expected_status" :min="100" :max="599" /></el-form-item>
      <el-form-item label="期望关键字"><el-input v-model="form.expected_keyword" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" @click="createCase">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { http } from '../api/http'

const loading = ref(false)
const visible = ref(false)
const cases = ref<Array<Record<string, unknown>>>([])

const form = reactive({
  project_id: 1,
  name: '新用例',
  method: 'GET',
  path: '/health',
  body: '{}',
  expected_status: 200,
  expected_keyword: 'ok'
})

const fetchCases = async () => {
  loading.value = true
  try {
    const { data } = await http.get('/api-case/list')
    cases.value = data
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  visible.value = true
}

const createCase = async () => {
  await http.post('/api-case/create', form)
  visible.value = false
  ElMessage.success('创建成功')
  await fetchCases()
}

const runCase = async (id: number) => {
  const { data } = await http.post(`/api-case/run/${id}`)
  const status = data.status === 'passed' ? '通过' : '失败'
  ElMessage.success(`执行完成：${status}`)
}

const removeCase = async (id: number) => {
  await http.delete(`/api-case/${id}`)
  ElMessage.success('删除成功')
  await fetchCases()
}

onMounted(fetchCases)
</script>
