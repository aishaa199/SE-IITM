<template>
  <div class="content-layout">
    <!-- Sidebar -->
    <div class="sidebar">
      <div class="sidebar-logo">
        <div class="sidebar-logo-text">Glow Suite</div>
        <div class="sidebar-logo-sub">Customer Portal</div>
      </div>
      <nav class="sidebar-nav">
        <div class="nav-section">Bookings</div>
        <div
          :class="['nav-item', { active: currentView === 'dashboard' }]"
          @click="currentView = 'dashboard'"
        >
          <span class="nav-icon">📊</span> Dashboard
        </div>
        <div
          :class="['nav-item', { active: currentView === 'book-appointment' }]"
          @click="currentView = 'book-appointment'"
        >
          <span class="nav-icon">📅</span> Book Appointment
        </div>
        <div
          :class="['nav-item', { active: currentView === 'appointments' }]"
          @click="currentView = 'appointments'"
        >
          <span class="nav-icon">📋</span> My Appointments
        </div>
        <div
          :class="['nav-item', { active: currentView === 'feedback' }]"
          @click="currentView = 'feedback'"
        >
          <span class="nav-icon">💬</span> Feedback & Reviews
        </div>
        <div
          :class="['nav-item', { active: currentView === 'services' }]"
          @click="currentView = 'services'"
        >
          <span class="nav-icon">💇</span> Browse Services
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
          <div class="sidebar-avatar">{{ customerData.name[0] }}</div>
          <div>
            <div class="sidebar-username">{{ customerData.name }}</div>
            <div class="sidebar-role">{{ customerData.membershipStatus }}</div>
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
                  <button class="btn btn-sm btn-outline w-full">
                    Reschedule
                  </button>
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
                <div class="grid-2">
                  <div class="form-group">
                    <label for="service">Select Service *</label>
                    <select 
                      id="service"
                      v-model="bookingForm.serviceId" 
                      class="form-input"
                      required
                    >
                      <option value="">Choose a service</option>
                      <option v-for="service in customerData.availableServices" :key="service.id" :value="service.id">
                        {{ service.name }} - ₹{{ service.price }} ({{ service.duration }} min)
                      </option>
                    </select>
                  </div>

                  <div class="form-group">
                    <label for="stylist">Select Stylist *</label>
                    <select 
                      id="stylist"
                      v-model="bookingForm.staffId" 
                      class="form-input"
                      required
                    >
                      <option value="">Choose a stylist</option>
                      <option v-for="staff in availableStylists" :key="staff.id" :value="staff.id">
                        {{ staff.name }} - ⭐ {{ staff.rating }}
                      </option>
                    </select>
                  </div>

                  <div class="form-group">
                    <label for="date">Select Date *</label>
                    <input 
                      id="date"
                      v-model="bookingForm.date" 
                      type="date" 
                      class="form-input"
                      :min="getTodayDate"
                      required
                    />
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

                <button type="submit" class="btn btn-primary" style="margin-top: 20px">
                  Confirm Booking
                </button>
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
                    <tr v-for="appt in customerData.appointmentHistory" :key="appt.id">
                      <td>{{ appt.service }}</td>
                      <td>{{ appt.staff }}</td>
                      <td>{{ appt.date }}</td>
                      <td>₹{{ appt.price }}</td>
                      <td>
                        <span :class="['badge', getStatusBadgeClass(appt.status)]">{{ appt.status }}</span>
                      </td>
                      <td>{{ appt.rating }} ⭐</td>
                    </tr>
                  </tbody>
                </table>
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
              <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px">
                <div v-for="service in customerData.availableServices" :key="service.id" class="service-card" style="border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 16px">
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
                  <button class="btn btn-primary w-full">Book Now</button>
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
                  <input type="text" :value="customerData.name" class="form-input" disabled />
                </div>
                <div class="form-group">
                  <label>Email</label>
                  <input type="email" :value="customerData.email" class="form-input" disabled />
                </div>
                <div class="form-group">
                  <label>Phone</label>
                  <input type="tel" :value="customerData.phone" class="form-input" disabled />
                </div>
                <div class="form-group">
                  <label>Member Since</label>
                  <input type="text" :value="customerData.memberSince" class="form-input" disabled />
                </div>
                <div class="form-group">
                  <label>Membership Status</label>
                  <input type="text" :value="customerData.membershipStatus" class="form-input" disabled />
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
</template>

<script setup>
import { ref, computed } from "vue";

const currentView = ref("dashboard");
const showChangePasswordModal = ref(false);
const passwordForm = ref({
  currentPassword: "",
  newPassword: "",
  confirmPassword: ""
});
const passwordError = ref("");
const passwordSuccess = ref("");

// Booking form state
const bookingForm = ref({
  serviceId: "",
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

// Mock data
const customerData = {
  name: "John Anderson",
  email: "john@example.com",
  phone: "+233 123 456 789",
  memberSince: "2024-01-15",
  membershipStatus: "Gold",
  totalSpent: 1250,
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

// Available stylists
const availableStylists = ref([
  { id: 1, name: "Sarah Johnson", rating: 4.8 },
  { id: 2, name: "Emma Davis", rating: 4.6 },
  { id: 3, name: "Lisa Chen", rating: 4.9 },
  { id: 4, name: "Priya Nair", rating: 4.7 },
  { id: 5, name: "Amara Osei", rating: 4.8 },
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

// Get today's date for min date validation
const getTodayDate = computed(() => {
  const today = new Date();
  return today.toISOString().split('T')[0];
});

const pageTitle = computed(() => {
  const titles = {
    dashboard: "Customer Dashboard",
    "book-appointment": "Book Appointment",
    appointments: "My Appointments",
    feedback: "Feedback & Reviews",
    services: "Browse Services",
    profile: "My Profile",
  };
  return titles[currentView.value] || "Customer Dashboard";
});

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

const handleBookAppointment = () => {
  bookingError.value = "";
  bookingSuccess.value = "";

  if (!bookingForm.value.serviceId) {
    bookingError.value = "Please select a service";
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

  // Find service and staff names
  const service = customerData.availableServices.find(s => s.id === parseInt(bookingForm.value.serviceId));
  const staff = availableStylists.value.find(s => s.id === parseInt(bookingForm.value.staffId));

  // Create new appointment
  const newAppointment = {
    id: Math.max(...customerData.upcomingAppointments.map(a => a.id || 0), 0) + 1,
    service: service.name,
    staff: staff.name,
    date: bookingForm.value.date,
    time: bookingForm.value.time,
    price: `₹ ${service.price}`,
    status: "confirmed"
  };

  customerData.upcomingAppointments.push(newAppointment);
  bookingSuccess.value = `Appointment booked successfully with ${staff.name} on ${bookingForm.value.date} at ${bookingForm.value.time}!`;

  setTimeout(() => {
    bookingForm.value = {
      serviceId: "",
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
