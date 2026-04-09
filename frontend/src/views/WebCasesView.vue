<template>
  <el-card>
    <template #header>
      <div class="flex items-center justify-between">
        <span>WEB 用例管理</span>
        <el-button type="primary" @click="openCreate">新增用例</el-button>
      </div>
    </template>

    <el-table :data="cases" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="name" label="用例名称" min-width="160" />
      <el-table-column prop="page_url" label="页面URL" min-width="220" />
      <el-table-column prop="selector" label="Selector" width="100" />
      <el-table-column prop="expect_text" label="期望文本" width="120" />
      <el-table-column label="操作" width="220">
        <template #default="scope">
          <el-button link type="success" @click="runCase(scope.row.id)">执行</el-button>
          <el-button link type="danger" @click="removeCase(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>

  <el-dialog v-model="visible" title="新增WEB用例" width="560px">
    <el-form :model="form" label-width="96px">
      <el-form-item label="名称"><el-input v-model="form.name" /></el-form-item>
      <el-form-item label="页面URL"><el-input v-model="form.page_url" /></el-form-item>
      <el-form-item label="Selector"><el-input v-model="form.selector" /></el-form-item>
      <el-form-item label="期望文本"><el-input v-model="form.expect_text" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="visible=false">取消</el-button>
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
  name: 'WEB 冒烟用例',
  page_url: 'https://example.com',
  selector: 'h1',
  expect_text: 'Example'
})

const fetchCases = async () => {
  loading.value = true
  try {
    const { data } = await http.get('/web-case/list')
    cases.value = data
  } finally {
    loading.value = false
  }
}

const openCreate = () => { visible.value = true }

const createCase = async () => {
  await http.post('/web-case/create', form)
  visible.value = false
  ElMessage.success('创建成功')
  await fetchCases()
}

const runCase = async (id: number) => {
  const { data } = await http.post(`/web-case/run/${id}`)
  ElMessage.success(`执行完成：${data.status === 'passed' ? '通过' : '失败'}`)
}

const removeCase = async (id: number) => {
  await http.delete(`/web-case/${id}`)
  ElMessage.success('删除成功')
  await fetchCases()
}

onMounted(fetchCases)
</script>
