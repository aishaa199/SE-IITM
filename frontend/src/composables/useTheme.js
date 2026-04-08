import { ref } from 'vue'

const isDark = ref(true)

function applyTheme(dark) {
  document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light')
  localStorage.setItem('glow-theme', dark ? 'dark' : 'light')
  isDark.value = dark
}

export function useTheme() {
  function toggleTheme() {
    applyTheme(!isDark.value)
  }

  function initTheme() {
    const saved = localStorage.getItem('glow-theme')
    if (saved) {
      applyTheme(saved === 'dark')
    } else {
      // Default to dark theme
      applyTheme(true)
    }
  }

  return { isDark, toggleTheme, initTheme }
}
