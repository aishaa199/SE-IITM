import { createRouter, createWebHistory } from 'vue-router'
import { useAppStore } from '@/stores/appStore'
import HomePage from '@/views/HomePage.vue'
import LoginView from '@/views/LoginView.vue'
import DashboardView from '@/views/DashboardView.vue'
import StaffDashboard from '@/views/StaffDashboard.vue'
import CustomerDashboard from '@/views/CustomerDashboard.vue'
import OwnerDashboard from '@/views/OwnerDashboard.vue'
import ResetPasswordView from '@/views/ResetPasswordView.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage,
  },
  {
    path: '/login',
    redirect: '/login/manager',
  },
  {
    path: '/login/owner',
    name: 'login-owner',
    component: LoginView,
    meta: { loginRole: 'owner' }
  },
  {
    path: '/login/manager',
    name: 'login-manager',
    component: LoginView,
    meta: { loginRole: 'manager' }
  },
  {
    path: '/login/staff',
    name: 'login-staff',
    component: LoginView,
    meta: { loginRole: 'staff' }
  },
  {
    path: '/login/customer',
    name: 'login-customer',
    component: LoginView,
    meta: { loginRole: 'customer' }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/manager-dashboard',
    name: 'manager-dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/staff-dashboard',
    name: 'staff-dashboard',
    component: StaffDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/customer-dashboard',
    name: 'customer-dashboard',
    component: CustomerDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/owner-dashboard',
    name: 'owner-dashboard',
    component: OwnerDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/reset-password',
    name: 'reset-password',
    component: ResetPasswordView
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to) => {
  const appStore = useAppStore()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const isLoginPage = to.path === '/' || to.path.startsWith('/login')

  if (requiresAuth && !appStore.isAuthenticated) {
    return '/'
  }

  if (isLoginPage && appStore.isAuthenticated) {
    const userRole = appStore.user?.role?.toLowerCase()
    if (userRole === 'owner')    return '/owner-dashboard'
    if (userRole === 'manager')  return '/manager-dashboard'
    if (userRole === 'staff')    return '/staff-dashboard'
    if (userRole === 'customer') return '/customer-dashboard'
    return '/dashboard'
  }
})

export default router

