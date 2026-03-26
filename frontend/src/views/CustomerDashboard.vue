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
          @click="currentView = 'dashboard'; sidebarOpen = false"
        >
          <span class="nav-icon">📊</span> Dashboard
        </div>
        <div
          :class="['nav-item', { active: currentView === 'book-appointment' }]"
          @click="currentView = 'book-appointment'; sidebarOpen = false"
        >
          <span class="nav-icon">📅</span> Book Appointment
        </div>
        <div
          :class="['nav-item', { active: currentView === 'appointments' }]"
          @click="currentView = 'appointments'; sidebarOpen = false"
        >
          <span class="nav-icon">📋</span> My Appointments
        </div>
        <div
          :class="['nav-item', { active: currentView === 'feedback' }]"
          @click="currentView = 'feedback'; sidebarOpen = false"
        >
          <span class="nav-icon">💬</span> Feedback & Reviews
        </div>
        <div
          :class="['nav-item', { active: currentView === 'services' }]"
          @click="currentView = 'services'; sidebarOpen = false"
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
              <div class="stat-value">{{ customerData.todayStats.upcomingAppointments }}</div>
              <div class="stat-label">Upcoming Appointments</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">✅</div>
              <div class="stat-value">{{ customerData.todayStats.totalAppointments }}</div>
              <div class="stat-label">Total Appointments</div>
            </div>

            <div class="stat-card">
              <div class="stat-icon">⭐</div>
              <div class="stat-value">{{ customerData.membershipStatus }}</div>
              <div class="stat-label">Membership Status</div>
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
                <div v-if="customerData.upcomingAppointments.length === 0" class="empty-state">
                  <div class="empty-state-icon">📅</div>
                  <div class="empty-state-text">No upcoming appointments</div>
                  <button class="btn btn-primary" style="margin-top: 12px" @click="currentView = 'book-appointment'">Book Now</button>
                </div>
                <div v-for="appt in customerData.upcomingAppointments" :key="appt.id" class="booking-item">
                  <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px">
                    <div>
                      <div style="font-weight: 600">{{ appt.service }}</div>
                      <div class="text-muted">with {{ appt.staff }}</div>
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
              <div class="card-header">
                <h3 class="card-title">🤖 AI Beauty Assistant</h3>
              </div>
              <div class="card-body" style="display: flex; flex-direction: column; height: 450px">
                <div class="chat-messages" style="flex: 1; overflow-y: auto; margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid var(--border)">
                  <div v-for="(msg, idx) in chatMessages" :key="idx" :class="['chat-message', msg.type]" style="margin-bottom: 12px">
                    <div :style="msg.type === 'user' ? { textAlign: 'right', paddingLeft: '40px' } : { textAlign: 'left', paddingRight: '40px' }">
                      <div :style="msg.type === 'user' ? { background: 'var(--gold)', color: 'white' } : { background: 'var(--light-bg)', color: 'var(--charcoal)' }" style="padding: 8px 12px; border-radius: 8px; display: inline-block; max-width: 250px; word-wrap: break-word; text-align: left">
                        {{ msg.text }}
                      </div>
                      <div class="text-muted" style="font-size: 11px; margin-top: 4px">{{ msg.time }}</div>
                    </div>
                  </div>
                </div>
                <div style="display: flex; gap: 8px">
                  <input 
                    v-model="chatInput" 
                    type="text" 
                    placeholder="Ask me about services..." 
                    class="form-input"
                    style="flex: 1"
                    @keyup.enter="sendChatMessage"
                  />
                  <button class="btn btn-primary" style="padding: 10px 16px" @click="sendChatMessage">Send</button>
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
                        {{ staff.name }} - ⭐ {{ staff.rating }} - {{ staff.skills }}
                      </option>
                    </select>
                    <div v-if="bookingForm.staffId" class="text-muted" style="font-size: 12px; margin-top: 6px">
                      Selected: {{ availableStylists.find(s => s.id == bookingForm.staffId)?.name }} (⭐ {{ availableStylists.find(s => s.id == bookingForm.staffId)?.rating }}) - Specializes in {{ availableStylists.find(s => s.id == bookingForm.staffId)?.skills }}
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
              <h3 class="card-title">Appointment History</h3>
            </div>
            <div class="card-body">
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
                    <tr v-for="appt in filteredAppointmentHistory" :key="appt.id" @click="viewAppointmentDetails(appt.id)" style="cursor: pointer; transition: background-color 0.2s;" @mouseenter="($event.target.parentNode.style.backgroundColor = 'var(--light-bg)')" @mouseleave="($event.target.parentNode.style.backgroundColor = 'transparent')">
                      <td>{{ appt.service }}</td>
                      <td>{{ appt.staff }}</td>
                      <td>{{ appt.date }}</td>
                      <td>₹{{ appt.price }}</td>
                      <td>
                        <span :class="['badge', getStatusBadgeClass(appt.status)]">{{ appt.status }}</span>
                      </td>
                      <td>
                        <div style="display: flex; align-items: center; gap: 6px">
                          <span style="letter-spacing: 1px">
                            <span v-for="i in 5" :key="i" :style="{ color: i <= appt.rating ? 'var(--gold)' : 'var(--border)', fontSize: '12px' }">⭐</span>
                          </span>
                          <span style="font-size: 12px; font-weight: 600; color: var(--gold)">{{ appt.rating }}</span>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- Ratings Details Section -->
              <div v-if="filteredAppointmentHistory.length > 0" style="margin-top: 24px; padding-top: 24px; border-top: 2px solid var(--border)">
                <h4 style="margin-bottom: 16px; font-weight: 600">📊 Your Service Ratings</h4>
                <div style="display: flex; flex-direction: column; gap: 12px">
                  <div v-for="appt in filteredAppointmentHistory" :key="appt.id" style="padding: 16px; background: var(--light-bg); border-radius: var(--radius); margin-bottom: 12px">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px">
                      <div>
                        <div style="font-weight: 600">{{ appt.service }}</div>
                        <div style="font-size: 12px; color: var(--text-muted)">with {{ appt.staff }} • {{ appt.date }}</div>
                      </div>
                      <div style="display: flex; align-items: center; gap: 6px; font-weight: 600">
                        <span style="letter-spacing: 1px">
                          <span v-for="i in 5" :key="i" :style="{ color: i <= appt.rating ? 'var(--gold)' : 'var(--border)' }">⭐</span>
                        </span>
                        <span style="color: var(--gold)">{{ appt.rating }}/5</span>
                      </div>
                    </div>
                    <div v-if="getReviewForBooking(appt.id)" style="font-size: 13px; color: var(--text); padding: 8px; background: var(--card-bg); border-left: 3px solid var(--gold); border-radius: 4px">
                      <div style="margin-bottom: 4px"><strong>Your Review:</strong></div>
                      "{{ getReviewForBooking(appt.id).comment }}"
                    </div>
                    <div v-else style="font-size: 12px; color: var(--text-muted); font-style: italic; padding: 8px">
                      No detailed review provided for this booking
                    </div>
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
              <!-- Category Tabs -->
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
                  <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px">
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
              <div v-if="customerData.feedback.length === 0" class="empty-state">
                <div class="empty-state-icon">💬</div>
                <div class="empty-state-text">No feedback yet. Book and complete a service to leave feedback!</div>
              </div>
              <div v-for="feedback in customerData.feedback" :key="feedback.id" style="margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid var(--border)">
                <div style="margin-bottom: 8px">
                  <div style="font-weight: 600">{{ feedback.service }}</div>
                  <div class="text-muted" style="font-size: 12px">with {{ feedback.staff }} • {{ feedback.date }}</div>
                </div>
                <div style="font-size: 16px; margin-bottom: 8px">{{ '⭐'.repeat(feedback.rating) }}</div>
                <div class="text-muted">{{ feedback.comment }}</div>
              </div>

              <div style="margin-top: 24px; padding-top: 24px; border-top: 2px solid var(--border)">
                <h4 style="margin-bottom: 16px">Leave Feedback on an Appointment</h4>
                <div class="form-group">
                  <label for="feedback-service">Select Appointment *</label>
                  <select 
                    id="feedback-service"
                    v-model="feedbackForm.appointmentId" 
                    class="form-input"
                  >
                    <option value="">Choose an appointment</option>
                    <option v-for="appt in customerData.appointmentHistory" :key="appt.id" :value="appt.id">
                      {{ appt.service }} with {{ appt.staff }} - {{ appt.date }}
                    </option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="feedback-rating">Rating *</label>
                  <div style="display: flex; gap: 8px; margin-top: 8px">
                    <button 
                      v-for="star in 5" 
                      :key="star"
                      type="button"
                      @click="feedbackForm.rating = star"
                      style="background: none; border: none; font-size: 32px; cursor: pointer; opacity: feedbackForm.rating >= star ? 1 : 0.3; transition: opacity 0.2s"
                    >
                      ⭐
                    </button>
                  </div>
                </div>

                <div class="form-group">
                  <label for="feedback-comment">Your Feedback</label>
                  <textarea 
                    id="feedback-comment"
                    v-model="feedbackForm.comment" 
                    placeholder="Share your experience..."
                    class="form-input"
                    style="resize: vertical; min-height: 100px"
                  ></textarea>
                </div>

                <div v-if="feedbackError" class="error-message">{{ feedbackError }}</div>
                <div v-if="feedbackSuccess" class="success-message">{{ feedbackSuccess }}</div>

                <button type="button" @click="handleSubmitFeedback" class="btn btn-primary" style="margin-top: 12px">
                  Submit Feedback
                </button>
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
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">
            <div class="detail-item">
              <label class="detail-label">Service</label>
              <div class="detail-value">{{ selectedAppointment.service }}</div>
            </div>
            <div class="detail-item">
              <label class="detail-label">Staff Member</label>
              <div class="detail-value">{{ selectedAppointment.staff }}</div>
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
          <div style="margin-top: 12px;">
            <label class="detail-label">Rating</label>
            <div style="display: flex; align-items: center; gap: 6px;">
              <span style="letter-spacing: 1px;">
                <span v-for="i in 5" :key="i" :style="{ color: i <= selectedAppointment.rating ? 'var(--gold)' : 'var(--border)', fontSize: '14px' }">⭐</span>
              </span>
              <span style="font-size: 14px; font-weight: 600; color: var(--gold);">{{ selectedAppointment.rating || 'Not rated' }}</span>
            </div>
          </div>
        </div>
      </div>
      <div style="display: flex; gap: 12px; margin-top: 20px;">
        <button type="button" class="btn btn-outline" @click="showAppointmentDetailsModal = false" style="flex: 1;">
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useAppStore } from "../stores/appStore";

const router = useRouter();
const appStore = useAppStore();
const API_BASE_URL = "http://localhost:5000";

const currentView = ref("dashboard");
const sidebarOpen = ref(false);
const showChangePasswordModal = ref(false);
const showProfileMenu = ref(false);
const showProfileEditModal = ref(false);
const showAppointmentDetailsModal = ref(false);
const selectedAppointment = ref(null);
const loadingAppointmentDetails = ref(false);
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

// Feedback form state
const feedbackForm = ref({
  appointmentId: "",
  rating: 0,
  comment: ""
});
const feedbackError = ref("");
const feedbackSuccess = ref("");

// Chat state
const chatInput = ref("");
const chatMessages = ref([
  { type: "bot", text: "Hi! I'm your beauty assistant. How can I help you today?", time: "Now" }
]);

// Filter state
const appointmentHistoryFilter = ref("");
const selectedServiceCategory = ref(null);

// Mock data
const customerData = {
  name: "John Anderson",
  email: "john@example.com",
  phone: "+233 123 456 789",
  address: "123 Main Street, Accra",
  dob: "1992-05-20",
  memberSince: "2024-01-15",
  membershipStatus: "Gold",
  totalSpent: 1250,
  preferredServices: [1, 4, 6], // IDs of preferred services
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
  availableServices: [
    {
      id: 1,
      name: "Hair Styling",
      category: "Hair",
      description: "Professional hair styling",
      price: 50,
      duration: 60,
    },
    {
      id: 2,
      name: "Manicure",
      category: "Nails",
      description: "Full manicure service",
      price: 30,
      duration: 45,
    },
    {
      id: 3,
      name: "Pedicure",
      category: "Nails",
      description: "Complete pedicure treatment",
      price: 35,
      duration: 45,
    },
    {
      id: 4,
      name: "Facial Treatment",
      category: "Skin Care",
      description: "Deep cleansing facial",
      price: 70,
      duration: 60,
    },
    {
      id: 5,
      name: "Massage Therapy",
      category: "Wellness",
      description: "Relaxing full body massage",
      price: 80,
      duration: 60,
    },
    {
      id: 6,
      name: "Spa Package",
      category: "Wellness",
      description: "Complete spa experience",
      price: 120,
      duration: 120,
    },
    {
      id: 7,
      name: "Bridal Package",
      category: "Special Events",
      description: "Complete bridal makeup and styling",
      price: 250,
      duration: 180,
    },
  ],
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

const preferredServiceIds = ref([...customerData.preferredServices]);

// Available stylists
const availableStylists = ref([
  { id: 1, name: "Sarah Johnson", rating: 4.8, skills: "Hair Styling, Coloring" },
  { id: 2, name: "Emma Davis", rating: 4.6, skills: "Manicure, Pedicure" },
  { id: 3, name: "Lisa Chen", rating: 4.9, skills: "Facial Treatment, Massage" },
  { id: 4, name: "Priya Nair", rating: 4.7, skills: "Hair Styling, Pedicure" },
  { id: 5, name: "Amara Osei", rating: 4.8, skills: "Spa Package, Massage Therapy" },
]);

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
  return customerData.availableServices.filter(service => 
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
  return customerData.membershipStatus === "Platinum" || customerData.membershipStatus === "Gold";
};

// Helper function to check if booking is for bridal package
const hasbridalPackageSelected = () => {
  return bookingForm.value.serviceIds.some(serviceId => {
    const service = customerData.availableServices.find(s => s.id === parseInt(serviceId));
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
    minDate.setDate(minDate.getDate() + 1); // Tomorrow for normal services
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

// Service categories
const serviceCategories = computed(() => {
  const categories = [...new Set(customerData.availableServices.map(s => s.category))];
  return categories.sort();
});

// Filtered services by category
const filteredServices = computed(() => {
  if (!selectedServiceCategory.value) return customerData.availableServices;
  return customerData.availableServices.filter(s => s.category === selectedServiceCategory.value);
});

// Get services by category
const getServicesByCategory = (category) => {
  return customerData.availableServices.filter(s => s.category === category);
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
    // Check if appointment exists in local data first
    const appointment = customerData.appointmentHistory.find(a => a.id === appointmentId);
    
    if (appointment) {
      // In a real scenario, you would fetch from backend like this:
      // const response = await fetch(`/api/appointments/${appointmentId}`);
      // const data = await response.json();
      // selectedAppointment.value = data;
      
      // For now, using the local data with additional enriched details
      selectedAppointment.value = {
        ...appointment,
        time: appointment.time || '10:00 AM',
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

const handleBookAppointment = () => {
  bookingError.value = "";
  bookingSuccess.value = "";

  if (bookingForm.value.serviceIds.length === 0) {
    bookingError.value = "Please select at least one service";
    return;
  }

  if (!bookingForm.value.staffId) {
    bookingError.value = "Please select a stylist";
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
    if (hasbridalPackageSelected()) {
      bookingError.value = `Bridal Package must be booked 1 to 6 months in advance`;
    } else {
      const daysWindow = isVIPCustomer() ? 5 : 2;
      bookingError.value = `Please select a date from tomorrow onwards for ${daysWindow} days`;
    }
    return;
  }

  // Find staff name
  const staff = availableStylists.value.find(s => s.id === parseInt(bookingForm.value.staffId));
  
  // Get service names and total price
  const services = bookingForm.value.serviceIds.map(serviceId => {
    const service = customerData.availableServices.find(s => s.id === parseInt(serviceId));
    return service;
  });
  
  const serviceNames = services.map(s => s.name).join(", ");
  const totalPrice = services.reduce((sum, s) => sum + s.price, 0);

  // Create new appointment
  const newAppointment = {
    id: Math.max(...customerData.upcomingAppointments.map(a => a.id || 0), 0) + 1,
    service: serviceNames,
    staff: staff.name,
    date: bookingForm.value.date,
    time: bookingForm.value.time,
    price: `₹ ${totalPrice}`,
    status: "confirmed"
  };

  customerData.upcomingAppointments.push(newAppointment);
  bookingSuccess.value = `Appointment booked successfully with ${staff.name} on ${bookingForm.value.date} at ${bookingForm.value.time}!`;

  setTimeout(() => {
    bookingForm.value = {
      serviceIds: [],
      staffId: "",
      date: "",
      time: ""
    };
    bookingSuccess.value = "";
    currentView.value = "dashboard";
  }, 2000);
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

const sendChatMessage = () => {
  if (!chatInput.value.trim()) return;

  // Add user message
  chatMessages.value.push({
    type: "user",
    text: chatInput.value,
    time: "Now"
  });

  const userMessage = chatInput.value.toLowerCase();
  chatInput.value = "";

  // Simulate AI response with RAG-like patterns
  setTimeout(() => {
    let response = "";

    if (userMessage.includes("price") || userMessage.includes("cost")) {
      response = "Our services range from ₹30 for manicures to ₹120 for spa packages. Would you like details on a specific service?";
    } else if (userMessage.includes("hair")) {
      response = "We offer hair styling (₹50) and balayage services (₹220). Both are 60-120 minutes. Would you like to book?";
    } else if (userMessage.includes("manicure") || userMessage.includes("nails")) {
      response = "We have manicure (₹30, 45 min) and pedicure (₹35, 45 min) services available. Our stylists are highly rated!";
    } else if (userMessage.includes("facial") || userMessage.includes("skin")) {
      response = "Our facial treatment is ₹70 for 60 minutes. It includes deep cleansing and rejuvenation. Book now?";
    } else if (userMessage.includes("available") || userMessage.includes("time") || userMessage.includes("appointment")) {
      response = "We're available from 9:00 AM to 5:00 PM daily. You can book an appointment with any of our stylists. Would you like to proceed?";
    } else if (userMessage.includes("stylist") || userMessage.includes("staff")) {
      response = "We have experienced stylists including Sarah Johnson (4.8⭐), Emma Davis (4.6⭐), and Lisa Chen (4.9⭐). All are highly skilled!";
    } else if (userMessage.includes("massage")) {
      response = "Our massage therapy costs ₹80 for 60 minutes. It's perfect for relaxation and wellness. Would you like to book?";
    } else {
      response = "I can help you with service information, pricing, booking appointments, or anything about our beauty salon. What would you like to know?";
    }

    chatMessages.value.push({
      type: "bot",
      text: response,
      time: "Now"
    });
  }, 500);
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
