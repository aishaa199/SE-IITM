<template>
  <div class="dashboard-container">
    <!-- Sidebar Navigation -->
    <div class="dashboard-sidebar">
      <div class="sidebar-header">
        <h2 style="color: var(--gold); font-size: 24px; margin: 0">⚙️ Manager Hub</h2>
        <p style="color: #999; margin: 8px 0 0 0; font-size: 12px">{{ managerData.name }}</p>
      </div>

      <div class="sidebar-menu">
        <div
          :class="['nav-item', { active: currentView === 'overview' }]"
          @click="currentView = 'overview'"
        >
          <span class="nav-icon">📊</span> Overview
        </div>

        <div
          :class="['nav-item', { active: currentView === 'bookings' }]"
          @click="currentView = 'bookings'"
        >
          <span class="nav-icon">📅</span> Manage Appointments
        </div>

        <div
          :class="['nav-item', { active: currentView === 'book-appointment' }]"
          @click="currentView = 'book-appointment'"
        >
          <span class="nav-icon">📝</span> Book Appointment
        </div>

        <div
          :class="['nav-item', { active: currentView === 'packages' }]"
          @click="currentView = 'packages'"
        >
          <span class="nav-icon">📦</span> Service Packages
        </div>

        <div
          :class="['nav-item', { active: currentView === 'customers' }]"
          @click="currentView = 'customers'"
        >
          <span class="nav-icon">👥</span> Customers
        </div>

        <div
          :class="['nav-item', { active: currentView === 'staff-schedule' }]"
          @click="currentView = 'staff-schedule'"
        >
          <span class="nav-icon">📅</span> Staff Schedule
        </div>

        <div
          :class="['nav-item', { active: currentView === 'services' }]"
          @click="currentView = 'services'"
        >
          <span class="nav-icon">✨</span> Create Services
        </div>

        <div
          :class="['nav-item', { active: currentView === 'profile' }]"
          @click="currentView = 'profile'"
        >
          <span class="nav-icon">👤</span> My Profile
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
              <div class="stat-icon">📅</div>
              <div class="stat-label">Total Appointments</div>
              <div class="stat-value">{{ bookings.length }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">👥</div>
              <div class="stat-label">Active Customers</div>
              <div class="stat-value">{{ activeCustomers }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">📦</div>
              <div class="stat-label">Service Packages</div>
              <div class="stat-value">{{ packages.length }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">✨</div>
              <div class="stat-label">Services Created</div>
              <div class="stat-value">{{ servicesCreated }}</div>
            </div>
          </div>
        </div>

        <!-- BOOKINGS VIEW -->
        <div v-if="currentView === 'bookings'" class="fade-in">
          <!-- Appointments List -->
          <div class="card" style="margin-bottom: 24px">
            <div class="card-header">
              <h3 class="card-title">📅 Customer Appointments</h3>
            </div>
            
            <div class="appointments-list">
              <div v-if="bookings.length === 0" class="empty-state" style="padding: 32px; text-align: center; color: var(--text-muted)">
                <div style="font-size: 24px; margin-bottom: 12px">📅</div>
                <div>No appointments scheduled yet</div>
              </div>
              <div v-for="booking in bookings" :key="booking.id" class="appointment-card">
                <div class="appointment-info">
                  <h4 style="margin: 0 0 8px 0">{{ booking.customerName }}</h4>
                  <p style="margin: 0 0 8px 0; color: #666; font-size: 14px">{{ formatDate(booking.datetime) }}</p>
                  <span class="badge" :class="`badge-${booking.status.toLowerCase()}`">{{ booking.status }}</span>
                </div>
                <div class="appointment-actions">
                  <button class="btn btn-sm btn-secondary" @click="editBooking(booking)">Edit</button>
                  <button class="btn btn-sm btn-danger" @click="deleteBooking(booking.id)">Delete</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Create New Appointment -->
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">📅 Create New Appointment</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleCreateAppointment" style="max-width: 800px">
                <div class="form-group">
                  <label>Select Services * (You can choose multiple)</label>
                  <div style="border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 12px; max-height: 300px; overflow-y: auto">
                    <div v-for="service in availableServices" :key="service.id" style="display: flex; align-items: center; margin-bottom: 12px">
                      <input 
                        :id="'service-' + service.id"
                        type="checkbox" 
                        :value="service.id" 
                        v-model="newBookingForm.serviceIds"
                        style="margin-right: 8px; width: 18px; height: 18px; cursor: pointer"
                      />
                      <label :for="'service-' + service.id" style="cursor: pointer; flex: 1; margin: 0">
                        {{ service.name }} - ₹{{ service.price }} ({{ service.duration }} min)
                      </label>
                    </div>
                  </div>
                  <div v-if="newBookingForm.serviceIds.length === 0" class="text-muted" style="margin-top: 8px; font-size: 12px">Please select at least one service</div>
                </div>

                <div class="grid-2" style="margin-top: 16px">
                  <div class="form-group">
                    <label for="customer">Select Customer *</label>
                    <select 
                      id="customer"
                      v-model="newBookingForm.customerId" 
                      class="form-input"
                      required
                    >
                      <option value="">Choose a customer</option>
                      <option v-for="customer in customers" :key="customer.id" :value="customer.id">
                        {{ customer.name }}
                      </option>
                    </select>
                  </div>

                  <div class="form-group">
                    <label for="stylist">Select Stylist (Optional)</label>
                    <select 
                      id="stylist"
                      v-model="newBookingForm.staffId" 
                      class="form-input"
                    >
                      <option value="">Choose a stylist (Optional)</option>
                      <option v-for="staff in availableStylists" :key="staff.id" :value="staff.id">
                        {{ staff.name }} - {{ staff.skills }}
                      </option>
                    </select>
                    <div v-if="newBookingForm.staffId" class="text-muted" style="font-size: 12px; margin-top: 6px">
                      Selected: {{ availableStylists.find(s => s.id == newBookingForm.staffId)?.name }} - Specializes in {{ availableStylists.find(s => s.id == newBookingForm.staffId)?.skills }}
                    </div>
                  </div>

                  <div class="form-group">
                    <label for="date">Select Date *</label>
                    <input 
                      id="date"
                      v-model="newBookingForm.date" 
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
                      v-model="newBookingForm.time" 
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
                    Confirm Booking ({{ newBookingForm.serviceIds.length }} service{{ newBookingForm.serviceIds.length !== 1 ? 's' : '' }})
                  </button>
                  <button type="button" class="btn btn-outline" @click="resetBookingForm">
                    Clear Form
                  </button>
                </div>
              </form>
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
                    <div v-for="service in availableServices" :key="service.id" style="display: flex; align-items: center; margin-bottom: 12px">
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
                    <label for="customer">Select Customer *</label>
                    <select 
                      id="customer"
                      v-model="bookingForm.customerId" 
                      class="form-input"
                      required
                    >
                      <option value="">Choose a customer</option>
                      <option v-for="customer in customers" :key="customer.id" :value="customer.id">
                        {{ customer.name }}
                      </option>
                    </select>
                  </div>

                  <div class="form-group">
                    <label for="stylist">Select Stylist (Optional)</label>
                    <select 
                      id="stylist"
                      v-model="bookingForm.staffId" 
                      class="form-input"
                    >
                      <option value="">Choose a stylist (Optional)</option>
                      <option v-for="staff in availableStylists" :key="staff.id" :value="staff.id">
                        {{ staff.name }} - {{ staff.skills }}
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

                <div style="display: flex; gap: 12px; margin-top: 20px">
                  <button type="submit" class="btn btn-primary">
                    Confirm Booking ({{ bookingForm.serviceIds.length }} service{{ bookingForm.serviceIds.length !== 1 ? 's' : '' }})
                  </button>
                  <button type="button" class="btn btn-outline" @click="currentView = 'bookings'">
                    Back to Appointments
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>

        <!-- PACKAGES VIEW -->
        <div v-if="currentView === 'packages'" class="fade-in">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">📦 Service Packages</h3>
              <button class="btn btn-primary" @click="showPackageModal = true">+ New Package</button>
            </div>

            <div class="packages-grid">
              <div v-for="pkg in packages" :key="pkg.id" class="package-card">
                <div class="package-header">
                  <h4>{{ pkg.name }}</h4>
                  <span v-if="pkg.exclusive" class="badge badge-exclusive">Exclusive</span>
                </div>
                <p class="package-desc">{{ pkg.description }}</p>
                <div class="services-list">
                  <small v-for="service in pkg.services" :key="service.id">
                    ✓ {{ service.name }}
                  </small>
                </div>
                <div class="package-actions">
                  <button class="btn btn-sm btn-secondary" @click="editPackage(pkg)">Edit</button>
                  <button class="btn btn-sm btn-danger" @click="deletePackage(pkg.id)">Delete</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- CUSTOMERS VIEW -->
        <div v-if="currentView === 'customers'" class="fade-in">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">👥 Customers</h3>
            </div>

            <div class="card-body">
              <div style="overflow-x: auto">
                <table style="width: 100%; border-collapse: collapse">
                  <thead>
                    <tr style="border-bottom: 2px solid var(--border)">
                      <th style="padding: 12px; text-align: left; font-weight: 600">Name</th>
                      <th style="padding: 12px; text-align: left; font-weight: 600">Email</th>
                      <th style="padding: 12px; text-align: left; font-weight: 600">Phone</th>
                      <th style="padding: 12px; text-align: left; font-weight: 600">Preferences</th>
                      <th style="padding: 12px; text-align: center; font-weight: 600">No. of Visits</th>
                      <th style="padding: 12px; text-align: center; font-weight: 600">Invoices</th>
                      <th style="padding: 12px; text-align: right; font-weight: 600">Total Spent (₹)</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="customer in customers" :key="customer.id" style="border-bottom: 1px solid var(--border); hover: background-color: #f9f9f9">
                      <td style="padding: 12px; font-weight: 500">{{ customer.name }}</td>
                      <td style="padding: 12px; color: #666; font-size: 14px">{{ customer.email }}</td>
                      <td style="padding: 12px">{{ customer.phone }}</td>
                      <td style="padding: 12px; color: #666; font-size: 13px; max-width: 200px">{{ customer.preferences }}</td>
                      <td style="padding: 12px; text-align: center; font-weight: 600">{{ customer.noOfVisits }}</td>
                      <td style="padding: 12px; text-align: center"><span class="badge badge-gold">{{ customer.invoices }}</span></td>
                      <td style="padding: 12px; text-align: right; font-weight: 600; color: var(--gold)">₹{{ customer.totalSpent }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- STAFF SCHEDULE VIEW -->
        <div v-if="currentView === 'staff-schedule'" class="fade-in">
          <div class="card" style="margin-bottom: 24px">
            <div class="card-header">
              <h3 class="card-title">📅 Staff Schedule</h3>
            </div>
            <div class="card-body">
              <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 20px">
                <label style="font-weight: 600">Select Date:</label>
                <input 
                  v-model="selectedStaffDate" 
                  type="date" 
                  class="form-input"
                  :min="getTodayDate"
                  style="max-width: 200px"
                />
              </div>

              <div v-if="staffForSelectedDay.length === 0" style="text-align: center; padding: 32px; color: var(--text-muted)">
                <div style="font-size: 24px; margin-bottom: 12px">📭</div>
                <div>No staff scheduled for {{ selectedStaffDate }}</div>
              </div>

              <div v-else style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px">
                <div v-for="staff in staffForSelectedDay" :key="staff.id" style="border: 1px solid var(--border); border-radius: 8px; padding: 16px; background: var(--light-bg)">
                  <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px">
                    <div style="width: 48px; height: 48px; background: linear-gradient(135deg, var(--gold), var(--charcoal)); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 20px; font-weight: 600">
                      {{ staff.name.charAt(0) }}
                    </div>
                    <div style="flex: 1">
                      <h4 style="margin: 0 0 4px 0; font-weight: 600">{{ staff.name }}</h4>
                      <div style="font-size: 12px; color: var(--text-muted)">{{ staff.role }}</div>
                    </div>
                  </div>

                  <div style="background: var(--bg); padding: 12px; border-radius: 6px; margin-bottom: 12px">
                    <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 6px">Skills</div>
                    <div style="font-size: 13px; font-weight: 500">{{ staff.skills }}</div>
                  </div>

                  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px">
                    <div style="background: var(--bg); padding: 8px; border-radius: 6px; text-align: center">
                      <div style="font-size: 11px; color: var(--text-muted)">Rating</div>
                      <div style="font-weight: 600; color: var(--gold)">⭐ {{ staff.rating }}</div>
                    </div>
                    <div style="background: var(--bg); padding: 8px; border-radius: 6px; text-align: center">
                      <div style="font-size: 11px; color: var(--text-muted)">Status</div>
                      <div style="font-weight: 600; color: #22c55e">✓ Active</div>
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
              <h3 class="card-title">✨ Create New Service</h3>
            </div>

            <form @submit.prevent="createService" class="form">
              <div class="form-group">
                <label>Service Name</label>
                <input v-model="serviceForm.name" type="text" required>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Category</label>
                  <select v-model="serviceForm.category" required>
                    <option value="">Select Category</option>
                    <option value="bridal">Bridal</option>
                    <option value="regular">Regular</option>
                    <option value="wellness">Wellness</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                <div class="form-group">
                  <label>Price (₹)</label>
                  <input v-model.number="serviceForm.price" type="number" required>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Duration (minutes)</label>
                  <input v-model.number="serviceForm.duration" type="number" required>
                </div>

                <div class="form-group">
                  <label>Reward Points Earned</label>
                  <input v-model.number="serviceForm.rewardPoints" type="number">
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>From Date</label>
                  <input v-model="serviceForm.fromDate" type="date">
                </div>

                <div class="form-group">
                  <label>To Date</label>
                  <input v-model="serviceForm.toDate" type="date">
                </div>
              </div>

              <div class="form-group">
                <label>
                  <input v-model="serviceForm.isAllergyFree" type="checkbox">
                  Allergy-Free Service
                </label>
              </div>

              <div class="form-group">
                <label>
                  <input v-model="serviceForm.isExclusive" type="checkbox">
                  Exclusive Package
                </label>
              </div>

              <div class="form-group">
                <label>Description</label>
                <textarea v-model="serviceForm.description"></textarea>
              </div>

              <button type="submit" class="btn btn-primary">Create Service</button>
            </form>
          </div>
        </div>

        <!-- PROFILE VIEW -->
        <div v-if="currentView === 'profile'" class="fade-in">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">👤 My Profile</h3>
              <button v-if="!editingProfile" class="btn btn-secondary" @click="editingProfile = true">
                Edit Profile
              </button>
            </div>

            <div v-if="!editingProfile" class="profile-info">
              <div class="info-row">
                <label>Name:</label>
                <span>{{ managerData.name }}</span>
              </div>
              <div class="info-row">
                <label>Email:</label>
                <span>{{ managerData.email }}</span>
              </div>
              <div class="info-row">
                <label>Contact:</label>
                <span>{{ managerData.contact }}</span>
              </div>
              <div class="info-row">
                <label>Address:</label>
                <span>{{ managerData.address }}</span>
              </div>
              <div class="info-row">
                <label>Date of Birth:</label>
                <span>{{ formatDate(managerData.dob) }}</span>
              </div>
              <div class="info-row">
                <label>Date of Joining:</label>
                <span>{{ formatDate(managerData.doj) }}</span>
              </div>
            </div>

            <div v-else class="profile-form">
              <form @submit.prevent="updateProfile">
                <div class="form-group">
                  <label>Name</label>
                  <input v-model="managerData.name" type="text">
                </div>
                <div class="form-group">
                  <label>Email</label>
                  <input v-model="managerData.email" type="email">
                </div>
                <div class="form-group">
                  <label>Contact</label>
                  <input v-model="managerData.contact" type="tel">
                </div>
                <button type="submit" class="btn btn-primary">Save Changes</button>
              </form>

              <hr style="margin: 24px 0">

              <div class="password-form">
                <h4>Change Password</h4>
                <form @submit.prevent="changePassword">
                  <div class="form-group">
                    <label>Current Password</label>
                    <input v-model="passwordForm.oldPassword" type="password" required>
                  </div>
                  <div class="form-group">
                    <label>New Password</label>
                    <input v-model="passwordForm.newPassword" type="password" required>
                  </div>
                  <div class="form-group">
                    <label>Confirm Password</label>
                    <input v-model="passwordForm.confirmPassword" type="password" required>
                  </div>
                  <button type="submit" class="btn btn-primary">Update Password</button>
                  <button type="button" class="btn btn-secondary" @click="editingProfile = false">Cancel</button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Booking Modal -->
    <div v-if="showBookingModal" class="modal-overlay" @click="showBookingModal = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>{{ editingBooking ? 'Edit Appointment' : 'Create Appointment' }}</h3>
          <button @click="showBookingModal = false" class="close-btn">×</button>
        </div>

        <form @submit.prevent="saveBooking" class="form">
          <div class="form-group">
            <label>Customer</label>
            <select v-model="bookingForm.customerId" required>
              <option value="">Select Customer</option>
              <option value="cust1">Customer 1</option>
              <option value="cust2">Customer 2</option>
            </select>
          </div>

          <div class="form-group">
            <label>Select Services</label>
            <p class="text-muted" style="font-size: 12px; margin-bottom: 8px">Choose one or more services for this appointment</p>
            <div class="checkbox-group">
              <label v-for="service in availableServices" :key="service.id">
                <input v-model="bookingForm.selectedServices" type="checkbox" :value="service.id">
                {{ service.name }}
              </label>
            </div>
          </div>

          <div class="form-group">
            <label>Date & Time</label>
            <input v-model="bookingForm.datetime" type="datetime-local" required>
          </div>

          <div class="form-group">
            <label>Notes</label>
            <textarea v-model="bookingForm.notes"></textarea>
          </div>

          <div style="display: flex; gap: 12px">
            <button type="submit" class="btn btn-primary">Save Appointment</button>
            <button type="button" class="btn btn-secondary" @click="showBookingModal = false">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Package Modal -->
    <div v-if="showPackageModal" class="modal-overlay" @click="showPackageModal = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>Create Service Package</h3>
          <button @click="showPackageModal = false" class="close-btn">×</button>
        </div>

        <form @submit.prevent="savePackage" class="form">
          <div class="form-group">
            <label>Package Name</label>
            <input v-model="packageForm.name" type="text" required>
          </div>

          <div class="form-group">
            <label>Description</label>
            <textarea v-model="packageForm.description"></textarea>
          </div>

          <div class="form-group">
            <label>
              <input v-model="packageForm.exclusive" type="checkbox">
              Exclusive Package
            </label>
          </div>

          <div class="form-group">
            <label>Select Services</label>
            <div class="checkbox-group">
              <label v-for="service in availableServices" :key="service.id">
                <input v-model="packageForm.selectedServices" type="checkbox" :value="service.id">
                {{ service.name }}
              </label>
            </div>
          </div>

          <div style="display: flex; gap: 12px">
            <button type="submit" class="btn btn-primary">Create Package</button>
            <button type="button" class="btn btn-secondary" @click="showPackageModal = false">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAppStore } from '@/stores/appStore'
import { useRouter } from 'vue-router'
import { apiClient } from '@/api/apiClient'

const router = useRouter()
const appStore = useAppStore()

// View Management
const currentView = ref('overview')

// Data
const managerData = ref({
  name: 'Manager Name',
  email: 'manager@email.com',
  contact: '+91-9876543210',
  address: 'Bangalore, India',
  dob: '1990-01-15',
  doj: '2020-06-01'
})

const bookings = ref([
  { id: 1, customerName: 'Sofia Mensah', datetime: '2025-03-25T14:00', status: 'Confirmed' },
  { id: 2, customerName: 'Amara Osei', datetime: '2025-03-26T10:30', status: 'Completed' }
])

const packages = ref([
  { id: 1, name: 'Rajam Package', description: 'Pedicure, Manicure, Facial', services: [{ id: 1, name: 'Pedicure' }], exclusive: true }
])

const customers = ref([
  { id: 1, name: 'Sofia Mensah', email: 'sofia@email.com', phone: '+91-9876543210', preferences: 'Relaxing massage, No chemicals', noOfVisits: 5, invoices: 3, totalSpent: 2500 },
  { id: 2, name: 'Amara Osei', email: 'amara@email.com', phone: '+91-9876543211', preferences: 'Hair coloring, Natural products', noOfVisits: 12, invoices: 8, totalSpent: 5800 },
  { id: 3, name: 'Aisha Khan', email: 'aisha@email.com', phone: '+91-9876543212', preferences: 'Bridal services, Detailed makeup', noOfVisits: 2, invoices: 2, totalSpent: 1200 }
])

const availableServices = ref([
  { id: 1, name: 'Pedicure' },
  { id: 2, name: 'Manicure' },
  { id: 3, name: 'Facial' }
])

// Service Form
const serviceForm = ref({
  name: '',
  category: '',
  price: 0,
  duration: 0,
  rewardPoints: 0,
  fromDate: '',
  toDate: '',
  isAllergyFree: false,
  isExclusive: false,
  description: ''
})

// Booking Form
const bookingForm = ref({
  customerId: '',
  selectedServices: [],
  datetime: '',
  notes: '',
  serviceIds: [],
  staffId: '',
  date: '',
  time: ''
})

// New Booking Form for appointments view
const newBookingForm = ref({
  customerId: '',
  serviceIds: [],
  staffId: '',
  date: '',
  time: ''
})

const bookingError = ref('')
const bookingSuccess = ref('')

// Available Stylists
const availableStylists = ref([
  { id: 1, name: 'Sarah Johnson', rating: 4.8, skills: 'Hair Styling, Coloring' },
  { id: 2, name: 'Emma Davis', rating: 4.6, skills: 'Manicure, Pedicure' },
  { id: 3, name: 'Lisa Chen', rating: 4.9, skills: 'Facial Treatment, Massage' },
  { id: 4, name: 'Priya Nair', rating: 4.7, skills: 'Hair Styling, Pedicure' },
  { id: 5, name: 'Amara Osei', rating: 4.8, skills: 'Spa Package, Massage Therapy' }
])

// Available time slots
const availableTimes = computed(() => {
  const times = []
  for (let hour = 9; hour <= 17; hour++) {
    times.push(`${String(hour).padStart(2, '0')}:00`)
    times.push(`${String(hour).padStart(2, '0')}:30`)
  }
  return times
})

// Staff Schedule
const selectedStaffDate = ref(new Date().toISOString().split('T')[0])

const staffForSelectedDay = computed(() => {
  // Get all staff with appointments on the selected date
  // For now, return all available stylists (in a real app, filter by date)
  return availableStylists.value
})

// Get today's date for min date validation
const getTodayDate = computed(() => {
  const today = new Date()
  return today.toISOString().split('T')[0]
})

// Package Form
const packageForm = ref({
  name: '',
  description: '',
  exclusive: false,
  selectedServices: []
})

// Password Form
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// Modal States
const showBookingModal = ref(false)
const showPackageModal = ref(false)
const editingProfile = ref(false)
const editingBooking = ref(false)

// Computed
const activeCustomers = computed(() => new Set(bookings.value.map(b => b.customerName)).size)
const servicesCreated = computed(() => availableServices.value.length)

// Methods
const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}

const createService = async () => {
  try {
    // API call would go here
    console.log('Creating service:', serviceForm.value)
    availableServices.value.push({ id: Date.now(), name: serviceForm.value.name })
    
    // Reset form
    serviceForm.value = {
      name: '',
      category: '',
      price: 0,
      duration: 0,
      rewardPoints: 0,
      fromDate: '',
      toDate: '',
      isAllergyFree: false,
      isExclusive: false,
      description: ''
    }
    
    alert('Service created successfully!')
  } catch (error) {
    console.error('Error creating service:', error)
  }
}

const editBooking = (booking) => {
  editingBooking.value = true
  bookingForm.value = { ...booking }
  showBookingModal.value = true
}

const saveBooking = () => {
  if (editingBooking.value) {
    const index = bookings.value.findIndex(b => b.id === bookingForm.value.id)
    if (index !== -1) {
      bookings.value[index] = { ...bookingForm.value }
    }
  } else {
    bookings.value.push({
      id: Date.now(),
      ...bookingForm.value,
      status: 'Confirmed'
    })
  }
  
  showBookingModal.value = false
  editingBooking.value = false
  bookingForm.value = { customerId: '', selectedServices: [], datetime: '', notes: '' }
  alert('Appointment saved successfully!')
}

const handleBookAppointment = () => {
  bookingError.value = ''
  bookingSuccess.value = ''

  if (bookingForm.value.serviceIds.length === 0) {
    bookingError.value = "Please select at least one service"
    return
  }

  if (!bookingForm.value.customerId) {
    bookingError.value = "Please select a customer"
    return
  }

  if (!bookingForm.value.date) {
    bookingError.value = "Please select a date"
    return
  }

  if (!bookingForm.value.time) {
    bookingError.value = "Please select a time"
    return
  }

  const selectedServices = bookingForm.value.serviceIds.map(id => 
    availableServices.value.find(s => s.id == id)
  ).filter(s => s)
  
  const serviceNames = selectedServices.map(s => s.name).join(', ')
  const staff = availableStylists.value.find(s => s.id == bookingForm.value.staffId)
  const staffName = staff ? staff.name : 'Not assigned'
  const customer = customers.value.find(c => c.id == bookingForm.value.customerId)
  const customerName = customer ? customer.name : 'Unknown'

  const newAppointment = {
    id: Math.max(...bookings.value.map(a => a.id || 0), 0) + 1,
    customerName: customerName,
    datetime: `${bookingForm.value.date}T${bookingForm.value.time}`,
    status: "Confirmed",
    services: serviceNames,
    staff: staffName
  }

  bookings.value.push(newAppointment)
  bookingSuccess.value = `Appointment booked successfully with ${staffName} on ${bookingForm.value.date} at ${bookingForm.value.time}!`

  setTimeout(() => {
    bookingForm.value = {
      customerId: '',
      selectedServices: [],
      datetime: '',
      notes: '',
      serviceIds: [],
      staffId: '',
      date: '',
      time: ''
    }
    bookingSuccess.value = ''
    currentView.value = 'bookings'
  }, 2000)
}

const deleteBooking = (id) => {
  if (confirm('Are you sure you want to delete this appointment?')) {
    bookings.value = bookings.value.filter(b => b.id !== id)
  }
}

const handleCreateAppointment = () => {
  bookingError.value = ''
  bookingSuccess.value = ''

  if (newBookingForm.value.serviceIds.length === 0) {
    bookingError.value = "Please select at least one service"
    return
  }

  if (!newBookingForm.value.customerId) {
    bookingError.value = "Please select a customer"
    return
  }

  if (!newBookingForm.value.date) {
    bookingError.value = "Please select a date"
    return
  }

  if (!newBookingForm.value.time) {
    bookingError.value = "Please select a time"
    return
  }

  const selectedServices = newBookingForm.value.serviceIds.map(id => 
    availableServices.value.find(s => s.id == id)
  ).filter(s => s)
  
  const serviceNames = selectedServices.map(s => s.name).join(', ')
  const staff = availableStylists.value.find(s => s.id == newBookingForm.value.staffId)
  const staffName = staff ? staff.name : 'Not assigned'
  const customer = customers.value.find(c => c.id == newBookingForm.value.customerId)
  const customerName = customer ? customer.name : 'Unknown'

  const newAppointment = {
    id: Math.max(...bookings.value.map(a => a.id || 0), 0) + 1,
    customerName: customerName,
    datetime: `${newBookingForm.value.date}T${newBookingForm.value.time}`,
    status: "Confirmed",
    services: serviceNames,
    staff: staffName
  }

  bookings.value.push(newAppointment)
  bookingSuccess.value = `Appointment booked successfully with ${staffName} on ${newBookingForm.value.date} at ${newBookingForm.value.time}!`

  setTimeout(() => {
    resetBookingForm()
    bookingSuccess.value = ''
  }, 2000)
}

const resetBookingForm = () => {
  newBookingForm.value = {
    customerId: '',
    serviceIds: [],
    staffId: '',
    date: '',
    time: ''
  }
}

const editPackage = (pkg) => {
  packageForm.value = { ...pkg }
  showPackageModal.value = true
}

const savePackage = () => {
  const newPackage = {
    id: Date.now(),
    ...packageForm.value,
    services: packageForm.value.selectedServices.map(id => 
      availableServices.value.find(s => s.id === id)
    )
  }
  packages.value.push(newPackage)
  
  showPackageModal.value = false
  packageForm.value = { name: '', description: '', exclusive: false, selectedServices: [] }
  alert('Package created successfully!')
}

const deletePackage = (id) => {
  if (confirm('Are you sure you want to delete this package?')) {
    packages.value = packages.value.filter(p => p.id !== id)
  }
}

const updateProfile = async () => {
  try {
    // API call would go here
    editingProfile.value = false
    alert('Profile updated successfully!')
  } catch (error) {
    console.error('Error updating profile:', error)
  }
}

const changePassword = async () => {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    alert('New passwords do not match!')
    return
  }

  try {
    // API call would go here
    console.log('Changing password...')
    alert('Password changed successfully!')
    editingProfile.value = false
    passwordForm.value = { oldPassword: '', newPassword: '', confirmPassword: '' }
  } catch (error) {
    console.error('Error changing password:', error)
  }
}

const handleLogout = () => {
  appStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.dashboard-container {
  display: flex;
  height: 100vh;
  background: var(--light-bg);
}

.dashboard-sidebar {
  width: 260px;
  background: var(--charcoal);
  color: white;
  padding: 24px;
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--border);
}

.sidebar-header {
  margin-bottom: 32px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-menu {
  flex: 1;
}

.nav-item {
  padding: 12px 16px;
  margin-bottom: 8px;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 10px;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.nav-item.active {
  background: var(--gold);
  color: var(--charcoal);
  font-weight: 600;
}

.nav-icon {
  font-size: 18px;
}

.sidebar-footer {
  display: flex;
}

.dashboard-main {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
}

.content-wrap {
  max-width: 1200px;
  margin: 0 auto;
}

.fade-in {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  text-align: center;
}

.stat-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.stat-label {
  color: #666;
  font-size: 14px;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--gold);
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
}

.card-header {
  padding: 20px;
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.card-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--border);
  border-radius: 4px;
  font-size: 14px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 0;
}

.checkbox-group input[type="checkbox"] {
  width: auto;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.2);
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.appointments-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 20px;
}

.appointment-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: #f9f9f9;
}

.appointment-info {
  flex: 1;
}

.appointment-info h4 {
  margin: 0 0 8px 0;
  font-weight: 600;
}

.appointment-info p {
  margin: 0 0 8px 0;
  color: #666;
  font-size: 14px;
}

.appointment-actions {
  display: flex;
  gap: 8px;
}

.packages-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 20px;
}

.package-card {
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  background: #f9f9f9;
}

.package-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.package-header h4 {
  margin: 0;
}

.package-desc {
  font-size: 14px;
  color: #666;
  margin-bottom: 12px;
}

.services-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 12px;
}

.services-list small {
  font-size: 12px;
  color: #888;
}

.package-actions {
  display: flex;
  gap: 8px;
}

.btn {
  padding: 10px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.btn-primary {
  background: var(--gold);
  color: var(--charcoal);
}

.btn-primary:hover {
  background: #d4a956;
}

.btn-secondary {
  background: #e0e0e0;
  color: var(--charcoal);
}

.btn-secondary:hover {
  background: #d0d0d0;
}

.btn-danger {
  background: #ff6b6b;
  color: white;
}

.btn-danger:hover {
  background: #ff5252;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
}

.w-full {
  width: 100%;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.badge-confirmed {
  background: #d4edda;
  color: #155724;
}

.badge-completed {
  background: #cfe2ff;
  color: #084298;
}

.badge-cancelled {
  background: #f8d7da;
  color: #842029;
}

.badge-exclusive {
  background: var(--gold);
  color: var(--charcoal);
}

.profile-info {
  padding: 20px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
}

.info-row label {
  font-weight: 600;
  color: #666;
}

.profile-form {
  padding: 20px;
}

.password-form {
  padding: 20px 0;
}

.password-form h4 {
  margin: 0 0 16px 0;
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
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1);
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.btn-outline {
  background: white;
  border: 1px solid var(--border);
  color: var(--charcoal);
}

.btn-outline:hover {
  background: var(--light-bg);
}


.text-muted {
  color: #777;
}

@media (max-width: 768px) {
  .dashboard-container {
    flex-direction: column;
  }

  .dashboard-sidebar {
    width: 100%;
    padding: 16px;
  }

  .sidebar-menu {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 8px;
  }

  .nav-item {
    margin-bottom: 0;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .packages-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
