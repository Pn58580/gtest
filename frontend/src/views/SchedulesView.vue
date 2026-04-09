<template>
  <el-card>
    <template #header>
      <div class="flex items-center justify-between">
        <span>定时任务</span>
        <el-button type="primary" @click="createSchedule">新增任务</el-button>
      </div>
    </template>

    <el-table :data="schedules" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="任务名" />
      <el-table-column prop="cron" label="CRON" width="140" />
      <el-table-column prop="engine" label="引擎" width="100" />
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button link type="primary" @click="triggerNow(scope.row.id)">立即执行</el-button>
          <el-button link type="danger" @click="remove(scope.row.id)">删除</el-button>
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
const schedules = ref<Array<Record<string, unknown>>>([])

const fetchList = async () => {
  loading.value = true
  try {
    const { data } = await http.get('/task/schedule/list')
    schedules.value = data
  } finally {
    loading.value = false
  }
}

const createSchedule = async () => {
  const { value } = await ElMessageBox.prompt('请输入任务名称', '新增任务')
  if (!value) return
  await http.post('/task/schedule/create', {
    name: value,
    cron: '*/5 * * * *',
    engine: 'api',
    project_id: 1,
    case_id: 1
  })
  ElMessage.success('创建成功')
  await fetchList()
}

const triggerNow = async (id: number) => {
  await http.post(`/task/schedule/${id}/trigger`)
  ElMessage.success('触发成功')
}

const remove = async (id: number) => {
  await http.delete(`/task/schedule/${id}`)
  ElMessage.success('删除成功')
  await fetchList()
}

onMounted(fetchList)
</script>
