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
          <div class="sidebar-logo-sub">Customer Portal</div>
        </div>
        <button style="display: none; background: none; border: none; cursor: pointer; font-size: 24px" @click="sidebarOpen = false" class="mobile-close-btn">✕</button>
      </div>
      <nav class="sidebar-nav">
        <div class="nav-section">Bookings</div>
        <div
          :class="['nav-item', { active: currentView === 'dashboard' }]"
          @click.stop="currentView = 'dashboard'; sidebarOpen = false"
          style="cursor: pointer; user-select: none"
        >
          <span class="nav-icon">📊</span> Dashboard
        </div>
        <div
          :class="['nav-item', { active: currentView === 'book-appointment' }]"
          @click.stop="currentView = 'book-appointment'; sidebarOpen = false"
          style="cursor: pointer; user-select: none"
        >
          <span class="nav-icon">📅</span> Book Appointment
        </div>
        <div
          :class="['nav-item', { active: currentView === 'appointments' }]"
          @click.stop="currentView = 'appointments'; sidebarOpen = false"
          style="cursor: pointer; user-select: none"
        >
          <span class="nav-icon">📋</span> My Appointments
        </div>
        <div
          :class="['nav-item', { active: currentView === 'feedback' }]"
          @click.stop="currentView = 'feedback'; sidebarOpen = false"
          style="cursor: pointer; user-select: none"
        >
          <span class="nav-icon">💬</span> Feedback & Reviews
        </div>
        <div
          :class="['nav-item', { active: currentView === 'services' }]"
          @click="currentView = 'services'; sidebarOpen = false"
          style="cursor: pointer; user-select: none; z-index: 10"
        >
          <span class="nav-icon">💇</span> Browse Services
        </div>
      </nav>
      <div class="sidebar-footer">
        <div class="sidebar-user" @click="showProfileMenu = !showProfileMenu" style="cursor: pointer; position: relative">
          <div class="sidebar-avatar">{{ customerData.name[0] }}</div>
          <div style="flex: 1">
            <div class="sidebar-username">{{ customerData.name }}</div>
            <div class="sidebar-role">{{ customerData.membershipStatus }}</div>
          </div>
          <div style="font-size: 18px">▼</div>
          
          <!-- Profile Dropdown Menu -->
          <div v-if="showProfileMenu" class="profile-dropdown" @click.stop style="position: absolute; bottom: 100%; left: 0; width: 220px; background: white; border: 1px solid var(--border); border-radius: 8px; box-shadow: 0 -2px 8px rgba(0,0,0,0.1); margin-bottom: 8px; z-index: 1000">
            <button class="profile-menu-item" @click="currentView = 'profile'; showProfileMenu = false" style="width: 100%; padding: 12px 16px; text-align: left; border: none; background: none; cursor: pointer; font-size: 14px; color: var(--charcoal); transition: background-color 0.2s; border-bottom: 1px solid var(--border)">
              👤 Profile
            </button>
            <button class="profile-menu-item" @click="showChangePasswordModal = true; showProfileMenu = false" style="width: 100%; padding: 12px 16px; text-align: left; border: none; background: none; cursor: pointer; font-size: 14px; color: var(--charcoal); transition: background-color 0.2s; border-bottom: 1px solid var(--border)">
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
              <div class="stat-value">{{ summaryData.upcoming_appointments_count }}</div>
              <div class="stat-label">Upcoming Appointments</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">✅</div>
              <div class="stat-value">{{ summaryData.past_appointments_count }}</div>
              <div class="stat-label">Past Appointments</div>
            </div>

            <div class="stat-card">
              <div class="stat-icon">⭐</div>
              <div class="stat-value">{{ summaryData.customer_type || 'Regular' }}</div>
              <div class="stat-label">Membership Status</div>
            </div>

            <div class="stat-card">
              <div class="stat-icon">🎁</div>
              <div class="stat-value">{{ summaryData.available_rewards }}</div>
              <div class="stat-label">Reward Points</div>
            </div>
          </div>

          <!-- Upcoming & Recent Services + AI Chatbot -->
          <div class="grid-2" style="margin-top: 24px">
            <!-- Upcoming Appointments -->
            <div class="card">
              <div class="card-header">
                <h3 class="card-title">📅 Upcoming Appointments</h3>
              </div>
              <div class="card-body">
                <div v-if="loadingUpcomingAppointments" style="text-align: center; padding: 20px; color: var(--text-muted)">
                  <p>Loading...</p>
                </div>
                <div v-else-if="upcomingAppointmentsData.length === 0" class="empty-state">
                  <div class="empty-state-icon">📅</div>
                  <div class="empty-state-text">No upcoming appointments</div>
                  <button class="btn btn-primary" style="margin-top: 12px" @click="currentView = 'book-appointment'">Book Now</button>
                </div>
                <div v-for="appt in upcomingAppointmentsData" :key="appt.id" class="booking-item">
                  <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px">
                    <div>
                      <div style="font-weight: 600">{{ appt.service_name }}</div>
                      <div class="text-muted">with {{ appt.staff_name }}</div>
                    </div>
                    <span class="badge badge-gold">₹{{ appt.price }}</span>
                  </div>
                  <div class="text-muted" style="font-size: 12px; margin-bottom: 8px">
                    {{ appt.date }} at {{ appt.time }}
                  </div>
                  <div style="display: flex; gap: 8px">
                    <button class="btn btn-sm btn-outline" style="flex: 1">
                      Reschedule
                    </button>
                    <button class="btn btn-sm btn-danger" style="flex: 1">
                      Cancel
                    </button>
                  </div>
                  <div style="height: 1px; background: var(--border); margin: 8px 0"></div>
                </div>
              </div>
            </div>

            <!-- AI Assistant Chatbot -->
            <div class="card">
              <div class="card-header" style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 18px;">🤖</span>
                <h3 class="card-title" style="margin: 0;">AI Beauty Assistant</h3>
                <span style="font-size: 11px; background: #e6f4ea; color: #276749; padding: 2px 8px; border-radius: 10px; font-weight: 600; margin-left: 4px;">AI Powered</span>
              </div>
              <!-- Quick prompt chips -->
              <div style="padding: 8px 16px; display: flex; flex-wrap: wrap; gap: 6px; border-bottom: 1px solid var(--border);">
                <button v-for="chip in ['Recommend a service', 'My reward points', 'How to book?', 'Best for dry hair', 'Bridal packages']"
                  :key="chip"
                  @click="chatInput = chip; sendChatMessage()"
                  style="font-size: 11px; padding: 3px 10px; border-radius: 12px; border: 1px solid var(--border); background: var(--light-bg); cursor: pointer; color: var(--charcoal);"
                  :disabled="chatLoading"
                >{{ chip }}</button>
              </div>
              <div class="card-body" style="display: flex; flex-direction: column; height: 400px">
                <div class="chat-messages" ref="chatScrollEl" style="flex: 1; overflow-y: auto; margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid var(--border)">
                  <div v-for="(msg, idx) in chatMessages" :key="idx" :class="['chat-message', msg.type]" style="margin-bottom: 12px">
                    <div :style="msg.type === 'user' ? { textAlign: 'right', paddingLeft: '40px' } : { textAlign: 'left', paddingRight: '40px' }">
                      <div :style="msg.type === 'user' ? { background: 'var(--gold)', color: 'white' } : { background: 'var(--light-bg)', color: 'var(--charcoal)' }" style="padding: 8px 12px; border-radius: 8px; display: inline-block; max-width: 260px; word-wrap: break-word; text-align: left; white-space: pre-wrap;">
                        <span v-if="msg.isTyping" style="letter-spacing: 2px; opacity: 0.6;">● ● ●</span>
                        <span v-else>{{ msg.text }}</span>
                      </div>
                      <div class="text-muted" style="font-size: 11px; margin-top: 4px">{{ msg.time }}</div>
                    </div>
                  </div>
                </div>
                <div style="display: flex; gap: 8px">
                  <input
                    v-model="chatInput"
                    type="text"
                    placeholder="Ask about services, prices, stylists…"
                    class="form-input"
                    style="flex: 1"
                    @keyup.enter="sendChatMessage"
                    :disabled="chatLoading"
                  />
                  <button class="btn btn-primary" style="padding: 10px 16px" @click="sendChatMessage" :disabled="chatLoading">
                    {{ chatLoading ? '…' : 'Send' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- BOOK APPOINTMENT VIEW -->
        <div v-if="currentView === 'book-appointment'" class="fade-in">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">📅 Book an Appointment</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleBookAppointment" style="max-width: 800px">
                <div class="form-group">
                  <label>Select Services * (You can choose multiple)</label>
                  <div style="border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 12px; max-height: 300px; overflow-y: auto">
                    <div v-for="service in customerData.availableServices" :key="service.id" style="display: flex; align-items: center; margin-bottom: 12px">
                      <input 
                        :id="'service-' + service.id"
                        type="checkbox" 
                        :value="service.id" 
                        v-model="bookingForm.serviceIds"
                        style="margin-right: 8px; width: 18px; height: 18px; cursor: pointer"
                      />
                      <label :for="'service-' + service.id" style="cursor: pointer; flex: 1; margin: 0">
                        {{ service.name }} - ₹{{ service.price }} ({{ service.duration }} min)
                      </label>
                    </div>
                  </div>
                  <div v-if="bookingForm.serviceIds.length === 0" class="text-muted" style="margin-top: 8px; font-size: 12px">Please select at least one service</div>
                </div>

                <div class="grid-2" style="margin-top: 16px">
                  <div class="form-group">
                    <label for="stylist">Select Stylist (Optional)</label>
                    <select 
                      id="stylist"
                      v-model="bookingForm.staffId" 
                      class="form-input"
                    >
                      <option value="">Choose a stylist (Optional)</option>
                      <option v-for="staff in availableStylists" :key="staff.id" :value="staff.id">
                        {{ staff.name }}{{ staff.skills ? ' - ' + staff.skills : '' }}
                      </option>
                    </select>
                    <div v-if="bookingForm.staffId" class="text-muted" style="font-size: 12px; margin-top: 6px">
                      Selected: {{ availableStylists.find(s => s.id == bookingForm.staffId)?.name }}{{ availableStylists.find(s => s.id == bookingForm.staffId)?.skills ? ' - Specializes in ' + availableStylists.find(s => s.id == bookingForm.staffId)?.skills : '' }}
                    </div>
                  </div>

                  <div class="form-group">
                    <label for="date">Select Date *</label>
                    <input 
                      id="date"
                      v-model="bookingForm.date" 
                      type="date" 
                      class="form-input"
                      :min="minBookingDate"
                      :max="maxBookingDate"
                      required
                    />
                    <div v-if="bookingDateInfo" class="text-muted" style="font-size: 12px; margin-top: 6px">
                      {{ bookingDateInfo }}
                    </div>
                  </div>

                  <div class="form-group">
                    <label for="time">Select Time *</label>
                    <select 
                      id="time"
                      v-model="bookingForm.time" 
                      class="form-input"
                      required
                    >
                      <option value="">Choose a time</option>
                      <option v-for="time in availableTimes" :key="time">
                        {{ time }}
                      </option>
                    </select>
                  </div>
                </div>



                <div v-if="bookingError" class="error-message">{{ bookingError }}</div>
                <div v-if="bookingSuccess" class="success-message">{{ bookingSuccess }}</div>

                <div style="display: flex; gap: 12px; margin-top: 20px">
                  <button type="submit" class="btn btn-primary">
                    Confirm Booking ({{ bookingForm.serviceIds.length }} service{{ bookingForm.serviceIds.length !== 1 ? 's' : '' }})
                  </button>
                  <button type="button" class="btn btn-outline" @click="currentView = 'services'">
                    Back to Services
                  </button>
                </div>
              </form>
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
              <!-- Tab Navigation -->
              <div style="display: flex; gap: 12px; margin-bottom: 20px; border-bottom: 2px solid var(--border); padding-bottom: 0">
                <button
                  @click="appointmentsTab = 'upcoming'"
                  :style="{
                    padding: '12px 16px',
                    border: 'none',
                    background: 'none',
                    cursor: 'pointer',
                    fontSize: '14px',
                    fontWeight: '600',
                    color: appointmentsTab === 'upcoming' ? 'var(--gold)' : 'var(--text-muted)',
                    borderBottom: appointmentsTab === 'upcoming' ? '3px solid var(--gold)' : 'none',
                    transition: 'all 0.2s'
                  }"
                >
                  📅 Upcoming ({{ upcomingAppointmentsData.length }})
                </button>
                <button
                  @click="appointmentsTab = 'history'"
                  :style="{
                    padding: '12px 16px',
                    border: 'none',
                    background: 'none',
                    cursor: 'pointer',
                    fontSize: '14px',
                    fontWeight: '600',
                    color: appointmentsTab === 'history' ? 'var(--gold)' : 'var(--text-muted)',
                    borderBottom: appointmentsTab === 'history' ? '3px solid var(--gold)' : 'none',
                    transition: 'all 0.2s'
                  }"
                >
                  ✅ History ({{ historyAppointmentsData.length }})
                </button>
              </div>

              <!-- UPCOMING APPOINTMENTS TAB -->
              <div v-if="appointmentsTab === 'upcoming'">
                <div v-if="loadingUpcomingAppointments" style="text-align: center; padding: 20px; color: var(--text-muted)">
                  <p>Loading upcoming appointments...</p>
                </div>
                <div v-else-if="upcomingAppointmentsError" class="error-message" style="margin-bottom: 16px">
                  {{ upcomingAppointmentsError }}
                </div>
                <div v-else-if="upcomingAppointmentsData.length === 0" style="text-align: center; padding: 40px 20px; color: var(--text-muted)">
                  <div style="font-size: 48px; margin-bottom: 12px">📅</div>
                  <div style="font-size: 16px; margin-bottom: 12px">No upcoming appointments</div>
                  <p style="margin-bottom: 16px">You don't have any scheduled appointments yet.</p>
                  <button class="btn btn-primary" @click="currentView = 'book-appointment'">Book an Appointment</button>
                </div>
                <div v-else>
                  <div style="display: grid; gap: 12px">
                    <div v-for="appt in upcomingAppointmentsData" :key="appt.id" style="padding: 16px; background: var(--light-bg); border-radius: var(--radius); border-left: 4px solid var(--gold)">
                      <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px">
                        <div>
                          <div style="font-weight: 600; font-size: 16px">{{ appt.service_name }}</div>
                          <div class="text-muted" style="font-size: 13px; margin-top: 4px">with {{ appt.staff_name }}</div>
                        </div>
                        <span class="badge badge-gold" style="padding: 6px 12px">{{ appt.status }}</span>
                      </div>
                      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px">
                        <div>
                          <div class="text-muted" style="font-size: 12px">Date</div>
                          <div style="font-weight: 600">{{ appt.date }}</div>
                        </div>
                        <div>
                          <div class="text-muted" style="font-size: 12px">Time</div>
                          <div style="font-weight: 600">{{ appt.time }}</div>
                        </div>
                        <div>
                          <div class="text-muted" style="font-size: 12px">Price</div>
                          <div style="font-weight: 600; color: var(--gold)">₹{{ appt.price }}</div>
                        </div>
                      </div>
                      <div style="display: flex; gap: 8px">
                        <button class="btn btn-sm btn-outline" style="flex: 1; font-size: 12px" @click="startEditAppointment(appt)">
                          ✏️ Edit
                        </button>
                        <button class="btn btn-sm btn-danger" style="flex: 1; font-size: 12px" @click="handleCancelAppointment(appt.id)">
                          ❌ Cancel
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- APPOINTMENT HISTORY TAB -->
              <div v-if="appointmentsTab === 'history'">
                <div v-if="loadingHistoryAppointments" style="text-align: center; padding: 20px; color: var(--text-muted)">
                  <p>Loading appointment history...</p>
                </div>
                <div v-else-if="historyAppointmentsError" class="error-message" style="margin-bottom: 16px">
                  {{ historyAppointmentsError }}
                </div>
                <div v-else-if="historyAppointmentsData.length === 0" style="text-align: center; padding: 40px 20px; color: var(--text-muted)">
                  <div style="font-size: 48px; margin-bottom: 12px">✅</div>
                  <div style="font-size: 16px; margin-bottom: 12px">No past appointments yet</div>
                  <p style="margin-bottom: 16px">Start by booking your first appointment!</p>
                  <button class="btn btn-primary" @click="currentView = 'book-appointment'">Book Now</button>
                </div>
                <div v-else>
                  <div style="margin-bottom: 16px">
                    <input 
                      v-model="appointmentHistoryFilter"
                      type="text" 
                      placeholder="🔍 Filter by service or staff name..." 
                      class="form-input"
                      style="width: 100%; max-width: 300px"
                    />
                  </div>
                  <div class="table-wrap">
                    <table>
                      <thead>
                        <tr>
                          <th>Service</th>
                          <th>Staff Member</th>
                          <th>Date & Time</th>
                          <th>Price</th>
                          <th>Status</th>
                          <th>Rating</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="appt in filteredHistoryAppointments" :key="appt.id" @click="viewAppointmentDetails(appt.id)" style="cursor: pointer; transition: background-color 0.2s;" @mouseenter="($event.target.parentNode.style.backgroundColor = 'var(--light-bg)')" @mouseleave="($event.target.parentNode.style.backgroundColor = 'transparent')">
                          <td>{{ appt.service }}</td>
                          <td>{{ appt.staff }}</td>
                          <td>{{ appt.date }} {{ appt.time }}</td>
                          <td>₹{{ appt.price }}</td>
                          <td>
                            <span :class="['badge', getStatusBadgeClass(appt.status)]">{{ appt.status }}</span>
                          </td>
                          <td>
                            <div style="display: flex; align-items: center; gap: 6px">
                              <span style="letter-spacing: 1px">
                                <span v-for="i in 5" :key="i" :style="{ color: i <= (appt.rating || 0) ? 'var(--gold)' : 'var(--border)', fontSize: '12px' }">⭐</span>
                              </span>
                              <span style="font-size: 12px; font-weight: 600; color: var(--gold)">{{ appt.rating || '-' }}</span>
                            </div>
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

        <!-- SERVICES VIEW -->
        <div v-if="currentView === 'services'" class="fade-in">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Browse All Services</h3>
            </div>
            <div class="card-body">
              <!-- Loading State -->
              <div v-if="loadingServices" style="text-align: center; padding: 40px">
                <div style="font-size: 18px; color: var(--muted)">Loading services...</div>
              </div>

              <!-- Error State -->
              <div v-else-if="servicesError" style="padding: 20px; background-color: #fee; border: 1px solid #fcc; border-radius: 8px; color: #c33; margin-bottom: 20px">
                <div style="font-weight: 600">⚠️ Error Loading Services</div>
                <div style="font-size: 14px; margin-top: 8px">{{ servicesError }}</div>
              </div>

              <!-- Empty State -->
              <div v-else-if="availableServicesData.length === 0" style="text-align: center; padding: 60px 20px; color: var(--muted)">
                <div style="font-size: 48px; margin-bottom: 16px">🛁</div>
                <div style="font-size: 18px; font-weight: 600; margin-bottom: 8px">No Services Available</div>
                <div style="font-size: 14px">Services will appear here once they are added by the salon manager.</div>
              </div>

              <!-- Category Tabs -->
              <div v-else>
                <div style="display: flex; gap: 8px; margin-bottom: 24px; flex-wrap: wrap">
                  <button 
                    @click="selectedServiceCategory = null" 
                    :class="['btn', selectedServiceCategory === null ? 'btn-primary' : 'btn-outline']"
                    style="font-size: 13px; padding: 8px 14px"
                  >
                    All Services
                  </button>
                  <button 
                    v-for="category in serviceCategories" 
                    :key="category"
                    @click="selectedServiceCategory = category" 
                    :class="['btn', selectedServiceCategory === category ? 'btn-primary' : 'btn-outline']"
                    style="font-size: 13px; padding: 8px 14px"
                  >
                    {{ category }}
                  </button>
                </div>

                <!-- Services Grid -->
                <div v-if="selectedServiceCategory">
                  <!-- Single Category View -->
                  <div>
                    <h4 style="margin: 0 0 16px 0; font-weight: 600; color: var(--charcoal)">📋 {{ selectedServiceCategory }}</h4>
                    <div v-if="filteredServices.length > 0" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px">
                      <div v-for="service in filteredServices" :key="service.id" class="service-card" style="border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 16px">
                        <div style="margin-bottom: 8px">
                          <div style="font-weight: 600; font-size: 16px">{{ service.name }}</div>
                          <div class="text-muted" style="font-size: 12px">{{ service.category }}</div>
                        </div>
                        <div class="text-muted" style="font-size: 13px; margin-bottom: 12px">
                          {{ service.description }}
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px">
                          <span style="font-weight: 600; color: var(--gold); font-size: 16px">₹{{ service.price }}</span>
                          <span class="text-muted" style="font-size: 12px">{{ service.duration }} min</span>
                        </div>
                        <button type="button" class="btn btn-primary w-full" @click="startBookingFromService(service.id)">
                          Book Now
                        </button>
                      </div>
                    </div>
                    <div v-else style="text-align: center; padding: 40px; color: var(--muted)">
                      <div>No services in this category</div>
                    </div>
                  </div>
                </div>

                <div v-else>
                  <!-- All Categories View -->
                  <div v-for="category in serviceCategories" :key="category" style="margin-bottom: 32px">
                    <h4 style="margin: 0 0 16px 0; font-weight: 600; color: var(--charcoal); padding-bottom: 8px; border-bottom: 2px solid var(--gold)">📋 {{ category }}</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px">
                      <div v-for="service in getServicesByCategory(category)" :key="service.id" class="service-card" style="border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 16px">
                        <div style="margin-bottom: 8px">
                          <div style="font-weight: 600; font-size: 16px">{{ service.name }}</div>
                          <div class="text-muted" style="font-size: 12px">{{ service.category }}</div>
                        </div>
                        <div class="text-muted" style="font-size: 13px; margin-bottom: 12px">
                          {{ service.description }}
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px">
                          <span style="font-weight: 600; color: var(--gold); font-size: 16px">₹{{ service.price }}</span>
                          <span class="text-muted" style="font-size: 12px">{{ service.duration }} min</span>
                        </div>
                        <button type="button" class="btn btn-primary w-full" @click="startBookingFromService(service.id)">
                          Book Now
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- PROFILE VIEW -->
        <div v-if="currentView === 'profile'" class="fade-in">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">👤 My Profile</h3>
            </div>
            <div class="card-body">
              <div style="max-width: 600px">
                <!-- Profile Header -->
                <div style="display: flex; align-items: center; margin-bottom: 24px; padding-bottom: 24px; border-bottom: 2px solid var(--border)">
                  <div class="sidebar-avatar" style="width: 80px; height: 80px; font-size: 32px; display: flex; align-items: center; justify-content: center">{{ customerData.name[0] }}</div>
                  <div style="flex: 1; margin-left: 16px">
                    <h2 style="margin: 0 0 4px 0; font-size: 24px; color: var(--charcoal)">{{ customerData.name }}</h2>
                    <div style="font-size: 14px; color: var(--text-muted)">{{ customerData.membershipStatus }} Member</div>
                  </div>
                </div>

                <!-- Profile Details -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px">
                  <div class="detail-item">
                    <label class="detail-label">Email</label>
                    <div class="detail-value">{{ customerData.email }}</div>
                  </div>
                  <div class="detail-item">
                    <label class="detail-label">Phone</label>
                    <div class="detail-value">{{ customerData.phone }}</div>
                  </div>
                  <div class="detail-item">
                    <label class="detail-label">Address</label>
                    <div class="detail-value">{{ customerData.address || 'Not provided' }}</div>
                  </div>
                  <div class="detail-item">
                    <label class="detail-label">Date of Birth</label>
                    <div class="detail-value">{{ customerData.dob || 'Not provided' }}</div>
                  </div>
                  <div class="detail-item">
                    <label class="detail-label">Member Since</label>
                    <div class="detail-value">{{ customerData.memberSince }}</div>
                  </div>
                </div>

                <!-- Account Stats -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; padding: 16px; background: var(--light-bg); border-radius: var(--radius)">
                  <div>
                    <div style="font-size: 12px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px">Total Spent</div>
                    <div style="font-size: 20px; font-weight: 600; color: var(--gold)">₹{{ customerData.totalSpent }}</div>
                  </div>
                  <div>
                    <div style="font-size: 12px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px">Membership Status</div>
                    <div style="font-size: 20px; font-weight: 600; color: var(--charcoal)">{{ customerData.membershipStatus }}</div>
                  </div>
                </div>

                <!-- Preferred Services -->
                <div style="margin-bottom: 24px">
                  <h4 style="margin-bottom: 12px; color: var(--charcoal); font-size: 16px">💖 Preferred Services</h4>
                  <div v-if="preferredServicesList.length === 0" style="color: var(--text-muted); font-style: italic">
                    No preferred services selected
                  </div>
                  <div v-else style="display: flex; flex-wrap: wrap; gap: 8px">
                    <span v-for="service in preferredServicesList" :key="service.id" class="badge badge-gold" style="padding: 6px 12px; border-radius: 20px; font-size: 14px; font-weight: 600">
                      {{ service.name }}
                    </span>
                  </div>
                </div>

                <!-- Action Buttons -->
                <div style="display: flex; gap: 12px">
                  <button class="btn btn-primary" style="flex: 1" @click="openProfileEdit">
                    ✏️ Edit Profile
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- FEEDBACK VIEW -->
        <div v-if="currentView === 'feedback'" class="fade-in">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">💬 My Feedback & Reviews</h3>
            </div>
            <div class="card-body">
              <!-- Tab Navigation -->
              <div style="display: flex; gap: 12px; margin-bottom: 20px; border-bottom: 2px solid var(--border); padding-bottom: 0">
                <button
                  @click="appointmentsTab = 'pending'"
                  :style="{
                    padding: '12px 16px',
                    border: 'none',
                    background: 'none',
                    cursor: 'pointer',
                    fontSize: '14px',
                    fontWeight: '600',
                    color: appointmentsTab === 'pending' ? 'var(--gold)' : 'var(--text-muted)',
                    borderBottom: appointmentsTab === 'pending' ? '3px solid var(--gold)' : 'none',
                    transition: 'all 0.2s'
                  }"
                >
                  📝 Pending Reviews ({{ pendingReviews.length }})
                </button>
                <button
                  @click="appointmentsTab = 'reviewed'"
                  :style="{
                    padding: '12px 16px',
                    border: 'none',
                    background: 'none',
                    cursor: 'pointer',
                    fontSize: '14px',
                    fontWeight: '600',
                    color: appointmentsTab === 'reviewed' ? 'var(--gold)' : 'var(--text-muted)',
                    borderBottom: appointmentsTab === 'reviewed' ? '3px solid var(--gold)' : 'none',
                    transition: 'all 0.2s'
                  }"
                >
                  ⭐ My Reviews ({{ reviewedAppointments.length }})
                </button>
              </div>

              <!-- PENDING REVIEWS TAB -->
              <div v-if="appointmentsTab === 'pending'">
                <div v-if="loadingPendingReviews" style="text-align: center; padding: 20px; color: var(--text-muted)">
                  <p>Loading pending reviews...</p>
                </div>
                <div v-else-if="pendingReviewsError" class="error-message" style="margin-bottom: 16px">
                  {{ pendingReviewsError }}
                </div>
                <div v-else-if="pendingReviews.length === 0" class="empty-state">
                  <div class="empty-state-icon">📝</div>
                  <div class="empty-state-text">No pending reviews</div>
                  <p style="color: var(--text-muted); margin-top: 8px">All completed appointments have been reviewed!</p>
                </div>
                <div v-else>
                  <div style="display: grid; gap: 12px">
                    <div v-for="review in pendingReviews" :key="review.appointment_id" style="padding: 16px; background: var(--light-bg); border-radius: var(--radius); border-left: 4px solid var(--gold)">
                      <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px">
                        <div>
                          <div style="font-weight: 600; font-size: 16px">{{ review.services.join(', ') }}</div>
                          <div class="text-muted" style="font-size: 13px; margin-top: 4px">with {{ review.staff_name }}</div>
                        </div>
                        <span class="badge badge-gold" style="padding: 6px 12px">Review Needed</span>
                      </div>
                      <div class="text-muted" style="font-size: 12px; margin-bottom: 12px">
                        {{ new Date(review.datetime).toLocaleDateString() }} at {{ new Date(review.datetime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }}
                      </div>
                      <button class="btn btn-primary" style="width: 100%" @click="openReviewModal(review)">
                        Add Rating & Review
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- REVIEWED APPOINTMENTS TAB -->
              <div v-if="appointmentsTab === 'reviewed'">
                <div v-if="loadingReviewedAppointments" style="text-align: center; padding: 20px; color: var(--text-muted)">
                  <p>Loading reviewed appointments...</p>
                </div>
                <div v-else-if="reviewedAppointmentsError" class="error-message" style="margin-bottom: 16px">
                  {{ reviewedAppointmentsError }}
                </div>
                <div v-else-if="reviewedAppointments.length === 0" class="empty-state">
                  <div class="empty-state-icon">⭐</div>
                  <div class="empty-state-text">No reviews yet</div>
                  <p style="color: var(--text-muted); margin-top: 8px">Complete an appointment to leave a review</p>
                </div>
                <div v-else>
                  <div style="display: grid; gap: 16px">
                    <div v-for="review in reviewedAppointments" :key="review.appointment_id" style="padding: 16px; border: 1px solid var(--border); border-radius: var(--radius); background: white">
                      <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px">
                        <div>
                          <div style="font-weight: 600; font-size: 16px">{{ review.services.join(', ') }}</div>
                          <div class="text-muted" style="font-size: 13px; margin-top: 4px">with {{ review.staff_name }}</div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px">
                          <span style="letter-spacing: 1px">
                            <span v-for="i in 5" :key="i" :style="{ color: i <= (review.rating || 0) ? 'var(--gold)' : 'var(--border)', fontSize: '16px' }">⭐</span>
                          </span>
                          <span style="font-size: 14px; font-weight: 600; color: var(--gold)">{{ review.rating }}</span>
                        </div>
                      </div>
                      <div class="text-muted" style="font-size: 12px; margin-bottom: 12px">
                        {{ new Date(review.datetime).toLocaleDateString() }}
                      </div>
                      <div v-if="review.review" style="padding: 12px; background: var(--light-bg); border-radius: var(--radius); font-size: 14px; color: var(--charcoal)">
                        "{{ review.review }}"
                      </div>
                      <div v-else style="padding: 12px; background: var(--light-bg); border-radius: var(--radius); font-size: 14px; color: var(--text-muted); font-style: italic">
                        No review text provided
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
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
            <input id="profile-name" v-model="profileForm.name" type="text" placeholder="Enter full name" class="form-input" />
          </div>
          <div class="form-group">
            <label for="profile-email">Email</label>
            <input id="profile-email" v-model="profileForm.email" type="email" placeholder="Enter email" class="form-input" />
          </div>
          <div class="form-group">
            <label for="profile-phone">Phone</label>
            <input id="profile-phone" v-model="profileForm.phone" type="tel" placeholder="Enter phone" class="form-input" />
          </div>
          <div class="form-group">
            <label>Preferred Services</label>
            <div style="max-height: 200px; overflow-y: auto; border: 1px solid var(--border); border-radius: var(--radius); padding: 12px; background: var(--light-bg)">
              <div v-for="service in customerData.availableServices" :key="service.id" style="margin-bottom: 8px">
                <label style="display: flex; align-items: center; cursor: pointer; font-size: 14px">
                  <input 
                    type="checkbox" 
                    :value="service.id" 
                    v-model="profileForm.preferredServices"
                    style="margin-right: 8px"
                  />
                  <span>{{ service.name }} ({{ service.category }})</span>
                </label>
              </div>
            </div>
            <div class="form-hint">Select your favorite services for personalized recommendations</div>
          </div>
          <div style="display: flex; gap: 12px; margin-top: 20px">
            <button type="button" class="btn btn-outline" style="flex: 1" @click="showProfileEditModal = false">Cancel</button>
            <button type="submit" class="btn btn-primary" style="flex: 1">Save Changes</button>
          </div>
        </form>
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

  <!-- Review Rating Modal -->
  <div v-if="showReviewModal" class="modal-overlay" @click="showReviewModal = false">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3 class="modal-title">⭐ Rate & Review</h3>
        <button class="modal-close" @click="showReviewModal = false">✕</button>
      </div>
      <div class="modal-body">
        <div v-if="selectedPendingReview">
          <div style="margin-bottom: 16px; padding: 12px; background: var(--light-bg); border-radius: var(--radius)">
            <div style="font-weight: 600; margin-bottom: 4px">{{ selectedPendingReview.services.join(', ') }}</div>
            <div class="text-muted" style="font-size: 12px">
              with {{ selectedPendingReview.staff_name }} • {{ new Date(selectedPendingReview.datetime).toLocaleDateString() }}
            </div>
          </div>

          <div class="form-group">
            <label style="margin-bottom: 12px">Rating *</label>
            <div style="display: flex; gap: 12px; margin-top: 12px">
              <button 
                v-for="star in 5" 
                :key="star"
                type="button"
                @click="reviewFormData.rating = star"
                :style="{
                  background: 'none',
                  border: 'none',
                  fontSize: '40px',
                  cursor: 'pointer',
                  opacity: reviewFormData.rating >= star ? 1 : 0.3,
                  transition: 'opacity 0.2s',
                  transform: reviewFormData.rating >= star ? 'scale(1.1)' : 'scale(1)'
                }"
              >
                ⭐
              </button>
            </div>
            <div v-if="reviewFormData.rating > 0" style="margin-top: 8px; text-align: center; font-weight: 600; color: var(--gold)">
              {{ reviewFormData.rating }} out of 5 stars
            </div>
          </div>

          <div class="form-group">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <label for="review-text" style="margin: 0;">Your Review (Optional)</label>
              <button
                type="button"
                @click="showAiFeedbackPanel = !showAiFeedbackPanel; aiFeedbackError = ''"
                style="font-size: 12px; padding: 4px 10px; border-radius: 12px; border: 1px solid var(--gold); background: #fffbea; color: #8B6914; cursor: pointer; font-weight: 600;"
              >
                ✨ {{ showAiFeedbackPanel ? 'Hide AI Writer' : 'Write with AI' }}
              </button>
            </div>

            <!-- AI Feedback Writer Panel -->
            <div v-if="showAiFeedbackPanel" style="background: #fffbea; border: 1px solid #f0d060; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
              <div style="font-size: 13px; font-weight: 600; color: #8B6914; margin-bottom: 10px;">✨ Select topics your feedback covers:</div>
              <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px;">
                <button
                  v-for="kw in FEEDBACK_KEYWORDS"
                  :key="kw"
                  type="button"
                  @click="toggleFeedbackKeyword(kw)"
                  :style="{
                    fontSize: '12px',
                    padding: '5px 12px',
                    borderRadius: '14px',
                    border: aiFeedbackKeywords.includes(kw) ? '2px solid var(--gold)' : '1px solid #ddd',
                    background: aiFeedbackKeywords.includes(kw) ? 'var(--gold)' : 'white',
                    color: aiFeedbackKeywords.includes(kw) ? 'white' : 'var(--charcoal)',
                    cursor: 'pointer',
                    fontWeight: aiFeedbackKeywords.includes(kw) ? '600' : '400',
                    transition: 'all 0.15s',
                  }"
                >{{ kw }}</button>
              </div>
              <textarea
                v-model="aiFeedbackNote"
                placeholder="Optional: Add a short personal note (e.g. 'waited 20 mins, coloring was great')"
                style="width: 100%; border: 1px solid #ddd; border-radius: 6px; padding: 8px; font-size: 13px; resize: vertical; min-height: 60px; box-sizing: border-box;"
              ></textarea>
              <div v-if="aiFeedbackError" style="color: #e53e3e; font-size: 12px; margin-top: 6px;">{{ aiFeedbackError }}</div>
              <button
                type="button"
                @click="generateAiFeedback"
                :disabled="aiFeedbackLoading"
                class="btn btn-primary"
                style="margin-top: 10px; width: 100%; font-size: 13px;"
              >
                {{ aiFeedbackLoading ? '✨ Generating…' : '✨ Generate Feedback' }}
              </button>
            </div>

            <textarea
              id="review-text"
              v-model="reviewFormData.review"
              placeholder="Share your experience with this service…"
              class="form-input"
              style="resize: vertical; min-height: 100px"
            ></textarea>
          </div>

          <div v-if="reviewSubmitError" class="error-message">{{ reviewSubmitError }}</div>
          <div v-if="reviewSubmitSuccess" class="success-message">{{ reviewSubmitSuccess }}</div>

          <div style="display: flex; gap: 12px; margin-top: 20px">
            <button type="button" class="btn btn-outline" style="flex: 1" @click="showReviewModal = false">
              Cancel
            </button>
            <button type="button" class="btn btn-primary" style="flex: 1" @click="submitReview">
              Submit Review
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Appointment Details Modal -->
  <div v-if="showAppointmentDetailsModal" class="modal-overlay" @click="showAppointmentDetailsModal = false">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3 class="modal-title">📋 Appointment Details</h3>
        <button class="modal-close" @click="showAppointmentDetailsModal = false">✕</button>
      </div>
      <div class="modal-body">
        <div v-if="loadingAppointmentDetails" style="text-align: center; padding: 20px;">
          <p>Loading appointment details...</p>
        </div>
        <div v-else-if="selectedAppointment">
          <div v-if="editingAppointmentId" style="margin-bottom: 20px;">
            <!-- EDIT MODE -->
            <form @submit.prevent="handleEditAppointmentSubmit">
              <div class="form-group">
                <label>Select Services</label>
                <div style="border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 12px; max-height: 250px; overflow-y: auto">
                  <div v-for="service in customerData.availableServices" :key="service.id" style="display: flex; align-items: center; margin-bottom: 12px">
                    <input 
                      :id="'edit-service-' + service.id"
                      type="checkbox" 
                      :value="service.id" 
                      v-model="editAppointmentForm.serviceIds"
                      style="margin-right: 8px; width: 18px; height: 18px; cursor: pointer"
                    />
                    <label :for="'edit-service-' + service.id" style="cursor: pointer; flex: 1; margin: 0">
                      {{ service.name }} - ₹{{ service.price }} ({{ service.duration }} min)
                    </label>
                  </div>
                </div>
              </div>

              <div class="form-group">
                <label for="edit-stylist">Stylist (Optional)</label>
                <select 
                  id="edit-stylist"
                  v-model="editAppointmentForm.staffId" 
                  class="form-input"
                >
                  <option value="">Choose a stylist</option>
                  <option v-for="staff in availableStylists" :key="staff.id" :value="staff.id">
                    {{ staff.name }}
                  </option>
                </select>
              </div>

              <div class="form-group">
                <label for="edit-datetime">Date & Time</label>
                <input 
                  id="edit-datetime"
                  v-model="editAppointmentForm.datetime" 
                  type="datetime-local" 
                  class="form-input"
                />
              </div>

              <div style="display: flex; gap: 12px; margin-top: 20px">
                <button type="button" class="btn btn-outline" @click="editingAppointmentId = null; showAppointmentDetailsModal = false" style="flex: 1">
                  Cancel
                </button>
                <button type="submit" class="btn btn-primary" style="flex: 1">
                  Save Changes
                </button>
              </div>
            </form>
          </div>
          <div v-else style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">
            <!-- VIEW MODE -->
            <div class="detail-item">
              <label class="detail-label">Service</label>
              <div class="detail-value">{{ selectedAppointment.service || selectedAppointment.service_name }}</div>
            </div>
            <div class="detail-item">
              <label class="detail-label">Staff Member</label>
              <div class="detail-value">{{ selectedAppointment.staff || selectedAppointment.staff_name }}</div>
            </div>
            <div class="detail-item">
              <label class="detail-label">Date & Time</label>
              <div class="detail-value">{{ selectedAppointment.date }} {{ selectedAppointment.time || 'N/A' }}</div>
            </div>
            <div class="detail-item">
              <label class="detail-label">Price</label>
              <div class="detail-value">₹{{ selectedAppointment.price }}</div>
            </div>
            <div class="detail-item">
              <label class="detail-label">Duration</label>
              <div class="detail-value">{{ selectedAppointment.duration || 'N/A' }} minutes</div>
            </div>
            <div class="detail-item">
              <label class="detail-label">Status</label>
              <div class="detail-value">
                <span :class="['badge', getStatusBadgeClass(selectedAppointment.status)]">{{ selectedAppointment.status }}</span>
              </div>
            </div>
          </div>
          <div v-if="!editingAppointmentId" style="margin-top: 12px;">
            <label class="detail-label">Rating</label>
            <div style="display: flex; align-items: center; gap: 6px;">
              <span style="letter-spacing: 1px;">
                <span v-for="i in 5" :key="i" :style="{ color: i <= (selectedAppointment.rating || 0) ? 'var(--gold)' : 'var(--border)', fontSize: '14px' }">⭐</span>
              </span>
              <span style="font-size: 14px; font-weight: 600; color: var(--gold);">{{ selectedAppointment.rating || 'Not rated' }}</span>
            </div>
          </div>
        </div>
      </div>
      <div style="display: flex; gap: 12px; margin-top: 20px;">
        <button type="button" class="btn btn-outline" @click="editingAppointmentId = null; showAppointmentDetailsModal = false" style="flex: 1;">
          Close
        </button>
        <button v-if="!editingAppointmentId && selectedAppointment && selectedAppointment.status !== 'Completed'" type="button" class="btn btn-primary" @click="startEditAppointment(selectedAppointment)" style="flex: 1;">
          ✏️ Edit
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAppStore } from "../stores/appStore";
import { apiClient } from "../api/apiClient";

const router = useRouter();
const appStore = useAppStore();
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
const loadingAppointmentDetails = ref(false);
const editingAppointmentId = ref(null);
const editAppointmentForm = ref({
  staffId: "",
  serviceIds: [],
  datetime: ""
});
const profileForm = ref({
  name: "",
  email: "",
  phone: "",
  preferredServices: []
});
const passwordForm = ref({
  currentPassword: "",
  newPassword: "",
  confirmPassword: ""
});
const passwordError = ref("");
const passwordSuccess = ref("");

// Booking form state
const bookingForm = ref({
  serviceIds: [],  // Array to support multiple services
  staffId: "",
  date: "",
  time: ""
});
const bookingError = ref("");
const bookingSuccess = ref("");

// Services from backend
const availableServicesData = ref([]);
const loadingServices = ref(false);
const servicesError = ref("");

// Feedback form state
const feedbackForm = ref({
  appointmentId: "",
  rating: 0,
  comment: ""
});
const feedbackError = ref("");
const feedbackSuccess = ref("");

// Summary data state
const summaryData = ref({
  customer_type: "",
  upcoming_appointments_count: 0,
  past_appointments_count: 0,
  available_rewards: 0
});
const loadingSummary = ref(false);

// Pending reviews state
const pendingReviews = ref([]);
const loadingPendingReviews = ref(false);
const pendingReviewsError = ref("");
const showReviewModal = ref(false);
const selectedPendingReview = ref(null);
const reviewFormData = ref({
  rating: 0,
  review: ""
});
const reviewSubmitError = ref("");
const reviewSubmitSuccess = ref("");

// Reviewed appointments state
const reviewedAppointments = ref([]);
const loadingReviewedAppointments = ref(false);
const reviewedAppointmentsError = ref("");

// Chat state
const chatInput = ref("");
const chatMessages = ref([
  { type: "bot", text: "Hi! I'm your beauty assistant. How can I help you today?", time: "Now" }
]);

// Filter state
const appointmentHistoryFilter = ref("");
const selectedServiceCategory = ref(null);
const appointmentsTab = ref("upcoming"); // "upcoming" or "history"
const upcomingAppointmentsData = ref([]);
const upcomingAppointmentsError = ref("");
const loadingUpcomingAppointments = ref(false);
const historyAppointmentsData = ref([]);
const historyAppointmentsError = ref("");
const loadingHistoryAppointments = ref(false);

// Mock data with real customer name from appStore
const customerData = computed(() => {
  const username = appStore.user?.username;
  const customer = appStore.data.customers.find(c => c.customerType); // Find a customer or use first
  return {
    name: customer?.name || "John Anderson",
    email: customer?.email || "john@example.com",
    phone: customer?.phone || "+233 123 456 789",
    address: customer?.address || "123 Main Street, Accra",
    dob: customer?.dob || "1992-05-20",
    memberSince: "2024-01-15",
    membershipStatus: customer?.customerType === "VIP" ? "Gold" : "Silver",
    totalSpent: customer?.totalSpent || 1250,
    preferredServices: [1, 4, 6],
  todayStats: {
    upcomingAppointments: 1,
    totalAppointments: 12,
    lastService: "Hair Styling",
    lastServiceDate: "2026-03-02",
  },
  upcomingAppointments: [
    {
      id: 1,
      service: "Hair Styling",
      staff: "Sarah Johnson",
      date: "2026-03-06",
      time: "10:00 AM",
      price: "₹ 50",
      status: "confirmed",
    },
  ],
  appointmentHistory: [
    {
      id: 1,
      service: "Hair Styling",
      staff: "Sarah Johnson",
      date: "2026-03-02",
      price: 50,
      status: "completed",
      rating: 5,
    },
    {
      id: 2,
      service: "Manicure",
      staff: "Emma Davis",
      date: "2026-02-28",
      price: 30,
      status: "completed",
      rating: 4.5,
    },
    {
      id: 3,
      service: "Spa Package",
      staff: "Lisa Chen",
      date: "2026-02-20",
      price: 120,
      status: "completed",
      rating: 5,
    },
    {
      id: 4,
      service: "Facial Treatment",
      staff: "Sarah Johnson",
      date: "2026-02-15",
      price: 70,
      status: "completed",
      rating: 4,
    },
  ],
  availableServices: availableServicesData.value,
  feedback: [
    {
      id: 1,
      service: "Hair Styling",
      staff: "Sarah Johnson",
      date: "2026-03-02",
      rating: 5,
      comment: "Excellent service! Very professional and friendly. Highly recommend!"
    },
    {
      id: 2,
      service: "Manicure",
      staff: "Emma Davis",
      date: "2026-02-25",
      rating: 4,
      comment: "Great work! The nails look perfect."
    }
  ]
  };
});

const preferredServiceIds = ref([...customerData.value.preferredServices]);

// Available stylists
const availableStylists = ref([]);

// Fetch staff from backend
const fetchAvailableStaff = async () => {
  const token = localStorage.getItem("authToken");
  if (!token) {
    console.error("Not authenticated - cannot fetch staff");
    availableStylists.value = [];
    return;
  }

  try {
    console.log("Fetching staff with token...");
    const response = await fetch(`${API_BASE_URL}/api/staff`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token
      }
    });

    console.log("Staff fetch response status:", response.status);
    
    if (response.ok) {
      const staffList = await response.json();
      console.log("Staff list received:", staffList);
      
      if (Array.isArray(staffList)) {
        availableStylists.value = staffList.map(staff => ({
          id: staff.staff_id,
          name: staff.staff_name,
          skills: staff.staff_skills || "General Services"
        }));
        console.log("Available stylists mapped:", availableStylists.value);
      } else {
        console.error("Staff response is not an array:", staffList);
      }
    } else {
      const errorData = await response.json();
      console.error("Failed to fetch staff:", response.status, errorData);
    }
  } catch (error) {
    console.error("Error fetching staff:", error);
    availableStylists.value = [];
  }
};

// Available time slots
const availableTimes = computed(() => {
  const times = [];
  for (let hour = 9; hour <= 17; hour++) {
    times.push(`${String(hour).padStart(2, '0')}:00`);
    times.push(`${String(hour).padStart(2, '0')}:30`);
  }
  return times;
});

// Preferred services list
const preferredServicesList = computed(() => {
  const selectedIds = preferredServiceIds.value.map((id) => Number(id));
  return customerData.value.availableServices.filter(service => 
    selectedIds.includes(Number(service.id))
  );
});

// Get today's date for min date validation
const getTodayDate = computed(() => {
  const today = new Date();
  return today.toISOString().split('T')[0];
});

// Helper function to check if customer is VIP
const isVIPCustomer = () => {
  return customerData.value.membershipStatus === "Platinum" || customerData.value.membershipStatus === "Gold";
};

// Helper function to check if booking is for bridal package
const hasbridalPackageSelected = () => {
  return bookingForm.value.serviceIds.some(serviceId => {
    const service = customerData.value.availableServices.find(s => s.id === parseInt(serviceId));
    return service && service.name === "Bridal Package";
  });
};

// Compute minimum booking date based on service type and customer type
// Compute minimum booking date based on service type
const minBookingDate = computed(() => {
  const today = new Date();
  const minDate = new Date(today);
  
  if (hasbridalPackageSelected()) {
    minDate.setMonth(minDate.getMonth() + 1); // 1 month for bridal package
  } else {
    minDate.setDate(minDate.getDate()); // Allow booking today for normal services
  }
  
  return minDate.toISOString().split('T')[0];
});

// Compute maximum booking date (6 months for bridal, VIP=5days/Regular=2days for others)
const maxBookingDate = computed(() => {
  const today = new Date();
  const maxDate = new Date(today);
  
  if (hasbridalPackageSelected()) {
    maxDate.setMonth(maxDate.getMonth() + 6); // 6 months for bridal package
  } else {
    const daysToAdd = isVIPCustomer() ? 5 : 2; // VIP=5 days, Regular=2 days for other services
    maxDate.setDate(maxDate.getDate() + daysToAdd);
  }
  
  return maxDate.toISOString().split('T')[0];
});

// Helper text for booking date info
const bookingDateInfo = computed(() => {
  if (bookingForm.value.serviceIds.length === 0) {
    return "Select a service to see available booking dates";
  }
  
  if (hasbridalPackageSelected()) {
    return `Bridal Package: Book 1 to 6 months in advance`;
  } else {
    const daysWindow = isVIPCustomer() ? 5 : 2;
    return `Other services: Book from tomorrow onwards for ${daysWindow} days`;
  }
});

const pageTitle = computed(() => {
  const titles = {
    dashboard: "Customer Dashboard",
    "book-appointment": "Book Appointment",
    appointments: "My Appointments",
    feedback: "Feedback & Reviews",
    services: "Browse Services",
    profile: "My Profile"
  };
  return titles[currentView.value] || "Customer Dashboard";
});

// Filtered appointment history (limited to 3 months)
const filteredAppointmentHistory = computed(() => {
  const threeMonthsAgo = new Date();
  threeMonthsAgo.setMonth(threeMonthsAgo.getMonth() - 3);
  const threeMonthsAgoStr = threeMonthsAgo.toISOString().split('T')[0];
  
  let filtered = customerData.appointmentHistory.filter(appt => appt.date >= threeMonthsAgoStr);
  
  if (!appointmentHistoryFilter.value.trim()) return filtered;
  return filtered.filter(appt =>
    appt.service.toLowerCase().includes(appointmentHistoryFilter.value.toLowerCase()) ||
    appt.staff.toLowerCase().includes(appointmentHistoryFilter.value.toLowerCase())
  );
});

// Filtered history appointments from API
const filteredHistoryAppointments = computed(() => {
  if (!appointmentHistoryFilter.value.trim()) return historyAppointmentsData.value;
  return historyAppointmentsData.value.filter(appt =>
    appt.service.toLowerCase().includes(appointmentHistoryFilter.value.toLowerCase()) ||
    appt.staff.toLowerCase().includes(appointmentHistoryFilter.value.toLowerCase())
  );
});

// Service categories
const serviceCategories = computed(() => {
  const categories = [...new Set(availableServicesData.value.map(s => s.category))];
  return categories.sort();
});

// Filtered services by category
const filteredServices = computed(() => {
  if (!selectedServiceCategory.value) return availableServicesData.value;
  return availableServicesData.value.filter(s => s.category === selectedServiceCategory.value);
});

// Get services by category
const getServicesByCategory = (category) => {
  return availableServicesData.value.filter(s => s.category === category);
};

const getStatusBadgeClass = (status) => {
  const badges = {
    completed: "badge-green",
    scheduled: "badge-blue",
    confirmed: "badge-gold",
    pending: "badge-gray",
    cancelled: "badge-red",
  };
  return badges[status] || "badge-gray";
};

// Fetch appointment details from backend
const viewAppointmentDetails = async (appointmentId) => {
  selectedAppointment.value = null;
  showAppointmentDetailsModal.value = true;
  loadingAppointmentDetails.value = true;

  try {
    // Check if appointment exists in history data first
    let appointment = historyAppointmentsData.value.find(a => a.id === appointmentId);
    
    if (appointment) {
      selectedAppointment.value = {
        ...appointment,
        service: appointment.service || appointment.service_name,
        staff: appointment.staff || appointment.staff_name,
        duration: 60 // This would come from backend
      };
    } else {
      selectedAppointment.value = null;
    }
  } catch (error) {
    console.error('Error fetching appointment details:', error);
    alert('Failed to load appointment details');
  } finally {
    loadingAppointmentDetails.value = false;
  }
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

const openProfileEdit = () => {
  profileForm.value = {
    name: customerData.name,
    email: customerData.email,
    phone: customerData.phone,
    preferredServices: [...preferredServiceIds.value]
  };
  showProfileEditModal.value = true;
};

const handleUpdateProfile = () => {
  customerData.name = profileForm.value.name.trim() || customerData.name;
  customerData.email = profileForm.value.email.trim() || customerData.email;
  customerData.phone = profileForm.value.phone.trim() || customerData.phone;
  const normalizedPreferred = profileForm.value.preferredServices.map((id) => Number(id));
  preferredServiceIds.value = [...normalizedPreferred];
  customerData.preferredServices = [...normalizedPreferred];
  showProfileEditModal.value = false;
};

const handleLogout = () => {
  appStore.logout();
  router.push("/login/customer");
};

const startBookingFromService = (serviceId) => {
  bookingForm.value.serviceIds = [serviceId.toString()];
  currentView.value = 'book-appointment';
};

const handleSubmitFeedback = () => {
  feedbackError.value = "";
  feedbackSuccess.value = "";

  if (!feedbackForm.value.appointmentId) {
    feedbackError.value = "Please select an appointment";
    return;
  }

  if (!feedbackForm.value.rating) {
    feedbackError.value = "Please provide a rating";
    return;
  }

  const appointment = customerData.appointmentHistory.find(a => a.id === parseInt(feedbackForm.value.appointmentId));

  const newFeedback = {
    id: Math.max(...customerData.feedback.map(f => f.id || 0), 0) + 1,
    service: appointment.service,
    staff: appointment.staff,
    date: new Date().toISOString().split('T')[0],
    rating: feedbackForm.value.rating,
    comment: feedbackForm.value.comment || "No comment"
  };

  customerData.feedback.push(newFeedback);
  feedbackSuccess.value = "Thank you for your feedback!";

  setTimeout(() => {
    feedbackForm.value = {
      appointmentId: "",
      rating: 0,
      comment: ""
    };
    feedbackSuccess.value = "";
  }, 1500);
};

const chatLoading = ref(false);

const sendChatMessage = async () => {
  if (!chatInput.value.trim() || chatLoading.value) return;

  const userText = chatInput.value.trim();
  chatInput.value = "";

  chatMessages.value.push({ type: "user", text: userText, time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) });
  chatLoading.value = true;
  // Typing indicator
  chatMessages.value.push({ type: "bot", text: "...", time: "", isTyping: true });

  const token = localStorage.getItem("authToken");
  try {
    const res = await fetch(`${API_BASE_URL}/ai/customer-chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token,
      },
      body: JSON.stringify({ message: userText }),
    });
    const data = await res.json();
    // Remove typing indicator
    chatMessages.value = chatMessages.value.filter(m => !m.isTyping);
    chatMessages.value.push({
      type: "bot",
      text: data.response || "Sorry, I couldn't process that. Please try again.",
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    });
  } catch {
    chatMessages.value = chatMessages.value.filter(m => !m.isTyping);
    chatMessages.value.push({
      type: "bot",
      text: "I'm having trouble connecting right now. Please try again shortly.",
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    });
  } finally {
    chatLoading.value = false;
  }
};

const logout = () => {
  // Add logout logic here
  console.log("Logout");
};

const getReviewForBooking = (appointmentId) => {
  return customerData.feedback.find(f => {
    const appt = customerData.appointmentHistory.find(a => a.id === appointmentId);
    return f.service === appt?.service && f.staff === appt?.staff;
  });
};

// Fetch upcoming appointments from API
const fetchUpcomingAppointments = async () => {
  const token = localStorage.getItem("authToken");
  
  // Don't attempt to fetch if token is missing
  if (!token) {
    console.warn("No authentication token found");
    return;
  }
  
  loadingUpcomingAppointments.value = true;
  upcomingAppointmentsError.value = "";
  
  try {
    const data = await apiClient.get("/api/customer-upcoming-appointments");
    console.log("Raw customer upcoming appointments:", data);
    // Transform API data to match frontend format
    upcomingAppointmentsData.value = data.map(appt => ({
      id: appt.appointment_id,
      service_name: appt.service_name || appt.service_desc || "Service",
      staff_name: appt.staff_name,
      datetime: appt.datetime,
      price: appt.price,
      status: appt.status,
      // Extract date and time from ISO datetime
      date: appt.datetime ? appt.datetime.split('T')[0] : '',
      time: appt.datetime ? appt.datetime.split('T')[1]?.substring(0, 5) : ''
    }));
    console.log("Mapped upcoming appointments:", upcomingAppointmentsData.value);
  } catch (error) {
    console.error("Error fetching upcoming appointments:", error);
    upcomingAppointmentsError.value = "Failed to load upcoming appointments";
  } finally {
    loadingUpcomingAppointments.value = false;
  }
};

// Fetch past appointments from API
const fetchHistoryAppointments = async () => {
  const token = localStorage.getItem("authToken");
  
  if (!token) {
    console.warn("No authentication token found");
    return;
  }
  
  loadingHistoryAppointments.value = true;
  historyAppointmentsError.value = "";
  
  try {
    const data = await apiClient.get("/api/customer-history-appointments");
    console.log("Raw customer history appointments:", data);
    // Transform API data to match frontend format
    historyAppointmentsData.value = data.map(appt => ({
      id: appt.appointment_id,
      service: appt.service_name || appt.service_desc || "Service",
      staff: appt.staff_name,
      datetime: appt.datetime,
      price: appt.price,
      status: appt.status,
      rating: appt.rating || 0,
      date: appt.datetime ? appt.datetime.split('T')[0] : '',
      time: appt.datetime ? appt.datetime.split('T')[1]?.substring(0, 5) : ''
    }));
    console.log("Mapped history appointments:", historyAppointmentsData.value);
  } catch (error) {
    console.error("Error fetching history appointments:", error);
    historyAppointmentsError.value = "Failed to load appointment history";
  } finally {
    loadingHistoryAppointments.value = false;
  }
};

// Fetch appointments on component mount
// Fetch services from backend
const fetchServices = async () => {
  loadingServices.value = true;
  servicesError.value = "";
  
  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      servicesError.value = "Please log in to view services";
      availableServicesData.value = [];
      loadingServices.value = false;
      return;
    }
    
    const response = await apiClient.get("/api/service");
    
    if (!response || response.length === 0) {
      servicesError.value = "No services available at the moment. Please check back later.";
      availableServicesData.value = [];
    } else {
      // Transform backend data to match frontend structure
      availableServicesData.value = response.map(service => ({
        id: service.service_id,
        name: service.service_desc,
        category: service.service_category,
        price: service.service_price,
        duration: service.service_duration,
        description: service.service_desc
      }));
      servicesError.value = "";
    }
  } catch (error) {
    console.error("Error fetching services:", error);
    servicesError.value = `Failed to load services: ${error.message || "Unknown error"}`;
    availableServicesData.value = [];
  } finally {
    loadingServices.value = false;
  }
};

// Fetch customer summary data
const fetchCustomerSummary = async () => {
  const token = localStorage.getItem("authToken");
  
  if (!token) {
    console.warn("No authentication token found");
    return;
  }
  
  loadingSummary.value = true;
  
  try {
    const data = await apiClient.get("/api/customer-summary");
    summaryData.value = data;
    console.log("Customer summary data:", data);
  } catch (error) {
    console.error("Error fetching customer summary:", error);
  } finally {
    loadingSummary.value = false;
  }
};

// Fetch pending reviews (appointments that need feedback)
const fetchPendingReviews = async () => {
  const token = localStorage.getItem("authToken");
  
  if (!token) {
    console.warn("No authentication token found");
    return;
  }
  
  loadingPendingReviews.value = true;
  pendingReviewsError.value = "";
  
  try {
    const data = await apiClient.get("/api/customer-review");
    pendingReviews.value = data;
    console.log("Pending reviews:", data);
  } catch (error) {
    console.error("Error fetching pending reviews:", error);
    pendingReviewsError.value = "Failed to load pending reviews";
  } finally {
    loadingPendingReviews.value = false;
  }
};

// Fetch reviewed appointments
const fetchReviewedAppointments = async () => {
  const token = localStorage.getItem("authToken");
  
  if (!token) {
    console.warn("No authentication token found");
    return;
  }
  
  loadingReviewedAppointments.value = true;
  reviewedAppointmentsError.value = "";
  
  try {
    const data = await apiClient.get("/api/customer-reviewed-appointments");
    reviewedAppointments.value = data;
    console.log("Reviewed appointments:", data);
  } catch (error) {
    console.error("Error fetching reviewed appointments:", error);
    reviewedAppointmentsError.value = "Failed to load reviewed appointments";
  } finally {
    loadingReviewedAppointments.value = false;
  }
};

// Submit review/rating for an appointment
const submitReview = async () => {
  if (!selectedPendingReview.value) {
    reviewSubmitError.value = "Please select an appointment";
    return;
  }

  if (reviewFormData.value.rating === 0) {
    reviewSubmitError.value = "Please provide a rating";
    return;
  }

  reviewSubmitError.value = "";
  reviewSubmitSuccess.value = "";

  try {
    const payload = {
      appointment_id: selectedPendingReview.value.appointment_id,
      rating: reviewFormData.value.rating,
      review: reviewFormData.value.review || ""
    };

    await apiClient.post("/api/customer-reviewed-appointments", payload);

    reviewSubmitSuccess.value = "Review submitted successfully!";
    
    // Reset form
    reviewFormData.value = {
      rating: 0,
      review: ""
    };
    selectedPendingReview.value = null;
    showReviewModal.value = false;

    // Refresh pending and reviewed appointments
    setTimeout(() => {
      fetchPendingReviews();
      fetchReviewedAppointments();
    }, 1500);
  } catch (error) {
    console.error("Error submitting review:", error);
    reviewSubmitError.value = error.message || "Failed to submit review";
  }
};

// Open review modal for a pending appointment
const openReviewModal = (pendingReview) => {
  selectedPendingReview.value = pendingReview;
  reviewFormData.value = { rating: 0, review: "" };
  reviewSubmitError.value = "";
  reviewSubmitSuccess.value = "";
  aiFeedbackKeywords.value = [];
  aiFeedbackNote.value = "";
  aiFeedbackLoading.value = false;
  showAiFeedbackPanel.value = false;
  showReviewModal.value = true;
};

// ── AI Feedback Writer state ────────────────────────────────────────────────
const FEEDBACK_KEYWORDS = [
  "Service Quality", "Staff Behaviour", "Waiting Time",
  "Cleanliness", "Pricing", "Overall Experience", "Product Quality", "Ambience",
];
const showAiFeedbackPanel = ref(false);
const aiFeedbackKeywords  = ref([]);
const aiFeedbackNote      = ref("");
const aiFeedbackLoading   = ref(false);
const aiFeedbackError     = ref("");

const toggleFeedbackKeyword = (kw) => {
  const idx = aiFeedbackKeywords.value.indexOf(kw);
  if (idx === -1) aiFeedbackKeywords.value.push(kw);
  else aiFeedbackKeywords.value.splice(idx, 1);
};

const generateAiFeedback = async () => {
  if (!aiFeedbackKeywords.value.length && !aiFeedbackNote.value.trim()) {
    aiFeedbackError.value = "Select at least one keyword or add a note.";
    return;
  }
  aiFeedbackError.value = "";
  aiFeedbackLoading.value = true;
  const token = localStorage.getItem("authToken");
  try {
    const body = {
      keywords: aiFeedbackKeywords.value,
      customer_note: aiFeedbackNote.value.trim(),
      service_name: selectedPendingReview.value?.services?.join(', ') || '',
      staff_name: selectedPendingReview.value?.staff_name || '',
    };
    const res = await fetch(`${API_BASE_URL}/ai/generate-feedback`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Authentication-Token": token,
      },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    if (data.feedback_message) {
      reviewFormData.value.review = data.feedback_message;
      showAiFeedbackPanel.value = false;
    } else {
      aiFeedbackError.value = data.message || "AI generation failed.";
    }
  } catch {
    aiFeedbackError.value = "Connection error. Please try again.";
  } finally {
    aiFeedbackLoading.value = false;
  }
};

onMounted(() => {
  fetchServices();
  fetchUpcomingAppointments();
  fetchHistoryAppointments();
  fetchCustomerSummary();
  fetchPendingReviews();
  fetchReviewedAppointments();
  fetchAvailableStaff();
});

// Book appointment API using apiClient
const handleBookAppointment = async () => {
  bookingError.value = "";
  bookingSuccess.value = "";

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

  try {
    // Combine date and time into ISO datetime string
    const dateTime = `${bookingForm.value.date}T${bookingForm.value.time}:00`;
    
    const payload = {
      service_ids: bookingForm.value.serviceIds.map(id => parseInt(id)),
      appointment_datetime: dateTime
    };
    
    if (bookingForm.value.staffId) {
      payload.staff_id = parseInt(bookingForm.value.staffId);
    }
    
    const response = await apiClient.post("/api/customer-upcoming-appointments", payload);
    
    bookingSuccess.value = "Appointment booked successfully!";
    
    // Reset form and refresh appointments
    bookingForm.value = {
      serviceIds: [],
      staffId: "",
      date: "",
      time: ""
    };
    
    // Refresh upcoming appointments
    setTimeout(() => {
      fetchUpcomingAppointments();
      fetchAvailableStaff();
      currentView.value = "appointments";
      appointmentsTab.value = "upcoming";
    }, 1500);
  } catch (error) {
    console.error("Error booking appointment:", error);
    bookingError.value = error.message || "Failed to book appointment";
  }
};

// Edit appointment
const startEditAppointment = (appt) => {
  editingAppointmentId.value = appt.id;
  editAppointmentForm.value = {
    staffId: appt.staff_id || "",
    serviceIds: appt.service_ids || [],
    datetime: appt.datetime || `${appt.date}T${appt.time}:00`
  };
  showAppointmentDetailsModal.value = true;
};

// Update appointment handler
const handleEditAppointmentSubmit = async () => {
  if (!editingAppointmentId.value) return;
  
  try {
    const dateTime = editAppointmentForm.value.datetime;
    
    const payload = {};
    if (editAppointmentForm.value.staffId) {
      payload.staff_id = parseInt(editAppointmentForm.value.staffId);
    }
    if (editAppointmentForm.value.serviceIds.length > 0) {
      payload.service_ids = editAppointmentForm.value.serviceIds.map(id => parseInt(id));
    }
    if (editAppointmentForm.value.datetime) {
      payload.appointment_datetime = dateTime;
    }
    
    const response = await apiClient.put(`/api/customer-upcoming-appointments/${editingAppointmentId.value}`, payload);
    
    // Refresh appointments
    await fetchUpcomingAppointments();
    selectedAppointment.value = null;
    editingAppointmentId.value = null;
    showAppointmentDetailsModal.value = false;
    
    alert("Appointment updated successfully!");
  } catch (error) {
    console.error("Error editing appointment:", error);
    alert("Failed to edit appointment: " + error.message);
  }
};

// Cancel appointment
const handleCancelAppointment = async (appointmentId) => {
  if (!confirm("Are you sure you want to cancel this appointment?")) return;
  
  try {
    const response = await apiClient.delete(`/api/customer-upcoming-appointments/${appointmentId}`);
    
    // Refresh appointments
    await fetchUpcomingAppointments();
    
    alert("Appointment cancelled successfully!");
  } catch (error) {
    console.error("Error canceling appointment:", error);
    alert("Failed to cancel appointment: " + error.message);
  }
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

/* Detail Item Styles */
.detail-item {
  padding: 12px;
  background: var(--light-bg);
  border-radius: var(--radius);
}

.detail-label {
  display: block;
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-weight: 600;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 1rem;
  color: var(--text);
  font-weight: 500;
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
