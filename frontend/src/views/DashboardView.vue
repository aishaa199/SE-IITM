<template>
  <div class="content-layout">
    <!-- Mobile Menu Toggle -->
    <div style="display: none; position: fixed; top: 16px; left: 16px; z-index: 1001; background: var(--surface); border-radius: 8px; border: 1px solid var(--border); padding: 8px; cursor: pointer" @click="sidebarOpen = !sidebarOpen" class="mobile-menu-toggle">
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
        <div :class="['nav-item', { active: currentView === 'dashboard' }]" @click="currentView = 'dashboard'; sidebarOpen = false">
          <span class="nav-icon"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg></span> Dashboard
        </div>
        <div :class="['nav-item', { active: currentView === 'bookings' }]" @click="currentView = 'bookings'; fetchSalonConfig(); sidebarOpen = false">
          <span class="nav-icon"><svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg></span> Appointments
        </div>
        <div :class="['nav-item', { active: currentView === 'services' }]" @click="currentView = 'services'; sidebarOpen = false">
          <span class="nav-icon"><svg viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg></span> Services
        </div>

        <div class="nav-section">Management</div>
        <div :class="['nav-item', { active: currentView === 'customers' }]" @click="currentView = 'customers'; sidebarOpen = false">
          <span class="nav-icon"><svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></span> Customers
        </div>
        <div :class="['nav-item', { active: currentView === 'staff-by-day' }]" @click="currentView = 'staff-by-day'; sidebarOpen = false">
          <span class="nav-icon"><svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><polyline points="9 16 11 18 15 14"/></svg></span> Staff by Day
        </div>
        <div :class="['nav-item', { active: currentView === 'staff' }]" @click="currentView = 'staff'; sidebarOpen = false">
          <span class="nav-icon"><svg viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></span> Staff
        </div>
        <div :class="['nav-item', { active: currentView === 'rewards' }]" @click="currentView = 'rewards'; fetchRewardsSettings(); sidebarOpen = false">
          <span class="nav-icon"><svg viewBox="0 0 24 24"><polyline points="20 12 20 22 4 22 4 12"/><rect x="2" y="7" width="20" height="5"/><line x1="12" y1="22" x2="12" y2="7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/></svg></span> Rewards
        </div>
        <div :class="['nav-item', { active: currentView === 'invoices' }]" @click="currentView = 'invoices'; fetchInvoices(); sidebarOpen = false">
          <span class="nav-icon"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></span> Invoices
        </div>

        <div class="nav-section">Operations</div>
        <div :class="['nav-item', { active: currentView === 'inventory' }]" @click="currentView = 'inventory'">
          <span class="nav-icon"><svg viewBox="0 0 24 24"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg></span> Inventory
        </div>
        <div :class="['nav-item', { active: currentView === 'orders' }]" @click="currentView = 'orders'">
          <span class="nav-icon"><svg viewBox="0 0 24 24"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg></span> Orders
        </div>
        <div :class="['nav-item', { active: currentView === 'finance' }]" @click="handleFinanceAccess">
          <span class="nav-icon"><svg viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></span> Finance
        </div>
        <div :class="['nav-item', { active: currentView === 'reports' }]" @click="handleReportsAccess">
          <span class="nav-icon"><svg viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg></span> Download Reports
        </div>

        <div class="nav-section">Settings</div>
        <div :class="['nav-item', { active: currentView === 'settings' }]" @click="currentView = 'settings'; fetchSalonConfig()">
          <span class="nav-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg></span> Salon Settings
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
          <div v-if="showProfileMenu" class="profile-dropdown" @click.stop>
            <button class="profile-menu-item" @click="currentView = 'profile'; showProfileMenu = false">
              👤 Profile
            </button>
            <button class="profile-menu-item" @click="showChangePasswordModal = true; showProfileMenu = false">
              🔑 Change Password
            </button>
            <button class="profile-menu-item profile-menu-danger" @click="handleLogout">
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
          <button class="notif-btn" @click="toggleNotificationPanel">
            🔔
            <span v-if="unreadCount > 0" class="notif-badge">{{ unreadCount }}</span>
          </button>
        </div>
      </div>

      <!-- Notification Panel -->
      <div v-if="showNotificationPanel" class="notification-panel">
        <div class="notification-panel-header">
          <h3>Notifications</h3>
          <div class="notification-header-actions">
            <button 
              v-if="unreadCount > 0"
              @click="markAllNotificationsAsRead" 
              class="mark-all-btn"
              title="Mark all as read"
            >
              ✓ Mark All
            </button>
            <button @click="showNotificationPanel = false" class="close-btn">✕</button>
          </div>
        </div>
        
        <div class="notification-panel-content">
          <!-- Loading state -->
          <div v-if="notificationsLoading" class="notification-loading">
            <p>Loading notifications...</p>
          </div>
          
          <!-- Empty state -->
          <div v-else-if="unreadNotifications.length === 0" class="notification-empty">
            <p>No unread notifications</p>
          </div>
          
          <!-- Unread Notifications list -->
          <div v-else class="notifications-list">
            <div v-for="notif in unreadNotifications" :key="notif.id" class="notification-item">
              <div class="notification-content">
                <div class="notification-subject">{{ notif.subject }}</div>
                <div class="notification-message">{{ notif.message }}</div>
                <div class="notification-time">{{ new Date(notif.created_at).toLocaleString('en-IN') }}</div>
              </div>
              <button 
                @click="markNotificationAsRead(notif.id)" 
                class="mark-read-btn"
              >
                Mark as Read
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Page Content -->
      <div class="page-content">
        <!-- DASHBOARD VIEW -->
        <div v-if="currentView === 'dashboard'" class="fade-in">

          <!-- AI Daily Briefing Card -->
          <div v-if="!briefingDismissed" style="margin-bottom: 24px; border-radius: 12px; overflow: hidden; background: linear-gradient(135deg, #8B6914 0%, #C9A96E 60%, #b8945a 100%); box-shadow: 0 4px 20px rgba(139,105,20,0.35); border: 1px solid rgba(255,220,140,0.3);">

            <!-- Loading state -->
            <div v-if="briefingLoading" style="padding: 32px; text-align: center; color: rgba(255,255,255,0.9);">
              <div style="font-size: 30px; margin-bottom: 10px;">✨</div>
              <div style="font-size: 14px; opacity: 0.8;">Generating your AI briefing…</div>
            </div>

            <!-- Error state -->
            <div v-else-if="briefingError" style="padding: 20px 24px; display: flex; align-items: center; justify-content: space-between; color: rgba(255,255,255,0.9);">
              <span style="font-size: 14px; opacity: 0.85;">⚠️ {{ briefingError }}</span>
              <div style="display: flex; gap: 8px;">
                <button @click="fetchBriefing()" style="background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3); color: #fff; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 600;">Retry</button>
                <button @click="briefingDismissed = true" style="background: transparent; border: none; color: rgba(255,255,255,0.6); cursor: pointer; font-size: 18px; line-height: 1;">✕</button>
              </div>
            </div>

            <!-- Briefing content -->
            <div v-else-if="briefingData" style="padding: 24px; color: rgba(255,255,255,0.92);">
              <!-- Header row -->
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
                <div>
                  <div style="font-size: 20px; font-weight: 700; margin-bottom: 4px; color: #fff;">{{ briefingData.greeting }}</div>
                  <div style="font-size: 14px; color: rgba(255,255,255,0.75);">{{ briefingData.summary }}</div>
                </div>
                <div style="display: flex; gap: 8px; flex-shrink: 0; margin-left: 16px;">
                  <button @click="fetchBriefing()" title="Refresh briefing" style="background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3); color: #fff; width: 32px; height: 32px; border-radius: 50%; cursor: pointer; font-size: 15px; display: flex; align-items: center; justify-content: center;">↻</button>
                  <button @click="briefingDismissed = true" title="Dismiss" style="background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3); color: #fff; width: 32px; height: 32px; border-radius: 50%; cursor: pointer; font-size: 13px; display: flex; align-items: center; justify-content: center;">✕</button>
                </div>
              </div>

              <!-- Divider -->
              <div style="height: 1px; background: rgba(255,255,255,0.18); margin-bottom: 18px;"></div>

              <!-- Insights + Recommendations columns -->
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                  <div style="font-size: 11px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; color: rgba(255,255,255,0.55); margin-bottom: 10px;">Key Insights</div>
                  <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px;">
                    <li v-for="(insight, i) in briefingData.insights" :key="'ins-' + i" style="font-size: 13px; padding-left: 18px; position: relative; color: rgba(255,255,255,0.88); line-height: 1.45;">
                      <span style="position: absolute; left: 0; color: #F0DEB0; font-size: 16px; line-height: 1;">•</span>{{ insight }}
                    </li>
                  </ul>
                </div>
                <div>
                  <div style="font-size: 11px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; color: rgba(255,255,255,0.55); margin-bottom: 10px;">Recommendations</div>
                  <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px;">
                    <li v-for="(rec, i) in briefingData.recommendations" :key="'rec-' + i" style="font-size: 13px; padding-left: 18px; position: relative; color: rgba(255,255,255,0.88); line-height: 1.45;">
                      <span style="position: absolute; left: 0; color: #7ec8a0; font-size: 14px; line-height: 1.1;">→</span>{{ rec }}
                    </li>
                  </ul>
                </div>
              </div>

              <div v-if="briefingData.ai_error" style="margin-top: 14px; font-size: 11px; color: rgba(255,255,255,0.4);">Note: AI unavailable — showing data-driven fallback.</div>
            </div>

            <!-- Initial state (no data yet, not loading) -->
            <div v-else style="padding: 28px; text-align: center; color: rgba(255,255,255,0.9);">
              <div style="font-size: 28px; margin-bottom: 10px;">🤖</div>
              <div style="font-size: 14px; opacity: 0.75; margin-bottom: 16px;">Get your AI-powered daily briefing</div>
              <button @click="fetchBriefing()" style="background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.35); color: #fff; padding: 8px 22px; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 600;">Generate Briefing</button>
            </div>
          </div>
          <!-- End AI Daily Briefing Card -->

          <!-- AI Task Checklist Card -->
          <div style="margin-bottom: 24px; background: var(--surface); border-radius: 14px; border: 1px solid var(--border); box-shadow: var(--shadow-sm);">
            <div style="padding: 16px 20px; border-bottom: 1px solid var(--divider); display: flex; justify-content: space-between; align-items: center;">
              <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 18px;">✅</span>
                <span style="font-weight: 600; font-size: 15px; color: var(--text); letter-spacing: 0.01em;">Today's AI Tasks</span>
                <span v-if="managerTasks.length > 0" style="background: rgba(212,175,55,0.15); color: var(--gold-bright); border-radius: 10px; padding: 2px 8px; font-size: 11px; font-weight: 700; border: 1px solid rgba(212,175,55,0.28);">{{ pendingTasks.length }} left</span>
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
          <div class="card" style="margin-bottom: 24px; border-left: 3px solid var(--gold);">
            <div class="card-body">
              <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px">
                <span style="font-size: 24px">👥</span>
                <div>
                  <div style="font-weight: 600; color: var(--text); font-size: 15px; letter-spacing: 0.01em">
                    Available Staff Today
                  </div>
                  <div style="font-size: 12px; color: var(--text-muted)">
                    {{ todayAvailableStaff.length }} staff member{{ todayAvailableStaff.length !== 1 ? 's' : '' }} present
                  </div>
                </div>
              </div>
              <div v-if="todayAvailableStaff.length > 0" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px">
                <div v-for="staff in todayAvailableStaff" :key="staff.id" style="background: var(--light-bg); border: 1px solid rgba(212,175,55,0.2); border-radius: 10px; padding: 12px; transition: all 0.2s">
                  <div style="display: flex; align-items: flex-start; gap: 8px">
                    <span style="font-size: 20px; flex-shrink: 0">✓</span>
                    <div style="flex: 1; min-width: 0">
                      <div style="font-weight: 600; color: var(--text); font-size: 14px; margin-bottom: 4px">{{ staff.name }}</div>
                      <div style="font-size: 12px; color: var(--text-muted); line-height: 1.4">
                        {{ staff.skills || 'Skills not specified' }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else style="text-align: center; padding: 20px; color: var(--text-muted); font-size: 14px">
                <div style="font-size: 32px; margin-bottom: 8px">😴</div>
                No staff available today
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
                <div v-for="group in groupedTodayAppointments" :key="group.customerId" style="padding: 16px; background: var(--light-bg); border-radius: var(--radius); border-left: 4px solid var(--gold); margin-bottom: 12px">
                  <!-- Group header with date/time -->
                  <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid var(--border)">
                    <div>
                      <div style="font-weight: 600; font-size: 14px">{{ group.customerName }}</div>
                      <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px">{{ getTimeFromDate(group.appointments[0].datetime) }} • {{ group.appointments[0].date }}</div>
                    </div>
                    <button class="btn btn-sm btn-primary" @click="handleCreateInvoiceFromAppointment(group.appointments[0])" style="padding: 6px 12px; font-size: 12px">
                      📄 Invoice
                    </button>
                  </div>
                  
                  <!-- Services in this group -->
                  <div style="display: grid; gap: 8px">
                    <div v-for="appt in group.appointments" :key="appt.id" style="display: flex; justify-content: space-between; align-items: center; font-size: 13px; padding: 8px; background: var(--surface); border-radius: 6px">
                      <div style="flex: 1">
                        <div style="font-weight: 600">{{ getServiceName(appt.serviceId) }}</div>
                        <div class="text-muted" style="font-size: 11px">Staff: {{ getStaffName(appt.staffId) || "Unassigned" }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Alerts Widget -->
            <div class="card">
              <div class="card-header">
                <h3 class="card-title">⚡ Alerts & Notifications</h3>
              </div>
              <div class="card-body">
                <div v-if="unreadNotifications.length === 0" class="empty-state">
                  <div class="empty-state-icon">✅</div>
                  <div class="empty-state-text">All systems operational</div>
                </div>
                <div v-for="notif in unreadNotifications" :key="notif.id" class="alert-item warning">
                  <div class="alert-icon">⚠️</div>
                  <div style="flex: 1">
                    <div class="alert-title">{{ notif.subject }}</div>
                    <div class="alert-message">{{ notif.message }}</div>
                  </div>
                  <div class="alert-time">{{ new Date(notif.created_at).toLocaleString('en-IN', { hour: '2-digit', minute: '2-digit' }) }}</div>
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
                  <input 
                    v-model="bookingServiceSearch"
                    type="text"
                    class="form-input"
                    placeholder="Search services..."
                    style="margin-bottom: 12px"
                  />
                  <div style="border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 12px; max-height: 300px; overflow-y: auto">
                    <div v-for="service in data.services.filter(s => getServiceStatus(s) === 'Active' && s.name.toLowerCase().includes(bookingServiceSearch.toLowerCase()))" :key="service.id" style="display: flex; align-items: center; margin-bottom: 12px">
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
                      <option v-for="time in availableTimeSlots" :key="time" :value="time">
                        {{ time }}
                      </option>
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
                  <div style="display: flex; flex-direction: column; gap: 4px">
                    <div class="booking-time">{{ getTimeFromDate(appt.datetime) }}</div>
                    <div style="font-size: 11px; color: var(--text-muted)">{{ appt.date }}</div>
                  </div>
                  <div>
                    <div style="font-weight: 600">{{ getCustomerName(appt.customerId) }}</div>
                    <div class="text-muted">{{ getServiceName(appt.serviceId) }}</div>
                  </div>
                </div>
                <div style="display: flex; align-items: center; justify-content: space-between">
                  <div style="display: flex; align-items: center; gap: 12px; flex: 1">
                    <div class="text-muted" style="font-size: 12px">Staff: {{ getStaffName(appt.staffId) || "Unassigned" }}</div>
                    <span :class="['badge', apptStatusBadge(appt.status)]" :title="apptStatusLabel(appt.status)" :style="{ color: apptStatusColor(appt.status), fontWeight: '600' }">{{ apptStatusLabel(appt.status) }}</span>
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
          <div ref="serviceFormRef" class="card" style="margin-bottom: 20px">
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
                      :min="today()"
                    />
                  </div>

                  <div class="form-group">
                    <label for="service-to-date">To Date</label>
                    <input 
                      id="service-to-date"
                      v-model="serviceForm.toDate"
                      type="date"
                      class="form-input"
                      :min="today()"
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
              <div style="margin-bottom: 16px; display: flex; gap: 12px; align-items: flex-end; flex-wrap: wrap">
                <div style="flex: 1; min-width: 200px">
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
                <div style="flex: 1; min-width: 200px">
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
                <div style="flex: 1; min-width: 200px">
                  <label for="service-status-filter" style="display: block; font-size: 12px; color: var(--text-muted); margin-bottom: 4px">Status</label>
                  <select 
                    id="service-status-filter"
                    v-model="serviceStatusFilter"
                    class="form-input"
                    style="width: 100%"
                  >
                    <option value="">All Status</option>
                    <option value="Active">Active</option>
                    <option value="Disabled">Disabled</option>
                  </select>
                </div>
              </div>
              <div class="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th style="cursor: pointer" @click="toggleSort('services', 'name')">Service Name {{ getSortIndicator('services', 'name') }}</th>
                      <th style="cursor: pointer" @click="toggleSort('services', 'categoryId')">Category {{ getSortIndicator('services', 'categoryId') }}</th>
                      <th style="cursor: pointer; text-align: right" @click="toggleSort('services', 'price')">Price {{ getSortIndicator('services', 'price') }}</th>
                      <th style="cursor: pointer" @click="toggleSort('services', 'duration')">Duration (min) {{ getSortIndicator('services', 'duration') }}</th>
                      <th>From Date</th>
                      <th>To Date</th>
                      <th>Status</th>
                      <th>Products Required</th>
                      <th>Rating</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="service in paginatedServices" :key="service.id">
                      <td>{{ service.name }}</td>
                      <td>{{ getCategoryName(service.categoryId) }}</td>
                      <td style="text-align: right">₹{{ service.price }}</td>
                      <td>{{ service.duration }}</td>
                      <td style="font-size: 12px">{{ service.fromDate || '-' }}</td>
                      <td style="font-size: 12px">{{ service.toDate || '-' }}</td>
                      <td>
                        <span v-if="getServiceStatus(service) === 'Active'" style="background: rgba(45,138,78,0.15); color: #5cba7d; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; border: 1px solid rgba(45,138,78,0.28)">✓ Active</span>
                        <span v-else-if="getServiceStatus(service) === 'Disabled'" style="background: rgba(192,57,43,0.15); color: #f08070; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; border: 1px solid rgba(192,57,43,0.28)">⊘ Disabled</span>
                        <span v-else style="background: rgba(192,57,43,0.10); color: #f08070; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; border: 1px solid rgba(192,57,43,0.22)">✗ Inactive</span>
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
              <!-- Pagination Controls -->
              <div v-if="totalPagesServices > 1" style="display: flex; align-items: center; justify-content: center; gap: 12px; margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--border)">
                <button :disabled="currentPageServices === 1" @click="goToPageServices(currentPageServices - 1)" class="btn btn-sm btn-outline" title="Previous page">← Previous</button>
                <span style="font-size: 14px; font-weight: 600">Page {{ currentPageServices }} of {{ totalPagesServices }}</span>
                <button :disabled="currentPageServices === totalPagesServices" @click="goToPageServices(currentPageServices + 1)" class="btn btn-sm btn-outline" title="Next page">Next →</button>
              </div>
            </div>
          </div>
        </div>

        <!-- CUSTOMERS VIEW -->
        <div v-if="currentView === 'customers'" class="fade-in">
          <!-- Add Customer Form -->
          <div ref="customerFormRef" class="card" style="margin-bottom: 20px">
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
                      :max="todayDate"
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
              <div style="margin-bottom: 16px; display: flex; gap: 12px; align-items: flex-end; flex-wrap: wrap">
                <div style="flex: 1; min-width: 200px">
                  <label style="display: block; font-size: 12px; color: var(--text-muted); margin-bottom: 4px">Name or Email</label>
                  <input 
                    v-model="customerName"
                    type="text" 
                    placeholder="🔍 Filter by name or email..." 
                    class="form-input"
                    style="width: 100%"
                  />
                </div>
                <div style="flex: 1; min-width: 200px">
                  <label style="display: block; font-size: 12px; color: var(--text-muted); margin-bottom: 4px">Customer Type</label>
                  <select 
                    v-model="customerTypeFilter"
                    class="form-input"
                    style="width: 100%"
                  >
                    <option value="">All Types</option>
                    <option value="VIP">VIP</option>
                    <option value="Regular">Regular</option>
                    <option value="Walk-in">Walk-in</option>
                  </select>
                </div>
              </div>
              <div class="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th style="cursor: pointer" @click="toggleSort('customers', 'name')">Name {{ getSortIndicator('customers', 'name') }}</th>
                      <th>Email</th>
                      <th style="cursor: pointer" @click="toggleSort('customers', 'phone')">Phone {{ getSortIndicator('customers', 'phone') }}</th>
                      <th>Customer Type</th>
                      <th style="cursor: pointer; text-align: right" @click="toggleSort('customers', 'totalSpent')">Total Spent {{ getSortIndicator('customers', 'totalSpent') }}</th>
                      <th>Available Rewards</th>
                      <th>Preferences</th>
                      <th style="cursor: pointer; text-align: center" @click="toggleSort('customers', 'noOfVisits')">Visits {{ getSortIndicator('customers', 'noOfVisits') }}</th>
                      <th>Address</th>
                      <th>Registered</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="customer in paginatedCustomers" :key="customer.id" @click="viewCustomerVisits(customer)" style="cursor: pointer; transition: background-color 0.2s" @mouseenter="$event.target.parentElement.style.backgroundColor = 'var(--light-bg)'" @mouseleave="$event.target.parentElement.style.backgroundColor = 'transparent'">
                      <td>{{ customer.name }}</td>
                      <td>{{ customer.email }}</td>
                      <td>{{ customer.phone }}</td>
                      <td><span class="badge" :style="{ background: customer.customerType === 'VIP' ? '#FFD700' : '#95a5a6', color: customer.customerType === 'VIP' ? '#000' : '#fff', padding: '4px 8px', borderRadius: '12px', fontSize: '11px', fontWeight: '600' }">{{ customer.customerType || 'Normal' }}</span></td>
                      <td style="text-align: right; font-weight: 600; color: var(--success)">₹{{ customer.totalSpent || 0 }}</td>
                      <td style="text-align: center; font-weight: 600; color: var(--gold)">🎁 {{ customer.pointsBalance || 0 }}</td>
                      <td style="font-size: 12px; color: var(--text-muted)">{{ customer.preferences || '-' }}</td>
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
              <!-- Pagination Controls -->
              <div v-if="totalPagesCustomers > 1" style="display: flex; align-items: center; justify-content: center; gap: 12px; margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--border)">
                <button :disabled="currentPageCustomers === 1" @click="goToPageCustomers(currentPageCustomers - 1)" class="btn btn-sm btn-outline" title="Previous page">← Previous</button>
                <span style="font-size: 14px; font-weight: 600">Page {{ currentPageCustomers }} of {{ totalPagesCustomers }}</span>
                <button :disabled="currentPageCustomers === totalPagesCustomers" @click="goToPageCustomers(currentPageCustomers + 1)" class="btn btn-sm btn-outline" title="Next page">Next →</button>
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
              <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 24px; flex-wrap: wrap">
                <label style="font-weight: 600">Select Date:</label>
                <input 
                  v-model="selectedStaffDate" 
                  type="date" 
                  class="form-input"
                  style="max-width: 200px"
                  :max="new Date().toISOString().split('T')[0]"
                />
                <button 
                  @click="handleMarkStaffAbsentWithNotifications" 
                  class="btn btn-primary"
                  style="padding: 8px 16px; font-size: 13px; background: #e74c3c"
                  title="Mark all unmarked staff as absent for today and send notifications to manager"
                >
                  🔔 Mark All Absent & Notify
                </button>
              </div>

              <div v-if="(appStore.data?.staff || []).length === 0" style="text-align: center; padding: 32px; color: var(--text-muted)">
                <div style="font-size: 32px; margin-bottom: 12px">📭</div>
                <div style="font-size: 16px">No staff available</div>
              </div>

              <div v-else style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px">
                <div v-for="staff in staffForSelectedDay" :key="staff.id" style="border: 1px solid var(--border); border-radius: 8px; padding: 20px; background: var(--light-bg); transition: all 0.3s ease; position: relative" @mouseenter="hoveredStaff = staff.id" @mouseleave="hoveredStaff = null" :style="{ boxShadow: hoveredStaff === staff.id ? '0 8px 24px rgba(212, 175, 55, 0.2)' : 'none', borderColor: hoveredStaff === staff.id ? 'var(--gold)' : 'var(--border)', opacity: staff.attendanceStatus === 'present' ? '1' : (staff.attendanceStatus === 'absent' ? '0.7' : '0.5') }">
                  <!-- Attendance Status Badge -->
                  <div style="position: absolute; top: 12px; right: 12px; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 600" :style="{ background: staff.attendanceStatus === 'present' ? 'rgba(92, 186, 125, 0.2)' : (staff.attendanceStatus === 'absent' ? 'rgba(240, 128, 112, 0.2)' : 'rgba(200, 200, 200, 0.2)'), color: staff.attendanceStatus === 'present' ? '#5cba7d' : (staff.attendanceStatus === 'absent' ? '#f08070' : '#999') }">
                    {{ staff.attendanceStatus === 'present' ? '✓ Present' : (staff.attendanceStatus === 'absent' ? '✗ Absent' : '• Unmarked') }}
                  </div>
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
          <div ref="staffFormRef" class="card" style="margin-bottom: 20px">
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
                      :max="todayDate"
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

          <!-- Staff Members Table -->
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">👔 Staff Members</h3>
            </div>
            <div class="card-body">
              <div style="margin-bottom: 16px; display: flex; gap: 12px; align-items: flex-end; flex-wrap: wrap">
                <div style="flex: 1; min-width: 200px">
                  <label style="display: block; font-size: 12px; color: var(--text-muted); margin-bottom: 4px">Name or Email</label>
                  <input 
                    v-model="staffName"
                    type="text" 
                    placeholder="🔍 Filter by name or email..." 
                    class="form-input"
                    style="width: 100%"
                  />
                </div>
                <div style="flex: 1; min-width: 200px">
                  <label style="display: block; font-size: 12px; color: var(--text-muted); margin-bottom: 4px">Sort Order</label>
                  <select 
                    v-model="tableSort.staff.direction"
                    class="form-input"
                    style="width: 100%"
                  >
                    <option value="asc">⬆ Ascending</option>
                    <option value="desc">⬇ Descending</option>
                  </select>
                </div>
              </div>
              <div class="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th style="cursor: pointer" @click="toggleSort('staff', 'name')">Name {{ getSortIndicator('staff', 'name') }}</th>
                      <th style="cursor: pointer" @click="toggleSort('staff', 'role')">Role {{ getSortIndicator('staff', 'role') }}</th>
                      <th>Skills</th>
                      <th>Email</th>
                      <th style="cursor: pointer" @click="toggleSort('staff', 'phone')">Phone {{ getSortIndicator('staff', 'phone') }}</th>
                      <th>Date of Birth</th>
                      <th>Date of Joining</th>
                      <th style="cursor: pointer; text-align: center" @click="toggleSort('staff', 'rating')">Rating {{ getSortIndicator('staff', 'rating') }}</th>
                      <th>Attendance</th>
                      <th>Today's Appts</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="staff in paginatedStaff" :key="staff.id" @click="viewStaffBookings(staff)" style="cursor: pointer; transition: background-color 0.2s" @mouseenter="$event.target.parentElement.style.backgroundColor = 'var(--light-bg)'" @mouseleave="$event.target.parentElement.style.backgroundColor = 'transparent'">
                      <td>{{ staff.name }}</td>
                      <td>{{ staff.role }}</td>
                      <td><span style="font-size: 12px; color: var(--text-muted)">{{ staff.skills || '-' }}</span></td>
                      <td>{{ staff.email }}</td>
                      <td>{{ staff.phone }}</td>
                      <td>{{ staff.dob || '-' }}</td>
                      <td>{{ staff.doj }}</td>
                      <td style="text-align: center"><span style="font-weight: 600; color: #f5a623">⭐ {{ staff.rating || 'N/A' }}</span></td>
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
              <!-- Pagination Controls -->
              <div v-if="totalPagesStaff > 1" style="display: flex; align-items: center; justify-content: center; gap: 12px; margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--border)">
                <button :disabled="currentPageStaff === 1" @click="goToPageStaff(currentPageStaff - 1)" class="btn btn-sm btn-outline" title="Previous page">← Previous</button>
                <span style="font-size: 14px; font-weight: 600">Page {{ currentPageStaff }} of {{ totalPagesStaff }}</span>
                <button :disabled="currentPageStaff === totalPagesStaff" @click="goToPageStaff(currentPageStaff + 1)" class="btn btn-sm btn-outline" title="Next page">Next →</button>
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
                    <select 
                      id="product-category"
                      v-model="inventoryForm.categoryName"
                      class="form-input"
                      required
                    >
                      <option value="">Select a category</option>
                      <option value="Hair Care">Hair Care</option>
                      <option value="Skin Care">Skin Care</option>
                      <option value="Makeup">Makeup</option>
                      <option value="Nails">Nails</option>
                      <option value="Waxing">Waxing</option>
                      <option value="Tools & Brushes">Tools & Brushes</option>
                      <option value="Accessories">Accessories</option>
                      <option value="Other">Other</option>
                    </select>
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
              <div style="margin-bottom: 16px; display: flex; gap: 12px; align-items: flex-end; flex-wrap: wrap">
                <div style="flex: 1; min-width: 200px">
                  <label style="display: block; font-size: 12px; color: var(--text-muted); margin-bottom: 4px">Product Name</label>
                  <input 
                    v-model="productName"
                    type="text" 
                    placeholder="🔍 Filter by product name or category..." 
                    class="form-input"
                    style="width: 100%"
                  />
                </div>
                <div style="flex: 1; min-width: 200px">
                  <label style="display: block; font-size: 12px; color: var(--text-muted); margin-bottom: 4px">Stock Status</label>
                  <select 
                    v-model="stockStatusFilter"
                    class="form-input"
                    style="width: 100%"
                  >
                    <option value="">All Stock</option>
                    <option value="low">Low Stock</option>
                    <option value="high">Adequate Stock</option>
                  </select>
                </div>
              </div>
              <div class="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th style="cursor: pointer" @click="toggleSort('inventory', 'name')">Product {{ getSortIndicator('inventory', 'name') }}</th>
                      <th>Category</th>
                      <th style="cursor: pointer; text-align: center" @click="toggleSort('inventory', 'stock')">Stock {{ getSortIndicator('inventory', 'stock') }}</th>
                      <th style="cursor: pointer; text-align: center" @click="toggleSort('inventory', 'minStock')">Min Stock {{ getSortIndicator('inventory', 'minStock') }}</th>
                      <th style="cursor: pointer; text-align: right" @click="toggleSort('inventory', 'costPrice')">Cost Price {{ getSortIndicator('inventory', 'costPrice') }}</th>
                      <th>Supplier</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="product in paginatedProducts" :key="product.id" @click="viewProductDetails(product)" style="cursor: pointer">
                      <td>{{ product.name }}</td>
                      <td>{{ product.categoryName }}</td>
                      <td style="text-align: center"><span :class="['badge', product.stock <= product.minStock ? 'badge-red' : 'badge-green']">{{ product.stock }} {{ product.unit }}</span></td>
                      <td style="text-align: center">{{ product.minStock }}</td>
                      <td style="text-align: right">₹{{ product.costPrice }}</td>
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
              <!-- Pagination Controls -->
              <div v-if="totalPagesInventory > 1" style="display: flex; align-items: center; justify-content: center; gap: 12px; margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--border)">
                <button :disabled="currentPageInventory === 1" @click="goToPageInventory(currentPageInventory - 1)" class="btn btn-sm btn-outline" title="Previous page">← Previous</button>
                <span style="font-size: 14px; font-weight: 600">Page {{ currentPageInventory }} of {{ totalPagesInventory }}</span>
                <button :disabled="currentPageInventory === totalPagesInventory" @click="goToPageInventory(currentPageInventory + 1)" class="btn btn-sm btn-outline" title="Next page">Next →</button>
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
                <div v-for="order in pendingOrders" :key="order.order_id" class="order-item">
                  <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px">
                    <div>
                      <div style="font-weight: 600">{{ order.product_name }}</div>
                      <div class="text-muted">Ordered: {{ new Date(order.order_date).toLocaleDateString('en-IN') }}</div>
                    </div>
                    <span class="badge badge-gold">{{ order.order_quantity }} units</span>
                  </div>
                  <div style="display: flex; align-items: center; gap: 8px">
                    <span style="flex: 1" class="text-muted">📝 {{ order.reason_for_order }}</span>
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
              <div style="display: flex; justify-content: space-between; align-items: center; width: 100%">
                <h3 class="card-title">📊 Balance Sheet</h3>
                <div style="display: flex; gap: 12px; align-items: center">
                  <div>
                    <label style="font-size: 12px; color: var(--text-muted); display: block; margin-bottom: 4px">Select Month</label>
                    <input 
                      v-model="selectedBalanceSheetMonth"
                      type="month" 
                      class="form-input"
                      @change="loadBalanceSheetForMonth"
                      style="width: 150px; height: 36px"
                    />
                  </div>
                  <button 
                    @click="loadBalanceSheetForMonth" 
                    class="btn btn-outline" 
                    style="padding: 8px 16px; margin-top: 20px"
                    :disabled="financeLoading"
                  >
                    🔄 Load
                  </button>
                </div>
              </div>
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
                      <td style="text-align: right; font-weight: 600; padding-top: 12px; color: #5cba7d">₹{{ Math.max(0, calculatedNetProfit).toLocaleString() }}</td>
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
                <!-- Search and filter controls -->
                <div style="margin-bottom: 16px; display: flex; gap: 12px; align-items: flex-end; flex-wrap: wrap">
                  <div style="flex: 1; min-width: 200px">
                    <label style="font-size: 12px; color: var(--text-muted)">Search</label>
                    <input 
                      v-model="staffReplenishmentSearch"
                      type="text" 
                      class="form-input"
                      placeholder="Search by product, staff, or service..."
                      style="width: 100%"
                    />
                  </div>
                </div>
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
                <div v-if="filteredStaffReplenishments.length === 0" class="empty-state">
                  <div class="empty-state-icon">📊</div>
                  <div class="empty-state-text">{{ staffOrderRequests.length === 0 ? 'No staff orders found' : 'No results match your search' }}</div>
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
                      <tr v-for="txn in filteredStaffReplenishments" :key="txn.txn_id">
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
                  <input v-model="replenishmentForm.supplier" id="replen-supplier" type="text" class="form-input" placeholder="Auto-filled from product info" disabled style="background: var(--light-bg); color: var(--text-muted); cursor: not-allowed" />
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
                            <th>Order Date</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="item in group.items" :key="item.order_id">
                            <td><strong>{{ item.product_name }}</strong></td>
                            <td>{{ item.order_quantity }}</td>
                            <td><strong>₹{{ item.order_cost.toFixed(2) }}</strong></td>
                            <td><small>{{ new Date(item.order_date).toLocaleDateString('en-IN') }}</small></td>
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

                <!-- Filter -->
                <div style="margin-bottom: 16px; display: flex; gap: 12px; align-items: flex-end; flex-wrap: wrap">
                  <div style="flex: 1; min-width: 200px">
                    <label style="display: block; font-size: 12px; color: var(--text-muted); margin-bottom: 4px">Filter by Status</label>
                    <select 
                      v-model="orderStatusFilter"
                      class="form-input"
                      style="width: 100%"
                    >
                      <option value="">All Status</option>
                      <option value="0">Pending</option>
                      <option value="1">Delivered</option>
                    </select>
                  </div>
                </div>

                <!-- Orders Table -->
                <div v-if="filteredWholesaleOrders.length === 0" class="empty-state">
                  <div class="empty-state-icon">📮</div>
                  <div class="empty-state-text">No wholesale orders placed yet</div>
                </div>
                <div v-else class="table-wrap">
                  <table>
                    <thead>
                      <tr>
                        <th style="cursor: pointer" @click="toggleSort('orders', 'product_name')">Product {{ getSortIndicator('orders', 'product_name') }}</th>
                        <th style="cursor: pointer; text-align: center" @click="toggleSort('orders', 'order_quantity')">Quantity {{ getSortIndicator('orders', 'order_quantity') }}</th>
                        <th style="cursor: pointer; text-align: right" @click="toggleSort('orders', 'order_date')">Cost (₹) {{ getSortIndicator('orders', 'order_date') }}</th>
                        <th style="cursor: pointer" @click="toggleSort('orders', 'supplier_name')">Supplier {{ getSortIndicator('orders', 'supplier_name') }}</th>
                        <th>Reason</th>
                        <th style="cursor: pointer" @click="toggleSort('orders', 'status')">Status {{ getSortIndicator('orders', 'status') }}</th>
                        <th style="cursor: pointer" @click="toggleSort('orders', 'order_date')">Order Date {{ getSortIndicator('orders', 'order_date') }}</th>
                        <th>Replenishment Date</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="order in orderStatusFilter ? filteredWholesaleOrders.filter(o => parseInt(orderStatusFilter) === o.status) : filteredWholesaleOrders" :key="order.order_id">
                        <td><strong>{{ order.product_name }}</strong></td>
                        <td style="text-align: center">{{ order.order_quantity }}</td>
                        <td style="text-align: right">₹{{ (order.order_quantity * (data.products.find(p => p.id === order.product_id)?.price || 0)).toFixed(2) }}</td>
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
                        <td><small>{{ new Date(order.order_date).toLocaleDateString('en-IN') }}</small></td>
                        <td><small>{{ order.order_replenishment_date ? new Date(order.order_replenishment_date).toLocaleDateString('en-IN') : '-' }}</small></td>
                        <td style="display: flex; gap: 6px; flex-wrap: wrap">
                          <button v-if="order.status === 0" @click="handleMarkOrderDelivered(order)" class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 11px; color: #27ae60; border-color: #27ae60">✓ Delivered</button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
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
                <div class="grid-2" style="margin-top: 16px; opacity: 0.7">
                  <div class="form-group">
                    <label>Customer</label>
                    <input type="text" :value="getCustomerName(invoiceForm.customerId)" class="form-input" disabled />
                  </div>
                  <div class="form-group">
                    <label>Staff</label>
                    <input type="text" :value="invoiceForm.staffName || 'Unassigned'" class="form-input" disabled />
                  </div>
                </div>

                <!-- Selected Services Display -->
                <div v-if="invoiceForm.services.length > 0" style="margin-top: 16px; padding: 16px; background: var(--light-bg); border-radius: 8px; border-left: 4px solid var(--gold)">
                  <div style="font-weight: 600; font-size: 14px; margin-bottom: 12px">Services Included:</div>
                  <div style="display: grid; gap: 8px; margin-bottom: 12px">
                    <div v-for="service in invoiceForm.services" :key="service.id" style="display: flex; justify-content: space-between; align-items: center; padding: 8px; background: var(--surface); border-radius: 6px; font-size: 13px">
                      <span>{{ service.name || service.service_desc }}</span>
                      <span style="font-weight: 600; color: var(--gold)">₹{{ service.price || service.service_price }}</span>
                    </div>
                  </div>
                  <div style="padding-top: 12px; border-top: 1px solid var(--border); display: flex; justify-content: space-between; font-weight: 600; font-size: 14px">
                    <span>Total Bill:</span>
                    <span style="color: var(--gold); font-size: 16px">₹{{ invoiceForm.totalServiceAmount }}</span>
                  </div>
                </div>

                <div class="grid-2" style="margin-top: 16px; opacity: 0.7">
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

                <!-- Birthday Alert -->
                <div v-if="invoiceBirthdayAlert" style="margin-top: 16px; padding: 14px 16px; border-radius: 8px; background: rgba(255,200,50,0.12); border: 1px solid rgba(255,200,50,0.4); display: flex; align-items: flex-start; gap: 12px">
                  <span style="font-size: 22px; line-height: 1">{{ invoiceBirthdayAlert.days === 0 ? '🎂' : '🎁' }}</span>
                  <div>
                    <div style="font-weight: 600; font-size: 13px; color: #f0c040; margin-bottom: 4px">
                      {{ invoiceBirthdayAlert.days === 0 ? "Today is " + invoiceBirthdayAlert.name + "'s Birthday!" : invoiceBirthdayAlert.name + "'s birthday is in " + invoiceBirthdayAlert.days + " day" + (invoiceBirthdayAlert.days > 1 ? 's' : '') + "!" }}
                    </div>
                    <div style="font-size: 12px; color: rgba(255,255,255,0.6)">
                      Consider giving a special birthday discount.
                    </div>
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
          </div>

          <!-- Invoices Table -->
          <div class="card" style="margin-top: 24px">
            <div class="card-header">
              <h3 class="card-title">All Invoices</h3>
            </div>
            <div class="card-body">
              <div style="margin-bottom: 16px; display: flex; gap: 12px; align-items: flex-end; flex-wrap: wrap">
                <div style="flex: 1; min-width: 200px">
                  <label style="display: block; font-size: 12px; color: var(--text-muted); margin-bottom: 4px">Customer Name</label>
                  <input 
                    v-model="invoiceCustomerName"
                    type="text" 
                    placeholder="🔍 Filter by customer name..." 
                    class="form-input"
                    style="width: 100%"
                  />
                </div>
                <div style="flex: 1; min-width: 200px">
                  <label style="display: block; font-size: 12px; color: var(--text-muted); margin-bottom: 4px">Invoice Status</label>
                  <select 
                    v-model="invoiceStatusFilter"
                    class="form-input"
                    style="width: 100%"
                  >
                    <option value="">All Status</option>
                    <option value="1">Invoiced</option>
                    <option value="2">Sent</option>
                  </select>
                </div>
                <div style="flex: 1; min-width: 200px">
                  <label style="display: block; font-size: 12px; color: var(--text-muted); margin-bottom: 4px">Sort Order</label>
                  <select 
                    v-model="tableSort.invoices.direction"
                    class="form-input"
                    style="width: 100%"
                  >
                    <option value="desc"> Newest to Oldest</option>
                    <option value="asc"> Oldest to Newest</option>
                  </select>
                </div>
              </div>
              
              <div v-if="filteredInvoices.length === 0" class="empty-state">
                <div class="empty-state-icon">📄</div>
                <div class="empty-state-text">No invoices found</div>
              </div>
              
              <div v-else class="table-wrap" style="overflow-x: auto; width: 100%">
                <table style="min-width: 1000px; width: 100%">
                  <thead>
                    <tr>
                      <th style="min-width: 80px; cursor: pointer" @click="toggleSort('invoices', 'invoice_number')">Invoice # {{ getSortIndicator('invoices', 'invoice_number') }}</th>
                      <th style="min-width: 120px; cursor: pointer" @click="toggleSort('invoices', 'customer_name')">Customer {{ getSortIndicator('invoices', 'customer_name') }}</th>
                      <th style="min-width: 120px">Staff</th>
                      <th style="min-width: 150px">Services</th>
                      <th style="min-width: 100px; cursor: pointer; text-align: right" @click="toggleSort('invoices', 'total_charges')">Amount (₹) {{ getSortIndicator('invoices', 'total_charges') }}</th>
                      <th style="min-width: 100px; cursor: pointer" @click="toggleSort('invoices', 'invoice_date')">Date {{ getSortIndicator('invoices', 'invoice_date') }}</th>
                      <th style="min-width: 90px">Status</th>
                      <th style="min-width: 90px">Feedback</th>
                      <th style="min-width: 200px">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="invoice in paginatedInvoices" :key="invoice.id">
                      <td><strong>{{ invoice.invoice_number }}</strong></td>
                      <td>{{ invoice.customer_name || getCustomerName(invoice.customer_id) }}</td>
                      <td>{{ invoice.staffName || invoice.staff_name || getStaffName(invoice.staff_id) || "Unassigned" }}</td>
                      <td><small>{{ invoice.service_names || invoice.service_ids || 'N/A' }}</small></td>
                      <td style="text-align: right"><strong>₹{{ invoice.total_charges?.toFixed(2) || 0 }}</strong></td>
                      <td><small>{{ new Date(invoice.invoice_date).toLocaleDateString() }}</small></td>
                      <td>
                        <span :style="{ 
                          padding: '4px 8px', 
                          borderRadius: '4px', 
                          fontSize: '11px', 
                          fontWeight: '600',
                          backgroundColor: invoice.status === 1 ? '#fff3cd' : '#e0f2fe',
                          color: invoice.status === 1 ? '#856404' : '#0369a1'
                        }">
                          {{ invoice.status === 1 ? 'Invoiced' : invoice.status === 2 ? 'Sent' : 'Unknown' }}
                        </span>
                      </td>
                      <td>
                        <button v-if="invoice.appointment_id && invoice.rating" @click="viewFeedback(invoice)" class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 11px; color: #f59e0b; border-color: #f59e0b; background-color: rgba(245, 158, 11, 0.1); font-weight: 600">
                          ⭐ {{ invoice.rating }}/5
                        </button>
                        <button v-else-if="invoice.appointment_id" disabled class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 11px; color: #999; border-color: #ddd; opacity: 0.6; cursor: not-allowed">
                          ⭐ No Review
                        </button>
                        <span v-else style="font-size: 11px; color: var(--text-muted)">-</span>
                      </td>
                      <td>
                        <div style="display: flex; gap: 6px; flex-wrap: wrap">
                          <button @click="viewInvoice(invoice)" class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 11px">
                            📄 View
                          </button>
                          <button @click="handleSendInvoice(invoice)" class="btn btn-sm btn-outline" style="padding: 4px 8px; font-size: 11px; color: #27ae60; border-color: #27ae60">
                            📧 Send
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!-- Pagination Controls -->
              <div v-if="totalPagesInvoices > 1" style="display: flex; align-items: center; justify-content: center; gap: 12px; margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--border)">
                <button :disabled="currentPageInvoices === 1" @click="goToPageInvoices(currentPageInvoices - 1)" class="btn btn-sm btn-outline" title="Previous page">← Previous</button>
                <span style="font-size: 14px; font-weight: 600">Page {{ currentPageInvoices }} of {{ totalPagesInvoices }}</span>
                <button :disabled="currentPageInvoices === totalPagesInvoices" @click="goToPageInvoices(currentPageInvoices + 1)" class="btn btn-sm btn-outline" title="Next page">Next →</button>
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
                  <span v-if="shareMessage" style="font-size: 12px; color: #5cba7d;">{{ shareMessage }}</span>
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
                        <span v-if="report.shared" style="margin-left: 6px; font-size: 10px; background: rgba(45,138,78,0.15); color: #5cba7d; padding: 1px 7px; border-radius: 10px; font-weight: 600; border: 1px solid rgba(45,138,78,0.28);">Shared</span>
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

        <!-- Profile View -->
        <div v-if="currentView === 'profile'" class="fade-in">
          <div class="card" style="margin-bottom: 24px">
            <div class="card-header">
              <h3 class="card-title">My Profile</h3>
            </div>
            <div class="card-body">
              <!-- Header with Avatar -->
              <div style="display: grid; grid-template-columns: auto 1fr; gap: 16px; align-items: center; margin-bottom: 24px; padding-bottom: 24px; border-bottom: 1px solid var(--border)">
                <div style="width: 80px; height: 80px; border-radius: 50%; background: var(--gold); display: flex; align-items: center; justify-content: center; color: white; font-size: 32px; font-weight: bold">
                  {{ user.name?.charAt(0) || "M" }}
                </div>
                <div>
                  <div style="font-size: 24px; font-weight: 700; margin-bottom: 4px">{{ user.name }}</div>
                  <div style="color: var(--gold); font-size: 14px; font-weight: 600; margin-bottom: 4px">{{ managerProfileData?.manager_role || 'Manager' }}</div>
                  <div style="color: var(--text-muted); font-size: 12px">ID: {{ managerProfileData?.manager_id }}</div>
                </div>
              </div>

              <!-- Information Grid -->
              <div style="background: var(--light-bg); padding: 20px; border-radius: 8px; margin-bottom: 24px">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px">
                  <!-- Email -->
                  <div>
                    <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-weight: 700; margin-bottom: 6px">Email</div>
                    <div style="font-size: 14px; color: var(--charcoal); font-weight: 500">{{ managerProfileData?.manager_email || 'Not provided' }}</div>
                  </div>

                  <!-- Phone -->
                  <div>
                    <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-weight: 700; margin-bottom: 6px">Phone</div>
                    <div style="font-size: 14px; color: var(--charcoal); font-weight: 500">{{ managerProfileData?.manager_contact || 'Not provided' }}</div>
                  </div>

                  <!-- Role -->
                  <div>
                    <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-weight: 700; margin-bottom: 6px">Role</div>
                    <div style="font-size: 14px; color: var(--charcoal); font-weight: 500">{{ managerProfileData?.manager_role || 'Not provided' }}</div>
                  </div>

                  <!-- Date of Birth -->
                  <div>
                    <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-weight: 700; margin-bottom: 6px">Date of Birth</div>
                    <div style="font-size: 14px; color: var(--charcoal); font-weight: 500">{{ managerProfileData?.manager_dob?.substring(0, 10) || 'Not provided' }}</div>
                  </div>

                  <!-- Date of Joining -->
                  <div>
                    <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-weight: 700; margin-bottom: 6px">Date of Joining</div>
                    <div style="font-size: 14px; color: var(--charcoal); font-weight: 500">{{ managerProfileData?.manager_doj?.substring(0, 10) || 'Not provided' }}</div>
                  </div>

                  <!-- Branch -->
                  <div>
                    <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-weight: 700; margin-bottom: 6px">Branch</div>
                    <div style="font-size: 14px; color: var(--charcoal); font-weight: 500">{{ managerProfileData?.branch_name || 'Not provided' }}</div>
                  </div>

                  <!-- Skills -->
                  <div style="grid-column: 1 / -1">
                    <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-weight: 700; margin-bottom: 6px">Skills</div>
                    <div style="font-size: 14px; color: var(--charcoal); font-weight: 500">{{ managerProfileData?.manager_skills || 'Not provided' }}</div>
                  </div>
                </div>
              </div>

              <!-- Action Buttons -->
              <div style="display: flex; gap: 12px; flex-wrap: wrap">
                <button class="btn btn-primary" @click="openProfileEdit()">
                  ✏️ Edit Profile
                </button>
                <button class="btn btn-outline" @click="showChangePasswordModal = true">
                  🔑 Change Password
                </button>
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
  <div v-if="showChangePasswordModal" class="modal-overlay" @click="showChangePasswordModal = false; showCurrentPassword.value = false; showNewPassword.value = false; showConfirmPassword.value = false">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3 class="modal-title">🔑 Change Password</h3>
        <button class="modal-close" @click="showChangePasswordModal = false; showCurrentPassword.value = false; showNewPassword.value = false; showConfirmPassword.value = false">✕</button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="handleChangePassword">
          <div class="form-group">
            <label for="current-password">Current Password</label>
            <div style="position: relative; display: flex; align-items: center">
              <input 
                id="current-password"
                v-model="passwordForm.currentPassword" 
                :type="showCurrentPassword.value ? 'text' : 'password'" 
                placeholder="Enter current password"
                class="form-input"
                required
              />
              <button type="button" @click.prevent="showCurrentPassword.value = !showCurrentPassword.value" style="position: absolute; right: 12px; background: none; border: none; cursor: pointer; font-size: 18px; color: var(--text-muted); padding: 4px; line-height: 1">
                {{ showCurrentPassword.value ? '🙈' : '👁️' }}
              </button>
            </div>
          </div>
          <div class="form-group">
            <label for="new-password">New Password</label>
            <div style="position: relative; display: flex; align-items: center">
              <input 
                id="new-password"
                v-model="passwordForm.newPassword" 
                :type="showNewPassword.value ? 'text' : 'password'" 
                placeholder="Enter new password"
                class="form-input"
                required
              />
              <button type="button" @click.prevent="showNewPassword.value = !showNewPassword.value" style="position: absolute; right: 12px; background: none; border: none; cursor: pointer; font-size: 18px; color: var(--text-muted); padding: 4px; line-height: 1">
                {{ showNewPassword.value ? '🙈' : '👁️' }}
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
                :type="showConfirmPassword.value ? 'text' : 'password'" 
                placeholder="Confirm new password"
                class="form-input"
                required
              />
              <button type="button" @click.prevent="showConfirmPassword.value = !showConfirmPassword.value" style="position: absolute; right: 12px; background: none; border: none; cursor: pointer; font-size: 18px; color: var(--text-muted); padding: 4px; line-height: 1">
                {{ showConfirmPassword.value ? '🙈' : '👁️' }}
              </button>
            </div>
          </div>
          <div v-if="passwordError" class="error-message">{{ passwordError }}</div>
          <div v-if="passwordSuccess" class="success-message">{{ passwordSuccess }}</div>
          <div style="display: flex; gap: 12px; margin-top: 20px">
            <button type="button" class="btn btn-outline" @click="showChangePasswordModal = false; showCurrentPassword.value = false; showNewPassword.value = false; showConfirmPassword.value = false" style="flex: 1">
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
            <label for="profile-dob">Date of Birth</label>
            <input 
              id="profile-dob"
              v-model="profileEditForm.dob" 
              type="date" 
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
          <div class="form-group">
            <label for="profile-skills">Skills</label>
            <textarea
              id="profile-skills"
              v-model="profileEditForm.skills" 
              placeholder="Enter skills (comma-separated)"
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
            <input type="text" :value="getCustomerName(editingAppointment.customerId)" class="form-input" readonly style="background: #f5f5f5; color: black"/>
          </div>

          <div class="form-group" style="margin-bottom: 16px">
            <label style="font-weight: 600; display: block; margin-bottom: 8px">Select Services *</label>
            <div style="border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 12px; max-height: 200px; overflow-y: auto">
              <div v-for="service in data.services.filter(s => getServiceStatus(s) === 'Active')" :key="service.id" style="display: flex; align-items: center; margin-bottom: 12px">
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
                <option v-for="time in editAppointmentTimeSlots" :key="time" :value="time">
                  {{ time }}
                </option>
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
                <td><span :class="['badge', apptStatusBadge(booking.status)]" :title="apptStatusLabel(booking.status)" :style="{ color: apptStatusColor(booking.status), fontWeight: '600' }">{{ apptStatusLabel(booking.status) }}</span></td>
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
                <th>Amount</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="visit in customerVisits" :key="visit.id">
                <td>{{ getServiceName(visit.serviceId) }}</td>
                <td>{{ visit.date }}</td>
                <td>{{ getStaffName(visit.staffId) }}</td>
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
              <span style="font-weight: 500">{{ selectedInvoice.service_names || selectedInvoice.service_ids || 'N/A' }}</span>
            </div>
            <div style="display: grid; grid-template-columns: 140px 1fr">
              <span style="color: var(--text-muted)">Staff:</span>
              <span style="font-weight: 500">{{ selectedInvoice.staff_name || 'Not Assigned' }}</span>
            </div>
          </div>
        </div>

        <div style="border-top: 2px solid var(--border-color); padding-top: 16px; margin-bottom: 20px">
          <div style="display: grid; grid-template-columns: 160px 1fr; gap: 8px; margin-bottom: 6px">
            <span style="color: var(--text-muted)">Subtotal:</span>
            <span style="text-align: right; font-weight: 500">₹{{ (selectedInvoice.invoice_amount || 0).toFixed(2) }}</span>
          </div>
          <div v-if="selectedInvoice.other_charges" style="display: grid; grid-template-columns: 160px 1fr; gap: 8px; margin-bottom: 6px">
            <span style="color: var(--text-muted)">Other Charges:</span>
            <span style="text-align: right; font-weight: 500">₹{{ (selectedInvoice.other_charges || 0).toFixed(2) }}</span>
          </div>
          <div v-if="selectedInvoice.discount_percentage" style="display: grid; grid-template-columns: 160px 1fr; gap: 8px; margin-bottom: 6px">
            <span style="color: var(--text-muted)">Discount ({{ (selectedInvoice.discount_percentage || 0).toFixed(2) }}%):</span>
            <span style="text-align: right; font-weight: 500; color: #4caf50">
              -₹{{ ((selectedInvoice.invoice_amount || 0) * (selectedInvoice.discount_percentage || 0) / 100).toFixed(2) }}
            </span>
          </div>
          <div v-if="selectedInvoice.rewards_utilized" style="display: grid; grid-template-columns: 160px 1fr; gap: 8px; margin-bottom: 6px">
            <span style="color: var(--text-muted)">Rewards ({{ selectedInvoice.rewards_utilized }} pts):</span>
            <span style="text-align: right; font-weight: 500; color: #4caf50">
              -₹{{ (selectedInvoice.rewards_monetary_discount || 0).toFixed(2) }}
            </span>
          </div>
          <div style="display: grid; grid-template-columns: 160px 1fr; gap: 8px; padding-top: 8px; border-top: 1px solid var(--border-color)">
            <span style="color: var(--text-muted); font-weight: 600">Total Payable:</span>
            <span style="text-align: right; font-weight: 700; color: var(--gold); font-size: 16px">₹{{ Number(selectedInvoice.payable_amount || selectedInvoice.total_charges || 0).toFixed(2) }}</span>
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
              <span style="font-weight: 500; color: #5cba7d">+{{ selectedInvoice.rewards_earned }} pts</span>
            </div>
            <div style="display: grid; grid-template-columns: 140px 1fr" v-if="selectedInvoice.rewards_utilized > 0">
              <span style="color: var(--text-muted)">Rewards Used:</span>
              <span style="font-weight: 500; color: #f08070">-{{ selectedInvoice.rewards_utilized }} pts</span>
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

  <!-- Feedback Modal -->
  <div v-if="showFeedbackModal" class="modal-overlay" @click="showFeedbackModal = false">
    <div class="modal-content" @click.stop style="max-width: 600px">
      <div class="modal-header">
        <h3 class="modal-title">⭐ Customer Feedback</h3>
        <button class="modal-close" @click="showFeedbackModal = false">✕</button>
      </div>
      <div class="modal-body">
        <div v-if="feedbackError" class="error-message" style="margin-bottom: 16px">
          {{ feedbackError }}
        </div>
        <div v-else-if="currentFeedback">
          <div style="margin-bottom: 20px">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px">
              <span style="font-size: 24px">⭐</span>
              <span style="font-size: 18px; font-weight: 600; color: #f59e0b">
                {{ currentFeedback.rating }}/5 Stars
              </span>
            </div>
            <div style="padding: 16px; background: #ffffff; border-radius: 8px; border-left: 4px solid #f59e0b;">
              <p style="margin: 0; color: #1a1a1a; line-height: 1.7; font-size: 15px; word-wrap: break-word; white-space: normal; font-weight: 500;">
                {{ currentFeedback.review || currentFeedback.review_text || "No review text provided" }}
              </p>
            </div>
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--border)">
            <div>
              <small style="color: var(--text-muted); font-weight: 600">Staff</small>
              <div style="font-weight: 600">{{ currentFeedback.staff_name || "Unknown" }}</div>
            </div>
            <div>
              <small style="color: var(--text-muted); font-weight: 600">Services</small>
              <div style="font-weight: 600; font-size: 12px">{{ Array.isArray(currentFeedback.services) ? currentFeedback.services.join(", ") : currentFeedback.services }}</div>
            </div>
            <div>
              <small style="color: var(--text-muted); font-weight: 600">Date</small>
              <div style="font-weight: 600">{{ currentFeedback.datetime ? new Date(currentFeedback.datetime).toLocaleDateString() : "N/A" }}</div>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">
          <div class="empty-state-icon">📝</div>
          <div class="empty-state-text">No feedback available</div>
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
const showCurrentPassword = ref(false);
const showNewPassword = ref(false);
const showConfirmPassword = ref(false);
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
const selectedBalanceSheetMonth = ref(new Date().toISOString().split('T')[0].slice(0, 7)); // YYYY-MM format
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
const lastReportIntent = ref(null); // remembers last report type/period for format follow-ups

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
const bookingServiceSearch = ref("");
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
const serviceFormRef = ref(null);
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
  preferences: "",
  customerType: ""
});
// Customer form ref for scrolling
const customerFormRef = ref(null);
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
// Staff form ref for scrolling
const staffFormRef = ref(null);
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
  serviceIds: [],
  totalServiceAmount: 0,
  date: "",
  paymentType: "cash",
  discount: 0,
  services: [],
  amount: 0,
  customerName: "",
  staffName: "",
  serviceNames: ""
});

const invoiceBirthdayAlert = computed(() => {
  if (!invoiceForm.value.customerId) return null;
  const customer = data.value.customers?.find(c => c.id === invoiceForm.value.customerId);
  if (!customer?.dob) return null;
  const today = new Date();
  const dob = new Date(customer.dob);
  const thisYearBday = new Date(today.getFullYear(), dob.getMonth(), dob.getDate());
  const diffMs = thisYearBday - new Date(today.getFullYear(), today.getMonth(), today.getDate());
  const diffDays = Math.round(diffMs / (1000 * 60 * 60 * 24));
  if (diffDays >= 0 && diffDays <= 7) return { days: diffDays, name: customer.name };
  return null;
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

// Sorting and filtering states
const tableSort = ref({
  services: { column: "name", direction: "asc" },
  customers: { column: "name", direction: "asc" },
  staff: { column: "name", direction: "asc" },
  inventory: { column: "name", direction: "asc" },
  orders: { column: "order_date", direction: "desc" },
  invoices: { column: "invoice_date", direction: "desc" },
  transactions: { column: "date", direction: "desc" }
});

// Additional filters
const serviceStatusFilter = ref("");
const customerTypeFilter = ref("");

const stockStatusFilter = ref("");
const invoiceStatusFilter = ref("");
const orderStatusFilter = ref("");

// Pagination state
const pageSize = ref(12);
const currentPageServices = ref(1);
const currentPageCustomers = ref(1);
const currentPageStaff = ref(1);
const currentPageInventory = ref(1);
const currentPageInvoices = ref(1);
const currentPageAppointments = ref(1);
const currentPageOrders = ref(1);

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

// Notification panel state
const showNotificationPanel = ref(false);
const notificationsList = ref([]);
const notificationsLoading = ref(false);

// Computed property for unread notifications count
const unreadCount = computed(() => {
  return notificationsList.value.filter(n => !n.is_read).length;
});

// Computed property for only unread notifications
const unreadNotifications = computed(() => {
  return notificationsList.value.filter(n => !n.is_read);
});

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

// Feedback Modal State
const showFeedbackModal = ref(false);
const currentFeedback = ref(null);
const feedbackError = ref("");

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
const allManagerReplenishmentTransactions = ref([]);
const managerTransactionDateFrom = ref("");
const managerTransactionDateTo = ref("");
const staffReplenishmentSearch = ref("");

// Track which products already have low stock notifications to prevent duplicates
const notifiedLowStockProducts = new Set();

// Manager wholesale orders tracking
const managerOrders = ref([]);

const fetchManagerAttendance = async (selectedDate = null) => {
  attendanceLoading.value = true;
  attendanceError.value = "";
  
  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      attendanceError.value = "Not authenticated";
      attendanceLoading.value = false;
      return;
    }

    // Fetch attendance for selected date or today (backend defaults to today when no date param provided)
    const dateParam = selectedDate ? `?date=${selectedDate}` : "";
    const response = await fetch(
      `${API_BASE_URL}/api/manager-staff-attendance${dateParam}`,
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
      const mappedAttendance = attendanceData.map(record => {
        // Ensure date is in YYYY-MM-DD format, handling timezone issues
        let recordDate;
        if (typeof record.register_datetime === 'string') {
          // If it's already a string, extract date part
          recordDate = record.register_datetime.includes('T') 
            ? record.register_datetime.split('T')[0]
            : record.register_datetime.split(' ')[0];
        } else {
          // If it's a date object, convert to ISO string and extract date
          recordDate = new Date(record.register_datetime).toISOString().split('T')[0];
        }
        return {
          staffId: record.staff_id,
          date: recordDate,
          status: record.present_flag ? "present" : "absent"
        };
      });
      fetchedAttendance.value = mappedAttendance;
      // Update the main data store with fetched attendance
      appStore.data.attendance = mappedAttendance;
      console.log("✅ Manager attendance loaded for", selectedDate || 'today', ":", {
        rawCount: attendanceData.length,
        mappedCount: mappedAttendance.length,
        mappedData: mappedAttendance
      });
    } else if (response.status === 404) {
      // No records found for that date is OK - means no staff marked attendance
      fetchedAttendance.value = [];
      appStore.data.attendance = [];
      console.log("ℹ️ No attendance records found for", selectedDate || 'today');
    } else {
      attendanceError.value = `Failed to load attendance data (Status: ${response.status})`;
      console.warn("⚠️ Attendance fetch failed:", response.status);
    }
  } catch (error) {
    console.error("❌ Error fetching attendance:", error);
    attendanceError.value = "Error loading attendance: " + error.message;
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
          status: 0,
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
  return data.value.appointments.filter(a => a.date === today() && !a.invoiceGenerated && a.status !== 5);
});

// Group today's appointments by customer
const groupedTodayAppointments = computed(() => {
  const grouped = {};
  todayAppointments.value.forEach(appt => {
    const customerId = appt.customerId;
    if (!grouped[customerId]) {
      grouped[customerId] = {
        customerId: customerId,
        customerName: getCustomerName(customerId),
        appointments: []
      };
    }
    grouped[customerId].appointments.push(appt);
  });
  return Object.values(grouped);
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
  const attendanceData = fetchedAttendance.value.length > 0 ? fetchedAttendance.value : (appStore.data?.attendance || []);
  const staffList = appStore.data?.staff || [];
  
  console.log("staffForSelectedDay computed:", {
    staffCount: staffList.length,
    attendanceRecords: attendanceData.length,
    selectedDate: selectedStaffDate.value,
    attendanceData: attendanceData
  });
  
  // Map staff with attendance status
  const mappedStaff = staffList.map(staff => {
    const attendance = attendanceData.find(
      a => a.staffId === staff.id && a.date === selectedStaffDate.value
    );
    return {
      ...staff,
      isPresent: attendance && attendance.status === 'present',
      isAbsent: attendance && attendance.status === 'absent',
      attendanceStatus: attendance && attendance.status === 'present' ? 'present' : 'absent'
    };
  });
  
  // Separate and sort: present first, then absent (includes unmarked)
  const present = mappedStaff.filter(s => s.attendanceStatus === 'present').sort((a, b) => a.name.localeCompare(b.name));
  const absent = mappedStaff.filter(s => s.attendanceStatus === 'absent').sort((a, b) => a.name.localeCompare(b.name));
  
  return [...present, ...absent];
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
  return allManagerReplenishmentTransactions.value.filter(o => o.status === 0);
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

const filteredStaffReplenishments = computed(() => {
  if (!staffReplenishmentSearch.value.trim()) return staffOrderRequests.value;
  const query = staffReplenishmentSearch.value.toLowerCase();
  return staffOrderRequests.value.filter(txn => {
    const productMatch = txn.product_name?.toLowerCase().includes(query);
    const staffMatch = getStaffName(txn.staff_id)?.toLowerCase().includes(query);
    const serviceMatch = txn.service_name?.toLowerCase().includes(query);
    return productMatch || staffMatch || serviceMatch;
  });
});

const managerReplenishmentOrders = computed(() => {
  // Show all cart orders (status === 2) - not yet sent to wholesale
  const filtered = allManagerReplenishmentTransactions.value.filter(order => order.status === 2);
  return sortData(filtered, tableSort.value.orders);
});

const groupedSupplierOrders = computed(() => {
  const grouped = {};
  managerReplenishmentOrders.value.forEach(order => {
    const supplier = order.supplier_name || "Unknown Supplier";
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

const filteredWholesaleOrders = computed(() => {
  // Only show orders that have been sent to wholesale (status 0) or delivered (status 1)
  // Exclude cart items (status 2)
  const filtered = managerOrders.value.filter(order => order.status === 0 || order.status === 1);
  return sortData(filtered, tableSort.value.orders);
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

// Sorting helper function
const sortData = (data, sortConfig) => {
  if (!sortConfig.column) return data;
  const sorted = [...data];
  sorted.sort((a, b) => {
    const aVal = a[sortConfig.column];
    const bVal = b[sortConfig.column];
    let comparison = 0;
    if (typeof aVal === 'string') {
      comparison = aVal.localeCompare(bVal);
    } else if (typeof aVal === 'number') {
      comparison = aVal - bVal;
    } else if (aVal instanceof Date) {
      comparison = aVal - bVal;
    } else {
      comparison = String(aVal).localeCompare(String(bVal));
    }
    return sortConfig.direction === 'asc' ? comparison : -comparison;
  });
  return sorted;
};

// Toggle sort function
const toggleSort = (table, column) => {
  const current = tableSort.value[table];
  if (current.column === column) {
    current.direction = current.direction === 'asc' ? 'desc' : 'asc';
  } else {
    current.column = column;
    current.direction = 'asc';
  }
};

// Get sort indicator
const getSortIndicator = (table, column) => {
  const current = tableSort.value[table];
  if (current.column !== column) return '↕';
  return current.direction === 'asc' ? '↑' : '↓';
};

// ──── PAGINATION HELPER FUNCTIONS ────
const goToPageServices = (page) => {
  if (page >= 1 && page <= totalPagesServices.value) {
    currentPageServices.value = page;
  }
};

const goToPageCustomers = (page) => {
  if (page >= 1 && page <= totalPagesCustomers.value) {
    currentPageCustomers.value = page;
  }
};

const goToPageStaff = (page) => {
  if (page >= 1 && page <= totalPagesStaff.value) {
    currentPageStaff.value = page;
  }
};

const goToPageInventory = (page) => {
  if (page >= 1 && page <= totalPagesInventory.value) {
    currentPageInventory.value = page;
  }
};

const goToPageInvoices = (page) => {
  if (page >= 1 && page <= totalPagesInvoices.value) {
    currentPageInvoices.value = page;
  }
};

const goToPageBookings = (page) => {
  if (page >= 1 && page <= totalPagesBookings.value) {
    currentPageAppointments.value = page;
  }
};

const goToPageOrders = (page) => {
  if (page >= 1 && page <= totalPagesOrders.value) {
    currentPageOrders.value = page;
  }
};

// Reset pagination when filters change
watch([serviceName, serviceCategoryFilter, serviceStatusFilter], () => {
  currentPageServices.value = 1;
});

watch([customerName, customerTypeFilter], () => {
  currentPageCustomers.value = 1;
});

watch([staffName], () => {
  currentPageStaff.value = 1;
});

watch([productName, stockStatusFilter], () => {
  currentPageInventory.value = 1;
});

watch([invoiceCustomerName, invoiceStatusFilter], () => {
  currentPageInvoices.value = 1;
});

watch([bookingCustomerName], () => {
  currentPageAppointments.value = 1;
});

watch([orderTab], () => {
  currentPageOrders.value = 1;
});

const displayedBookings = computed(() => {
  if (selectedDate.value) {
    return getDateBookings(selectedDate.value);
  }
  // Show all appointments (past and future)
  return data.value.appointments;
});

// Filtered data computed properties
const filteredServices = computed(() => {
  let filtered = data.value.services.filter(s => {
    const nameMatch = !serviceName.value.trim() || s.name.toLowerCase().includes(serviceName.value.toLowerCase());
    const categoryMatch = !serviceCategoryFilter.value || s.categoryId == serviceCategoryFilter.value;
    const statusMatch = !serviceStatusFilter.value || getServiceStatus(s) === serviceStatusFilter.value;
    return nameMatch && categoryMatch && statusMatch;
  });
  return sortData(filtered, tableSort.value.services);
});

const filteredCustomers = computed(() => {
  let filtered = data.value.customers;
  if (customerName.value.trim()) {
    filtered = filtered.filter(c => 
      c.name.toLowerCase().includes(customerName.value.toLowerCase()) ||
      c.email.toLowerCase().includes(customerName.value.toLowerCase())
    );
  }
  if (customerTypeFilter.value) {
    filtered = filtered.filter(c => c.customerType === customerTypeFilter.value);
  }
  return sortData(filtered, tableSort.value.customers);
});

const filteredStaff = computed(() => {
  let filtered = data.value.staff;
  if (staffName.value.trim()) {
    filtered = filtered.filter(s => 
      s.name.toLowerCase().includes(staffName.value.toLowerCase()) ||
      s.email.toLowerCase().includes(staffName.value.toLowerCase())
    );
  }
  return sortData(filtered, tableSort.value.staff);
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
  let filtered = data.value.products;
  if (productName.value.trim()) {
    filtered = filtered.filter(p => 
      p.name.toLowerCase().includes(productName.value.toLowerCase()) ||
      p.categoryName.toLowerCase().includes(productName.value.toLowerCase())
    );
  }
  if (stockStatusFilter.value === 'low') {
    filtered = filtered.filter(p => p.stock <= p.minStock);
  } else if (stockStatusFilter.value === 'high') {
    filtered = filtered.filter(p => p.stock > p.minStock);
  }
  return sortData(filtered, tableSort.value.inventory);
});

const filteredInvoices = computed(() => {
  let filtered = invoices.value;
  if (invoiceCustomerName.value.trim()) {
    filtered = filtered.filter(inv => {
      const customerNameStr = inv.customer_name ? inv.customer_name.toLowerCase() : getCustomerName(inv.customer_id).toLowerCase();
      return customerNameStr.includes(invoiceCustomerName.value.toLowerCase());
    });
  }
  if (invoiceStatusFilter.value) {
    filtered = filtered.filter(inv => inv.status === parseInt(invoiceStatusFilter.value));
  }
  return sortData(filtered, tableSort.value.invoices);
});

// ─────────────────────── PAGINATION COMPUTED PROPERTIES ───────────────────────
// Paginated Services
const paginatedServices = computed(() => {
  const start = (currentPageServices.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filteredServices.value.slice(start, end);
});

const totalPagesServices = computed(() => Math.ceil(filteredServices.value.length / pageSize.value) || 1);

// Paginated Customers
const paginatedCustomers = computed(() => {
  const start = (currentPageCustomers.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filteredCustomers.value.slice(start, end);
});

const totalPagesCustomers = computed(() => Math.ceil(filteredCustomers.value.length / pageSize.value) || 1);

// Paginated Staff
const paginatedStaff = computed(() => {
  const start = (currentPageStaff.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filteredStaff.value.slice(start, end);
});

const totalPagesStaff = computed(() => Math.ceil(filteredStaff.value.length / pageSize.value) || 1);

// Paginated Inventory
const paginatedProducts = computed(() => {
  const start = (currentPageInventory.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filteredProducts.value.slice(start, end);
});

const totalPagesInventory = computed(() => Math.ceil(filteredProducts.value.length / pageSize.value) || 1);

// Paginated Invoices
const paginatedInvoices = computed(() => {
  const start = (currentPageInvoices.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filteredInvoices.value.slice(start, end);
});

const totalPagesInvoices = computed(() => Math.ceil(filteredInvoices.value.length / pageSize.value) || 1);

// Paginated Bookings
const paginatedBookings = computed(() => {
  const start = (currentPageAppointments.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filteredBookings.value.slice(start, end);
});

const totalPagesBookings = computed(() => Math.ceil(filteredBookings.value.length / pageSize.value) || 1);

// Paginated Orders
const paginatedOrders = computed(() => {
  const start = (currentPageOrders.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  const orders = orderTab.value === 'pending-orders' ? staffOrderRequests.value : managerReplenishmentOrders.value;
  return orders.slice(start, end);
});

const totalPagesOrders = computed(() => {
  const orders = orderTab.value === 'pending-orders' ? staffOrderRequests.value : managerReplenishmentOrders.value;
  return Math.ceil(orders.length / pageSize.value) || 1;
});

// ─────────────────────────────────────────────────────────────────────────────

// Get today's date in YYYY-MM-DD format for DOB max date constraint
const todayDate = computed(() => {
  const now = new Date();
  return now.toISOString().split('T')[0];
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

// Filter appointments to exclude those already invoiced
const getAvailableAppointmentsForInvoice = computed(() => {
  const invoicedAppointmentIds = new Set(invoices.value.map(inv => inv.appointment_id).filter(id => id));
  return data.value.appointments.filter(appt => !invoicedAppointmentIds.has(appt.id));
});

// Get available time slots (filter out past times if booking for today)
const availableTimeSlots = computed(() => {
  // Generate times dynamically based on salon config
  const allTimes = [];
  
  // Get salon hours from config
  let openHour = 9, openMinute = 0, closeHour = 17, closeMinute = 0;
  if (salonConfigList.value && salonConfigList.value.length > 0) {
    const openConfig = salonConfigList.value.find(c => c.param_name === 'SALON_OPEN_TIME');
    const closeConfig = salonConfigList.value.find(c => c.param_name === 'SALON_CLOSE_TIME');
    
    if (openConfig) {
      const [h, m] = openConfig.param_value.split(':').map(Number);
      openHour = h;
      openMinute = m;
    }
    if (closeConfig) {
      const [h, m] = closeConfig.param_value.split(':').map(Number);
      closeHour = h;
      closeMinute = m;
    }
  }
  
  // Generate 30-minute slots
  let currentHour = openHour;
  let currentMinute = openMinute;
  
  while (currentHour < closeHour || (currentHour === closeHour && currentMinute < closeMinute)) {
    allTimes.push(`${String(currentHour).padStart(2, '0')}:${String(currentMinute).padStart(2, '0')}`);
    currentMinute += 30;
    if (currentMinute >= 60) {
      currentMinute = 0;
      currentHour += 1;
    }
  }
  
  if (!bookingForm.value.date) return allTimes;
  
  const todayDate = new Date().toISOString().split('T')[0];
  const selectedDate = bookingForm.value.date;
  
  // If not today, show all times
  if (selectedDate !== todayDate) return allTimes;
  
  // If today, filter out past times
  const now = new Date();
  const currentTimeHour = now.getHours();
  const currentTimeMinute = now.getMinutes();
  
  return allTimes.filter(time => {
    const [hour, minute] = time.split(':').map(Number);
    // Convert to minutes since midnight for easier comparison
    const timeInMinutes = hour * 60 + minute;
    const nowInMinutes = currentTimeHour * 60 + currentTimeMinute;
    // Only show times 30 minutes or more in the future
    return timeInMinutes > nowInMinutes + 30;
  });
});

// Available time slots for edit appointment (generates times based on salon config)
const editAppointmentTimeSlots = computed(() => {
  // Generate times dynamically based on salon config
  const allTimes = [];
  
  // Get salon hours from config
  let openHour = 9, openMinute = 0, closeHour = 17, closeMinute = 0;
  if (salonConfigList.value && salonConfigList.value.length > 0) {
    const openConfig = salonConfigList.value.find(c => c.param_name === 'SALON_OPEN_TIME');
    const closeConfig = salonConfigList.value.find(c => c.param_name === 'SALON_CLOSE_TIME');
    
    if (openConfig) {
      const [h, m] = openConfig.param_value.split(':').map(Number);
      openHour = h;
      openMinute = m;
    }
    if (closeConfig) {
      const [h, m] = closeConfig.param_value.split(':').map(Number);
      closeHour = h;
      closeMinute = m;
    }
  }
  
  // Generate 30-minute slots
  let currentHour = openHour;
  let currentMinute = openMinute;
  
  while (currentHour < closeHour || (currentHour === closeHour && currentMinute < closeMinute)) {
    allTimes.push(`${String(currentHour).padStart(2, '0')}:${String(currentMinute).padStart(2, '0')}`);
    currentMinute += 30;
    if (currentMinute >= 60) {
      currentMinute = 0;
      currentHour += 1;
    }
  }
  
  if (!editAppointmentForm.value.date) return allTimes;
  
  const todayDate = new Date().toISOString().split('T')[0];
  const selectedDate = editAppointmentForm.value.date;
  
  // If not today, show all times
  if (selectedDate !== todayDate) return allTimes;
  
  // If today, filter out past times
  const now = new Date();
  const currentTimeHour = now.getHours();
  const currentTimeMinute = now.getMinutes();
  
  return allTimes.filter(time => {
    const [hour, minute] = time.split(':').map(Number);
    // Convert to minutes since midnight for easier comparison
    const timeInMinutes = hour * 60 + minute;
    const nowInMinutes = currentTimeHour * 60 + currentTimeMinute;
    // Only show times 30 minutes or more in the future
    return timeInMinutes > nowInMinutes + 30;
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
    0: "badge-gray",    // 0: Booked
    1: "badge-green",   // 1: Completed
    2: "badge-red",     // 2: No-show
    3: "badge-gray",    // 3: Cancelled
    4: "badge-blue",    // 4: Rescheduled
    5: "badge-gold",    // 5: Invoiced
  };
  return badges[status] || "badge-gray";
};

const apptStatusLabel = (status) => {
  const labels = {
    0: "Booked",
    1: "Completed",
    2: "No-show",
    3: "Cancelled",
    4: "Rescheduled",
    5: "Invoiced",
  };
  return labels[status] || "Unknown";
};

const apptStatusColor = (status) => {
  const colors = {
    0: "#95a3a3",       // 0: Booked - gray
    1: "#27ae60",       // 1: Completed - green
    2: "#e74c3c",       // 2: No-show - red
    3: "#95a3a3",       // 3: Cancelled - gray
    4: "#3498db",       // 4: Rescheduled - blue
    5: "#d4af37",       // 5: Invoiced - gold
  };
  return colors[status] || "#95a3a3";
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

const logout = async () => {
  const token = localStorage.getItem("authToken");
  if (token) {
    try {
      await fetch(`${API_BASE_URL}/logout`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
          "Authentication-Token": token
        }
      });
    } catch (error) {
      console.error("Logout error:", error);
    }
  }
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
        dob: parseDateString(manager.manager_dob),
        doj: parseDateString(manager.manager_doj),
        skills: manager.manager_skills || ''
      };

      // Wait for Vue to update form refs before showing modal
      await nextTick();
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
        manager_dob: profileEditForm.value.dob,
        manager_doj: profileEditForm.value.doj,
        manager_skills: profileEditForm.value.skills
      })
    });

    if (response.ok) {
      // Update local store
      if (appStore.user) {
        appStore.user.name = profileEditForm.value.name;
        appStore.user.email = profileEditForm.value.email;
        appStore.user.phone = profileEditForm.value.phone;
        appStore.user.role = profileEditForm.value.role;
        appStore.user.dob = profileEditForm.value.dob;
        appStore.user.doj = profileEditForm.value.doj;
        appStore.user.skills = profileEditForm.value.skills;
      }

      // Refresh manager profile data
      await fetchManagerProfileData();
      
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
        status: appt.status !== null && appt.status !== undefined ? Number(appt.status) : 0,
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
    // Fetch invoices
    const invoiceResponse = await fetch(`${API_BASE_URL}/api/get-all-invoices`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    // Fetch all reviews in parallel
    const reviewResponse = await fetch(`${API_BASE_URL}/api/customer-reviewed-appointments`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (invoiceResponse.ok) {
      const fetchedInvoices = await invoiceResponse.json();
      
      // Create a map of reviews by appointment_id for quick lookup
      let reviewsMap = {};
      if (reviewResponse.ok) {
        try {
          const reviewsData = await reviewResponse.json();
          console.log("Reviews fetched:", reviewsData);
          reviewsData.forEach(review => {
            reviewsMap[review.appointment_id] = review;
          });
        } catch (e) {
          console.log("No reviews available or error parsing reviews");
        }
      }

      // Map backend response to frontend format
      const mappedInvoices = fetchedInvoices.map(inv => ({
        id: inv.invoice_number || inv.id,
        invoice_number: inv.invoice_number,
        appointment_id: inv.appointment_id,
        customer_id: inv.customer_id,
        customer_name: inv.customer_name || "",
        staff_id: inv.staff_id,
        staff_name: inv.staff_name || "",
        service_ids: inv.service_ids || "",
        service_names: inv.service_names || "",
        invoice_amount: inv.invoice_amount || 0,
        other_charges: inv.other_charges || 0,
        discount_percentage: inv.discount_percentage || 0,
        total_charges: inv.total_charges || inv.invoice_amount || 0,
        payable_amount: inv.payable_amount ?? inv.total_charges ?? inv.invoice_amount ?? 0,
        rewards_monetary_discount: inv.rewards_monetary_discount || 0,
        invoice_date: inv.invoice_date || new Date().toISOString().split('T')[0],
        status: inv.status || 0,
        rewards_earned: inv.rewards_earned || 0,
        rewards_utilized: inv.rewards_utilized || 0,
        current_reward_points: inv.current_reward_points || 0,
        // Map review data
        has_review: inv.has_review || false,
        review: reviewsMap[inv.appointment_id] || null,
        rating: reviewsMap[inv.appointment_id]?.rating || null,
        review_text: reviewsMap[inv.appointment_id]?.review || null
      }));
      invoices.value = mappedInvoices;
      console.log("Invoices with reviews mapped:", mappedInvoices);
    } else {
      console.error("Failed to fetch invoices - Status:", invoiceResponse.status);
      invoices.value = [];
    }
  } catch (error) {
    console.error("Error fetching invoices:", error);
    invoices.value = [];
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

const fetchAllManagerReplenishments = async () => {
  const token = localStorage.getItem("authToken");
  if (!token) {
    console.error("Not authenticated");
    return;
  }

  try {
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
      allManagerReplenishmentTransactions.value = orders;
      console.log("All manager replenishment orders fetched:", orders);
    } else {
      console.error("Failed to fetch manager replenishment orders:", response.status);
    }
  } catch (error) {
    console.error("Error fetching manager replenishment orders:", error);
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
  if (!invoiceForm.value.appointmentId) {
    invoiceError.value = "Please select an appointment";
    return;
  }

  const token = localStorage.getItem("authToken");
  if (!token) {
    invoiceError.value = "Not authenticated";
    return;
  }

  try {
    // First, fetch the appointment details from the API
    console.log("Fetching appointment details for ID:", invoiceForm.value.appointmentId);
    const apptResponse = await fetch(`${API_BASE_URL}/api/appointment/${invoiceForm.value.appointmentId}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (!apptResponse.ok) {
      const errText = await apptResponse.text();
      console.error("Failed to fetch appointment details:", apptResponse.status, errText);
      invoiceError.value = "Failed to fetch appointment details";
      return;
    }

    const appointment = await apptResponse.json();
    console.log("Appointment fetched:", appointment);

    // Extract ALL service IDs and calculate total from the appointment
    const serviceIds = appointment.services && appointment.services.length > 0 ? appointment.services.map(s => s.id) : [];
    const totalAmount = appointment.services ? appointment.services.reduce((sum, s) => sum + (s.price || 0), 0) : 0;

    if (!serviceIds || serviceIds.length === 0) {
      invoiceError.value = "Appointment has no services";
      return;
    }

    // Create invoice with the appointment data
    const invoicePayload = {
      customer_id: appointment.customer_id,
      staff_id: appointment.staff_id,
      service_ids: serviceIds.join(','),
      invoice_amount: totalAmount,
      other_charges: 0,
      discount_percentage: invoiceForm.value.discount || 0
    };

    console.log("📋 Creating invoice for appointment:", invoiceForm.value.appointmentId);
    console.log("📋 Invoice payload:", invoicePayload);

    const response = await fetch(`${API_BASE_URL}/api/invoice/${invoiceForm.value.appointmentId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      },
      body: JSON.stringify(invoicePayload)
    });

    if (response.ok) {
      const result = await response.json();
      console.log("✅ Invoice created successfully:", result);
      invoiceSuccess.value = "Invoice created successfully!";
      invoiceError.value = "";
      invoiceForm.value = {
        appointmentId: null,
        customerId: null,
        staffId: null,
        staffName: null,
        serviceIds: [],
        totalServiceAmount: 0,
        date: new Date().toISOString().split('T')[0],
        paymentType: "cash",
        discount: 0,
        services: []
      };
      setTimeout(() => invoiceSuccess.value = "", 3000);
      await fetchInvoices();
      await fetchAppointments(); // Reload appointments to refresh the list
    } else {
      const errText = await response.text();
      console.error("❌ Failed to create invoice. Status:", response.status, "Error:", errText);
      invoiceError.value = "Failed to create invoice: " + errText;
    }
  } catch (error) {
    console.error("❌ Error creating invoice:", error);
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

    // Create order delivered notification IMMEDIATELY when clicked
    try {
      const notificationPayload = {
        subject: "Order Delivered",
        body: `Order for ${order.product_name} has been successfully delivered. Stock replenished by ${order.order_quantity} units.`,
        phone_number: "N/A"
      };

      await fetch(`${API_BASE_URL}/api/send-notification`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
          "Authentication-Token": token
        },
        body: JSON.stringify(notificationPayload)
      });
    } catch (notifError) {
      console.warn("Failed to create order delivered notification:", notifError);
    }

    // Step 1: Update order status to Delivered (1) via PUT order API
    const orderPayload = {
      status: 1, // Mark as Processed/Delivered
      order_quantity: order.order_quantity
    };

    const orderResponse = await fetch(`${API_BASE_URL}/api/order/${order.order_id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      },
      body: JSON.stringify(orderPayload)
    });

    const orderResult = await orderResponse.json();

    if (!orderResponse.ok) {
      alert(orderResult.message || "Failed to mark order as delivered");
      console.error("Error marking order delivered:", orderResult);
      return;
    }

    // Step 2: Create inventory transaction to replenish stock via POST inventory-transaction API
    const txnPayload = {
      product_id: order.product_id,
      quantity: order.order_quantity
      // txn_type will be set to 1 (manager replenishment) by the backend
    };

    const txnResponse = await fetch(`${API_BASE_URL}/api/inventory-transaction`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      },
      body: JSON.stringify(txnPayload)
    });

    const txnResult = await txnResponse.json();

    if (txnResponse.ok) {
      alert(`Order marked as Delivered! Stock replenished by ${order.order_quantity} units.`);
      console.log("Order delivered:", orderResult);
      console.log("Inventory transaction created:", txnResult);
      
      // Refresh both orders and products
      await fetchManagerOrders();
      console.log("Manager orders refreshed after delivery");
      
      await fetchAllManagerReplenishments();
      console.log("Manager replenishments refreshed after delivery");
      
      await fetchProducts();
      console.log("Products refreshed after delivery");
    } else {
      alert("Order marked as delivered, but failed to create inventory transaction: " + (txnResult.message || "Unknown error"));
      console.error("Error creating inventory transaction:", txnResult);
      
      // Still refresh since order was updated
      await fetchManagerOrders();
      await fetchAllManagerReplenishments();
      await fetchProducts();
    }
  } catch (error) {
    alert("Unable to connect to server. Please try again.");
    console.error("Network error:", error);
  }
};

// Place grouped supplier orders to wholesale
const handlePlaceOrderToWholesale = async (supplierGroup) => {
  if (!confirm(`Are you sure you want to mark all ${supplierGroup.items.length} item(s) as sent to wholesale for supplier "${supplierGroup.supplier}"?`)) {
    return;
  }

  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      alert("Authentication required. Please login again.");
      return;
    }

    // Get supplier email from the first item
    const supplierEmail = supplierGroup.items[0]?.supplier_email;
    if (!supplierEmail) {
      alert("Error: Supplier email not found");
      return;
    }

    // Create pending delivery notification IMMEDIATELY when clicked
    try {
      const notificationPayload = {
        subject: "Order Pending Delivery",
        body: `${supplierGroup.items.length} order(s) placed with supplier "${supplierGroup.supplier}" and sent to wholesaler. Awaiting delivery.`,
        phone_number: "N/A"
      };

      await fetch(`${API_BASE_URL}/api/send-notification`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
          "Authentication-Token": token
        },
        body: JSON.stringify(notificationPayload)
      });
    } catch (notifError) {
      console.warn("Failed to create pending delivery notification:", notifError);
    }

    // Call API to generate PDF, send email, and advance orders to Pending Delivery (status=0)
    console.log(`Calling API to generate wholesale order PDF for ${supplierEmail}...`);
    
    const generateResponse = await fetch(`${API_BASE_URL}/api/generate-wholesaler-order/${encodeURIComponent(supplierEmail)}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    console.log("Generate response status:", generateResponse.status);

    if (generateResponse.ok) {
      // Handle PDF file download
      const blob = await generateResponse.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `order_${supplierGroup.supplier.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      console.log("PDF downloaded successfully");
    } else {
      const errorText = await generateResponse.text();
      console.error("Error generating PDF:", generateResponse, errorText);
    }

    // Refresh lists to reflect the updated order statuses
    await fetchManagerOrders();
    await fetchAllManagerReplenishments();

    const summary = `Orders Confirmed for Wholesale!\n================================\nSupplier: ${supplierGroup.supplier}\nTotal Items: ${supplierGroup.items.length}\n\nWholesale Order PDF has been generated and sent to: ${supplierEmail}\n\nOrders are now visible in "Wholesale Orders Placed"`;
    alert(summary);

    console.log(`${supplierGroup.items.length} orders confirmed for wholesale with ${supplierGroup.supplier}`);
  } catch (error) {
    alert("Error: " + error.message);
    console.error("Critical error:", error);
  }
};

// Get status color
const getStatusColor = (status) => {
  switch(status) {
    case 2: // Added to Cart - In progress
      return { bg: '#fff3cd', text: '#856404' };
    case 0: // Pending - Sent to wholesale, awaiting delivery
      return { bg: '#cfe2ff', text: '#084298' };
    case 1: // Delivered - Completed
      return { bg: '#d4edda', text: '#155724' };
    default:
      return { bg: '#e2e3e5', text: '#383d41' };
  }
};

// Get status label
const getStatusLabel = (status) => {
  switch(status) {
    case 2: return "Added to Cart";
    case 0: return "Pending Delivery";
    case 1: return "Delivered";
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
        bookingServiceSearch.value = "";
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
  
  // Scroll to the service form after DOM update
  nextTick(() => {
    if (serviceFormRef.value) {
      serviceFormRef.value.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
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

const viewFeedback = async (invoice) => {
  try {
    console.log("📝 Opening feedback for appointment:", invoice.appointment_id);
    
    // Check if review is already mapped in invoice object
    if (invoice.review) {
      console.log("✅ Review already loaded:", invoice.review);
      currentFeedback.value = invoice.review;
      feedbackError.value = "";
    } else if (invoice.rating || invoice.review_text) {
      // Construct feedback object from mapped data
      currentFeedback.value = {
        rating: invoice.rating,
        review: invoice.review_text,
        staff_name: invoice.staff_name,
        services: invoice.service_names ? invoice.service_names.split(",") : [],
        datetime: invoice.invoice_date
      };
      feedbackError.value = "";
    } else {
      console.log("No feedback found for this invoice");
      currentFeedback.value = null;
      feedbackError.value = "No feedback has been provided yet for this invoice";
    }
    
    showFeedbackModal.value = true;
  } catch (error) {
    console.error("❌ Error viewing feedback:", error);
    feedbackError.value = "Error loading feedback: " + error.message;
    showFeedbackModal.value = true;
  }
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
        pointsBalance: c.customer_available_rewards || 0,
        totalSpent: c.total_spend || 0
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
  
  // Scroll to the customer form
  setTimeout(() => {
    if (customerFormRef.value) {
      customerFormRef.value.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }, 50);
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
        status: s.active ? "active" : "inactive"
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

const handleSendInvoice = async (invoice) => {
  const customerEmail = data.value.customers.find(c => c.id === invoice.customer_id)?.email;
  const customerName = getCustomerName(invoice.customer_id);
  
  if (!customerEmail) {
    alert("Customer email not found!");
    return;
  }

  // Show confirmation dialog
  if (!confirm(`Send invoice to ${customerName} (${customerEmail})?\n\nInvoice: #${invoice.invoice_number}\nAmount: ₹${invoice.total_charges}`)) {
    return;
  }

  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      alert("Authentication required. Please login again.");
      return;
    }

    // Call API to generate and send invoice PDF
    const response = await fetch(`${API_BASE_URL}/api/generate-invoice-pdf/${encodeURIComponent(invoice.invoice_number)}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (response.ok) {
      const contentType = response.headers.get("Content-Type") || "";
      if (contentType.includes("application/pdf")) {
        // Trigger PDF download in browser
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `invoice_${invoice.invoice_number}.pdf`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      }

      alert(`✓ Invoice #${invoice.invoice_number} PDF generated and sent successfully to ${customerEmail}!`);

      // Refresh invoices list
      await fetchInvoices();
    } else {
      let errorMsg = "Failed to generate PDF";
      try {
        const result = await response.json();
        errorMsg = result.message || errorMsg;
      } catch (_) {}
      alert(`Error sending invoice: ${errorMsg}`);
    }
  } catch (error) {
    alert("Unable to connect to server. Please try again.");
    console.error("Network error:", error);
  }
};

// Mark staff absent with automated notifications
const handleMarkStaffAbsentWithNotifications = async () => {
  if (!confirm("Are you sure you want to mark all unmarked staff as absent for today? Notifications will be sent to manager.")) {
    return;
  }

  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      alert("Authentication required. Please login again.");
      return;
    }

    // Step 1: Mark all unmarked staff as absent
    const markResponse = await fetch(`${API_BASE_URL}/api/mark-staff-absent`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    const markResult = await markResponse.json();

    if (!markResponse.ok) {
      alert("Error marking staff absent: " + (markResult.message || "Unknown error"));
      console.error("Error marking staff absent:", markResult);
      return;
    }

    // Step 2: Get today's absent staff for notifications
    const attendanceResponse = await fetch(`${API_BASE_URL}/api/manager-staff-attendance?date=${new Date().toISOString().split('T')[0]}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    const attendanceData = await attendanceResponse.json();
    
    if (!attendanceResponse.ok) {
      // Still show success since staff were marked absent, but notify about notification error
      alert(markResult.message || "Staff marked absent (notification fetch failed)");
      return;
    }

    // Step 3: Find absent staff (present_flag = false)
    const absentStaffList = Array.isArray(attendanceData) ? attendanceData.filter(a => !a.present_flag) : [];

    let notificationsSent = 0;
    let notificationsFailed = 0;

    // Step 4: Send notifications for each absent staff member
    for (const attendance of absentStaffList) {
      try {
        const staffMember = data.value.staff.find(s => s.id === attendance.staff_id);
        if (!staffMember) continue;

        const notificationPayload = {
          subject: "Staff Absent Notification",
          body: `${staffMember.name} is marked absent today (${new Date().toLocaleDateString()})`,
          phone_number: staffMember.phone || "N/A"
        };

        const notifResponse = await fetch(`${API_BASE_URL}/api/send-notification`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
            "Authentication-Token": token
          },
          body: JSON.stringify(notificationPayload)
        });

        if (notifResponse.ok) {
          notificationsSent++;
          console.log(`Notification sent for ${staffMember.name}`);
        } else {
          notificationsFailed++;
          console.error(`Failed to send notification for ${staffMember.name}`);
        }
      } catch (error) {
        notificationsFailed++;
        console.error("Error sending notification:", error);
      }
    }

    const summary = `Staff Marked Absent!\n================================\n${markResult.message}\n\nNotifications Sent: ${notificationsSent}\nNotifications Failed: ${notificationsFailed}`;
    alert(summary);

    // Refresh attendance data
    await fetchManagerAttendance();
    
    console.log(`Marked staff absent and sent ${notificationsSent} notifications`);
  } catch (error) {
    alert("Critical error: " + error.message);
    console.error("Critical error:", error);
  }
};

// Fetch all notifications for current user
const fetchNotifications = async () => {
  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      alert("Authentication required. Please login again.");
      return;
    }

    notificationsLoading.value = true;
    const response = await fetch(`${API_BASE_URL}/api/send-notification?include_read=false`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (response.ok) {
      notificationsList.value = await response.json();
    } else {
      console.error("Failed to fetch notifications:", response.statusText);
      notificationsList.value = [];
    }
  } catch (error) {
    console.error("Error fetching notifications:", error);
    notificationsList.value = [];
  } finally {
    notificationsLoading.value = false;
  }
};

// Mark a notification as read
const markNotificationAsRead = async (notificationId) => {
  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      alert("Authentication required. Please login again.");
      return;
    }

    const response = await fetch(`${API_BASE_URL}/api/send-notification/${notificationId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (response.ok) {
      // Update local state to mark as read
      const notification = notificationsList.value.find(n => n.id === notificationId);
      if (notification) {
        notification.is_read = true;
      }
      console.log(`Notification ${notificationId} marked as read`);
    } else {
      console.error("Failed to mark notification as read:", response.statusText);
    }
  } catch (error) {
    console.error("Error marking notification as read:", error);
  }
};

// Toggle notification panel
const toggleNotificationPanel = async () => {
  showNotificationPanel.value = !showNotificationPanel.value;
  if (showNotificationPanel.value) {
    await fetchNotifications();
  }
};

// Mark all notifications as read
const markAllNotificationsAsRead = async () => {
  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      alert("Authentication required. Please login again.");
      return;
    }

    const unreadNotifs = notificationsList.value.filter(n => !n.is_read);
    
    for (const notification of unreadNotifs) {
      await markNotificationAsRead(notification.id);
    }
    
    console.log(`Marked ${unreadNotifs.length} notifications as read`);
  } catch (error) {
    console.error("Error marking all notifications as read:", error);
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

const fetchFinanceData = async (monthInYYYYMMFormat = null) => {
  try {
    financeLoading.value = true;
    financeError.value = null;
    
    const token = localStorage.getItem('authToken');
    if (!token) {
      financeError.value = "User not authenticated";
      return;
    }

    // Get the month's last date
    let lastDateStr;
    if (monthInYYYYMMFormat) {
      // Parse YYYY-MM format
      const [year, month] = monthInYYYYMMFormat.split('-');
      const lastDay = new Date(parseInt(year), parseInt(month), 0);
      lastDateStr = lastDay.toISOString().split('T')[0];
    } else {
      // Current month's last date
      const now = new Date();
      const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0);
      lastDateStr = lastDay.toISOString().split('T')[0];
    }
    
    // Always call POST first to ensure fresh calculations
    console.log('Regenerating finance report for', lastDateStr);
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
      console.log('Finance data populated with fresh calculations:', data);
    } else {
      throw new Error(`Failed to populate balance sheet: ${response.status}`);
    }
  } catch (error) {
    console.error('Error populating finance data:', error);
    financeError.value = error.message;
  } finally {
    financeLoading.value = false;
  }
};

const loadBalanceSheetForMonth = async () => {
  await fetchFinanceData(selectedBalanceSheetMonth.value);
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
const _triggerReportFromChat = async (userMessage, overrideIntent = null) => {
  const token = localStorage.getItem("authToken");
  const format = userMessage.includes('pdf') ? 'pdf' : 'csv';
  try {
    let intent = overrideIntent;
    if (!intent) {
      const intentRes = await fetch(`${API_BASE_URL}/ai/report-intent`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          "Authentication-Token": token,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userMessage }),
      });
      intent = await intentRes.json();
      if (!intentRes.ok || !intent.report_type) {
        return intent.message ||
          'Please specify the report type: sales, staff, appointments, inventory, or feedback.';
      }
    }

    lastReportIntent.value = intent;

    await _callGenerateReport(
      intent.report_type,
      intent.time_period,
      format,
      intent.custom_start,
      intent.custom_end,
    );

    return `Done! Your ${intent.time_period} ${intent.report_type} report (${format.toUpperCase()}) is downloading now. You can also find it in the Download Reports section.`;
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

  // Format follow-up: user says "in pdf" / "as pdf" / "pdf format" after a prior report
  const isFormatFollowUp = lastReportIntent.value && (
    userMessage.includes('pdf') || userMessage.includes('csv')
  ) && !userMessage.includes('report');
  if (isFormatFollowUp) {
    const fmt = userMessage.includes('pdf') ? 'pdf' : 'csv';
    aiMessages.value.push({ type: 'assistant', text: `Regenerating the ${lastReportIntent.value.report_type} report as ${fmt.toUpperCase()}…` });
    scrollChat();
    _triggerReportFromChat(userMessage, lastReportIntent.value).then(reply => {
      aiMessages.value.push({ type: 'assistant', text: reply });
      scrollChat();
    });
    return;
  }

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

  // All other questions → real AI with DB context
  const token = localStorage.getItem('authToken');
  const historyForApi = aiMessages.value.slice(0, -1).slice(-20); // exclude the just-added user msg
  fetch(`${API_BASE_URL}/ai/manager-chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      'Authentication-Token': token
    },
    body: JSON.stringify({
      message: userMessage,
      history: historyForApi
    })
  })
    .then(r => r.json())
    .then(data => {
      aiMessages.value.push({ type: 'assistant', text: data.response || 'Sorry, I could not get a response.' });
      scrollChat();
    })
    .catch(() => {
      aiMessages.value.push({ type: 'assistant', text: 'Connection error. Please try again.' });
      scrollChat();
    });
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
  
  // Scroll to the staff form
  nextTick(() => {
    if (staffFormRef.value) {
      staffFormRef.value.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
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
  // Ensure salon config is loaded for time slots
  fetchSalonConfig();
  
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

    const product = data.value.products.find(p => p.id === parseInt(replenishmentForm.value.productId));
    const productName = product?.name || "Product";

    const payload = {
      product_id: parseInt(replenishmentForm.value.productId),
      order_quantity: parseInt(replenishmentForm.value.quantity),
      reason_for_order: replenishmentForm.value.reason.trim()
    };

    console.log("Creating replenishment order with payload:", payload);

    const response = await fetch(`${API_BASE_URL}/api/order`, {
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
      // Reset form
      replenishmentForm.value = {
        productId: "",
        quantity: 1,
        reason: "",
        supplier: ""
      };
      
      // Refresh manager replenishments list
      await fetchAllManagerReplenishments();
      
      console.log(`Replenishment order added for ${productName}`, result);
    } else {
      replenishmentError.value = result.message || "Failed to add replenishment order";
      console.error("Error adding replenishment order:", result);
    }
  } catch (error) {
    replenishmentError.value = "Unable to connect to server. Please try again.";
    console.error("Network error:", error);
  }
};

const handleCreateInvoiceFromAppointment = async (appt) => {
  // Fetch appointment details from API
  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      console.error("Not authenticated");
      return;
    }

    console.log("Fetching appointment details for ID:", appt.id);
    const response = await fetch(`${API_BASE_URL}/api/appointment/${appt.id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error("Failed to fetch appointment details:", response.status, errText);
      return;
    }

    const appointment = await response.json();
    console.log("Appointment fetched:", appointment);
    
    // Extract ALL service IDs from services array
    const serviceIds = appointment.services && appointment.services.length > 0 ? appointment.services.map(s => s.id) : [];
    const totalServiceAmount = appointment.services ? appointment.services.reduce((sum, s) => sum + (s.price || 0), 0) : 0;
    
    // Update form with appointment details (this will auto-select the appointment)
    invoiceForm.value = {
      appointmentId: appointment.appointment_id,
      customerId: appointment.customer_id,
      staffId: appointment.staff_id,
      staffName: appointment.staff_name,
      serviceIds: serviceIds,
      totalServiceAmount: totalServiceAmount,
      date: appointment.datetime.split('T')[0],
      paymentType: "cash",
      discount: 0,
      services: appointment.services || []
    };
    console.log("Invoice form populated:", invoiceForm.value);
    currentView.value = "invoices";
    
    // Mark appointment as invoice generated
    const index = data.value.appointments.findIndex(b => b.id === appointment.appointment_id);
    if (index > -1) {
      data.value.appointments[index].invoiceGenerated = true;
    }
    
    console.log(`📄 Creating invoice for appointment #${appointment.appointment_id} (${appointment.customer_name}) - Staff: ${appointment.staff_name}, Services:`, appointment.services);
    
    // Scroll to top of page after a brief delay to allow DOM update
    setTimeout(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }, 100);
  } catch (error) {
    console.error("Error fetching appointment details:", error);
  }
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
      
      // Create notifications for low stock items
      await createLowStockNotifications();
    }
  } catch (error) {
    console.error("Error fetching products:", error);
  }
};

// Create notifications for low stock items (prevent duplicates)
const createLowStockNotifications = async () => {
  try {
    const token = localStorage.getItem("authToken");
    if (!token) return;

    // Initialize notifiedLowStockProducts from existing unread notifications
    // This prevents duplicate notifications on page reload
    notificationsList.value.forEach(n => {
      if (n.subject === "Low Stock Alert" && !n.is_read) {
        // Extract product ID or name from the notification body
        const products = data.value.products.filter(p => n.body.includes(p.name));
        products.forEach(p => notifiedLowStockProducts.add(p.id));
      }
    });

    // Get current low stock items
    const lowStockProducts = data.value.products.filter(p => p.stock <= p.minStock);
    
    if (lowStockProducts.length === 0) return;

    // Create notification only for products we haven't notified about yet
    for (const product of lowStockProducts) {
      // Skip if we've already notified about this product
      if (notifiedLowStockProducts.has(product.id)) {
        continue;
      }

      const notificationPayload = {
        subject: "Low Stock Alert",
        body: `${product.name} is running low on stock. Current: ${product.stock} units, Minimum: ${product.minStock} units.`,
        phone_number: "N/A"
      };

      try {
        await fetch(`${API_BASE_URL}/api/send-notification`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
            "Authentication-Token": token
          },
          body: JSON.stringify(notificationPayload)
        });
        // Mark this product as notified
        notifiedLowStockProducts.add(product.id);
        // Refresh notifications to show the newly created one
        await fetchNotifications();
      } catch (notifError) {
        console.warn(`Failed to create low stock notification for ${product.name}:`, notifError);
      }
    }
  } catch (error) {
    console.warn("Error creating low stock notifications:", error);
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
    from_date: extractDateOnly(setting.from_date),
    to_date: extractDateOnly(setting.to_date)
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
  // Extract just the date portion (handles "yyyy-MM-dd HH:MM:SS" format)
  const datePart = typeof dateStr === 'string' ? dateStr.substring(0, 10) : dateStr;
  const date = new Date(datePart);
  return date.toLocaleDateString();
};

// Helper function to extract date portion from various formats
const extractDateOnly = (dateStr) => {
  if (!dateStr) return '';
  // Handle both "yyyy-MM-dd HH:MM:SS" and "yyyy-MM-ddTHH:MM:SS" formats
  if (dateStr.includes('T')) {
    return dateStr.split('T')[0];
  } else if (dateStr.includes(' ')) {
    return dateStr.split(' ')[0];
  }
  return dateStr;
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
  // Fetch notifications FIRST so we can check against existing ones
  fetchNotifications();
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
  // Fetch all manager replenishments (not filtered by date)
  fetchAllManagerReplenishments();
  // Fetch manager wholesale orders
  fetchManagerOrders();
  // Fetch finance data for balance sheet
  fetchFinanceData();
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});

// Watch for date changes in staff attendance section
watch(() => selectedStaffDate.value, (newDate) => {
  if (newDate) {
    fetchManagerAttendance(newDate);
  }
});

// Watch for profile view access to load profile data
watch(() => currentView.value, (newView) => {
  if (newView === 'profile' && managerProfileData.value) {
    // Populate profileEditForm with current manager data for display
    const parseDateString = (dateString) => {
      if (!dateString) return '';
      return dateString.substring(0, 10);
    };
    
    profileEditForm.value = {
      name: managerProfileData.value.manager_name || '',
      email: managerProfileData.value.manager_email || '',
      phone: managerProfileData.value.manager_contact || '',
      role: managerProfileData.value.manager_role || '',
      doj: parseDateString(managerProfileData.value.manager_doj)
    };
  }
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
  background: var(--surface);
  border: 1.5px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 20px;
  text-align: center;
  transition: all 0.2s;
}

.report-item:hover {
  border-color: var(--gold);
  box-shadow: 0 8px 32px rgba(212,175,55,0.15);
}

.report-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.report-title {
  font-weight: 600;
  font-size: 14px;
  color: var(--text);
  margin-bottom: 4px;
}

.calendar-date {
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border);
  font-size: 12px;
  color: var(--text);
  transition: all 0.2s;
}

.calendar-date:hover {
  background: rgba(212,175,55,0.08);
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
  background: rgba(212,175,55,0.2);
  color: var(--gold-bright);
  border-radius: 50%;
  font-size: 11px;
  font-weight: 600;
}

.calendar-date.has-bookings .date-badge {
  background: var(--obsidian);
  color: var(--gold);
}

.booking-item {
  padding: 0 0 12px 0;
  font-size: 13px;
  color: var(--text);
}

.booking-time {
  background: rgba(212,175,55,0.12);
  border: 1px solid rgba(212,175,55,0.28);
  border-radius: var(--radius-sm);
  padding: 6px 10px;
  font-weight: 600;
  color: var(--gold-bright);
  white-space: nowrap;
}

.calendar-date-horizontal {
  padding: 12px;
  border-radius: var(--radius-sm);
  background: rgba(255,255,255,0.04);
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
  background: rgba(212,175,55,0.08);
  border-color: var(--gold);
}

.calendar-date-horizontal.has-bookings {
  background: rgba(212,175,55,0.15);
  color: var(--gold-bright);
  border-color: var(--gold);
  font-weight: 600;
}

.calendar-date-horizontal.selected {
  background: linear-gradient(135deg, var(--gold-deep), var(--gold));
  color: var(--obsidian);
  border-color: transparent;
}

.calendar-date-horizontal.selected.has-bookings {
  background: linear-gradient(135deg, var(--gold-deep), var(--gold));
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
  background: rgba(255,255,255,0.04);
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
  color: var(--text);
}
.dropdown-search-input::placeholder { color: rgba(255,255,255,0.28); }

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
  background: #1E1E1E;
  border: 1px solid var(--border);
  border-top: none;
  border-radius: 0 0 var(--radius-sm) var(--radius-sm);
  max-height: 250px;
  overflow-y: auto;
  z-index: 10;
  box-shadow: var(--shadow-md);
}

.dropdown-option {
  padding: 12px 12px;
  cursor: pointer;
  border-bottom: 1px solid var(--divider);
  transition: background-color 0.2s;
  color: var(--text);
  font-size: 13px;
}

.dropdown-option:hover {
  background-color: rgba(212,175,55,0.08);
}

.dropdown-option.selected {
  background-color: rgba(212, 175, 55, 0.12);
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
  background: var(--surface);
  border: 1px solid rgba(212,175,55,0.18);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-xl);
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
  border-bottom: 1px solid var(--divider);
}

.modal-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text);
  margin: 0;
  font-family: var(--font-display);
}

.modal-close {
  background: none;
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 18px;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.modal-close:hover {
  border-color: var(--gold);
  color: var(--gold);
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
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 7px;
}

.form-input {
  width: 100%;
  padding: 10px 12px;
  border: 1.5px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-family: inherit;
  background: rgba(255,255,255,0.04);
  color: var(--text);
  transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
  box-sizing: border-box;
  outline: none;
}

.form-input::placeholder { color: rgba(255,255,255,0.22); }

.form-input:focus {
  border-color: var(--gold);
  background: rgba(212,175,55,0.04);
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.10);
}

.form-hint {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 4px;
}

.error-message {
  padding: 10px 12px;
  background: rgba(192, 57, 43, 0.10);
  border-left: 3px solid rgba(192,57,43,0.6);
  border-radius: var(--radius-sm);
  color: #f08070;
  font-size: 13px;
  margin-top: 12px;
}

.success-message {
  padding: 10px 12px;
  background: rgba(39, 174, 96, 0.10);
  border-left: 3px solid rgba(39,174,96,0.6);
  border-radius: var(--radius-sm);
  color: #5cba7d;
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
  background: #1A1A1A;
  border: 1px solid rgba(212,175,55,0.18);
  border-radius: 14px;
  box-shadow: var(--shadow-xl);
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
  background: rgba(0,0,0,0.2);
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
  background: rgba(255,255,255,0.07);
  color: var(--text);
  border-radius: 4px 10px 10px 10px;
  border: 1px solid var(--border);
}

.ai-assistant-input {
  display: flex;
  gap: 8px;
  padding: 12px;
  background: #1A1A1A;
  border-top: 1px solid var(--divider);
  border-radius: 0 0 14px 14px;
}

.ai-input-field {
  flex: 1;
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 13px;
  font-family: inherit;
  outline: none;
  background: rgba(255,255,255,0.05);
  color: var(--text);
  transition: border-color 0.2s;
}

.ai-input-field::placeholder { color: rgba(255,255,255,0.25); }

.ai-input-field:focus {
  border-color: var(--gold);
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.10);
}

.ai-send-btn {
  background: linear-gradient(135deg, var(--gold-deep), var(--gold));
  color: var(--obsidian);
  border: none;
  border-radius: 6px;
  padding: 8px 14px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.ai-send-btn:hover {
  filter: brightness(1.1);
  box-shadow: var(--shadow-gold);
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
.generate-tasks-btn:hover { background: var(--gold-deep); }
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
.task-item:hover { background: rgba(212,175,55,0.06); }
.task-item.completed-task { opacity: 0.55; }

.task-checkbox {
  font-size: 18px;
  line-height: 1.2;
  flex-shrink: 0;
}
.pending-cb  { color: var(--gold); }
.completed-cb { color: #5cba7d; }

.task-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.task-description {
  font-size: 13px;
  color: var(--text);
  line-height: 1.4;
}

.task-badge {
  display: inline-block;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 2px 8px;
  border-radius: 10px;
  width: fit-content;
  background: rgba(255,255,255,0.07);
  color: var(--text-muted);
}
.badge-appointments { background: rgba(43,108,176,0.15); color: #7eb8f7; border: 1px solid rgba(43,108,176,0.25); }
.badge-inventory    { background: rgba(133,100,4,0.15);  color: #e8c96a; border: 1px solid rgba(133,100,4,0.25); }
.badge-feedback     { background: rgba(197,48,48,0.15);  color: #f98080; border: 1px solid rgba(197,48,48,0.25); }
.badge-staff        { background: rgba(39,103,73,0.15);  color: #7ec8a0; border: 1px solid rgba(39,103,73,0.25); }
.badge-general      { background: rgba(255,255,255,0.07); color: var(--text-muted); }

/* ── Report Generation UI ───────────────────────────────────────────────── */
.report-ai-msg {
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  line-height: 1.5;
  margin-top: 4px;
}
.report-ai-msg--success {
  background: rgba(39,174,96,0.10);
  border: 1px solid rgba(39,174,96,0.35);
  color: #5cba7d;
}
.report-ai-msg--error {
  background: rgba(192,57,43,0.10);
  border: 1px solid rgba(192,57,43,0.35);
  color: #f08070;
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
  background: var(--surface);
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
  font-size: 15px;
  color: #ffffff;
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
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

/* Bell icon badge for unread count */
.notif-btn {
  position: relative;
  background: transparent;
  border: none;
  font-size: 20px;
  cursor: pointer;
  transition: transform 0.2s;
}

.notif-btn:hover {
  transform: scale(1.1);
}

.notif-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
  font-size: 9px;
  font-weight: 700;
  padding: 2px 5px;
  border-radius: 50%;
  min-width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

/* Notification Panel Styles */
.notification-panel {
  position: fixed;
  top: 60px;
  right: 20px;
  width: 420px;
  max-height: 600px;
  background: linear-gradient(135deg, #2a2a2a 0%, #1e1e1e 100%);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 12px;
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.6);
  display: flex;
  flex-direction: column;
  z-index: 999;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.notification-panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid rgba(212, 175, 55, 0.2);
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, rgba(212, 175, 55, 0.05) 100%);
}

.notification-panel-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--gold-bright);
  display: flex;
  align-items: center;
  gap: 8px;
}

.notification-panel-header h3::before {
  content: "⚡";
  font-size: 18px;
}

.notification-header-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.mark-all-btn {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.3), rgba(76, 175, 80, 0.1));
  border: 1px solid rgba(76, 175, 80, 0.4);
  color: #7cfc7c;
  padding: 6px 10px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.mark-all-btn:hover {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.5), rgba(76, 175, 80, 0.3));
  border-color: #7cfc7c;
}

.close-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-size: 20px;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.close-btn:hover {
  color: var(--gold);
}

.notification-panel-content {
  flex: 1;
  overflow-y: auto;
  padding: 8px 0;
}

.notification-loading,
.notification-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: var(--text-muted);
  font-size: 13px;
}

.notifications-list {
  display: flex;
  flex-direction: column;
}

.notification-item {
  padding: 14px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  display: flex;
  gap: 12px;
  align-items: flex-start;
  justify-content: space-between;
  transition: background-color 0.2s;
  border-left: 3px solid rgba(230, 126, 34, 0.6);
}

.notification-item:hover {
  background-color: rgba(212, 175, 55, 0.08);
}

.notification-item::before {
  content: "⚠";
  font-size: 18px;
  flex-shrink: 0;
  margin-top: 2px;
  margin-right: 4px;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-subject {
  font-weight: 600;
  font-size: 13px;
  color: #fff;
  margin-bottom: 4px;
}

.notification-message {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.75);
  line-height: 1.4;
  margin-bottom: 6px;
  word-break: break-word;
}

.notification-time {
  font-size: 10px;
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 8px;
}

.mark-read-btn {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.3), rgba(212, 175, 55, 0.1));
  border: 1px solid rgba(212, 175, 55, 0.4);
  color: var(--gold-bright);
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  flex-shrink: 0;
}

.mark-read-btn:hover {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.5), rgba(212, 175, 55, 0.3));
  border-color: var(--gold);
}

</style>

