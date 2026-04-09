import { defineStore } from 'pinia'
import { http } from '../api/http'

interface UserProfile {
  id: number
  username: string
  role: string
}

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('access_token') || '',
    profile: null as UserProfile | null
  }),
  getters: {
    isAdmin: (state) => state.profile?.role === 'admin'
  },
  actions: {
    async login(username: string, password: string) {
      const { data } = await http.post('/auth/login', { username, password })
      this.token = data.access_token
      localStorage.setItem('access_token', data.access_token)
      await this.fetchProfile()
    },
    async fetchProfile() {
      if (!this.token) return
      const { data } = await http.get('/auth/me')
      this.profile = data
    },
    logout() {
      this.token = ''
      this.profile = null
      localStorage.removeItem('access_token')
    }
  }
})
