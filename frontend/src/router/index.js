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
  const isLoginPage = to.path === '/' || to.path.startsWith('/login')
  
  
  // If trying to access protected route without auth
  if (requiresAuth && !appStore.isAuthenticated) {
    return next('/')
  }
  
  // If logged in and trying to access login page, redirect to appropriate dashboard
  if (isLoginPage && appStore.isAuthenticated) {
    const userRole = appStore.user?.role?.toLowerCase()
    if (userRole === 'owner') {
      return next('/owner-dashboard')
    } else if (userRole === 'staff') {
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

