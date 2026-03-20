<template>
  <div class="invoice-section">
    <div class="invoice-container">
      <!-- Invoice Header -->
      <div class="invoice-header">
        <div class="salon-info">
          <h1>Glow Suite</h1>
          <p class="subtitle">Premium Salon & Spa</p>
          <p class="address">📍 123 Beauty Lane, Bangalore - 560001</p>
          <p class="contact">📞 +91-9876543210 | 📧 hello@glowsuite.com</p>
        </div>
        
        <div class="invoice-meta">
          <div class="meta-item">
            <span class="label">Invoice #</span>
            <span class="value">{{ invoice.number }}</span>
          </div>
          <div class="meta-item">
            <span class="label">Date</span>
            <span class="value">{{ formatDate(invoice.date) }}</span>
          </div>
        </div>
      </div>

      <!-- Customer & Invoice Details -->
      <div class="details-section">
        <div class="customer-details">
          <h3>Bill To</h3>
          <p class="customer-name">{{ invoice.customerName }}</p>
          <p>{{ invoice.customerEmail }}</p>
          <p>{{ invoice.customerPhone }}</p>
        </div>
        
        <div class="invoice-details">
          <div class="detail-row">
            <span>Booking Date:</span>
            <span>{{ formatDate(invoice.bookingDate) }}</span>
          </div>
          <div class="detail-row">
            <span>Staff:</span>
            <span>{{ invoice.staffName }}</span>
          </div>
          <div class="detail-row">
            <span>Status:</span>
            <span class="badge" :class="`badge-${invoice.status.toLowerCase()}`">{{ invoice.status }}</span>
          </div>
        </div>
      </div>

      <!-- Services Table -->
      <div class="services-section">
        <table class="invoice-table">
          <thead>
            <tr>
              <th>Service</th>
              <th>Duration</th>
              <th>Price</th>
              <th>Reward Points</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in invoice.services" :key="service.id">
              <td>{{ service.name }}</td>
              <td>{{ service.duration }} min</td>
              <td class="amount">₹{{ service.price }}</td>
              <td class="amount">{{ service.rewardPoints }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Payment Summary -->
      <div class="payment-summary">
        <div class="summary-row">
          <span>Subtotal</span>
          <span>₹{{ subtotal }}</span>
        </div>
        <div v-if="invoice.discount" class="summary-row discount">
          <span>Discount</span>
          <span>-₹{{ invoice.discount }}</span>
        </div>
        <div v-if="invoice.tax" class="summary-row">
          <span>Tax (18%)</span>
          <span>₹{{ invoice.tax }}</span>
        </div>
        <div class="summary-row total">
          <span>Total Amount</span>
          <span>₹{{ invoice.totalAmount }}</span>
        </div>
      </div>

      <!-- Reward Points Section -->
      <div class="rewards-section">
        <h3>Reward Points Summary</h3>
        
        <div class="rewards-grid">
          <div class="reward-card earned">
            <div class="reward-icon">📈</div>
            <div class="reward-label">Points Earned</div>
            <div class="reward-value">+{{ totalPointsEarned }}</div>
          </div>
          
          <div class="reward-card spent">
            <div class="reward-icon">📉</div>
            <div class="reward-label">Points Used</div>
            <div class="reward-value">-{{ invoice.pointsSpent }}</div>
          </div>
          
          <div class="reward-card balance">
            <div class="reward-icon">💎</div>
            <div class="reward-label">Total Balance</div>
            <div class="reward-value">{{ invoice.customerRewardBalance }}</div>
          </div>
        </div>

        <!-- Reward Transactions Table -->
        <div class="transactions-table">
          <h4>Reward Point Transactions</h4>
          <table>
            <thead>
              <tr>
                <th>Transaction Type</th>
                <th>Points</th>
                <th>Date</th>
                <th>Expiry Date</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="txn in rewardTransactions" :key="txn.id" :class="`txn-${txn.type}`">
                <td>{{ txn.type === 'earned' ? 'Earned' : 'Spent' }}</td>
                <td class="points-value">{{ txn.type === 'earned' ? '+' : '-' }}{{ txn.points }}</td>
                <td>{{ formatDate(txn.date) }}</td>
                <td v-if="txn.type === 'earned'">{{ formatDate(txn.expiryDate) }}</td>
                <td v-else>—</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Notes & Terms -->
      <div class="notes-section">
        <h4>Thank You for Your Visit!</h4>
        <p>We appreciate your business. We look forward to seeing you again soon!</p>
        <p class="terms">📌 All promotional offers are valid for 30 days. Unused reward points expire after 1 year.</p>
      </div>

      <!-- Actions -->
      <div class="invoice-actions">
        <button class="btn btn-primary" @click="printInvoice">🖨️ Print</button>
        <button class="btn btn-secondary" @click="downloadPDF">📥 Download PDF</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const invoice = ref({
  number: 'INV-2025-001234',
  date: new Date(),
  customerName: 'Sofia Mensah',
  customerEmail: 'sofia@email.com',
  customerPhone: '+91-9876543210',
  bookingDate: new Date('2025-03-15'),
  staffName: 'Priya Sharma',
  status: 'Completed',
  discount: 500,
  tax: 441.60,
  totalAmount: 3441.60,
  pointsSpent: 50,
  customerRewardBalance: 325,
  services: [
    { id: 1, name: 'Diamond Facial', duration: 90, price: 4500, rewardPoints: 100 },
    { id: 2, name: 'Head Massage', duration: 30, price: 1500, rewardPoints: 30 }
  ]
})

const rewardTransactions = ref([
  { id: 1, type: 'earned', points: 130, date: new Date('2025-03-15'), expiryDate: new Date('2026-03-15') },
  { id: 2, type: 'spent', points: 50, date: new Date('2025-03-12'), expiryDate: null }
])

const subtotal = computed(() => {
  return invoice.value.services.reduce((sum, s) => sum + s.price, 0)
})

const totalPointsEarned = computed(() => {
  return invoice.value.services.reduce((sum, s) => sum + s.rewardPoints, 0)
})

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}

const printInvoice = () => {
  window.print()
}

const downloadPDF = () => {
  alert('Download PDF - Feature to be implemented')
}
</script>

<style scoped>
.invoice-section {
  padding: 24px;
  background: #f5f5f5;
  min-height: 100vh;
}

.invoice-container {
  max-width: 900px;
  margin: 0 auto;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* Invoice Header */
.invoice-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 40px;
  background: linear-gradient(135deg, var(--charcoal), #222);
  color: white;
}

.salon-info h1 {
  margin: 0 0 4px 0;
  font-size: 32px;
  color: var(--gold);
}

.salon-info p {
  margin: 4px 0;
  font-size: 13px;
}

.subtitle {
  font-size: 14px !important;
  color: #ddd !important;
}

.invoice-meta {
  text-align: right;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 12px;
}

.meta-item .label {
  font-size: 11px;
  color: #aaa;
  text-transform: uppercase;
}

.meta-item .value {
  font-size: 16px;
  font-weight: 600;
  color: var(--gold);
}

/* Details Section */
.details-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  padding: 24px 40px;
  border-bottom: 1px solid #eee;
}

.customer-details h3,
.invoice-details h3 {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #666;
  text-transform: uppercase;
}

.customer-name {
  font-weight: 600;
  font-size: 16px;
  margin: 0 0 4px 0;
}

.customer-details p,
.detail-row {
  margin: 4px 0;
  font-size: 13px;
  color: #666;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin: 8px 0;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
}

.badge-completed {
  background: #d4edda;
  color: #155724;
}

/* Services Section */
.services-section {
  padding: 24px 40px;
  border-bottom: 1px solid #eee;
}

.invoice-table {
  width: 100%;
  border-collapse: collapse;
}

.invoice-table thead {
  background: #f5f5f5;
  border-bottom: 2px solid #ddd;
}

.invoice-table th {
  padding: 12px;
  text-align: left;
  font-weight: 600;
  font-size: 12px;
  color: #666;
  text-transform: uppercase;
}

.invoice-table td {
  padding: 12px;
  border-bottom: 1px solid #eee;
  font-size: 13px;
}

.invoice-table .amount {
  text-align: right;
  font-weight: 600;
}

/* Payment Summary */
.payment-summary {
  padding: 24px 40px;
  border-bottom: 1px solid #eee;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 14px;
}

.summary-row.discount {
  color: #4caf50;
}

.summary-row.total {
  border-top: 2px solid #ddd;
  padding-top: 16px;
  font-weight: 700;
  font-size: 18px;
  color: var(--gold);
}

/* Rewards Section */
.rewards-section {
  padding: 40px;
}

.rewards-section h3 {
  margin: 0 0 24px 0;
  font-size: 18px;
  color: #333;
}

.rewards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}

.reward-card {
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  background: #f9f9f9;
  border: 2px solid #eee;
}

.reward-card.earned {
  border-color: #4caf50;
  background: rgba(76, 175, 80, 0.05);
}

.reward-card.spent {
  border-color: #ff9800;
  background: rgba(255, 152, 0, 0.05);
}

.reward-card.balance {
  border-color: var(--gold);
  background: rgba(212, 169, 84, 0.05);
}

.reward-icon {
  font-size: 28px;
  margin-bottom: 8px;
}

.reward-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 8px;
  text-transform: uppercase;
}

.reward-value {
  font-size: 24px;
  font-weight: 700;
  color: #333;
}

.reward-card.earned .reward-value {
  color: #4caf50;
}

.reward-card.spent .reward-value {
  color: #ff9800;
}

.reward-card.balance .reward-value {
  color: var(--gold);
}

/* Transactions Table */
.transactions-table {
  margin-top: 24px;
}

.transactions-table h4 {
  margin: 0 0 12px 0;
  font-size: 13px;
  color: #666;
  text-transform: uppercase;
}

.transactions-table table {
  width: 100%;
  border-collapse: collapse;
}

.transactions-table th {
  padding: 8px;
  text-align: left;
  font-weight: 600;
  font-size: 11px;
  color: #999;
  text-transform: uppercase;
  border-bottom: 1px solid #eee;
}

.transactions-table td {
  padding: 8px;
  font-size: 12px;
  border-bottom: 1px solid #eee;
}

.transactions-table .points-value {
  font-weight: 600;
}

.txn-earned .points-value {
  color: #4caf50;
}

.txn-spent .points-value {
  color: #ff9800;
}

/* Notes Section */
.notes-section {
  padding: 24px 40px;
  text-align: center;
  border-bottom: 1px solid #eee;
}

.notes-section h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #333;
}

.notes-section p {
  margin: 4px 0;
  font-size: 12px;
  color: #666;
}

.notes-section .terms {
  font-size: 11px;
  color: #999;
  margin-top: 12px;
}

/* Actions */
.invoice-actions {
  padding: 24px 40px;
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary {
  background: var(--gold);
  color: var(--charcoal);
}

.btn-primary:hover {
  background: #d4a956;
}

.btn-secondary {
  background: #e0e0e0;
  color: #333;
}

.btn-secondary:hover {
  background: #d0d0d0;
}

@media print {
  .invoice-actions {
    display: none;
  }

  .invoice-container {
    box-shadow: none;
  }
}

@media (max-width: 768px) {
  .invoice-container {
    border-radius: 0;
  }

  .invoice-header {
    flex-direction: column;
    gap: 20px;
  }

  .details-section {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .invoice-header,
  .details-section,
  .services-section,
  .payment-summary,
  .rewards-section,
  .notes-section,
  .invoice-actions {
    padding: 20px;
  }

  .rewards-grid {
    grid-template-columns: 1fr;
  }
}
</style>
