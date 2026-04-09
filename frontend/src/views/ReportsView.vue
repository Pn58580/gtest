<template>
  <el-card>
    <template #header>
      <div class="flex items-center justify-between">
        <span>测试报告</span>
        <el-button @click="fetchReports">刷新</el-button>
      </div>
    </template>

    <el-table :data="reports" v-loading="loading" stripe>
      <el-table-column prop="run_id" label="Run ID" min-width="220" />
      <el-table-column prop="engine" label="引擎" width="90" />
      <el-table-column prop="status" label="状态" width="100" />
      <el-table-column prop="duration_ms" label="耗时(ms)" width="120" />
      <el-table-column prop="triggered_by" label="触发人" width="160" />
    </el-table>
  </el-card>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { http } from '../api/http'

const loading = ref(false)
const reports = ref<Array<Record<string, unknown>>>([])

const fetchReports = async () => {
  loading.value = true
  try {
    const { data } = await http.get('/report/recent?limit=50')
    reports.value = data
  } finally {
    loading.value = false
  }
}

onMounted(fetchReports)
</script>
