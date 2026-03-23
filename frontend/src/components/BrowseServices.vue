<template>
  <div class="services-section">
    <h2>Explore Our Services</h2>

    <!-- Exclusive Packages Carousel -->
    <div v-if="exclusivePackages.length > 0" class="exclusive-section">
      <h3>✨ Exclusive Packages</h3>
      <p class="section-subtitle">Limited time offers for our VIP members</p>
      
      <div class="packages-carousel">
        <div v-for="pkg in exclusivePackages" :key="pkg.id" class="package-card exclusive">
          <div class="package-badge">Exclusive</div>
          <h4>{{ pkg.name }}</h4>
          <p class="package-desc">{{ pkg.description }}</p>
          
          <div class="date-range">
            <span class="date-label">Available:</span>
            <span>{{ formatDate(pkg.fromDate) }} - {{ formatDate(pkg.toDate) }}</span>
          </div>
          
          <div class="benefits">
            <div class="benefit-item">
              <span class="benefit-icon">✓</span>
              <span>VIP Member Benefit</span>
            </div>
            <div class="benefit-item">
              <span class="benefit-icon">✓</span>
              <span>Premium Quality</span>
            </div>
          </div>
          
          <button class="btn btn-primary">Book Now</button>
        </div>
      </div>
    </div>

    <!-- Services Table -->
    <div class="services-table-section">
      <h3>All Services</h3>
      
      <div class="table-wrapper">
        <table class="services-table">
          <thead>
            <tr>
              <th>Service Name</th>
              <th>Category</th>
              <th>Price</th>
              <th>Duration</th>
              <th>Reward Pts</th>
              <th>Allergy-Free</th>
              <th>Advance Days</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in services" :key="service.id" class="service-row">
              <td class="service-name">{{ service.name }}</td>
              <td>{{ service.category }}</td>
              <td class="price">₹{{ service.price }}</td>
              <td>{{ service.duration }} min</td>
              <td class="reward-pts">{{ service.rewardPoints }}</td>
              <td>
                <span v-if="service.isAllergyFree" class="badge badge-success">✓</span>
                <span v-else class="badge badge-gray">—</span>
              </td>
              <td>
                <span v-if="service.advanceDays">{{ service.advanceDays }} days</span>
                <span v-else class="text-muted">No restriction</span>
              </td>
              <td>
                <button class="btn btn-sm btn-primary" @click="bookService(service.id)">Book</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Booking Guidelines -->
    <div class="guidelines-section">
      <h3>📋 Booking Guidelines</h3>
      
      <div class="guidelines-grid">
        <div class="guideline-card">
          <div class="guideline-icon">📅</div>
          <h4>Bridal Services</h4>
          <p>For exclusive bridal packages, book at least 2 months in advance for best availability.</p>
        </div>
        
        <div class="guideline-card">
          <div class="guideline-icon">⏰</div>
          <h4>Regular Services</h4>
          <p>Regular services can be booked up to 5 days in advance for optimal scheduling.</p>
        </div>
        
        <div class="guideline-card">
          <div class="guideline-icon">👑</div>
          <h4>VIP Priority</h4>
          <p>VIP members enjoy priority booking and shorter advance booking requirements.</p>
        </div>
        
        <div class="guideline-card">
          <div class="guideline-icon">🔄</div>
          <h4>Flexible Changes</h4>
          <p>Cancel or reschedule your booking up to 24 hours before your appointment.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const exclusivePackages = ref([
  {
    id: 1,
    name: 'Rajam Premium',
    description: 'Complete bridal package with facial, massage, and styling',
    fromDate: '2025-03-01',
    toDate: '2025-05-31',
    benefits: ['Complimentary consultation', 'Day-of touch-ups', 'Premium products']
  },
  {
    id: 2,
    name: 'Wellness Retreat',
    description: 'Relaxation package with spa massage and facial',
    fromDate: '2025-03-15',
    toDate: '2025-06-30',
    benefits: ['Aromatic massage', 'Hydrating facial', 'Herbal tea']
  }
])

const services = ref([
  { id: 1, name: 'Classic Facial', category: 'Facial', price: 2500, duration: 60, rewardPoints: 50, isAllergyFree: true, advanceDays: 0 },
  { id: 2, name: 'Diamond Facial', category: 'Facial', price: 4500, duration: 90, rewardPoints: 100, isAllergyFree: true, advanceDays: 2 },
  { id: 3, name: 'Full Body Massage', category: 'Wellness', price: 3500, duration: 60, rewardPoints: 75, isAllergyFree: true, advanceDays: 0 },
  { id: 4, name: 'Bridal Makeup', category: 'Makeup', price: 5000, duration: 120, rewardPoints: 150, isAllergyFree: false, advanceDays: 60 },
  { id: 5, name: 'Hair Color', category: 'Hair', price: 3000, duration: 90, rewardPoints: 80, isAllergyFree: false, advanceDays: 7 },
  { id: 6, name: 'Pedicure', category: 'Nails', price: 1500, duration: 45, rewardPoints: 30, isAllergyFree: true, advanceDays: 0 },
  { id: 7, name: 'Threading', category: 'Hair Removal', price: 500, duration: 30, rewardPoints: 10, isAllergyFree: false, advanceDays: 0 },
  { id: 8, name: 'Waxing', category: 'Hair Removal', price: 1000, duration: 30, rewardPoints: 20, isAllergyFree: false, advanceDays: 1 }
])

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}

const bookService = (serviceId) => {
  alert(`Booking service ${serviceId}`)
}
</script>

<style scoped>
.services-section {
  padding: 24px;
}

h2 {
  color: #333;
  margin-bottom: 32px;
}

h3 {
  color: #333;
  margin-bottom: 12px;
  font-size: 18px;
}

.section-subtitle {
  color: #999;
  margin-bottom: 20px;
  font-size: 13px;
}

/* Exclusive Packages Section */
.exclusive-section {
  margin-bottom: 48px;
}

.packages-carousel {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.package-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: all 0.3s ease;
}

.package-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.package-card.exclusive {
  border: 2px solid var(--gold);
  background: linear-gradient(135deg, rgba(212, 169, 84, 0.05), rgba(255, 255, 255, 0.95));
}

.package-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  background: var(--gold);
  color: var(--charcoal);
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
}

.package-card h4 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 16px;
}

.package-desc {
  color: #666;
  font-size: 13px;
  margin-bottom: 12px;
}

.date-range {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  padding: 8px;
  background: #f5f5f5;
  border-radius: 4px;
  font-size: 12px;
}

.date-label {
  font-weight: 600;
  color: #333;
}

.benefits {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #666;
}

.benefit-icon {
  color: var(--gold);
  font-weight: 700;
}

/* Services Table Section */
.services-table-section {
  margin-bottom: 48px;
}

.table-wrapper {
  overflow-x: auto;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.services-table {
  width: 100%;
  border-collapse: collapse;
}

.services-table thead {
  background: #f5f5f5;
  border-bottom: 2px solid #ddd;
}

.services-table th {
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  font-size: 12px;
  color: #666;
  text-transform: uppercase;
}

.services-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #eee;
  font-size: 13px;
}

.service-row:hover {
  background: #f9f9f9;
}

.service-name {
  font-weight: 600;
  color: #333;
}

.price {
  color: var(--gold);
  font-weight: 600;
}

.reward-pts {
  color: #4caf50;
  font-weight: 600;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
}

.badge-success {
  background: #d4edda;
  color: #155724;
}

.badge-gray {
  background: #e8e8e8;
  color: #666;
}

.text-muted {
  color: #999;
  font-size: 12px;
}

.btn {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-sm {
  padding: 6px 10px;
}

.btn-primary {
  background: var(--gold);
  color: var(--charcoal);
}

.btn-primary:hover {
  background: #d4a956;
}

/* Guidelines Section */
.guidelines-section {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.guidelines-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}

.guideline-card {
  padding: 16px;
  border: 1px solid #eee;
  border-radius: 6px;
  text-align: center;
  background: #f9f9f9;
}

.guideline-icon {
  font-size: 28px;
  margin-bottom: 8px;
}

.guideline-card h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #333;
}

.guideline-card p {
  margin: 0;
  font-size: 12px;
  color: #666;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .services-table {
    font-size: 12px;
  }

  .services-table th,
  .services-table td {
    padding: 8px 12px;
  }

  .guidelines-grid {
    grid-template-columns: 1fr;
  }
}
</style>
