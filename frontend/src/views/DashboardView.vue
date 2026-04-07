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
          @click="currentView = 'rewards'; fetchRewardsSettings(); sidebarOpen = false"
        >
          <span class="nav-icon">🎁</span> Rewards
        </div>
        <div
          :class="['nav-item', { active: currentView === 'invoices' }]"
          @click="currentView = 'invoices'; fetchInvoices(); sidebarOpen = false"
        >
          <span class="nav-icon">📄</span> Invoices
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
          <span class="nav-icon">📮</span> Orders
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

        <div class="nav-section">Settings</div>
        <div
          :class="['nav-item', { active: currentView === 'settings' }]"
          @click="currentView = 'settings'; fetchSalonConfig()"
        >
          <span class="nav-icon">⚙️</span> Salon Settings
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

          <!-- AI Daily Briefing Card -->
          <div v-if="!briefingDismissed" style="margin-bottom: 24px; border-radius: 12px; overflow: hidden; background: linear-gradient(135deg, #8B6914 0%, #C9A96E 60%, #b8945a 100%); box-shadow: 0 4px 20px rgba(139,105,20,0.35); border: 1px solid rgba(255,220,140,0.3);">

            <!-- Loading state -->
            <div v-if="briefingLoading" style="padding: 32px; text-align: center; color: #1A1A1A;">
              <div style="font-size: 30px; margin-bottom: 10px;">✨</div>
              <div style="font-size: 14px; opacity: 0.7;">Generating your AI briefing…</div>
            </div>

            <!-- Error state -->
            <div v-else-if="briefingError" style="padding: 20px 24px; display: flex; align-items: center; justify-content: space-between; color: #1A1A1A;">
              <span style="font-size: 14px; opacity: 0.8;">⚠️ {{ briefingError }}</span>
              <div style="display: flex; gap: 8px;">
                <button @click="fetchBriefing()" style="background: rgba(26,26,26,0.12); border: 1px solid rgba(26,26,26,0.25); color: #1A1A1A; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 600;">Retry</button>
                <button @click="briefingDismissed = true" style="background: transparent; border: none; color: rgba(26,26,26,0.5); cursor: pointer; font-size: 18px; line-height: 1;">✕</button>
              </div>
            </div>

            <!-- Briefing content -->
            <div v-else-if="briefingData" style="padding: 24px; color: #1A1A1A;">
              <!-- Header row -->
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
                <div>
                  <div style="font-size: 20px; font-weight: 700; margin-bottom: 4px; color: #1A1A1A;">{{ briefingData.greeting }}</div>
                  <div style="font-size: 14px; color: #2D2D2D; opacity: 0.8;">{{ briefingData.summary }}</div>
                </div>
                <div style="display: flex; gap: 8px; flex-shrink: 0; margin-left: 16px;">
                  <button @click="fetchBriefing()" title="Refresh briefing" style="background: rgba(26,26,26,0.1); border: 1px solid rgba(26,26,26,0.2); color: #1A1A1A; width: 32px; height: 32px; border-radius: 50%; cursor: pointer; font-size: 15px; display: flex; align-items: center; justify-content: center;">↻</button>
                  <button @click="briefingDismissed = true" title="Dismiss" style="background: rgba(26,26,26,0.1); border: 1px solid rgba(26,26,26,0.2); color: #1A1A1A; width: 32px; height: 32px; border-radius: 50%; cursor: pointer; font-size: 13px; display: flex; align-items: center; justify-content: center;">✕</button>
                </div>
              </div>

              <!-- Divider -->
              <div style="height: 1px; background: rgba(26,26,26,0.15); margin-bottom: 18px;"></div>

              <!-- Insights + Recommendations columns -->
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                  <div style="font-size: 11px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; color: #4A4A4A; margin-bottom: 10px;">Key Insights</div>
                  <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px;">
                    <li v-for="(insight, i) in briefingData.insights" :key="'ins-' + i" style="font-size: 13px; padding-left: 18px; position: relative; color: #1A1A1A; line-height: 1.45;">
                      <span style="position: absolute; left: 0; color: #4A3000; font-size: 16px; line-height: 1;">•</span>{{ insight }}
                    </li>
                  </ul>
                </div>
                <div>
                  <div style="font-size: 11px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; color: #4A4A4A; margin-bottom: 10px;">Recommendations</div>
                  <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px;">
                    <li v-for="(rec, i) in briefingData.recommendations" :key="'rec-' + i" style="font-size: 13px; padding-left: 18px; position: relative; color: #1A1A1A; line-height: 1.45;">
                      <span style="position: absolute; left: 0; color: #2D5A27; font-size: 14px; line-height: 1.1;">→</span>{{ rec }}
                    </li>
                  </ul>
                </div>
              </div>

              <div v-if="briefingData.ai_error" style="margin-top: 14px; font-size: 11px; color: rgba(26,26,26,0.4);">Note: AI unavailable — showing data-driven fallback.</div>
            </div>

            <!-- Initial state (no data yet, not loading) -->
            <div v-else style="padding: 28px; text-align: center; color: #1A1A1A;">
              <div style="font-size: 28px; margin-bottom: 10px;">🤖</div>
              <div style="font-size: 14px; opacity: 0.7; margin-bottom: 16px;">Get your AI-powered daily briefing</div>
              <button @click="fetchBriefing()" style="background: rgba(26,26,26,0.12); border: 1px solid rgba(26,26,26,0.25); color: #1A1A1A; padding: 8px 22px; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 600;">Generate Briefing</button>
            </div>
          </div>
          <!-- End AI Daily Briefing Card -->

          <!-- AI Task Checklist Card -->
          <div style="margin-bottom: 24px; background: white; border-radius: 12px; border: 1px solid var(--border); box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
            <div style="padding: 16px 20px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center;">
              <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 18px;">✅</span>
                <span style="font-weight: 700; font-size: 15px; color: var(--charcoal);">Today's AI Tasks</span>
                <span v-if="managerTasks.length > 0" style="background: var(--gold); color: white; border-radius: 10px; padding: 1px 8px; font-size: 11px; font-weight: 600;">{{ pendingTasks.length }} left</span>
              </div>
              <button @click="generateManagerTasks" :disabled="tasksLoading" class="generate-tasks-btn">
                <span v-if="tasksLoading">⏳ Generating…</span>
                <span v-else>✨ Generate Tasks</span>
              </button>
            </div>

            <div style="padding: 16px 20px;">
              <!-- Error state -->
              <div v-if="tasksError" style="color: #e53e3e; font-size: 13px; padding: 6px 0;">⚠️ {{ tasksError }}</div>

              <!-- Empty state -->
              <div v-else-if="managerTasks.length === 0 && !tasksLoading" style="color: var(--text-muted); font-size: 13px; text-align: center; padding: 14px 0;">
                Ask the chatbot <strong>"Create a task checklist for today"</strong> or click <em>Generate Tasks</em> above.
              </div>

              <!-- Pending tasks -->
              <div v-if="pendingTasks.length > 0">
                <div class="task-section-label">Pending</div>
                <div v-for="task in pendingTasks" :key="task.task_id" class="task-item" @click="toggleTask(task)">
                  <span class="task-checkbox pending-cb">☐</span>
                  <div class="task-info">
                    <span class="task-description">{{ task.task_description }}</span>
                    <span :class="['task-badge', 'badge-' + task.task_section]">{{ task.task_section }}</span>
                  </div>
                </div>
              </div>

              <!-- Completed tasks -->
              <div v-if="completedTasks.length > 0" :style="pendingTasks.length > 0 ? 'margin-top: 16px;' : ''">
                <div class="task-section-label">Completed</div>
                <div v-for="task in completedTasks" :key="task.task_id" class="task-item completed-task" @click="toggleTask(task)">
                  <span class="task-checkbox completed-cb">☑</span>
                  <div class="task-info">
                    <span class="task-description" style="text-decoration: line-through; color: var(--text-muted);">{{ task.task_description }}</span>
                    <span :class="['task-badge', 'badge-' + task.task_section]">{{ task.task_section }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- End AI Task Checklist Card -->

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
                    <div class="booking-time">{{ getTimeFromDate(appt.datetime) }}</div>
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
                    <button class="btn btn-sm btn-primary" @click="handleCreateInvoiceFromAppointment(appt)" style="padding: 4px 8px; font-size: 11px">
                      📄 Invoice
                    </button>
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

          <!-- Daywise Appointment Count -->
          <div class="card" style="margin-top: 24px">
            <div class="card-header">
              <h3 class="card-title">📊 Salon Appointments - Daywise</h3>
            </div>
            <div class="card-body">
              <div v-if="dailyCountLoading" style="text-align: center; padding: 20px; color: var(--text-muted)">
                ⏳ Loading appointment data...
              </div>
              <div v-else-if="dailyCountError" class="error-message" style="margin-bottom: 16px">
                {{ dailyCountError }}
              </div>
              <div v-else-if="dailyAppointmentCounts.length === 0" class="empty-state">
                <div class="empty-state-icon">📊</div>
                <div class="empty-state-text">No appointment data available</div>
              </div>
              <div v-else style="overflow-x: auto">
                <table style="width: 100%; border-collapse: collapse">
                  <thead>
                    <tr style="background: var(--light-bg); border-bottom: 2px solid var(--border)">
                      <th style="padding: 12px; text-align: left; font-weight: 600">Date</th>
                      <th style="padding: 12px; text-align: center; font-weight: 600">Appointments</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="dayCount in dailyAppointmentCounts" :key="dayCount.date" style="border-bottom: 1px solid var(--border); cursor: pointer; transition: background-color 0.2s" @mouseenter="$event.target.closest('tr').style.backgroundColor = 'var(--light-bg)'" @mouseleave="$event.target.closest('tr').style.backgroundColor = 'transparent'">
                      <td style="padding: 12px; text-align: left">
                        {{ new Date(dayCount.date).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', weekday: 'short' }) }}
                      </td>
                      <td style="padding: 12px; text-align: center">
                        <span style="display: inline-block; background: var(--gold); color: white; padding: 6px 12px; border-radius: 20px; font-weight: 600; font-size: 14px">
                          {{ dayCount.count }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
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
                    <label for="booking-customer-email">Customer Email</label>
                    <input
                      id="booking-customer-email"
                      :value="selectedBookingCustomer?.email || ''"
                      type="email"
                      class="form-input"
                      placeholder="Auto-filled after selecting customer"
                      readonly
                    />
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

                <button type="submit" class="btn btn-primary" style="margin-top: 16px; width: 100%">
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
            <div class="card-header" style="display: flex; justify-content: space-between; align-items: center">
              <h3 class="card-title">📅 {{ selectedDate ? 'Appointments - ' + formatDateShort(selectedDate) : "All Appointments" }}</h3>
              <button v-if="selectedDate" @click="selectedDate = null" class="btn btn-sm btn-outline" style="padding: 6px 12px">
                View All
              </button>
            </div>
            <div class="card-body">
              <div style="margin-bottom: 16px">
                <input 
                  v-model="bookingCustomerName"
                  type="text" 
                  placeholder="🔍 Filter by customer name or email..." 
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
                  <div class="booking-time">{{ getTimeFromDate(appt.datetime) }}</div>
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
              <h3 class="card-title">{{ isEditingService ? '✎ Edit Service' : '➕ Add New Service' }}</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleServiceSubmit" style="max-width: 800px">
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

                  <div class="form-group">
                    <label for="service-from-date">From Date</label>
                    <input 
                      id="service-from-date"
                      v-model="serviceForm.fromDate"
                      type="date"
                      class="form-input"
                    />
                  </div>

                  <div class="form-group">
                    <label for="service-to-date">To Date</label>
                    <input 
                      id="service-to-date"
                      v-model="serviceForm.toDate"
                      type="date"
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
                      <th>From Date</th>
                      <th>To Date</th>
                      <th>Status</th>
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
                      <td style="font-size: 12px">{{ service.fromDate || '-' }}</td>
                      <td style="font-size: 12px">{{ service.toDate || '-' }}</td>
                      <td>
                        <span v-if="getServiceStatus(service) === 'Active'" style="background: #d4edda; color: #155724; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600">✓ Active</span>
                        <span v-else-if="getServiceStatus(service) === 'Disabled'" style="background: #f8cccb; color: #c1272d; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600">⊘ Disabled</span>
                        <span v-else style="background: #f8d7da; color: #721c24; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600">✗ Inactive</span>
                      </td>
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
                      <th>Available Rewards</th>
                      <th>Preferences</th>
                      <th>No. of Visits</th>
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
                      <td style="text-align: center; font-weight: 600; color: var(--gold)">🎁 {{ customer.pointsBalance || 0 }}</td>
                      <td style="font-size: 12px; color: #666">{{ customer.preferences || '-' }}</td>
                      <td style="text-align: center; font-weight: 600">{{ customer.noOfVisits || 0 }}</td>
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

          <!-- Edit Customer Modal -->
          <div v-if="isEditingCustomer" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000" @click.self="cancelEditCustomer">
            <div style="background: white; border-radius: 12px; padding: 32px; max-width: 700px; width: 90%; max-height: 90vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0,0,0,0.3)">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px">
                <h2 style="margin: 0; font-size: 24px; font-weight: 600">✎ Edit Customer</h2>
                <button @click="cancelEditCustomer" style="background: none; border: none; font-size: 24px; cursor: pointer; color: #999">✕</button>
              </div>

              <!-- Customer Info Display -->
              <div style="background: var(--light-bg); padding: 16px; border-radius: 8px; margin-bottom: 24px">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                  <div>
                    <div style="font-size: 12px; color: var(--text-muted); font-weight: 600; margin-bottom: 4px">REGISTRATION DATE</div>
                    <div style="font-weight: 600">{{ editingCustomerData?.registrationDate || 'N/A' }}</div>
                  </div>
                  <div>
                    <div style="font-size: 12px; color: var(--text-muted); font-weight: 600; margin-bottom: 4px">DATE OF BIRTH</div>
                    <div style="font-weight: 600">{{ editingCustomerData?.dob || 'N/A' }}</div>
                  </div>
                  <div>
                    <div style="font-size: 12px; color: var(--text-muted); font-weight: 600; margin-bottom: 4px">TOTAL VISITS</div>
                    <div style="font-weight: 600">{{ editingCustomerData?.noOfVisits || 0 }}</div>
                  </div>
                  <div>
                    <div style="font-size: 12px; color: var(--text-muted); font-weight: 600; margin-bottom: 4px">POINTS BALANCE</div>
                    <div style="font-weight: 600; color: var(--primary)">{{ Math.round(editingCustomerData?.pointsBalance || 0) }}</div>
                  </div>
                </div>
              </div>

              <!-- Edit Form -->
              <form @submit.prevent="handleUpdateCustomer" style="margin-bottom: 20px">
                <div class="grid-2">
                  <div class="form-group">
                    <label for="edit-customer-name">Name *</label>
                    <input 
                      id="edit-customer-name"
                      v-model="customerForm.name"
                      type="text"
                      placeholder="e.g., Sofia Mensah"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="edit-customer-email">Email *</label>
                    <input 
                      id="edit-customer-email"
                      v-model="customerForm.email"
                      type="email"
                      placeholder="e.g., sofia@email.com"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="edit-customer-phone">Phone *</label>
                    <input 
                      id="edit-customer-phone"
                      v-model="customerForm.phone"
                      type="tel"
                      placeholder="e.g., 030-111-2222"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="edit-customer-dob">Date of Birth *</label>
                    <input 
                      id="edit-customer-dob"
                      v-model="customerForm.dob"
                      type="date"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="edit-customer-type">Customer Type</label>
                    <select 
                      id="edit-customer-type"
                      v-model="customerForm.customerType"
                      class="form-input"
                    >
                      <option value="Normal">Normal</option>
                      <option value="VIP">VIP</option>
                    </select>
                  </div>

                  <div class="form-group" style="grid-column: 1 / -1">
                    <label for="edit-customer-address">Address</label>
                    <input 
                      id="edit-customer-address"
                      v-model="customerForm.address"
                      type="text"
                      placeholder="e.g., 14 Cantonments Rd"
                      class="form-input"
                    />
                  </div>

                  <div class="form-group" style="grid-column: 1 / -1">
                    <label for="edit-customer-preferences">Preferences</label>
                    <textarea 
                      id="edit-customer-preferences"
                      v-model="customerForm.preferences"
                      placeholder="e.g., Relaxing massage, No harsh chemicals, etc."
                      class="form-input"
                      style="resize: vertical; min-height: 60px"
                    ></textarea>
                  </div>
                </div>

                <div v-if="customerError" class="error-message">{{ customerError }}</div>
                <div v-if="customerSuccess" class="success-message">{{ customerSuccess }}</div>

                <div style="display: flex; gap: 12px; margin-top: 20px">
                  <button type="submit" class="btn btn-primary">
                    Update Customer
                  </button>
                  <button type="button" class="btn btn-outline" @click="cancelEditCustomer">
                    Cancel
                  </button>
                </div>
              </form>
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
              <h3 class="card-title">{{ isEditingStaff ? '✎ Edit Staff' : '➕ Add New Staff' }}</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="isEditingStaff ? handleUpdateStaff() : handleAddStaff()" style="max-width: 800px">
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
                    <label for="staff-dob">Date of Birth *</label>
                    <input
                      id="staff-dob"
                      v-model="staffForm.dob"
                      type="date"
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

                <div style="display: flex; gap: 12px; margin-top: 16px">
                  <button type="submit" class="btn btn-primary">
                    {{ isEditingStaff ? 'Update Staff' : 'Add Staff' }}
                  </button>
                  <button v-if="isEditingStaff" type="button" class="btn btn-outline" @click="cancelEditStaff">
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>

          <!-- Edit Staff Modal -->
          <div v-if="isEditingStaff" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000" @click.self="cancelEditStaff">
            <div style="background: white; border-radius: 12px; padding: 32px; max-width: 700px; width: 90%; max-height: 90vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0,0,0,0.3)">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px">
                <h2 style="margin: 0; font-size: 24px; font-weight: 600">✎ Edit Staff</h2>
                <button @click="cancelEditStaff" style="background: none; border: none; font-size: 24px; cursor: pointer; color: #999">✕</button>
              </div>

              <!-- Staff Info Display -->
              <div style="background: var(--light-bg); padding: 16px; border-radius: 8px; margin-bottom: 24px">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                  <div>
                    <div style="font-size: 12px; color: var(--text-muted); font-weight: 600; margin-bottom: 4px">DATE OF JOINING</div>
                    <div style="font-weight: 600">{{ editingStaffData?.doj || 'N/A' }}</div>
                  </div>
                  <div>
                    <div style="font-size: 12px; color: var(--text-muted); font-weight: 600; margin-bottom: 4px">DATE OF BIRTH</div>
                    <div style="font-weight: 600">{{ editingStaffData?.dob || 'N/A' }}</div>
                  </div>
                  <div>
                    <div style="font-size: 12px; color: var(--text-muted); font-weight: 600; margin-bottom: 4px">RATING</div>
                    <div style="font-weight: 600; color: var(--gold)">⭐ {{ editingStaffData?.rating || 'N/A' }}</div>
                  </div>
                  <div>
                    <div style="font-size: 12px; color: var(--text-muted); font-weight: 600; margin-bottom: 4px">REVIEWS</div>
                    <div style="font-weight: 600">{{ editingStaffData?.reviews || 0 }}</div>
                  </div>
                </div>
              </div>

              <!-- Edit Form -->
              <form @submit.prevent="handleUpdateStaff" style="margin-bottom: 20px">
                <div class="grid-2">
                  <div class="form-group">
                    <label for="edit-staff-name">Name *</label>
                    <input 
                      id="edit-staff-name"
                      v-model="staffForm.name"
                      type="text"
                      placeholder="e.g., Amara Osei"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="edit-staff-role">Role *</label>
                    <input 
                      id="edit-staff-role"
                      v-model="staffForm.role"
                      type="text"
                      placeholder="e.g., Senior Stylist"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="edit-staff-email">Email *</label>
                    <input 
                      id="edit-staff-email"
                      v-model="staffForm.email"
                      type="email"
                      placeholder="e.g., amara@glowsuite.com"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="edit-staff-phone">Phone *</label>
                    <input 
                      id="edit-staff-phone"
                      v-model="staffForm.phone"
                      type="tel"
                      placeholder="e.g., 050-111-2222"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group" style="grid-column: 1 / -1">
                    <label for="edit-staff-skills">Skills *</label>
                    <input 
                      id="edit-staff-skills"
                      v-model="staffForm.skills"
                      type="text"
                      placeholder="e.g., Hair Cutting, Styling, Coloring"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="edit-staff-dob">Date of Birth *</label>
                    <input
                      id="edit-staff-dob"
                      v-model="staffForm.dob"
                      type="date"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="edit-staff-doj">Date of Joining *</label>
                    <input 
                      id="edit-staff-doj"
                      v-model="staffForm.doj"
                      type="date"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="edit-staff-salary">Salary (₹) *</label>
                    <input 
                      id="edit-staff-salary"
                      v-model.number="staffForm.salary"
                      type="number"
                      placeholder="e.g., 2000"
                      class="form-input"
                      required
                      min="0"
                    />
                  </div>
                </div>

                <div v-if="staffError" class="error-message">{{ staffError }}</div>
                <div v-if="staffSuccess" class="success-message">{{ staffSuccess }}</div>

                <div style="display: flex; gap: 12px; margin-top: 20px">
                  <button type="submit" class="btn btn-primary">
                    Update Staff
                  </button>
                  <button type="button" class="btn btn-outline" @click="cancelEditStaff">
                    Cancel
                  </button>
                </div>
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
                      <th>Date of Birth</th>
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
                      <td>{{ staff.dob || '-' }}</td>
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

                  <div class="form-group">
                    <label for="product-supplier-contact">Supplier Contact *</label>
                    <input
                      id="product-supplier-contact"
                      v-model="inventoryForm.supplierContact"
                      type="text"
                      placeholder="e.g., +91-9876543210"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="product-supplier-email">Supplier Email *</label>
                    <input
                      id="product-supplier-email"
                      v-model="inventoryForm.supplierEmail"
                      type="email"
                      placeholder="e.g., supplier@company.com"
                      class="form-input"
                      required
                    />
                  </div>
                </div>

                <div style="display: flex; gap: 12px; margin-top: 16px">
                  <button type="submit" class="btn btn-primary" style="flex: 1">
                    Add Product
                  </button>
                </div>
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
                    <tr v-for="product in filteredProducts" :key="product.id" @click="viewProductDetails(product)" style="cursor: pointer">
                      <td>{{ product.name }}</td>
                      <td>{{ product.categoryName }}</td>
                      <td><span :class="['badge', product.stock <= product.minStock ? 'badge-red' : 'badge-green']">{{ product.stock }} {{ product.unit }}</span></td>
                      <td>{{ product.minStock }}</td>
                      <td>₹{{ product.costPrice }}</td>
                      <td class="text-muted">{{ product.supplier }}</td>
                      <td>
                        <div style="display: flex; gap: 6px">
                          <button class="btn btn-sm btn-outline" @click.stop="handleEditProduct(product)" style="padding: 4px 8px; font-size: 12px">
                            ✎ Edit
                          </button>
                          <button class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 12px; color: #e74c3c; border-color: #e74c3c" @click.stop="handleDeleteProduct(product.id)">
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
                      <td style="text-align: right; display: flex; justify-content: space-between; align-items: center">
                        <span>₹{{ overheadBillsTotal.toLocaleString() }}</span>
                        <button @click="openEditOverheadModal" class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 12px; margin-left: 12px">
                          ✏️ Edit
                        </button>
                      </td>
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
          <!-- REPLENISHMENT REQUESTS SECTION -->
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">🔄 Inventory Replenishment</h3>
            </div>
            <div class="card-body">
              <!-- Staff Replenishments -->
              <div style="margin-bottom: 24px">
                <h4 style="margin-bottom: 16px; font-weight: 600">📥 Staff Replenishments</h4>
                <!-- Date range filter -->
                <div style="margin-bottom: 16px; display: flex; gap: 12px; align-items: flex-end; flex-wrap: wrap">
                  <div>
                    <label style="font-size: 12px; color: var(--text-muted)">From Date</label>
                    <input 
                      v-model="managerTransactionDateFrom"
                      type="date" 
                      class="form-input"
                      style="width: 150px"
                    />
                  </div>
                  <div>
                    <label style="font-size: 12px; color: var(--text-muted)">To Date</label>
                    <input 
                      v-model="managerTransactionDateTo"
                      type="date" 
                      class="form-input"
                      style="width: 150px"
                    />
                  </div>
                  <button 
                    @click="fetchManagerInventoryTransactions" 
                    class="btn btn-primary"
                    style="padding: 8px 16px; font-size: 12px"
                  >
                    Filter
                  </button>
                  <button 
                    @click="managerTransactionDateFrom = ''; managerTransactionDateTo = ''; fetchManagerInventoryTransactions()"
                    class="btn btn-outline"
                    style="padding: 8px 16px; font-size: 12px; border-color: var(--border)"
                  >
                    Reset
                  </button>
                </div>

                <!-- Transaction Table -->
                <div v-if="staffOrderRequests.length === 0" class="empty-state">
                  <div class="empty-state-icon">📊</div>
                  <div class="empty-state-text">No staff orders found</div>
                </div>
                <div v-else class="table-wrap">
                  <table>
                    <thead>
                      <tr>
                        <th>Product</th>
                        <th>Quantity</th>
                        <th>Staff Name</th>
                        <th>Service</th>
                        <th>Date</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="txn in staffOrderRequests" :key="txn.txn_id">
                        <td><strong>{{ txn.product_name }}</strong></td>
                        <td>{{ txn.quantity }}</td>
                        <td>{{ getStaffName(txn.staff_id) || "Unknown" }}</td>
                        <td>{{ txn.service_name || "N/A" }}</td>
                        <td>{{ new Date(txn.date_of_txn).toLocaleDateString() }}</td>
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
                  <select v-model="replenishmentForm.productId" @change="handleReplenishmentProductSelect" id="replen-product" class="form-input" required>
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
                  <label for="replen-supplier">Supplier</label>
                  <input v-model="replenishmentForm.supplier" id="replen-supplier" type="text" class="form-input" placeholder="Auto-filled from product info" disabled style="background: var(--light-bg); color: #666; cursor: not-allowed" />
                  <small class="text-muted" style="font-size: 11px; margin-top: 4px">Auto-filled from product supplier information</small>
                </div>
                <div v-if="replenishmentError" class="error-message" style="margin-bottom: 12px">{{ replenishmentError }}</div>
                <button type="submit" class="btn btn-primary" style="width: 100%">+ Add to Order List</button>
              </form>

              <!-- Grouped Supplier Orders for Replenishment -->
              <div style="margin-top: 24px; padding-top: 24px; border-top: 2px solid var(--border)">
                <h4 style="margin-bottom: 16px; font-weight: 600">📦 Manager Replenishment Orders (Grouped by Supplier)</h4>
                <div v-if="groupedSupplierOrders.length === 0" class="empty-state">
                  <div class="empty-state-icon">📦</div>
                  <div class="empty-state-text">No manager replenishment orders</div>
                </div>
                <div v-else style="display: flex; flex-direction: column; gap: 20px">
                  <div v-for="(group, index) in groupedSupplierOrders" :key="index" style="border: 1px solid var(--border); border-radius: var(--radius); padding: 16px; background: var(--light-bg)">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px">
                      <h5 style="margin: 0; font-weight: 600">🏢 {{ group.supplier }}</h5>
                      <button @click="handlePlaceOrderToWholesale(group)" class="btn btn-primary" style="padding: 8px 16px; font-size: 12px">
                        📤 Place Order to Wholesale
                      </button>
                    </div>
                    <div class="table-wrap">
                      <table style="font-size: 13px">
                        <thead>
                          <tr>
                            <th>Product</th>
                            <th>Qty</th>
                            <th>Cost (₹)</th>
                            <th>Date</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="item in group.items" :key="item.txn_id">
                            <td><strong>{{ getProductName(item.product_id) }}</strong></td>
                            <td>{{ item.quantity }}</td>
                            <td><strong>₹{{ (item.quantity * (data.products.find(p => p.id === item.product_id)?.price || 0)).toFixed(2) }}</strong></td>
                            <td><small>{{ formatDate(item.date_of_txn) }}</small></td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </div>

              <!-- WHOLESALE SUPPLIER ORDERS SECTION -->
              <div style="margin-top: 32px; padding-top: 32px; border-top: 2px solid var(--border)">
                <h4 style="margin-bottom: 24px; font-weight: 600">🛒 Wholesale Orders Placed</h4>

                <!-- Orders Table -->
                <div v-if="managerOrders.length === 0" class="empty-state">
                  <div class="empty-state-icon">📮</div>
                  <div class="empty-state-text">No wholesale orders placed yet</div>
                </div>
                <div v-else class="table-wrap">
                  <table>
                    <thead>
                      <tr>
                        <th>Product</th>
                        <th>Quantity</th>
                        <th>Cost (₹)</th>
                        <th>Supplier</th>
                        <th>Reason</th>
                        <th>Status</th>
                        <th>Order Date</th>
                        <th>Replenishment Date</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="order in managerOrders" :key="order.order_id">
                        <td><strong>{{ order.product_name }}</strong></td>
                        <td>{{ order.order_quantity }}</td>
                        <td>₹{{ (order.order_quantity * (data.products.find(p => p.id === order.product_id)?.price || 0)).toFixed(2) }}</td>
                        <td><small>{{ order.supplier_name }}</small></td>
                        <td><small>{{ order.reason_for_order || '-' }}</small></td>
                        <td>
                          <span :style="{ 
                            padding: '4px 8px', 
                            borderRadius: '4px', 
                            fontSize: '11px', 
                            fontWeight: '600',
                            backgroundColor: getStatusColor(order.status).bg,
                            color: getStatusColor(order.status).text
                          }">
                            {{ getStatusLabel(order.status) }}
                          </span>
                        </td>
                        <td><small>{{ formatDate(order.order_date) }}</small></td>
                        <td><small>{{ order.order_replenishment_date ? formatDate(order.order_replenishment_date) : '-' }}</small></td>
                        <td style="display: flex; gap: 6px; flex-wrap: wrap">
                          <button v-if="order.status === 0" @click="handleMarkOrderDelivered(order)" class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 11px; color: #27ae60; border-color: #27ae60">✓ Delivered</button>
                          <button @click="openEditOrderModal(order)" class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 11px">✏️ Edit</button>
                          <button @click="handleDeleteOrder(order.order_id)" class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 11px; color: #e74c3c; border-color: #e74c3c">🗑️ Delete</button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Edit Order Modal -->
        <div v-if="showEditOrderModal && editingOrder" class="modal-overlay" @click.self="showEditOrderModal = false">
          <div class="modal">
            <div class="modal-header">
              <h4 class="modal-title">✏️ Edit Order</h4>
              <button type="button" class="close" @click="showEditOrderModal = false">&times;</button>
            </div>
            <div class="modal-body">
              <div v-if="editOrderError" class="error-message">{{ editOrderError }}</div>
              <form @submit.prevent="handleUpdateOrder">
                <div class="form-group">
                  <label>Product</label>
                  <input type="text" class="form-input" :value="editingOrder.product_name" disabled />
                </div>
                <div class="form-group">
                  <label>Quantity</label>
                  <input 
                    v-model.number="editOrderForm.quantity" 
                    type="number" 
                    min="1" 
                    class="form-input" 
                    required 
                  />
                </div>
                <div class="form-group">
                  <label>Cost (₹)</label>
                  <input 
                    type="text" 
                    class="form-input" 
                    :value="(editOrderForm.quantity * editingOrder.product_price).toFixed(2)" 
                    disabled 
                  />
                </div>
                <div class="form-group">
                  <label>Status</label>
                  <select v-model.number="editOrderForm.status" class="form-input">
                    <option :value="0">Pending</option>
                    <option :value="1">Processed</option>
                    <option :value="2">Cancelled</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Reason for Order</label>
                  <textarea 
                    v-model="editOrderForm.reason" 
                    class="form-input" 
                    rows="3"
                    placeholder="e.g., Low stock, seasonal demand..."
                  ></textarea>
                </div>
                <div class="form-group">
                  <label>Replenishment Date</label>
                  <input 
                    v-model="editOrderForm.replenishment_date" 
                    type="date" 
                    class="form-input"
                  />
                </div>
                <div style="display: flex; gap: 8px; margin-top: 16px">
                  <button type="submit" class="btn btn-primary">💾 Save Changes</button>
                  <button type="button" @click="showEditOrderModal = false" class="btn btn-secondary">Cancel</button>
                </div>
              </form>
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

          <!-- Stats Cards -->
          <div class="stat-grid">
            <div class="stat-card">
              <div class="stat-icon">📋</div>
              <div class="stat-value">{{ invoices.length }}</div>
              <div class="stat-label">Total Invoices</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">✅</div>
              <div class="stat-value">{{ invoices.filter(inv => inv.status === 1).length }}</div>
              <div class="stat-label">Completed</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">⏳</div>
              <div class="stat-value">{{ invoices.filter(inv => inv.status === 0).length }}</div>
              <div class="stat-label">Pending</div>
            </div>
          </div>

          <!-- Invoices Table -->
          <div class="card" style="margin-top: 24px">
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
              
              <div v-if="filteredInvoices.length === 0" class="empty-state">
                <div class="empty-state-icon">📄</div>
                <div class="empty-state-text">No invoices found</div>
              </div>
              
              <div v-else class="table-wrap" style="overflow-x: auto; width: 100%">
                <table style="min-width: 1000px; width: 100%">
                  <thead>
                    <tr>
                      <th style="min-width: 80px">Invoice #</th>
                      <th style="min-width: 120px">Customer</th>
                      <th style="min-width: 120px">Staff</th>
                      <th style="min-width: 150px">Services</th>
                      <th style="min-width: 100px">Amount (₹)</th>
                      <th style="min-width: 100px">Date</th>
                      <th style="min-width: 90px">Status</th>
                      <th style="min-width: 200px">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="invoice in filteredInvoices" :key="invoice.id">
                      <td><strong>{{ invoice.invoice_number }}</strong></td>
                      <td>{{ invoice.customer_name || getCustomerName(invoice.customer_id) }}</td>
                      <td>{{ invoice.staff_name || getStaffName(invoice.staff_id) }}</td>
                      <td><small>{{ invoice.service_descs || 'N/A' }}</small></td>
                      <td><strong>₹{{ invoice.total_charges?.toFixed(2) || 0 }}</strong></td>
                      <td><small>{{ new Date(invoice.invoice_date).toLocaleDateString() }}</small></td>
                      <td>
                        <span :style="{ 
                          padding: '4px 8px', 
                          borderRadius: '4px', 
                          fontSize: '11px', 
                          fontWeight: '600',
                          backgroundColor: invoice.status === 0 ? '#e8f5e9' : '#fff3cd',
                          color: invoice.status === 0 ? '#27ae60' : '#856404'
                        }">
                          {{ invoice.status === 0 ? 'Pending' : 'Completed' }}
                        </span>
                      </td>
                      <td>
                        <div style="display: flex; gap: 6px; flex-wrap: wrap">
                          <button @click="viewInvoice(invoice)" class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 11px">
                            📄 View
                          </button>
                          <button @click="handleSendInvoice(invoice)" class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 11px; color: #27ae60; border-color: #27ae60">
                            📧 Send
                          </button>
                          <button @click="handleDeleteInvoice(invoice.id)" class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 11px; color: #e74c3c; border-color: #e74c3c">
                            🗑️ Delete
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
                    <label for="points-per-currency">Points Per Currency (₹)</label>
                    <input 
                      id="points-per-currency"
                      v-model.number="rewardsForm.POINTS_PER_CURRENCY"
                      type="number"
                      step="0.01"
                      min="0"
                      placeholder="e.g., 0.1"
                      class="form-input"
                      required
                    />
                    <small class="text-muted">Points earned per rupee spent (e.g., 0.1 = 10 points for ₹100)</small>
                  </div>

                  <div class="form-group">
                    <label for="points-for-redemption">Points For Redemption</label>
                    <input 
                      id="points-for-redemption"
                      v-model.number="rewardsForm.POINTS_FOR_REDUMPTION"
                      type="number"
                      min="1"
                      placeholder="e.g., 500"
                      class="form-input"
                      required
                    />
                    <small class="text-muted">Points needed to redeem</small>
                  </div>

                  <div class="form-group">
                    <label for="redemption-value">Redemption Value Per Point (₹)</label>
                    <input 
                      id="redemption-value"
                      v-model.number="rewardsForm.REDUMPTION_VALUE_PER_POINT"
                      type="number"
                      step="0.01"
                      min="0"
                      placeholder="e.g., 0.05"
                      class="form-input"
                      required
                    />
                    <small class="text-muted">Rupees value per point (e.g., 0.05 = ₹25 for 500 points)</small>
                  </div>

                  <div class="form-group">
                    <label for="first-visit">First Visit Bonus Points</label>
                    <input 
                      id="first-visit"
                      v-model.number="rewardsForm.FIRST_VISIT_BONUS_POINTS"
                      type="number"
                      min="0"
                      placeholder="e.g., 20"
                      class="form-input"
                      required
                    />
                    <small class="text-muted">Bonus points for first-time customers</small>
                  </div>

                  <div class="form-group">
                    <label for="birthday-bonus">Birthday Bonus Points</label>
                    <input 
                      id="birthday-bonus"
                      v-model.number="rewardsForm.BIRTHDAY_BONUS_POINTS"
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
                      v-model.number="rewardsForm.VIP_DISCOUNT_PERCENTAGE"
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
                    <label for="reward-expiry">Reward Expiry (Days)</label>
                    <input 
                      id="reward-expiry"
                      v-model.number="rewardsForm.REWARD_EXPIRY_DAYS"
                      type="number"
                      min="1"
                      placeholder="e.g., 180"
                      class="form-input"
                      required
                    />
                    <small class="text-muted">Days until points expire</small>
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
                      <div class="stat-value">{{ (rewardsForm.POINTS_PER_CURRENCY * 100).toFixed(1) }} pts per ₹100</div>
                    </div>
                    <div class="stat-item">
                      <div class="stat-label">Redemption Rate</div>
                      <div class="stat-value">{{ rewardsForm.POINTS_FOR_REDUMPTION }} pts = ₹{{ (rewardsForm.POINTS_FOR_REDUMPTION * rewardsForm.REDUMPTION_VALUE_PER_POINT).toFixed(2) }}</div>
                    </div>
                    <div class="stat-item">
                      <div class="stat-label">VIP Discount</div>
                      <div class="stat-value">{{ rewardsForm.VIP_DISCOUNT_PERCENTAGE }}% discount</div>
                    </div>
                    <div class="stat-item">
                      <div class="stat-label">First Visit Points</div>
                      <div class="stat-value">{{ rewardsForm.FIRST_VISIT_BONUS_POINTS }} pts</div>
                    </div>
                    <div class="stat-item">
                      <div class="stat-label">Birthday Bonus</div>
                      <div class="stat-value">{{ rewardsForm.BIRTHDAY_BONUS_POINTS }} pts</div>
                    </div>
                    <div class="stat-item">
                      <div class="stat-label">Points Expiry</div>
                      <div class="stat-value">{{ rewardsForm.REWARD_EXPIRY_DAYS }} days</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- REPORTS VIEW -->
        <div v-if="currentView === 'reports'" class="fade-in">

          <!-- Analytics View (shown when a report type is selected) -->
          <div v-if="analyticsView">
            <!-- Back + header row -->
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
              <button class="btn btn-outline" style="padding: 6px 14px; font-size: 13px;" @click="analyticsView = null">
                ← Back to Reports
              </button>
              <h2 style="margin: 0; font-size: 18px; font-weight: 700; color: var(--charcoal);">
                {{ REPORT_ICONS[analyticsView.type] }} {{ analyticsView.title }} — {{ analyticsView.periodLabel }}
              </h2>
            </div>

            <!-- Loading -->
            <div v-if="analyticsLoading" style="text-align: center; padding: 40px; color: var(--text-muted);">
              <div style="font-size: 36px; margin-bottom: 12px;">📊</div>
              <div>Loading analytics…</div>
            </div>

            <!-- Error -->
            <div v-else-if="analyticsError" class="card" style="padding: 20px; color: #e53e3e;">
              ⚠️ {{ analyticsError }}
            </div>

            <template v-else-if="analyticsData">
              <!-- Summary stat cards -->
              <div class="stat-grid" style="margin-bottom: 20px;">
                <template v-if="analyticsView.type === 'appointments'">
                  <div class="stat-card"><div class="stat-icon">📅</div><div class="stat-value">{{ analyticsData.total }}</div><div class="stat-label">Total Appointments</div></div>
                  <div class="stat-card" v-for="s in analyticsData.by_status" :key="s.name"><div class="stat-icon">{{ s.name === 'Completed' ? '✅' : s.name === 'Cancelled' ? '❌' : '📌' }}</div><div class="stat-value">{{ s.value }}</div><div class="stat-label">{{ s.name }}</div></div>
                </template>
                <template v-else-if="analyticsView.type === 'sales'">
                  <div class="stat-card"><div class="stat-icon">💰</div><div class="stat-value">₹{{ analyticsData.total_revenue?.toLocaleString() }}</div><div class="stat-label">Total Revenue</div></div>
                  <div class="stat-card"><div class="stat-icon">🧾</div><div class="stat-value">{{ analyticsData.invoice_count }}</div><div class="stat-label">Invoices</div></div>
                  <div class="stat-card"><div class="stat-icon">📈</div><div class="stat-value">₹{{ analyticsData.invoice_count ? Math.round(analyticsData.total_revenue / analyticsData.invoice_count).toLocaleString() : 0 }}</div><div class="stat-label">Avg per Invoice</div></div>
                </template>
                <template v-else-if="analyticsView.type === 'inventory'">
                  <div class="stat-card"><div class="stat-icon">📦</div><div class="stat-value">{{ analyticsData.items?.length }}</div><div class="stat-label">Total Products</div></div>
                  <div class="stat-card"><div class="stat-icon">⚠️</div><div class="stat-value">{{ analyticsData.low_stock_count }}</div><div class="stat-label">Low Stock Alerts</div></div>
                </template>
                <template v-else-if="analyticsView.type === 'feedback'">
                  <div class="stat-card"><div class="stat-icon">⭐</div><div class="stat-value">{{ analyticsData.average }}</div><div class="stat-label">Avg Rating</div></div>
                  <div class="stat-card"><div class="stat-icon">📝</div><div class="stat-value">{{ analyticsData.total }}</div><div class="stat-label">Total Reviews</div></div>
                  <div class="stat-card" v-for="s in analyticsData.sentiment" :key="s.name"><div class="stat-icon">{{ s.name === 'Positive' ? '😊' : s.name === 'Neutral' ? '😐' : '😞' }}</div><div class="stat-value">{{ s.value }}</div><div class="stat-label">{{ s.name }}</div></div>
                </template>
              </div>

              <!-- Charts grid -->
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                <!-- Appointments: line chart by day + pie by status -->
                <template v-if="analyticsView.type === 'appointments'">
                  <div class="card">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Appointments Over Time</h3></div>
                    <div class="card-body" style="padding: 12px;"><canvas ref="chartLine" style="max-height: 220px;"></canvas></div>
                  </div>
                  <div class="card">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Top Services</h3></div>
                    <div class="card-body" style="padding: 12px;"><canvas ref="chartBar" style="max-height: 220px;"></canvas></div>
                  </div>
                  <div class="card" style="grid-column: 1 / -1;">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Status Breakdown</h3></div>
                    <div class="card-body" style="padding: 12px; display: flex; justify-content: center;"><canvas ref="chartPie" style="max-height: 260px; max-width: 380px;"></canvas></div>
                  </div>
                </template>

                <!-- Sales: revenue line + service bar -->
                <template v-else-if="analyticsView.type === 'sales'">
                  <div class="card">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Revenue Over Time (INR)</h3></div>
                    <div class="card-body" style="padding: 12px;"><canvas ref="chartLine" style="max-height: 220px;"></canvas></div>
                  </div>
                  <div class="card">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Revenue by Service</h3></div>
                    <div class="card-body" style="padding: 12px;"><canvas ref="chartBar" style="max-height: 220px;"></canvas></div>
                  </div>
                </template>

                <!-- Staff: bar chart -->
                <template v-else-if="analyticsView.type === 'staff'">
                  <div class="card" style="grid-column: 1 / -1;">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Appointments per Staff</h3></div>
                    <div class="card-body" style="padding: 12px;"><canvas ref="chartBar" style="max-height: 240px;"></canvas></div>
                  </div>
                  <div class="card" style="grid-column: 1 / -1;">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Staff Ratings</h3></div>
                    <div class="card-body" style="padding: 12px;"><canvas ref="chartLine" style="max-height: 200px;"></canvas></div>
                  </div>
                </template>

                <!-- Inventory: bar chart current vs min -->
                <template v-else-if="analyticsView.type === 'inventory'">
                  <div class="card" style="grid-column: 1 / -1;">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Stock Levels</h3></div>
                    <div class="card-body" style="padding: 12px;"><canvas ref="chartBar" style="max-height: 260px;"></canvas></div>
                  </div>
                </template>

                <!-- Feedback: rating bar + sentiment pie -->
                <template v-else-if="analyticsView.type === 'feedback'">
                  <div class="card">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Ratings Distribution</h3></div>
                    <div class="card-body" style="padding: 12px;"><canvas ref="chartBar" style="max-height: 220px;"></canvas></div>
                  </div>
                  <div class="card">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Sentiment Breakdown</h3></div>
                    <div class="card-body" style="padding: 12px; display: flex; justify-content: center;"><canvas ref="chartPie" style="max-height: 220px; max-width: 280px;"></canvas></div>
                  </div>
                </template>

                <!-- Financial: revenue vs profit line -->
                <template v-else-if="analyticsView.type === 'financial'">
                  <div class="card" style="grid-column: 1 / -1;">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Monthly Revenue vs Profit</h3></div>
                    <div class="card-body" style="padding: 12px;"><canvas ref="chartLine" style="max-height: 240px;"></canvas></div>
                  </div>
                </template>
              </div>

              <!-- Download + Share row -->
              <div class="card">
                <div class="card-body" style="display: flex; gap: 12px; flex-wrap: wrap; align-items: center;">
                  <button class="btn btn-primary" @click="downloadFromAnalytics('csv')" :disabled="quickLoading">
                    📥 Download CSV
                  </button>
                  <button class="btn btn-primary" @click="downloadFromAnalytics('pdf')" :disabled="quickLoading">
                    📄 Download PDF
                  </button>
                  <button
                    class="btn btn-outline"
                    @click="shareAnalyticsReport()"
                    :disabled="analyticsView.shared || analyticsView.sharing"
                    style="margin-left: auto;"
                  >
                    {{ analyticsView.shared ? '✓ Shared with Owner' : analyticsView.sharing ? '⏳ Sharing...' : '📤 Send to Owner' }}
                  </button>
                  <span v-if="shareMessage" style="font-size: 12px; color: #276749;">{{ shareMessage }}</span>
                </div>
              </div>
            </template>
          </div>

          <!-- Reports list view (default) -->
          <div v-else>
            <!-- ① AI Report Generator -->
            <div class="card" style="margin-bottom: 20px;">
              <div class="card-header" style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 18px;">🤖</span>
                <h3 class="card-title" style="margin: 0;">AI Report Generator</h3>
              </div>
              <div class="card-body">
                <p class="text-muted" style="font-size: 13px; margin-bottom: 12px;">
                  Describe the report you need in plain English and the AI will generate it instantly.
                </p>
                <div style="display: flex; gap: 8px; margin-bottom: 10px;">
                  <input
                    v-model="reportChatInput"
                    type="text"
                    class="form-input"
                    placeholder='e.g. "Generate weekly staff report" or "Monthly sales CSV"'
                    style="flex: 1; font-size: 13px;"
                    :disabled="reportChatLoading"
                    @keyup.enter="sendReportChatRequest"
                  />
                  <select v-model="reportChatFormat" class="form-input" style="width: 90px; font-size: 13px;">
                    <option value="csv">CSV</option>
                    <option value="pdf">PDF</option>
                  </select>
                  <button class="btn btn-primary" @click="sendReportChatRequest" :disabled="reportChatLoading || !reportChatInput.trim()" style="white-space: nowrap;">
                    <span v-if="reportChatLoading">⏳ Generating…</span>
                    <span v-else>✨ Generate</span>
                  </button>
                </div>
                <div v-if="reportChatMessage" :class="['report-ai-msg', reportChatError ? 'report-ai-msg--error' : 'report-ai-msg--success']">
                  {{ reportChatMessage }}
                </div>
              </div>
            </div>

            <!-- ② Report Cards Grid -->
            <div class="card" style="margin-bottom: 20px;">
              <div class="card-header">
                <h3 class="card-title">View & Export Reports</h3>
              </div>
              <div class="card-body">
                <!-- Period selector -->
                <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 16px; align-items: center;">
                  <label style="font-size: 13px; font-weight: 600; color: var(--text-muted);">Period:</label>
                  <select v-model="quickPeriod" class="form-input" style="font-size: 13px; width: 160px;">
                    <option value="daily">Today</option>
                    <option value="yesterday">Yesterday</option>
                    <option value="weekly">This Week</option>
                    <option value="monthly">This Month</option>
                    <option value="custom">Custom Range</option>
                  </select>
                  <template v-if="quickPeriod === 'custom'">
                    <input v-model="quickCustomStart" type="date" class="form-input" style="font-size: 13px; width: 150px;" />
                    <span style="color: var(--text-muted); font-size: 13px;">to</span>
                    <input v-model="quickCustomEnd" type="date" class="form-input" style="font-size: 13px; width: 150px;" />
                  </template>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px;">
                  <div v-for="rt in reportTypes" :key="rt.type" class="report-card">
                    <div class="report-card-icon">{{ rt.icon }}</div>
                    <div class="report-card-title">{{ rt.label }}</div>
                    <div class="report-card-desc">{{ rt.desc }}</div>
                    <div class="report-card-actions">
                      <button class="btn btn-outline" style="font-size: 12px; flex: 1;" @click="openAnalyticsView(rt)">
                        📊 View Analytics
                      </button>
                      <button class="btn btn-primary" style="font-size: 12px;" :disabled="quickLoading" @click="quickGenerateReportFor(rt.type, 'csv')">
                        CSV
                      </button>
                      <button class="btn btn-primary" style="font-size: 12px;" :disabled="quickLoading" @click="quickGenerateReportFor(rt.type, 'pdf')">
                        PDF
                      </button>
                    </div>
                  </div>
                </div>
                <div v-if="quickError" style="color: #e53e3e; font-size: 12px; margin-top: 10px;">⚠️ {{ quickError }}</div>
              </div>
            </div>

            <!-- ③ Saved & Shared Reports -->
            <div class="card">
              <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
                <h3 class="card-title">Saved Reports</h3>
                <button class="btn btn-outline" style="font-size: 12px; padding: 5px 12px;" @click="fetchSavedReports">↻ Refresh</button>
              </div>
              <div class="card-body">
                <div v-if="savedReports.length === 0" class="empty-state">
                  <div class="empty-state-icon">📄</div>
                  <div class="empty-state-text">No saved reports yet. Generate one above to see it here.</div>
                </div>
                <div v-else>
                  <div v-for="report in savedReports" :key="report.id" class="gen-report-item">
                    <div style="font-size: 22px;">{{ REPORT_ICONS[report.report_type] || '📄' }}</div>
                    <div style="flex: 1; min-width: 0;">
                      <div style="font-weight: 600; font-size: 14px; color: var(--charcoal);">
                        {{ report.report_type.charAt(0).toUpperCase() + report.report_type.slice(1) }} Report
                        <span v-if="report.shared" style="margin-left: 6px; font-size: 10px; background: #e6f4ea; color: #276749; padding: 1px 7px; border-radius: 10px; font-weight: 600;">Shared</span>
                      </div>
                      <div style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">
                        {{ REPORT_PERIOD_LABELS[report.time_period] || report.time_period }} &bull; {{ new Date(report.created_at).toLocaleDateString() }}
                      </div>
                    </div>
                    <div style="display: flex; gap: 6px; flex-shrink: 0; flex-wrap: wrap;">
                      <button v-if="report.has_csv" class="btn btn-outline" style="font-size: 11px; padding: 4px 10px;" @click="downloadSavedReport(report.id, 'csv')">CSV</button>
                      <button v-if="report.has_pdf" class="btn btn-outline" style="font-size: 11px; padding: 4px 10px;" @click="downloadSavedReport(report.id, 'pdf')">PDF</button>
                      <button v-if="!report.shared" class="btn btn-primary" style="font-size: 11px; padding: 4px 10px;" @click="shareReportWithOwner(report.id, report)">📤 Share</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Salon Settings View -->
        <div v-if="currentView === 'settings'" class="fade-in">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">⚙️ Salon Settings</h3>
            </div>
            <div class="card-body">
              <div v-if="filteredSalonConfig.length === 0" class="empty-state">
                <div class="empty-state-icon">⚙️</div>
                <div class="empty-state-text">No settings available</div>
              </div>
              <div v-else>
                <table style="width: 100%; border-collapse: collapse">
                  <thead>
                    <tr style="border-bottom: 2px solid var(--border)">
                      <th style="padding: 12px; text-align: left; font-weight: 600">Setting Name</th>
                      <th style="padding: 12px; text-align: left; font-weight: 600">Value</th>
                      <th style="padding: 12px; text-align: left; font-weight: 600">From Date</th>
                      <th style="padding: 12px; text-align: left; font-weight: 600">To Date</th>
                      <th style="padding: 12px; text-align: center; font-weight: 600">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="setting in filteredSalonConfig" :key="setting.setting_id" style="border-bottom: 1px solid var(--border)">
                      <td style="padding: 12px">{{ setting.param_name }}</td>
                      <td style="padding: 12px">{{ setting.param_value }}</td>
                      <td style="padding: 12px">{{ formatDate(setting.from_date) }}</td>
                      <td style="padding: 12px">{{ setting.to_date ? formatDate(setting.to_date) : 'N/A' }}</td>
                      <td style="padding: 12px; text-align: center">
                        <button class="btn btn-sm btn-outline" @click="handleEditSetting(setting)" style="padding: 4px 8px; font-size: 11px">
                          ✎ Edit
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
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
            <label for="profile-role">Role</label>
            <input 
              id="profile-role"
              v-model="profileEditForm.role" 
              type="text" 
              placeholder="Enter role"
              class="form-input"
            />
          </div>
          <div class="form-group">
            <label for="profile-doj">Date of Joining</label>
            <input 
              id="profile-doj"
              v-model="profileEditForm.doj" 
              type="date" 
              class="form-input"
            />
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

  <!-- Edit Overhead Bills Modal -->
  <div v-if="showEditOverheadModal" class="modal-overlay" @click="showEditOverheadModal = false">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3 class="modal-title">💵 Edit Overhead Bills</h3>
        <button class="modal-close" @click="showEditOverheadModal = false">✕</button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="handleUpdateOverhead">
          <div class="form-group">
            <label for="overhead-bills">Overhead Bills Amount (₹)</label>
            <input 
              id="overhead-bills"
              v-model.number="overheadEditForm.overheads" 
              type="number" 
              placeholder="Enter overhead bills amount"
              class="form-input"
              min="0"
              step="0.01"
              required
            />
          </div>
          <div style="display: flex; gap: 12px; margin-top: 20px">
            <button type="button" class="btn btn-outline" @click="showEditOverheadModal = false" style="flex: 1">
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

  <!-- Edit Appointment Modal -->
  <div v-if="showEditAppointmentModal && editingAppointment" class="modal-overlay" @click="closeEditAppointmentModal">
    <div class="modal-content" @click.stop style="max-width: 600px">
      <div class="modal-header">
        <h3 class="modal-title">✎ Edit Appointment</h3>
        <button class="modal-close" @click="closeEditAppointmentModal">✕</button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="handleSubmitEditAppointment">
          <div class="form-group" style="margin-bottom: 16px">
            <label style="font-weight: 600; display: block; margin-bottom: 8px">Customer</label>
            <input type="text" :value="getCustomerName(editingAppointment.customerId)" class="form-input" readonly style="background: #f5f5f5"/>
          </div>

          <div class="form-group" style="margin-bottom: 16px">
            <label style="font-weight: 600; display: block; margin-bottom: 8px">Select Services *</label>
            <div style="border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 12px; max-height: 200px; overflow-y: auto">
              <div v-for="service in data.services" :key="service.id" style="display: flex; align-items: center; margin-bottom: 12px">
                <input 
                  :id="'edit-service-' + service.id"
                  type="checkbox" 
                  :value="service.id" 
                  v-model="editAppointmentForm.serviceIds"
                  style="margin-right: 8px; width: 18px; height: 18px; cursor: pointer"
                />
                <label :for="'edit-service-' + service.id" style="cursor: pointer; flex: 1; margin: 0">
                  {{ service.name }} - ₹{{ service.price }}
                </label>
              </div>
            </div>
          </div>

          <div class="grid-2" style="gap: 16px; margin-bottom: 16px">
            <div class="form-group">
              <label for="edit-appt-date">Date * <span style="font-size: 12px; color: var(--text-muted); font-weight: 400">({{ editBookingDateInfo }})</span></label>
              <input 
                id="edit-appt-date"
                v-model="editAppointmentForm.date"
                type="date"
                class="form-input"
                :min="minEditBookingDate"
                :max="maxEditBookingDate"
                required
              />
            </div>

            <div class="form-group">
              <label for="edit-appt-time">Time *</label>
              <select 
                id="edit-appt-time"
                v-model="editAppointmentForm.time"
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

            <div class="form-group" style="grid-column: 1 / -1">
              <label for="edit-appt-staff">Stylist (Optional)</label>
              <select 
                id="edit-appt-staff"
                v-model="editAppointmentForm.staffId"
                class="form-input"
              >
                <option value="">Unassigned</option>
                <option 
                  v-for="staff in data.staff" 
                  :key="staff.id" 
                  :value="staff.id"
                >
                  {{ staff.name }}{{ staff.skills ? ' - ' + staff.skills : '' }}
                </option>
              </select>
            </div>
          </div>

          <div v-if="editAppointmentError" class="error-message">{{ editAppointmentError }}</div>
          <div v-if="editAppointmentSuccess" class="success-message">{{ editAppointmentSuccess }}</div>

          <div style="display: flex; gap: 12px; margin-top: 20px">
            <button type="button" class="btn btn-outline" @click="closeEditAppointmentModal" style="flex: 1">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" style="flex: 1">
              ✓ Save Changes
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
            <div style="position: relative">
              <input 
                id="financial-password"
                v-model="financialPasswordInput" 
                :type="showFinancePassword ? 'text' : 'password'" 
                placeholder="Enter password"
                class="form-input"
                required
                autofocus
              />
              <button
                type="button"
                @click="showFinancePassword = !showFinancePassword"
                style="position: absolute; right: 12px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; font-size: 18px; padding: 0; color: var(--text-muted)"
              >
                {{ showFinancePassword ? '👁️' : '👁️‍🗨️' }}
              </button>
            </div>
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
            <div style="position: relative">
              <input 
                id="reports-password"
                v-model="financialPasswordInput" 
                :type="showReportsPassword ? 'text' : 'password'" 
                placeholder="Enter password"
                class="form-input"
                required
                autofocus
              />
              <button
                type="button"
                @click="showReportsPassword = !showReportsPassword"
                style="position: absolute; right: 12px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; font-size: 18px; padding: 0; color: var(--text-muted)"
              >
                {{ showReportsPassword ? '👁️' : '👁️‍🗨️' }}
              </button>
            </div>
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
              <div style="font-size: 18px; font-weight: 600; color: var(--charcoal)">#{{ selectedInvoice.invoice_number }}</div>
            </div>
            <div>
              <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 4px">Invoice Date</div>
              <div style="font-size: 18px; font-weight: 600; color: var(--charcoal)">{{ selectedInvoice.invoice_date }}</div>
            </div>
          </div>
        </div>

        <div style="margin-bottom: 24px">
          <h4 style="font-size: 14px; font-weight: 600; color: var(--charcoal); margin-bottom: 12px">Customer Details</h4>
          <div style="display: grid; gap: 8px">
            <div style="display: grid; grid-template-columns: 140px 1fr">
              <span style="color: var(--text-muted)">Name:</span>
              <span style="font-weight: 500">{{ selectedInvoice.customer_name }}</span>
            </div>
            <div style="display: grid; grid-template-columns: 140px 1fr">
              <span style="color: var(--text-muted)">Email:</span>
              <span style="font-weight: 500">{{ data.customers.find(c => c.id === selectedInvoice.customer_id)?.email || '-' }}</span>
            </div>
            <div style="display: grid; grid-template-columns: 140px 1fr">
              <span style="color: var(--text-muted)">Phone:</span>
              <span style="font-weight: 500">{{ data.customers.find(c => c.id === selectedInvoice.customer_id)?.phone || '-' }}</span>
            </div>
          </div>
        </div>

        <div style="margin-bottom: 24px">
          <h4 style="font-size: 14px; font-weight: 600; color: var(--charcoal); margin-bottom: 12px">Service Details</h4>
          <div style="display: grid; gap: 8px">
            <div style="display: grid; grid-template-columns: 140px 1fr">
              <span style="color: var(--text-muted)">Services:</span>
              <span style="font-weight: 500">{{ selectedInvoice.service_descs || 'N/A' }}</span>
            </div>
            <div style="display: grid; grid-template-columns: 140px 1fr">
              <span style="color: var(--text-muted)">Staff:</span>
              <span style="font-weight: 500">{{ selectedInvoice.staff_name || 'Not Assigned' }}</span>
            </div>
          </div>
        </div>

        <div style="border-top: 2px solid var(--border-color); padding-top: 16px; margin-bottom: 20px">
          <div style="display: grid; grid-template-columns: 140px 1fr; gap: 12px; margin-bottom: 8px">
            <span style="color: var(--text-muted)">Subtotal:</span>
            <span style="text-align: right; font-weight: 500">₹{{ selectedInvoice.invoice_amount || getServicePrice(selectedInvoice.serviceId) }}</span>
          </div>
          <div style="display: grid; grid-template-columns: 140px 1fr; gap: 12px; margin-bottom: 8px" v-if="selectedInvoice.other_charges">
            <span style="color: var(--text-muted)">Other Charges:</span>
            <span style="text-align: right; font-weight: 500">₹{{ selectedInvoice.other_charges }}</span>
          </div>
          <div style="display: grid; grid-template-columns: 140px 1fr; gap: 12px; font-size: 14px; margin-bottom: 8px">
            <span style="color: var(--text-muted)">Total Amount:</span>
            <span style="text-align: right; font-weight: 600; color: var(--gold); font-size: 16px">₹{{ selectedInvoice.total_charges || selectedInvoice.invoice_amount || getServicePrice(selectedInvoice.serviceId) }}</span>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 140px 1fr">
          <span style="color: var(--text-muted)">Payment Method:</span>
          <span style="font-weight: 500; text-transform: capitalize">{{ selectedInvoice.paymentType || 'Cash' }}</span>
        </div>
        <div style="display: grid; grid-template-columns: 140px 1fr; margin-top: 8px">
          <span style="color: var(--text-muted)">Status:</span>
          <span :class="['badge', selectedInvoice.status === 1 ? 'badge-green' : 'badge-gold']">
            {{ selectedInvoice.status === 0 ? 'Pending' : selectedInvoice.status === 1 ? 'Invoiced' : 'Sent' }}
          </span>
        </div>

        <div v-if="selectedInvoice.rewards_earned > 0 || selectedInvoice.rewards_utilized > 0" style="margin-top: 20px; padding-top: 16px; border-top: 1px solid var(--border-color)">
          <h4 style="font-size: 14px; font-weight: 600; color: var(--charcoal); margin-bottom: 12px">Rewards Details</h4>
          <div style="display: grid; gap: 8px">
            <div style="display: grid; grid-template-columns: 140px 1fr" v-if="selectedInvoice.rewards_earned > 0">
              <span style="color: var(--text-muted)">Rewards Earned:</span>
              <span style="font-weight: 500; color: #27ae60">+{{ selectedInvoice.rewards_earned }} pts</span>
            </div>
            <div style="display: grid; grid-template-columns: 140px 1fr" v-if="selectedInvoice.rewards_utilized > 0">
              <span style="color: var(--text-muted)">Rewards Used:</span>
              <span style="font-weight: 500; color: #e74c3c">-{{ selectedInvoice.rewards_utilized }} pts</span>
            </div>
            <div style="display: grid; grid-template-columns: 140px 1fr">
              <span style="color: var(--text-muted)">Current Balance:</span>
              <span style="font-weight: 500">{{ selectedInvoice.current_reward_points }} pts</span>
            </div>
          </div>
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

  <!-- Edit Product Modal -->
  <div v-if="showEditProductModal" class="modal-overlay" @click.self="cancelEditProduct">
    <div class="modal-content" @click.stop style="max-width: 640px">
      <div class="modal-header">
        <h3 class="modal-title">✎ Edit Product</h3>
        <button class="modal-close" @click="cancelEditProduct">✕</button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="handleSaveEditProduct">
          <div class="form-group">
            <label for="edit-product-name">Product Name *</label>
            <input 
              id="edit-product-name"
              v-model="editProductForm.name"
              type="text"
              placeholder="e.g., L'Oreal Serum"
              class="form-input"
              required
            />
          </div>

          <div class="form-group">
            <label for="edit-product-category">Category *</label>
            <input 
              id="edit-product-category"
              v-model="editProductForm.categoryName"
              type="text"
              placeholder="e.g., Hair Care"
              class="form-input"
              required
            />
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px">
            <div class="form-group">
              <label for="edit-product-stock">Stock Quantity *</label>
              <input 
                id="edit-product-stock"
                v-model.number="editProductForm.stock"
                type="number"
                placeholder="e.g., 10"
                class="form-input"
                required
                min="0"
              />
            </div>

            <div class="form-group">
              <label for="edit-product-minstock">Minimum Stock *</label>
              <input 
                id="edit-product-minstock"
                v-model.number="editProductForm.minStock"
                type="number"
                placeholder="e.g., 5"
                class="form-input"
                required
                min="0"
              />
            </div>

            <div class="form-group">
              <label for="edit-product-costprice">Cost Price (₹) *</label>
              <input 
                id="edit-product-costprice"
                v-model.number="editProductForm.costPrice"
                type="number"
                placeholder="e.g., 45"
                class="form-input"
                required
                min="0"
              />
            </div>
          </div>

          <div class="form-group">
            <label for="edit-product-supplier">Supplier *</label>
            <input 
              id="edit-product-supplier"
              v-model="editProductForm.supplier"
              type="text"
              placeholder="e.g., BeautyPro Ltd"
              class="form-input"
              required
            />
          </div>

          <div class="form-group">
            <label for="edit-product-supplier-contact">Supplier Contact *</label>
            <input
              id="edit-product-supplier-contact"
              v-model="editProductForm.supplierContact"
              type="text"
              placeholder="e.g., +91-9876543210"
              class="form-input"
              required
            />
          </div>

          <div class="form-group">
            <label for="edit-product-supplier-email">Supplier Email *</label>
            <input
              id="edit-product-supplier-email"
              v-model="editProductForm.supplierEmail"
              type="email"
              placeholder="e.g., supplier@company.com"
              class="form-input"
              required
            />
          </div>

          <div v-if="editProductError" class="error-message">{{ editProductError }}</div>
          <div v-if="editProductSuccess" class="success-message">{{ editProductSuccess }}</div>

          <div style="display: flex; gap: 12px; margin-top: 20px">
            <button type="button" class="btn btn-outline" @click="cancelEditProduct" style="flex: 1">
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


  <div v-if="showProductDetailsModal && selectedProduct" class="modal-overlay" @click="showProductDetailsModal = false">
    <div class="modal-content" @click.stop style="max-width: 640px">
      <div class="modal-header">
        <h3 class="modal-title">📦 Product Details</h3>
        <button class="modal-close" @click="showProductDetailsModal = false">✕</button>
      </div>
      <div class="modal-body">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px">
          <div><strong>Name:</strong> {{ selectedProduct.name || '-' }}</div>
          <div><strong>Category:</strong> {{ selectedProduct.categoryName || '-' }}</div>
          <div><strong>Stock:</strong> {{ selectedProduct.stock ?? '-' }} {{ selectedProduct.unit || '' }}</div>
          <div><strong>Min Stock:</strong> {{ selectedProduct.minStock ?? '-' }}</div>
          <div><strong>Cost Price:</strong> ₹{{ selectedProduct.costPrice ?? '-' }}</div>
          <div><strong>Supplier:</strong> {{ selectedProduct.supplier || '-' }}</div>
          <div><strong>Supplier Contact:</strong> {{ selectedProduct.supplierContact || '-' }}</div>
          <div style="grid-column: 1 / -1"><strong>Supplier Email:</strong> {{ selectedProduct.supplierEmail || '-' }}</div>
        </div>
        <div style="display: flex; justify-content: flex-end; margin-top: 20px">
          <button class="btn btn-outline" @click="showProductDetailsModal = false">Close</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Edit Salon Setting Modal -->
  <div v-if="showEditSettingModal" class="modal-overlay" @click="showEditSettingModal = false">
    <div class="modal-content" @click.stop style="max-width: 500px">
      <div class="modal-header">
        <h3 class="modal-title">⚙️ Edit Setting</h3>
        <button class="modal-close" @click="showEditSettingModal = false">✕</button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="handleSaveSetting">
          <div class="form-group">
            <label>Setting Name</label>
            <input 
              :value="editSettingForm.param_name"
              type="text" 
              class="form-input" 
              disabled
            />
          </div>
          <div class="form-group">
            <label for="setting-value">Value</label>
            <input 
              id="setting-value"
              v-model="editSettingForm.param_value"
              type="text" 
              placeholder="Enter setting value"
              class="form-input"
              required
            />
          </div>
          <div class="form-group">
            <label for="setting-from-date">From Date</label>
            <input 
              id="setting-from-date"
              v-model="editSettingForm.from_date"
              type="date" 
              class="form-input"
            />
          </div>
          <div class="form-group">
            <label for="setting-to-date">To Date</label>
            <input 
              id="setting-to-date"
              v-model="editSettingForm.to_date"
              type="date" 
              class="form-input"
            />
          </div>
          <div v-if="settingError" class="error-message">{{ settingError }}</div>
          <div v-if="settingSuccess" class="success-message">{{ settingSuccess }}</div>
          <div style="display: flex; gap: 12px; margin-top: 20px">
            <button type="button" class="btn btn-outline" @click="showEditSettingModal = false" style="flex: 1">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" style="flex: 1">
              Save Setting
            </button>
          </div>
        </form>
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
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from "vue";
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);
import { useRouter } from "vue-router";
import { useAppStore } from "@/stores/appStore";

const router = useRouter();
const appStore = useAppStore();
const API_BASE_URL = "http://localhost:5000";

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
  role: '',
  doj: ''
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
const showFinancePassword = ref(false);
const showReportsPassword = ref(false);
const financeAuthenticated = ref(false);
const reportsAuthenticated = ref(false);
const pendingFinancialView = ref(null); // Track which view user tried to access

// Finance data state
const financeData = ref(null);
const financeLoading = ref(false);
const financeError = ref(null);
const showEditOverheadModal = ref(false);
const overheadEditForm = ref({
  overheads: 0
});

// AI Daily Briefing state
const briefingData = ref(null);
const briefingLoading = ref(false);
const briefingError = ref(null);
const briefingDismissed = ref(false);

// AI Assistant state
const showAIAssistant = ref(false);
const aiMessages = ref([
  { type: 'assistant', text: 'Hi! I\'m your AI Assistant. I\'m here to help you manage appointments, customers, services, staff, packages, and resolve any issues. Try asking me to "Create a task checklist for today"!' }
]);
const aiUserInput = ref('');

// Manager Task Checklist state
const managerTasks = ref([]);
const tasksLoading = ref(false);
const tasksError = ref(null);
const pendingTasks = computed(() => managerTasks.value.filter(t => t.status === 'pending'));
const completedTasks = computed(() => managerTasks.value.filter(t => t.status === 'completed'));

// ── Report Generation state ────────────────────────────────────────────────
// AI chat path
const reportChatInput   = ref('');
const reportChatFormat  = ref('csv');
const reportChatLoading = ref(false);
const reportChatMessage = ref('');
const reportChatError   = ref(false);

// Quick-generate path
const quickType        = ref('sales');
const quickPeriod      = ref('monthly');
const quickFormat      = ref('csv');
const quickCustomStart = ref('');
const quickCustomEnd   = ref('');
const quickLoading     = ref(false);
const quickError       = ref('');

// Session report history (blobs kept in memory)
const generatedReports = ref([]);
const _reportBlobs     = new Map();  // id → Blob

const REPORT_ICONS = {
  sales: '📊', appointments: '📅', staff: '👥',
  inventory: '📦', financial: '💰', feedback: '⭐',
};
const REPORT_PERIOD_LABELS = {
  daily: 'Today', yesterday: 'Yesterday', weekly: 'This Week',
  monthly: 'This Month', custom: 'Custom Range',
};

// Report type catalogue shown in the cards grid
const reportTypes = [
  { type: 'sales',        icon: '📊', label: 'Sales Report',        desc: 'Total revenue, invoices & top services'          },
  { type: 'appointments', icon: '📅', label: 'Appointments Report',  desc: 'Booking trends, status breakdown & top services' },
  { type: 'staff',        icon: '👥', label: 'Staff Report',         desc: 'Performance, attendance & ratings'               },
  { type: 'inventory',    icon: '📦', label: 'Inventory Report',     desc: 'Stock levels, usage & low-stock alerts'          },
  { type: 'financial',    icon: '💰', label: 'Financial Report',     desc: 'Revenue, expenses & profit by month'             },
  { type: 'feedback',     icon: '⭐', label: 'Feedback Report',      desc: 'Customer ratings & sentiment summary'            },
];

// ── Analytics view state ──────────────────────────────────────────────────
const analyticsView    = ref(null);   // { type, title, icon, periodLabel, dbId, shared }
const analyticsData    = ref(null);
const analyticsLoading = ref(false);
const analyticsError   = ref(null);
const savedReports     = ref([]);
const shareMessage     = ref('');

// Chart.js canvas refs
const chartLine = ref(null);
const chartBar  = ref(null);
const chartPie  = ref(null);

// Keep Chart instances so we can destroy before re-render
let _chartLineInst = null;
let _chartBarInst  = null;
let _chartPieInst  = null;

// Booking form state
const bookingForm = ref({
  customerId: "",
  serviceIds: [],
  date: "",
  time: "",
  staffId: "",
  appointmentId: null
});
const bookingError = ref("");
const bookingSuccess = ref("");

// Appointment Edit Modal state
const showEditAppointmentModal = ref(false);
const editingAppointment = ref(null);
const editAppointmentForm = ref({
  serviceIds: [],
  date: "",
  time: "",
  staffId: ""
});
const editAppointmentError = ref("");
const editAppointmentSuccess = ref("");

// Service form state
const serviceForm = ref({
  name: "",
  categoryId: "",
  price: 0,
  duration: 0,
  productsRequired: "",
  fromDate: "",
  toDate: ""
});
const isEditingService = ref(false);
const editingServiceId = ref(null);
const editingServiceData = ref(null);
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
const isEditingCustomer = ref(false);
const editingCustomerId = ref(null);
const editingCustomerData = ref(null);
const customerError = ref("");
const customerSuccess = ref("");

// Staff form state
const staffForm = ref({
  name: "",
  role: "",
  email: "",
  phone: "",
  skills: "",
  dob: "",
  doj: "",
  salary: 0,
  username: ""
});
const isEditingStaff = ref(false);
const editingStaffId = ref(null);
const editingStaffData = ref(null);
const staffError = ref("");
const staffSuccess = ref("");

// Invoice form state
const invoiceForm = ref({
  appointmentId: "",
  customerId: "",
  staffId: "",
  serviceId: "",
  date: "",
  paymentType: "cash",
  discount: 0,
  services: [],
  amount: 0,
  customerName: "",
  staffName: "",
  serviceNames: ""
});
const invoiceError = ref("");
const invoiceSuccess = ref("");
const invoices = ref([]);
const todaysAppointmentsForInvoice = ref([]);
const quickAppointmentForm = ref({
  customerId: "",
  serviceIds: [],
  time: "",
  staffId: ""
});
const quickAppointmentError = ref("");
const quickAppointmentSuccess = ref("");

// Inventory/Product form state
const inventoryForm = ref({
  name: "",
  categoryName: "",
  stock: 0,
  minStock: 0,
  costPrice: 0,
  supplier: "",
  supplierContact: "",
  supplierEmail: ""
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

// Product editing state
const showEditProductModal = ref(false);
const editProductForm = ref({
  name: "",
  categoryName: "",
  stock: 0,
  minStock: 0,
  costPrice: 0,
  supplier: "",
  supplierContact: "",
  supplierEmail: ""
});
const editingProductId = ref(null);
const editProductError = ref("");
const editProductSuccess = ref("");



// Staff bookings modal state
const showStaffBookingsModal = ref(false);
const selectedStaffForBookings = ref(null);

// Customer visits modal state
const showCustomerVisitsModal = ref(false);
const selectedCustomerForVisits = ref(null);

// Invoice modal state
const showInvoiceModal = ref(false);
const selectedInvoice = ref(null);
const showProductDetailsModal = ref(false);
const selectedProduct = ref(null);

// Order Tab & Replenishment
const orderTab = ref("pending-orders");
const replenishmentForm = ref({
  productId: "",
  quantity: 1,
  reason: "",
  supplier: ""
});
const replenishmentError = ref("");
const pendingReplenishmentList = ref([]);
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
  POINTS_PER_CURRENCY: 0.1,
  POINTS_FOR_REDUMPTION: 500,
  REDUMPTION_VALUE_PER_POINT: 0.05,
  FIRST_VISIT_BONUS_POINTS: 20,
  BIRTHDAY_BONUS_POINTS: 50,
  VIP_DISCOUNT_PERCENTAGE: 15,
  REWARD_EXPIRY_DAYS: 180
});
const rewardsError = ref("");
const rewardsSuccess = ref("");

// Salon Config state
const salonConfigList = ref([]);
const showEditSettingModal = ref(false);
const editingSettingData = ref(null);
const editSettingForm = ref({
  param_name: "",
  param_value: "",
  from_date: "",
  to_date: ""
});
const settingError = ref("");
const settingSuccess = ref("");

// Store manager profile data fetched from backend
const managerProfileData = ref(null);

const user = computed(() => {
  const currentUser = appStore.user;
  if (!currentUser) {
    return {
      name: "Manager",
      userId: "manager",
      role: "manager"
    };
  }
  // Display manager name from backend profile data if available
  return {
    name: managerProfileData.value?.manager_name || currentUser.username || "Manager",
    userId: currentUser.username || "manager",
    role: currentUser.role || "manager"
  };
});
const data = computed(() => appStore.data);

// Attendance API integration for manager
const fetchedAttendance = ref([]);
const attendanceLoading = ref(false);
const attendanceError = ref("");

// Daily appointment count for salon
const dailyAppointmentCounts = ref([]);
const dailyCountLoading = ref(false);
const dailyCountError = ref("");

// Manager inventory transaction tracking
const managerInventoryTransactions = ref([]);
const managerTransactionDateFrom = ref("");
const managerTransactionDateTo = ref("");

// Manager wholesale orders tracking
const managerOrders = ref([]);

// Edit order modal state
const showEditOrderModal = ref(false);
const editingOrder = ref(null);
const editOrderForm = ref({
  status: 0,
  quantity: 1,
  reason: "",
  replenishment_date: ""
});
const editOrderError = ref("");

const fetchManagerAttendance = async () => {
  attendanceLoading.value = true;
  attendanceError.value = "";
  
  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      attendanceError.value = "Not authenticated";
      attendanceLoading.value = false;
      return;
    }

    // Get today's attendance (backend defaults to today when no date param provided)
    const response = await fetch(
      `${API_BASE_URL}/api/manager-staff-attendance`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
          "Authentication-Token": token
        }
      }
    );

    if (response.ok) {
      const attendanceData = await response.json();
      const mappedAttendance = attendanceData.map(record => ({
        staffId: record.staff_id,
        date: new Date(record.register_datetime).toISOString().split('T')[0],
        status: "present" // Marking means present
      }));
      fetchedAttendance.value = mappedAttendance;
      // Update the main data store with fetched attendance
      data.value.attendance = mappedAttendance;
      console.log("Manager attendance loaded:", fetchedAttendance.value);
    } else if (response.status === 404) {
      fetchedAttendance.value = [];
      data.value.attendance = [];
    } else {
      attendanceError.value = "Failed to load attendance data";
    }
  } catch (error) {
    console.error("Error fetching attendance:", error);
    attendanceError.value = "Error loading attendance";
  } finally {
    attendanceLoading.value = false;
  }
};

// Fetch daywise appointment counts for the salon
const fetchDailyAppointmentCounts = async () => {
  dailyCountLoading.value = true;
  dailyCountError.value = "";
  
  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      dailyCountError.value = "Not authenticated";
      dailyCountLoading.value = false;
      return;
    }

    const response = await fetch(
      `${API_BASE_URL}/api/daily-appointment-count`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
          "Authentication-Token": token
        }
      }
    );

    console.log("Daily appointment count response status:", response.status);

    if (response.ok) {
      const data = await response.json();
      dailyAppointmentCounts.value = data;
      console.log("Daily appointment counts loaded:", dailyAppointmentCounts.value);
    } else if (response.status === 404) {
      dailyAppointmentCounts.value = [];
      console.log("No appointment count data found");
    } else if (response.status === 403) {
      dailyCountError.value = "You don't have permission to view appointment counts";
      console.error("Access denied - likely not a manager");
      dailyAppointmentCounts.value = [];
    } else {
      const errorData = await response.json().catch(() => ({}));
      dailyCountError.value = errorData.message || "Failed to load daily appointment counts";
      console.error("Error response:", response.status, errorData);
    }
  } catch (error) {
    console.error("Error fetching daily counts:", error);
    dailyCountError.value = "Error loading daily appointment counts";
  } finally {
    dailyCountLoading.value = false;
  }
};

const today = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
};

// Fetch today's appointments from dedicated endpoint for invoice creation
const fetchTodaysAppointmentsForInvoice = async () => {
  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      console.error("Not authenticated for today's appointments");
      return;
    }

    const response = await fetch(
      `${API_BASE_URL}/api/todays-appointments`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
          "Authentication-Token": token
        }
      }
    );

    if (response.ok) {
      const todaysAppts = await response.json();
      if (Array.isArray(todaysAppts) && todaysAppts.length > 0) {
        // Map today's appointments to frontend format for easier invoice creation
        const mappedTodayAppts = todaysAppts.map(appt => ({
          id: appt.appointment_id,
          customerId: appt.customer_id,
          customer_name: appt.customer_name,
          staffId: appt.staff_id,
          staff_name: appt.staff_name,
          date: new Date(appt.datetime).toISOString().split('T')[0],
          datetime: appt.datetime,
          time: new Date(appt.datetime).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true }),
          services: appt.services || [],
          status: "confirmed",
          invoiceStatus: "pending"
        }));
        todaysAppointmentsForInvoice.value = mappedTodayAppts;
        console.log("Today's appointments fetched for invoice creation:", mappedTodayAppts);
      } else {
        todaysAppointmentsForInvoice.value = [];
      }
    }
  } catch (error) {
    console.error("Error fetching today's appointments:", error);
  }
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
  // Use fetched attendance data from API if available, otherwise use mock data
  const attendanceData = fetchedAttendance.value.length > 0 ? fetchedAttendance.value : data.value.attendance;
  
  return data.value.staff.filter(staff => {
    const isPresent = attendanceData.find(
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

// Check if bridal package is selected in edit form
const hasBridalPackageSelectedInEdit = () => {
  return editAppointmentForm.value.serviceIds.some(serviceId => {
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
    // Allow booking today for managers
    minDate.setDate(minDate.getDate()); // Today for normal services
  }
  
  return minDate.toISOString().split('T')[0];
});

// Compute minimum booking date (6 months for bridal, 3 days for others - today through 2 days out)
const maxBookingDate = computed(() => {
  const today = new Date();
  const maxDate = new Date(today);
  
  if (hasBridalPackageSelected()) {
    maxDate.setMonth(maxDate.getMonth() + 6); // 6 months for bridal package
  } else {
    maxDate.setDate(maxDate.getDate() + 2); // 2 days from today for other services
  }
  
  return maxDate.toISOString().split('T')[0];
});

// Edit appointment date constraints (same rules as create)
const minEditBookingDate = computed(() => {
  const today = new Date();
  const minDate = new Date(today);
  
  if (hasBridalPackageSelectedInEdit()) {
    minDate.setMonth(minDate.getMonth() + 1); // 1 month for bridal package
  } else {
    // Allow booking today for managers
    minDate.setDate(minDate.getDate()); // Today for normal services
  }
  
  return minDate.toISOString().split('T')[0];
});

// Compute maximum edit booking date (6 months for bridal, 2 days for others)
const maxEditBookingDate = computed(() => {
  const today = new Date();
  const maxDate = new Date(today);
  
  if (hasBridalPackageSelectedInEdit()) {
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
    return `Other services: Book today or within next 2 days`;
  }
});

// Helper text for edit appointment date info
const editBookingDateInfo = computed(() => {
  if (editAppointmentForm.value.serviceIds.length === 0) {
    return "Select a service to see available booking dates";
  }
  
  if (hasBridalPackageSelectedInEdit()) {
    return `Bridal Package: Book 1 to 6 months in advance`;
  } else {
    return `Other services: Book today or within next 2 days`;
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
    settings: "Salon Settings"
  };
  return titles[currentView.value] || "Dashboard";
});

const invoicedAppointments = computed(() => {
  return data.value.appointments.filter(a => a.invoiceStatus === "invoiced");
});

const pendingInvoices = computed(() => {
  return data.value.appointments.filter(a => a.invoiceStatus === "pending");
});

const staffOrderRequests = computed(() => {
  return managerInventoryTransactions.value.filter(txn => txn.txn_type === 0);
});

const managerReplenishmentOrders = computed(() => {
  const replenishments = managerInventoryTransactions.value.filter(txn => txn.txn_type === 1);
  // Filter out replenishment orders that already have wholesale orders placed
  const placedProductIds = new Set(managerOrders.value.map(order => order.product_id));
  return replenishments.filter(txn => !placedProductIds.has(txn.product_id));
});

const groupedSupplierOrders = computed(() => {
  const grouped = {};
  managerReplenishmentOrders.value.forEach(order => {
    const supplier = getProductSupplier(order.product_id);
    if (!grouped[supplier]) {
      grouped[supplier] = {
        supplier: supplier,
        items: []
      };
    }
    grouped[supplier].items.push(order);
  });
  return Object.values(grouped);
});

const totalRevenue = computed(() => {
  if (financeData.value?.total_revenue !== undefined) {
    return "₹" + financeData.value.total_revenue.toLocaleString();
  }
  return "₹0";
});

const totalProductCost = computed(() => {
  return financeData.value?.total_revenue || 0;
});

const productInventoryCost = computed(() => {
  return financeData.value?.product_cost || 0;
});

const netProfit = computed(() => {
  if (financeData.value?.net_profit !== undefined) {
    return "₹" + financeData.value.net_profit.toLocaleString();
  }
  return "₹0";
});

const staffSalaryTotal = computed(() => {
  return financeData.value?.staff_salary || 0;
});

const serviceCommissionTotal = computed(() => {
  return Math.round((financeData.value?.total_revenue || 0) * 0.05); // 5% commission on services
});

const overheadBillsTotal = computed(() => {
  return financeData.value?.overheads || 0;
});

const calculatedNetProfit = computed(() => {
  return financeData.value?.net_profit || 0;
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
  
  // Start from today and go for next 7 days
  for (let i = 0; i < 7; i++) {
    const date = new Date(today);
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
  // Show all appointments (past and future)
  return data.value.appointments;
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

const selectedBookingCustomer = computed(() => {
  return data.value.customers.find(c => String(c.id) === bookingForm.value.customerId) || null;
});

const filteredProducts = computed(() => {
  if (!productName.value.trim()) return data.value.products;
  return data.value.products.filter(p => 
    p.name.toLowerCase().includes(productName.value.toLowerCase()) ||
    p.categoryName.toLowerCase().includes(productName.value.toLowerCase())
  );
});

const filteredInvoices = computed(() => {
  if (!invoiceCustomerName.value.trim()) return invoices.value;
  return invoices.value.filter(inv => {
    const customerNameStr = inv.customer_name ? inv.customer_name.toLowerCase() : getCustomerName(inv.customer_id).toLowerCase();
    return customerNameStr.includes(invoiceCustomerName.value.toLowerCase());
  });
});

const filteredBookings = computed(() => {
  if (!bookingCustomerName.value.trim()) return displayedBookings.value;
  return displayedBookings.value.filter(appt => {
    const customerNameStr = getCustomerName(appt.customerId).toLowerCase();
    const customerEmailStr = getCustomerEmail(appt.customerId).toLowerCase();
    const searchTerm = bookingCustomerName.value.toLowerCase();
    return customerNameStr.includes(searchTerm) || customerEmailStr.includes(searchTerm);
  });
});

// Filter out reward-related settings from salon config display (they're in Rewards tab)
const filteredSalonConfig = computed(() => {
  const rewardFields = [
    "REWARD_EXPIRY_DAYS",
    "POINTS_PER_CURRENCY",
    "POINTS_FOR_REDUMPTION",
    "REDUMPTION_VALUE_PER_POINT",
    "FIRST_VISIT_BONUS_POINTS",
    "BIRTHDAY_BONUS_POINTS",
    "VIP_DISCOUNT_PERCENTAGE"
  ];
  return salonConfigList.value.filter(config => !rewardFields.includes(config.param_name));
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
    const customerEmailStr = getCustomerEmail(appt.customerId).toLowerCase();
    const staffNameStr = (getStaffName(appt.staffId) || "Unassigned").toLowerCase();
    const serviceNameStr = getServiceName(appt.serviceId).toLowerCase();
    const searchTerm = completedAppointmentFilter.value.toLowerCase();
    return customerNameStr.includes(searchTerm) || 
           customerEmailStr.includes(searchTerm) ||
           staffNameStr.includes(searchTerm) || 
           serviceNameStr.includes(searchTerm);
  });
});

// Helper functions
const getCustomerName = (id) => {
  const customerId = parseInt(id) || id;
  return data.value.customers.find(c => c.id === customerId || String(c.id) === String(id))?.name || "Unknown";
};

const getCustomerEmail = (id) => {
  const customerId = parseInt(id) || id;
  return data.value.customers.find(c => c.id === customerId || String(c.id) === String(id))?.email || "";
};

const getServiceName = (id) => {
  return data.value.services.find(s => s.id === id)?.name || "Unknown";
};

const getServicePrice = (id) => {
  return data.value.services.find(s => s.id === id)?.price || 0;
};

// Get service name from appointment (handles both serviceId and services array)
const getAppointmentServiceName = (appt) => {
  if (appt.services && appt.services.length > 0) {
    // Show all services, not just the first one
    // Try different field names: name, service_desc, service_name
    const serviceNames = appt.services.map(s => {
      console.log("Service object:", s);
      return s.name || s.service_desc || s.service_name || "Service";
    }).join(', ');
    console.log("Service names for appt", appt.id, ":", serviceNames);
    return serviceNames;
  } else if (appt.serviceId) {
    return getServiceName(appt.serviceId);
  }
  console.log("No services for appt", appt.id, "services:", appt.services, "serviceId:", appt.serviceId);
  return "Unknown";
};

const getStaffName = (id) => {
  return data.value.staff.find(s => s.id === id)?.name || null;
};

const getCategoryName = (id) => {
  return data.value.serviceCategories.find(c => c.id === id)?.name || "Unknown";
};

const getServiceStatus = (service) => {
  // Check if service is disabled
  if (service.active === false || service.active_flg === false) {
    return "Disabled";
  }
  
  // Check if service date has passed
  if (!service.toDate) return "Active";
  const today = new Date().toISOString().split('T')[0];
  return service.toDate < today ? "Inactive" : "Active";
};

const getProductNameForOrder = (id) => {
  return data.value.products.find(p => p.id === id)?.name || "Unknown";
};

const getProductName = (id) => {
  return data.value.products.find(p => p.id === id)?.name || "Unknown";
};

const getProductSupplier = (id) => {
  return data.value.products.find(p => p.id === id)?.supplier || "Unknown";
};

const getStaffAttendance = (staffId) => {
  const att = data.value.attendance.find(a => a.staffId === staffId && a.date === today());
  return att?.status || "not marked";
};

const getStaffAppointments = (staffId) => {
  return data.value.appointments.filter(a => a.staffId === staffId && a.date === today()).length;
};

const getTimeFromDate = (datetimeStr) => {
  if (!datetimeStr) return "N/A";
  try {
    // Extract time from ISO datetime format (YYYY-MM-DDTHH:MM:SS)
    const timePart = datetimeStr.split('T')[1];
    if (!timePart) return "N/A";
    const [hours, minutes] = timePart.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour % 12 || 12;
    return `${displayHour}:${minutes} ${ampm}`;
  } catch (e) {
    console.error("Error parsing datetime:", datetimeStr, e);
    return "N/A";
  }
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

const handleChangePassword = async () => {
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

const openProfileEdit = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const userId = appStore.user?.id;
    
    if (!token || !userId) {
      alert('User information not found. Please login again.');
      return;
    }

    // Fetch current manager's data using userId
    const response = await fetch(`${API_BASE_URL}/api/manager/${userId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': token,
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.ok) {
      const manager = await response.json();
      console.log('Current manager data:', manager);
      
      // Parse dates properly - handle both "YYYY-MM-DD HH:MM:SS" and "YYYY-MM-DDTHH:MM:SS" formats
      const parseDateString = (dateString) => {
        if (!dateString) return '';
        // Remove time portion by taking only the first 10 characters (YYYY-MM-DD)
        return dateString.substring(0, 10);
      };

      profileEditForm.value = {
        name: manager.manager_name || '',
        email: manager.manager_email || '',
        phone: manager.manager_contact || '',
        role: manager.manager_role || '',
        doj: parseDateString(manager.manager_doj)
      };
    } else {
      alert('Failed to load profile data');
      console.error('Response status:', response.status);
    }
  } catch (error) {
    console.error('Error fetching manager data:', error);
    alert('Error loading profile: ' + error.message);
  }
  
  showProfileEditModal.value = true;
};

const handleUpdateProfile = async () => {
  // Validate name
  if (!profileEditForm.value.name.trim()) {
    alert('Name is required');
    return;
  }

  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      alert('Not authenticated');
      return;
    }

    // Get current user ID
    const userId = appStore.user?.id;
    if (!userId) {
      alert('Unable to identify user');
      return;
    }

    // Send update to backend
    const response = await fetch(`${API_BASE_URL}/api/manager/${userId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': token,
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        manager_name: profileEditForm.value.name,
        manager_email: profileEditForm.value.email,
        manager_contact: profileEditForm.value.phone,
        manager_role: profileEditForm.value.role,
        manager_doj: profileEditForm.value.doj
      })
    });

    if (response.ok) {
      // Update local store
      if (appStore.user) {
        appStore.user.name = profileEditForm.value.name;
        appStore.user.email = profileEditForm.value.email;
        appStore.user.phone = profileEditForm.value.phone;
        appStore.user.role = profileEditForm.value.role;
        appStore.user.doj = profileEditForm.value.doj;
      }
      
      alert('Profile updated successfully');
      showProfileEditModal.value = false;
    } else {
      const error = await response.json();
      alert(`Failed to update profile: ${error.message || 'Unknown error'}`);
    }
  } catch (error) {
    console.error('Error updating profile:', error);
    alert('Error updating profile: ' + error.message);
  }
};

// Booking handlers
const selectBookingCustomer = (customer) => {
  bookingForm.value.customerId = String(customer.id);
  bookingCustomerSearch.value = customer.name;
  showBookingCustomerDropdown.value = false;
};

// Fetch appointments from API
const fetchAppointments = async () => {
  const token = localStorage.getItem("authToken");
  if (!token) {
    console.error("Not authenticated");
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/appointment`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (response.ok) {
      const appointments = await response.json();
      console.log("Raw backend response:", appointments);
      // Map backend response to frontend format
      const mappedAppointments = appointments.map(appt => ({
        id: appt.appointment_id,
        customerId: appt.customer_id,
        customer_name: appt.customer_name,
        staffId: appt.staff_id,
        staff_name: appt.staff_name,
        serviceId: appt.services && appt.services.length > 0 ? appt.services[0].id : null,
        date: appt.datetime.split('T')[0],
        datetime: appt.datetime,
        notes: appt.datetime.split('T')[1],
        services: appt.services || [],
        status: "confirmed",
        invoiceStatus: "pending"
      }));
      console.log("Mapped appointments:", mappedAppointments);
      appStore.data.appointments = mappedAppointments;
      console.log("Appointments fetched successfully:", mappedAppointments);
    } else {
      console.error("Failed to fetch appointments:", response.status);
    }
  } catch (error) {
    console.error("Error fetching appointments:", error);
  }
};

const fetchInvoices = async () => {
  const token = localStorage.getItem("authToken");
  if (!token) {
    console.error("Not authenticated");
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/invoice`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (response.ok) {
      const fetchedInvoices = await response.json();
      // Map backend response to frontend format
      const mappedInvoices = fetchedInvoices.map(inv => ({
        id: inv.invoice_number || inv.id,
        invoice_number: inv.invoice_number,
        customer_id: inv.customer_id,
        customer_name: inv.customer_name || "",
        staff_id: inv.staff_id,
        staff_name: inv.staff_name || "",
        service_ids: inv.service_ids || "",
        service_descs: inv.service_descs || "",
        invoice_amount: inv.invoice_amount || 0,
        other_charges: inv.other_charges || 0,
        total_charges: inv.total_charges || inv.invoice_amount || 0,
        invoice_date: inv.invoice_date || new Date().toISOString().split('T')[0],
        status: inv.status || 0,
        rewards_earned: inv.rewards_earned || 0,
        rewards_utilized: inv.rewards_utilized || 0,
        current_reward_points: inv.current_reward_points || 0
      }));
      invoices.value = mappedInvoices;
      console.log("Invoices fetched successfully:", mappedInvoices);
    } else {
      console.error("Failed to fetch invoices:", response.status);
    }
  } catch (error) {
    console.error("Error fetching invoices:", error);
  }
};

const fetchManagerInventoryTransactions = async () => {
  const token = localStorage.getItem("authToken");
  if (!token) {
    console.error("Not authenticated");
    return;
  }

  try {
    let url = `${API_BASE_URL}/api/inventory-transaction`;
    
    // Add date range if provided
    if (managerTransactionDateFrom.value && managerTransactionDateTo.value) {
      url += `?from_date=${managerTransactionDateFrom.value}&to_date=${managerTransactionDateTo.value}`;
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
      const transactions = await response.json();
      managerInventoryTransactions.value = transactions;
      console.log("Manager inventory transactions fetched:", transactions);
    } else {
      console.error("Failed to fetch inventory transactions:", response.status);
    }
  } catch (error) {
    console.error("Error fetching inventory transactions:", error);
  }
};

const handleAppointmentSelect = (event) => {
  const appointmentId = parseInt(event.target.value);
  if (!appointmentId) {
    invoiceForm.value.customerId = null;
    invoiceForm.value.serviceId = null;
    invoiceForm.value.date = "";
    return;
  }
  
  const selected = data.value.appointments.find(a => a.id === appointmentId);
  if (selected) {
    invoiceForm.value.customerId = selected.customerId;
    invoiceForm.value.serviceId = selected.serviceId;
    invoiceForm.value.date = selected.date;
    console.log("Selected appointment:", selected);
    console.log("Form values:", invoiceForm.value);
  }
};

const handleAddInvoice = async () => {
  if (!invoiceForm.value.customerId || !invoiceForm.value.serviceId) {
    invoiceError.value = "Please select an appointment";
    return;
  }

  const token = localStorage.getItem("authToken");
  if (!token) {
    invoiceError.value = "Not authenticated";
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/invoice`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      },
      body: JSON.stringify({
        customer_id: invoiceForm.value.customerId,
        staff_id: 1, // Default or from appointment
        service_ids: String(invoiceForm.value.serviceId),
        invoice_amount: getServicePrice(invoiceForm.value.serviceId) || 0,
        other_charges: 0,
        status: 0
      })
    });

    if (response.ok) {
      invoiceSuccess.value = "Invoice created successfully!";
      invoiceError.value = "";
      invoiceForm.value = {
        customerId: null,
        serviceId: null,
        date: new Date().toISOString().split('T')[0],
        paymentType: "cash",
        discount: 0
      };
      setTimeout(() => invoiceSuccess.value = "", 3000);
      await fetchInvoices();
    } else {
      invoiceError.value = "Failed to create invoice";
    }
  } catch (error) {
    invoiceError.value = "Error creating invoice: " + error.message;
  }
};

const handleDeleteInvoice = async (invoiceId) => {
  if (!confirm("Are you sure you want to delete this invoice?")) return;

  const token = localStorage.getItem("authToken");
  if (!token) return;

  try {
    const response = await fetch(`${API_BASE_URL}/api/invoice/${invoiceId}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (response.ok) {
      invoiceSuccess.value = "Invoice deleted successfully!";
      setTimeout(() => invoiceSuccess.value = "", 3000);
      await fetchInvoices();
    }
  } catch (error) {
    invoiceError.value = "Error deleting invoice";
  }
};

const fetchManagerOrders = async () => {
  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      console.error("Not authenticated");
      return;
    }

    const response = await fetch(`${API_BASE_URL}/api/order`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (response.ok) {
      const orders = await response.json();
      managerOrders.value = orders;
      console.log("Manager wholesale orders fetched:", orders);
    } else {
      console.error("Failed to fetch orders:", response.status);
    }
  } catch (error) {
    console.error("Error fetching orders:", error);
  }
};

// Create supplier order
// Open edit order modal
const openEditOrderModal = (order) => {
  editingOrder.value = order;
  editOrderForm.value = {
    status: order.status,
    quantity: order.order_quantity,
    reason: order.reason_for_order || "",
    replenishment_date: order.order_replenishment_date ? new Date(order.order_replenishment_date).toISOString().split('T')[0] : ""
  };
  editOrderError.value = "";
  showEditOrderModal.value = true;
};

// Update supplier order
const handleUpdateOrder = async () => {
  editOrderError.value = "";

  if (!editingOrder.value) {
    editOrderError.value = "No order selected";
    return;
  }

  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      editOrderError.value = "Authentication required. Please login again.";
      return;
    }

    const payload = {
      status: parseInt(editOrderForm.value.status),
      order_quantity: parseInt(editOrderForm.value.quantity),
      reason_for_order: editOrderForm.value.reason
    };

    if (editOrderForm.value.replenishment_date) {
      payload.order_replenishment_date = editOrderForm.value.replenishment_date;
    }

    const response = await fetch(`${API_BASE_URL}/api/order/${editingOrder.value.order_id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      },
      body: JSON.stringify(payload)
    });

    const result = await response.json();

    if (response.ok) {
      console.log("Order updated successfully:", result);
      showEditOrderModal.value = false;
      editingOrder.value = null;
      
      // Refresh orders list
      await fetchManagerOrders();
    } else {
      editOrderError.value = result.message || "Failed to update order";
      console.error("Error updating order:", result);
    }
  } catch (error) {
    editOrderError.value = "Unable to connect to server. Please try again.";
    console.error("Network error:", error);
  }
};

// Delete supplier order
const handleDeleteOrder = async (orderId) => {
  if (!confirm("Are you sure you want to delete this order? This action cannot be undone.")) {
    return;
  }

  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      alert("Authentication required. Please login again.");
      return;
    }

    const response = await fetch(`${API_BASE_URL}/api/order/${orderId}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    const result = await response.json();

    if (response.ok) {
      console.log("Order deleted successfully");
      // Refresh orders list
      await fetchManagerOrders();
    } else {
      alert(result.message || "Failed to delete order");
      console.error("Error deleting order:", result);
    }
  } catch (error) {
    alert("Unable to connect to server. Please try again.");
    console.error("Network error:", error);
  }
};

// Mark order as delivered and auto-replenish stock
const handleMarkOrderDelivered = async (order) => {
  if (!confirm(`Mark order for "${order.product_name}" as Delivered? This will auto-replenish the stock.`)) {
    return;
  }

  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      alert("Authentication required. Please login again.");
      return;
    }

    const payload = {
      status: 1, // Mark as Processed/Delivered
      order_quantity: order.order_quantity
    };

    const response = await fetch(`${API_BASE_URL}/api/order/${order.order_id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      },
      body: JSON.stringify(payload)
    });

    const result = await response.json();

    if (response.ok) {
      alert(`Order marked as Delivered! Stock replenished by ${order.order_quantity} units.`);
      console.log("Order delivered and stock replenished:", result);
      
      // Refresh both orders and products
      await fetchManagerOrders();
      await fetchProducts();
    } else {
      alert(result.message || "Failed to mark order as delivered");
      console.error("Error marking order delivered:", result);
    }
  } catch (error) {
    alert("Unable to connect to server. Please try again.");
    console.error("Network error:", error);
  }
};

// Place grouped supplier orders to wholesale
const handlePlaceOrderToWholesale = async (supplierGroup) => {
  if (!confirm(`Are you sure you want to place all ${supplierGroup.items.length} item(s) to wholesale for supplier "${supplierGroup.supplier}"?`)) {
    return;
  }

  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      alert("Authentication required. Please login again.");
      return;
    }

    let successCount = 0;
    let failCount = 0;

    // Post each item as a separate order to wholesale
    for (const item of supplierGroup.items) {
      try {
        const product = data.value.products.find(p => p.id === item.product_id);
        const orderPayload = {
          product_id: item.product_id,
          order_quantity: item.quantity,
          reason_for_order: item.reason || "Manager replenishment order"
        };

        const response = await fetch(`${API_BASE_URL}/api/order`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
            "Authentication-Token": token
          },
          body: JSON.stringify(orderPayload)
        });

        if (response.ok) {
          successCount++;
          console.log(`Order placed for product ID ${item.product_id}`);
        } else {
          failCount++;
          console.error(`Failed to place order for product ID ${item.product_id}`);
        }
      } catch (error) {
        failCount++;
        console.error("Error placing order:", error);
      }
    }

    const summary = `Orders Placed to Wholesale!\n================================\nSupplier: ${supplierGroup.supplier}\nSuccessful: ${successCount}\nFailed: ${failCount}\nTotal Items: ${supplierGroup.items.length}`;
    alert(summary);
    
    // Refresh both lists
    await fetchManagerOrders();
    await fetchManagerInventoryTransactions();
    
    console.log(`${successCount} orders placed to wholesale, ${failCount} failed`);
  } catch (error) {
    alert("Error placing orders: " + error.message);
    console.error("Critical error:", error);
  }
};

// Get status color
const getStatusColor = (status) => {
  switch(status) {
    case 0: // Pending
      return { bg: '#fff3cd', text: '#856404' };
    case 1: // Processed
      return { bg: '#d4edda', text: '#155724' };
    case 2: // Cancelled
      return { bg: '#f8d7da', text: '#721c24' };
    default:
      return { bg: '#e2e3e5', text: '#383d41' };
  }
};

// Get status label
const getStatusLabel = (status) => {
  switch(status) {
    case 0: return "Pending";
    case 1: return "Processed";
    case 2: return "Cancelled";
    default: return "Unknown";
  }
};

const handleCreateBooking = async () => {
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
      bookingError.value = `Please select today or within the next 2 days`;
    }
    return;
  }

  // Get customer email
  if (!bookingForm.value.customerId) {
    bookingError.value = "Please select a customer";
    return;
  }
  
  if (!data.value.customers || data.value.customers.length === 0) {
    bookingError.value = "No customers found. Please wait for data to load and try again.";
    return;
  }
  
  const customerEmail = getCustomerEmail(bookingForm.value.customerId);
  if (!customerEmail) {
    const customerId = parseInt(bookingForm.value.customerId) || bookingForm.value.customerId;
    const customer = data.value.customers.find(c => c.id === customerId || String(c.id) === String(bookingForm.value.customerId));
    bookingError.value = customer ? `Customer "${customer.name}" has no email address` : "Selected customer not found. Please select a valid customer.";
    console.error("Customer lookup failed for ID:", bookingForm.value.customerId, "Available customers:", data.value.customers);
    return;
  }

  // Combine date and time into ISO datetime
  const appointmentDateTime = `${bookingForm.value.date}T${bookingForm.value.time}:00`;

  // Get staff ID if assigned
  const staffId = bookingForm.value.staffId ? parseInt(bookingForm.value.staffId) : null;

  const token = localStorage.getItem("authToken");
  if (!token) {
    bookingError.value = "Authentication token not found";
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/appointment`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      },
      body: JSON.stringify({
        customer_email: customerEmail,
        service_ids: bookingForm.value.serviceIds.map(id => parseInt(id)),
        appointment_datetime: appointmentDateTime,
        staff_id: staffId
      })
    });

    const data_response = await response.json();
    
    if (response.ok) {
      const serviceNames = bookingForm.value.serviceIds.map(serviceId => {
        const service = data.value.services.find(s => s.id == serviceId);
        return service ? service.name : '';
      }).filter(Boolean).join(', ');

      bookingSuccess.value = `Booking created successfully for ${serviceNames}!`;
      
      // Refresh appointments list
      await fetchAppointments();
      
      // Clear form
      setTimeout(() => {
        bookingForm.value = {
          customerId: "",
          serviceIds: [],
          date: "",
          time: "",
          staffId: ""
        };
        bookingCustomerSearch.value = "";
        bookingSuccess.value = "";
      }, 1500);
    } else {
      bookingError.value = data_response.message || "Failed to create appointment";
    }
  } catch (error) {
    console.error("Fetch error:", error);
    bookingError.value = "Network error: " + error.message;
  }
};

const handleCreateQuickAppointmentForToday = async () => {
  quickAppointmentError.value = "";
  quickAppointmentSuccess.value = "";

  if (!quickAppointmentForm.value.customerId) {
    quickAppointmentError.value = "Please select a customer";
    return;
  }

  if (quickAppointmentForm.value.serviceIds.length === 0) {
    quickAppointmentError.value = "Please select at least one service";
    return;
  }

  if (!quickAppointmentForm.value.time) {
    quickAppointmentError.value = "Please select a time";
    return;
  }

  const customerEmail = getCustomerEmail(quickAppointmentForm.value.customerId);
  if (!customerEmail) {
    const customerId = parseInt(quickAppointmentForm.value.customerId) || quickAppointmentForm.value.customerId;
    const customer = data.value.customers.find(c => c.id === customerId || String(c.id) === String(quickAppointmentForm.value.customerId));
    quickAppointmentError.value = customer ? `Customer "${customer.name}" has no email address` : "Selected customer not found";
    return;
  }

  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      quickAppointmentError.value = "Authentication required";
      return;
    }

    // Get today's date
    const today = new Date().toISOString().split('T')[0];
    const appointmentDateTime = `${today}T${quickAppointmentForm.value.time}:00`;

    const staffId = quickAppointmentForm.value.staffId ? parseInt(quickAppointmentForm.value.staffId) : null;

    const response = await fetch(`${API_BASE_URL}/api/appointment`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      },
      body: JSON.stringify({
        customer_email: customerEmail,
        service_ids: quickAppointmentForm.value.serviceIds.map(id => parseInt(id)),
        appointment_datetime: appointmentDateTime,
        staff_id: staffId
      })
    });

    const result = await response.json();

    if (response.ok) {
      const serviceNames = quickAppointmentForm.value.serviceIds.map(serviceId => {
        const service = data.value.services.find(s => s.id == serviceId);
        return service ? service.name : '';
      }).filter(Boolean).join(', ');

      quickAppointmentSuccess.value = `Appointment created for today at ${quickAppointmentForm.value.time}!`;

      // Reset form
      setTimeout(() => {
        quickAppointmentForm.value = {
          customerId: "",
          serviceIds: [],
          time: "",
          staffId: ""
        };
        quickAppointmentSuccess.value = "";
        // Refresh appointments
        fetchAppointments();
        fetchTodaysAppointmentsForInvoice();
      }, 1500);
    } else {
      quickAppointmentError.value = result.message || "Failed to create appointment";
    }
  } catch (error) {
    console.error("Error creating appointment:", error);
    quickAppointmentError.value = "Network error: " + error.message;
  }
};

// Fetch services from API
const fetchServices = async () => {
  console.log("fetchServices() called");
  const token = localStorage.getItem("authToken");
  if (!token) {
    console.error("Not authenticated");
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/service`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (response.ok) {
      const services = await response.json();
      console.log("Services API returned:", services);
      // Map backend field names to frontend field names
      appStore.data.services = services.map(s => {
        // Find the category ID from the category name
        const category = data.value.serviceCategories.find(
          c => c.name.toLowerCase() === (s.service_category || '').toLowerCase()
        );
        const categoryId = category ? category.id : 1;

        return {
          id: s.service_id,
          name: s.service_desc,
          categoryId: categoryId,
          category: s.service_category,
          price: s.service_price,
          duration: s.service_duration,
          productsRequired: s.service_products || "None",
          fromDate: s.from_date,
          toDate: s.to_date,
          rating: s.service_rating,
          reviews: s.no_of_reviews,
          active: s.active_flg
        };
      });
      console.log("Services after mapping:", appStore.data.services);
    } else {
      console.error("Failed to fetch services:", response.status);
    }
  } catch (error) {
    console.error("Error fetching services:", error);
  }
};

// Service handlers
const handleServiceSubmit = async () => {
  console.log("handleServiceSubmit called - isEditingService:", isEditingService.value);
  if (isEditingService.value) {
    return await handleUpdateService();
  } else {
    return await handleAddService();
  }
};

const handleAddService = async () => {
  serviceError.value = "";
  serviceSuccess.value = "";

  if (!serviceForm.value.name?.trim()) {
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

  const token = localStorage.getItem("authToken");
  if (!token) {
    serviceError.value = "Authentication token not found";
    return;
  }

  // Find category name from category ID
  const categoryName = data.value.serviceCategories.find(c => c.id == serviceForm.value.categoryId)?.name || "Hair";

  const payload = {
    service_desc: serviceForm.value.name.trim(),
    service_category: categoryName,
    service_price: serviceForm.value.price,
    service_duration: serviceForm.value.duration,
    service_products: serviceForm.value.productsRequired?.trim() || "",
    from_date: serviceForm.value.fromDate || new Date().toISOString().split('T')[0],
    to_date: serviceForm.value.toDate || null
  };

  try {
    const response = await fetch(`${API_BASE_URL}/api/service`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      },
      body: JSON.stringify(payload)
    });

    if (response.ok) {
      const result = await response.json();
      console.log("Service created:", result);
      serviceSuccess.value = "Service added successfully!";
      
      // Fetch updated service list
      await fetchServices();
      
      // Reset form
      serviceForm.value = {
        name: "",
        categoryId: "",
        price: 0,
        duration: 0,
        productsRequired: "",
        fromDate: "",
        toDate: ""
      };
      
      setTimeout(() => {
        serviceSuccess.value = "";
      }, 1500);
    } else {
      const error = await response.json();
      serviceError.value = error.message || "Failed to add service";
      console.error("Error adding service:", error);
    }
  } catch (error) {
    serviceError.value = "Error adding service: " + error.message;
    console.error("Error adding service:", error);
  }
};

const cancelEditService = () => {
  serviceForm.value = {
    name: "",
    categoryId: "",
    price: 0,
    duration: 0,
    productsRequired: "",
    fromDate: "",
    toDate: ""
  };
  isEditingService.value = false;
  editingServiceId.value = null;
  editingServiceData.value = null;
  serviceError.value = "";
  serviceSuccess.value = "";
};

const handleEditService = (service) => {
  console.log("handleEditService called with service:", service);
  serviceError.value = "";
  serviceSuccess.value = "";
  
  // Store service data for display in modal
  editingServiceData.value = service;
  
  // Populate form with service data
  serviceForm.value = {
    name: service.name,
    categoryId: Number(service.categoryId),
    price: service.price,
    duration: service.duration,
    productsRequired: service.productsRequired || "",
    fromDate: service.fromDate || "",
    toDate: service.toDate || ""
  };
  
  console.log("Setting isEditingService to true, editingServiceId to:", service.id);
  console.log("Form populated:", serviceForm.value);
  
  isEditingService.value = true;
  editingServiceId.value = service.id;
  
  console.log("After setting flags - isEditingService:", isEditingService.value, "editingServiceId:", editingServiceId.value);
};

const handleUpdateService = async () => {
  console.log("handleUpdateService called - isEditingService:", isEditingService.value, "editingServiceId:", editingServiceId.value);
  console.log("Current form values:", serviceForm.value);
  serviceError.value = "";
  serviceSuccess.value = "";

  if (!serviceForm.value.name?.trim()) {
    serviceError.value = "Service name is required";
    console.error("Validation failed: name required");
    return;
  }

  if (!serviceForm.value.categoryId) {
    serviceError.value = "Please select a category";
    console.error("Validation failed: category required", serviceForm.value.categoryId);
    return;
  }

  if (!serviceForm.value.price || serviceForm.value.price <= 0) {
    serviceError.value = "Price must be greater than 0";
    console.error("Validation failed: price required");
    return;
  }

  if (!serviceForm.value.duration || serviceForm.value.duration < 15) {
    serviceError.value = "Duration must be at least 15 minutes";
    console.error("Validation failed: duration required");
    return;
  }

  const token = localStorage.getItem("authToken");
  if (!token) {
    serviceError.value = "Authentication token not found";
    console.error("No auth token");
    return;
  }

  // Find category name from category ID
  const categoryName = data.value.serviceCategories.find(c => c.id == serviceForm.value.categoryId)?.name || "Hair";
  console.log("Category ID:", serviceForm.value.categoryId, "Category Name:", categoryName);

  const payload = {
    service_desc: serviceForm.value.name.trim(),
    service_category: categoryName,
    service_price: serviceForm.value.price,
    service_duration: serviceForm.value.duration,
    service_products: serviceForm.value.productsRequired?.trim() || "",
    from_date: serviceForm.value.fromDate || new Date().toISOString().split('T')[0],
    to_date: serviceForm.value.toDate || null
  };

  console.log("Sending payload:", payload);

  try {
    const response = await fetch(`${API_BASE_URL}/api/service/${editingServiceId.value}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      },
      body: JSON.stringify(payload)
    });

    console.log("PUT Response status:", response.status, "OK:", response.ok);

    if (response.ok) {
      const result = await response.json();
      console.log("Service updated:", result);
      serviceSuccess.value = "Service updated successfully!";
      
      console.log("Calling fetchServices to refresh the list...");
      // Fetch updated service list
      await fetchServices();
      console.log("Services refreshed after update. Total services:", data.value.services.length);
      data.value.services.forEach(s => {
        console.log("  -", s.id, ":", s.name, "($" + s.price + ")");
      });
      
      // Reset form
      isEditingService.value = false;
      editingServiceId.value = null;
      editingServiceData.value = null;
      serviceForm.value = {
        name: "",
        categoryId: "",
        price: 0,
        duration: 0,
        productsRequired: "",
        fromDate: "",
        toDate: ""
      };
      
      setTimeout(() => {
        serviceSuccess.value = "";
      }, 1500);
    } else {
      console.error("Response status:", response.status);
      const error = await response.json();
      serviceError.value = error.message || "Failed to update service";
      console.error("Error updating service:", error);
    }
  } catch (error) {
    serviceError.value = "Error updating service: " + error.message;
    console.error("Error updating service - catch block:", error);
  }
};

const handleDeleteService = async (serviceId) => {
  if (!confirm("Are you sure you want to delete this service?")) {
    return;
  }

  const token = localStorage.getItem("authToken");
  if (!token) {
    alert("Authentication token not found");
    return;
  }

  try {
    console.log("Attempting to delete service:", serviceId);
    console.log("API URL:", `${API_BASE_URL}/api/service/${serviceId}`);
    
    const response = await fetch(`${API_BASE_URL}/api/service/${serviceId}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    console.log("Delete response status:", response.status, "OK:", response.ok);

    if (response.ok) {
      console.log("Service deleted successfully");
      alert("Service deleted successfully!");
      
      // Fetch updated service list
      await fetchServices();
    } else {
      console.error("Delete failed with status:", response.status);
      let errorMsg = "Failed to delete service";
      
      try {
        const error = await response.json();
        errorMsg = error.message || errorMsg;
      } catch (e) {
        console.error("Could not parse error response:", e);
      }
      
      alert("Error: " + errorMsg);
    }
  } catch (error) {
    console.error("Fetch error:", error);
    alert("Network error: " + error.message + "\n\nMake sure the backend server is running on " + API_BASE_URL);
  }
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

// Fetch customers from API
const fetchCustomers = async () => {
  const token = localStorage.getItem("authToken");
  if (!token) {
    console.error("Not authenticated");
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/customer`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (response.ok) {
      const customers = await response.json();
      // Map backend field names to frontend field names
      appStore.data.customers = customers.map(c => ({
        id: c.customer_id,
        name: c.customer_name,
        email: c.customer_email,
        phone: c.customer_contact,
        dob: c.customer_dob,
        address: c.customer_address,
        preferences: c.customer_preferences,
        customerType: c.customer_type,
        noOfVisits: c.number_of_visits,
        registrationDate: c.customer_reg_date,
        pointsBalance: c.customer_available_rewards || 0
      }));
      console.log("Customers fetched:", appStore.data.customers);
    } else {
      console.error("Failed to fetch customers:", response.status);
    }
  } catch (error) {
    console.error("Error fetching customers:", error);
  }
};

// Customer handlers
const handleAddCustomer = async () => {
  customerError.value = "";
  customerSuccess.value = "";

  if (!customerForm.value.name?.trim()) {
    customerError.value = "Customer name is required";
    return;
  }

  if (!customerForm.value.email?.trim()) {
    customerError.value = "Email is required";
    return;
  }

  if (!customerForm.value.phone?.trim()) {
    customerError.value = "Phone is required";
    return;
  }

  if (!customerForm.value.dob) {
    customerError.value = "Date of birth is required";
    return;
  }

  const token = localStorage.getItem("authToken");
  if (!token) {
    customerError.value = "Authentication token not found";
    return;
  }

  const payload = {
    customer_name: customerForm.value.name.trim(),
    customer_email: customerForm.value.email.trim(),
    customer_contact: customerForm.value.phone.trim(),
    customer_dob: customerForm.value.dob,
    customer_address: customerForm.value.address?.trim() || "",
    customer_preferences: customerForm.value.preferences?.trim() || "",
    customer_type: customerForm.value.customerType || "Normal"
  };

  try {
    console.log("Sending payload:", payload);
    const response = await fetch(`${API_BASE_URL}/api/customer`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      },
      body: JSON.stringify(payload)
    });

    console.log("Response status:", response.status);
    const responseData = await response.json();
    console.log("Response data:", responseData);

    if (response.ok) {
      customerSuccess.value = "Customer added successfully!";
      
      // Fetch updated customer list
      await fetchCustomers();
      
      // Reset form
      customerForm.value = {
        name: "",
        email: "",
        phone: "",
        dob: "",
        address: "",
        preferences: "",
        customerType: "Normal"
      };
      
      setTimeout(() => {
        customerSuccess.value = "";
      }, 1500);
    } else {
      customerError.value = responseData.message || "Failed to add customer";
      console.error("Error adding customer:", responseData);
    }
  } catch (error) {
    customerError.value = "Error adding customer: " + error.message;
    console.error("Error adding customer:", error);
  }
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
  editingCustomerData.value = null;
  customerError.value = "";
  customerSuccess.value = "";
};

const handleEditCustomer = (customer) => {
  customerError.value = "";
  customerSuccess.value = "";
  
  // Store customer data for display in modal
  editingCustomerData.value = customer;
  
  // Populate form with customer data
  customerForm.value = {
    name: customer.name,
    email: customer.email,
    phone: customer.phone,
    dob: customer.dob,
    address: customer.address || "",
    preferences: customer.preferences || "",
    customerType: customer.customerType || "Normal"
  };
  
  isEditingCustomer.value = true;
  editingCustomerId.value = customer.id;
};

const handleUpdateCustomer = async () => {
  customerError.value = "";
  customerSuccess.value = "";

  if (!customerForm.value.name?.trim()) {
    customerError.value = "Customer name is required";
    return;
  }

  if (!customerForm.value.email?.trim()) {
    customerError.value = "Email is required";
    return;
  }

  if (!customerForm.value.phone?.trim()) {
    customerError.value = "Phone is required";
    return;
  }

  if (!customerForm.value.dob) {
    customerError.value = "Date of birth is required";
    return;
  }

  const token = localStorage.getItem("authToken");
  if (!token) {
    customerError.value = "Authentication token not found";
    return;
  }

  const payload = {
    customer_name: customerForm.value.name.trim(),
    customer_email: customerForm.value.email.trim(),
    customer_contact: customerForm.value.phone.trim(),
    customer_dob: customerForm.value.dob,
    customer_address: customerForm.value.address?.trim() || "",
    customer_preferences: customerForm.value.preferences?.trim() || "",
    customer_type: customerForm.value.customerType || "Normal"
  };

  try {
    const response = await fetch(`${API_BASE_URL}/api/customer/${editingCustomerId.value}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      },
      body: JSON.stringify(payload)
    });

    if (response.ok) {
      const result = await response.json();
      console.log("Customer updated:", result);
      customerSuccess.value = "Customer updated successfully!";
      
      // Fetch updated customer list
      await fetchCustomers();
      
      // Reset form
      isEditingCustomer.value = false;
      editingCustomerId.value = null;
      editingCustomerData.value = null;
      customerForm.value = {
        name: "",
        email: "",
        phone: "",
        dob: "",
        address: "",
        preferences: "",
        customerType: "Normal"
      };
      
      setTimeout(() => {
        customerSuccess.value = "";
      }, 1500);
    } else {
      const error = await response.json();
      customerError.value = error.message || "Failed to update customer";
      console.error("Error updating customer:", error);
    }
  } catch (error) {
    customerError.value = "Error updating customer: " + error.message;
    console.error("Error updating customer:", error);
  }
};

const handleDeleteCustomer = async (customerId) => {
  if (!confirm("Are you sure you want to delete this customer?")) {
    return;
  }

  const token = localStorage.getItem("authToken");
  if (!token) {
    alert("Authentication token not found");
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/customer/${customerId}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (response.ok) {
      const result = await response.json();
      console.log("Customer deleted:", result);
      alert("Customer deleted successfully!");
      
      // Fetch updated customer list
      await fetchCustomers();
    } else {
      const error = await response.json();
      const errorMsg = error.message || "Failed to delete customer";
      alert("Error: " + errorMsg);
      console.error("Error deleting customer:", error);
    }
  } catch (error) {
    alert("Error deleting customer: " + error.message);
    console.error("Error deleting customer:", error);
  }
};

// Initialize rewards form with store data
const initializeRewardsForm = () => {
  if (data.value.rewards) {
    rewardsForm.value = { ...data.value.rewards };
  }
};

// Call initialization
initializeRewardsForm();

// Fetch Rewards Settings from salon_config
const fetchRewardsSettings = async () => {
  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      console.error("Not authenticated");
      return;
    }

    const response = await fetch(`${API_BASE_URL}/api/salon-config`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (response.ok) {
      const allConfigs = await response.json();
      const rewardSettings = Array.isArray(allConfigs) ? allConfigs : [allConfigs];
      
      rewardSettings.forEach(setting => {
        if (setting.param_name === "POINTS_PER_CURRENCY") {
          rewardsForm.value.POINTS_PER_CURRENCY = parseFloat(setting.param_value);
        } else if (setting.param_name === "POINTS_FOR_REDUMPTION") {
          rewardsForm.value.POINTS_FOR_REDUMPTION = parseInt(setting.param_value);
        } else if (setting.param_name === "REDUMPTION_VALUE_PER_POINT") {
          rewardsForm.value.REDUMPTION_VALUE_PER_POINT = parseFloat(setting.param_value);
        } else if (setting.param_name === "FIRST_VISIT_BONUS_POINTS") {
          rewardsForm.value.FIRST_VISIT_BONUS_POINTS = parseInt(setting.param_value);
        } else if (setting.param_name === "BIRTHDAY_BONUS_POINTS") {
          rewardsForm.value.BIRTHDAY_BONUS_POINTS = parseInt(setting.param_value);
        } else if (setting.param_name === "VIP_DISCOUNT_PERCENTAGE") {
          rewardsForm.value.VIP_DISCOUNT_PERCENTAGE = parseFloat(setting.param_value);
        } else if (setting.param_name === "REWARD_EXPIRY_DAYS") {
          rewardsForm.value.REWARD_EXPIRY_DAYS = parseInt(setting.param_value);
        }
      });
    }
  } catch (error) {
    console.error("Error fetching rewards settings:", error);
  }
};

const handleUpdateRewards = async () => {
  rewardsError.value = "";
  rewardsSuccess.value = "";

  // Validation
  if (rewardsForm.value.POINTS_PER_CURRENCY <= 0) {
    rewardsError.value = "Points per currency must be greater than 0";
    return;
  }

  if (rewardsForm.value.POINTS_FOR_REDUMPTION <= 0) {
    rewardsError.value = "Points for redemption must be greater than 0";
    return;
  }

  if (rewardsForm.value.REDUMPTION_VALUE_PER_POINT <= 0) {
    rewardsError.value = "Redemption value per point must be greater than 0";
    return;
  }

  if (rewardsForm.value.REWARD_EXPIRY_DAYS <= 0) {
    rewardsError.value = "Reward expiry days must be greater than 0";
    return;
  }

  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      rewardsError.value = "Not authenticated";
      return;
    }

    const getResponse = await fetch(`${API_BASE_URL}/api/salon-config`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (!getResponse.ok) {
      rewardsError.value = "Failed to fetch current settings";
      return;
    }

    const allConfigs = await getResponse.json();
    const configArray = Array.isArray(allConfigs) ? allConfigs : [allConfigs];
    
    const rewardUpdates = [
      { name: "POINTS_PER_CURRENCY", value: rewardsForm.value.POINTS_PER_CURRENCY.toString() },
      { name: "POINTS_FOR_REDUMPTION", value: rewardsForm.value.POINTS_FOR_REDUMPTION.toString() },
      { name: "REDUMPTION_VALUE_PER_POINT", value: rewardsForm.value.REDUMPTION_VALUE_PER_POINT.toString() },
      { name: "FIRST_VISIT_BONUS_POINTS", value: rewardsForm.value.FIRST_VISIT_BONUS_POINTS.toString() },
      { name: "BIRTHDAY_BONUS_POINTS", value: rewardsForm.value.BIRTHDAY_BONUS_POINTS.toString() },
      { name: "VIP_DISCOUNT_PERCENTAGE", value: rewardsForm.value.VIP_DISCOUNT_PERCENTAGE.toString() },
      { name: "REWARD_EXPIRY_DAYS", value: rewardsForm.value.REWARD_EXPIRY_DAYS.toString() }
    ];

    for (const update of rewardUpdates) {
      const config = configArray.find(c => c.param_name === update.name);
      if (config) {
        const putResponse = await fetch(`${API_BASE_URL}/api/salon-config/${config.setting_id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
            "Authentication-Token": token
          },
          body: JSON.stringify({ param_value: update.value })
        });

        if (!putResponse.ok) {
          rewardsError.value = `Failed to update ${update.name}`;
          return;
        }
      }
    }

    rewardsSuccess.value = "Reward settings updated successfully!";
    setTimeout(() => {
      rewardsSuccess.value = "";
    }, 3000);
  } catch (error) {
    console.error("Error updating rewards:", error);
    rewardsError.value = "Error updating reward settings";
  }
};

// Fetch staff from API
const fetchStaff = async () => {
  const token = localStorage.getItem("authToken");
  if (!token) {
    console.error("Not authenticated");
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/staff`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (response.ok) {
      const staffList = await response.json();
      // Map backend field names to frontend field names
      appStore.data.staff = staffList.map(s => ({
        id: s.staff_id,
        name: s.staff_name,
        email: s.staff_email,
        phone: s.staff_contact,
        role: s.staff_role,
        dob: s.staff_dob,
        doj: s.staff_doj,
        skills: s.staff_skills,
        salary: s.staff_salary,
        rating: s.staff_cumulative_rating,
        reviews: s.no_of_reviews,
        status: "active"
      }));
      console.log("Staff fetched:", appStore.data.staff);
    } else {
      console.error("Failed to fetch staff:", response.status);
    }
  } catch (error) {
    console.error("Error fetching staff:", error);
  }
};

// Staff handlers
const handleAddStaff = async () => {
  staffError.value = "";
  staffSuccess.value = "";

  if (!staffForm.value.name?.trim()) {
    staffError.value = "Staff name is required";
    return;
  }

  if (!staffForm.value.role?.trim()) {
    staffError.value = "Role is required";
    return;
  }

  if (!staffForm.value.email?.trim()) {
    staffError.value = "Email is required";
    return;
  }

  if (!staffForm.value.phone?.trim()) {
    staffError.value = "Phone is required";
    return;
  }

  if (!staffForm.value.skills?.trim()) {
    staffError.value = "Skills are required";
    return;
  }

  if (!staffForm.value.dob) {
    staffError.value = "Date of birth is required";
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

  if (!staffForm.value.username?.trim()) {
    staffError.value = "Username is required";
    return;
  }

  const token = localStorage.getItem("authToken");
  if (!token) {
    staffError.value = "Authentication token not found";
    return;
  }

  const payload = {
    staff_name: staffForm.value.name.trim(),
    staff_role: staffForm.value.role.trim(),
    staff_email: staffForm.value.email.trim(),
    staff_contact: staffForm.value.phone.trim(),
    staff_skills: staffForm.value.skills.trim(),
    staff_dob: staffForm.value.dob,
    staff_doj: staffForm.value.doj,
    staff_salary: staffForm.value.salary,
    username: staffForm.value.username.trim()
  };

  try {
    const response = await fetch(`${API_BASE_URL}/api/staff`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      },
      body: JSON.stringify(payload)
    });

    if (response.ok) {
      const result = await response.json();
      console.log("Staff created:", result);
      staffSuccess.value = "Staff member added successfully!";
      
      // Fetch updated staff list
      await fetchStaff();
      
      // Reset form
      staffForm.value = {
        name: "",
        role: "",
        email: "",
        phone: "",
        skills: "",
        dob: "",
        doj: "",
        salary: 0,
        username: ""
      };
      
      setTimeout(() => {
        staffSuccess.value = "";
      }, 1500);
    } else {
      const error = await response.json();
      staffError.value = error.message || "Failed to add staff";
      console.error("Error adding staff:", error);
    }
  } catch (error) {
    staffError.value = "Error adding staff: " + error.message;
    console.error("Error adding staff:", error);
  }
};

// Invoice handlers

const handleSendInvoice = (invoice) => {
  const customerEmail = data.value.customers.find(c => c.id === invoice.customer_id)?.email;
  const customerName = getCustomerName(invoice.customer_id);
  
  if (!customerEmail) {
    alert("Customer email not found!");
    return;
  }

  // Show confirmation dialog
  if (confirm(`Send invoice to ${customerName} (${customerEmail})?\n\nInvoice: #${invoice.invoice_number}\nAmount: ₹${invoice.total_charges}`)) {
    // Update invoice status to Invoiced (1) in the local state
    invoice.status = 1;
    
    // Show success message
    alert(`✓ Invoice #${invoice.invoice_number} sent successfully to ${customerEmail}!`);
    
    console.log(`Invoice ${invoice.invoice_number} marked as sent to ${customerEmail}`);
  }
};

// Financial section password handlers
const handleFinanceAccess = async () => {
  if (financeAuthenticated.value) {
    currentView.value = 'finance';
    await fetchFinanceData();
  } else {
    financialPasswordInput.value = "";
    financialPasswordError.value = "";
    showFinancePassword.value = false;
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
    showReportsPassword.value = false;
    pendingFinancialView.value = 'reports';
    showReportsPasswordModal.value = true;
  }
};

const verifyFinancialPassword = async () => {
  financialPasswordError.value = "";
  
  if (!financialPasswordInput.value) {
    financialPasswordError.value = "❌ Password is required.";
    return;
  }
  
  try {
    if (!appStore.user || !appStore.user.username) {
      financialPasswordError.value = "❌ User information not found. Please login again.";
      return;
    }

    // Determine login endpoint based on user role
    let loginEndpoint = "";
    const userRole = appStore.user.role?.toLowerCase() || "manager";
    
    if (userRole === "owner") {
      loginEndpoint = `${API_BASE_URL}/owner-login`;
    } else if (userRole === "manager") {
      loginEndpoint = `${API_BASE_URL}/manager-login`;
    } else if (userRole === "staff") {
      loginEndpoint = `${API_BASE_URL}/staff-login`;
    } else if (userRole === "customer") {
      loginEndpoint = `${API_BASE_URL}/customer-login`;
    }

    const response = await fetch(loginEndpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username: appStore.user.username,
        password: financialPasswordInput.value
      })
    });

    const data = await response.json();

    if (response.ok && data.token) {
      financeAuthenticated.value = true;
      showFinancePasswordModal.value = false;
      showFinancePassword.value = false;
      currentView.value = 'finance';
      financialPasswordInput.value = "";
      await fetchFinanceData();
    } else {
      financialPasswordError.value = "❌ Incorrect password. Please try again.";
      financialPasswordInput.value = "";
    }
  } catch (error) {
    console.error("Error verifying password:", error);
    financialPasswordError.value = "❌ Error verifying password. Please try again.";
  }
};

const verifyReportsPassword = async () => {
  financialPasswordError.value = "";
  
  if (!financialPasswordInput.value) {
    financialPasswordError.value = "❌ Password is required.";
    return;
  }
  
  try {
    if (!appStore.user || !appStore.user.username) {
      financialPasswordError.value = "❌ User information not found. Please login again.";
      return;
    }

    // Determine login endpoint based on user role
    let loginEndpoint = "";
    const userRole = appStore.user.role?.toLowerCase() || "manager";
    
    if (userRole === "owner") {
      loginEndpoint = `${API_BASE_URL}/owner-login`;
    } else if (userRole === "manager") {
      loginEndpoint = `${API_BASE_URL}/manager-login`;
    } else if (userRole === "staff") {
      loginEndpoint = `${API_BASE_URL}/staff-login`;
    } else if (userRole === "customer") {
      loginEndpoint = `${API_BASE_URL}/customer-login`;
    }

    const response = await fetch(loginEndpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username: appStore.user.username,
        password: financialPasswordInput.value
      })
    });

    const data = await response.json();

    if (response.ok && data.token) {
      reportsAuthenticated.value = true;
      showReportsPasswordModal.value = false;
      showReportsPassword.value = false;
      currentView.value = 'reports';
      financialPasswordInput.value = "";
    } else {
      financialPasswordError.value = "❌ Incorrect password. Please try again.";
      financialPasswordInput.value = "";
    }
  } catch (error) {
    console.error("Error verifying password:", error);
    financialPasswordError.value = "❌ Error verifying password. Please try again.";
  }
};

// ── Manager Profile Data Fetch ────────────────────────────────────────────
const fetchManagerProfileData = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const userId = appStore.user?.id;
    
    if (!token || !userId) return;

    const response = await fetch(`${API_BASE_URL}/api/manager/${userId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': token,
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.ok) {
      managerProfileData.value = await response.json();
      console.log('Manager profile data loaded:', managerProfileData.value);
    }
  } catch (error) {
    console.error('Error fetching manager profile:', error);
  }
};

// ── Finance API Functions ──────────────────────────────────────────────────

const openEditOverheadModal = async () => {
  try {
    if (financeData.value) {
      overheadEditForm.value = {
        overheads: financeData.value.overheads || 0
      };
      showEditOverheadModal.value = true;
    }
  } catch (error) {
    console.error('Error opening edit modal:', error);
  }
};

const handleUpdateOverhead = async () => {
  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      alert('User not authenticated');
      return;
    }

    // Get current month's last date
    const now = new Date();
    const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0);
    const lastDateStr = lastDay.toISOString().split('T')[0];

    const response = await fetch(`${API_BASE_URL}/api/finance`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': token,
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        last_date: lastDateStr,
        overheads: parseFloat(overheadEditForm.value.overheads)
      }),
    });

    if (response.ok) {
      const data = await response.json();
      financeData.value = data;
      showEditOverheadModal.value = false;
      alert('✅ Overhead bills updated successfully!');
    } else {
      const errorData = await response.json();
      alert(`❌ Failed to update: ${errorData.message}`);
    }
  } catch (error) {
    console.error('Error updating overhead bills:', error);
    alert(`❌ Error: ${error.message}`);
  }
};

const fetchFinanceData = async () => {
  try {
    financeLoading.value = true;
    financeError.value = null;
    
    const token = localStorage.getItem('authToken');
    if (!token) {
      financeError.value = "User not authenticated";
      return;
    }

    // Get current month's last date
    const now = new Date();
    const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0);
    const lastDateStr = lastDay.toISOString().split('T')[0];
    
    // Try to fetch existing finance record
    const response = await fetch(`${API_BASE_URL}/api/finance?last_date=${lastDateStr}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': token,
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.status === 404) {
      // Finance record not found, create it
      console.log('Finance record not found, creating new one...');
      await createFinanceReport(lastDateStr);
    } else if (response.ok) {
      const data = await response.json();
      financeData.value = data;
      console.log('Finance data fetched:', data);
    } else {
      throw new Error(`Failed to fetch finance data: ${response.status}`);
    }
  } catch (error) {
    console.error('Error fetching finance data:', error);
    financeError.value = error.message;
  } finally {
    financeLoading.value = false;
  }
};

const createFinanceReport = async (lastDateStr) => {
  try {
    const token = localStorage.getItem('authToken');
    if (!token) return;

    const response = await fetch(`${API_BASE_URL}/api/finance`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': token,
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ last_date: lastDateStr }),
    });

    if (response.ok) {
      const data = await response.json();
      financeData.value = data;
      console.log('Finance report created:', data);
    } else {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to create finance report');
    }
  } catch (error) {
    console.error('Error creating finance report:', error);
    financeError.value = error.message;
  }
};

// ── Report helpers ─────────────────────────────────────────────────────────

/** Trigger a browser download from a Blob. */
const _downloadBlob = (blob, filename) => {
  const url = URL.createObjectURL(blob);
  const a   = document.createElement('a');
  a.href     = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  setTimeout(() => URL.revokeObjectURL(url), 2000);
};

/** Call the backend, get a Blob, add to session history, trigger download. */
const _callGenerateReport = async (reportType, timePeriod, format, customStart, customEnd) => {
  const token = localStorage.getItem("authToken");
  const res = await fetch(`${API_BASE_URL}/generate-report`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      "Authentication-Token": token,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      report_type: reportType,
      time_period: timePeriod,
      format,
      custom_start: customStart || null,
      custom_end:   customEnd   || null,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.message || 'Report generation failed');
  }
  const blob     = await res.blob();
  const filename = `${reportType}_report_${timePeriod}.${format}`;
  const id       = `${Date.now()}-${Math.random().toString(36).slice(2)}`;

  _reportBlobs.set(id, { blob, filename });

  generatedReports.value.unshift({
    id,
    title:       `${REPORT_ICONS[reportType] || '📄'} ${reportType.charAt(0).toUpperCase() + reportType.slice(1)} Report`,
    icon:        REPORT_ICONS[reportType] || '📄',
    type:        reportType,
    format,
    periodLabel: REPORT_PERIOD_LABELS[timePeriod] || timePeriod,
    generatedAt: new Date().toLocaleTimeString(),
  });

  _downloadBlob(blob, filename);
};

/** Re-download a previously generated report from the session blob store. */
const reDownloadReport = (report) => {
  const entry = _reportBlobs.get(report.id);
  if (entry) _downloadBlob(entry.blob, entry.filename);
};

/** Called when manager sends a natural-language report request from the reports page. */
const sendReportChatRequest = async () => {
  const msg = reportChatInput.value.trim();
  if (!msg || reportChatLoading.value) return;

  reportChatLoading.value = true;
  reportChatMessage.value = '';
  reportChatError.value   = false;

  const token = localStorage.getItem("authToken");
  try {
    // Step 1: AI intent classification
    const intentRes = await fetch(`${API_BASE_URL}/ai/report-intent`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: msg }),
    });
    const intent = await intentRes.json();

    if (!intentRes.ok || !intent.report_type) {
      reportChatMessage.value = intent.message ||
        'Please specify the report type: sales, staff, appointments, inventory, financial, or feedback.';
      reportChatError.value = true;
      return;
    }

    reportChatMessage.value = `Understood! Generating a ${intent.time_period} ${intent.report_type} report…`;

    // Step 2: Generate report
    await _callGenerateReport(
      intent.report_type,
      intent.time_period,
      reportChatFormat.value,
      intent.custom_start,
      intent.custom_end,
    );

    reportChatMessage.value =
      `Your ${intent.time_period} ${intent.report_type} report (${reportChatFormat.value.toUpperCase()}) is ready — check below or your Downloads folder!`;
    reportChatInput.value = '';

  } catch (err) {
    reportChatMessage.value = err.message || 'Something went wrong. Please try again.';
    reportChatError.value   = true;
  } finally {
    reportChatLoading.value = false;
  }
};

/** Quick Generate button handler. */
const quickGenerateReport = async () => {
  quickError.value   = '';
  quickLoading.value = true;

  if (quickPeriod.value === 'custom' && (!quickCustomStart.value || !quickCustomEnd.value)) {
    quickError.value   = 'Please select both a start and end date for the custom range.';
    quickLoading.value = false;
    return;
  }

  try {
    await _callGenerateReport(
      quickType.value,
      quickPeriod.value,
      quickFormat.value,
      quickCustomStart.value,
      quickCustomEnd.value,
    );
  } catch (err) {
    quickError.value = err.message || 'Failed to generate report. Please try again.';
  } finally {
    quickLoading.value = false;
  }
};

// ── Chatbot report trigger (from the floating assistant) ───────────────────
const _triggerReportFromChat = async (userMessage) => {
  const token = localStorage.getItem("authToken");
  try {
    const intentRes = await fetch(`${API_BASE_URL}/ai/report-intent`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userMessage }),
    });
    const intent = await intentRes.json();

    if (!intentRes.ok || !intent.report_type) {
      return intent.message ||
        'Please specify the report type: sales, staff, appointments, inventory, or feedback.';
    }

    await _callGenerateReport(
      intent.report_type,
      intent.time_period,
      'csv',
      intent.custom_start,
      intent.custom_end,
    );

    return `Done! Your ${intent.time_period} ${intent.report_type} report (CSV) is downloading now. You can also find it in the Download Reports section.`;
  } catch (err) {
    return `Report generation failed: ${err.message || 'Please try again.'}`;
  }
};

// ── Analytics helpers ──────────────────────────────────────────────────────

/** Destroy existing Chart.js instances before re-rendering. */
const _destroyCharts = () => {
  if (_chartLineInst) { _chartLineInst.destroy(); _chartLineInst = null; }
  if (_chartBarInst)  { _chartBarInst.destroy();  _chartBarInst  = null; }
  if (_chartPieInst)  { _chartPieInst.destroy();  _chartPieInst  = null; }
};

const CHART_COLORS = [
  '#d4af37','#8B6914','#3b82f6','#22c55e','#f59e0b',
  '#ef4444','#a855f7','#06b6d4','#ec4899','#84cc16',
];

/** Render Chart.js charts based on current analyticsView.type and analyticsData. */
const _renderCharts = () => {
  _destroyCharts();
  if (!analyticsData.value || !analyticsView.value) return;

  const type = analyticsView.value.type;
  const data = analyticsData.value;
  const defaultOptions = { responsive: true, maintainAspectRatio: true, plugins: { legend: { position: 'bottom', labels: { font: { size: 11 } } } } };

  if (type === 'appointments') {
    // Line: appointments by day
    if (chartLine.value && data.by_day?.length) {
      _chartLineInst = new Chart(chartLine.value, {
        type: 'line',
        data: {
          labels: data.by_day.map(d => d.date),
          datasets: [{ label: 'Appointments', data: data.by_day.map(d => d.count), borderColor: '#d4af37', backgroundColor: 'rgba(212,175,55,0.15)', tension: 0.35, fill: true, pointRadius: 4 }],
        },
        options: { ...defaultOptions, scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } } },
      });
    }
    // Bar: top services
    if (chartBar.value && data.top_services?.length) {
      _chartBarInst = new Chart(chartBar.value, {
        type: 'bar',
        data: {
          labels: data.top_services.map(s => s.name),
          datasets: [{ label: 'Bookings', data: data.top_services.map(s => s.count), backgroundColor: CHART_COLORS }],
        },
        options: { ...defaultOptions, plugins: { ...defaultOptions.plugins, legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } } },
      });
    }
    // Pie: status breakdown
    if (chartPie.value && data.by_status?.length) {
      _chartPieInst = new Chart(chartPie.value, {
        type: 'pie',
        data: {
          labels: data.by_status.map(s => s.name),
          datasets: [{ data: data.by_status.map(s => s.value), backgroundColor: CHART_COLORS }],
        },
        options: defaultOptions,
      });
    }
  } else if (type === 'sales') {
    // Line: revenue over time
    if (chartLine.value && data.by_day?.length) {
      _chartLineInst = new Chart(chartLine.value, {
        type: 'line',
        data: {
          labels: data.by_day.map(d => d.date),
          datasets: [{ label: 'Revenue (INR)', data: data.by_day.map(d => d.revenue), borderColor: '#22c55e', backgroundColor: 'rgba(34,197,94,0.12)', tension: 0.35, fill: true, pointRadius: 4 }],
        },
        options: { ...defaultOptions, scales: { y: { beginAtZero: true } } },
      });
    }
    // Bar: revenue by service
    if (chartBar.value && data.by_service?.length) {
      _chartBarInst = new Chart(chartBar.value, {
        type: 'bar',
        data: {
          labels: data.by_service.map(s => s.name),
          datasets: [{ label: 'Revenue (INR)', data: data.by_service.map(s => s.revenue), backgroundColor: CHART_COLORS }],
        },
        options: { ...defaultOptions, plugins: { ...defaultOptions.plugins, legend: { display: false } }, scales: { y: { beginAtZero: true } } },
      });
    }
  } else if (type === 'staff') {
    // Bar: appointments per staff
    if (chartBar.value && data.staff?.length) {
      _chartBarInst = new Chart(chartBar.value, {
        type: 'bar',
        data: {
          labels: data.staff.map(s => s.name),
          datasets: [
            { label: 'Total',     data: data.staff.map(s => s.total),     backgroundColor: 'rgba(212,175,55,0.7)' },
            { label: 'Completed', data: data.staff.map(s => s.completed), backgroundColor: 'rgba(34,197,94,0.7)' },
          ],
        },
        options: { ...defaultOptions, scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } } },
      });
    }
    // Line: ratings per staff
    if (chartLine.value && data.staff?.length) {
      _chartLineInst = new Chart(chartLine.value, {
        type: 'bar',
        data: {
          labels: data.staff.map(s => s.name),
          datasets: [{ label: 'Avg Rating', data: data.staff.map(s => s.rating), backgroundColor: CHART_COLORS, borderRadius: 6 }],
        },
        options: { ...defaultOptions, plugins: { ...defaultOptions.plugins, legend: { display: false } }, scales: { y: { beginAtZero: true, max: 5, ticks: { stepSize: 1 } } } },
      });
    }
  } else if (type === 'inventory') {
    // Grouped bar: current stock vs minimum
    if (chartBar.value && data.items?.length) {
      _chartBarInst = new Chart(chartBar.value, {
        type: 'bar',
        data: {
          labels: data.items.map(i => i.name),
          datasets: [
            { label: 'Current Stock', data: data.items.map(i => i.current), backgroundColor: 'rgba(59,130,246,0.7)' },
            { label: 'Min Required',  data: data.items.map(i => i.minimum), backgroundColor: 'rgba(239,68,68,0.6)',  borderDash: [4, 4] },
          ],
        },
        options: { ...defaultOptions, scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } } },
      });
    }
  } else if (type === 'feedback') {
    // Bar: ratings distribution
    if (chartBar.value && data.by_rating?.length) {
      _chartBarInst = new Chart(chartBar.value, {
        type: 'bar',
        data: {
          labels: data.by_rating.map(r => `${r.rating} Star${r.rating !== 1 ? 's' : ''}`),
          datasets: [{ label: 'Reviews', data: data.by_rating.map(r => r.count), backgroundColor: ['#ef4444','#f97316','#f59e0b','#84cc16','#22c55e'] }],
        },
        options: { ...defaultOptions, plugins: { ...defaultOptions.plugins, legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } } },
      });
    }
    // Pie: sentiment
    if (chartPie.value && data.sentiment?.length) {
      _chartPieInst = new Chart(chartPie.value, {
        type: 'doughnut',
        data: {
          labels: data.sentiment.map(s => s.name),
          datasets: [{ data: data.sentiment.map(s => s.value), backgroundColor: ['#22c55e','#f59e0b','#ef4444'] }],
        },
        options: defaultOptions,
      });
    }
  } else if (type === 'financial') {
    // Multi-line: revenue vs profit
    if (chartLine.value && data.months?.length) {
      _chartLineInst = new Chart(chartLine.value, {
        type: 'line',
        data: {
          labels: data.months.map(m => m.month),
          datasets: [
            { label: 'Revenue',  data: data.months.map(m => m.revenue), borderColor: '#22c55e', backgroundColor: 'rgba(34,197,94,0.1)',   tension: 0.35, fill: true },
            { label: 'Cost',     data: data.months.map(m => m.cost),    borderColor: '#ef4444', backgroundColor: 'rgba(239,68,68,0.07)',   tension: 0.35 },
            { label: 'Profit',   data: data.months.map(m => m.profit),  borderColor: '#d4af37', backgroundColor: 'rgba(212,175,55,0.12)',  tension: 0.35, fill: true },
          ],
        },
        options: { ...defaultOptions, scales: { y: { beginAtZero: true } } },
      });
    }
  }
};

// Watch analyticsData to re-render charts after Vue updates the DOM
watch(analyticsData, () => {
  nextTick(_renderCharts);
});

/** Open the analytics view for a given report type card. */
const openAnalyticsView = async (rt) => {
  analyticsView.value = {
    type:        rt.type,
    title:       rt.label,
    icon:        rt.icon,
    periodLabel: REPORT_PERIOD_LABELS[quickPeriod.value] || quickPeriod.value,
    dbId:        null,
    shared:      false,
    sharing:     false,
  };
  analyticsData.value    = null;
  analyticsLoading.value = true;
  analyticsError.value   = null;
  shareMessage.value     = '';

  const token = localStorage.getItem("authToken");
  try {
    const params = new URLSearchParams({ type: rt.type, period: quickPeriod.value });
    if (quickPeriod.value === 'custom' && quickCustomStart.value) params.append('custom_start', quickCustomStart.value);
    if (quickPeriod.value === 'custom' && quickCustomEnd.value)   params.append('custom_end',   quickCustomEnd.value);

    const res = await fetch(`${API_BASE_URL}/reports/analytics?${params}`, {
      headers: { Authorization: `Bearer ${token}`, "Authentication-Token": token },
    });
    if (!res.ok) throw new Error('Analytics fetch failed');
    analyticsData.value = await res.json();

    // Try to link the most recent saved report of this type/period
    const saved = savedReports.value.find(r => r.report_type === rt.type && r.time_period === quickPeriod.value);
    if (saved) {
      analyticsView.value.dbId   = saved.id;
      analyticsView.value.shared = saved.shared;
    }
  } catch (err) {
    analyticsError.value = err.message || 'Failed to load analytics.';
  } finally {
    analyticsLoading.value = false;
  }
};

/** Generate a report for a specific type+format from the card grid (no analytics view). */
const quickGenerateReportFor = async (reportType, format) => {
  quickError.value   = '';
  quickLoading.value = true;
  try {
    await _callGenerateReport(
      reportType,
      quickPeriod.value,
      format,
      quickCustomStart.value || null,
      quickCustomEnd.value   || null,
    );
    await fetchSavedReports();
  } catch (err) {
    quickError.value = err.message || 'Failed to generate report.';
  } finally {
    quickLoading.value = false;
  }
};

/** Download a report from the analytics view using current period settings. */
const downloadFromAnalytics = async (format) => {
  quickLoading.value = true;
  quickError.value   = '';
  try {
    await _callGenerateReport(
      analyticsView.value.type,
      quickPeriod.value,
      format,
      quickCustomStart.value || null,
      quickCustomEnd.value   || null,
    );
    await fetchSavedReports();
    // Update the dbId link in analyticsView if a matching saved report now exists
    const saved = savedReports.value.find(r => r.report_type === analyticsView.value.type && r.time_period === quickPeriod.value);
    if (saved) {
      analyticsView.value.dbId   = saved.id;
      analyticsView.value.shared = saved.shared;
    }
  } catch (err) {
    quickError.value = err.message || 'Failed to download report.';
  } finally {
    quickLoading.value = false;
  }
};

/** Fetch the list of saved reports from the backend. */
const fetchSavedReports = async () => {
  const token = localStorage.getItem("authToken");
  if (!token) return;
  try {
    const res = await fetch(`${API_BASE_URL}/reports`, {
      headers: { Authorization: `Bearer ${token}`, "Authentication-Token": token },
    });
    if (!res.ok) return;
    savedReports.value = await res.json();
  } catch (err) {
    console.error('Failed to fetch saved reports:', err);
  }
};

/** Download a previously saved report by ID from the backend. */
const downloadSavedReport = async (reportId, format) => {
  const token = localStorage.getItem("authToken");
  try {
    const res = await fetch(`${API_BASE_URL}/reports/${reportId}/download?format=${format}`, {
      headers: { Authorization: `Bearer ${token}`, "Authentication-Token": token },
    });
    if (!res.ok) throw new Error('Download failed');
    const blob     = await res.blob();
    const filename = `report_${reportId}.${format}`;
    _downloadBlob(blob, filename);
  } catch (err) {
    console.error('Download saved report error:', err);
  }
};

/** Share a saved report (already in DB) with the owner. */
const shareReportWithOwner = async (reportId, reportRef) => {
  const token = localStorage.getItem("authToken");
  shareMessage.value = '';
  try {
    const res = await fetch(`${API_BASE_URL}/reports/${reportId}/share`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, "Authentication-Token": token },
    });
    if (!res.ok) throw new Error('Share failed');
    shareMessage.value = 'Report shared with owner successfully!';
    if (reportRef) reportRef.shared = true;
    if (analyticsView.value?.dbId === reportId) analyticsView.value.shared = true;
    await fetchSavedReports();
    setTimeout(() => { shareMessage.value = ''; }, 4000);
  } catch (err) {
    shareMessage.value = `Failed to share: ${err.message}`;
  }
};

/** Generate both PDF + CSV silently and share with owner from the analytics view. */
const shareAnalyticsReport = async () => {
  if (!analyticsView.value) return;
  const token = localStorage.getItem("authToken");
  shareMessage.value = '';
  analyticsView.value.sharing = true;
  try {
    const body = {
      report_type:  analyticsView.value.type,
      time_period:  quickPeriod.value,
      custom_start: quickPeriod.value === 'custom' ? quickCustomStart.value : null,
      custom_end:   quickPeriod.value === 'custom' ? quickCustomEnd.value   : null,
    };
    const res = await fetch(`${API_BASE_URL}/reports/generate-and-share`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
        'Authentication-Token': token,
      },
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.message || 'Share failed');
    }
    const data = await res.json();
    shareMessage.value = 'Report (PDF + CSV) shared with owner!';
    analyticsView.value.shared = true;
    analyticsView.value.dbId   = data.id;
    await fetchSavedReports();
    setTimeout(() => { shareMessage.value = ''; }, 4000);
  } catch (err) {
    shareMessage.value = `Failed to share: ${err.message}`;
  } finally {
    analyticsView.value.sharing = false;
  }
};

// Fetch today's tasks for the current manager
const fetchManagerTasks = async () => {
  const token = localStorage.getItem("authToken");
  if (!token) return;
  try {
    const response = await fetch(`${API_BASE_URL}/ai/manager-tasks`, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token,
      },
    });
    if (!response.ok) return;
    const data = await response.json();
    managerTasks.value = data.tasks || [];
  } catch (err) {
    console.error("Failed to fetch manager tasks:", err);
  }
};

// Call backend to generate AI tasks and persist them
const generateManagerTasks = async () => {
  tasksLoading.value = true;
  tasksError.value = null;
  const token = localStorage.getItem("authToken");
  if (!token) { tasksLoading.value = false; return; }
  try {
    const response = await fetch(`${API_BASE_URL}/ai/generate-manager-tasks`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token,
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.message || 'Failed to generate tasks');
    }
    const data = await response.json();
    managerTasks.value = data.tasks || [];
  } catch (err) {
    tasksError.value = err.message || 'Failed to generate tasks. Please try again.';
  } finally {
    tasksLoading.value = false;
  }
};

// Toggle a task between pending and completed
const toggleTask = async (task) => {
  const token = localStorage.getItem("authToken");
  if (!token) return;
  const newStatus = task.status === 'pending' ? 'completed' : 'pending';
  try {
    const response = await fetch(`${API_BASE_URL}/tasks/${task.task_id}`, {
      method: 'PATCH',
      headers: {
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ status: newStatus }),
    });
    if (!response.ok) throw new Error('Failed to update task');
    task.status = newStatus;
  } catch (err) {
    console.error('Failed to toggle task:', err);
  }
};

// AI Assistant handler
const sendAIMessage = () => {
  if (!aiUserInput.value.trim()) return;

  aiMessages.value.push({ type: 'user', text: aiUserInput.value });
  const userMessage = aiUserInput.value.toLowerCase();
  aiUserInput.value = '';

  const scrollChat = () => {
    setTimeout(() => {
      const chatBox = document.querySelector('.ai-chat-messages');
      if (chatBox) chatBox.scrollTop = chatBox.scrollHeight;
    }, 0);
  };

  // Report generation — async path (checked before task checklist)
  const reportKeywords = [
    'report', 'generate report', 'download report', 'sales report',
    'staff report', 'appointment report', 'inventory report',
    'financial report', 'feedback report', 'weekly report',
    'monthly report', 'daily report', 'export', 'download csv', 'download pdf',
  ];
  if (reportKeywords.some(kw => userMessage.includes(kw))) {
    aiMessages.value.push({ type: 'assistant', text: 'On it! Classifying your report request and generating the file…' });
    scrollChat();
    _triggerReportFromChat(userMessage).then(reply => {
      aiMessages.value.push({ type: 'assistant', text: reply });
      scrollChat();
    });
    return;
  }

  // Task checklist — async path
  if (
    userMessage.includes('checklist') ||
    userMessage.includes('task') ||
    userMessage.includes('todo') ||
    userMessage.includes('to do') ||
    userMessage.includes('what should i') ||
    userMessage.includes('tasks for today') ||
    userMessage.includes('tasks today')
  ) {
    aiMessages.value.push({ type: 'assistant', text: 'Generating your AI-powered task checklist based on today\'s salon data…' });
    scrollChat();
    generateManagerTasks().then(() => {
      const count = managerTasks.value.length;
      const reply = count > 0
        ? `Done! I've created ${count} priority tasks for today. Check the task checklist on your dashboard above!`
        : (tasksError.value || 'Could not generate tasks. Please try again.');
      aiMessages.value.push({ type: 'assistant', text: reply });
      scrollChat();
    });
    return;
  }

  // Static keyword responses
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
    assistantResponse = 'The Finance section (password protected) shows your total revenue, product costs, staff salaries, overhead, and net profit. Access it from the sidebar for a complete financial overview. You can also ask me to "Generate a monthly financial report" to download a PDF or CSV!';
  } else if (userMessage.includes('issue') || userMessage.includes('problem') || userMessage.includes('error')) {
    assistantResponse = 'I\'m sorry you\'re experiencing an issue. Please describe the problem in detail, and I\'ll help you troubleshoot. Is it related to appointments, customers, services, staff, inventory, or invoices?';
  } else if (userMessage.includes('help')) {
    assistantResponse = 'I\'m here to help! I can assist you with:\n• Managing appointments & bookings\n• Customer information & preferences\n• Creating & managing services\n• Staff management & scheduling\n• Inventory & product management\n• Invoices & billing\n• Finance & reports\n• Generating a daily task checklist (just ask!)\n\nWhat would you like help with?';
  } else if (userMessage.includes('hello') || userMessage.includes('hi')) {
    assistantResponse = 'Hello! I\'m your AI Assistant for the Manager Dashboard. How can I help you today? Feel free to ask about appointments, customers, services, staff, inventory, or say "Create a task checklist for today"!';
  } else if (userMessage.includes('overview') || userMessage.includes('stats') || userMessage.includes('dashboard')) {
    assistantResponse = 'The Dashboard Overview shows you key metrics: Today\'s appointments, available staff, low stock items, and pending orders. This gives you a quick snapshot of your business for the day.';
  } else {
    assistantResponse = 'That\'s a great question! I can help with appointment management, customer details, service creation, staff management, inventory, invoices, and financial reports. You can also ask me to "Create a task checklist for today"!';
  }

  setTimeout(() => {
    aiMessages.value.push({ type: 'assistant', text: assistantResponse });
    scrollChat();
  }, 500);
};

// Product/Inventory handlers
const handleAddProduct = async () => {
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

  if (inventoryForm.value.stock < 0) {
    inventoryError.value = "Stock quantity cannot be negative";
    return;
  }

  if (inventoryForm.value.minStock < 0) {
    inventoryError.value = "Minimum stock cannot be negative";
    return;
  }

  if (!inventoryForm.value.supplier || !inventoryForm.value.supplier.trim()) {
    inventoryError.value = "Supplier is required";
    return;
  }

  if (!inventoryForm.value.supplierContact || !inventoryForm.value.supplierContact.trim()) {
    inventoryError.value = "Supplier contact is required";
    return;
  }

  if (!inventoryForm.value.supplierEmail || !inventoryForm.value.supplierEmail.trim()) {
    inventoryError.value = "Supplier email is required";
    return;
  }

  const token = localStorage.getItem("authToken");
  if (!token) {
    inventoryError.value = "You are not authenticated. Please log in again.";
    return;
  }

  const payload = {
    product_name: inventoryForm.value.name.trim(),
    product_category: inventoryForm.value.categoryName.trim(),
    stock_quantity: inventoryForm.value.stock,
    minimum_stock: inventoryForm.value.minStock,
    price: inventoryForm.value.costPrice,
    supplier_name: inventoryForm.value.supplier.trim(),
    supplier_contact: inventoryForm.value.supplierContact.trim(),
    supplier_email: inventoryForm.value.supplierEmail.trim()
  };

  console.log("Payload being sent:", payload);
  console.log("Form values:", inventoryForm.value);

  try {
    const response = await fetch(`${API_BASE_URL}/api/product`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      },
      body: JSON.stringify(payload)
    });

    const data_response = await response.json();
    if (!response.ok) {
      inventoryError.value = data_response.message || "Failed to add product";
      console.error("Product add error response:", data_response);
      return;
    }

    inventorySuccess.value = data_response.message || "Product added successfully!";
    
    // Refresh products list
    await fetchProducts();

    setTimeout(() => {
      inventoryForm.value = {
        name: "",
        categoryName: "",
        stock: 0,
        minStock: 0,
        costPrice: 0,
        supplier: "",
        supplierContact: "",
        supplierEmail: ""
      };
      inventorySuccess.value = "";
    }, 1500);
  } catch (error) {
    inventoryError.value = "Unable to connect to server. Please try again.";
    console.error("Product operation error:", error);
  }
};



const handleDeleteProduct = async (productId) => {
  if (!confirm("Are you sure you want to delete this product?")) {
    return;
  }

  const token = localStorage.getItem("authToken");
  if (!token) {
    inventoryError.value = "You are not authenticated. Please log in again.";
    return;
  }

  inventoryError.value = "";
  inventorySuccess.value = "";

  try {
    const response = await fetch(`${API_BASE_URL}/api/product/${productId}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    const data_response = await response.json();
    if (!response.ok) {
      inventoryError.value = data_response.message || "Failed to delete product";
      return;
    }

    inventorySuccess.value = data_response.message || "Product deleted successfully!";
    
    // Refresh products list
    await fetchProducts();

    setTimeout(() => {
      inventorySuccess.value = "";
    }, 1500);
  } catch (error) {
    inventoryError.value = "Unable to connect to server. Please try again.";
    console.error("Delete product error:", error);
  }
};

const handleEditProduct = (product) => {
  editingProductId.value = product.product_id || product.id;
  editProductForm.value = {
    name: product.product_desc || product.name,
    categoryName: product.product_category_name || product.categoryName,
    stock: product.product_curr_qoh || product.stock,
    minStock: product.product_min_qoh || product.minStock,
    costPrice: product.product_price || product.costPrice,
    supplier: product.product_supplier_name || product.supplier,
    supplierContact: product.product_supplier_contact || product.supplierContact || "",
    supplierEmail: product.product_supplier_email || product.supplierEmail || ""
  };
  showEditProductModal.value = true;
};

const handleSaveEditProduct = async () => {
  editProductError.value = "";
  editProductSuccess.value = "";

  if (!editProductForm.value.name) {
    editProductError.value = "Product name is required";
    return;
  }

  if (!editProductForm.value.categoryName) {
    editProductError.value = "Category is required";
    return;
  }

  if (editProductForm.value.costPrice <= 0) {
    editProductError.value = "Cost price must be greater than 0";
    return;
  }

  if (!editProductForm.value.supplier) {
    editProductError.value = "Supplier is required";
    return;
  }

  if (!editProductForm.value.supplierContact) {
    editProductError.value = "Supplier contact is required";
    return;
  }

  if (!editProductForm.value.supplierEmail) {
    editProductError.value = "Supplier email is required";
    return;
  }

  const token = localStorage.getItem("authToken");
  if (!token) {
    editProductError.value = "You are not authenticated. Please log in again.";
    return;
  }

  const payload = {
    product_name: editProductForm.value.name,
    product_category: editProductForm.value.categoryName,
    stock_quantity: editProductForm.value.stock,
    minimum_stock: editProductForm.value.minStock,
    price: editProductForm.value.costPrice,
    supplier_name: editProductForm.value.supplier,
    product_supplier_contact: editProductForm.value.supplierContact,
    product_supplier_email: editProductForm.value.supplierEmail
  };

  try {
    const response = await fetch(`${API_BASE_URL}/api/product/${editingProductId.value}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      },
      body: JSON.stringify(payload)
    });

    const data_response = await response.json();
    if (!response.ok) {
      editProductError.value = data_response.message || "Failed to update product";
      return;
    }

    editProductSuccess.value = data_response.message || "Product updated successfully!";
    
    // Refresh products list
    await fetchProducts();

    setTimeout(() => {
      showEditProductModal.value = false;
      editingProductId.value = null;
      editProductForm.value = {
        name: "",
        categoryName: "",
        stock: 0,
        minStock: 0,
        costPrice: 0,
        supplier: "",
        supplierContact: "",
        supplierEmail: ""
      };
      editProductSuccess.value = "";
    }, 1500);
  } catch (error) {
    editProductError.value = "Unable to connect to server. Please try again.";
    console.error("Update product error:", error);
  }
};

const cancelEditProduct = () => {
  showEditProductModal.value = false;
  editingProductId.value = null;
  editProductForm.value = {
    name: "",
    categoryName: "",
    stock: 0,
    minStock: 0,
    costPrice: 0,
    supplier: "",
    supplierContact: "",
    supplierEmail: ""
  };
  editProductError.value = "";
};

const viewProductDetails = (product) => {
  selectedProduct.value = product;
  showProductDetailsModal.value = true;
};

// Staff edit/delete handlers
const handleEditStaff = (staff) => {
  staffError.value = "";
  staffSuccess.value = "";
  
  // Store staff data for display in modal
  editingStaffData.value = staff;
  
  // Populate form with staff data
  staffForm.value = {
    name: staff.name,
    role: staff.role,
    email: staff.email,
    phone: staff.phone,
    skills: staff.skills || "",
    dob: staff.dob || "",
    doj: staff.doj,
    salary: staff.salary,
    username: staff.username || ""
  };
  
  isEditingStaff.value = true;
  editingStaffId.value = staff.id;
};

const cancelEditStaff = () => {
  staffForm.value = {
    name: "",
    role: "",
    email: "",
    phone: "",
    skills: "",
    dob: "",
    doj: "",
    salary: 0,
    username: ""
  };
  isEditingStaff.value = false;
  editingStaffId.value = null;
  editingStaffData.value = null;
  staffError.value = "";
  staffSuccess.value = "";
};

const handleUpdateStaff = async () => {
  staffError.value = "";
  staffSuccess.value = "";

  if (!staffForm.value.name?.trim()) {
    staffError.value = "Staff name is required";
    return;
  }

  if (!staffForm.value.role?.trim()) {
    staffError.value = "Role is required";
    return;
  }

  if (!staffForm.value.email?.trim()) {
    staffError.value = "Email is required";
    return;
  }

  if (!staffForm.value.phone?.trim()) {
    staffError.value = "Phone is required";
    return;
  }

  if (!staffForm.value.skills?.trim()) {
    staffError.value = "Skills are required";
    return;
  }

  if (!staffForm.value.dob) {
    staffError.value = "Date of birth is required";
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

  const token = localStorage.getItem("authToken");
  if (!token) {
    staffError.value = "Authentication token not found";
    return;
  }

  const payload = {
    staff_name: staffForm.value.name.trim(),
    staff_role: staffForm.value.role.trim(),
    staff_email: staffForm.value.email.trim(),
    staff_contact: staffForm.value.phone.trim(),
    staff_skills: staffForm.value.skills.trim(),
    staff_dob: staffForm.value.dob,
    staff_doj: staffForm.value.doj,
    staff_salary: staffForm.value.salary
  };

  try {
    const response = await fetch(`${API_BASE_URL}/api/staff/${editingStaffId.value}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      },
      body: JSON.stringify(payload)
    });

    if (response.ok) {
      const result = await response.json();
      console.log("Staff updated:", result);
      staffSuccess.value = "Staff member updated successfully!";
      
      // Fetch updated staff list
      await fetchStaff();
      
      // Reset form
      isEditingStaff.value = false;
      editingStaffId.value = null;
      editingStaffData.value = null;
      staffForm.value = {
        name: "",
        role: "",
        email: "",
        phone: "",
        skills: "",
        dob: "",
        doj: "",
        salary: 0,
        username: ""
      };
      
      setTimeout(() => {
        staffSuccess.value = "";
      }, 1500);
    } else {
      const error = await response.json();
      staffError.value = error.message || "Failed to update staff";
      console.error("Error updating staff:", error);
    }
  } catch (error) {
    staffError.value = "Error updating staff: " + error.message;
    console.error("Error updating staff:", error);
  }
};

const handleDeleteStaff = async (staffId) => {
  if (!confirm("Are you sure you want to delete this staff member?")) {
    return;
  }

  const token = localStorage.getItem("authToken");
  if (!token) {
    alert("Authentication token not found");
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/staff/${staffId}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (response.ok) {
      const result = await response.json();
      console.log("Staff deleted:", result);
      alert("Staff member deleted successfully!");
      
      // Fetch updated staff list
      await fetchStaff();
    } else {
      const error = await response.json();
      const errorMsg = error.message || "Failed to delete staff";
      alert("Error: " + errorMsg);
      console.error("Error deleting staff:", error);
    }
  } catch (error) {
    alert("Error deleting staff: " + error.message);
    console.error("Error deleting staff:", error);
  }
};

// Booking edit/delete handlers
const handleEditBooking = (booking) => {
  editingAppointment.value = booking;
  
  // Extract time from datetime (format: "HH:MM:SS" or "HH:MM")
  let timeValue = "";
  if (booking.datetime) {
    const timePart = booking.datetime.split('T')[1]; // Get HH:MM:SS
    if (timePart) {
      timeValue = timePart.substring(0, 5); // Get only HH:MM
    }
  } else if (booking.notes) {
    timeValue = booking.notes.substring(0, 5); // In case time is in notes
  }
  
  editAppointmentForm.value = {
    serviceIds: booking.services.map(s => s.id) || [],
    date: booking.date,
    time: timeValue,
    staffId: booking.staffId || ""
  };
  editAppointmentError.value = "";
  editAppointmentSuccess.value = "";
  showEditAppointmentModal.value = true;
};

const handleSubmitEditAppointment = async () => {
  editAppointmentError.value = "";
  editAppointmentSuccess.value = "";

  if (!editingAppointment.value) {
    editAppointmentError.value = "No appointment selected";
    return;
  }

  if (!editAppointmentForm.value.date) {
    editAppointmentError.value = "Please select a date";
    return;
  }

  if (!editAppointmentForm.value.time) {
    editAppointmentError.value = "Please select a time";
    return;
  }

  // Validate appointment date is within allowed range
  const selectedDate = new Date(editAppointmentForm.value.date);
  const minDate = new Date(minEditBookingDate.value);
  const maxDate = new Date(maxEditBookingDate.value);

  if (selectedDate < minDate || selectedDate > maxDate) {
    if (hasBridalPackageSelectedInEdit()) {
      editAppointmentError.value = `Bridal Package must be booked 1 to 6 months in advance`;
    } else {
      editAppointmentError.value = `Appointment must be scheduled today or within the next 2 days`;
    }
    return;
  }

  // Combine date and time into ISO datetime
  const appointmentDateTime = `${editAppointmentForm.value.date}T${editAppointmentForm.value.time}:00`;

  // Get staff ID if assigned
  const staffId = editAppointmentForm.value.staffId ? parseInt(editAppointmentForm.value.staffId) : null;

  const token = localStorage.getItem("authToken");
  if (!token) {
    editAppointmentError.value = "Authentication token not found";
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/appointment/${editingAppointment.value.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      },
      body: JSON.stringify({
        appointment_datetime: appointmentDateTime,
        service_ids: editAppointmentForm.value.serviceIds.length > 0 ? editAppointmentForm.value.serviceIds.map(id => parseInt(id)) : undefined,
        staff_id: staffId
      })
    });

    const data_response = await response.json();
    
    if (response.ok) {
      editAppointmentSuccess.value = "Appointment updated successfully!";
      
      // Refresh appointments list
      await fetchAppointments();
      
      // Close modal after brief success message
      setTimeout(() => {
        showEditAppointmentModal.value = false;
        editingAppointment.value = null;
        editAppointmentForm.value = {
          serviceIds: [],
          date: "",
          time: "",
          staffId: ""
        };
        editAppointmentError.value = "";
        editAppointmentSuccess.value = "";
      }, 1500);
    } else {
      editAppointmentError.value = data_response.message || "Failed to update appointment";
    }
  } catch (error) {
    console.error("Fetch error:", error);
    editAppointmentError.value = "Network error: " + error.message;
  }
};

const closeEditAppointmentModal = () => {
  showEditAppointmentModal.value = false;
  editingAppointment.value = null;
  editAppointmentForm.value = {
    serviceIds: [],
    date: "",
    time: "",
    staffId: ""
  };
  editAppointmentError.value = "";
  editAppointmentSuccess.value = "";
};

const handleSubmitEditBooking = async () => {
  // This function is deprecated - using handleSubmitEditAppointment instead
};

const cancelEditBooking = () => {
  // This function is deprecated - using closeEditAppointmentModal instead
};

const handleDeleteBooking = async (bookingId) => {
  if (!confirm("Are you sure you want to delete this appointment?")) {
    return;
  }

  const token = localStorage.getItem("authToken");
  if (!token) {
    alert("Authentication token not found");
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/appointment/${bookingId}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (response.ok) {
      alert("Appointment deleted successfully!");
      // Refresh appointments list
      await fetchAppointments();
    } else {
      const error = await response.json();
      alert("Error: " + (error.message || "Failed to delete appointment"));
    }
  } catch (error) {
    console.error("Fetch error:", error);
    alert("Network error: " + error.message);
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

const handleReplenishmentProductSelect = () => {
  // Auto-populate supplier info from selected product
  const selectedProductId = replenishmentForm.value.productId;
  if (selectedProductId) {
    const selectedProduct = data.value.products.find(p => p.id === selectedProductId);
    if (selectedProduct) {
      replenishmentForm.value.supplier = selectedProduct.supplier || "Not specified";
    }
  } else {
    replenishmentForm.value.supplier = "";
  }
};

const handleAddReplenishment = async () => {
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

  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      replenishmentError.value = "Authentication required. Please login again.";
      return;
    }

    const payload = {
      product_id: parseInt(replenishmentForm.value.productId),
      quantity: parseInt(replenishmentForm.value.quantity)
      // Note: service_id is optional - manager replenishment doesn't require it
    };

    console.log("Creating replenishment with payload:", payload);

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
      const product = data.value.products.find(p => p.id === parseInt(replenishmentForm.value.productId));
      const productName = product?.name || "Product";
      
      // Update product stock if returned from backend
      if (result.updated_stock !== undefined && product) {
        product.currentStock = result.updated_stock;
      }
      
      // Reset form
      replenishmentForm.value = {
        productId: "",
        quantity: 1,
        reason: "",
        supplier: ""
      };
      
      // Refresh inventory transactions to show newly created replenishment
      await fetchManagerInventoryTransactions();
      
      console.log(`Replenishment added for ${productName}`, result);
    } else {
      replenishmentError.value = result.message || "Failed to add replenishment";
      console.error("Error adding replenishment:", result);
    }
  } catch (error) {
    replenishmentError.value = "Unable to connect to server. Please try again.";
    console.error("Network error:", error);
  }
};

const handleCreateInvoiceFromAppointment = (appt) => {
  // Pre-fill invoice form with appointment details
  // Extract first service ID from services array, or use serviceId if available
  const serviceId = appt.services && appt.services.length > 0 ? appt.services[0].id : (appt.serviceId || null);
  
  // Create a hidden select event to trigger dropdown selection
  const selectElement = document.querySelector('#invoice-appointment');
  if (selectElement) {
    selectElement.value = appt.id;
  }
  
  invoiceForm.value = {
    appointmentId: appt.id,
    customerId: appt.customerId,
    staffId: appt.staffId,
    serviceId: serviceId,
    date: appt.date,
    paymentType: "cash",
    discount: 0,
    services: appt.services || []
  };
  currentView.value = "invoices";
  
  // Mark appointment as invoice generated
  const index = data.value.appointments.findIndex(b => b.id === appt.id);
  if (index > -1) {
    data.value.appointments[index].invoiceGenerated = true;
  }
  
  console.log(`📄 Creating invoice for appointment #${appt.id} (${getCustomerName(appt.customerId)}) - Staff: ${appt.staff_name}, Services:`, appt.services);
  
  // Scroll to invoice form after a brief delay to allow DOM update
  setTimeout(() => {
    const invoiceFormElement = document.querySelector('#invoice-form');
    if (invoiceFormElement) {
      invoiceFormElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }, 100);
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

// Fetch products from API
const fetchProducts = async () => {
  const token = localStorage.getItem("authToken");
  if (!token) {
    console.error("Not authenticated");
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/product`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (response.ok) {
      const products = await response.json();
      // Update the store data with fetched products, converting backend field names to frontend names
      appStore.data.products = products.map(p => ({
        product_id: p.product_id,
        id: p.product_id,
        product_desc: p.product_desc,
        name: p.product_desc,
        product_category_name: p.product_category_name,
        categoryName: p.product_category_name,
        product_price: p.product_price,
        price: p.product_price,
        costPrice: p.product_price,
        product_min_qoh: p.product_min_qoh,
        minStock: p.product_min_qoh,
        product_curr_qoh: p.product_curr_qoh,
        currentStock: p.product_curr_qoh,
        stock: p.product_curr_qoh,
        product_supplier_name: p.product_supplier_name,
        supplier: p.product_supplier_name,
        product_supplier_contact: p.product_supplier_contact,
        supplierContact: p.product_supplier_contact,
        product_supplier_email: p.product_supplier_email,
        supplierEmail: p.product_supplier_email,
        product_low_stock_alert: p.product_low_stock_alert,
        unit: "unit"
      }));
    }
  } catch (error) {
    console.error("Error fetching products:", error);
  }
};

// Fetch Salon Config from API
const fetchSalonConfig = async () => {
  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      console.error("Not authenticated");
      return;
    }
    
    const response = await fetch(`${API_BASE_URL}/api/salon-config`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      salonConfigList.value = Array.isArray(data) ? data : [data];
    } else {
      console.error("Failed to fetch salon config:", response.status);
    }
  } catch (error) {
    console.error("Error fetching salon config:", error);
  }
};

// Handle Edit Setting
const handleEditSetting = (setting) => {
  editingSettingData.value = setting;
  editSettingForm.value = {
    param_name: setting.param_name,
    param_value: setting.param_value,
    from_date: setting.from_date ? setting.from_date.split('T')[0] : '',
    to_date: setting.to_date ? setting.to_date.split('T')[0] : ''
  };
  showEditSettingModal.value = true;
  settingError.value = "";
  settingSuccess.value = "";
};

// Save Setting
const handleSaveSetting = async () => {
  settingError.value = "";
  settingSuccess.value = "";
  
  if (!editSettingForm.value.param_value.trim()) {
    settingError.value = "Setting value is required";
    return;
  }
  
  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      settingError.value = "Not authenticated";
      return;
    }
    
    const response = await fetch(`${API_BASE_URL}/api/salon-config/${editingSettingData.value.setting_id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      },
      body: JSON.stringify({
        param_value: editSettingForm.value.param_value,
        from_date: editSettingForm.value.from_date,
        to_date: editSettingForm.value.to_date
      })
    });
    
    if (response.ok) {
      settingSuccess.value = "Setting updated successfully";
      showEditSettingModal.value = false;
      fetchSalonConfig();
      setTimeout(() => {
        settingSuccess.value = "";
      }, 3000);
    } else {
      settingError.value = "Failed to update setting";
    }
  } catch (error) {
    console.error("Error updating setting:", error);
    settingError.value = "Error updating setting";
  }
};

const formatDate = (dateStr) => {
  if (!dateStr) return 'N/A';
  const date = new Date(dateStr);
  return date.toLocaleDateString();
};

const fetchBriefing = async () => {
  briefingLoading.value = true;
  briefingError.value = null;
  try {
    const token = localStorage.getItem("authToken");
    if (!token) return;
    const response = await fetch(`${API_BASE_URL}/ai/daily-briefing`, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token,
      },
    });
    if (!response.ok) throw new Error("Request failed");
    briefingData.value = await response.json();
  } catch (err) {
    briefingError.value = "Could not load AI briefing.";
    console.error("Briefing fetch error:", err);
  } finally {
    briefingLoading.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
  // Fetch AI daily briefing
  fetchBriefing();
  // Fetch manager profile data for name display
  fetchManagerProfileData();
  // Fetch today's AI tasks
  fetchManagerTasks();
  // Fetch saved reports list
  fetchSavedReports();
  // Fetch products, customers, staff, and services from API on component mount
  fetchProducts();
  fetchCustomers();
  fetchStaff();
  fetchServices();
  fetchAppointments();
  fetchInvoices();
  // Fetch manager attendance data
  fetchManagerAttendance();
  // Fetch daily appointment counts
  fetchDailyAppointmentCounts();
  // Fetch today's appointments for invoice creation
  fetchTodaysAppointmentsForInvoice();
  // Fetch manager inventory transactions
  fetchManagerInventoryTransactions();
  // Fetch manager wholesale orders
  fetchManagerOrders();
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

/* ── Task Checklist ─────────────────────────────────────── */
.generate-tasks-btn {
  background: var(--gold);
  color: white;
  border: none;
  border-radius: 6px;
  padding: 7px 14px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, opacity 0.2s;
}
.generate-tasks-btn:hover { background: var(--gold-dark); }
.generate-tasks-btn:disabled { opacity: 0.6; cursor: not-allowed; }

.task-section-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 10px;
}

.task-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 9px 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s;
  margin-bottom: 6px;
}
.task-item:hover { background: var(--light-bg); }
.task-item.completed-task { opacity: 0.65; }

.task-checkbox {
  font-size: 18px;
  line-height: 1.2;
  flex-shrink: 0;
}
.pending-cb  { color: var(--gold-dark); }
.completed-cb { color: #38a169; }

.task-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.task-description {
  font-size: 13px;
  color: var(--charcoal);
  line-height: 1.4;
}

.task-badge {
  display: inline-block;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 1px 7px;
  border-radius: 10px;
  width: fit-content;
  background: #e8e0d5;
  color: var(--text-muted);
}
.badge-appointments { background: #ebf4ff; color: #2b6cb0; }
.badge-inventory    { background: #fff3cd; color: #856404; }
.badge-feedback     { background: #fce8e8; color: #c53030; }
.badge-staff        { background: #e6f4ea; color: #276749; }
.badge-general      { background: #e8e0d5; color: var(--text-muted); }

/* ── Report Generation UI ───────────────────────────────────────────────── */
.report-ai-msg {
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  line-height: 1.5;
  margin-top: 4px;
}
.report-ai-msg--success {
  background: #f0fff4;
  border: 1px solid #c6f6d5;
  color: #276749;
}
.report-ai-msg--error {
  background: #fff5f5;
  border: 1px solid #fed7d7;
  color: #c53030;
}

.report-quick-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  align-items: flex-start;
}
@media (max-width: 900px) {
  .report-quick-row { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 560px) {
  .report-quick-row { grid-template-columns: 1fr; }
}

.report-quick-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.report-quick-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  color: var(--text-muted);
}

.gen-report-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 10px;
  border-radius: 8px;
  border: 1px solid var(--border);
  margin-bottom: 8px;
  transition: background 0.15s;
}
.gen-report-item:hover {
  background: var(--light-bg);
}
.gen-report-item:last-child {
  margin-bottom: 0;
}

/* ── Report type cards ──────────────────────────────────────────────────── */
.report-card {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 18px 16px 14px;
  border: 1px solid var(--border);
  border-radius: 10px;
  background: white;
  transition: box-shadow 0.2s, border-color 0.2s;
}
.report-card:hover {
  border-color: var(--gold);
  box-shadow: 0 4px 16px rgba(212,175,55,0.15);
}
.report-card-icon {
  font-size: 28px;
}
.report-card-title {
  font-weight: 700;
  font-size: 14px;
  color: var(--charcoal);
}
.report-card-desc {
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.4;
  flex: 1;
}
.report-card-actions {
  display: flex;
  gap: 6px;
  margin-top: 6px;
  flex-wrap: wrap;
}
</style>

