<template>
  <div class="dashboard-container">
    <!-- Sidebar Navigation -->
    <div class="dashboard-sidebar">
      <div class="sidebar-header">
        <h2 style="color: var(--gold); font-size: 24px; margin: 0">👑 Owner Hub</h2>
        <p style="color: #999; margin: 8px 0 0 0; font-size: 12px">{{ ownerData.ownerName }}</p>
      </div>

      <div class="sidebar-menu">
        <div
          :class="['nav-item', { active: currentView === 'overview' }]"
          @click="currentView = 'overview'"
        >
          <span class="nav-icon">📊</span> Overview
        </div>

        <div
          :class="['nav-item', { active: currentView === 'managers' }]"
          @click="currentView = 'managers'"
        >
          <span class="nav-icon">👤</span> Managers ({{ ownerData.managers.length }})
        </div>

        <div
          :class="['nav-item', { active: currentView === 'reports' }]"
          @click="currentView = 'reports'"
        >
          <span class="nav-icon">📄</span> Download Reports
        </div>
      </div>

      <div class="sidebar-footer">
        <button class="btn btn-secondary w-full" @click="handleLogout" style="margin-top: auto">
          🚪 Logout
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="dashboard-main">
      <div class="content-wrap">
        <!-- OVERVIEW VIEW -->
        <div v-if="currentView === 'overview'" class="fade-in">
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon">👤</div>
              <div class="stat-label">Total Managers</div>
              <div class="stat-value">{{ ownerData.managers.length }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">📊</div>
              <div class="stat-label">Total Revenue</div>
              <div class="stat-value">₹{{ totalRevenue }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">📅</div>
              <div class="stat-label">Total Bookings</div>
              <div class="stat-value">{{ totalBookings }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">👥</div>
              <div class="stat-label">Total Customers</div>
              <div class="stat-value">{{ totalCustomers }}</div>
            </div>
          </div>
        </div>

        <!-- MANAGERS VIEW -->
        <div v-if="currentView === 'managers'" class="fade-in">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">➕ Add New Manager</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleCreateManager">
                <div class="form-grid">
                  <div class="form-group">
                    <label for="manager-name">Full Name *</label>
                    <input 
                      id="manager-name"
                      v-model="managerForm.name"
                      type="text"
                      placeholder="Enter full name"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="manager-email">Email *</label>
                    <input 
                      id="manager-email"
                      v-model="managerForm.email"
                      type="email"
                      placeholder="example@salon.com"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="manager-phone">Phone *</label>
                    <input 
                      id="manager-phone"
                      v-model="managerForm.phone"
                      type="tel"
                      placeholder="Enter phone number"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="manager-location">Salon Location *</label>
                    <input 
                      id="manager-location"
                      v-model="managerForm.location"
                      type="text"
                      placeholder="Enter salon location/branch name"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="manager-username">Username *</label>
                    <input 
                      id="manager-username"
                      v-model="managerForm.username"
                      type="text"
                      placeholder="Unique username"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="manager-doj">Date of Joining *</label>
                    <input 
                      id="manager-doj"
                      v-model="managerForm.doj"
                      type="date"
                      class="form-input"
                      required
                    />
                  </div>
                </div>

                <div v-if="managerError" class="error-message">{{ managerError }}</div>
                <div v-if="managerSuccess" class="success-message">{{ managerSuccess }}</div>

                <button type="submit" class="btn btn-primary" style="margin-top: 16px">
                  Create Manager
                </button>
              </form>
            </div>
          </div>

          <!-- Managers List -->
          <div class="card" style="margin-top: 24px">
            <div class="card-header">
              <h3 class="card-title">👥 Existing Managers</h3>
            </div>
            <div class="card-body">
              <div class="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Phone</th>
                      <th>Location</th>
                      <th>Username</th>
                      <th>Date of Joining</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="manager in ownerData.managers" :key="manager.id">
                      <td>{{ manager.name }}</td>
                      <td>{{ manager.email }}</td>
                      <td>{{ manager.phone }}</td>
                      <td>{{ manager.location }}</td>
                      <td><span class="badge badge-info">{{ manager.username }}</span></td>
                      <td>{{ manager.doj }}</td>
                      <td>
                        <span :class="['badge', getStatusBadgeClass(manager.status)]">
                          {{ manager.status }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- REPORTS VIEW -->
        <div v-if="currentView === 'reports'" class="fade-in">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Download Reports</h3>
            </div>
            <div class="card-body">
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px">
                <div class="report-item">
                  <div class="report-icon">📊</div>
                  <div class="report-title">Sales Report</div>
                  <div class="text-muted" style="margin: 8px 0">Total sales and revenue summary</div>
                  <button class="btn btn-primary w-full">📥 Download CSV</button>
                </div>

                <div class="report-item">
                  <div class="report-icon">📅</div>
                  <div class="report-title">Bookings Report</div>
                  <div class="text-muted" style="margin: 8px 0">All appointments and bookings</div>
                  <button class="btn btn-primary w-full">📥 Download CSV</button>
                </div>

                <div class="report-item">
                  <div class="report-icon">👥</div>
                  <div class="report-title">Staff Report</div>
                  <div class="text-muted" style="margin: 8px 0">Staff performance and attendance</div>
                  <button class="btn btn-primary w-full">📥 Download CSV</button>
                </div>

                <div class="report-item">
                  <div class="report-icon">📦</div>
                  <div class="report-title">Inventory Report</div>
                  <div class="text-muted" style="margin: 8px 0">Stock levels and movements</div>
                  <button class="btn btn-primary w-full">📥 Download CSV</button>
                </div>

                <div class="report-item">
                  <div class="report-icon">💰</div>
                  <div class="report-title">Financial Report</div>
                  <div class="text-muted" style="margin: 8px 0">Revenue and expenses summary</div>
                  <button class="btn btn-primary w-full">📥 Download CSV</button>
                </div>

                <div class="report-item">
                  <div class="report-icon">⭐</div>
                  <div class="report-title">Feedback Report</div>
                  <div class="text-muted" style="margin: 8px 0">Customer reviews and ratings</div>
                  <button class="btn btn-primary w-full">📥 Download CSV</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAppStore } from '@/stores/appStore';

export default {
  name: 'OwnerDashboard',
  setup() {
    const router = useRouter();
    const appStore = useAppStore();
    const currentView = ref('overview');

    const managerForm = ref({
      name: "",
      email: "",
      phone: "",
      location: "",
      username: "",
      doj: ""
    });
    const managerError = ref("");
    const managerSuccess = ref("");

    const ownerData = ref({
      ownerName: "Glow Suite Owner",
      managers: [
        {
          id: 1,
          name: "Rajesh Kumar",
          email: "rajesh@glowsuite.com",
          phone: "+91-9876543210",
          location: "Downtown Branch",
          username: "rajesh_manager",
          doj: "2025-01-15",
          status: "active"
        },
        {
          id: 2,
          name: "Priya Sharma",
          email: "priya@glowsuite.com",
          phone: "+91-9876543211",
          location: "Mall Branch",
          username: "priya_manager",
          doj: "2025-02-10",
          status: "active"
        }
      ],
      bookings: [
        { id: 1, customerId: 1, amount: 500, date: "2026-03-05" },
        { id: 2, customerId: 2, amount: 750, date: "2026-03-06" },
        { id: 3, customerId: 3, amount: 600, date: "2026-03-07" },
        { id: 4, customerId: 1, amount: 450, date: "2026-03-08" },
        { id: 5, customerId: 4, amount: 800, date: "2026-03-09" }
      ],
      customers: [
        { id: 1, name: "Alice Johnson" },
        { id: 2, name: "Bob Williams" },
        { id: 3, name: "Carol Smith" },
        { id: 4, name: "Diana Prince" }
      ]
    });

    const totalRevenue = computed(() => {
      return ownerData.value.bookings.reduce((sum, booking) => sum + booking.amount, 0);
    });

    const totalBookings = computed(() => {
      return ownerData.value.bookings.length;
    });

    const totalCustomers = computed(() => {
      return ownerData.value.customers.length;
    });

    const getStatusBadgeClass = (status) => {
      const baseClasses = ['badge'];
      if (status === 'active') {
        baseClasses.push('badge-success');
      } else if (status === 'inactive') {
        baseClasses.push('badge-danger');
      } else {
        baseClasses.push('badge-warning');
      }
      return baseClasses;
    };

    const handleCreateManager = () => {
      managerError.value = "";
      managerSuccess.value = "";

      // Validation
      if (!managerForm.value.name) {
        managerError.value = "Name is required";
        return;
      }

      if (!managerForm.value.email) {
        managerError.value = "Email is required";
        return;
      }

      if (!managerForm.value.phone) {
        managerError.value = "Phone is required";
        return;
      }

      if (!managerForm.value.location) {
        managerError.value = "Salon location is required";
        return;
      }

      if (!managerForm.value.username) {
        managerError.value = "Username is required";
        return;
      }

      if (!managerForm.value.doj) {
        managerError.value = "Date of joining is required";
        return;
      }

      // Check if username already exists
      if (ownerData.value.managers.some(m => m.username === managerForm.value.username)) {
        managerError.value = "Username already exists";
        return;
      }

      // Create new manager
      const newManager = {
        id: Math.max(...ownerData.value.managers.map(m => m.id || 0), 0) + 1,
        name: managerForm.value.name,
        email: managerForm.value.email,
        phone: managerForm.value.phone,
        location: managerForm.value.location,
        username: managerForm.value.username,
        doj: managerForm.value.doj,
        status: "active"
      };

      ownerData.value.managers.push(newManager);
      managerSuccess.value = "Manager created successfully!";

      // Reset form
      setTimeout(() => {
        managerForm.value = {
          name: "",
          email: "",
          phone: "",
          location: "",
          username: "",
          doj: ""
        };
        managerSuccess.value = "";
      }, 1500);
    };

    const handleLogout = () => {
      appStore.logout();
      router.push('/');
    };

    return {
      currentView,
      managerForm,
      managerError,
      managerSuccess,
      ownerData,
      totalRevenue,
      totalBookings,
      totalCustomers,
      getStatusBadgeClass,
      handleCreateManager,
      handleLogout
    };
  }
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

:root {
  --gold: #d4af37;
  --bg: #1a1a1a;
  --card-bg: #2a2a2a;
  --text: #e0e0e0;
  --border: #444;
  --light-bg: #3a3a3a;
  --success: #4caf50;
  --danger: #f44336;
  --warning: #ff9800;
  --info: #2196f3;
  --radius: 8px;
}

.dashboard-container {
  display: flex;
  height: 100vh;
  background-color: var(--bg);
  color: var(--text);
}

.dashboard-sidebar {
  width: 280px;
  background-color: var(--card-bg);
  border-right: 1px solid var(--border);
  padding: 20px;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.3);
}

.sidebar-header {
  margin-bottom: 30px;
}

.sidebar-menu {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-item {
  padding: 12px 16px;
  border-radius: var(--radius);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--text);
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
  background-color: transparent;
}

.nav-item:hover {
  background-color: var(--light-bg);
  border-left-color: var(--gold);
}

.nav-item.active {
  background-color: var(--light-bg);
  border-left-color: var(--gold);
  color: var(--gold);
}

.nav-icon {
  font-size: 18px;
}

.sidebar-footer {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.dashboard-main {
  flex: 1;
  overflow-y: auto;
  padding: 30px;
}

.content-wrap {
  max-width: 1200px;
  margin: 0 auto;
}

.fade-in {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background-color: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.stat-card:hover {
  border-color: var(--gold);
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.2);
}

.stat-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.stat-label {
  color: #999;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: var(--gold);
}

.card {
  background-color: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.card-header {
  padding: 20px;
  border-bottom: 1px solid var(--border);
  background-color: rgba(212, 175, 55, 0.05);
}

.card-title {
  margin: 0;
  color: var(--gold);
  font-size: 18px;
}

.card-body {
  padding: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 8px;
  color: var(--text);
  font-weight: 500;
}

.form-input {
  padding: 10px 12px;
  background-color: var(--light-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text);
  font-size: 14px;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--gold);
  box-shadow: 0 0 8px rgba(212, 175, 55, 0.3);
}

.error-message {
  background-color: rgba(244, 67, 54, 0.1);
  border-left: 4px solid var(--danger);
  padding: 12px 16px;
  border-radius: var(--radius);
  color: #ff8a8a;
  margin: 12px 0;
}

.success-message {
  background-color: rgba(76, 175, 80, 0.1);
  border-left: 4px solid var(--success);
  padding: 12px 16px;
  border-radius: var(--radius);
  color: #81c784;
  margin: 12px 0;
}

.btn {
  padding: 10px 16px;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  display: inline-block;
  text-align: center;
}

.btn-primary {
  background-color: var(--gold);
  color: #1a1a1a;
}

.btn-primary:hover {
  background-color: #e0c250;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
}

.btn-secondary {
  background-color: var(--light-bg);
  color: var(--text);
  border: 1px solid var(--border);
}

.btn-secondary:hover {
  background-color: var(--border);
}

.w-full {
  width: 100%;
}

.table-wrap {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

table thead {
  background-color: rgba(212, 175, 55, 0.05);
}

table th {
  padding: 12px;
  text-align: left;
  color: var(--gold);
  font-weight: 600;
  border-bottom: 2px solid var(--border);
}

table td {
  padding: 12px;
  border-bottom: 1px solid var(--border);
}

table tbody tr:hover {
  background-color: var(--light-bg);
}

.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.badge-success {
  background-color: rgba(76, 175, 80, 0.2);
  color: #81c784;
}

.badge-danger {
  background-color: rgba(244, 67, 54, 0.2);
  color: #ff8a8a;
}

.badge-warning {
  background-color: rgba(255, 152, 0, 0.2);
  color: #ffb74d;
}

.badge-info {
  background-color: rgba(33, 150, 243, 0.2);
  color: #64b5f6;
}

.report-item {
  background-color: var(--light-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  text-align: center;
  transition: all 0.3s ease;
}

.report-item:hover {
  border-color: var(--gold);
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.2);
}

.report-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.report-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 8px;
}

.text-muted {
  color: #999;
  font-size: 13px;
}

@media (max-width: 768px) {
  .dashboard-container {
    flex-direction: column;
  }

  .dashboard-sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid var(--border);
  }

  .dashboard-main {
    padding: 20px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
