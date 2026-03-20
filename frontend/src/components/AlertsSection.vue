<template>
  <div class="alerts-section">
    <div class="alerts-container">
      <h3>Notifications 🔔</h3>
      
      <div v-if="unreadAlerts.length > 0" class="unread-alerts">
        <div v-for="alert in unreadAlerts" :key="alert.id" class="alert-item" :class="`alert-${alert.type}`">
          <div class="alert-icon">{{ getAlertIcon(alert.type) }}</div>
          <div class="alert-content">
            <div class="alert-title">{{ alert.title }}</div>
            <div class="alert-message">{{ alert.message }}</div>
            <div class="alert-time">{{ getTimeAgo(alert.date) }}</div>
          </div>
          <button class="alert-close" @click="markAsRead(alert.id)">✓</button>
        </div>
      </div>

      <div v-if="unreadAlerts.length === 0" class="no-alerts">
        <div class="no-alerts-icon">✨</div>
        <p>All caught up! You have no new notifications</p>
      </div>

      <div v-if="readAlerts.length > 0" class="read-alerts-section">
        <button class="expand-btn" @click="showReadAlerts = !showReadAlerts">
          {{ showReadAlerts ? '▼' : '▶' }} Previous Notifications ({{ readAlerts.length }})
        </button>

        <div v-if="showReadAlerts" class="read-alerts">
          <div v-for="alert in readAlerts" :key="alert.id" class="alert-item read" :class="`alert-${alert.type}`">
            <div class="alert-icon">{{ getAlertIcon(alert.type) }}</div>
            <div class="alert-content">
              <div class="alert-title">{{ alert.title }}</div>
              <div class="alert-message">{{ alert.message }}</div>
              <div class="alert-time">{{ getTimeAgo(alert.date) }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const showReadAlerts = ref(false)
const alerts = ref([
  {
    id: 1,
    type: 'reward_expiry',
    title: '⏰ Reward Points Expiring Soon!',
    message: '50 points will expire in 7 days. Use them before they go away!',
    date: new Date(Date.now() - 2 * 60 * 60 * 1000),
    isRead: false
  },
  {
    id: 2,
    type: 'birthday',
    title: '🎂 Birthday Offer Available!',
    message: 'Claim your exclusive 20% discount on your birthday month!',
    date: new Date(Date.now() - 5 * 60 * 60 * 1000),
    isRead: false
  },
  {
    id: 3,
    type: 'appointment_reminder',
    title: '📅 Appointment Reminder',
    message: 'You have a facial appointment tomorrow at 3:00 PM',
    date: new Date(Date.now() - 24 * 60 * 60 * 1000),
    isRead: true
  },
  {
    id: 4,
    type: 'reward_earned',
    title: '🎉 Reward Points Earned!',
    message: 'You earned 50 points from your recent booking',
    date: new Date(Date.now() - 48 * 60 * 60 * 1000),
    isRead: true
  }
])

const unreadAlerts = computed(() => alerts.value.filter(a => !a.isRead))
const readAlerts = computed(() => alerts.value.filter(a => a.isRead))

const getAlertIcon = (type) => {
  const icons = {
    reward_expiry: '⏰',
    birthday: '🎂',
    appointment_reminder: '📅',
    reward_earned: '🎉',
    promotion: '🎁'
  }
  return icons[type] || '📌'
}

const getTimeAgo = (date) => {
  const now = new Date()
  const diff = Math.floor((now - date) / 1000)
  
  if (diff < 60) return 'just now'
  if (diff < 3600) return `${Math.floor(diff / 60)} minutes ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)} hours ago`
  return `${Math.floor(diff / 86400)} days ago`
}

const markAsRead = (alertId) => {
  const alert = alerts.value.find(a => a.id === alertId)
  if (alert) alert.isRead = true
}
</script>

<style scoped>
.alerts-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 24px;
  margin: 24px 0;
}

h3 {
  margin: 0 0 16px 0;
  font-size: 18px;
  color: #333;
}

.unread-alerts {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.alert-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  border-radius: 6px;
  border-left: 4px solid #ddd;
  background: #f9f9f9;
  transition: all 0.3s ease;
}

.alert-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.alert-item.read {
  opacity: 0.7;
}

.alert-item.alert-reward_expiry {
  border-left-color: #ff9800;
  background: rgba(255, 152, 0, 0.05);
}

.alert-item.alert-birthday {
  border-left-color: #e91e63;
  background: rgba(233, 30, 99, 0.05);
}

.alert-item.alert-appointment_reminder {
  border-left-color: #2196f3;
  background: rgba(33, 150, 243, 0.05);
}

.alert-item.alert-reward_earned {
  border-left-color: #4caf50;
  background: rgba(76, 175, 80, 0.05);
}

.alert-item.alert-promotion {
  border-left-color: #9c27b0;
  background: rgba(156, 39, 176, 0.05);
}

.alert-icon {
  font-size: 24px;
  min-width: 32px;
  text-align: center;
}

.alert-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.alert-title {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.alert-message {
  color: #666;
  font-size: 13px;
  line-height: 1.4;
}

.alert-time {
  color: #999;
  font-size: 11px;
}

.alert-close {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #999;
  padding: 4px 8px;
  transition: color 0.3s ease;
  align-self: flex-start;
}

.alert-close:hover {
  color: #4caf50;
}

.no-alerts {
  text-align: center;
  padding: 32px 24px;
  color: #999;
}

.no-alerts-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.no-alerts p {
  margin: 0;
  font-size: 14px;
}

.read-alerts-section {
  border-top: 1px solid #ddd;
  padding-top: 16px;
}

.expand-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #666;
  font-weight: 500;
  font-size: 13px;
  padding: 8px 0;
  transition: color 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.expand-btn:hover {
  color: var(--gold);
}

.read-alerts {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 12px;
}

@media (max-width: 768px) {
  .alert-item {
    flex-direction: column;
    gap: 8px;
  }

  .alert-close {
    align-self: flex-end;
  }
}
</style>
