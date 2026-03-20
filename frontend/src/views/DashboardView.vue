<template>
  <div class="content-layout">
    <!-- Sidebar -->
    <div class="sidebar">
      <div class="sidebar-logo">
        <div class="sidebar-logo-text">Glow Suite</div>
        <div class="sidebar-logo-sub">Beauty Management</div>
      </div>
      <nav class="sidebar-nav">
        <div class="nav-section">Appointment & Services</div>
        <div
          :class="['nav-item', { active: currentView === 'dashboard' }]"
          @click="currentView = 'dashboard'"
        >
          <span class="nav-icon">📊</span> Dashboard
        </div>
        <div
          :class="['nav-item', { active: currentView === 'bookings' }]"
          @click="currentView = 'bookings'"
        >
          <span class="nav-icon">📅</span> Appointments
        </div>
        <div
          :class="['nav-item', { active: currentView === 'services' }]"
          @click="currentView = 'services'"
        >
          <span class="nav-icon">💇</span> Services
        </div>

        <div class="nav-section">Management</div>
        <div
          :class="['nav-item', { active: currentView === 'customers' }]"
          @click="currentView = 'customers'"
        >
          <span class="nav-icon">👥</span> Customers
        </div>
        <div
          :class="['nav-item', { active: currentView === 'staff-by-day' }]"
          @click="currentView = 'staff-by-day'"
        >
          <span class="nav-icon">📅</span> Staff by Day
        </div>
        <div
          :class="['nav-item', { active: currentView === 'staff' }]"
          @click="currentView = 'staff'"
        >
          <span class="nav-icon">👔</span> Staff
        </div>

        <div class="nav-section">Operations</div>
        <div
          :class="['nav-item', { active: currentView === 'inventory' }]"
          @click="currentView = 'inventory'"
        >
          <span class="nav-icon">📦</span> Inventory
        </div>
        <div
          :class="['nav-item', { active: currentView === 'orders' }]"
          @click="currentView = 'orders'"
        >
          <span class="nav-icon">📮</span> Orders ({{ pendingOrders.length }})
        </div>
        <div
          :class="['nav-item', { active: currentView === 'invoices' }]"
          @click="currentView = 'invoices'"
        >
          <span class="nav-icon">📋</span> Invoices
        </div>
        <div
          :class="['nav-item', { active: currentView === 'finance' }]"
          @click="handleFinanceAccess"
        >
          <span class="nav-icon">💰</span> Finance
        </div>
        <div
          :class="['nav-item', { active: currentView === 'reports' }]"
          @click="handleReportsAccess"
        >
          <span class="nav-icon">📄</span> Download Reports
        </div>
      </nav>
      <div class="sidebar-footer">
        <div class="sidebar-user">
          <div class="sidebar-avatar">{{ user.name?.[0] || user.userId?.[0] }}</div>
          <div>
            <div class="sidebar-username">{{ user.name || user.userId }}</div>
            <div class="sidebar-role">{{ user.role }}</div>
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
          <div class="search-bar">
            <span>🔍</span>
            <input type="text" placeholder="Search..." />
          </div>
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
              <div class="stat-value">{{ todayAppointments.length }}</div>
              <div class="stat-label">Appointments Today</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">✅</div>
              <div class="stat-value">{{ staffPresentCount }}</div>
              <div class="stat-label">Staff Present</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">⚠️</div>
              <div class="stat-value">{{ lowStockItems.length }}</div>
              <div class="stat-label">Low Stock Items</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">🚚</div>
              <div class="stat-value">{{ pendingOrders.length }}</div>
              <div class="stat-label">Pending Orders</div>
            </div>
          </div>

          <!-- Available Staff Today -->
          <div class="card" style="margin-bottom: 24px; background: linear-gradient(135deg, var(--ivory) 0%, var(--cream) 100%); border-left: 4px solid var(--gold)">
            <div class="card-body">
              <div style="display: flex; align-items: center; gap: 12px">
                <span style="font-size: 24px">👥</span>
                <div style="flex: 1">
                  <div style="font-weight: 600; color: var(--charcoal); margin-bottom: 8px; font-size: 16px">
                    Available Staff Today
                  </div>
                  <div v-if="todayAvailableStaff.length > 0" style="color: var(--charcoal); font-size: 15px">
                    <div v-for="staff in todayAvailableStaff" :key="staff.id" style="margin-bottom: 12px">
                      <div style="display: inline-block; margin-right: 16px">
                        <span style="background: var(--gold); color: white; padding: 6px 12px; border-radius: 16px; font-size: 14px; font-weight: 600">✓ {{ staff.name }}</span>
                      </div>
                      <div style="font-size: 12px; color: var(--charcoal-light); margin-top: 2px">
                        {{ staff.skills || 'Skills not specified' }}
                      </div>
                    </div>
                  </div>
                  <div v-else style="color: var(--charcoal-light); font-size: 14px">
                    ℹ️ No staff available today
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Alerts & Today's Bookings -->
          <div class="grid-2" style="margin-top: 24px">
            <!-- Today's Appointments -->
            <div class="card">
              <div class="card-header">
                <h3 class="card-title">📅 Today's Appointments</h3>
              </div>
              <div class="card-body">
                <div v-if="todayAppointments.length === 0" class="empty-state">
                  <div class="empty-state-icon">📅</div>
                  <div class="empty-state-text">No appointments today</div>
                </div>
                <div v-for="appt in todayAppointments" :key="appt.id" class="booking-item">
                  <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px">
                    <div class="booking-time">{{ getTimeFromDate(appt.date) }}</div>
                    <div>
                      <div style="font-weight: 600">{{ getCustomerName(appt.customerId) }}</div>
                      <div class="text-muted">{{ getServiceName(appt.serviceId) }}</div>
                    </div>
                  </div>
                  <div style="display: flex; align-items: center; justify-content: space-between">
                    <div class="text-muted" style="font-size: 12px">Staff: {{ getStaffName(appt.staffId) || "Unassigned" }}</div>
                    <span :class="['badge', apptStatusBadge(appt.status)]">{{ appt.status }}</span>
                  </div>
                  <div style="height: 1px; background: var(--border); margin: 8px 0"></div>
                </div>
              </div>
            </div>

            <!-- Alerts Widget -->
            <div class="card">
              <div class="card-header">
                <h3 class="card-title">⚡ Alerts & Notifications</h3>
              </div>
              <div class="card-body">
                <div v-if="systemAlerts.length === 0" class="empty-state">
                  <div class="empty-state-icon">✅</div>
                  <div class="empty-state-text">All systems operational</div>
                </div>
                <div v-for="(alert, idx) in systemAlerts" :key="idx" :class="['alert-item', alert.type]">
                  <div class="alert-icon">{{ alert.icon }}</div>
                  <div style="flex: 1">
                    <div class="alert-title">{{ alert.title }}</div>
                    <div class="alert-message">{{ alert.message }}</div>
                  </div>
                  <div class="alert-time">{{ alert.time }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- APPOINTMENTS VIEW -->
        <div v-if="currentView === 'bookings'" class="fade-in">
          <!-- New Appointment Form -->
          <div class="card" style="margin-bottom: 20px">
            <div class="card-header">
              <h3 class="card-title">📅 Create New Appointment</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleCreateBooking" style="max-width: 800px">
                <div class="form-group">
                  <label>Select Services * (You can choose multiple)</label>
                  <div style="border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 12px; max-height: 300px; overflow-y: auto">
                    <div v-for="service in data.services" :key="service.id" style="display: flex; align-items: center; margin-bottom: 12px">
                      <input 
                        :id="'service-' + service.id"
                        type="checkbox" 
                        :value="service.id" 
                        v-model="bookingForm.serviceIds"
                        style="margin-right: 8px; width: 18px; height: 18px; cursor: pointer"
                      />
                      <label :for="'service-' + service.id" style="cursor: pointer; flex: 1; margin: 0">
                        {{ service.name }} - ₹{{ service.price }} ({{ service.duration || 60 }} min)
                      </label>
                    </div>
                  </div>
                  <div v-if="bookingForm.serviceIds.length === 0" class="text-muted" style="margin-top: 8px; font-size: 12px">Please select at least one service</div>
                </div>

                <div class="grid-2" style="margin-top: 16px">
                  <div class="form-group">
                    <label for="booking-customer">Customer Name *</label>
                    <select 
                      id="booking-customer"
                      v-model="bookingForm.customerId"
                      class="form-input"
                      required
                    >
                      <option value="">Select a customer</option>
                      <option v-for="customer in data.customers" :key="customer.id" :value="customer.id">
                        {{ customer.name }}
                      </option>
                    </select>
                  </div>

                  <div class="form-group">
                    <label for="booking-stylist">Stylist (Optional)</label>
                    <select 
                      id="booking-stylist"
                      v-model="bookingForm.staffId"
                      class="form-input"
                    >
                      <option value="">Choose a stylist (Optional)</option>
                      <option 
                        v-for="staff in data.staff" 
                        :key="staff.id" 
                        :value="staff.id"
                      >
                        {{ staff.name }}{{ staff.skills ? ' - ' + staff.skills : '' }}
                      </option>
                    </select>
                    <div v-if="bookingForm.staffId" class="text-muted" style="font-size: 12px; margin-top: 6px">
                      Selected: {{ data.staff.find(s => s.id == bookingForm.staffId)?.name }}{{ data.staff.find(s => s.id == bookingForm.staffId)?.skills ? ' - Specializes in ' + data.staff.find(s => s.id == bookingForm.staffId)?.skills : '' }}
                    </div>
                  </div>

                  <div class="form-group">
                    <label for="booking-date">Date *</label>
                    <input 
                      id="booking-date"
                      v-model="bookingForm.date"
                      type="date"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="booking-time">Time *</label>
                    <select 
                      id="booking-time"
                      v-model="bookingForm.time"
                      class="form-input"
                      required
                    >
                      <option value="">Choose a time</option>
                      <option value="09:00">09:00</option>
                      <option value="09:30">09:30</option>
                      <option value="10:00">10:00</option>
                      <option value="10:30">10:30</option>
                      <option value="11:00">11:00</option>
                      <option value="11:30">11:30</option>
                      <option value="12:00">12:00</option>
                      <option value="12:30">12:30</option>
                      <option value="13:00">13:00</option>
                      <option value="13:30">13:30</option>
                      <option value="14:00">14:00</option>
                      <option value="14:30">14:30</option>
                      <option value="15:00">15:00</option>
                      <option value="15:30">15:30</option>
                      <option value="16:00">16:00</option>
                      <option value="16:30">16:30</option>
                      <option value="17:00">17:00</option>
                    </select>
                  </div>
                </div>

                <div v-if="bookingError" class="error-message">{{ bookingError }}</div>
                <div v-if="bookingSuccess" class="success-message">{{ bookingSuccess }}</div>

                <button type="submit" class="btn btn-primary" style="margin-top: 16px">
                  Create Appointment ({{ bookingForm.serviceIds.length }} service{{ bookingForm.serviceIds.length !== 1 ? 's' : '' }})
                </button>
              </form>
            </div>
          </div>

          <!-- Horizontal Calendar Strip -->
          <div class="card" style="margin-bottom: 20px">
            <div class="card-header">
              <h3 class="card-title">📆 Calendar - {{ currentMonthYear }}</h3>
            </div>
            <div class="card-body" style="padding: 12px; overflow-x: auto">
              <div style="display: flex; gap: 8px; min-width: min-content">
                <div v-for="date in upcomingDates" :key="date" 
                     :class="['calendar-date-horizontal', { 'has-appointments': getDateBookings(date).length > 0, 'selected': selectedDate === date }]"
                     @click="selectedDate = date"
                     style="cursor: pointer; flex-shrink: 0">
                  <div style="font-size: 11px; color: inherit">{{ formatDateShort(date) }}</div>
                  <div v-if="getDateBookings(date).length > 0" style="font-size: 12px; font-weight: 600; margin-top: 4px">{{ getDateBookings(date).length }} 📅</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Appointments List -->
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">📅 {{ selectedDate ? 'Appointments - ' + formatDateShort(selectedDate) : "All Appointments" }}</h3>
            </div>
            <div class="card-body">
              <div style="margin-bottom: 16px">
                <input 
                  v-model="bookingCustomerName"
                  type="text" 
                  placeholder="🔍 Filter by customer name..." 
                  class="form-input"
                  style="width: 100%; max-width: 300px"
                />
              </div>
              <div v-if="filteredBookings.length === 0" class="empty-state">
                <div class="empty-state-icon">📅</div>
                <div class="empty-state-text">{{ selectedDate ? 'No appointments on this date' : 'No appointments' }}</div>
              </div>
              <div v-for="appt in filteredBookings" :key="appt.id" class="booking-item">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px">
                  <div class="booking-time">{{ getTimeFromDate(appt.date) }}</div>
                  <div>
                    <div style="font-weight: 600">{{ getCustomerName(appt.customerId) }}</div>
                    <div class="text-muted">{{ getServiceName(appt.serviceId) }}</div>
                  </div>
                </div>
                <div style="display: flex; align-items: center; justify-content: space-between">
                  <div style="display: flex; align-items: center; gap: 12px; flex: 1">
                    <div class="text-muted" style="font-size: 12px">Staff: {{ getStaffName(appt.staffId) || "Unassigned" }}</div>
                    <span :class="['badge', apptStatusBadge(appt.status)]">{{ appt.status }}</span>
                  </div>
                  <div style="display: flex; gap: 6px">
                    <button class="btn btn-sm btn-outline" @click="handleEditBooking(appt)" style="padding: 4px 8px; font-size: 11px">
                      ✎ Edit
                    </button>
                    <button class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 11px; color: #e74c3c; border-color: #e74c3c" @click="handleDeleteBooking(appt.id)">
                      🗑 Delete
                    </button>
                  </div>
                </div>
                <div style="height: 1px; background: var(--border); margin: 8px 0"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- SERVICES VIEW -->
        <div v-if="currentView === 'services'" class="fade-in">
          <!-- Add Service Form -->
          <div class="card" style="margin-bottom: 20px">
            <div class="card-header">
              <h3 class="card-title">➕ Add New Service</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleAddService" style="max-width: 800px">
                <div class="grid-2">
                  <div class="form-group">
                    <label for="service-name">Service Name *</label>
                    <input 
                      id="service-name"
                      v-model="serviceForm.name"
                      type="text"
                      placeholder="e.g., Hair Cut & Style"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="service-category">Category *</label>
                    <select 
                      id="service-category"
                      v-model="serviceForm.categoryId"
                      class="form-input"
                      required
                    >
                      <option value="">Select a category</option>
                      <option v-for="cat in data.serviceCategories" :key="cat.id" :value="cat.id">
                        {{ cat.name }}
                      </option>
                    </select>
                  </div>

                  <div class="form-group">
                    <label for="service-price">Price (₹) *</label>
                    <input 
                      id="service-price"
                      v-model.number="serviceForm.price"
                      type="number"
                      placeholder="e.g., 85"
                      class="form-input"
                      required
                      min="0"
                    />
                  </div>

                  <div class="form-group">
                    <label for="service-duration">Duration (minutes) *</label>
                    <input 
                      id="service-duration"
                      v-model.number="serviceForm.duration"
                      type="number"
                      placeholder="e.g., 60"
                      class="form-input"
                      required
                      min="15"
                    />
                  </div>

                  <div class="form-group" style="grid-column: 1 / -1">
                    <label for="service-products">Products Required (comma-separated)</label>
                    <input 
                      id="service-products"
                      v-model="serviceForm.productsRequired"
                      type="text"
                      placeholder="e.g., L'Oreal Serum, Bleach Powder"
                      class="form-input"
                    />
                  </div>


                </div>

                <div v-if="serviceError" class="error-message">{{ serviceError }}</div>
                <div v-if="serviceSuccess" class="success-message">{{ serviceSuccess }}</div>

                <button type="submit" class="btn btn-primary" style="margin-top: 16px">
                  Add Service
                </button>
              </form>
            </div>
          </div>

          <!-- Services Table -->
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">All Services</h3>
            </div>
            <div class="card-body">
              <div style="margin-bottom: 16px">
                <input 
                  v-model="serviceName"
                  type="text" 
                  placeholder="🔍 Filter by service name..." 
                  class="form-input"
                  style="width: 100%; max-width: 300px"
                />
              </div>
              <div class="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Service Name</th>
                      <th>Category</th>
                      <th>Price</th>
                      <th>Duration (min)</th>
                      <th>Products Required</th>
                      <th>Rating</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="service in filteredServices" :key="service.id">
                      <td>{{ service.name }}</td>
                      <td>{{ getCategoryName(service.categoryId) }}</td>
                      <td>₹{{ service.price }}</td>
                      <td>{{ service.duration }}</td>
                      <td class="text-muted" style="font-size: 12px">{{ service.productsRequired || "None" }}</td>
                      <td>{{ service.rating ? service.rating + ' ⭐' : 'No rating' }}</td>
                      <td>
                        <div style="display: flex; gap: 6px">
                          <button class="btn btn-sm btn-outline" @click="handleEditService(service)" style="padding: 4px 8px; font-size: 12px">
                            ✎ Edit
                          </button>
                          <button class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 12px; color: #e74c3c; border-color: #e74c3c" @click="handleDeleteService(service.id)">
                            🗑 Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- CUSTOMERS VIEW -->
        <div v-if="currentView === 'customers'" class="fade-in">
          <!-- Add Customer Form -->
          <div class="card" style="margin-bottom: 20px">
            <div class="card-header">
              <h3 class="card-title">➕ Add New Customer</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleAddCustomer" style="max-width: 800px">
                <div class="grid-2">
                  <div class="form-group">
                    <label for="customer-name">Name *</label>
                    <input 
                      id="customer-name"
                      v-model="customerForm.name"
                      type="text"
                      placeholder="e.g., Sofia Mensah"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="customer-email">Email *</label>
                    <input 
                      id="customer-email"
                      v-model="customerForm.email"
                      type="email"
                      placeholder="e.g., sofia@email.com"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="customer-phone">Phone *</label>
                    <input 
                      id="customer-phone"
                      v-model="customerForm.phone"
                      type="tel"
                      placeholder="e.g., 030-111-2222"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="customer-dob">Date of Birth *</label>
                    <input 
                      id="customer-dob"
                      v-model="customerForm.dob"
                      type="date"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group" style="grid-column: 1 / -1">
                    <label for="customer-address">Address</label>
                    <input 
                      id="customer-address"
                      v-model="customerForm.address"
                      type="text"
                      placeholder="e.g., 14 Cantonments Rd"
                      class="form-input"
                    />
                  </div>

                  <div class="form-group" style="grid-column: 1 / -1">
                    <label for="customer-preferences">Preferences</label>
                    <textarea 
                      id="customer-preferences"
                      v-model="customerForm.preferences"
                      placeholder="e.g., Relaxing massage, No harsh chemicals, etc."
                      class="form-input"
                      style="resize: vertical; min-height: 60px"
                    ></textarea>
                  </div>
                </div>

                <div v-if="customerError" class="error-message">{{ customerError }}</div>
                <div v-if="customerSuccess" class="success-message">{{ customerSuccess }}</div>

                <button type="submit" class="btn btn-primary" style="margin-top: 16px">
                  Add Customer
                </button>
              </form>
            </div>
          </div>

          <!-- Customers Table -->
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">All Customers</h3>
            </div>
            <div class="card-body">
              <div style="margin-bottom: 16px">
                <input 
                  v-model="customerName"
                  type="text" 
                  placeholder="🔍 Filter by name or email..." 
                  class="form-input"
                  style="width: 100%; max-width: 300px"
                />
              </div>
              <div class="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Phone</th>
                      <th>Preferences</th>
                      <th>No. of Visits</th>
                      <th>Invoices</th>
                      <th>Address</th>
                      <th>Registered</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="customer in filteredCustomers" :key="customer.id">
                      <td>{{ customer.name }}</td>
                      <td>{{ customer.email }}</td>
                      <td>{{ customer.phone }}</td>
                      <td style="font-size: 12px; color: #666">{{ customer.preferences || '-' }}</td>
                      <td style="text-align: center; font-weight: 600">{{ customer.noOfVisits || 0 }}</td>
                      <td style="text-align: center"><span class="badge" style="background: var(--gold); color: white">{{ customer.invoices || 0 }}</span></td>
                      <td class="text-muted">{{ customer.address || "N/A" }}</td>
                      <td>{{ customer.registrationDate }}</td>
                      <td>
                        <div style="display: flex; gap: 6px">
                          <button class="btn btn-sm btn-outline" @click="handleEditCustomer(customer)" style="padding: 4px 8px; font-size: 12px">
                            ✎ Edit
                          </button>
                          <button class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 12px; color: #e74c3c; border-color: #e74c3c" @click="handleDeleteCustomer(customer.id)">
                            🗑 Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- STAFF BY DAY VIEW -->
        <div v-if="currentView === 'staff-by-day'" class="fade-in">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">📅 Select Staff by Day</h3>
            </div>
            <div class="card-body">
              <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 24px">
                <label style="font-weight: 600">Select Date:</label>
                <input 
                  v-model="selectedStaffDate" 
                  type="date" 
                  class="form-input"
                  style="max-width: 200px"
                />
              </div>

              <div v-if="staffForSelectedDay.length === 0" style="text-align: center; padding: 32px; color: var(--text-muted)">
                <div style="font-size: 32px; margin-bottom: 12px">📭</div>
                <div style="font-size: 16px">No staff available on {{ selectedStaffDate }}</div>
              </div>

              <div v-else style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px">
                <div v-for="staff in staffForSelectedDay" :key="staff.id" style="border: 1px solid var(--border); border-radius: 8px; padding: 20px; background: var(--light-bg); transition: all 0.3s ease" @mouseenter="hoveredStaff = staff.id" @mouseleave="hoveredStaff = null" :style="{ boxShadow: hoveredStaff === staff.id ? '0 8px 24px rgba(212, 175, 55, 0.2)' : 'none', borderColor: hoveredStaff === staff.id ? 'var(--gold)' : 'var(--border)' }">
                  <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px">
                    <div style="width: 56px; height: 56px; background: linear-gradient(135deg, var(--gold), var(--charcoal)); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px; font-weight: 600">
                      {{ staff.name.charAt(0) }}
                    </div>
                    <div style="flex: 1">
                      <h4 style="margin: 0 0 4px 0; font-weight: 600; font-size: 16px">{{ staff.name }}</h4>
                      <div style="font-size: 12px; color: var(--text-muted)">{{ staff.role }}</div>
                    </div>
                  </div>

                  <div style="background: var(--bg); padding: 12px; border-radius: 6px; margin-bottom: 12px">
                    <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 6px; font-weight: 600">SPECIALTIES</div>
                    <div style="font-size: 13px; line-height: 1.5px">{{ staff.skills }}</div>
                  </div>

                  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px">
                    <div style="background: var(--bg); padding: 10px; border-radius: 6px; text-align: center">
                      <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 4px">Rating</div>
                      <div style="font-weight: 600; color: var(--gold); font-size: 14px">⭐ {{ staff.rating }}</div>
                    </div>
                    <div style="background: var(--bg); padding: 10px; border-radius: 6px; text-align: center">
                      <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 4px">Status</div>
                      <div style="font-weight: 600; color: #22c55e; font-size: 14px">✓ Available</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- STAFF VIEW -->
        <div v-if="currentView === 'staff'" class="fade-in">
          <!-- Add Staff Form -->
          <div class="card" style="margin-bottom: 20px">
            <div class="card-header">
              <h3 class="card-title">➕ Add New Staff</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleAddStaff" style="max-width: 800px">
                <div class="grid-2">
                  <div class="form-group">
                    <label for="staff-name">Name *</label>
                    <input 
                      id="staff-name"
                      v-model="staffForm.name"
                      type="text"
                      placeholder="e.g., Amara Osei"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="staff-role">Role *</label>
                    <input 
                      id="staff-role"
                      v-model="staffForm.role"
                      type="text"
                      placeholder="e.g., Senior Stylist"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="staff-email">Email *</label>
                    <input 
                      id="staff-email"
                      v-model="staffForm.email"
                      type="email"
                      placeholder="e.g., amara@glowsuite.com"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="staff-phone">Phone *</label>
                    <input 
                      id="staff-phone"
                      v-model="staffForm.phone"
                      type="tel"
                      placeholder="e.g., 050-111-2222"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group" style="grid-column: 1 / -1">
                    <label for="staff-skills">Skills *</label>
                    <input 
                      id="staff-skills"
                      v-model="staffForm.skills"
                      type="text"
                      placeholder="e.g., Hair Cutting, Styling, Coloring (comma-separated)"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="staff-doj">Date of Joining *</label>
                    <input 
                      id="staff-doj"
                      v-model="staffForm.doj"
                      type="date"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="staff-salary">Salary (₹) *</label>
                    <input 
                      id="staff-salary"
                      v-model.number="staffForm.salary"
                      type="number"
                      placeholder="e.g., 2000"
                      class="form-input"
                      required
                      min="0"
                    />
                  </div>

                  <div class="form-group" style="grid-column: 1 / -1">
                    <label for="staff-username">Username *</label>
                    <input 
                      id="staff-username"
                      v-model="staffForm.username"
                      type="text"
                      placeholder="e.g., amara01"
                      class="form-input"
                      required
                    />
                  </div>
                </div>

                <div v-if="staffError" class="error-message">{{ staffError }}</div>
                <div v-if="staffSuccess" class="success-message">{{ staffSuccess }}</div>

                <button type="submit" class="btn btn-primary" style="margin-top: 16px">
                  Add Staff
                </button>
              </form>
            </div>
          </div>

          <!-- Staff Members Table -->
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">👔 Staff Members</h3>
            </div>
            <div class="card-body">
              <div style="margin-bottom: 16px">
                <input 
                  v-model="staffName"
                  type="text" 
                  placeholder="🔍 Filter by name or email..." 
                  class="form-input"
                  style="width: 100%; max-width: 300px"
                />
              </div>
              <div class="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Role</th>
                      <th>Skills</th>
                      <th>Email</th>
                      <th>Phone</th>
                      <th>Date of Joining</th>
                      <th>Rating</th>
                      <th>Attendance</th>
                      <th>Today's Appts</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="staff in filteredStaff" :key="staff.id">
                      <td>{{ staff.name }}</td>
                      <td>{{ staff.role }}</td>
                      <td><span style="font-size: 12px; color: #666">{{ staff.skills || '-' }}</span></td>
                      <td>{{ staff.email }}</td>
                      <td>{{ staff.phone }}</td>
                      <td>{{ staff.doj }}</td>
                      <td><span style="font-weight: 600; color: #f5a623">⭐ {{ staff.rating || 'N/A' }}</span></td>
                      <td><span :class="['badge', staffAttendanceBadge(staff.id)]">{{ getStaffAttendance(staff.id) }}</span></td>
                      <td><span style="font-weight: 600">{{ getStaffAppointments(staff.id) }}</span></td>
                      <td><span :class="['badge', staff.status === 'active' ? 'badge-green' : 'badge-red']">{{ staff.status }}</span></td>
                      <td>
                        <div style="display: flex; gap: 6px">
                          <button class="btn btn-sm btn-outline" @click="handleEditStaff(staff)" style="padding: 4px 8px; font-size: 12px">
                            ✎ Edit
                          </button>
                          <button class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 12px; color: #e74c3c; border-color: #e74c3c" @click="handleDeleteStaff(staff.id)">
                            🗑 Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- INVENTORY VIEW -->
        <div v-if="currentView === 'inventory'" class="fade-in">
          <!-- Add Product/Inventory Form -->
          <div class="card" style="margin-bottom: 20px">
            <div class="card-header">
              <h3 class="card-title">➕ Add New Product</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleAddProduct" style="max-width: 800px">
                <div class="grid-2">
                  <div class="form-group">
                    <label for="product-name">Product Name *</label>
                    <input 
                      id="product-name"
                      v-model="inventoryForm.name"
                      type="text"
                      placeholder="e.g., L'Oreal Serum"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="product-category">Category *</label>
                    <input 
                      id="product-category"
                      v-model="inventoryForm.categoryName"
                      type="text"
                      placeholder="e.g., Hair Care"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="product-stock">Stock Quantity *</label>
                    <input 
                      id="product-stock"
                      v-model.number="inventoryForm.stock"
                      type="number"
                      placeholder="e.g., 10"
                      class="form-input"
                      required
                      min="0"
                    />
                  </div>



                  <div class="form-group">
                    <label for="product-minstock">Minimum Stock *</label>
                    <input 
                      id="product-minstock"
                      v-model.number="inventoryForm.minStock"
                      type="number"
                      placeholder="e.g., 5"
                      class="form-input"
                      required
                      min="0"
                    />
                  </div>

                  <div class="form-group">
                    <label for="product-costprice">Cost Price (₹) *</label>
                    <input 
                      id="product-costprice"
                      v-model.number="inventoryForm.costPrice"
                      type="number"
                      placeholder="e.g., 45"
                      class="form-input"
                      required
                      min="0"
                    />
                  </div>

                  <div class="form-group" style="grid-column: 1 / -1">
                    <label for="product-supplier">Supplier *</label>
                    <input 
                      id="product-supplier"
                      v-model="inventoryForm.supplier"
                      type="text"
                      placeholder="e.g., BeautyPro Ltd"
                      class="form-input"
                      required
                    />
                  </div>
                </div>

                <div v-if="inventoryError" class="error-message">{{ inventoryError }}</div>
                <div v-if="inventorySuccess" class="success-message">{{ inventorySuccess }}</div>

                <button type="submit" class="btn btn-primary" style="margin-top: 16px">
                  Add Product
                </button>
              </form>
            </div>
          </div>

          <!-- Inventory Table -->
          <div class="card" style="margin-bottom: 24px">
            <div class="card-header">
              <h3 class="card-title">📦 All Products</h3>
            </div>
            <div class="card-body">
              <div style="margin-bottom: 16px">
                <input 
                  v-model="productName"
                  type="text" 
                  placeholder="🔍 Filter by product name or category..." 
                  class="form-input"
                  style="width: 100%; max-width: 300px"
                />
              </div>
              <div class="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Product</th>
                      <th>Category</th>
                      <th>Stock</th>
                      <th>Min Stock</th>
                      <th>Cost Price</th>
                      <th>Supplier</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="product in filteredProducts" :key="product.id">
                      <td>{{ product.name }}</td>
                      <td>{{ product.categoryName }}</td>
                      <td><span :class="['badge', product.stock <= product.minStock ? 'badge-red' : 'badge-green']">{{ product.stock }} {{ product.unit }}</span></td>
                      <td>{{ product.minStock }}</td>
                      <td>₹{{ product.costPrice }}</td>
                      <td class="text-muted">{{ product.supplier }}</td>
                      <td>
                        <div style="display: flex; gap: 6px">
                          <button class="btn btn-sm btn-outline" @click="handleEditProduct(product)" style="padding: 4px 8px; font-size: 12px">
                            ✎ Edit
                          </button>
                          <button class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 12px; color: #e74c3c; border-color: #e74c3c" @click="handleDeleteProduct(product.id)">
                            🗑 Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Low Stock Alert & Pending Orders Side by Side -->
          <div class="grid-2">
            <!-- Low Stock Alert -->
            <div class="card">
              <div class="card-header">
                <h3 class="card-title">⚠️ Low Stock Items</h3>
              </div>
              <div class="card-body">
                <div v-if="lowStockItems.length === 0" class="empty-state">
                  <div class="empty-state-icon">📦</div>
                  <div class="empty-state-text">All items stocked</div>
                </div>
                <div v-for="product in lowStockItems" :key="product.id" class="low-stock-item">
                  <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px">
                    <div>
                      <div style="font-weight: 600">{{ product.name }}</div>
                      <div class="text-muted">{{ product.categoryName }}</div>
                    </div>
                    <span class="badge badge-red">{{ product.stock }} {{ product.unit }}</span>
                  </div>
                  <div class="progress-bar">
                    <div class="progress-fill" :style="{ width: stockPercentage(product) + '%', background: statusColor(product) }"></div>
                  </div>
                  <div style="display: flex; justify-content: space-between; margin-top: 6px; font-size: 12px">
                    <span class="text-muted">Min: {{ product.minStock }}</span>
                    <span :style="{ color: statusColor(product) }">{{ stockStatus(product) }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Pending Orders -->
            <div class="card">
              <div class="card-header">
                <h3 class="card-title">🚚 Pending Orders</h3>
              </div>
              <div class="card-body">
                <div v-if="pendingOrders.length === 0" class="empty-state">
                  <div class="empty-state-icon">✅</div>
                  <div class="empty-state-text">No pending orders</div>
                </div>
                <div v-for="order in pendingOrders" :key="order.id" class="order-item">
                  <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px">
                    <div>
                      <div style="font-weight: 600">{{ getProductNameForOrder(order.productId) }}</div>
                      <div class="text-muted">Ordered: {{ order.date }}</div>
                    </div>
                    <span class="badge badge-gold">{{ order.qty }} units</span>
                  </div>
                  <div style="display: flex; align-items: center; gap: 8px">
                    <span style="flex: 1" class="text-muted">📝 {{ order.notes }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- FINANCE VIEW -->
        <div v-if="currentView === 'finance'" class="fade-in">
          <div class="stat-grid">
            <div class="stat-card">
              <div class="stat-icon">💰</div>
              <div class="stat-value">{{ totalRevenue }}</div>
              <div class="stat-label">Total Revenue</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">📦</div>
              <div class="stat-value">₹{{ productInventoryCost.toLocaleString() }}</div>
              <div class="stat-label">Product Cost</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">📈</div>
              <div class="stat-value">{{ netProfit }}</div>
              <div class="stat-label">Net Profit</div>
            </div>
          </div>

          <!-- Balance Sheet -->
          <div class="card" style="margin-bottom: 24px">
            <div class="card-header">
              <h3 class="card-title">📊 Balance Sheet</h3>
            </div>
            <div class="card-body">
              <div class="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Item</th>
                      <th style="text-align: right">Amount</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td style="font-weight: 600">Total Revenue</td>
                      <td style="text-align: right; font-weight: 600; color: var(--gold)">₹{{ totalProductCost.toLocaleString() }}</td>
                    </tr>
                    <tr style="border-top: 1px solid var(--border); border-bottom: 1px solid var(--border)">
                      <td colspan="2" style="padding: 8px 0; font-size: 12px; color: var(--text-muted)">Expenses:</td>
                    </tr>
                    <tr>
                      <td style="padding-left: 24px">Staff Salary</td>
                      <td style="text-align: right">₹{{ staffSalaryTotal.toLocaleString() }}</td>
                    </tr>
                    <tr>
                      <td style="padding-left: 24px">Product Cost</td>
                      <td style="text-align: right">₹{{ productInventoryCost.toLocaleString() }}</td>
                    </tr>
                    <tr>
                      <td style="padding-left: 24px">Overhead Bills</td>
                      <td style="text-align: right">₹{{ overheadBillsTotal.toLocaleString() }}</td>
                    </tr>
                    <tr style="border-top: 2px solid var(--border)">
                      <td style="font-weight: 600; padding-top: 12px">Net Profit</td>
                      <td style="text-align: right; font-weight: 600; padding-top: 12px; color: #27ae60">₹{{ Math.max(0, calculatedNetProfit).toLocaleString() }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>


        </div>

        <!-- ORDERS VIEW -->
        <div v-if="currentView === 'orders'" class="fade-in">
          <!-- Pending Staff Orders -->
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">📮 Pending Staff Orders</h3>
            </div>
            <div class="card-body">
              <div style="margin-bottom: 16px">
                <input 
                  v-model="orderFilter"
                  type="text" 
                  placeholder="🔍 Filter by product name or staff name..." 
                  class="form-input"
                  style="width: 100%; max-width: 300px"
                />
              </div>
              <div v-if="filteredOrders.length === 0" class="empty-state">
                <div class="empty-state-icon">✅</div>
                <div class="empty-state-text">{{ orderFilter.trim() ? 'No orders match the filter' : 'No pending orders - all caught up!' }}</div>
              </div>
              <div v-else class="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Order ID</th>
                      <th>Product</th>
                      <th>Date</th>
                      <th>Staff</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="order in filteredOrders" :key="order.id">
                      <td>#{{ order.id }}</td>
                      <td>{{ getProductNameForOrder(order.productId) }}</td>
                      <td>{{ order.date }}</td>
                      <td>{{ order.staffId ? getStaffName(order.staffId) : (order.requestedBy || 'N/A') }}</td>
                      <td>
                        <span class="badge badge-gold">{{ order.status }}</span>
                      </td>
                      <td>
                        <button class="btn btn-sm btn-primary" @click="handleAcceptOrder(order)" style="margin-right: 6px">
                          ✓ Accept
                        </button>
                        <button class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 12px; color: #e74c3c; border-color: #e74c3c" @click="handleRejectOrder(order)">
                          ✕ Reject
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Completed Appointments Awaiting Invoice -->
          <div class="card" style="margin-top: 20px">
            <div class="card-header">
              <h3 class="card-title">🔔 Completed Appointments - Invoice Needed</h3>
            </div>
            <div class="card-body">
              <div style="margin-bottom: 16px">
                <input 
                  v-model="completedAppointmentFilter"
                  type="text" 
                  placeholder="🔍 Filter by customer, staff, or service name..." 
                  class="form-input"
                  style="width: 100%; max-width: 300px"
                />
              </div>
              <div v-if="filteredCompletedAppointments.length === 0" class="empty-state">
                <div class="empty-state-icon">✨</div>
                <div class="empty-state-text">{{ completedAppointmentFilter.trim() ? 'No appointments match the filter' : 'No completed appointments awaiting invoices' }}</div>
              </div>
              <div v-else class="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Appointment ID</th>
                      <th>Customer</th>
                      <th>Staff</th>
                      <th>Service</th>
                      <th>Date</th>
                      <th>Invoice Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="appt in filteredCompletedAppointments" :key="appt.id">
                      <td>#{{ appt.id }}</td>
                      <td>{{ getCustomerName(appt.customerId) }}</td>
                      <td>{{ getStaffName(appt.staffId) || "Unassigned" }}</td>
                      <td>{{ getServiceName(appt.serviceId) }}</td>
                      <td>{{ appt.date }}</td>
                      <td><strong>{{ appt.invoiceStatus }}</strong></td>
                      <td>
                        <button class="btn btn-sm btn-primary" @click="handleCreateInvoiceFromAppointment(appt)">
                          📄 Create Invoice
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- INVOICES VIEW -->
        <div v-if="currentView === 'invoices'" class="fade-in">
          <!-- Add Invoice Form -->
          <div class="card" style="margin-bottom: 20px">
            <div class="card-header">
              <h3 class="card-title">➕ Create New Invoice</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleAddInvoice" style="max-width: 800px">
                <div class="grid-2">
                  <div class="form-group">
                    <label for="invoice-appointment">Select Appointment *</label>
                    <select 
                      id="invoice-appointment"
                      @change="handleAppointmentSelect"
                      class="form-input"
                      required
                    >
                      <option value="">Choose an appointment</option>
                      <option v-for="appt in data.appointments" :key="appt.id" :value="appt.id">
                        {{ getCustomerName(appt.customerId) }} - {{ getServiceName(appt.serviceId) }} ({{ appt.date }})
                      </option>
                    </select>
                  </div>
                </div>
                <div class="grid-2" style="margin-top: 16px; opacity: 0.7">
                  <div class="form-group">
                    <label>Customer</label>
                    <input type="text" :value="getCustomerName(invoiceForm.customerId)" class="form-input" disabled />
                  </div>
                  <div class="form-group">
                    <label>Service</label>
                    <input type="text" :value="getServiceName(invoiceForm.serviceId)" class="form-input" disabled />
                  </div>
                  <div class="form-group">
                    <label>Invoice Date</label>
                    <input type="text" :value="invoiceForm.date" class="form-input" disabled />
                  </div>
                </div>

                <div class="grid-2" style="margin-top: 16px">
                  <div class="form-group">
                    <label for="invoice-payment">Payment Type *</label>
                    <select 
                      id="invoice-payment"
                      v-model="invoiceForm.paymentType"
                      class="form-input"
                      required
                    >
                      <option value="cash">Cash</option>
                      <option value="card">Card</option>
                    </select>
                  </div>

                  <div class="form-group">
                    <label for="invoice-discount">Discount (%) *</label>
                    <input 
                      id="invoice-discount"
                      v-model.number="invoiceForm.discount"
                      type="number"
                      placeholder="e.g., 10"
                      class="form-input"
                      required
                      min="0"
                      max="100"
                    />
                  </div>
                </div>

                <div v-if="invoiceError" class="error-message">{{ invoiceError }}</div>
                <div v-if="invoiceSuccess" class="success-message">{{ invoiceSuccess }}</div>

                <button type="submit" class="btn btn-primary" style="margin-top: 16px">
                  Create Invoice
                </button>
              </form>
            </div>
          </div>

          <div class="stat-grid">
            <div class="stat-card">
              <div class="stat-icon">📋</div>
              <div class="stat-value">{{ data.appointments.length }}</div>
              <div class="stat-label">Total Invoices</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">✅</div>
              <div class="stat-value">{{ invoicedAppointments.length }}</div>
              <div class="stat-label">Paid</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">⏳</div>
              <div class="stat-value">{{ pendingInvoices.length }}</div>
              <div class="stat-label">Pending</div>
            </div>
          </div>

          <div class="card">
            <div class="card-header">
              <h3 class="card-title">All Invoices</h3>
            </div>
            <div class="card-body">
              <div style="margin-bottom: 16px">
                <input 
                  v-model="invoiceCustomerName"
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
                      <th>Invoice ID</th>
                      <th>Customer</th>
                      <th>Service</th>
                      <th>Amount</th>
                      <th>Date</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(appt, idx) in filteredInvoices" :key="appt.id">
                      <td>#INV{{ String(1000 + idx).slice(-4) }}</td>
                      <td>{{ getCustomerName(appt.customerId) }}</td>
                      <td>{{ getServiceName(appt.serviceId) }}</td>
                      <td>₹{{ getServicePrice(appt.serviceId) }}</td>
                      <td>{{ appt.date }}</td>
                      <td><span :class="['badge', appt.invoiceStatus === 'invoiced' ? 'badge-green' : 'badge-gold']">{{ appt.invoiceStatus }}</span></td>
                      <td>
                        <div style="display: flex; gap: 6px">
                          <button class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 12px">
                            📄 View
                          </button>
                          <button class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 12px; color: #27ae60; border-color: #27ae60" @click="handleSendInvoice(appt)">
                            📧 Send
                          </button>
                          <button class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 12px; color: #e74c3c; border-color: #e74c3c" @click="handleDeleteInvoice(appt.id)">
                            🗑 Delete
                          </button>
                        </div>
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
                  <div class="report-title">Appointments Report</div>
                  <div class="text-muted" style="margin: 8px 0">All appointments and schedules</div>
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

  <!-- Change Password Modal -->
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

  <!-- Financial Password Modal -->
  <div v-if="showFinancePasswordModal" class="modal-overlay" @click.self="showFinancePasswordModal = false">
    <div class="modal-content" @click.stop style="max-width: 400px">
      <div class="modal-header">
        <h3 class="modal-title">🔐 Service Password Required</h3>
        <button class="modal-close" @click="showFinancePasswordModal = false">✕</button>
      </div>
      <div class="modal-body">
        <p style="color: var(--text-muted); margin-bottom: 16px; font-size: 14px">
          This section requires authentication.
        </p>
        <form @submit.prevent="verifyFinancialPassword">
          <div class="form-group">
            <label for="financial-password">Enter Password</label>
            <input 
              id="financial-password"
              v-model="financialPasswordInput" 
              type="password" 
              placeholder="Enter password"
              class="form-input"
              required
              autofocus
            />
          </div>
          <div v-if="financialPasswordError" class="error-message">{{ financialPasswordError }}</div>
          <div style="display: flex; gap: 12px; margin-top: 20px">
            <button type="button" class="btn btn-outline" @click="showFinancePasswordModal = false" style="flex: 1">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" style="flex: 1">
              Verify
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- Reports Password Modal -->
  <div v-if="showReportsPasswordModal" class="modal-overlay" @click.self="showReportsPasswordModal = false">
    <div class="modal-content" @click.stop style="max-width: 400px">
      <div class="modal-header">
        <h3 class="modal-title">🔐 Service Password Required</h3>
        <button class="modal-close" @click="showReportsPasswordModal = false">✕</button>
      </div>
      <div class="modal-body">
        <p style="color: var(--text-muted); margin-bottom: 16px; font-size: 14px">
          This section requires authentication.
        </p>
        <form @submit.prevent="verifyReportsPassword">
          <div class="form-group">
            <label for="reports-password">Enter Password</label>
            <input 
              id="reports-password"
              v-model="financialPasswordInput" 
              type="password" 
              placeholder="Enter password"
              class="form-input"
              required
              autofocus
            />
          </div>
          <div v-if="financialPasswordError" class="error-message">{{ financialPasswordError }}</div>
          <div style="display: flex; gap: 12px; margin-top: 20px">
            <button type="button" class="btn btn-outline" @click="showReportsPasswordModal = false" style="flex: 1">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" style="flex: 1">
              Verify
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useAppStore } from "@/stores/appStore";

const router = useRouter();
const appStore = useAppStore();

const currentView = ref("dashboard");
const selectedDate = ref(null);
const selectedStaffDate = ref(new Date().toISOString().split('T')[0]);
const hoveredStaff = ref(null);
const showChangePasswordModal = ref(false);
const passwordForm = ref({
  currentPassword: "",
  newPassword: "",
  confirmPassword: ""
});
const passwordError = ref("");
const passwordSuccess = ref("");

// Financial section password protection
const showFinancePasswordModal = ref(false);
const showReportsPasswordModal = ref(false);
const financialPasswordInput = ref("");
const financialPasswordError = ref("");
const financeAuthenticated = ref(false);
const reportsAuthenticated = ref(false);
const pendingFinancialView = ref(null); // Track which view user tried to access

// Booking form state
const bookingForm = ref({
  customerId: "",
  serviceIds: [],
  date: "",
  time: "",
  staffId: ""
});
const bookingError = ref("");
const bookingSuccess = ref("");

// Service form state
const serviceForm = ref({
  name: "",
  categoryId: "",
  price: 0,
  duration: 0,
  productsRequired: ""
});
const serviceError = ref("");
const serviceSuccess = ref("");

// Customer form state
const customerForm = ref({
  name: "",
  email: "",
  phone: "",
  dob: "",
  address: "",
  preferences: ""
});
const customerError = ref("");
const customerSuccess = ref("");

// Staff form state
const staffForm = ref({
  name: "",
  role: "",
  email: "",
  phone: "",
  skills: "",
  doj: "",
  salary: 0,
  username: ""
});
const staffError = ref("");
const staffSuccess = ref("");

// Invoice form state
const invoiceForm = ref({
  customerId: "",
  serviceId: "",
  date: "",
  paymentType: "cash",
  discount: 0
});
const invoiceError = ref("");
const invoiceSuccess = ref("");

// Inventory/Product form state
const inventoryForm = ref({
  name: "",
  categoryName: "",
  stock: 0,
  minStock: 0,
  costPrice: 0,
  supplier: ""
});
const inventoryError = ref("");
const inventorySuccess = ref("");

// Filter states
const serviceName = ref("");
const customerName = ref("");
const staffName = ref("");
const productName = ref("");
const invoiceCustomerName = ref("");
const bookingCustomerName = ref("");
const orderFilter = ref("");
const completedAppointmentFilter = ref("");

const user = computed(() => appStore.user);
const data = computed(() => appStore.data);

const today = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
};

const todayAppointments = computed(() => {
  return data.value.appointments.filter(a => a.date === today());
});

const staffPresentCount = computed(() => {
  return data.value.attendance.filter(a => a.date === today() && a.status === "present").length;
});

const todayAvailableStaff = computed(() => {
  const todayDate = today();
  return data.value.staff.filter(staff => {
    const isPresent = data.value.attendance.find(
      a => a.staffId === staff.id && a.date === todayDate && a.status === "present"
    );
    return !!isPresent;
  });
});

const staffForSelectedDay = computed(() => {
  return data.value.staff.filter(staff => {
    const isPresent = data.value.attendance.find(
      a => a.staffId === staff.id && a.date === selectedStaffDate.value && a.status === "present"
    );
    return !!isPresent;
  });
});

const lowStockItems = computed(() => {
  return data.value.products.filter(p => p.stock <= p.minStock);
});

const pendingOrders = computed(() => {
  return data.value.orders.filter(o => o.status === "pending");
});

const completedAppointments = computed(() => {
  return data.value.appointments.filter(a => a.status === "completed" && !a.invoiceGenerated);
});

const systemAlerts = computed(() => {
  const alerts = [];

  // Check for absent staff
  const absentStaff = data.value.attendance.filter(a => a.date === today() && a.status === "absent");
  absentStaff.forEach(att => {
    const staff = data.value.staff.find(s => s.id === att.staffId);
    if (staff) {
      alerts.push({
        type: "warning",
        icon: "⚠️",
        title: "Staff Absent",
        message: `${staff.name} is marked absent today`,
        time: "Today"
      });
    }
  });

  // Check for out of stock items
  const outOfStock = data.value.products.filter(p => p.stock === 0);
  if (outOfStock.length > 0) {
    alerts.push({
      type: "error",
      icon: "🚨",
      title: "Out of Stock",
      message: `${outOfStock.length} item(s) are out of stock`,
      time: "Now"
    });
  }

  // Check for pending deliveries
  const pendingDeliveries = data.value.orders.filter(o => o.status === "pending");
  if (pendingDeliveries.length > 0) {
    alerts.push({
      type: "info",
      icon: "🚚",
      title: "Pending Delivery",
      message: `${pendingDeliveries.length} order(s) awaiting delivery`,
      time: "Pending"
    });
  }

  return alerts;
});

const pageTitle = computed(() => {
  const titles = {
    dashboard: "Manager Dashboard",
    bookings: "Appointments",
    services: "Services",
    customers: "Customers",
    "staff-by-day": "Staff by Day",
    staff: "Staff Management",
    inventory: "Inventory Management",
    invoices: "Invoices",
    finance: "Finance & Reports",
    reports: "Download Reports",
  };
  return titles[currentView.value] || "Dashboard";
});

const invoicedAppointments = computed(() => {
  return data.value.appointments.filter(a => a.invoiceStatus === "invoiced");
});

const pendingInvoices = computed(() => {
  return data.value.appointments.filter(a => a.invoiceStatus === "pending");
});

const totalRevenue = computed(() => {
  return "₹" + invoicedAppointments.value
    .reduce((sum, appt) => {
      const service = data.value.services.find(s => s.id === appt.serviceId);
      return sum + (service?.price || 0);
    }, 0)
    .toLocaleString();
});

const totalProductCost = computed(() => {
  return invoicedAppointments.value
    .reduce((sum, appt) => {
      const service = data.value.services.find(s => s.id === appt.serviceId);
      return sum + (service?.price || 0);
    }, 0);
});

const productInventoryCost = computed(() => {
  return data.value.products.reduce((sum, product) => {
    return sum + (product.costPrice * product.stock);
  }, 0);
});

const netProfit = computed(() => {
  const revenue = totalProductCost.value;
  const cost = productInventoryCost.value;
  return "₹" + (revenue - cost).toLocaleString();
});

const staffSalaryTotal = computed(() => {
  return data.value.staff.reduce((sum, staff) => {
    return sum + (staff.salary || 0);
  }, 0);
});

const serviceCommissionTotal = computed(() => {
  return Math.round(totalProductCost.value * 0.05); // 5% commission on services
});

const overheadBillsTotal = computed(() => {
  return 5000; // Fixed overhead bills amount
});

const calculatedNetProfit = computed(() => {
  const revenue = totalProductCost.value;
  const staffSalary = staffSalaryTotal.value;
  const productCost = productInventoryCost.value;
  const overhead = overheadBillsTotal.value;
  return revenue - staffSalary - productCost - overhead;
});

const currentMonthYear = computed(() => {
  const now = new Date();
  const months = ["January", "February", "March", "April", "May", "June", 
                  "July", "August", "September", "October", "November", "December"];
  return `${months[now.getMonth()]} ${now.getFullYear()}`;
});

const upcomingDates = computed(() => {
  const dates = [];
  const today = new Date();
  
  // Start from beginning of current month
  const startDate = new Date(today.getFullYear(), today.getMonth(), 1);
  
  // Go through 60 days (roughly 2 months)
  for (let i = 0; i < 60; i++) {
    const date = new Date(startDate);
    date.setDate(date.getDate() + i);
    const dateStr = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
    dates.push(dateStr);
  }
  return dates;
});

const getDateBookings = (date) => {
  return data.value.appointments.filter(a => a.date === date);
};

const getAvailableStaffForDate = (date) => {
  return data.value.staff.filter(staff => {
    const isPresent = data.value.attendance.find(
      a => a.staffId === staff.id && a.date === date && a.status === "present"
    );
    return !!isPresent;
  });
};

const formatDateShort = (dateStr) => {
  const [year, month, day] = dateStr.split("-");
  const date = new Date(parseInt(year), parseInt(month) - 1, parseInt(day));
  const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  const dayName = days[date.getDay()];
  return `${dayName} ${parseInt(day)} / ${parseInt(month)}`;
};

const displayedBookings = computed(() => {
  if (selectedDate.value) {
    return getDateBookings(selectedDate.value);
  }
  return todayAppointments.value;
});

// Filtered data computed properties
const filteredServices = computed(() => {
  if (!serviceName.value.trim()) return data.value.services;
  return data.value.services.filter(s => 
    s.name.toLowerCase().includes(serviceName.value.toLowerCase())
  );
});

const filteredCustomers = computed(() => {
  if (!customerName.value.trim()) return data.value.customers;
  return data.value.customers.filter(c => 
    c.name.toLowerCase().includes(customerName.value.toLowerCase()) ||
    c.email.toLowerCase().includes(customerName.value.toLowerCase())
  );
});

const filteredStaff = computed(() => {
  if (!staffName.value.trim()) return data.value.staff;
  return data.value.staff.filter(s => 
    s.name.toLowerCase().includes(staffName.value.toLowerCase()) ||
    s.email.toLowerCase().includes(staffName.value.toLowerCase())
  );
});

const filteredProducts = computed(() => {
  if (!productName.value.trim()) return data.value.products;
  return data.value.products.filter(p => 
    p.name.toLowerCase().includes(productName.value.toLowerCase()) ||
    p.categoryName.toLowerCase().includes(productName.value.toLowerCase())
  );
});

const filteredInvoices = computed(() => {
  if (!invoiceCustomerName.value.trim()) return data.value.appointments;
  return data.value.appointments.filter(appt => {
    const customerNameStr = getCustomerName(appt.customerId).toLowerCase();
    return customerNameStr.includes(invoiceCustomerName.value.toLowerCase());
  });
});

const filteredBookings = computed(() => {
  if (!bookingCustomerName.value.trim()) return displayedBookings.value;
  return displayedBookings.value.filter(appt => {
    const customerNameStr = getCustomerName(appt.customerId).toLowerCase();
    return customerNameStr.includes(bookingCustomerName.value.toLowerCase());
  });
});

const filteredOrders = computed(() => {
  if (!orderFilter.value.trim()) return pendingOrders.value;
  return pendingOrders.value.filter(order => {
    const productName = getProductNameForOrder(order.productId).toLowerCase();
    const staffName = (order.staffId ? getStaffName(order.staffId) : (order.requestedBy || "N/A")).toLowerCase();
    const searchTerm = orderFilter.value.toLowerCase();
    return productName.includes(searchTerm) || staffName.includes(searchTerm);
  });
});

const filteredCompletedAppointments = computed(() => {
  if (!completedAppointmentFilter.value.trim()) return completedAppointments.value;
  return completedAppointments.value.filter(appt => {
    const customerNameStr = getCustomerName(appt.customerId).toLowerCase();
    const staffNameStr = (getStaffName(appt.staffId) || "Unassigned").toLowerCase();
    const serviceNameStr = getServiceName(appt.serviceId).toLowerCase();
    const searchTerm = completedAppointmentFilter.value.toLowerCase();
    return customerNameStr.includes(searchTerm) || 
           staffNameStr.includes(searchTerm) || 
           serviceNameStr.includes(searchTerm);
  });
});

// Helper functions
const getCustomerName = (id) => {
  return data.value.customers.find(c => c.id === id)?.name || "Unknown";
};

const getServiceName = (id) => {
  return data.value.services.find(s => s.id === id)?.name || "Unknown";
};

const getServicePrice = (id) => {
  return data.value.services.find(s => s.id === id)?.price || 0;
};

const getStaffName = (id) => {
  return data.value.staff.find(s => s.id === id)?.name || null;
};

const getCategoryName = (id) => {
  return data.value.serviceCategories.find(c => c.id === id)?.name || "Unknown";
};

const getProductNameForOrder = (id) => {
  return data.value.products.find(p => p.id === id)?.name || "Unknown";
};

const getStaffAttendance = (staffId) => {
  const att = data.value.attendance.find(a => a.staffId === staffId && a.date === today());
  return att?.status || "not marked";
};

const getStaffAppointments = (staffId) => {
  return data.value.appointments.filter(a => a.staffId === staffId && a.date === today()).length;
};

const getTimeFromDate = (dateStr) => {
  // For demo, return a time range
  return "10:00 AM"; // In real app, parse from full datetime
};

const apptStatusBadge = (status) => {
  const badges = {
    completed: "badge-green",
    "in-progress": "badge-blue",
    confirmed: "badge-gold",
    pending: "badge-gray",
  };
  return badges[status] || "badge-gray";
};

const staffAttendanceBadge = (staffId) => {
  const attendance = getStaffAttendance(staffId);
  return attendance === "present" ? "badge-green" : "badge-red";
};

const stockPercentage = (product) => {
  const percentage = (product.stock / product.minStock) * 100;
  return Math.min(100, percentage);
};

const statusColor = (product) => {
  if (product.stock === 0) return "#e74c3c";
  if (product.stock <= product.minStock) return "#e67e22";
  return "#27ae60";
};

const stockStatus = (product) => {
  if (product.stock === 0) return "Out of Stock";
  if (product.stock <= product.minStock) return "Low Stock";
  return "In Stock";
};

const logout = () => {
  appStore.logout();
  router.push("/");
};

const handleChangePassword = () => {
  passwordError.value = "";
  passwordSuccess.value = "";

  // Validation
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

  // In a real application, validate the current password with backend
  // For now, we'll just show success and reset the form
  passwordSuccess.value = "Password changed successfully!";
  
  // Reset form
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

// Booking handlers
const handleCreateBooking = () => {
  bookingError.value = "";
  bookingSuccess.value = "";

  if (!bookingForm.value.customerId) {
    bookingError.value = "Please select a customer";
    return;
  }

  if (bookingForm.value.serviceIds.length === 0) {
    bookingError.value = "Please select at least one service";
    return;
  }

  if (!bookingForm.value.date) {
    bookingError.value = "Please select a date";
    return;
  }

  if (!bookingForm.value.time) {
    bookingError.value = "Please select a time";
    return;
  }

  // Create a booking for each selected service
  const serviceNames = bookingForm.value.serviceIds.map(serviceId => {
    const service = data.value.services.find(s => s.id == serviceId);
    return service ? service.name : '';
  }).filter(Boolean).join(', ');

  const newBooking = {
    id: Math.max(...data.value.appointments.map(a => a.id || 0), 0) + 1,
    customerId: parseInt(bookingForm.value.customerId),
    serviceId: parseInt(bookingForm.value.serviceIds[0]),
    services: bookingForm.value.serviceIds.map(s => parseInt(s)),
    serviceNames: serviceNames,
    date: bookingForm.value.date,
    status: "confirmed",
    notes: bookingForm.value.time,
    invoiceStatus: "pending",
    staffId: bookingForm.value.staffId ? parseInt(bookingForm.value.staffId) : null
  };

  data.value.appointments.push(newBooking);
  bookingSuccess.value = `Booking created successfully for ${serviceNames}!`;

  setTimeout(() => {
    bookingForm.value = {
      customerId: "",
      serviceIds: [],
      date: "",
      time: "",
      staffId: ""
    };
    bookingSuccess.value = "";
  }, 1500);
};

// Service handlers
const handleAddService = () => {
  serviceError.value = "";
  serviceSuccess.value = "";

  if (!serviceForm.value.name) {
    serviceError.value = "Service name is required";
    return;
  }

  if (!serviceForm.value.categoryId) {
    serviceError.value = "Please select a category";
    return;
  }

  if (!serviceForm.value.price || serviceForm.value.price <= 0) {
    serviceError.value = "Price must be greater than 0";
    return;
  }

  if (!serviceForm.value.duration || serviceForm.value.duration < 15) {
    serviceError.value = "Duration must be at least 15 minutes";
    return;
  }

  const newService = {
    id: Math.max(...data.value.services.map(s => s.id || 0), 0) + 1,
    categoryId: parseInt(serviceForm.value.categoryId),
    name: serviceForm.value.name,
    price: serviceForm.value.price,
    duration: serviceForm.value.duration,
    description: `${serviceForm.value.name} service`,
    productsRequired: serviceForm.value.productsRequired || "None"
  };

  data.value.services.push(newService);
  serviceSuccess.value = "Service added successfully!";

  setTimeout(() => {
    serviceForm.value = {
      name: "",
      categoryId: "",
      price: 0,
      duration: 0,
      productsRequired: ""
    };
    serviceSuccess.value = "";
  }, 1500);
};

const handleEditService = (service) => {
  serviceForm.value = {
    name: service.name,
    categoryId: service.categoryId,
    price: service.price,
    duration: service.duration,
    productsRequired: service.productsRequired || ""
  };
};

const handleDeleteService = (serviceId) => {
  if (confirm("Are you sure you want to delete this service?")) {
    const index = data.value.services.findIndex(s => s.id === serviceId);
    if (index > -1) {
      data.value.services.splice(index, 1);
    }
  }
};

// Customer handlers
const handleAddCustomer = () => {
  customerError.value = "";
  customerSuccess.value = "";

  if (!customerForm.value.name) {
    customerError.value = "Customer name is required";
    return;
  }

  if (!customerForm.value.email) {
    customerError.value = "Email is required";
    return;
  }

  if (!customerForm.value.phone) {
    customerError.value = "Phone is required";
    return;
  }

  if (!customerForm.value.dob) {
    customerError.value = "Date of birth is required";
    return;
  }

  const newCustomer = {
    id: Math.max(...data.value.customers.map(c => c.id || 0), 0) + 1,
    name: customerForm.value.name,
    email: customerForm.value.email,
    phone: customerForm.value.phone,
    dob: customerForm.value.dob,
    address: customerForm.value.address || "",
    preferences: customerForm.value.preferences || "",
    invoices: 0,
    noOfVisits: 0,
    registrationDate: new Date().toISOString().split('T')[0],
    password: "pass123"
  };

  data.value.customers.push(newCustomer);
  customerSuccess.value = "Customer added successfully!";

  setTimeout(() => {
    customerForm.value = {
      name: "",
      email: "",
      phone: "",
      dob: "",
      address: ""
    };
    customerSuccess.value = "";
  }, 1500);
};

// Staff handlers
const handleAddStaff = () => {
  staffError.value = "";
  staffSuccess.value = "";

  if (!staffForm.value.name) {
    staffError.value = "Staff name is required";
    return;
  }

  if (!staffForm.value.role) {
    staffError.value = "Role is required";
    return;
  }

  if (!staffForm.value.email) {
    staffError.value = "Email is required";
    return;
  }

  if (!staffForm.value.phone) {
    staffError.value = "Phone is required";
    return;
  }

  if (!staffForm.value.skills) {
    staffError.value = "Skills are required";
    return;
  }

  if (!staffForm.value.doj) {
    staffError.value = "Date of joining is required";
    return;
  }

  if (!staffForm.value.salary || staffForm.value.salary <= 0) {
    staffError.value = "Salary must be greater than 0";
    return;
  }

  if (!staffForm.value.username) {
    staffError.value = "Username is required";
    return;
  }

  const newStaff = {
    id: Math.max(...data.value.staff.map(s => s.id || 0), 0) + 1,
    name: staffForm.value.name,
    role: staffForm.value.role,
    email: staffForm.value.email,
    phone: staffForm.value.phone,
    skills: staffForm.value.skills,
    doj: staffForm.value.doj,
    username: staffForm.value.username,
    status: "active",
    registrationDate: staffForm.value.doj,
    salary: staffForm.value.salary
  };

  data.value.staff.push(newStaff);
  staffSuccess.value = "Staff member added successfully!";

  setTimeout(() => {
    staffForm.value = {
      name: "",
      role: "",
      email: "",
      phone: "",
      skills: "",
      doj: "",
      salary: 0,
      username: ""
    };
    staffSuccess.value = "";
  }, 1500);
};

// Invoice handlers
const handleAppointmentSelect = (event) => {
  const appointmentId = parseInt(event.target.value);
  if (!appointmentId) {
    invoiceForm.value.customerId = "";
    invoiceForm.value.serviceId = "";
    invoiceForm.value.date = "";
    return;
  }
  
  const appointment = data.value.appointments.find(a => a.id === appointmentId);
  if (appointment) {
    invoiceForm.value.customerId = appointment.customerId;
    invoiceForm.value.serviceId = appointment.serviceId;
    invoiceForm.value.date = appointment.date;
  }
};

const handleAddInvoice = () => {
  invoiceError.value = "";
  invoiceSuccess.value = "";

  if (!invoiceForm.value.customerId) {
    invoiceError.value = "Please select a customer";
    return;
  }

  if (!invoiceForm.value.serviceId) {
    invoiceError.value = "Please select a service";
    return;
  }

  if (!invoiceForm.value.date) {
    invoiceError.value = "Please select a date";
    return;
  }

  if (invoiceForm.value.discount < 0 || invoiceForm.value.discount > 100) {
    invoiceError.value = "Discount must be between 0 and 100";
    return;
  }

  const newInvoice = {
    id: Math.max(...data.value.appointments.map(a => a.id || 0), 0) + 1,
    customerId: parseInt(invoiceForm.value.customerId),
    serviceId: parseInt(invoiceForm.value.serviceId),
    date: invoiceForm.value.date,
    status: "confirmed",
    invoiceStatus: "pending",
    paymentType: invoiceForm.value.paymentType,
    discount: invoiceForm.value.discount,
    notes: "Invoice created"
  };

  data.value.appointments.push(newInvoice);
  invoiceSuccess.value = "Invoice created successfully!";

  setTimeout(() => {
    invoiceForm.value = {
      customerId: "",
      serviceId: "",
      date: "",
      paymentType: "cash",
      discount: 0
    };
    invoiceSuccess.value = "";
  }, 1500);
};

const handleDeleteInvoice = (appointmentId) => {
  if (confirm("Are you sure you want to delete this invoice?")) {
    const index = data.value.appointments.findIndex(a => a.id === appointmentId);
    if (index > -1) {
      data.value.appointments.splice(index, 1);
    }
  }
};

const handleSendInvoice = (invoice) => {
  const customerEmail = data.value.customers.find(c => c.id === invoice.customerId)?.email;
  const customerName = getCustomerName(invoice.customerId);
  const serviceName = getServiceName(invoice.serviceId);
  const servicePrice = getServicePrice(invoice.serviceId);
  
  if (!customerEmail) {
    alert("Customer email not found!");
    return;
  }

  // Show confirmation dialog
  if (confirm(`Send invoice to ${customerName} (${customerEmail})?\n\nService: ${serviceName}\nAmount: ₹${servicePrice}`)) {
    // In a real application, this would call an API to send email
    // For now, we'll just show a success message
    alert(`✓ Invoice sent successfully to ${customerEmail}!\n\nInvoice Details:\n- Customer: ${customerName}\n- Service: ${serviceName}\n- Amount: ₹${servicePrice}\n- Date: ${invoice.date}`);
  }
};

// Financial section password handlers
const handleFinanceAccess = () => {
  if (financeAuthenticated.value) {
    currentView.value = 'finance';
  } else {
    financialPasswordInput.value = "";
    financialPasswordError.value = "";
    pendingFinancialView.value = 'finance';
    showFinancePasswordModal.value = true;
  }
};

const handleReportsAccess = () => {
  if (reportsAuthenticated.value) {
    currentView.value = 'reports';
  } else {
    financialPasswordInput.value = "";
    financialPasswordError.value = "";
    pendingFinancialView.value = 'reports';
    showReportsPasswordModal.value = true;
  }
};

const verifyFinancialPassword = () => {
  financialPasswordError.value = "";
  
  // Default password is "admin123" - you can change this
  const correctPassword = "admin123";
  
  if (financialPasswordInput.value === correctPassword) {
    financeAuthenticated.value = true;
    showFinancePasswordModal.value = false;
    currentView.value = 'finance';
    financialPasswordInput.value = "";
  } else {
    financialPasswordError.value = "❌ Incorrect password. Please try again.";
    financialPasswordInput.value = "";
  }
};

const verifyReportsPassword = () => {
  financialPasswordError.value = "";
  
  // Default password is "admin123" - you can change this
  const correctPassword = "admin123";
  
  if (financialPasswordInput.value === correctPassword) {
    reportsAuthenticated.value = true;
    showReportsPasswordModal.value = false;
    currentView.value = 'reports';
    financialPasswordInput.value = "";
  } else {
    financialPasswordError.value = "❌ Incorrect password. Please try again.";
    financialPasswordInput.value = "";
  }
};

// Product/Inventory handlers
const handleAddProduct = () => {
  inventoryError.value = "";
  inventorySuccess.value = "";

  if (!inventoryForm.value.name) {
    inventoryError.value = "Product name is required";
    return;
  }

  if (!inventoryForm.value.categoryName) {
    inventoryError.value = "Category is required";
    return;
  }

  if (inventoryForm.value.costPrice <= 0) {
    inventoryError.value = "Cost price must be greater than 0";
    return;
  }

  if (!inventoryForm.value.supplier) {
    inventoryError.value = "Supplier is required";
    return;
  }

  const newProduct = {
    id: Math.max(...data.value.products.map(p => p.id || 0), 0) + 1,
    name: inventoryForm.value.name,
    categoryName: inventoryForm.value.categoryName,
    stock: inventoryForm.value.stock,
    minStock: inventoryForm.value.minStock,
    costPrice: inventoryForm.value.costPrice,
    sellPrice: inventoryForm.value.costPrice * 1.5,
    supplier: inventoryForm.value.supplier,
    supplierContact: "",
    description: `${inventoryForm.value.name} product`
  };

  data.value.products.push(newProduct);
  inventorySuccess.value = "Product added successfully!";

  setTimeout(() => {
    inventoryForm.value = {
      name: "",
      categoryName: "",
      stock: 0,
      minStock: 0,
      costPrice: 0,
      supplier: ""
    };
    inventorySuccess.value = "";
  }, 1500);
};

const handleEditProduct = (product) => {
  inventoryForm.value = {
    name: product.name,
    categoryName: product.categoryName,
    stock: product.stock,
    minStock: product.minStock,
    costPrice: product.costPrice,
    supplier: product.supplier
  };
};

const handleDeleteProduct = (productId) => {
  if (confirm("Are you sure you want to delete this product?")) {
    const index = data.value.products.findIndex(p => p.id === productId);
    if (index > -1) {
      data.value.products.splice(index, 1);
    }
  }
};

// Staff edit/delete handlers
const handleEditStaff = (staff) => {
  staffForm.value = {
    name: staff.name,
    role: staff.role,
    email: staff.email,
    phone: staff.phone,
    skills: staff.skills || "",
    doj: staff.doj,
    salary: staff.salary,
    username: staff.username,
    password: staff.password || ""
  };
};

const handleDeleteStaff = (staffId) => {
  if (confirm("Are you sure you want to delete this staff member?")) {
    const index = data.value.staff.findIndex(s => s.id === staffId);
    if (index > -1) {
      data.value.staff.splice(index, 1);
    }
  }
};

// Customer edit/delete handlers
const handleEditCustomer = (customer) => {
  customerForm.value = {
    name: customer.name,
    email: customer.email,
    phone: customer.phone,
    dob: customer.dob,
    address: customer.address,
    preferences: customer.preferences || ""
  };
};

const handleDeleteCustomer = (customerId) => {
  if (confirm("Are you sure you want to delete this customer?")) {
    const index = data.value.customers.findIndex(c => c.id === customerId);
    if (index > -1) {
      data.value.customers.splice(index, 1);
    }
  }
};

// Booking edit/delete handlers
const handleEditBooking = (booking) => {
  bookingForm.value = {
    customerId: booking.customerId,
    serviceId: booking.serviceId,
    date: booking.date,
    time: booking.notes,
    staffId: booking.staffId
  };
};

const handleDeleteBooking = (bookingId) => {
  if (confirm("Are you sure you want to delete this booking?")) {
    const index = data.value.appointments.findIndex(a => a.id === bookingId);
    if (index > -1) {
      data.value.appointments.splice(index, 1);
    }
  }
};

// Order handlers
const handleAcceptOrder = (order) => {
  const index = data.value.orders.findIndex(o => o.id === order.id);
  if (index > -1) {
    data.value.orders[index].status = "accepted";
    console.log(`✅ Order #${order.id} accepted - Product: ${getProductNameForOrder(order.productId)}, Qty: ${order.quantity || order.qty}`);
  }
};

const handleRejectOrder = (order) => {
  if (confirm(`Are you sure you want to reject order #${order.id}?`)) {
    const index = data.value.orders.findIndex(o => o.id === order.id);
    if (index > -1) {
      data.value.orders.splice(index, 1);
      console.log(`❌ Order #${order.id} rejected and removed`);
    }
  }
};

const handleCreateInvoiceFromAppointment = (appt) => {
  // Pre-fill invoice form with appointment details
  invoiceForm.value = {
    customerId: appt.customerId,
    serviceId: appt.serviceId || appt.service,
    date: appt.date,
    invoiceStatus: "pending",
    paymentType: "cash",
    discount: 0
  };
  currentView.value = "invoices";
  
  // Mark appointment as invoice generated
  const index = data.value.appointments.findIndex(b => b.id === appt.id);
  if (index > -1) {
    data.value.appointments[index].invoiceGenerated = true;
  }
  
  console.log(`📄 Creating invoice for appointment #${appt.id} (${getCustomerName(appt.customerId)})`);
};
</script>

<style scoped>
.booking-item,
.staff-attendance-item,
.low-stock-item,
.order-item {
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
}

.booking-item:last-child,
.staff-attendance-item:last-child,
.low-stock-item:last-child,
.order-item:last-child {
  border-bottom: none;
}

.booking-time {
  background: var(--gold);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  min-width: 70px;
  text-align: center;
}

.alert-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  border-radius: var(--radius-sm);
  margin-bottom: 8px;
  border-left: 3px solid;
}

.alert-item.info {
  background: rgba(52, 152, 219, 0.1);
  border-left-color: #3498db;
}

.alert-item.warning {
  background: rgba(230, 126, 34, 0.1);
  border-left-color: #e67e22;
}

.alert-item.error {
  background: rgba(231, 76, 60, 0.1);
  border-left-color: #e74c3c;
}

.alert-icon {
  font-size: 20px;
  margin-top: 2px;
}

.alert-title {
  font-weight: 600;
  font-size: 13px;
  color: var(--charcoal);
}

.alert-message {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
}

.alert-time {
  font-size: 11px;
  color: var(--text-muted);
  white-space: nowrap;
}

.report-item {
  background: white;
  border: 1.5px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 20px;
  text-align: center;
  transition: all 0.2s;
}

.report-item:hover {
  border-color: var(--gold);
  box-shadow: var(--shadow);
}

.report-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.report-title {
  font-weight: 600;
  font-size: 14px;
  color: var(--charcoal);
  margin-bottom: 4px;
}

.calendar-date {
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  background: white;
  border: 1px solid var(--border);
  font-size: 12px;
  color: var(--text);
  transition: all 0.2s;
}

.calendar-date:hover {
  background: var(--ivory);
  border-color: var(--gold);
}

.calendar-date.has-bookings {
  background: var(--gold);
  color: white;
  border-color: var(--gold);
  font-weight: 600;
}

.date-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  background: var(--charcoal);
  color: white;
  border-radius: 50%;
  font-size: 11px;
  font-weight: 600;
}

.calendar-date.has-bookings .date-badge {
  background: white;
  color: var(--gold);
}

.booking-item {
  padding: 0 0 12px 0;
  font-size: 13px;
}

.booking-time {
  background: var(--ivory);
  border-radius: var(--radius-sm);
  padding: 6px 10px;
  font-weight: 600;
  color: var(--charcoal);
  white-space: nowrap;
}

.calendar-date-horizontal {
  padding: 12px;
  border-radius: var(--radius-sm);
  background: white;
  border: 1px solid var(--border);
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 70px;
}

.calendar-date-horizontal:hover {
  background: var(--ivory);
  border-color: var(--gold);
}

.calendar-date-horizontal.has-bookings {
  background: var(--gold);
  color: white;
  border-color: var(--gold);
  font-weight: 600;
}

.calendar-date-horizontal.selected {
  background: var(--charcoal);
  color: white;
  border-color: var(--charcoal);
}

.calendar-date-horizontal.selected.has-bookings {
  background: var(--charcoal);
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

/* Form Styles */
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
</style>

