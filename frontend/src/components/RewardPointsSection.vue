<template>
  <div class="reward-section">
    <div class="progress-card">
      <h3>Your Reward Points 🎁</h3>
      <div class="points-display">
        <div class="points-value">{{ totalPoints }}</div>
        <div class="points-label">Points</div>
      </div>
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: (totalPoints / 500) * 100 + '%' }"></div>
      </div>
      <div class="progress-text">{{ totalPoints }} / 500 points to premium status</div>
    </div>

    <div class="transactions-card">
      <h3>Recent Transactions</h3>
      <div class="filter-buttons">
        <button 
          v-for="type in ['all', 'earned', 'spent']" 
          :key="type"
          :class="['filter-btn', { active: filterType === type }]"
          @click="filterType = type"
        >
          {{ type.charAt(0).toUpperCase() + type.slice(1) }}
        </button>
      </div>

      <div v-if="filteredTransactions.length === 0" class="empty-state">
        No transactions found
      </div>

      <div v-else class="transaction-list">
        <div v-for="txn in filteredTransactions" :key="txn.id" class="transaction-item">
          <div class="transaction-info">
            <div class="transaction-type" :class="txn.type">
              {{ txn.type === 'earned' ? '📈 Earned' : '📉 Spent' }}
            </div>
            <div class="transaction-date">{{ formatDate(txn.date) }}</div>
          </div>
          <div class="transaction-points" :class="txn.type">
            {{ txn.type === 'earned' ? '+' : '-' }}{{ txn.points }}
          </div>
        </div>
      </div>

      <div class="summary">
        <div class="summary-item">
          <span>Total Earned:</span>
          <span>{{ totalEarned }}</span>
        </div>
        <div class="summary-item">
          <span>Total Spent:</span>
          <span>{{ totalSpent }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const filterType = ref('all')
const totalPoints = ref(325)
const transactions = ref([
  { id: 1, type: 'earned', points: 50, date: new Date('2025-03-15') },
  { id: 2, type: 'spent', points: 25, date: new Date('2025-03-10') },
  { id: 3, type: 'earned', points: 100, date: new Date('2025-03-05') },
  { id: 4, type: 'spent', points: 50, date: new Date('2025-02-28') },
  { id: 5, type: 'earned', points: 150, date: new Date('2025-02-20') },
  { id: 6, type: 'spent', points: 30, date: new Date('2025-02-15') }
])

const filteredTransactions = computed(() => {
  if (filterType.value === 'all') return transactions.value
  return transactions.value.filter(t => t.type === filterType.value)
})

const totalEarned = computed(() => 
  transactions.value.filter(t => t.type === 'earned').reduce((sum, t) => sum + t.points, 0)
)

const totalSpent = computed(() => 
  transactions.value.filter(t => t.type === 'spent').reduce((sum, t) => sum + t.points, 0)
)

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}
</script>

<style scoped>
.reward-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin: 24px 0;
}

.progress-card, .transactions-card {
  background: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h3 {
  margin: 0 0 16px 0;
  font-size: 18px;
  color: #333;
}

.points-display {
  text-align: center;
  margin: 24px 0;
}

.points-value {
  font-size: 48px;
  font-weight: 700;
  color: var(--gold);
  margin-bottom: 8px;
}

.points-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 16px;
}

.progress-bar {
  height: 24px;
  background: #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 12px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--gold), #d4a956);
  transition: width 0.3s ease;
}

.progress-text {
  text-align: center;
  font-size: 12px;
  color: #888;
}

.filter-buttons {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.filter-btn {
  padding: 6px 12px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s ease;
}

.filter-btn.active {
  background: var(--gold);
  border-color: var(--gold);
  color: white;
}

.empty-state {
  text-align: center;
  padding: 24px;
  color: #999;
}

.transaction-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.transaction-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 6px;
  border-left: 4px solid #ddd;
}

.transaction-item:has(.transaction-type.earned) {
  border-left-color: #4caf50;
}

.transaction-item:has(.transaction-type.spent) {
  border-left-color: #ff9800;
}

.transaction-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.transaction-type {
  font-weight: 600;
  font-size: 14px;
}

.transaction-type.earned {
  color: #4caf50;
}

.transaction-type.spent {
  color: #ff9800;
}

.transaction-date {
  font-size: 12px;
  color: #999;
}

.transaction-points {
  font-weight: 700;
  font-size: 16px;
}

.transaction-points.earned {
  color: #4caf50;
}

.transaction-points.spent {
  color: #ff9800;
}

.summary {
  border-top: 1px solid #ddd;
  padding-top: 16px;
  display: flex;
  justify-content: space-between;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.summary-item span:first-child {
  font-size: 12px;
  color: #999;
}

.summary-item span:last-child {
  font-weight: 700;
  font-size: 16px;
  color: #333;
}

@media (max-width: 768px) {
  .reward-section {
    grid-template-columns: 1fr;
  }
}
</style>
