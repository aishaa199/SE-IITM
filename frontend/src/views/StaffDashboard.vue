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
          <div class="sidebar-logo-sub">Staff Portal</div>
        </div>
        <button style="display: none; background: none; border: none; cursor: pointer; font-size: 24px" @click="sidebarOpen = false" class="mobile-close-btn">✕</button>
      </div>
      <nav class="sidebar-nav">
        <div class="nav-section">My Schedule</div>
        <div
          :class="['nav-item', { active: currentView === 'dashboard' }]"
          @click="currentView = 'dashboard'; sidebarOpen = false"
        >
          <span class="nav-icon">📊</span> Dashboard
        </div>
        <div
          :class="['nav-item', { active: currentView === 'appointments' }]"
          @click="currentView = 'appointments'; sidebarOpen = false"
        >
          <span class="nav-icon">📅</span> My Appointments
        </div>

        <div class="nav-section">Operations</div>
        <div
          :class="['nav-item', { active: currentView === 'order-products' }]"
          @click="currentView = 'order-products'; sidebarOpen = false"
        >
          <span class="nav-icon">📦</span> Order Products
        </div>
      </nav>
      <div class="sidebar-footer">
        <div class="sidebar-user" @click="showProfileMenu = !showProfileMenu" style="cursor: pointer; position: relative">
          <div class="sidebar-avatar">{{ staffData.name[0] }}</div>
          <div>
            <div class="sidebar-username">{{ staffData.name }}</div>
            <div class="sidebar-role">{{ staffData.role }}</div>
          </div>
          <div style="font-size: 18px">▼</div>

          <!-- Profile Dropdown Menu -->
          <div v-if="showProfileMenu" style="position: absolute; bottom: 100%; left: 0; right: 0; background: white; border: 1px solid var(--border); border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 1000; margin-bottom: 8px">
            <button @click="currentView = 'profile'; showProfileMenu = false" style="width: 100%; padding: 12px 16px; border: none; background: none; text-align: left; cursor: pointer; font-size: 14px; border-bottom: 1px solid var(--border)">
              👤 Profile
            </button>
            <button @click="showChangePasswordModal = true; showProfileMenu = false" style="width: 100%; padding: 12px 16px; border: none; background: none; text-align: left; cursor: pointer; font-size: 14px; border-bottom: 1px solid var(--border)">
              🔑 Change Password
            </button>
            <button @click="handleLogout" style="width: 100%; padding: 12px 16px; border: none; background: none; text-align: left; cursor: pointer; font-size: 14px">
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
                <div v-if="fetchedTodayAppointments.length === 0" class="empty-state">
                  <div class="empty-state-icon">📅</div>
                  <div class="empty-state-text">No appointments today</div>
                </div>
                <div v-for="appt in fetchedTodayAppointments" :key="appt.id" class="booking-item">
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
                <button class="btn btn-primary" style="padding: 6px 12px; font-size: 12px" @click="handleMarkTodayAttendance()">Mark Attendance (Today)</button>
              </div>
              <div class="card-body">
                <!-- Loading state -->
                <div v-if="attendanceLoading" style="text-align: center; padding: 24px; color: var(--text-muted)">
                  ⏳ Loading attendance data...
                </div>
                
                <!-- Success message -->
                <div v-if="attendanceSuccess" class="success-message">{{ attendanceSuccess }}</div>
                
                <!-- Error message -->
                <div v-if="attendanceError" class="error-message">{{ attendanceError }}</div>
                
                <!-- Attendance data -->
                <div v-if="!attendanceLoading && !attendanceSuccess && !attendanceError">
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
                    <div v-if="fetchedAttendance.length === 0" style="text-align: center; padding: 20px; color: var(--text-muted)">
                      No attendance records for this month
                    </div>
                    <div v-for="record in fetchedAttendance" :key="record.id" class="attendance-item" style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid var(--border)">
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
        </div>

        <!-- Customer Ratings & Reviews -->
        <div v-if="currentView === 'dashboard'" class="card" style="margin-top: 24px">
          <div class="card-header">
            <h3 class="card-title">⭐ Customer Ratings & Reviews</h3>
          </div>
          <div class="card-body">
            <div v-if="staffRatings.totalRatings > 0">
              <!-- Overall Rating Summary -->
              <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-bottom: 24px; padding: 16px; background: var(--light-bg); border-radius: var(--radius)">
                <div style="text-align: center">
                  <div style="font-size: 32px; font-weight: 700; color: var(--gold)">{{ staffRatings.averageRating }}</div>
                  <div class="text-muted" style="font-size: 13px">Average Rating</div>
                  <div style="margin-top: 8px; letter-spacing: 2px">
                    <span v-for="i in 5" :key="i" :style="{ color: i <= Math.round(staffRatings.averageRating) ? 'var(--gold)' : 'var(--border)' }">⭐</span>
                  </div>
                </div>
                <div style="text-align: center">
                  <div style="font-size: 32px; font-weight: 700; color: var(--info)">{{ staffRatings.totalRatings }}</div>
                  <div class="text-muted" style="font-size: 13px">Total Reviews</div>
                  <div style="margin-top: 8px; font-size: 12px; color: var(--text-muted)">From customers</div>
                </div>
              </div>

              <!-- Individual Ratings List -->
              <div style="max-height: 400px; overflow-y: auto">
                <div v-for="rating in staffRatings.feedbacks" :key="rating.id" style="padding: 16px; border-bottom: 1px solid var(--border); display: flex; gap: 12px">
                  <div style="flex: 1">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px">
                      <div style="font-weight: 600; font-size: 13px">{{ rating.customerName }}</div>
                      <div style="letter-spacing: 1px">
                        <span v-for="i in 5" :key="i" :style="{ color: i <= rating.rating ? 'var(--gold)' : 'var(--border)', fontSize: '12px' }">⭐</span>
                      </div>
                    </div>
                    <div style="color: var(--text-muted); font-size: 13px; margin-bottom: 8px">{{ rating.comment }}</div>
                    <div style="font-size: 11px; color: var(--border)">{{ formatDate(rating.date) }}</div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <div class="empty-state-icon">⭐</div>
              <div class="empty-state-text">No customer ratings yet</div>
              <div class="text-muted" style="font-size: 12px; margin-top: 8px">Complete appointments to receive customer reviews</div>
            </div>
          </div>
        </div>

        <!-- APPOINTMENTS VIEW -->
        <div v-if="currentView === 'appointments'" class="fade-in">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">My Appointments</h3>
            </div>
            <div class="card-body">
              <!-- Appointment Mode Tabs -->
              <div style="display: flex; gap: 12px; margin-bottom: 20px; border-bottom: 2px solid var(--border); padding-bottom: 12px">
                <button 
                  @click="appointmentMode = 'today'; fetchAppointmentsByMode('today')"
                  :style="{ background: appointmentMode === 'today' ? 'var(--gold)' : 'transparent', color: appointmentMode === 'today' ? 'white' : 'var(--text)', borderBottom: 'none', padding: '8px 16px', borderRadius: 'var(--radius)', cursor: 'pointer', border: 'none', fontSize: '14px', fontWeight: '500' }"
                >
                  📅 Today
                </button>
                <button 
                  @click="appointmentMode = 'all'; fetchAppointmentsByMode('all')"
                  :style="{ background: appointmentMode === 'all' ? 'var(--gold)' : 'transparent', color: appointmentMode === 'all' ? 'white' : 'var(--text)', borderBottom: 'none', padding: '8px 16px', borderRadius: 'var(--radius)', cursor: 'pointer', border: 'none', fontSize: '14px', fontWeight: '500' }"
                >
                  📆 All Appointments
                </button>
              </div>

              <!-- Error message -->
              <div v-if="appointmentError" style="padding: 12px; background: var(--error-bg); border: 1px solid var(--error); color: var(--error); border-radius: var(--radius); margin-bottom: 16px">
                ❌ {{ appointmentError }}
              </div>

              <!-- Loading state -->
              <div v-if="appointmentLoading" style="text-align: center; padding: 24px; color: var(--text-muted)">
                ⏳ Loading appointments...
              </div>

              <!-- Filter input -->
              <div v-else style="margin-bottom: 16px">
                <input 
                  v-model="appointmentCustomerFilter"
                  type="text" 
                  placeholder="🔍 Filter by customer name or service..." 
                  class="form-input"
                  style="width: 100%; max-width: 300px"
                />
              </div>
              
              <!-- Empty state -->
              <div v-if="!appointmentLoading && filteredAppointments.length === 0" class="empty-state">
                <div class="empty-state-icon">📅</div>
                <div class="empty-state-text">No appointments found</div>
              </div>

              <!-- Appointments table -->
              <div v-if="!appointmentLoading && filteredAppointments.length > 0" class="table-wrap">
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
                    <tr v-for="appt in filteredAppointments" :key="appt.id" @click="handleViewAppointmentDetails(appt)" style="cursor: pointer; transition: background-color 0.2s" @mouseover="$event.target.closest('tr').style.backgroundColor = 'var(--light-bg)'" @mouseout="$event.target.closest('tr').style.backgroundColor = 'transparent'">
                      <td>{{ appt.customerName }}</td>
                      <td>{{ appt.service }}</td>
                      <td>{{ appt.date }} {{ appt.time }}</td>
                      <td>{{ appt.duration }} min</td>
                      <td>₹{{ appt.amount }}</td>
                      <td>
                        <span :class="['badge', getStatusBadgeClass(appt.status)]">{{ appt.status }}</span>
                      </td>
                      <td>
                        <button v-if="appt.status !== 'completed'" class="btn btn-sm btn-primary" @click.stop="handleMarkAppointmentComplete(appt)" style="padding: 4px 8px; font-size: 12px">
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
          <!-- Order Tabs -->
          <div style="display: flex; gap: 12px; margin-bottom: 20px; border-bottom: 2px solid var(--border); padding-bottom: 12px">
            <button 
              @click="orderTab = 'new-orders'"
              :style="{ background: orderTab === 'new-orders' ? 'var(--gold)' : 'transparent', color: orderTab === 'new-orders' ? 'white' : 'var(--text)', borderBottom: 'none', padding: '8px 16px', borderRadius: 'var(--radius)', cursor: 'pointer', border: 'none', fontSize: '14px', fontWeight: '500' }"
            >
              📦 New Orders
            </button>
          </div>

          <!-- NEW ORDERS TAB -->
          <div v-if="orderTab === 'new-orders'" class="card">
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
                    <option v-for="category in availableCategories" :key="category" :value="category">
                      {{ category }}
                    </option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="product-name">Product Name *</label>
                  <div class="custom-dropdown" v-if="orderForm.selectedCategory" @click.stop>
                    <div 
                      class="custom-dropdown-input"
                      @click="showProductDropdown = !showProductDropdown"
                      :style="{ borderColor: showProductDropdown ? 'var(--gold)' : 'var(--border)' }"
                    >
                      <input 
                        id="product-name"
                        v-model="orderForm.productSearch" 
                        type="text" 
                        placeholder="Type to search products..."
                        class="dropdown-search-input"
                        @focus="showProductDropdown = true"
                        @input="showProductDropdown = true"
                      />
                      <span class="dropdown-arrow">▼</span>
                    </div>
                    <div v-if="showProductDropdown" class="custom-dropdown-menu">
                      <div 
                        v-if="filteredProductsByCategory.length === 0" 
                        class="dropdown-no-results"
                      >
                        No products found
                      </div>
                      <div 
                        v-for="product in filteredProductsByCategory" 
                        :key="product.id"
                        class="dropdown-option"
                        @click="selectProduct(product)"
                        :class="{ selected: orderForm.productId === String(product.id) }"
                      >
                        <div style="font-weight: 500">{{ product.name }}</div>
                        <div class="text-muted" style="font-size: 12px">Stock: {{ product.currentStock }}</div>
                      </div>
                    </div>
                  </div>
                  <select 
                    v-else
                    id="product-name"
                    v-model="orderForm.productId" 
                    class="form-input"
                    required
                    disabled
                  >
                    <option value="">Please select a category first</option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="service">Service It's Required For *</label>
                  <div class="custom-dropdown" @click.stop>
                    <div 
                      class="custom-dropdown-input"
                      @click="showServiceDropdown = !showServiceDropdown"
                      :style="{ borderColor: showServiceDropdown ? 'var(--gold)' : 'var(--border)' }"
                    >
                      <input 
                        id="service"
                        v-model="orderForm.serviceSearch" 
                        type="text" 
                        placeholder="Type to search services..."
                        class="dropdown-search-input"
                        @focus="showServiceDropdown = true"
                        @input="showServiceDropdown = true"
                      />
                      <span class="dropdown-arrow">▼</span>
                    </div>
                    <div v-if="showServiceDropdown" class="custom-dropdown-menu">
                      <div 
                        v-if="filteredServices.length === 0" 
                        class="dropdown-no-results"
                      >
                        No services found
                      </div>
                      <div 
                        v-for="service in filteredServices" 
                        :key="service.id"
                        class="dropdown-option"
                        @click="selectService(service)"
                        :class="{ selected: orderForm.serviceId === String(service.id) }"
                      >
                        <div style="font-weight: 500">{{ service.name }}</div>
                        <div class="text-muted" style="font-size: 12px">₹{{ service.price }}</div>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="form-group">
                  <label for="quantity">Quantity Required *</label>
                  <input 
                    id="quantity"
                    v-model.number="orderForm.quantity" 
                    type="number" 
                    min="1" 
                    max="1000"
                    class="form-input"
                    required
                    placeholder="Enter quantity to order"
                  />
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
          <div class="card" style="margin-top: 24px" v-if="orderTab === 'new-orders'">
            <div class="card-header">
              <h3 class="card-title">My Order History</h3>
            </div>
            <div class="card-body">
              <!-- Date range filter -->
              <div style="margin-bottom: 16px; display: flex; gap: 12px; align-items: flex-end">
                <div>
                  <label style="font-size: 12px; color: var(--text-muted)">From Date</label>
                  <input 
                    v-model="transactionDateFrom"
                    type="date" 
                    class="form-input"
                    style="width: 150px"
                  />
                </div>
                <div>
                  <label style="font-size: 12px; color: var(--text-muted)">To Date</label>
                  <input 
                    v-model="transactionDateTo"
                    type="date" 
                    class="form-input"
                    style="width: 150px"
                  />
                </div>
                <button 
                  @click="fetchStaffInventoryTransactions" 
                  class="btn btn-primary"
                  style="padding: 8px 16px; font-size: 12px"
                >
                  Filter
                </button>
                <button 
                  @click="transactionDateFrom = ''; transactionDateTo = ''; fetchStaffInventoryTransactions()"
                  class="btn btn-outline"
                  style="padding: 8px 16px; font-size: 12px; border-color: var(--border)"
                >
                  Reset
                </button>
              </div>

              <div v-if="inventoryTransactions.length === 0" class="empty-state">
                <div class="empty-state-icon">📦</div>
                <div class="empty-state-text">No orders placed yet</div>
              </div>
              <div class="table-wrap" v-else>
                <table>
                  <thead>
                    <tr>
                      <th>Product</th>
                      <th>Quantity</th>
                      <th>Service</th>
                      <th>Order Type</th>
                      <th>Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="txn in inventoryTransactions" :key="txn.txn_id">
                      <td><strong>{{ txn.product_name }}</strong></td>
                      <td>{{ txn.quantity }}</td>
                      <td>{{ txn.service_name || "N/A" }}</td>
                      <td>
                        <span :class="['badge', txn.txn_type === 0 ? 'badge-info' : 'badge-success']" 
                              style="font-size: 11px; padding: 4px 8px">
                          {{ txn.txn_type === 0 ? 'Internal Order' : 'Replenishment' }}
                        </span>
                      </td>
                      <td>{{ new Date(txn.date_of_txn).toLocaleDateString() }}</td>
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
                <div class="form-group">
                  <label>Date of Birth</label>
                  <input type="text" :value="staffData.dob || 'Not provided'" class="form-input" disabled />
                </div>
                <div class="form-group">
                  <label>Address</label>
                  <textarea class="form-input" disabled rows="2">{{ staffData.address || 'Not provided' }}</textarea>
                </div>
                <div class="form-group">
                  <label>Skills</label>
                  <textarea class="form-input" disabled rows="2">{{ staffData.skills || 'Not provided' }}</textarea>
                </div>
                <button class="btn btn-primary" style="margin-top: 20px" @click="openProfileEdit">
                  Edit Profile
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Appointment Details Modal -->
  <div v-if="showAppointmentDetailsModal" class="modal-overlay" @click="showAppointmentDetailsModal = false">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3 class="modal-title">📅 Appointment Details</h3>
        <button class="modal-close" @click="showAppointmentDetailsModal = false">✕</button>
      </div>
      <div class="modal-body" v-if="selectedAppointment">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px">
          <div style="padding: 12px; background: var(--light-bg); border-radius: var(--radius)"> 
            <div class="text-muted" style="font-size: 12px; margin-bottom: 4px">Customer Name</div>
            <div style="font-weight: 600; font-size: 14px">{{ selectedAppointment.customerName }}</div>
          </div>
          <div style="padding: 12px; background: var(--light-bg); border-radius: var(--radius)">
            <div class="text-muted" style="font-size: 12px; margin-bottom: 4px">Service</div>
            <div style="font-weight: 600; font-size: 14px">{{ selectedAppointment.service }}</div>
          </div>
          <div style="padding: 12px; background: var(--light-bg); border-radius: var(--radius)">
            <div class="text-muted" style="font-size: 12px; margin-bottom: 4px">Date</div>
            <div style="font-weight: 600; font-size: 14px">{{ selectedAppointment.date ? selectedAppointment.date : 'Today' }}</div>
          </div>
          <div style="padding: 12px; background: var(--light-bg); border-radius: var(--radius)">
            <div class="text-muted" style="font-size: 12px; margin-bottom: 4px">Time</div>
            <div style="font-weight: 600; font-size: 14px">{{ selectedAppointment.time }}</div>
          </div>
          <div style="padding: 12px; background: var(--light-bg); border-radius: var(--radius)">
            <div class="text-muted" style="font-size: 12px; margin-bottom: 4px">Duration</div>
            <div style="font-weight: 600; font-size: 14px">{{ selectedAppointment.duration }} minutes</div>
          </div>
          <div style="padding: 12px; background: var(--light-bg); border-radius: var(--radius)">
            <div class="text-muted" style="font-size: 12px; margin-bottom: 4px">Amount</div>
            <div style="font-weight: 600; font-size: 14px; color: var(--success)">₹{{ selectedAppointment.amount }}</div>
          </div>
          <div style="padding: 12px; background: var(--light-bg); border-radius: var(--radius)">
            <div class="text-muted" style="font-size: 12px; margin-bottom: 4px">Status</div>
            <span :class="['badge', getStatusBadgeClass(selectedAppointment.status)]">{{ selectedAppointment.status }}</span>
          </div>
        </div>
        <div style="display: flex; gap: 12px; margin-top: 20px">
          <button class="btn btn-outline" @click="showAppointmentDetailsModal = false" style="flex: 1">
            Close
          </button>
        </div>
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
            <div style="position: relative; display: flex; align-items: center">
              <input 
                id="current-password"
                v-model="passwordForm.currentPassword" 
                :type="showCurrentPassword ? 'text' : 'password'" 
                placeholder="Enter current password"
                class="form-input"
                required
              />
              <button type="button" @click="showCurrentPassword = !showCurrentPassword" style="position: absolute; right: 12px; background: none; border: none; cursor: pointer; font-size: 18px; color: var(--text-muted); padding: 4px">
                {{ showCurrentPassword ? '👁️' : '👁️‍🗨️' }}
              </button>
            </div>
          </div>
          <div class="form-group">
            <label for="new-password">New Password</label>
            <div style="position: relative; display: flex; align-items: center">
              <input 
                id="new-password"
                v-model="passwordForm.newPassword" 
                :type="showNewPassword ? 'text' : 'password'" 
                placeholder="Enter new password"
                class="form-input"
                required
              />
              <button type="button" @click="showNewPassword = !showNewPassword" style="position: absolute; right: 12px; background: none; border: none; cursor: pointer; font-size: 18px; color: var(--text-muted); padding: 4px">
                {{ showNewPassword ? '👁️' : '👁️‍🗨️' }}
              </button>
            </div>
            <div class="form-hint">At least 8 characters</div>
          </div>
          <div class="form-group">
            <label for="confirm-password">Confirm Password</label>
            <div style="position: relative; display: flex; align-items: center">
              <input 
                id="confirm-password"
                v-model="passwordForm.confirmPassword" 
                :type="showConfirmPassword ? 'text' : 'password'" 
                placeholder="Confirm new password"
                class="form-input"
                required
              />
              <button type="button" @click="showConfirmPassword = !showConfirmPassword" style="position: absolute; right: 12px; background: none; border: none; cursor: pointer; font-size: 18px; color: var(--text-muted); padding: 4px">
                {{ showConfirmPassword ? '👁️' : '👁️‍🗨️' }}
              </button>
            </div>
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

  <!-- Edit Profile Modal -->
  <div v-if="showProfileEditModal" class="modal-overlay" @click="showProfileEditModal = false">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3 class="modal-title">✏️ Edit Profile</h3>
        <button class="modal-close" @click="showProfileEditModal = false">✕</button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="handleUpdateProfile">
          <div class="form-group">
            <label for="edit-name">Name *</label>
            <input 
              id="edit-name"
              v-model="profileForm.name" 
              type="text" 
              placeholder="Enter your name"
              class="form-input"
              required
            />
          </div>
          <div class="form-group">
            <label for="edit-email">Email *</label>
            <input 
              id="edit-email"
              v-model="profileForm.email" 
              type="email" 
              placeholder="Enter your email"
              class="form-input"
              required
            />
          </div>
          <div class="form-group">
            <label for="edit-phone">Phone *</label>
            <input 
              id="edit-phone"
              v-model="profileForm.phone" 
              type="tel" 
              placeholder="Enter your phone number"
              class="form-input"
              required
            />
          </div>
          <div class="form-group">
            <label for="edit-dob">Date of Birth</label>
            <input 
              id="edit-dob"
              v-model="profileForm.dob" 
              type="date" 
              class="form-input"
            />
          </div>
          <div class="form-group">
            <label for="edit-address">Address</label>
            <textarea 
              id="edit-address"
              v-model="profileForm.address" 
              placeholder="Enter your address"
              class="form-input"
              rows="3"
            ></textarea>
          </div>
          <div class="form-group">
            <label for="edit-skills">Skills</label>
            <textarea 
              id="edit-skills"
              v-model="profileForm.skills" 
              placeholder="Enter your skills"
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
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { useAppStore } from "../stores/appStore";

const router = useRouter();
const API_BASE_URL = "http://localhost:5000";

const currentView = ref("dashboard");
const sidebarOpen = ref(false);
const showChangePasswordModal = ref(false);
const showCurrentPassword = ref(false);
const showNewPassword = ref(false);
const showConfirmPassword = ref(false);
const showProfileMenu = ref(false);
const showProfileEditModal = ref(false);
const showAppointmentDetailsModal = ref(false);
const selectedAppointment = ref(null);
const showProductDropdown = ref(false);
const showServiceDropdown = ref(false);
const passwordForm = ref({
  currentPassword: "",
  newPassword: "",
  confirmPassword: ""
});
const orderForm = ref({
  productId: "",
  quantity: 1,
  serviceId: "",
  selectedCategory: "",
  productSearch: "",
  serviceSearch: ""
});
const profileForm = ref({
  name: "",
  email: "",
  phone: "",
  dob: "",
  address: "",
  skills: ""
});
const passwordError = ref("");
const passwordSuccess = ref("");
const orderError = ref("");
const orderSuccess = ref("");
const products = ref([]);
const services = ref([]);
const inventoryTransactions = ref([]);
const transactionDateFrom = ref("");
const transactionDateTo = ref("");

// Order Tab
const orderTab = ref("new-orders");

// Appointment mode and data
const appointmentMode = ref("today"); // 'today' or 'all'
const fetchedTodayAppointments = ref([]);
const fetchedAllAppointments = ref([]);
const appointmentLoading = ref(false);
const appointmentError = ref("");

// Attendance data
const attendanceLoading = ref(false);
const attendanceError = ref("");
const attendanceSuccess = ref("");
const fetchedAttendance = ref([]);

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

// Fetch appointments from API
const fetchAppointmentsByMode = async (mode = "today") => {
  appointmentLoading.value = true;
  appointmentError.value = "";

  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      appointmentError.value = "Not authenticated. Please login again.";
      return;
    }

    let appointmentsList = [];

    if (mode === "today") {
      // Fetch only today's appointments
      const today = new Date().toISOString().split('T')[0];
      const url = `${API_BASE_URL}/api/staff-appointments?date=${today}`;
      
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
          "Authentication-Token": token
        }
      });

      if (!response.ok) {
        const data = await response.json();
        
        // If it's a 404 for "No appointments found", treat as empty list
        if (response.status === 404 && data.message && data.message.includes("No appointments found")) {
          fetchedTodayAppointments.value = [];
          appointmentError.value = ""; // Clear error
          appointmentLoading.value = false;
          return;
        }
        
        appointmentError.value = data.message || `Failed to fetch today appointments`;
        fetchedTodayAppointments.value = [];
        appointmentLoading.value = false;
        return;
      }

      const data = await response.json();
      appointmentsList = data;
    } else {
      // Fetch all future appointments - fetch next 5 days
      const allAppointments = [];
      const baseDate = new Date();
      
      // Fetch appointments for next 5 days
      for (let i = 0; i < 5; i++) {
        const fetchDate = new Date(baseDate);
        fetchDate.setDate(fetchDate.getDate() + i);
        const dateStr = fetchDate.toISOString().split('T')[0];
        
        const url = `${API_BASE_URL}/api/staff-appointments?date=${dateStr}`;
        
        try {
          const response = await fetch(url, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
              "Authentication-Token": token
            }
          });

          if (response.ok) {
            const data = await response.json();
            if (data && data.length > 0) {
              allAppointments.push(...data);
            }
          } else if (response.status === 404) {
            // No appointments on this date, continue to next day
          }
        } catch (error) {
          // Handle fetch error silently, continue to next date
        }
      }
      
      appointmentsList = allAppointments;
    }

    // Transform API response into UI format
    const formattedAppointments = appointmentsList.map(appt => {
      const dateTime = new Date(appt.datetime);
      const date = dateTime.toISOString().split('T')[0];
      const time = dateTime.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });
      
      return {
        id: appt.appointment_id,
        customerName: appt.customer_name,
        service: appt.services && appt.services.length > 0 
          ? appt.services.map(s => s.name).join(", ")
          : "N/A",
        date: date,
        time: time,
        duration: 60, // Default, if not in API response
        status: "confirmed", // Default status if not in API response
        amount: 0 // Default, if not in API response
      };
    });

    if (mode === "today") {
      fetchedTodayAppointments.value = formattedAppointments;
      // Update mock data for backward compatibility
      staffData.todayAppointments = formattedAppointments;
    } else if (mode === "all") {
      fetchedAllAppointments.value = formattedAppointments;
      // Update mock data for backward compatibility
      staffData.upcomingAppointments = formattedAppointments;
    }
  } catch (error) {
    console.error("Error fetching appointments:", error);
    appointmentError.value = "Error fetching appointments. Please try again.";
  } finally {
    appointmentLoading.value = false;
  }
};

// Fetch attendance data for current month
const fetchAttendance = async () => {
  attendanceLoading.value = true;
  attendanceError.value = "";

  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      console.warn("No auth token found - skipping attendance fetch");
      attendanceLoading.value = false;
      attendanceError.value = "Authentication token not found. Please login again.";
      return;
    }

    // Get current month and year
    const now = new Date();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const year = now.getFullYear();

    console.log("Fetching attendance for", month, year);

    const response = await fetch(
      `${API_BASE_URL}/api/staff-attendance?month=${month}&year=${year}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
          "Authentication-Token": token
        }
      }
    );

    console.log("Attendance response status:", response.status);

    if (response.status === 403) {
      // Authorization denied - likely missing staff role
      console.error("Access denied to attendance records - check user role assignment");
      attendanceError.value = "You don't have permission to view attendance records. Contact your manager.";
      fetchedAttendance.value = [];
      return;
    }

    if (response.status === 404) {
      // No records found for this month - show empty state
      console.log("No attendance records for this month");
      fetchedAttendance.value = [];
      staffData.monthlyAttendance = [];
      return;
    }

    if (!response.ok) {
      const data = await response.json();
      console.error("Attendance fetch error:", response.status, data);
      attendanceError.value = data.message || "Failed to fetch attendance";
      fetchedAttendance.value = [];
      return;
    }

    const data = await response.json();
    console.log("Attendance data received:", data);
    console.log("Data is array?", Array.isArray(data));
    console.log("Data length:", data ? data.length : 0);
    
    // Handle both array and object responses
    let attendanceRecords = [];
    if (Array.isArray(data)) {
      attendanceRecords = data;
    } else if (data && typeof data === 'object') {
      // If response is an object with a message, it's an error-like response
      if (data.message) {
        console.log("API returned message:", data.message);
        fetchedAttendance.value = [];
        staffData.monthlyAttendance = [];
        attendanceLoading.value = false;
        return;
      }
      // Otherwise try to extract records from the object
      attendanceRecords = Object.values(data).filter(item => item && typeof item === 'object');
    }
    
    // Transform API response into UI format
    const formattedAttendance = attendanceRecords.map(record => ({
      id: record.register_id,
      date: new Date(record.register_datetime).toISOString().split('T')[0],
      status: "present" // Marking a record means the staff was present
    }));

    console.log("Formatted attendance:", formattedAttendance);
    fetchedAttendance.value = formattedAttendance;
    staffData.monthlyAttendance = formattedAttendance;
  } catch (error) {
    console.error("Error fetching attendance:", error);
    attendanceError.value = "Network error while fetching attendance. Please try again.";
    fetchedAttendance.value = [];
  } finally {
    attendanceLoading.value = false;
  }
};

// Calculate attendance stats
const attendanceStats = computed(() => {
  const stats = { present: 0, absent: 0, late: 0 };
  const records = fetchedAttendance.value.length > 0 ? fetchedAttendance.value : staffData.monthlyAttendance;
  records.forEach(record => {
    if (record.status === 'present') stats.present++;
    else if (record.status === 'absent') stats.absent++;
    else if (record.status === 'late') stats.late++;
  });
  return stats;
});

// Filtered appointments & orders
const filteredAppointments = computed(() => {
  // Use fetched appointments based on current mode
  const appointments = appointmentMode.value === "today" 
    ? fetchedTodayAppointments.value 
    : fetchedAllAppointments.value;
  
  if (!appointmentCustomerFilter.value.trim()) return appointments;
  const searchTerm = appointmentCustomerFilter.value.toLowerCase();
  return appointments.filter(appt =>
    appt.customerName.toLowerCase().includes(searchTerm) ||
    appt.service.toLowerCase().includes(searchTerm)
  );
});

const filteredOrders = computed(() => {
  if (!orderProductFilter.value.trim()) return staffData.orders;
  const searchTerm = orderProductFilter.value.toLowerCase();
  return staffData.orders.filter(order => {
    const productName = getProductName(order.productId).toLowerCase();
    const serviceName = getServiceName(order.serviceId).toLowerCase();
    return productName.includes(searchTerm) || serviceName.includes(searchTerm);
  });
});

const availableCategories = computed(() => {
  // Get unique categories from fetched products
  const categories = [...new Set(products.value.map(p => p.category))];
  return categories.filter(cat => cat && cat !== "Other");
});

const filteredProductsByCategory = computed(() => {
  if (!orderForm.value.selectedCategory) return [];
  let filtered = products.value.filter(product => {
    const category = getCategoryForProduct(product.id);
    return category === orderForm.value.selectedCategory;
  });

  // Apply search filter if search term exists
  if (orderForm.value.productSearch.trim()) {
    filtered = filtered.filter(product =>
      product.name.toLowerCase().includes(orderForm.value.productSearch.toLowerCase())
    );
  }

  return filtered;
});

const filteredServices = computed(() => {
  let svcs = services.value || [];
  
  if (orderForm.value.serviceSearch.trim()) {
    svcs = svcs.filter(service =>
      service.name.toLowerCase().includes(orderForm.value.serviceSearch.toLowerCase())
    );
  }
  
  return svcs;
});

// Get real staff data from appStore based on current user
const appStore = useAppStore();

// Mock data
const staffData = {
  name: "Sarah Johnson",
  role: "Beauty Therapist",
  email: "sarah@example.com",
  phone: "+233 123 456 789",
  dob: "1992-03-15",
  address: "123 Main Street, Accra, Ghana",
  skills: "Hair Styling, Makeup, Skincare, Customer Service",
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
      duration: 45,
      amount: 40,
    },
    {
      id: 7,
      customerName: "Grace Lee",
      service: "Spa Package",
      date: "2026-03-06",
      time: "02:00 PM",
      status: "confirmed",
      duration: 120,
      amount: 150,
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

// Get ratings received by current staff member
const currentStaffId = 1; // Amara Osei - would come from authenticated user in production

const staffRatings = computed(() => {
  const staffFeedbacks = appStore.data.feedbacks.filter(f => f.staffId === currentStaffId);
  if (staffFeedbacks.length === 0) return { feedbacks: [], averageRating: 0 };
  
  const totalRating = staffFeedbacks.reduce((sum, f) => sum + f.rating, 0);
  const averageRating = (totalRating / staffFeedbacks.length).toFixed(1);
  
  // Enrich feedbacks with customer names
  const enrichedFeedbacks = staffFeedbacks.map(f => {
    const customer = appStore.data.customers.find(c => c.id === f.customerId);
    return {
      ...f,
      customerName: customer ? customer.name : "Anonymous Customer"
    };
  });
  
  return {
    feedbacks: enrichedFeedbacks,
    averageRating: parseFloat(averageRating),
    totalRatings: staffFeedbacks.length
  };
});

const getProductName = (productId) => {
  const product = products.value.find(p => p.id === productId);
  return product ? product.name : "Unknown";
};

const getServiceName = (serviceId) => {
  const service = services.value.find(s => s.id === serviceId);
  return service ? service.name : "Unknown";
};

const getCategoryForProduct = (productId) => {
  const product = products.value.find(p => p.id === productId);
  return product ? product.category : "Other";
};

const handleViewAppointmentDetails = (appt) => {
  selectedAppointment.value = { ...appt };
  showAppointmentDetailsModal.value = true;
};

const selectProduct = (product) => {
  orderForm.value.productId = String(product.id);
  orderForm.value.productSearch = product.name;
  showProductDropdown.value = false;
};

const selectService = (service) => {
  orderForm.value.serviceId = String(service.id);
  orderForm.value.serviceSearch = service.name;
  showServiceDropdown.value = false;
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

const handleChangePassword = async () => {
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

  const token = localStorage.getItem("authToken");
  if (!token) {
    passwordError.value = "You are not authenticated. Please log in again.";
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/change-password`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token,
      },
      body: JSON.stringify({
        current_password: passwordForm.value.currentPassword,
        new_password: passwordForm.value.newPassword,
        confirm_password: passwordForm.value.confirmPassword,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      passwordError.value = data.message || "Failed to change password";
      return;
    }

    passwordSuccess.value = data.message || "Password changed successfully!";
    setTimeout(() => {
      passwordForm.value = {
        currentPassword: "",
        newPassword: "",
        confirmPassword: ""
      };
      passwordSuccess.value = "";
      showChangePasswordModal.value = false;
    }, 1500);
  } catch (error) {
    passwordError.value = "Unable to connect to server. Please try again.";
  }
};

const handleMarkTodayAttendance = async () => {
  attendanceError.value = "";
  attendanceSuccess.value = "";
  
  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      attendanceError.value = "Not authenticated. Please login again.";
      return;
    }

    console.log("Marking attendance...");
    
    // Call backend API to mark attendance
    const response = await fetch(`${API_BASE_URL}/api/staff-attendance`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    console.log("Mark attendance response status:", response.status);
    
    const data = await response.json();
    console.log("Mark attendance response:", data);

    if (response.ok) {
      // 201 Created - successfully marked
      attendanceSuccess.value = "✅ Attendance marked as present for today!";
      
      // Refresh attendance data from backend
      await fetchAttendance();
      
      setTimeout(() => {
        attendanceSuccess.value = "";
      }, 2000);
    } else if (response.status === 400) {
      // 400 - likely already marked or other validation error
      // Check if it's the "already marked" error specifically
      const message = data.message || "";
      console.log("400 error message:", message);
      
      if (message.toLowerCase().includes("already marked")) {
        // Attendance already marked - show as informational message
        attendanceSuccess.value = "ℹ️ Attendance already marked for today!";
        
        // Still refresh data in case
        await fetchAttendance();
        
        setTimeout(() => {
          attendanceSuccess.value = "";
        }, 2000);
      } else {
        // Some other 400 error
        attendanceError.value = message || "Invalid request. Please try again.";
      }
    } else if (response.status === 403) {
      attendanceError.value = "You don't have permission to mark attendance. Contact your manager.";
    } else {
      attendanceError.value = data.message || "Failed to mark attendance. Please try again.";
      console.error("Backend error:", response.status, data);
    }
  } catch (error) {
    console.error("Error marking attendance:", error);
    attendanceError.value = `Connection error: ${error.message}`;
  }
};

// Fetch products from backend
const fetchProducts = async () => {
  try {
    const token = localStorage.getItem("authToken");
    if (!token) return;

    const response = await fetch(`${API_BASE_URL}/api/product`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (response.ok) {
      const data = await response.json();
      // Map backend fields to frontend format
      products.value = data.map(p => ({
        id: p.product_id,
        name: p.product_desc,
        category: p.product_category_name,
        price: p.product_price,
        currentStock: p.product_curr_qoh,
        minStock: p.product_min_qoh,
        supplier: p.product_supplier_name
      }));
      console.log("Products fetched:", products.value);
    } else {
      console.error("Failed to fetch products:", response.status);
    }
  } catch (error) {
    console.error("Error fetching products:", error);
  }
};

// Fetch services from backend
const fetchServices = async () => {
  try {
    const token = localStorage.getItem("authToken");
    if (!token) return;

    const response = await fetch(`${API_BASE_URL}/api/service`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (response.ok) {
      const data = await response.json();
      // Map backend fields to frontend format and filter only active services
      services.value = data
        .filter(s => s.active_flg === true) // Only active services
        .map(s => ({
          id: s.service_id,
          name: s.service_desc,
          category: s.service_category,
          price: s.service_price,
          duration: s.service_duration
        }));
      console.log("Services fetched:", services.value);
    } else {
      console.error("Failed to fetch services:", response.status);
    }
  } catch (error) {
    console.error("Error fetching services:", error);
  }
};

// Fetch inventory transactions (orders) for staff
const fetchStaffInventoryTransactions = async () => {
  try {
    const token = localStorage.getItem("authToken");
    if (!token) return;

    let url = `${API_BASE_URL}/api/inventory-transaction`;
    
    // Add date range if provided
    if (transactionDateFrom.value && transactionDateTo.value) {
      url += `?from_date=${transactionDateFrom.value}&to_date=${transactionDateTo.value}`;
    }

    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (response.ok) {
      const data = await response.json();
      inventoryTransactions.value = data;
      console.log("Inventory transactions fetched:", data);
    } else {
      console.error("Failed to fetch inventory transactions:", response.status);
    }
  } catch (error) {
    console.error("Error fetching inventory transactions:", error);
  }
};

const handleOrderProduct = async () => {
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

  if (!orderForm.value.quantity || orderForm.value.quantity <= 0) {
    orderError.value = "Quantity must be greater than 0";
    return;
  }

  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      orderError.value = "Authentication required. Please login again.";
      return;
    }

    const payload = {
      product_id: parseInt(orderForm.value.productId),
      service_id: parseInt(orderForm.value.serviceId),
      quantity: parseInt(orderForm.value.quantity)
    };

    console.log("Placing order with payload:", payload);

    const response = await fetch(`${API_BASE_URL}/api/inventory-transaction`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      },
      body: JSON.stringify(payload)
    });

    const result = await response.json();

    if (response.ok) {
      orderSuccess.value = `Order placed successfully for ${getProductName(parseInt(orderForm.value.productId))}!`;
      console.log("Order created:", result);
      
      // Fetch updated orders history
      setTimeout(() => {
        orderForm.value = {
          productId: "",
          quantity: 1,
          serviceId: "",
          selectedCategory: "",
          productSearch: "",
          serviceSearch: ""
        };
        orderSuccess.value = "";
        showProductDropdown.value = false;
        showServiceDropdown.value = false;
      }, 1500);
    } else {
      orderError.value = result.message || "Failed to place order";
      console.error("Error placing order:", response.status, result);
    }
  } catch (error) {
    orderError.value = "Unable to connect to server. Please try again.";
    console.error("Network error:", error);
  }
};



const handleLogout = () => {
  appStore.logout();
  router.push("/login/staff");
};

const openProfileEdit = () => {
  profileForm.value = {
    name: staffData.name,
    email: staffData.email,
    phone: staffData.phone,
    dob: staffData.dob || "",
    address: staffData.address || "",
    skills: staffData.skills || ""
  };
  showProfileEditModal.value = true;
};

const handleUpdateProfile = () => {
  // Update staff data with form values
  staffData.name = profileForm.value.name;
  staffData.email = profileForm.value.email;
  staffData.phone = profileForm.value.phone;
  staffData.dob = profileForm.value.dob;
  staffData.address = profileForm.value.address;
  staffData.skills = profileForm.value.skills;
  
  // Close modal and show success
  showProfileEditModal.value = false;
  console.log("Profile updated successfully");
};

// Close dropdown when clicking outside
const handleClickOutside = (e) => {
  // Close product dropdown
  const productDropdown = document.querySelector('.custom-dropdown');
  if (productDropdown && !productDropdown.contains(e.target)) {
    showProductDropdown.value = false;
    showServiceDropdown.value = false;
  }
  
  // Close profile menu
  const sidebarUser = document.querySelector('.sidebar-user');
  if (sidebarUser && !sidebarUser.contains(e.target)) {
    showProfileMenu.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
  
  // Fetch today's appointments on mount
  fetchAppointmentsByMode("today");
  
  // Fetch attendance data on mount
  fetchAttendance();
  
  // Fetch products and services for ordering
  fetchProducts();
  fetchServices();
  
  // Fetch inventory transactions (order history)
  fetchStaffInventoryTransactions();
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
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
</style>
