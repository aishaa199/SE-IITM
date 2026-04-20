<template>
  <div class="login-page">
    <div class="login-bg-pattern"></div>
    <div class="login-deco login-deco-1"></div>
    <div class="login-deco login-deco-2"></div>

    <div class="login-card fade-in">
      <div class="login-logo">
        <div class="login-logo-gem">✦</div>
        <div class="login-logo-text">Glow Suite</div>
        <div class="login-logo-sub">Luxury Beauty Management</div>
      </div>

      <!-- Invalid / missing token -->
      <template v-if="!token">
        <div class="login-error">Invalid reset link. Please request a new one.</div>
        <button class="btn btn-outline w-full" style="margin-top: 16px; border-color: rgba(201,169,110,0.25); color: rgba(255,255,255,0.5); font-size: 11px; letter-spacing: 0.12em" @click="$router.push('/login/customer')">
          Back to Sign In
        </button>
      </template>

      <!-- Success state -->
      <template v-else-if="success">
        <div style="text-align: center; padding: 20px 0">
          <div style="font-size: 40px; margin-bottom: 16px">✓</div>
          <p style="color: rgba(201,169,110,0.9); font-size: 13px; font-weight: 600; margin-bottom: 8px">Password Updated!</p>
          <p style="color: rgba(255,255,255,0.5); font-size: 12px; line-height: 1.6; margin-bottom: 20px">
            Your password has been reset successfully. You can now sign in with your new password.
          </p>
          <button
            class="btn w-full"
            style="background: linear-gradient(135deg, var(--gold-deep), var(--gold), var(--gold-bright)); color: var(--obsidian); border: none; padding: 14px; font-size: 11px; letter-spacing: 0.18em; font-weight: 700; border-radius: var(--r-sm)"
            @click="$router.push('/login/customer')"
          >
            Sign In
          </button>
        </div>
      </template>

      <!-- Reset form -->
      <template v-else>
        <p style="color: rgba(255,255,255,0.6); font-size: 13px; font-weight: 600; margin-bottom: 4px">Set New Password</p>
        <p style="color: rgba(255,255,255,0.4); font-size: 11px; margin-bottom: 20px">Choose a strong password for your account.</p>

        <div v-if="error" class="login-error">{{ error }}</div>

        <div class="form-group">
          <label class="form-label">New Password</label>
          <div style="position: relative; display: flex; align-items: center">
            <input
              v-model="newPassword"
              :type="showPassword ? 'text' : 'password'"
              class="form-input"
              placeholder="Min. 6 characters"
              autocomplete="new-password"
            />
            <button type="button" @click="showPassword = !showPassword" style="position: absolute; right: 12px; background: none; border: none; cursor: pointer; font-size: 18px; color: rgba(255,255,255,0.5); padding: 4px">
              {{ showPassword ? '👁️' : '👁️‍🗨️' }}
            </button>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Confirm Password</label>
          <div style="position: relative; display: flex; align-items: center">
            <input
              v-model="confirmPassword"
              :type="showConfirm ? 'text' : 'password'"
              class="form-input"
              placeholder="Re-enter new password"
              autocomplete="new-password"
              @keydown.enter="resetPassword"
            />
            <button type="button" @click="showConfirm = !showConfirm" style="position: absolute; right: 12px; background: none; border: none; cursor: pointer; font-size: 18px; color: rgba(255,255,255,0.5); padding: 4px">
              {{ showConfirm ? '👁️' : '👁️‍🗨️' }}
            </button>
          </div>
        </div>

        <button
          class="btn w-full"
          style="background: linear-gradient(135deg, var(--gold-deep), var(--gold), var(--gold-bright)); color: var(--obsidian); border: none; padding: 14px; font-size: 11px; letter-spacing: 0.18em; font-weight: 700; margin-top: 4px; border-radius: var(--r-sm)"
          @click="resetPassword"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Updating…' : 'Reset Password' }}
        </button>
      </template>
    </div>

    <div class="login-tagline">
      <div class="login-tagline-text">"Excellence is not a destination — it is a continuous journey."</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route  = useRoute()
const router = useRouter()
const API_BASE_URL = 'http://localhost:5000'

const token           = ref(route.query.token || '')
const newPassword     = ref('')
const confirmPassword = ref('')
const showPassword    = ref(false)
const showConfirm     = ref(false)
const error           = ref('')
const isLoading       = ref(false)
const success         = ref(false)

const resetPassword = async () => {
  error.value = ''
  if (!newPassword.value || newPassword.value.length < 6) {
    error.value = 'Password must be at least 6 characters.'
    return
  }
  if (newPassword.value !== confirmPassword.value) {
    error.value = 'Passwords do not match.'
    return
  }
  isLoading.value = true
  try {
    const res  = await fetch(`${API_BASE_URL}/reset-password`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token: token.value, new_password: newPassword.value })
    })
    const data = await res.json()
    if (res.ok) {
      success.value = true
    } else {
      error.value = data.message || 'Failed to reset password. The link may have expired.'
    }
  } catch {
    error.value = 'Connection error. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>
