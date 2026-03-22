<template>
  <div class="content-layout">
    <!-- Mobile Menu Toggle -->
    <div style="display: none; position: fixed; top: 16px; left: 16px; z-index: 1001; background: white; border-radius: 8px; border: 1px solid var(--border); padding: 8px; cursor: pointer" @click="sidebarOpen = !sidebarOpen" class="mobile-menu-toggle">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <line x1="3" y1="6" x2="21" y2="6"></line>
        <line x1="3" y1="12" x2="21" y2="12"></line>
        <line x1="3" y1="18" x2="21" y2="18"></line>
      </svg>
    </div>

    <!-- Sidebar -->
    <div :class="['sidebar', { active: sidebarOpen }]">
      <div style="display: flex; justify-content: space-between; align-items: center">
        <div class="sidebar-logo">
          <div class="sidebar-logo-text">Glow Suite</div>
          <div class="sidebar-logo-sub">Beauty Management</div>
        </div>
        <button style="display: none; background: none; border: none; cursor: pointer; font-size: 24px" @click="sidebarOpen = false" class="mobile-close-btn">✕</button>
      </div>
      <nav class="sidebar-nav">
        <div class="nav-section">Appointment & Services</div>
        <div
          :class="['nav-item', { active: currentView === 'dashboard' }]"
          @click="currentView = 'dashboard'; sidebarOpen = false"
        >
          <span class="nav-icon">📊</span> Dashboard
        </div>
        <div
          :class="['nav-item', { active: currentView === 'bookings' }]"
          @click="currentView = 'bookings'; sidebarOpen = false"
        >
          <span class="nav-icon">📅</span> Appointments
        </div>
        <div
          :class="['nav-item', { active: currentView === 'services' }]"
          @click="currentView = 'services'; sidebarOpen = false"
        >
          <span class="nav-icon">💇</span> Services
        </div>

        <div class="nav-section">Management</div>
        <div
          :class="['nav-item', { active: currentView === 'customers' }]"
          @click="currentView = 'customers'; sidebarOpen = false"
        >
          <span class="nav-icon">👥</span> Customers
        </div>
        <div
          :class="['nav-item', { active: currentView === 'staff-by-day' }]"
          @click="currentView = 'staff-by-day'; sidebarOpen = false"
        >
          <span class="nav-icon">📅</span> Staff by Day
        </div>
        <div
          :class="['nav-item', { active: currentView === 'staff' }]"
          @click="currentView = 'staff'; sidebarOpen = false"
        >
          <span class="nav-icon">👔</span> Staff
        </div>
        <div
          :class="['nav-item', { active: currentView === 'rewards' }]"
          @click="currentView = 'rewards'; sidebarOpen = false"
        >
          <span class="nav-icon">🎁</span> Rewards
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
        <div class="sidebar-user" @click="showProfileMenu = !showProfileMenu" style="cursor: pointer; position: relative">
          <div class="sidebar-avatar">{{ user.name?.[0] || user.userId?.[0] }}</div>
          <div style="flex: 1">
            <div class="sidebar-username">{{ user.name || user.userId }}</div>
            <div class="sidebar-role">{{ user.role }}</div>
          </div>
          <div style="font-size: 18px">▼</div>
          
          <!-- Profile Dropdown Menu -->
          <div v-if="showProfileMenu" class="profile-dropdown" @click.stop style="position: absolute; bottom: 100%; left: 0; width: 220px; background: white; border: 1px solid var(--border-color); border-radius: 8px; box-shadow: 0 -2px 8px rgba(0,0,0,0.1); margin-bottom: 8px; z-index: 1000">
            <button class="profile-menu-item" @click="openProfileEdit(); showProfileMenu = false" style="width: 100%; padding: 12px 16px; text-align: left; border: none; background: none; cursor: pointer; font-size: 14px; color: var(--charcoal); transition: background-color 0.2s; border-bottom: 1px solid var(--border-color)">
              👤 Profile Edit
            </button>
            <button class="profile-menu-item" @click="showChangePasswordModal = true; showProfileMenu = false" style="width: 100%; padding: 12px 16px; text-align: left; border: none; background: none; cursor: pointer; font-size: 14px; color: var(--charcoal); transition: background-color 0.2s; border-bottom: 1px solid var(--border-color)">
              🔑 Change Password
            </button>
            <button class="profile-menu-item" @click="handleLogout" style="width: 100%; padding: 12px 16px; text-align: left; border: none; background: none; cursor: pointer; font-size: 14px; color: #e74c3c; transition: background-color 0.2s">
              🚪 Logout
            </button>
          </div>
        </div>
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
                    <div class="custom-dropdown" @click.stop>
                      <div 
                        class="custom-dropdown-input"
                        @click="showBookingCustomerDropdown = !showBookingCustomerDropdown"
                        :style="{ borderColor: showBookingCustomerDropdown ? 'var(--gold)' : 'var(--border)' }"
                      >
                        <input 
                          id="booking-customer"
                          v-model="bookingCustomerSearch" 
                          type="text" 
                          placeholder="Type to search customers..."
                          class="dropdown-search-input"
                          @focus="showBookingCustomerDropdown = true"
                          @input="showBookingCustomerDropdown = true"
                        />
                        <span class="dropdown-arrow">▼</span>
                      </div>
                      <div v-if="showBookingCustomerDropdown" class="custom-dropdown-menu">
                        <div 
                          v-if="filteredBookingCustomers.length === 0" 
                          class="dropdown-no-results"
                        >
                          No customers found
                        </div>
                        <div 
                          v-for="customer in filteredBookingCustomers" 
                          :key="customer.id"
                          class="dropdown-option"
                          @click="selectBookingCustomer(customer)"
                          :class="{ selected: bookingForm.customerId === String(customer.id) }"
                        >
                          <div style="font-weight: 500">{{ customer.name }}</div>
                          <div class="text-muted" style="font-size: 12px">{{ customer.email }}</div>
                        </div>
                      </div>
                    </div>
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
                    <label for="booking-date">Date * <span style="font-size: 12px; color: var(--text-muted); font-weight: 400">({{ bookingDateInfo }})</span></label>
                    <input 
                      id="booking-date"
                      v-model="bookingForm.date"
                      type="date"
                      class="form-input"
                      :min="minBookingDate"
                      :max="maxBookingDate"
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
                  {{ editingServiceId ? 'Save Changes' : 'Add Service' }}
                </button>
                <button v-if="editingServiceId" type="button" class="btn btn-outline" style="margin-top: 16px; margin-left: 8px" @click="cancelEditService">
                  ✕ Cancel
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
              <div style="margin-bottom: 16px; display: flex; gap: 12px; align-items: flex-end">
                <div style="flex: 1; max-width: 300px">
                  <label for="service-name-filter" style="display: block; font-size: 12px; color: var(--text-muted); margin-bottom: 4px">Service Name</label>
                  <input 
                    id="service-name-filter"
                    v-model="serviceName"
                    type="text" 
                    placeholder="🔍 Filter by service name..." 
                    class="form-input"
                    style="width: 100%"
                  />
                </div>
                <div style="flex: 1; max-width: 300px">
                  <label for="service-category-filter" style="display: block; font-size: 12px; color: var(--text-muted); margin-bottom: 4px">Category</label>
                  <select 
                    id="service-category-filter"
                    v-model="serviceCategoryFilter"
                    class="form-input"
                    style="width: 100%"
                  >
                    <option value="">All Categories</option>
                    <option v-for="cat in data.serviceCategories" :key="cat.id" :value="cat.id">
                      {{ cat.name }}
                    </option>
                  </select>
                </div>
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
              <h3 class="card-title">{{ isEditingCustomer ? '✎ Edit Customer' : '➕ Add New Customer' }}</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="isEditingCustomer ? handleUpdateCustomer() : handleAddCustomer()" style="max-width: 800px">
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

                  <div class="form-group">
                    <label for="customer-type">Customer Type</label>
                    <select 
                      id="customer-type"
                      v-model="customerForm.customerType"
                      class="form-input"
                    >
                      <option value="Normal">Normal</option>
                      <option value="VIP">VIP</option>
                    </select>
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

                <div style="display: flex; gap: 12px; margin-top: 16px">
                  <button type="submit" class="btn btn-primary">
                    {{ isEditingCustomer ? 'Update Customer' : 'Add Customer' }}
                  </button>
                  <button v-if="isEditingCustomer" type="button" class="btn btn-outline" @click="cancelEditCustomer">
                    Cancel
                  </button>
                </div>
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
                      <th>Customer Type</th>
                      <th>Total Spent</th>
                      <th>Points Balance</th>
                      <th>Preferences</th>
                      <th>No. of Visits</th>
                      <th>Invoices</th>
                      <th>Address</th>
                      <th>Registered</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="customer in filteredCustomers" :key="customer.id" @click="viewCustomerVisits(customer)" style="cursor: pointer; transition: background-color 0.2s" @mouseenter="$event.target.parentElement.style.backgroundColor = 'var(--light-bg)'" @mouseleave="$event.target.parentElement.style.backgroundColor = 'transparent'">
                      <td>{{ customer.name }}</td>
                      <td>{{ customer.email }}</td>
                      <td>{{ customer.phone }}</td>
                      <td><span class="badge" :style="{ background: customer.customerType === 'VIP' ? '#FFD700' : '#95a5a6', color: customer.customerType === 'VIP' ? '#000' : '#fff', padding: '4px 8px', borderRadius: '12px', fontSize: '11px', fontWeight: '600' }">{{ customer.customerType || 'Normal' }}</span></td>
                      <td style="text-align: center; font-weight: 600; color: var(--success)">₹{{ customer.totalSpent || 0 }}</td>
                      <td style="text-align: center; font-weight: 600; color: var(--primary)">{{ Math.round(customer.pointsBalance || 0) }}</td>
                      <td style="font-size: 12px; color: #666">{{ customer.preferences || '-' }}</td>
                      <td style="text-align: center; font-weight: 600">{{ customer.noOfVisits || 0 }}</td>
                      <td style="text-align: center"><span class="badge" style="background: var(--gold); color: white">{{ customer.invoices || 0 }}</span></td>
                      <td class="text-muted">{{ customer.address || "N/A" }}</td>
                      <td>{{ customer.registrationDate }}</td>
                      <td>
                        <div style="display: flex; gap: 6px">
                          <button class="btn btn-sm btn-outline" @click.stop="handleEditCustomer(customer)" style="padding: 4px 8px; font-size: 12px">
                            ✎ Edit
                          </button>
                          <button class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 12px; color: #e74c3c; border-color: #e74c3c" @click.stop="handleDeleteCustomer(customer.id)">
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
                    <tr v-for="staff in filteredStaff" :key="staff.id" @click="viewStaffBookings(staff)" style="cursor: pointer; transition: background-color 0.2s" @mouseenter="$event.target.parentElement.style.backgroundColor = 'var(--light-bg)'" @mouseleave="$event.target.parentElement.style.backgroundColor = 'transparent'">
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
                          <button class="btn btn-sm btn-outline" @click.stop="handleEditStaff(staff)" style="padding: 4px 8px; font-size: 12px">
                            ✎ Edit
                          </button>
                          <button class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 12px; color: #e74c3c; border-color: #e74c3c" @click.stop="handleDeleteStaff(staff.id)">
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
          <!-- Order Tabs -->
          <div style="display: flex; gap: 12px; margin-bottom: 20px; border-bottom: 2px solid var(--border); padding-bottom: 12px">
            <button 
              @click="orderTab = 'pending-orders'"
              :style="{ background: orderTab === 'pending-orders' ? 'var(--gold)' : 'transparent', color: orderTab === 'pending-orders' ? 'white' : 'var(--text)', borderBottom: 'none', padding: '8px 16px', borderRadius: 'var(--radius)', cursor: 'pointer', border: 'none', fontSize: '14px', fontWeight: '500' }"
            >
              📋 Pending Invoices
            </button>
            <button 
              @click="orderTab = 'replenishment'"
              :style="{ background: orderTab === 'replenishment' ? 'var(--gold)' : 'transparent', color: orderTab === 'replenishment' ? 'white' : 'var(--text)', borderBottom: 'none', padding: '8px 16px', borderRadius: 'var(--radius)', cursor: 'pointer', border: 'none', fontSize: '14px', fontWeight: '500' }"
            >
              🔄 Replenishment Requests
            </button>
          </div>

          <!-- PENDING INVOICES TAB -->
          <div v-if="orderTab === 'pending-orders'" class="card">
            <div class="card-header">
              <h3 class="card-title">📋 Pending Invoices</h3>
            </div>
            <div class="card-body">
              <!-- Completed Appointments Awaiting Invoice -->
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

          <!-- REPLENISHMENT REQUESTS TAB -->
          <div v-if="orderTab === 'replenishment'" class="card">
            <div class="card-header">
              <h3 class="card-title">🔄 Inventory Replenishment</h3>
            </div>
            <div class="card-body">
              <!-- Incoming Staff Requests -->
              <div style="margin-bottom: 24px">
                <h4 style="margin-bottom: 16px; font-weight: 600">📥 Incoming Staff Replenishment Requests</h4>
                <div v-if="managerReplenishmentRequests.length === 0" class="empty-state">
                  <div class="empty-state-icon">📥</div>
                  <div class="empty-state-text">No incoming staff requests</div>
                </div>
                <div v-else class="table-wrap">
                  <table>
                    <thead>
                      <tr>
                        <th>From Staff</th>
                        <th>Product</th>
                        <th>Quantity</th>
                        <th>Reason</th>
                        <th>Date</th>
                        <th>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="req in managerReplenishmentRequests" :key="req.id">
                        <td>{{ req.staffName }}</td>
                        <td>{{ getProductNameForOrder(req.productId) }}</td>
                        <td>{{ req.quantity }}</td>
                        <td>{{ req.reason }}</td>
                        <td>{{ req.date }}</td>
                        <td style="display: flex; gap: 4px; flex-wrap: wrap; align-items: center;">
                          <button @click="handleAcceptReplenishment(req)" class="btn btn-sm" style="background: var(--success); color: white; padding: 4px 8px; font-size: 12px; border: none; cursor: pointer; border-radius: var(--radius); white-space: nowrap;">✓ Accept</button>
                          <button @click="handleApproveReplenishment(req)" class="btn btn-sm" style="background: #2196F3; color: white; padding: 4px 8px; font-size: 12px; border: none; cursor: pointer; border-radius: var(--radius); white-space: nowrap; font-weight: 500;">✓ Approve</button>
                          <button @click="handleRejectReplenishment(req)" class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 12px; color: #e74c3c; border: 1px solid #e74c3c; border-radius: var(--radius); white-space: nowrap; background: none; cursor: pointer;">✕ Reject</button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- Add Replenishment Form -->
              <form @submit.prevent="handleAddReplenishment" style="max-width: 600px; margin-bottom: 24px; padding: 16px; background: var(--light-bg); border-radius: var(--radius)">
                <h4 style="margin-bottom: 16px; font-weight: 600">➕ Add Stock Replenishment</h4>
                <div class="form-group">
                  <label for="replen-product">Product Name *</label>
                  <select v-model="replenishmentForm.productId" id="replen-product" class="form-input" required>
                    <option value="">Select a product</option>
                    <option v-for="product in data.products" :key="product.id" :value="product.id">
                      {{ product.name }} (Current Stock: {{ product.currentStock }})
                    </option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="replen-qty">Quantity to Order *</label>
                  <input v-model.number="replenishmentForm.quantity" id="replen-qty" type="number" class="form-input" placeholder="Enter quantity" required min="1" />
                </div>
                <div class="form-group">
                  <label for="replen-reason">Reason for Order *</label>
                  <textarea v-model="replenishmentForm.reason" id="replen-reason" class="form-input" placeholder="e.g., Low stock alert, High demand period..." required rows="2"></textarea>
                </div>
                <div class="form-group">
                  <label for="replen-supplier">Supplier (Optional)</label>
                  <input v-model="replenishmentForm.supplier" id="replen-supplier" type="text" class="form-input" placeholder="Supplier name" />
                </div>
                <div v-if="replenishmentError" class="error-message" style="margin-bottom: 12px">{{ replenishmentError }}</div>
                <button type="submit" class="btn btn-primary" style="width: 100%">+ Add to Order List</button>
              </form>

              <!-- Pending Orders List -->
              <div>
                <h4 style="margin-bottom: 16px; font-weight: 600">📋 Items Pending Order ({{ pendingReplenishmentList.length }})</h4>
                <div v-if="pendingReplenishmentList.length === 0" class="empty-state">
                  <div class="empty-state-icon">🔄</div>
                  <div class="empty-state-text">No items pending order</div>
                </div>
                <div v-else class="table-wrap">
                  <table>
                    <thead>
                      <tr>
                        <th>Product</th>
                        <th>Quantity</th>
                        <th>Current Stock</th>
                        <th>Reason</th>
                        <th>Supplier</th>
                        <th>Source</th>
                        <th>Added Date</th>
                        <th>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="item in pendingReplenishmentList" :key="item.id">
                        <td><strong>{{ getProductNameForOrder(item.productId) }}</strong></td>
                        <td>{{ item.quantity }}</td>
                        <td style="color: item.currentStock < 5 ? '#e74c3c' : '#27ae60'">{{ item.currentStock }}</td>
                        <td>{{ item.reason }}</td>
                        <td>{{ item.supplier || '-' }}</td>
                        <td><span class="badge" :style="{ background: item.supplier?.includes('Staff') ? '#3498db' : '#95a5a6', color: 'white', padding: '2px 6px', borderRadius: '4px', fontSize: '11px' }">{{ item.supplier?.includes('Staff') ? 'Staff Order' : 'Manual' }}</span></td>
                        <td>{{ item.date }}</td>
                        <td>
                          <button @click="handleRemoveFromList(item.id)" class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 12px; color: #e74c3c; border-color: #e74c3c">Remove</button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- Place Order Button -->
              <div v-if="pendingReplenishmentList.length > 0" style="margin-top: 24px; padding-top: 24px; border-top: 2px solid var(--border); display: flex; gap: 12px">
                <button @click="handlePlaceReplenishmentOrder" class="btn btn-primary" style="padding: 12px 24px; font-size: 14px">
                  📤 Place Order ({{ pendingReplenishmentList.length }} items)
                </button>
                <span style="color: var(--text-muted); font-size: 13px; margin-top: 12px">Ready to order {{ pendingReplenishmentList.length }} item(s)</span>
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
                          <button class="btn btn-sm btn-outline" @click="viewInvoice(appt)" style="padding: 4px 8px; font-size: 12px">
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

        <!-- REWARDS VIEW -->
        <div v-if="currentView === 'rewards'" class="fade-in">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">🎁 Reward Points Configuration</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleUpdateRewards" style="max-width: 800px">
                <div class="grid-2">
                  <div class="form-group">
                    <label for="points-per-rupee">Points per Rupee Spent</label>
                    <input 
                      id="points-per-rupee"
                      v-model.number="rewardsForm.pointsPerRupee"
                      type="number"
                      step="0.1"
                      min="0"
                      placeholder="e.g., 0.1"
                      class="form-input"
                      required
                    />
                    <small class="text-muted">Points earned per rupee spent (e.g., 0.1 = 10 points for ₹100)</small>
                  </div>

                  <div class="form-group">
                    <label for="points-for-redemption">Points Required for Redemption</label>
                    <input 
                      id="points-for-redemption"
                      v-model.number="rewardsForm.pointsForRedemption"
                      type="number"
                      min="1"
                      placeholder="e.g., 500"
                      class="form-input"
                      required
                    />
                    <small class="text-muted">Points needed to redeem discount</small>
                  </div>

                  <div class="form-group">
                    <label for="redemption-value">Redemption Value (₹)</label>
                    <input 
                      id="redemption-value"
                      v-model.number="rewardsForm.redemptionValue"
                      type="number"
                      min="1"
                      placeholder="e.g., 25"
                      class="form-input"
                      required
                    />
                    <small class="text-muted">Rupees discount for redemption points</small>
                  </div>

                  <div class="form-group">
                    <label for="vip-threshold">VIP Threshold (₹ spent)</label>
                    <input 
                      id="vip-threshold"
                      v-model.number="rewardsForm.vipThreshold"
                      type="number"
                      min="1"
                      placeholder="e.g., 5000"
                      class="form-input"
                      required
                    />
                    <small class="text-muted">Total spending to become VIP customer</small>
                  </div>

                  <div class="form-group">
                    <label for="first-visit-points">First Visit Bonus Points</label>
                    <input 
                      id="first-visit-points"
                      v-model.number="rewardsForm.firstVisitPoints"
                      type="number"
                      min="0"
                      placeholder="e.g., 20"
                      class="form-input"
                      required
                    />
                    <small class="text-muted">Bonus points for first-time customers</small>
                  </div>

                  <div class="form-group">
                    <label for="birthday-points">Birthday Bonus Points</label>
                    <input 
                      id="birthday-points"
                      v-model.number="rewardsForm.birthdayPoints"
                      type="number"
                      min="0"
                      placeholder="e.g., 50"
                      class="form-input"
                      required
                    />
                    <small class="text-muted">Bonus points on customer's birthday</small>
                  </div>

                  <div class="form-group">
                    <label for="vip-discount">VIP Discount (%)</label>
                    <input 
                      id="vip-discount"
                      v-model.number="rewardsForm.vipDiscount"
                      type="number"
                      min="0"
                      max="100"
                      step="0.1"
                      placeholder="e.g., 15"
                      class="form-input"
                      required
                    />
                    <small class="text-muted">Percentage discount for VIP customers</small>
                  </div>

                  <div class="form-group">
                    <label for="points-expiry">Points Expiry (Months)</label>
                    <input 
                      id="points-expiry"
                      v-model.number="rewardsForm.pointsExpiryMonths"
                      type="number"
                      min="1"
                      placeholder="e.g., 6"
                      class="form-input"
                      required
                    />
                    <small class="text-muted">Months until points expire</small>
                  </div>
                </div>

                <div v-if="rewardsError" class="error-message">{{ rewardsError }}</div>
                <div v-if="rewardsSuccess" class="success-message">{{ rewardsSuccess }}</div>

                <button type="submit" class="btn btn-primary" style="margin-top: 16px">
                  💾 Save Reward Settings
                </button>
              </form>

              <!-- Current Reward Summary -->
              <div class="card" style="margin-top: 24px">
                <div class="card-header">
                  <h4 class="card-title">📊 Current Reward Summary</h4>
                </div>
                <div class="card-body">
                  <div class="grid-2">
                    <div class="stat-item">
                      <div class="stat-label">Points Earning Rate</div>
                      <div class="stat-value">{{ rewardsForm.pointsPerRupee * 100 }} pts per ₹100</div>
                    </div>
                    <div class="stat-item">
                      <div class="stat-label">Redemption Rate</div>
                      <div class="stat-value">{{ rewardsForm.pointsForRedemption }} pts = ₹{{ rewardsForm.redemptionValue }}</div>
                    </div>
                    <div class="stat-item">
                      <div class="stat-label">VIP Threshold</div>
                      <div class="stat-value">₹{{ rewardsForm.vipThreshold }} spent</div>
                    </div>
                    <div class="stat-item">
                      <div class="stat-label">VIP Benefits</div>
                      <div class="stat-value">{{ rewardsForm.vipDiscount }}% discount</div>
                    </div>
                    <div class="stat-item">
                      <div class="stat-label">Bonus Points</div>
                      <div class="stat-value">First visit: {{ rewardsForm.firstVisitPoints }} pts</div>
                    </div>
                    <div class="stat-item">
                      <div class="stat-label">Points Expiry</div>
                      <div class="stat-value">{{ rewardsForm.pointsExpiryMonths }} months</div>
                    </div>
                  </div>
                </div>
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

  <!-- Profile Edit Modal -->
  <div v-if="showProfileEditModal" class="modal-overlay" @click="showProfileEditModal = false">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3 class="modal-title">👤 Edit Profile</h3>
        <button class="modal-close" @click="showProfileEditModal = false">✕</button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="handleUpdateProfile">
          <div class="form-group">
            <label for="profile-name">Full Name</label>
            <input 
              id="profile-name"
              v-model="profileEditForm.name" 
              type="text" 
              placeholder="Enter full name"
              class="form-input"
              required
            />
          </div>
          <div class="form-group">
            <label for="profile-email">Email</label>
            <input 
              id="profile-email"
              v-model="profileEditForm.email" 
              type="email" 
              placeholder="Enter email address"
              class="form-input"
            />
          </div>
          <div class="form-group">
            <label for="profile-phone">Phone</label>
            <input 
              id="profile-phone"
              v-model="profileEditForm.phone" 
              type="tel" 
              placeholder="Enter phone number"
              class="form-input"
            />
          </div>
          <div class="form-group">
            <label for="profile-address">Address</label>
            <textarea 
              id="profile-address"
              v-model="profileEditForm.address" 
              placeholder="Enter address"
              class="form-input"
              rows="3"
            ></textarea>
          </div>
          <div style="display: flex; gap: 12px; margin-top: 20px">
            <button type="button" class="btn btn-outline" @click="showProfileEditModal = false" style="flex: 1">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" style="flex: 1">
              Save Changes
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

  <!-- AI Assistant Button -->
  <button 
    class="ai-assistant-btn" 
    @click="showAIAssistant = !showAIAssistant"
    title="AI Assistant"
  >
    🤖
  </button>

  <!-- Staff Bookings Modal -->
  <div v-if="showStaffBookingsModal && selectedStaffForBookings" class="modal-overlay" @click="showStaffBookingsModal = false">
    <div class="modal-content" @click.stop style="max-width: 700px">
      <div class="modal-header">
        <h3 class="modal-title">📅 {{ selectedStaffForBookings.name }} - Past Bookings</h3>
        <button class="modal-close" @click="showStaffBookingsModal = false">✕</button>
      </div>
      <div class="modal-body">
        <div v-if="staffBookings.length === 0" class="empty-state" style="padding: 32px; text-align: center">
          <div style="font-size: 24px; margin-bottom: 12px">📭</div>
          <div style="color: var(--text-muted)">No past bookings found</div>
        </div>
        <div v-else class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Customer</th>
                <th>Service</th>
                <th>Date</th>
                <th>Status</th>
                <th>Amount</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="booking in staffBookings" :key="booking.id">
                <td>{{ getCustomerName(booking.customerId) }}</td>
                <td>{{ getServiceName(booking.serviceId) }}</td>
                <td>{{ booking.date }}</td>
                <td><span :class="['badge', apptStatusBadge(booking.status)]">{{ booking.status }}</span></td>
                <td>₹{{ getServicePrice(booking.serviceId) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- Customer Visits Modal -->
  <div v-if="showCustomerVisitsModal && selectedCustomerForVisits" class="modal-overlay" @click="showCustomerVisitsModal = false">
    <div class="modal-content" @click.stop style="max-width: 700px">
      <div class="modal-header">
        <h3 class="modal-title">👤 {{ selectedCustomerForVisits.name }} - Past Visits</h3>
        <button class="modal-close" @click="showCustomerVisitsModal = false">✕</button>
      </div>
      <div class="modal-body">
        <div v-if="customerVisits.length === 0" class="empty-state" style="padding: 32px; text-align: center">
          <div style="font-size: 24px; margin-bottom: 12px">📭</div>
          <div style="color: var(--text-muted)">No past visits found</div>
        </div>
        <div v-else class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Service</th>
                <th>Date</th>
                <th>Staff</th>
                <th>Status</th>
                <th>Amount</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="visit in customerVisits" :key="visit.id">
                <td>{{ getServiceName(visit.serviceId) }}</td>
                <td>{{ visit.date }}</td>
                <td>{{ getStaffName(visit.staffId) }}</td>
                <td><span :class="['badge', apptStatusBadge(visit.status)]">{{ visit.status }}</span></td>
                <td>₹{{ getServicePrice(visit.serviceId) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- Invoice Details Modal -->
  <div v-if="showInvoiceModal && selectedInvoice" class="modal-overlay" @click="showInvoiceModal = false">
    <div class="modal-content" @click.stop style="max-width: 600px">
      <div class="modal-header">
        <h3 class="modal-title">📄 Invoice Details</h3>
        <button class="modal-close" @click="showInvoiceModal = false">✕</button>
      </div>
      <div class="modal-body">
        <div style="background: var(--light-bg); padding: 20px; border-radius: 8px; margin-bottom: 20px">
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px">
            <div style="border-right: 1px solid var(--border-color)">
              <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 4px">Invoice ID</div>
              <div style="font-size: 18px; font-weight: 600; color: var(--charcoal)">#INV{{ String(1000 + (data.appointments.findIndex(a => a.id === selectedInvoice.id))).slice(-4) }}</div>
            </div>
            <div>
              <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 4px">Invoice Date</div>
              <div style="font-size: 18px; font-weight: 600; color: var(--charcoal)">{{ selectedInvoice.date }}</div>
            </div>
          </div>
        </div>

        <div style="margin-bottom: 24px">
          <h4 style="font-size: 14px; font-weight: 600; color: var(--charcoal); margin-bottom: 12px">Customer Details</h4>
          <div style="display: grid; gap: 8px">
            <div style="display: grid; grid-template-columns: 140px 1fr">
              <span style="color: var(--text-muted)">Name:</span>
              <span style="font-weight: 500">{{ getCustomerName(selectedInvoice.customerId) }}</span>
            </div>
            <div style="display: grid; grid-template-columns: 140px 1fr">
              <span style="color: var(--text-muted)">Email:</span>
              <span style="font-weight: 500">{{ data.customers.find(c => c.id === selectedInvoice.customerId)?.email || '-' }}</span>
            </div>
            <div style="display: grid; grid-template-columns: 140px 1fr">
              <span style="color: var(--text-muted)">Phone:</span>
              <span style="font-weight: 500">{{ data.customers.find(c => c.id === selectedInvoice.customerId)?.phone || '-' }}</span>
            </div>
          </div>
        </div>

        <div style="margin-bottom: 24px">
          <h4 style="font-size: 14px; font-weight: 600; color: var(--charcoal); margin-bottom: 12px">Service Details</h4>
          <div style="display: grid; gap: 8px">
            <div style="display: grid; grid-template-columns: 140px 1fr">
              <span style="color: var(--text-muted)">Service:</span>
              <span style="font-weight: 500">{{ getServiceName(selectedInvoice.serviceId) }}</span>
            </div>
            <div style="display: grid; grid-template-columns: 140px 1fr">
              <span style="color: var(--text-muted)">Service Amount:</span>
              <span style="font-weight: 500">₹{{ getServicePrice(selectedInvoice.serviceId) }}</span>
            </div>
            <div style="display: grid; grid-template-columns: 140px 1fr">
              <span style="color: var(--text-muted)">Staff:</span>
              <span style="font-weight: 500">{{ getStaffName(selectedInvoice.staffId) }}</span>
            </div>
          </div>
        </div>

        <div style="border-top: 2px solid var(--border-color); padding-top: 16px; margin-bottom: 20px">
          <div style="display: grid; grid-template-columns: 140px 1fr; gap: 12px; margin-bottom: 8px">
            <span style="color: var(--text-muted)">Subtotal:</span>
            <span style="text-align: right; font-weight: 500">₹{{ getServicePrice(selectedInvoice.serviceId) }}</span>
          </div>
          <div style="display: grid; grid-template-columns: 140px 1fr; gap: 12px; font-size: 14px; margin-bottom: 8px">
            <span style="color: var(--text-muted)">Total Amount:</span>
            <span style="text-align: right; font-weight: 600; color: var(--gold); font-size: 16px">₹{{ getServicePrice(selectedInvoice.serviceId) }}</span>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 140px 1fr">
          <span style="color: var(--text-muted)">Payment Method:</span>
          <span style="font-weight: 500; text-transform: capitalize">{{ selectedInvoice.paymentType || 'Cash' }}</span>
        </div>
        <div style="display: grid; grid-template-columns: 140px 1fr; margin-top: 8px">
          <span style="color: var(--text-muted)">Status:</span>
          <span :class="['badge', selectedInvoice.invoiceStatus === 'invoiced' ? 'badge-green' : 'badge-gold']">{{ selectedInvoice.invoiceStatus }}</span>
        </div>

        <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--border-color); display: flex; gap: 8px">
          <button class="btn btn-primary" style="flex: 1" @click="handleSendInvoice(selectedInvoice)">
            📧 Send Email
          </button>
          <button class="btn btn-outline" style="flex: 1" @click="showInvoiceModal = false">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- AI Assistant Chat Modal -->
  <div v-if="showAIAssistant" class="ai-assistant-modal">
    <div class="ai-assistant-content">
      <div class="ai-assistant-header">
        <h3 class="ai-title">🤖 Manager Assistant</h3>
        <button class="ai-close-btn" @click="showAIAssistant = false">✕</button>
      </div>
      <div class="ai-assistant-chat">
        <div class="ai-chat-messages">
          <div v-for="(msg, idx) in aiMessages" :key="idx" :class="['ai-message', msg.type]">
            <div class="ai-message-content">{{ msg.text }}</div>
          </div>
        </div>
      </div>
      <div class="ai-assistant-input">
        <input 
          v-model="aiUserInput" 
          type="text" 
          placeholder="Ask me for help..."
          class="ai-input-field"
          @keyup.enter="sendAIMessage"
        />
        <button class="ai-send-btn" @click="sendAIMessage">Send</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { useAppStore } from "@/stores/appStore";

const router = useRouter();
const appStore = useAppStore();

const currentView = ref("dashboard");
const sidebarOpen = ref(false);
const selectedDate = ref(null);
const selectedStaffDate = ref(new Date().toISOString().split('T')[0]);
const hoveredStaff = ref(null);
const showChangePasswordModal = ref(false);
const showProfileMenu = ref(false);
const showProfileEditModal = ref(false);
const profileEditForm = ref({
  name: '',
  email: '',
  phone: '',
  address: ''
});
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

// AI Assistant state
const showAIAssistant = ref(false);
const aiMessages = ref([
  { type: 'assistant', text: 'Hi! I\'m your AI Assistant. I\'m here to help you manage appointments, customers, services, staff, packages, and resolve any issues. How can I assist you today?' }
]);
const aiUserInput = ref('');

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
  preferences: "",
  customerType: "Normal"
});
const isEditingCustomer = ref(false);
const editingCustomerId = ref(null);
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
const serviceCategoryFilter = ref("");
const customerName = ref("");
const staffName = ref("");
const productName = ref("");
const invoiceCustomerName = ref("");
const bookingCustomerName = ref("");
const orderFilter = ref("");
const completedAppointmentFilter = ref("");

// Customer search dropdown for appointment creation
const bookingCustomerSearch = ref("");
const showBookingCustomerDropdown = ref(false);

// Service editing state
const editingServiceId = ref(null);

// Staff bookings modal state
const showStaffBookingsModal = ref(false);
const selectedStaffForBookings = ref(null);

// Customer visits modal state
const showCustomerVisitsModal = ref(false);
const selectedCustomerForVisits = ref(null);

// Invoice modal state
const showInvoiceModal = ref(false);
const selectedInvoice = ref(null);

// Order Tab & Replenishment
const orderTab = ref("pending-orders");
const replenishmentForm = ref({
  productId: "",
  quantity: 1,
  reason: "",
  supplier: ""
});
const replenishmentError = ref("");
const pendingReplenishmentList = ref([
  { id: 1, productId: 2, quantity: 10, currentStock: 3, reason: "Low stock alert", supplier: "Beauty Supplies Ltd", date: "2026-03-20" },
  { id: 2, productId: 4, quantity: 5, currentStock: 2, reason: "High demand", supplier: "Health & Wellness Co", date: "2026-03-21" }
]);
const managerReplenishmentRequests = ref([
  { id: 1, staffName: "Alice Brown", productId: 2, quantity: 5, reason: "Low stock", date: "2026-03-22" },
  { id: 2, staffName: "Carol Smith", productId: 4, quantity: 3, reason: "High demand", date: "2026-03-21" }
]);
const staffReplenishmentRequests = ref([
  { id: 1, staffName: "Alice Brown", productId: 2, quantity: 5, reason: "Facial supplies", date: "2026-03-22", type: "replenishment" },
  { id: 2, staffName: "Carol Smith", productId: 4, quantity: 3, purpose: "Massage oils", date: "2026-03-21", type: "staff-order" }
]);

// Rewards form state
const rewardsForm = ref({
  pointsPerRupee: 0.1,
  pointsForRedemption: 500,
  redemptionValue: 25,
  vipThreshold: 5000,
  firstVisitPoints: 20,
  birthdayPoints: 50,
  vipDiscount: 15,
  pointsExpiryMonths: 6
});
const rewardsError = ref("");
const rewardsSuccess = ref("");

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

const staffBookings = computed(() => {
  if (!selectedStaffForBookings.value) return [];
  return data.value.appointments.filter(appt => appt.staffId === selectedStaffForBookings.value.id);
});

const customerVisits = computed(() => {
  if (!selectedCustomerForVisits.value) return [];
  return data.value.appointments.filter(appt => appt.customerId === selectedCustomerForVisits.value.id);
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

// Helper function to check if bridal package is selected
const hasBridalPackageSelected = () => {
  return bookingForm.value.serviceIds.some(serviceId => {
    const service = data.value.services.find(s => s.id === parseInt(serviceId));
    return service && service.name === "Bridal Package";
  });
};

// Compute minimum booking date based on service type
const minBookingDate = computed(() => {
  const today = new Date();
  const minDate = new Date(today);
  
  if (hasBridalPackageSelected()) {
    minDate.setMonth(minDate.getMonth() + 1); // 1 month for bridal package
  } else {
    minDate.setDate(minDate.getDate() + 1); // Tomorrow for normal services
  }
  
  return minDate.toISOString().split('T')[0];
});

// Compute maximum booking date (6 months for bridal, 2 days for others)
const maxBookingDate = computed(() => {
  const today = new Date();
  const maxDate = new Date(today);
  
  if (hasBridalPackageSelected()) {
    maxDate.setMonth(maxDate.getMonth() + 6); // 6 months for bridal package
  } else {
    maxDate.setDate(maxDate.getDate() + 2); // 2 days for other services
  }
  
  return maxDate.toISOString().split('T')[0];
});

// Helper text for booking date info
const bookingDateInfo = computed(() => {
  if (bookingForm.value.serviceIds.length === 0) {
    return "Select a service to see available booking dates";
  }
  
  if (hasBridalPackageSelected()) {
    return `Bridal Package: Book 1 to 6 months in advance`;
  } else {
    return `Other services: Book from tomorrow onwards for 2 days`;
  }
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
  return data.value.services.filter(s => {
    const nameMatch = !serviceName.value.trim() || s.name.toLowerCase().includes(serviceName.value.toLowerCase());
    const categoryMatch = !serviceCategoryFilter.value || s.categoryId == serviceCategoryFilter.value;
    return nameMatch && categoryMatch;
  });
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

// Filtered customers for booking creation form
const filteredBookingCustomers = computed(() => {
  if (!bookingCustomerSearch.value.trim()) return data.value.customers;
  return data.value.customers.filter(c => 
    c.name.toLowerCase().includes(bookingCustomerSearch.value.toLowerCase())
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

const handleLogout = () => {
  showProfileMenu.value = false;
  logout();
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

const openProfileEdit = () => {
  // Populate form with current user data
  profileEditForm.value.name = user.value?.name || '';
  profileEditForm.value.email = user.value?.email || '';
  profileEditForm.value.phone = user.value?.phone || '';
  profileEditForm.value.address = user.value?.address || '';
  showProfileEditModal.value = true;
};

const handleUpdateProfile = () => {
  // Update user profile
  if (profileEditForm.value.name.trim()) {
    appStore.user.name = profileEditForm.value.name;
  }
  
  // In a real application, send this data to the backend
  // For now, just show success message
  showProfileEditModal.value = false;
};

// Booking handlers
const selectBookingCustomer = (customer) => {
  bookingForm.value.customerId = String(customer.id);
  bookingCustomerSearch.value = customer.name;
  showBookingCustomerDropdown.value = false;
};

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

  // Validate booking date is within allowed range
  const selectedDate = new Date(bookingForm.value.date);
  const minDate = new Date(minBookingDate.value);
  const maxDate = new Date(maxBookingDate.value);

  if (selectedDate < minDate || selectedDate > maxDate) {
    if (hasBridalPackageSelected()) {
      bookingError.value = `Bridal Package must be booked 1 to 6 months in advance`;
    } else {
      bookingError.value = `Please select a date from tomorrow onwards for 2 days`;
    }
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

  if (editingServiceId.value) {
    // Update existing service
    const index = data.value.services.findIndex(s => s.id === editingServiceId.value);
    if (index > -1) {
      data.value.services[index] = {
        ...data.value.services[index],
        categoryId: parseInt(serviceForm.value.categoryId),
        name: serviceForm.value.name,
        price: serviceForm.value.price,
        duration: serviceForm.value.duration,
        description: `${serviceForm.value.name} service`,
        productsRequired: serviceForm.value.productsRequired || "None"
      };
      serviceSuccess.value = "Service updated successfully!";
    }
  } else {
    // Create new service
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
  }

  setTimeout(() => {
    serviceForm.value = {
      name: "",
      categoryId: "",
      price: 0,
      duration: 0,
      productsRequired: ""
    };
    editingServiceId.value = null;
    serviceSuccess.value = "";
  }, 1500);
};

const handleEditService = (service) => {
  editingServiceId.value = service.id;
  serviceForm.value = {
    name: service.name,
    categoryId: String(service.categoryId),
    price: service.price,
    duration: service.duration,
    productsRequired: service.productsRequired || ""
  };
};

const cancelEditService = () => {
  editingServiceId.value = null;
  serviceForm.value = {
    name: "",
    categoryId: "",
    price: 0,
    duration: 0,
    productsRequired: ""
  };
};

// Staff bookings handler
const viewStaffBookings = (staff) => {
  selectedStaffForBookings.value = staff;
  showStaffBookingsModal.value = true;
};

// Customer visits handler
const viewCustomerVisits = (customer) => {
  selectedCustomerForVisits.value = customer;
  showCustomerVisitsModal.value = true;
};

// Invoice view handler
const viewInvoice = (appointment) => {
  selectedInvoice.value = appointment;
  showInvoiceModal.value = true;
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
    customerType: customerForm.value.customerType || "Normal",
    totalSpent: 0,
    pointsBalance: data.value.rewards?.firstVisitPoints || 20,
    pointsEarned: data.value.rewards?.firstVisitPoints || 20,
    lastPointsUpdate: new Date().toISOString().split('T')[0],
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
      address: "",
      preferences: "",
      customerType: "Normal"
    };
    customerSuccess.value = "";
  }, 1500);
};

const cancelEditCustomer = () => {
  customerForm.value = {
    name: "",
    email: "",
    phone: "",
    dob: "",
    address: "",
    preferences: "",
    customerType: "Normal"
  };
  isEditingCustomer.value = false;
  editingCustomerId.value = null;
  customerError.value = "";
  customerSuccess.value = "";
};

const handleUpdateCustomer = () => {
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

  const customerIndex = data.value.customers.findIndex(c => c.id === editingCustomerId.value);
  if (customerIndex === -1) {
    customerError.value = "Customer not found";
    return;
  }

  data.value.customers[customerIndex] = {
    ...data.value.customers[customerIndex],
    name: customerForm.value.name,
    email: customerForm.value.email,
    phone: customerForm.value.phone,
    dob: customerForm.value.dob,
    address: customerForm.value.address || "",
    preferences: customerForm.value.preferences || "",
    customerType: customerForm.value.customerType || "Normal"
  };

  customerSuccess.value = "Customer updated successfully!";
  isEditingCustomer.value = false;
  editingCustomerId.value = null;

  setTimeout(() => {
    customerForm.value = {
      name: "",
      email: "",
      phone: "",
      dob: "",
      address: "",
      preferences: "",
      customerType: "Normal"
    };
    customerSuccess.value = "";
  }, 1500);
};

// Initialize rewards form with store data
const initializeRewardsForm = () => {
  if (data.value.rewards) {
    rewardsForm.value = { ...data.value.rewards };
  }
};

// Call initialization
initializeRewardsForm();

const handleUpdateRewards = () => {
  rewardsError.value = "";
  rewardsSuccess.value = "";

  // Validation
  if (rewardsForm.value.pointsPerRupee <= 0) {
    rewardsError.value = "Points per rupee must be greater than 0";
    return;
  }

  if (rewardsForm.value.pointsForRedemption <= 0) {
    rewardsError.value = "Points for redemption must be greater than 0";
    return;
  }

  if (rewardsForm.value.redemptionValue <= 0) {
    rewardsError.value = "Redemption value must be greater than 0";
    return;
  }

  if (rewardsForm.value.vipThreshold <= 0) {
    rewardsError.value = "VIP threshold must be greater than 0";
    return;
  }

  if (rewardsForm.value.pointsExpiryMonths <= 0) {
    rewardsError.value = "Points expiry must be greater than 0 months";
    return;
  }

  // Update the store
  data.value.rewards = { ...rewardsForm.value };

  rewardsSuccess.value = "Reward settings updated successfully!";

  setTimeout(() => {
    rewardsSuccess.value = "";
  }, 3000);
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

// AI Assistant handler
const sendAIMessage = () => {
  if (!aiUserInput.value.trim()) return;

  // Add user message
  aiMessages.value.push({ type: 'user', text: aiUserInput.value });

  const userMessage = aiUserInput.value.toLowerCase();
  aiUserInput.value = '';

  // Simulate AI responses based on keywords
  let assistantResponse = '';

  if (userMessage.includes('appointment') || userMessage.includes('booking')) {
    assistantResponse = 'I see you\'re asking about appointments. You can manage appointments in the "Appointments" section. You can create new appointments, edit existing ones, or view them by date. What would you like to do?';
  } else if (userMessage.includes('customer')) {
    assistantResponse = 'The Customers section shows all your clients, their contact information, preferences, visit history, and spending. You can add new customers, edit their details, or track customer loyalty there.';
  } else if (userMessage.includes('service')) {
    assistantResponse = 'You can create and manage services in the "Services" section. Add new services, set pricing, duration, products required, and manage all your service offerings there.';
  } else if (userMessage.includes('staff') || userMessage.includes('stylist')) {
    assistantResponse = 'You can view and manage your staff in the Staff Management section. Add new staff members, view their skills, attendance, appointments, and performance ratings.';
  } else if (userMessage.includes('package')) {
    assistantResponse = 'Service Packages allow you to bundle multiple services together in the "Service Packages" section. Create customized packages for special promotions or occasions.';
  } else if (userMessage.includes('inventory') || userMessage.includes('product') || userMessage.includes('stock')) {
    assistantResponse = 'The Inventory Management section lets you track products, stock levels, suppliers, and costs. You can see low stock alerts and manage orders from the Orders section.';
  } else if (userMessage.includes('invoice') || userMessage.includes('billing') || userMessage.includes('payment')) {
    assistantResponse = 'You can create and manage invoices in the Invoices section. Create invoices from completed appointments, track payment status, and send invoices to customers via email.';
  } else if (userMessage.includes('finance') || userMessage.includes('profit') || userMessage.includes('revenue')) {
    assistantResponse = 'The Finance section (password protected) shows your total revenue, product costs, staff salaries, overhead, and net profit. Access it from the sidebar for a complete financial overview.';
  } else if (userMessage.includes('issue') || userMessage.includes('problem') || userMessage.includes('error')) {
    assistantResponse = 'I\'m sorry you\'re experiencing an issue. Please describe the problem in detail, and I\'ll help you troubleshoot. Is it related to appointments, customers, services, staff, inventory, or invoices?';
  } else if (userMessage.includes('help')) {
    assistantResponse = 'I\'m here to help! I can assist you with:\n• Managing appointments & bookings\n• Customer information & preferences\n• Creating & managing services\n• Staff management & scheduling\n• Service packages\n• Inventory & product management\n• Invoices & billing\n• Finance & reports\n\nWhat would you like help with?';
  } else if (userMessage.includes('hello') || userMessage.includes('hi')) {
    assistantResponse = 'Hello! I\'m your AI Assistant for the Manager Dashboard. How can I help you today? Feel free to ask about appointments, customers, services, staff, packages, inventory, or any other concerns.';
  } else if (userMessage.includes('overview') || userMessage.includes('stats') || userMessage.includes('dashboard')) {
    assistantResponse = 'The Dashboard Overview shows you key metrics: Today\'s appointments, available staff, low stock items, and pending orders. This gives you a quick snapshot of your business for the day.';
  } else {
    assistantResponse = 'That\'s a great question! I can help with appointment management, customer details, service creation, staff management, packages, inventory, invoices, and financial reports. How would you like me to assist you?';
  }

  // Add assistant response after a small delay
  setTimeout(() => {
    aiMessages.value.push({ type: 'assistant', text: assistantResponse });
    
    // Auto-scroll to bottom
    setTimeout(() => {
      const chatBox = document.querySelector('.ai-chat-messages');
      if (chatBox) chatBox.scrollTop = chatBox.scrollHeight;
    }, 0);
  }, 500);
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
    preferences: customer.preferences || "",
    customerType: customer.customerType || "Normal"
  };
  isEditingCustomer.value = true;
  editingCustomerId.value = customer.id;
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

const handleApproveReplenishment = (req) => {
  const index = managerReplenishmentRequests.value.findIndex(r => r.id === req.id);
  if (index > -1) {
    const product = data.value.products.find(p => p.id === req.productId);
    // Add to pending replenishment list
    const newItem = {
      id: Math.max(...pendingReplenishmentList.value.map(r => r.id || 0), 0) + 1,
      productId: req.productId,
      quantity: req.quantity,
      currentStock: product?.currentStock || 0,
      reason: req.reason,
      supplier: "Staff Request",
      date: req.date
    };
    pendingReplenishmentList.value.push(newItem);
    // Remove from incoming requests
    managerReplenishmentRequests.value.splice(index, 1);
    alert(`✅ Request from ${req.staffName} approved and added to order list!`);
    console.log(`Approved replenishment request: ${req.staffName} - ${getProductNameForOrder(req.productId)}`);
  }
};

const handleAcceptReplenishment = (req) => {
  const index = managerReplenishmentRequests.value.findIndex(r => r.id === req.id);
  if (index > -1) {
    const product = data.value.products.find(p => p.id === req.productId);
    // Add to pending replenishment list
    const newItem = {
      id: Math.max(...pendingReplenishmentList.value.map(r => r.id || 0), 0) + 1,
      productId: req.productId,
      quantity: req.quantity,
      currentStock: product?.currentStock || 0,
      reason: req.reason,
      supplier: "Staff Request - Accepted",
      date: req.date
    };
    pendingReplenishmentList.value.push(newItem);
    // Remove from incoming requests
    managerReplenishmentRequests.value.splice(index, 1);
    alert(`✅ Request from ${req.staffName} accepted and added to order list!`);
    console.log(`Accepted replenishment request: ${req.staffName} - ${getProductNameForOrder(req.productId)}`);
  }
};

const handleRejectReplenishment = (req) => {
  if (confirm(`Reject replenishment request from ${req.staffName}?`)) {
    const index = managerReplenishmentRequests.value.findIndex(r => r.id === req.id);
    if (index > -1) {
      managerReplenishmentRequests.value.splice(index, 1);
      console.log(`❌ Rejected replenishment from ${req.staffName}`);
    }
  }
};

const handleApproveStaffOrder = (req) => {
  const index = staffReplenishmentRequests.value.findIndex(r => r.id === req.id);
  if (index > -1) {
    staffReplenishmentRequests.value.splice(index, 1);
    alert(`✅ Order from ${req.staffName} for ${getProductNameForOrder(req.productId)} (${req.quantity} units) has been approved!`);
    console.log(`Approved staff order: ${req.staffName} - ${getProductNameForOrder(req.productId)}`);
  }
};

const handleAcceptStaffOrder = (req) => {
  const index = staffReplenishmentRequests.value.findIndex(r => r.id === req.id);
  if (index > -1) {
    const product = data.value.products.find(p => p.id === req.productId);
    // Add to pending replenishment list
    const newItem = {
      id: Math.max(...pendingReplenishmentList.value.map(r => r.id || 0), 0) + 1,
      productId: req.productId,
      quantity: req.quantity,
      currentStock: product?.currentStock || 0,
      reason: req.reason || req.purpose || "Staff Order",
      supplier: "Staff Request - Accepted",
      date: req.date
    };
    pendingReplenishmentList.value.push(newItem);
    // Remove from staff orders list
    staffReplenishmentRequests.value.splice(index, 1);
    alert(`✅ Order from ${req.staffName} accepted and added to pending order list!`);
    console.log(`Accepted staff order: ${req.staffName} - ${getProductNameForOrder(req.productId)}`);
  }
};

const handleRejectStaffOrder = (req) => {
  const index = staffReplenishmentRequests.value.findIndex(r => r.id === req.id);
  if (index > -1) {
    staffReplenishmentRequests.value.splice(index, 1);
    alert(`✅ Order from ${req.staffName} has been rejected!`);
    console.log(`Rejected staff order: ${req.staffName}`);
  }
};

const handleAddReplenishment = () => {
  replenishmentError.value = "";

  if (!replenishmentForm.value.productId) {
    replenishmentError.value = "Please select a product";
    return;
  }

  if (replenishmentForm.value.quantity < 1) {
    replenishmentError.value = "Quantity must be at least 1";
    return;
  }

  if (!replenishmentForm.value.reason.trim()) {
    replenishmentError.value = "Please provide a reason for order";
    return;
  }

  const product = data.value.products.find(p => p.id === parseInt(replenishmentForm.value.productId));
  const newItem = {
    id: Math.max(...pendingReplenishmentList.value.map(r => r.id || 0), 0) + 1,
    productId: parseInt(replenishmentForm.value.productId),
    quantity: replenishmentForm.value.quantity,
    currentStock: product?.currentStock || 0,
    reason: replenishmentForm.value.reason,
    supplier: replenishmentForm.value.supplier || "TBD",
    date: new Date().toISOString().split('T')[0]
  };

  pendingReplenishmentList.value.push(newItem);
  
  // Reset form
  replenishmentForm.value = {
    productId: "",
    quantity: 1,
    reason: "",
    supplier: ""
  };
  
  console.log(`Added ${getProductNameForOrder(newItem.productId)} (${newItem.quantity} units) to order list`);
};

const handleRemoveFromList = (id) => {
  pendingReplenishmentList.value = pendingReplenishmentList.value.filter(item => item.id !== id);
  console.log(`Removed item from replenishment order list`);
};

const handlePlaceReplenishmentOrder = () => {
  if (pendingReplenishmentList.value.length === 0) {
    alert("No items to order");
    return;
  }

  const totalQty = pendingReplenishmentList.value.reduce((sum, item) => sum + item.quantity, 0);
  const summary = `Order Placed Successfully!\n================================\nTotal Items: ${pendingReplenishmentList.value.length}\nTotal Quantity: ${totalQty} units\n\nOrder Status: Awaiting Delivery\nDate: ${new Date().toISOString().split('T')[0]}`;

  alert(summary);
  
  // Clear the list after placing order
  pendingReplenishmentList.value = [];
  console.log(`Replenishment order placed for ${totalQty} units`);
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

// Close customer dropdown when clicking outside
const handleClickOutside = (event) => {
  const dropdown = document.querySelector('.custom-dropdown');
  if (dropdown && !dropdown.contains(event.target)) {
    showBookingCustomerDropdown.value = false;
  }
  
  const profileSection = document.querySelector('.sidebar-user');
  if (profileSection && !profileSection.contains(event.target)) {
    showProfileMenu.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
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

/* Custom Dropdown Styles */
.custom-dropdown {
  position: relative;
}

.custom-dropdown-input {
  display: flex;
  align-items: center;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: white;
  cursor: text;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.custom-dropdown-input:hover {
  border-color: var(--gold);
}

.dropdown-search-input {
  flex: 1;
  border: none;
  padding: 10px 12px;
  font-size: 13px;
  font-family: inherit;
  outline: none;
  background: transparent;
}

.dropdown-arrow {
  padding: 0 12px;
  color: var(--text-muted);
  font-size: 11px;
  user-select: none;
  pointer-events: none;
}

.custom-dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid var(--border);
  border-top: none;
  border-radius: 0 0 var(--radius-sm) var(--radius-sm);
  max-height: 250px;
  overflow-y: auto;
  z-index: 10;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
}

.dropdown-option {
  padding: 12px 12px;
  cursor: pointer;
  border-bottom: 1px solid var(--light-bg);
  transition: background-color 0.2s;
}

.dropdown-option:hover {
  background-color: var(--light-bg);
}

.dropdown-option.selected {
  background-color: rgba(229, 170, 84, 0.15);
  border-left: 3px solid var(--gold);
  padding-left: 9px;
}

.dropdown-no-results {
  padding: 12px;
  text-align: center;
  color: var(--text-muted);
  font-size: 13px;
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

/* AI Assistant Styles */
.ai-assistant-btn {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--gold), #d4a574);
  border: none;
  color: white;
  font-size: 28px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
  transition: all 0.3s ease;
  z-index: 999;
  display: flex !important;
  align-items: center;
  justify-content: center;
  visibility: visible !important;
  opacity: 1 !important;
  pointer-events: auto !important;
}

.ai-assistant-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(212, 175, 55, 0.4);
}

.ai-assistant-btn:active {
  transform: scale(0.95);
}

.dashboard-container > .ai-assistant-btn {
  visibility: visible !important;
  opacity: 1 !important;
}

.ai-assistant-modal {
  position: fixed;
  bottom: 100px;
  right: 30px;
  width: 380px;
  height: 500px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  animation: slideUp 0.3s ease;
  z-index: 998;
}

.ai-assistant-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.ai-assistant-header {
  padding: 16px;
  background: linear-gradient(135deg, var(--gold), #d4a574);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 12px 12px 0 0;
}

.ai-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.ai-close-btn {
  background: rgba(255, 255, 255, 0.3);
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background 0.2s;
}

.ai-close-btn:hover {
  background: rgba(255, 255, 255, 0.5);
}

.ai-assistant-chat {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: #f9f9f9;
}

.ai-chat-messages {
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex: 1;
  overflow-y: auto;
}

.ai-message {
  display: flex;
  animation: fadeIn 0.3s ease;
}

.ai-message.user {
  justify-content: flex-end;
}

.ai-message.assistant {
  justify-content: flex-start;
}

.ai-message-content {
  max-width: 70%;
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 13px;
  line-height: 1.4;
  word-wrap: break-word;
  white-space: pre-wrap;
}

.ai-message.user .ai-message-content {
  background: var(--gold);
  color: white;
  border-radius: 10px 4px 10px 10px;
}

.ai-message.assistant .ai-message-content {
  background: #e8e8e8;
  color: #333;
  border-radius: 4px 10px 10px 10px;
}

.ai-assistant-input {
  display: flex;
  gap: 8px;
  padding: 12px;
  background: white;
  border-top: 1px solid var(--border);
  border-radius: 0 0 12px 12px;
}

.ai-input-field {
  flex: 1;
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 13px;
  font-family: inherit;
  outline: none;
  transition: border-color 0.2s;
}

.ai-input-field:focus {
  border-color: var(--gold);
  box-shadow: 0 0 0 3px rgba(229, 170, 84, 0.1);
}

.ai-send-btn {
  background: var(--gold);
  color: white;
  border: none;
  border-radius: 6px;
  padding: 8px 14px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.ai-send-btn:hover {
  background: #d4a574;
}

.ai-send-btn:active {
  transform: scale(0.95);
}

@media (max-width: 768px) {
  .ai-assistant-modal {
    width: calc(100vw - 48px);
    height: 400px;
    right: 24px;
  }

  .ai-message-content {
    max-width: 90%;
  }
}
</style>

