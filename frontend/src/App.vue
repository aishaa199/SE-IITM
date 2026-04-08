<template>
  <RouterView />
</template>

<script setup>
import { RouterView } from 'vue-router';
import { onMounted, onUnmounted } from 'vue';
import { useTheme } from '@/composables/useTheme';

const { initTheme } = useTheme();

// ── Custom Cursor ────────────────────────────────────────────────
let cursorDot = null
let cursorRing = null
let mouseX = 0, mouseY = 0
let ringX = 0, ringY = 0
let rafId = null

const INTERACTIVE = 'a, button, [role="button"], label, .btn, .nav-item, ' +
  '.nav-link, .feature-card, .service-card-home, .card, .report-item, ' +
  '.stat-card, .stat-card-dark, .booking-item, select, [tabindex], ' +
  'input[type="checkbox"], input[type="radio"], .theme-toggle-btn, ' +
  '.profile-menu-item, .dropdown-option, .nav-item'

function onMouseMove(e) {
  mouseX = e.clientX
  mouseY = e.clientY
  if (cursorDot) {
    cursorDot.style.left = mouseX + 'px'
    cursorDot.style.top  = mouseY + 'px'
  }
}

function animateRing() {
  // Smooth lag follow for ring
  const ease = 0.11
  ringX += (mouseX - ringX) * ease
  ringY += (mouseY - ringY) * ease
  if (cursorRing) {
    cursorRing.style.left = ringX + 'px'
    cursorRing.style.top  = ringY + 'px'
  }
  rafId = requestAnimationFrame(animateRing)
}

function onMouseOver(e) {
  if (e.target.closest(INTERACTIVE)) {
    cursorDot?.classList.add('is-hovering')
    cursorRing?.classList.add('is-hovering')
  }
}

function onMouseOut(e) {
  if (e.target.closest(INTERACTIVE)) {
    cursorDot?.classList.remove('is-hovering')
    cursorRing?.classList.remove('is-hovering')
  }
}

function onMouseDown() {
  cursorDot?.classList.add('is-clicking')
  cursorRing?.classList.add('is-clicking')
}

function onMouseUp() {
  cursorDot?.classList.remove('is-clicking')
  cursorRing?.classList.remove('is-clicking')
}

function onMouseEnter() {
  if (cursorDot) cursorDot.style.opacity = '1'
  if (cursorRing) cursorRing.style.opacity = '1'
}

function onMouseLeave() {
  if (cursorDot) cursorDot.style.opacity = '0'
  if (cursorRing) cursorRing.style.opacity = '0'
}

function initCursor() {
  // Skip on touch-only devices
  if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return

  cursorDot = document.createElement('div')
  cursorDot.className = 'cursor-dot'
  cursorDot.style.opacity = '0'

  cursorRing = document.createElement('div')
  cursorRing.className = 'cursor-ring'
  cursorRing.style.opacity = '0'

  document.body.appendChild(cursorDot)
  document.body.appendChild(cursorRing)

  document.addEventListener('mousemove',  onMouseMove,  { passive: true })
  document.addEventListener('mouseover',  onMouseOver,  { passive: true })
  document.addEventListener('mouseout',   onMouseOut,   { passive: true })
  document.addEventListener('mousedown',  onMouseDown)
  document.addEventListener('mouseup',    onMouseUp)
  document.addEventListener('mouseenter', onMouseEnter)
  document.addEventListener('mouseleave', onMouseLeave)

  animateRing()
}

function destroyCursor() {
  if (rafId) cancelAnimationFrame(rafId)
  cursorDot?.remove()
  cursorRing?.remove()
  document.removeEventListener('mousemove',  onMouseMove)
  document.removeEventListener('mouseover',  onMouseOver)
  document.removeEventListener('mouseout',   onMouseOut)
  document.removeEventListener('mousedown',  onMouseDown)
  document.removeEventListener('mouseup',    onMouseUp)
  document.removeEventListener('mouseenter', onMouseEnter)
  document.removeEventListener('mouseleave', onMouseLeave)
}

onMounted(() => {
  initTheme()
  initCursor()
})

onUnmounted(() => {
  destroyCursor()
})
</script>

<style scoped>
</style>
