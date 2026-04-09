<template>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
    <el-card>
      <div class="text-#64748b">API 执行数</div>
      <div class="text-32px font-700">{{ stats.api_runs }}</div>
    </el-card>
    <el-card>
      <div class="text-#64748b">Web 执行数</div>
      <div class="text-32px font-700">{{ stats.web_runs }}</div>
    </el-card>
    <el-card>
      <div class="text-#64748b">App 执行数</div>
      <div class="text-32px font-700">{{ stats.app_runs }}</div>
    </el-card>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
    <el-card>
      <div class="text-#64748b">总执行数</div>
      <div class="text-28px font-700">{{ stats.total_runs }}</div>
    </el-card>
    <el-card>
      <div class="text-#16a34a">通过数</div>
      <div class="text-28px font-700 text-#16a34a">{{ stats.passed_runs }}</div>
    </el-card>
    <el-card>
      <div class="text-#dc2626">失败数</div>
      <div class="text-28px font-700 text-#dc2626">{{ stats.failed_runs }}</div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive } from 'vue'
import { http } from '../api/http'

const stats = reactive({
  total_runs: 0,
  passed_runs: 0,
  failed_runs: 0,
  api_runs: 0,
  web_runs: 0,
  app_runs: 0
})

const fetchStats = async () => {
  const { data } = await http.get('/report/stats')
  Object.assign(stats, data)
}

onMounted(fetchStats)
</script>
