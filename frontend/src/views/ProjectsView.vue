<template>
  <el-card>
    <template #header>
      <div class="flex items-center justify-between">
        <span>项目管理</span>
        <el-button type="primary" @click="createProject">新增项目</el-button>
      </div>
    </template>

    <el-table :data="projects" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="项目名称" />
      <el-table-column prop="owner_id" label="Owner" width="120" />
      <el-table-column label="操作" width="120">
        <template #default="scope">
          <el-button type="danger" link @click="removeProject(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { http } from '../api/http'

interface Project {
  id: number
  name: string
  owner_id: number
}

const loading = ref(false)
const projects = ref<Project[]>([])

const fetchProjects = async () => {
  loading.value = true
  try {
    const { data } = await http.get<Project[]>('/project/list')
    projects.value = data
  } finally {
    loading.value = false
  }
}

const createProject = async () => {
  const { value } = await ElMessageBox.prompt('请输入项目名称', '新增项目')
  if (!value) return
  await http.post('/project/create', { name: value })
  ElMessage.success('创建成功')
  await fetchProjects()
}

const removeProject = async (id: number) => {
  await http.delete(`/project/${id}`)
  ElMessage.success('删除成功')
  await fetchProjects()
}

onMounted(fetchProjects)
</script>
