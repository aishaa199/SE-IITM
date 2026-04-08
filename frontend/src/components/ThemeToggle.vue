<template>
  <button
    class="theme-toggle-btn"
    @click="toggleTheme"
    :title="isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
    :aria-label="isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
  >
    <!-- Sun: shown in dark mode, click → go light -->
    <svg v-if="isDark" viewBox="0 0 24 24" width="18" height="18" fill="none"
      stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="5"/>
      <line x1="12" y1="1" x2="12" y2="3"/>
      <line x1="12" y1="21" x2="12" y2="23"/>
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
      <line x1="1" y1="12" x2="3" y2="12"/>
      <line x1="21" y1="12" x2="23" y2="12"/>
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
    </svg>
    <!-- Moon: shown in light mode, click → go dark -->
    <svg v-else viewBox="0 0 24 24" width="18" height="18" fill="none"
      stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
    </svg>
    <span class="theme-toggle-label">{{ isDark ? 'Light' : 'Dark' }}</span>
  </button>
</template>

<script setup>
import { useTheme } from '@/composables/useTheme'
const { isDark, toggleTheme } = useTheme()
</script>

<style scoped>
.theme-toggle-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 13px;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 20px;
  cursor: pointer;
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.04em;
  transition: all 0.2s ease;
  white-space: nowrap;
}
.theme-toggle-btn:hover {
  border-color: var(--gold);
  color: var(--gold);
  background: rgba(212, 175, 55, 0.06);
}
.theme-toggle-btn svg {
  flex-shrink: 0;
  transition: transform 0.3s ease;
}
.theme-toggle-btn:hover svg {
  transform: rotate(15deg);
}
</style>
