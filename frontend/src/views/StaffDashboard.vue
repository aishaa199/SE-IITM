<template>
  <div class="content-layout">
    <!-- Sidebar -->
    <div class="sidebar">
      <div class="sidebar-logo">
        <div class="sidebar-logo-text">Glow Suite</div>
        <div class="sidebar-logo-sub">Staff Portal</div>
      </div>
      <nav class="sidebar-nav">
        <div class="nav-section">My Schedule</div>
        <div
          :class="['nav-item', { active: currentView === 'dashboard' }]"
          @click="currentView = 'dashboard'"
        >
          <span class="nav-icon">📊</span> Dashboard
        </div>
        <div
          :class="['nav-item', { active: currentView === 'appointments' }]"
          @click="currentView = 'appointments'"
        >
          <span class="nav-icon">📅</span> My Appointments
        </div>

        <div class="nav-section">Operations</div>
        <div
          :class="['nav-item', { active: currentView === 'order-products' }]"
          @click="currentView = 'order-products'"
        >
          <span class="nav-icon">📦</span> Order Products
        </div>

        <div class="nav-section">Account</div>
        <div
          :class="['nav-item', { active: currentView === 'profile' }]"
          @click="currentView = 'profile'"
        >
          <span class="nav-icon">👤</span> My Profile
        </div>
      </nav>
      <div class="sidebar-footer">
        <div class="sidebar-user">
          <div class="sidebar-avatar">{{ staffData.name[0] }}</div>
          <div>
            <div class="sidebar-username">{{ staffData.name }}</div>
            <div class="sidebar-role">{{ staffData.role }}</div>
          </div>
        </div>
        <button class="btn btn-ghost w-full" style="margin-top: 12px; font-size: 12px" @click="showChangePasswordModal = true">
          🔑 Change Password
        </button>
        <button class="btn btn-ghost w-full" style="margin-top: 8px; font-size: 12px" @click="logout">
          Logout
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Topbar -->
      <div class="topbar">
        <div class="topbar-title">{{ pageTitle }}</div>
        <div class="topbar-right">
          <button class="notif-btn">🔔</button>
        </div>
      </div>

      <!-- Page Content -->
      <div class="page-content">
        <!-- DASHBOARD VIEW -->
        <div v-if="currentView === 'dashboard'" class="fade-in">
          <!-- Quick Stats -->
          <div class="stat-grid">
            <div class="stat-card">
              <div class="stat-icon">📅</div>
              <div class="stat-value">{{ staffData.todayStats.appointmentsCount }}</div>
              <div class="stat-label">Today's Appointments</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">✅</div>
              <div class="stat-value">{{ staffData.todayStats.completedCount }}</div>
              <div class="stat-label">Completed</div>
            </div>
          </div>

          <!-- Today's Appointments & Upcoming -->
          <div class="grid-2" style="margin-top: 24px">
            <!-- Today's Schedule -->
            <div class="card">
              <div class="card-header">
                <h3 class="card-title">📅 Today's Schedule</h3>
              </div>
              <div class="card-body">
                <div v-if="staffData.todayAppointments.length === 0" class="empty-state">
                  <div class="empty-state-icon">📅</div>
                  <div class="empty-state-text">No appointments today</div>
                </div>
                <div v-for="appt in staffData.todayAppointments" :key="appt.id" class="booking-item">
                  <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px">
                    <div class="booking-time">{{ appt.time }}</div>
                    <div>
                      <div style="font-weight: 600">{{ appt.customerName }}</div>
                      <div class="text-muted">{{ appt.service }}</div>
                    </div>
                  </div>
                  <div style="display: flex; align-items: center; justify-content: space-between">
                    <div class="text-muted" style="font-size: 12px">
                      {{ appt.duration }} min • ₹{{ appt.amount }}
                    </div>
                    <span :class="['badge', getStatusBadgeClass(appt.status)]">{{ appt.status }}</span>
                  </div>
                  <div style="height: 1px; background: var(--border); margin: 8px 0"></div>
                </div>
              </div>
            </div>

            <!-- Monthly Attendance -->
            <div class="card">
              <div class="card-header" style="display: flex; justify-content: space-between; align-items: center">
                <h3 class="card-title">📅 Attendance - {{ currentMonth }}</h3>
                <button class="btn btn-primary" style="padding: 6px 12px; font-size: 12px" @click="showMarkAttendanceModal = true">Mark Attendance</button>
              </div>
              <div class="card-body">
                <div class="attendance-stats" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 16px">
                  <div style="text-align: center; padding: 12px; background: var(--light-bg); border-radius: var(--radius)">
                    <div style="font-size: 24px; font-weight: 600; color: var(--success)">{{ attendanceStats.present }}</div>
                    <div class="text-muted" style="font-size: 12px">Present</div>
                  </div>
                  <div style="text-align: center; padding: 12px; background: var(--light-bg); border-radius: var(--radius)">
                    <div style="font-size: 24px; font-weight: 600; color: var(--warning)">{{ attendanceStats.absent }}</div>
                    <div class="text-muted" style="font-size: 12px">Absent</div>
                  </div>
                  <div style="text-align: center; padding: 12px; background: var(--light-bg); border-radius: var(--radius)">
                    <div style="font-size: 24px; font-weight: 600; color: var(--info)">{{ attendanceStats.late }}</div>
                    <div class="text-muted" style="font-size: 12px">Late</div>
                  </div>
                </div>
                <div class="attendance-list">
                  <div v-for="record in staffData.monthlyAttendance" :key="record.date" class="attendance-item" style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid var(--border)">
                    <div>
                      <div style="font-weight: 600; font-size: 13px">{{ formatDate(record.date) }}</div>
                      <div class="text-muted" style="font-size: 11px">{{ getDayName(record.date) }}</div>
                    </div>
                    <span :class="['badge', getAttendanceBadgeClass(record.status)]">{{ record.status }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- APPOINTMENTS VIEW -->
        <div v-if="currentView === 'appointments'" class="fade-in">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">All My Appointments</h3>
            </div>
            <div class="card-body">
              <div style="margin-bottom: 16px">
                <input 
                  v-model="appointmentCustomerFilter"
                  type="text" 
                  placeholder="🔍 Filter by customer name..." 
                  class="form-input"
                  style="width: 100%; max-width: 300px"
                />
              </div>
              <div class="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Customer</th>
                      <th>Service</th>
                      <th>Date & Time</th>
                      <th>Duration</th>
                      <th>Amount</th>
                      <th>Status</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="appt in filteredAppointments" :key="appt.id">
                      <td>{{ appt.customerName }}</td>
                      <td>{{ appt.service }}</td>
                      <td>{{ appt.date ? appt.date : 'Today' }} {{ appt.time }}</td>
                      <td>{{ appt.duration }} min</td>
                      <td>₹{{ appt.amount }}</td>
                      <td>
                        <span :class="['badge', getStatusBadgeClass(appt.status)]">{{ appt.status }}</span>
                      </td>
                      <td>
                        <button v-if="appt.status !== 'completed'" class="btn btn-sm btn-primary" @click="handleMarkAppointmentComplete(appt)" style="padding: 4px 8px; font-size: 12px">
                          ✓ Complete
                        </button>
                        <span v-else class="text-muted" style="font-size: 12px">Completed</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- ORDER PRODUCTS VIEW -->
        <div v-if="currentView === 'order-products'" class="fade-in">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">📦 Order Products</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleOrderProduct" style="max-width: 600px">
                <div class="form-group">
                  <label for="product-category">Product Category *</label>
                  <select 
                    id="product-category"
                    v-model="orderForm.selectedCategory" 
                    class="form-input"
                    required
                  >
                    <option value="">Select a category</option>
                    <option value="Hair Care">Hair Care</option>
                    <option value="Skin Care">Skin Care</option>
                    <option value="Nails">Nails</option>
                    <option value="Wellness">Wellness</option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="product-name">Product Name *</label>
                  <select 
                    id="product-name"
                    v-model="orderForm.productId" 
                    class="form-input"
                    required
                    :disabled="!orderForm.selectedCategory"
                  >
                    <option value="">{{ orderForm.selectedCategory ? 'Select a product' : 'Please select a category first' }}</option>
                    <option v-for="product in filteredProductsByCategory" :key="product.id" :value="product.id">
                      {{ product.name }} (Stock: {{ product.currentStock }})
                    </option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="service">Service It's Required For *</label>
                  <select 
                    id="service"
                    v-model="orderForm.serviceId" 
                    class="form-input"
                    required
                  >
                    <option value="">Select a service</option>
                    <option v-for="service in staffData.services" :key="service.id" :value="service.id">
                      {{ service.name }} - ₹{{ service.price }}
                    </option>
                  </select>
                </div>

                <div v-if="orderError" class="error-message">{{ orderError }}</div>
                <div v-if="orderSuccess" class="success-message">{{ orderSuccess }}</div>

                <button type="submit" class="btn btn-primary" style="margin-top: 20px">
                  Place Order
                </button>
              </form>
            </div>
          </div>

          <!-- Orders History -->
          <div class="card" style="margin-top: 24px">
            <div class="card-header">
              <h3 class="card-title">My Orders</h3>
            </div>
            <div class="card-body">
              <div v-if="staffData.orders.length === 0" class="empty-state">
                <div class="empty-state-icon">📦</div>
                <div class="empty-state-text">No orders placed yet</div>
              </div>
              <div class="table-wrap" v-else>
                <div style="margin-bottom: 16px">
                  <input 
                    v-model="orderProductFilter"
                    type="text" 
                    placeholder="🔍 Filter by product name..." 
                    class="form-input"
                    style="width: 100%; max-width: 300px"
                  />
                </div>
                <table>
                  <thead>
                    <tr>
                      <th>Product</th>
                      <th>Service</th>
                      <th>Status</th>
                      <th>Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="order in filteredOrders" :key="order.id">
                      <td>{{ getProductName(order.productId) }}</td>
                      <td>{{ getServiceName(order.serviceId) }}</td>
                      <td>
                        <span :class="['badge', getOrderStatusBadgeClass(order.status)]">{{ order.status }}</span>
                      </td>
                      <td>{{ order.date }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

<!-- PROFILE VIEW -->
        <div v-if="currentView === 'profile'" class="fade-in">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">My Profile</h3>
            </div>
            <div class="card-body">
              <div style="max-width: 600px">
                <div class="form-group">
                  <label>Name</label>
                  <input type="text" :value="staffData.name" class="form-input" disabled />
                </div>
                <div class="form-group">
                  <label>Email</label>
                  <input type="email" :value="staffData.email" class="form-input" disabled />
                </div>
                <div class="form-group">
                  <label>Phone</label>
                  <input type="tel" :value="staffData.phone" class="form-input" disabled />
                </div>
                <div class="form-group">
                  <label>Role</label>
                  <input type="text" :value="staffData.role" class="form-input" disabled />
                </div>
                <button class="btn btn-primary" style="margin-top: 20px">
                  Edit Profile
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Mark Attendance Modal -->
  <div v-if="showMarkAttendanceModal" class="modal-overlay" @click="showMarkAttendanceModal = false">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3 class="modal-title">📅 Mark Attendance</h3>
        <button class="modal-close" @click="showMarkAttendanceModal = false">✕</button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="handleMarkAttendance">
          <div class="form-group">
            <label for="attendance-date">Date *</label>
            <input 
              id="attendance-date"
              v-model="attendanceForm.date" 
              type="date" 
              class="form-input"
              required
            />
          </div>
          <div class="form-group">
            <label for="attendance-status">Status *</label>
            <select 
              id="attendance-status"
              v-model="attendanceForm.status" 
              class="form-input"
              required
            >
              <option value="">Select Status</option>
              <option value="present">Present</option>
              <option value="absent">Absent</option>
              <option value="late">Late</option>
            </select>
          </div>
          <div v-if="attendanceError" class="error-message">{{ attendanceError }}</div>
          <div v-if="attendanceSuccess" class="success-message">{{ attendanceSuccess }}</div>
          <div style="display: flex; gap: 12px; margin-top: 20px">
            <button type="button" class="btn btn-outline" @click="showMarkAttendanceModal = false" style="flex: 1">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" style="flex: 1">
              Mark Attendance
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
  <div v-if="showChangePasswordModal" class="modal-overlay" @click="showChangePasswordModal = false">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3 class="modal-title">🔑 Change Password</h3>
        <button class="modal-close" @click="showChangePasswordModal = false">✕</button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="handleChangePassword">
          <div class="form-group">
            <label for="current-password">Current Password</label>
            <input 
              id="current-password"
              v-model="passwordForm.currentPassword" 
              type="password" 
              placeholder="Enter current password"
              class="form-input"
              required
            />
          </div>
          <div class="form-group">
            <label for="new-password">New Password</label>
            <input 
              id="new-password"
              v-model="passwordForm.newPassword" 
              type="password" 
              placeholder="Enter new password"
              class="form-input"
              required
            />
            <div class="form-hint">At least 8 characters</div>
          </div>
          <div class="form-group">
            <label for="confirm-password">Confirm Password</label>
            <input 
              id="confirm-password"
              v-model="passwordForm.confirmPassword" 
              type="password" 
              placeholder="Confirm new password"
              class="form-input"
              required
            />
          </div>
          <div v-if="passwordError" class="error-message">{{ passwordError }}</div>
          <div v-if="passwordSuccess" class="success-message">{{ passwordSuccess }}</div>
          <div style="display: flex; gap: 12px; margin-top: 20px">
            <button type="button" class="btn btn-outline" @click="showChangePasswordModal = false" style="flex: 1">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" style="flex: 1">
              Update Password
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const currentView = ref("dashboard");
const showChangePasswordModal = ref(false);
const showMarkAttendanceModal = ref(false);
const passwordForm = ref({
  currentPassword: "",
  newPassword: "",
  confirmPassword: ""
});
const attendanceForm = ref({
  date: "",
  status: ""
});
const orderForm = ref({
  productId: "",
  quantity: 1,
  serviceId: "",
  selectedCategory: ""
});
const passwordError = ref("");
const passwordSuccess = ref("");
const attendanceError = ref("");
const attendanceSuccess = ref("");
const orderError = ref("");
const orderSuccess = ref("");

// Filter states
const appointmentCustomerFilter = ref("");
const orderProductFilter = ref("");

// Get current month
const currentMonth = computed(() => {
  const date = new Date();
  const options = { year: 'numeric', month: 'long' };
  return date.toLocaleDateString('en-US', options);
});

// Format date helper
const formatDate = (dateString) => {
  const date = new Date(dateString);
  const options = { month: 'short', day: 'numeric' };
  return date.toLocaleDateString('en-US', options);
};

// Get day name
const getDayName = (dateString) => {
  const date = new Date(dateString);
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  return days[date.getDay()];
};

// Calculate attendance stats
const attendanceStats = computed(() => {
  const stats = { present: 0, absent: 0, late: 0 };
  staffData.monthlyAttendance.forEach(record => {
    if (record.status === 'present') stats.present++;
    else if (record.status === 'absent') stats.absent++;
    else if (record.status === 'late') stats.late++;
  });
  return stats;
});

// Filtered appointments & orders
const filteredAppointments = computed(() => {
  const threeMonthsAgo = new Date();
  threeMonthsAgo.setMonth(threeMonthsAgo.getMonth() - 3);
  const threeMonthsAgoStr = threeMonthsAgo.toISOString().split('T')[0];
  
  // Combine today and upcoming appointments
  const allAppointments = [...(staffData.todayAppointments || []), ...(staffData.upcomingAppointments || [])];
  const filteredByDate = allAppointments.filter(appt => {
    const apptDate = appt.date ? appt.date : new Date().toISOString().split('T')[0];
    return apptDate >= threeMonthsAgoStr;
  });
  
  if (!appointmentCustomerFilter.value.trim()) return filteredByDate;
  return filteredByDate.filter(appt =>
    appt.customerName.toLowerCase().includes(appointmentCustomerFilter.value.toLowerCase())
  );
});

const filteredOrders = computed(() => {
  if (!orderProductFilter.value.trim()) return staffData.orders;
  return staffData.orders.filter(order => {
    const productName = getProductName(order.productId).toLowerCase();
    return productName.includes(orderProductFilter.value.toLowerCase());
  });
});

const filteredProductsByCategory = computed(() => {
  if (!orderForm.value.selectedCategory) return [];
  return staffData.products.filter(product => {
    const category = getCategoryForProduct(product.id);
    return category === orderForm.value.selectedCategory;
  });
});

// Mock data
const staffData = {
  name: "Sarah Johnson",
  role: "Beauty Therapist",
  email: "sarah@example.com",
  phone: "+233 123 456 789",
  todayStats: {
    appointmentsCount: 5,
    completedCount: 2,
    cancelledCount: 1,
  },
  todayAppointments: [
    {
      id: 1,
      customerName: "Alice Brown",
      service: "Hair Styling",
      time: "09:00 AM",
      duration: 60,
      status: "completed",
      amount: 50,
    },
    {
      id: 2,
      customerName: "Betty White",
      service: "Manicure",
      time: "10:30 AM",
      duration: 45,
      status: "in-progress",
      amount: 30,
    },
    {
      id: 3,
      customerName: "Carol Smith",
      service: "Massage Therapy",
      time: "12:00 PM",
      duration: 60,
      status: "confirmed",
      amount: 80,
    },
    {
      id: 4,
      customerName: "Diana Prince",
      service: "Facial Treatment",
      time: "02:00 PM",
      duration: 60,
      status: "pending",
      amount: 70,
    },
    {
      id: 5,
      customerName: "Eve Wilson",
      service: "Pedicure",
      time: "04:00 PM",
      duration: 45,
      status: "confirmed",
      amount: 35,
    },
  ],
  upcomingAppointments: [
    {
      id: 6,
      customerName: "Frank Miller",
      service: "Hair Cut",
      date: "2026-03-05",
      time: "10:00 AM",
      status: "confirmed",
    },
    {
      id: 7,
      customerName: "Grace Lee",
      service: "Spa Package",
      date: "2026-03-06",
      time: "02:00 PM",
      status: "confirmed",
    },
  ],
  earnings: [
    { date: "2026-03-01", amount: 320, count: 4 },
    { date: "2026-03-02", amount: 280, count: 3 },
    { date: "2026-03-03", amount: 450, count: 6 },
    { date: "2026-03-04", amount: 250, count: 5 },
  ],
  monthlyAttendance: [
    { date: "2026-03-01", status: "present" },
    { date: "2026-03-02", status: "present" },
    { date: "2026-03-03", status: "late" },
    { date: "2026-03-04", status: "present" },
    { date: "2026-03-05", status: "present" },
    { date: "2026-03-06", status: "absent" },
  ],
  services: [
    { id: 1, name: "Hair Cut & Style", price: 85 },
    { id: 2, name: "Balayage", price: 220 },
    { id: 3, name: "Gel Manicure", price: 55 },
    { id: 4, name: "Hydra Facial", price: 120 },
  ],
  products: [
    { id: 1, name: "L'Oreal Serum", currentStock: 8 },
    { id: 2, name: "OPI Gel Polish", currentStock: 2 },
    { id: 3, name: "Bleach Powder", currentStock: 15 },
    { id: 4, name: "Cetaphil Cleanser", currentStock: 3 },
  ],
  orders: [
    { id: 1, productId: 2, quantity: 5, serviceId: 3, status: "pending", date: "2026-03-05" },
    { id: 2, productId: 1, quantity: 2, serviceId: 4, status: "completed", date: "2026-03-04" },
  ],
};

const pageTitle = computed(() => {
  const titles = {
    dashboard: "Staff Dashboard",
    appointments: "My Appointments",
    "order-products": "Order Products",
    profile: "My Profile",
  };
  return titles[currentView.value] || "Staff Dashboard";
});

const getStatusBadgeClass = (status) => {
  const badges = {
    completed: "badge-green",
    "in-progress": "badge-blue",
    confirmed: "badge-gold",
    pending: "badge-gray",
    cancelled: "badge-red",
  };
  return badges[status] || "badge-gray";
};

const getAttendanceBadgeClass = (status) => {
  const badges = {
    present: "badge-green",
    absent: "badge-red",
    late: "badge-orange",
  };
  return badges[status] || "badge-gray";
};

const getOrderStatusBadgeClass = (status) => {
  const badges = {
    pending: "badge-gray",
    completed: "badge-green",
    cancelled: "badge-red",
  };
  return badges[status] || "badge-gray";
};

const getProductName = (productId) => {
  const product = staffData.products.find(p => p.id === productId);
  return product ? product.name : "Unknown";
};

const getServiceName = (serviceId) => {
  const service = staffData.services.find(s => s.id === serviceId);
  return service ? service.name : "Unknown";
};

const getCategoryForProduct = (productId) => {
  const categoriesMap = {
    1: "Hair Care",
    2: "Nails",
    3: "Hair Care",
    4: "Skin Care"
  };
  return categoriesMap[productId] || "Other";
};

const handleMarkAppointmentComplete = (appt) => {
  appt.status = "completed";
  
  // Create appointment completion notification data
  const completionNotification = {
    appointmentId: appt.id,
    customerName: appt.customerName,
    service: appt.service,
    staffName: staffData.name,
    date: appt.date || new Date().toISOString().split('T')[0],
    time: appt.time,
    duration: appt.duration,
    amount: appt.amount,
    completedAt: new Date().toLocaleTimeString(),
    notes: "Appointment completed. Manager notified to generate invoice."
  };
  
  // Send notification to manager
  console.log("🔔 APPOINTMENT COMPLETION ALERT FOR MANAGER:");
  console.log(JSON.stringify(completionNotification, null, 2));
  console.log(`✅ Appointment #${appt.id} for ${appt.customerName} has been completed.`);
  console.log(`💰 Amount: ₹${appt.amount} | Service: ${appt.service}`);
  console.log("Manager will now generate the invoice...");
  
  // In production, this would be:
  // API.post('/manager/appointment-completed', completionNotification)
};

const handleChangePassword = () => {
  passwordError.value = "";
  passwordSuccess.value = "";

  if (!passwordForm.value.currentPassword) {
    passwordError.value = "Current password is required";
    return;
  }

  if (!passwordForm.value.newPassword) {
    passwordError.value = "New password is required";
    return;
  }

  if (passwordForm.value.newPassword.length < 8) {
    passwordError.value = "New password must be at least 8 characters";
    return;
  }

  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    passwordError.value = "Passwords do not match";
    return;
  }

  if (passwordForm.value.currentPassword === passwordForm.value.newPassword) {
    passwordError.value = "New password must be different from current password";
    return;
  }

  passwordSuccess.value = "Password changed successfully!";
  
  setTimeout(() => {
    passwordForm.value = {
      currentPassword: "",
      newPassword: "",
      confirmPassword: ""
    };
    passwordSuccess.value = "";
    showChangePasswordModal.value = false;
  }, 1500);
};

const handleMarkAttendance = () => {
  attendanceError.value = "";
  attendanceSuccess.value = "";

  if (!attendanceForm.value.date) {
    attendanceError.value = "Date is required";
    return;
  }

  if (!attendanceForm.value.status) {
    attendanceError.value = "Status is required";
    return;
  }

  // Check if attendance already exists for this date
  const existingIndex = staffData.monthlyAttendance.findIndex(
    (record) => record.date === attendanceForm.value.date
  );

  if (existingIndex !== -1) {
    // Update existing attendance
    staffData.monthlyAttendance[existingIndex].status = attendanceForm.value.status;
  } else {
    // Add new attendance record
    staffData.monthlyAttendance.push({
      date: attendanceForm.value.date,
      status: attendanceForm.value.status,
    });
  }

  // Sort by date
  staffData.monthlyAttendance.sort((a, b) => new Date(a.date) - new Date(b.date));

  attendanceSuccess.value = `Attendance marked as ${attendanceForm.value.status}!`;
  
  setTimeout(() => {
    attendanceForm.value = {
      date: "",
      status: ""
    };
    attendanceSuccess.value = "";
    showMarkAttendanceModal.value = false;
  }, 1500);
};

const handleOrderProduct = () => {
  orderError.value = "";
  orderSuccess.value = "";

  if (!orderForm.value.productId) {
    orderError.value = "Product is required";
    return;
  }

  if (!orderForm.value.serviceId) {
    orderError.value = "Service is required";
    return;
  }

  // Create new order
  const newOrder = {
    id: Math.max(...staffData.orders.map(o => o.id || 0), 0) + 1,
    productId: parseInt(orderForm.value.productId),
    quantity: orderForm.value.quantity,
    serviceId: parseInt(orderForm.value.serviceId),
    status: "pending",
    date: new Date().toISOString().split('T')[0],
    staffId: 1,  // Would come from authenticated user in production
    staffName: staffData.name
  };

  staffData.orders.push(newOrder);
  orderSuccess.value = `Order placed successfully for ${getProductName(newOrder.productId)}!`;
  
  setTimeout(() => {
    orderForm.value = {
      productId: "",
      quantity: 1,
      serviceId: "",
      selectedCategory: ""
    };
    orderSuccess.value = "";
  }, 1500);
};

const logout = () => {
  // Add logout logic here
  console.log("Logout");
};
</script>

<style scoped>
.booking-item {
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
}

.booking-item:last-child {
  border-bottom: none;
}

.booking-time {
  background: var(--gold);
  color: white;
  padding: 6px 10px;
  border-radius: var(--radius-sm);
  font-weight: 600;
  color: var(--charcoal);
  white-space: nowrap;
  background: var(--ivory);
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--charcoal);
  margin-bottom: 6px;
}

.form-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-family: inherit;
  transition: border-color 0.2s, box-shadow 0.2s;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: var(--gold);
  box-shadow: 0 0 0 3px rgba(229, 170, 84, 0.1);
}

.form-input:disabled {
  background-color: var(--ivory);
  color: var(--text-muted);
}

.form-hint {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 4px;
}

.error-message {
  padding: 10px 12px;
  background: rgba(231, 76, 60, 0.1);
  border-left: 3px solid #e74c3c;
  border-radius: var(--radius-sm);
  color: #c0392b;
  font-size: 13px;
  margin-top: 12px;
}

.success-message {
  padding: 10px 12px;
  background: rgba(39, 174, 96, 0.1);
  border-left: 3px solid #27ae60;
  border-radius: var(--radius-sm);
  color: #229954;
  font-size: 13px;
  margin-top: 12px;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background: white;
  border-radius: var(--radius-md);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 420px;
  max-height: 90vh;
  overflow-y: auto;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  border-bottom: 1px solid var(--border);
}

.modal-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--charcoal);
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.modal-close:hover {
  color: var(--charcoal);
}

.modal-body {
  padding: 20px;
}
</style>
