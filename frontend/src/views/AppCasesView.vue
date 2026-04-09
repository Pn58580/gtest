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
      <el-table-column prop="name" label="用例名称" min-width="160" />
      <el-table-column prop="device_id" label="设备" width="130" />
      <el-table-column prop="script_path" label="脚本路径" min-width="220" />
      <el-table-column prop="assert_keyword" label="断言关键字" width="120" />
      <el-table-column label="操作" width="220">
        <template #default="scope">
          <el-button link type="success" @click="runCase(scope.row.id)">执行</el-button>
          <el-button link type="danger" @click="removeCase(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>

  <el-dialog v-model="visible" title="新增APP用例" width="520px">
    <el-form :model="form" label-width="96px">
      <el-form-item label="名称"><el-input v-model="form.name" /></el-form-item>
      <el-form-item label="设备ID"><el-input v-model="form.device_id" /></el-form-item>
      <el-form-item label="脚本路径"><el-input v-model="form.script_path" /></el-form-item>
      <el-form-item label="断言关键字"><el-input v-model="form.assert_keyword" /></el-form-item>
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
  name: 'APP 冒烟用例',
  device_id: 'emulator-5554',
  script_path: 'scripts/login.air',
  assert_keyword: 'success'
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

const openCreate = () => { visible.value = true }

const createCase = async () => {
  await http.post('/app-case/create', form)
  visible.value = false
  ElMessage.success('创建成功')
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
