<template>
  <el-card>
    <template #header>
      <div class="font-600">执行中心（API/Web/App）</div>
    </template>

    <el-form :model="form" inline>
      <el-form-item label="项目ID">
        <el-input-number v-model="form.project_id" :min="1" />
      </el-form-item>
      <el-form-item label="用例ID">
        <el-input-number v-model="form.case_id" :min="1" />
      </el-form-item>
      <el-form-item label="引擎">
        <el-select v-model="form.engine" style="width: 120px">
          <el-option label="API" value="api" />
          <el-option label="WEB" value="web" />
          <el-option label="APP" value="app" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" :loading="running" @click="execute">执行</el-button>
      </el-form-item>
      <el-form-item>
        <el-button @click="fetchHistory">刷新历史</el-button>
      </el-form-item>
    </el-form>

    <el-divider />

    <pre v-if="lastResult" class="bg-#0f172a text-#e2e8f0 p-3 rounded mb-4">{{ JSON.stringify(lastResult, null, 2) }}</pre>

    <el-table :data="history" stripe>
      <el-table-column prop="run_id" label="Run ID" min-width="220" />
      <el-table-column prop="engine" label="引擎" width="90" />
      <el-table-column prop="status" label="状态" width="110" />
      <el-table-column prop="duration_ms" label="耗时(ms)" width="120" />
      <el-table-column prop="triggered_by" label="触发人" width="180" />
    </el-table>
  </el-card>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { http } from '../api/http'

const running = ref(false)
const history = ref<Array<Record<string, unknown>>>([])
const lastResult = ref<Record<string, unknown> | null>(null)

const form = reactive({
  project_id: 1,
  case_id: 1,
  engine: 'api',
  triggered_by: 'admin',
  params: {}
})

const fetchHistory = async () => {
  const { data } = await http.get('/run/history?limit=20')
  history.value = data
}

const execute = async () => {
  running.value = true
  try {
    const { data } = await http.post('/run', form)
    lastResult.value = data
    ElMessage.success('执行完成')
    await fetchHistory()
  } finally {
    running.value = false
  }
}

onMounted(fetchHistory)
</script>
