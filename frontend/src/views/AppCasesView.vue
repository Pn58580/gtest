<template>
  <el-card>
    <template #header>
      <div class="flex items-center justify-between">
        <span>APP 用例管理</span>
        <el-button type="primary" @click="openCreate">新增用例</el-button>
      </div>
    </template>

    <el-table :data="cases" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="name" label="用例名称" min-width="150" />
      <el-table-column prop="device_id" label="设备" width="130" />
      <el-table-column prop="app_package" label="App 包名" min-width="150" />
      <el-table-column prop="app_activity" label="启动 Activity" min-width="190" />
      <el-table-column prop="script_path" label="脚本路径" min-width="200" />
      <el-table-column prop="assert_keyword" label="断言关键字" width="120" />
      <el-table-column label="操作" width="220">
        <template #default="scope">
          <el-button link type="primary" @click="openEdit(scope.row as Record<string, unknown>)">编辑</el-button>
          <el-button link type="success" @click="runCase(scope.row.id as number)">执行</el-button>
          <el-button link type="danger" @click="removeCase(scope.row.id as number)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>

  <el-dialog v-model="visible" :title="editingId ? '编辑APP用例' : '新增APP用例'" width="720px">
    <el-form :model="form" label-width="110px">
      <el-form-item label="名称"><el-input v-model="form.name" /></el-form-item>
      <el-form-item label="设备ID"><el-input v-model="form.device_id" /></el-form-item>
      <el-form-item label="App 包名"><el-input v-model="form.app_package" /></el-form-item>
      <el-form-item label="启动 Activity"><el-input v-model="form.app_activity" /></el-form-item>
      <el-form-item label="脚本路径"><el-input v-model="form.script_path" /></el-form-item>
      <el-form-item label="断言关键字"><el-input v-model="form.assert_keyword" /></el-form-item>
      <el-form-item label="步骤定义(JSON)">
        <el-input
          v-model="form.steps_text"
          type="textarea"
          :rows="7"
          placeholder='[{"action":"launch_app"},{"action":"tap","target":"id=login"}]'
        />
      </el-form-item>
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
const editingId = ref<number | null>(null)
const cases = ref<Array<Record<string, unknown>>>([])

const defaultSteps = [
  { action: 'launch_app' },
  { action: 'input', target: 'id=username', value: 'demo' },
  { action: 'input', target: 'id=password', value: '123456' },
  { action: 'tap', target: 'id=login' },
  { action: 'assert_text', target: 'id=welcome', value: 'Welcome' }
]

const form = reactive({
  project_id: 1,
  name: 'APP 冒烟用例',
  device_id: 'emulator-5554',
  app_package: 'com.demo.app',
  app_activity: 'com.demo.app.MainActivity',
  script_path: 'scripts/login.air',
  steps_text: JSON.stringify(defaultSteps),
  assert_keyword: 'Welcome'
})

const fetchCases = async () => {
  loading.value = true
  try {
    const { data } = await http.get('/app-case/list')
    cases.value = data
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  editingId.value = null
  visible.value = true
}

const openEdit = (item: Record<string, unknown>) => {
  editingId.value = Number(item.id)
  form.name = String(item.name ?? '')
  form.device_id = String(item.device_id ?? '')
  form.app_package = String(item.app_package ?? '')
  form.app_activity = String(item.app_activity ?? '')
  form.script_path = String(item.script_path ?? '')
  form.assert_keyword = String(item.assert_keyword ?? '')
  form.steps_text = JSON.stringify(item.steps ?? [], null, 2)
  visible.value = true
}

const createCase = async () => {
  let steps: unknown[] = []
  try {
    const parsed = JSON.parse(form.steps_text)
    if (!Array.isArray(parsed)) {
      ElMessage.error('步骤定义必须是 JSON 数组')
      return
    }
    steps = parsed
  } catch {
    ElMessage.error('步骤定义必须是合法 JSON 数组')
    return
  }
  const payload = {
    project_id: form.project_id,
    name: form.name,
    device_id: form.device_id,
    app_package: form.app_package,
    app_activity: form.app_activity,
    script_path: form.script_path,
    steps,
    assert_keyword: form.assert_keyword
  }
  if (editingId.value) {
    await http.put(`/app-case/${editingId.value}`, payload)
  } else {
    await http.post('/app-case/create', payload)
  }
  visible.value = false
  ElMessage.success(editingId.value ? '更新成功' : '创建成功')
  await fetchCases()
}

const runCase = async (id: number) => {
  const { data } = await http.post(`/app-case/run/${id}`)
  ElMessage.success(`执行完成：${data.status === 'passed' ? '通过' : '失败'}`)
}

const removeCase = async (id: number) => {
  await http.delete(`/app-case/${id}`)
  ElMessage.success('删除成功')
  await fetchCases()
}

onMounted(fetchCases)
</script>
