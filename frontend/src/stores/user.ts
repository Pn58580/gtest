import { defineStore } from 'pinia'
import { http } from '../api/http'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('access_token') || ''
  }),
  actions: {
    async login(username: string, password: string) {
      const { data } = await http.post('/auth/login', { username, password })
      this.token = data.access_token
      localStorage.setItem('access_token', data.access_token)
    },
    logout() {
      this.token = ''
      localStorage.removeItem('access_token')
    }
  }
})
