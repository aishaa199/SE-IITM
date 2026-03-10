import { createRouter, createWebHistory } from 'vue-router'
import { useAppStore } from '@/stores/appStore'
import HomePage from '@/views/HomePage.vue'
import LoginView from '@/views/LoginView.vue'
import DashboardView from '@/views/DashboardView.vue'
import StaffDashboard from '@/views/StaffDashboard.vue'
import CustomerDashboard from '@/views/CustomerDashboard.vue'
import OwnerDashboard from '@/views/OwnerDashboard.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage,
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
  },
  {
    path: '/dashboard',
    name: 'dashboard',
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
  // Dev/Test routes for bypassing auth
  {
    path: '/test/staff',
    name: 'test-staff',
    component: StaffDashboard,
    meta: { testMode: true, testRole: 'staff' }
  },
  {
    path: '/test/customer',
    name: 'test-customer',
    component: CustomerDashboard,
    meta: { testMode: true, testRole: 'customer' }
  },
  {
    path: '/test/manager',
    name: 'test-manager',
    component: DashboardView,
    meta: { testMode: true, testRole: 'manager' }
  },
  {
    path: '/test/owner',
    name: 'test-owner',
    component: OwnerDashboard,
    meta: { testMode: true, testRole: 'owner' }
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const appStore = useAppStore()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const testMode = to.matched.some(record => record.meta.testMode)
  const isLoginPage = to.path === '/'
  
  // Test mode - auto-login with test user
  if (testMode) {
    const testRole = to.meta.testRole
    if (testRole === 'staff') {
      appStore.login({ role: 'staff', userId: 'amara01', name: 'Amara Osei' })
    } else if (testRole === 'customer') {
      appStore.login({ role: 'customer', email: 'sofia@email.com', name: 'Sofia Mensah' })
    } else if (testRole === 'manager') {
      appStore.login({ role: 'manager', userId: 'manager', name: 'Manager' })
    }
    return next()
  }
  
  // If trying to access protected route without auth
  if (requiresAuth && !appStore.isAuthenticated) {
    return next('/')
  }
  
  // If logged in and trying to access login page, redirect to appropriate dashboard
  if (isLoginPage && appStore.isAuthenticated) {
    const userRole = appStore.user?.role?.toLowerCase()
    if (userRole === 'staff') {
      return next('/staff-dashboard')
    } else if (userRole === 'customer') {
      return next('/customer-dashboard')
    } else {
      return next('/dashboard')
    }
  }
  
  // Otherwise, allow navigation
  return next()
})

export default router

