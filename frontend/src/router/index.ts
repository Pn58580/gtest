import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', component: () => import('../views/LoginView.vue') },
    {
      path: '/',
      component: () => import('../layouts/MainLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '', component: () => import('../views/DashboardView.vue') },
        { path: 'projects', component: () => import('../views/ProjectsView.vue') },
        { path: 'runs', component: () => import('../views/RunsView.vue') },
        { path: 'users', component: () => import('../views/UsersView.vue') }
      ]
    }
  ]
})

router.beforeEach((to) => {
  const hasToken = !!localStorage.getItem('access_token')
  if (to.meta.requiresAuth && !hasToken) return '/login'
  if (to.path === '/login' && hasToken) return '/'
  return true
})

export default router
