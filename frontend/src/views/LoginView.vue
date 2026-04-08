<template>
  <div class="login-page">
    <div class="login-bg-pattern"></div>

    <!-- Theme toggle — top-right corner -->
    <div style="position: fixed; top: 18px; right: 24px; z-index: 100;">
      <ThemeToggle />
    </div>

    <!-- Decorative elements -->
    <div class="login-deco login-deco-1"></div>
    <div class="login-deco login-deco-2"></div>

    <div class="login-card fade-in">

      <!-- Logo -->
      <div class="login-logo">
        <div class="login-logo-gem">✦</div>
        <div class="login-logo-text">Glow Suite</div>
        <div class="login-logo-sub">Luxury Beauty Management</div>
      </div>

      <!-- Registration Success -->
      <div v-if="regSuccess" class="alert alert-success" style="background: rgba(39,174,96,0.1); border-color: #27ae60; color: #a8f0c0; border-radius: var(--r-sm)">
        ✓ Account created! You may now sign in.
      </div>

      <!-- LOGIN MODE -->
      <template v-if="tab !== 'register'">
        <div class="login-tabs">
          <button
            v-for="t in ['owner', 'manager', 'staff', 'customer']"
            :key="t"
            :class="['login-tab', { active: tab === t }]"
            @click="switchTab(t)"
          >
            {{ t.charAt(0).toUpperCase() + t.slice(1) }}
          </button>
        </div>

        <div v-if="error" class="login-error">{{ error }}</div>

        <div class="form-group">
          <label class="form-label">{{ tab === 'customer' ? 'Email Address' : 'User ID' }}</label>
          <input
            v-if="tab !== 'customer'"
            v-model="form.userId"
            type="text"
            class="form-input"
            :placeholder="tab === 'owner' ? 'owner' : tab === 'manager' ? 'manager' : 'staff user ID'"
            autocomplete="username"
          />
          <input
            v-else
            v-model="form.email"
            type="email"
            class="form-input"
            placeholder="your@email.com"
            autocomplete="email"
          />
        </div>

        <div class="form-group">
          <label class="form-label">Password</label>
          <div style="position: relative; display: flex; align-items: center">
            <input
              v-model="form.password"
              :type="showLoginPassword ? 'text' : 'password'"
              class="form-input"
              placeholder="••••••••"
              @keydown.enter="login"
              autocomplete="current-password"
            />
            <button type="button" @click="showLoginPassword = !showLoginPassword" style="position: absolute; right: 12px; background: none; border: none; cursor: pointer; font-size: 18px; color: var(--text-muted); padding: 4px">
              {{ showLoginPassword ? '👁️' : '👁️‍🗨️' }}
            </button>
          </div>
        </div>

        <button
          class="btn w-full"
          style="background: linear-gradient(135deg, var(--gold-deep), var(--gold), var(--gold-bright)); color: var(--obsidian); border: none; padding: 14px; font-size: 11px; letter-spacing: 0.18em; font-weight: 700; margin-top: 4px; border-radius: var(--r-sm)"
          @click="login"
          :disabled="isLoading"
        >
          <span v-if="isLoading" class="login-loading">
            <span class="login-dot"></span>
            <span class="login-dot"></span>
            <span class="login-dot"></span>
          </span>
          <span v-else>Sign In</span>
        </button>

        <template v-if="tab === 'customer'">
          <div class="login-divider">or</div>
          <button
            class="btn btn-outline w-full"
            style="border-color: var(--border-strong); color: var(--text-muted); font-size: 11px; letter-spacing: 0.12em"
            @click="switchTab('register')"
          >
            Create Account
          </button>
        </template>

      </template>

      <!-- REGISTER MODE -->
      <template v-else>
        <button
          class="login-back"
          @click="switchTab('customer')"
        >
          ← Back to Sign In
        </button>

        <div v-if="error" class="login-error">{{ error }}</div>

        <div class="form-group">
          <label class="form-label">Full Name *</label>
          <input v-model="regForm.name" type="text" class="form-input" placeholder="Your full name" />
        </div>

        <div class="form-group">
          <label class="form-label">Email Address *</label>
          <input v-model="regForm.email" type="email" class="form-input" placeholder="your@email.com" />
        </div>

        <div class="register-grid">
          <div class="form-group">
            <label class="form-label">Date of Birth</label>
            <input v-model="regForm.dob" type="date" class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">Phone</label>
            <input v-model="regForm.phone" type="text" class="form-input" placeholder="+1 234 567 8900" />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Address <span style="opacity: 0.4; font-size: 9px">(optional)</span></label>
          <input v-model="regForm.address" type="text" class="form-input" placeholder="Your address" />
        </div>

        <div class="form-group">
          <label class="form-label">Password *</label>
          <div style="position: relative; display: flex; align-items: center">
            <input v-model="regForm.password" :type="showRegPassword ? 'text' : 'password'" class="form-input" placeholder="Min. 8 characters" />
            <button type="button" @click="showRegPassword = !showRegPassword" style="position: absolute; right: 12px; background: none; border: none; cursor: pointer; font-size: 18px; color: var(--text-muted); padding: 4px">
              {{ showRegPassword ? '👁️' : '👁️‍🗨️' }}
            </button>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label" style="margin-bottom: 10px; display: block">Service Preferences</label>
          <div class="preferences-group">
            <label
              v-for="service in preferenceOptions"
              :key="service"
              class="preference-checkbox"
            >
              <input v-model="regForm.preferences" type="checkbox" :value="service" />
              <span>{{ service }}</span>
            </label>
          </div>
        </div>

        <button
          class="btn w-full"
          style="background: linear-gradient(135deg, var(--gold-deep), var(--gold), var(--gold-bright)); color: var(--obsidian); border: none; padding: 14px; font-size: 11px; letter-spacing: 0.18em; font-weight: 700; margin-top: 4px; border-radius: var(--r-sm)"
          @click="register"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Creating Account…' : 'Create Account' }}
        </button>
      </template>

    </div>

    <!-- Side tagline -->
    <div class="login-tagline">
      <div class="login-tagline-text">
        "Excellence is not a destination — it is a continuous journey."
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAppStore } from '@/stores/appStore'
import ThemeToggle from '@/components/ThemeToggle.vue'

const router    = useRouter()
const route     = useRoute()
const appStore  = useAppStore()
const API_BASE_URL = 'http://localhost:5000'

const tab        = ref('manager')
const form       = reactive({ userId: '', email: '', password: '' })
const regForm    = reactive({ name: '', email: '', phone: '', password: '', address: '', dob: '', preferences: [] })
const error      = ref('')
const regSuccess = ref(false)
const isLoading  = ref(false)
const showLoginPassword = ref(false)
const showRegPassword = ref(false)

const preferenceOptions = ['Facial', 'Hair Care', 'Massage', 'Manicure', 'Pedicure', 'Threading', 'Waxing']

const switchTab = (newTab) => {
  tab.value   = newTab
  error.value = ''
  if (newTab !== 'register') router.replace(`/login/${newTab}`)
}

watch(() => route.path, (path) => {
  const role = path.split('/')[2]
  if (['owner', 'manager', 'staff', 'customer'].includes(role)) {
    tab.value   = role
    error.value = ''
  }
}, { immediate: true })

const login = async () => {
  error.value    = ''
  isLoading.value = true
  try {
    const endpoints = {
      owner:    `${API_BASE_URL}/owner-login`,
      manager:  `${API_BASE_URL}/manager-login`,
      staff:    `${API_BASE_URL}/staff-login`,
      customer: `${API_BASE_URL}/customer-login`,
    }
    const payload = tab.value === 'customer'
      ? { username: form.email,  password: form.password }
      : { username: form.userId, password: form.password }

    const res  = await fetch(endpoints[tab.value], {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    const data = await res.json()

    if (res.ok && data.token) {
      const user = { username: data.username || payload.username, role: (data.role || tab.value).toLowerCase(), id: data.userId }
      localStorage.setItem('authToken', data.token)
      localStorage.setItem('user', JSON.stringify(user))
      appStore.login({ token: data.token, ...user })
      const routes = { owner: '/owner-dashboard', manager: '/manager-dashboard', staff: '/staff-dashboard', customer: '/customer-dashboard' }
      router.push(routes[user.role] || '/dashboard')
    } else {
      error.value = data.message || 'Invalid credentials. Please try again.'
    }
  } catch {
    error.value = 'Connection error. Please check the backend is running.'
  } finally {
    isLoading.value = false
  }
}

const register = async () => {
  if (!regForm.name || !regForm.email || !regForm.password || !regForm.dob || !regForm.phone) {
    error.value = 'Please fill in all required fields.'
    return
  }
  isLoading.value = true
  try {
    const res  = await fetch(`${API_BASE_URL}/register-customer`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: regForm.name, email: regForm.email, phone: regForm.phone, address: regForm.address, password: regForm.password, dob: regForm.dob, preferences: regForm.preferences }),
    })
    const data = await res.json()
    if (res.status === 201 || data.customer_id) {
      regSuccess.value = true
      error.value = ''
      tab.value  = 'customer'
      form.email = regForm.email
    } else {
      error.value = data.message || 'Registration failed.'
    }
  } catch {
    error.value = 'Connection error.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* ─── DECORATIVE ─── */
.login-deco {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(201,169,110,0.10);
  pointer-events: none;
}

.login-deco-1 {
  width: 600px; height: 600px;
  top: -200px; left: -200px;
}

.login-deco-2 {
  width: 400px; height: 400px;
  bottom: -150px; right: -150px;
}

/* ─── GEM ─── */
.login-logo-gem {
  font-size: 24px;
  color: var(--gold);
  margin-bottom: 8px;
  animation: shimmer 2.5s ease-in-out infinite;
}

/* ─── ERROR ─── */
.login-error {
  background: rgba(192,57,43,0.12);
  border: 1px solid rgba(231,76,60,0.3);
  color: #ff8a80;
  padding: 11px 16px;
  border-radius: var(--r-sm);
  font-size: 12.5px;
  margin-bottom: 18px;
  letter-spacing: 0.01em;
}

/* ─── BACK BUTTON ─── */
.login-back {
  display: flex;
  align-items: center;
  gap: 6px;
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 11px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  cursor: pointer;
  margin-bottom: 24px;
  padding: 0;
  font-family: var(--font-body);
  transition: color var(--t-fast);
}

.login-back:hover { color: var(--gold-pale); }

/* ─── REGISTER GRID ─── */
.register-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

/* ─── PREFERENCES ─── */
.preferences-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
}

/* ─── LOADING DOTS ─── */
.login-loading {
  display: flex;
  gap: 5px;
  align-items: center;
  justify-content: center;
}

.login-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--obsidian);
  animation: dot-bounce 1s ease-in-out infinite;
}

.login-dot:nth-child(2) { animation-delay: 0.15s; }
.login-dot:nth-child(3) { animation-delay: 0.30s; }

@keyframes dot-bounce {
  0%, 80%, 100% { transform: translateY(0); opacity: 0.5; }
  40%           { transform: translateY(-5px); opacity: 1; }
}

/* ─── TAGLINE ─── */
.login-tagline {
  position: fixed;
  bottom: 32px;
  left: 40px;
  max-width: 260px;
  z-index: 0;
}

.login-tagline-text {
  font-family: var(--font-display);
  font-style: italic;
  font-size: 12px;
  color: var(--divider);
  line-height: 1.7;
  letter-spacing: 0.01em;
}

@media (max-width: 768px) {
  .login-tagline { display: none; }
  .register-grid { grid-template-columns: 1fr; }
  .preferences-group { grid-template-columns: 1fr; }
  .login-deco { display: none; }
}
</style>