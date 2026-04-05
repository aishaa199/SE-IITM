<template>
  <div class="dashboard-container">
    <!-- Sidebar Navigation -->
    <div class="dashboard-sidebar">
      <div class="sidebar-header">
        <h2 style="color: var(--gold); font-size: 24px; margin: 0">👑 Owner Hub</h2>
        <p style="color: #6f675a; margin: 8px 0 0 0; font-size: 12px">{{ ownerData.ownerName }}</p>
      </div>

      <div class="sidebar-menu">
        <div
          :class="['nav-item', { active: currentView === 'overview' }]"
          @click="currentView = 'overview'"
        >
          <span class="nav-icon">📊</span> Overview
        </div>

        <div
          :class="['nav-item', { active: currentView === 'managers' }]"
          @click="currentView = 'managers'"
        >
          <span class="nav-icon">⚙️</span> Manage Managers
        </div>

        <div
          :class="['nav-item', { active: currentView === 'reports' }]"
          @click="currentView = 'reports'"
        >
          <span class="nav-icon">📊</span> Reports & Analytics
        </div>
        <div
          :class="['nav-item', { active: currentView === 'profile' }]"
          @click="currentView = 'profile'"
        >
          <span class="nav-icon">👤</span> My Profile
        </div>
      </div>

      <div class="sidebar-footer">
        <button class="btn btn-secondary w-full" @click="showChangePasswordModal = true" style="margin-top: auto; margin-bottom: 8px">
          🔑 Change Password
        </button>
        <button class="btn btn-secondary w-full" @click="handleLogout">
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
              <div class="stat-icon">📊</div>
              <div class="stat-label">Total Revenue</div>
              <div class="stat-value">₹{{ totalRevenue }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">📅</div>
              <div class="stat-label">Total Bookings</div>
              <div class="stat-value">{{ totalBookings }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">👥</div>
              <div class="stat-label">Total Customers</div>
              <div class="stat-value">{{ totalCustomers }}</div>
            </div>
          </div>

          <!-- Additional Insights -->
          <div class="stats-grid" style="margin-top: 24px">
            <div class="stat-card">
              <div class="stat-icon">💰</div>
              <div class="stat-label">Avg Revenue/Booking</div>
              <div class="stat-value">₹{{ avgRevenuePerBooking }}</div>
              <div class="stat-icon">⭐</div>
              <div class="stat-label">Overall Performance</div>
              <div class="stat-value">{{ overallPerformance }}%</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">🎯</div>
              <div class="stat-label">Business Health</div>
              <div class="stat-value" :style="{ color: businessHealthColor }">{{ businessHealth }}</div>
            </div>
          </div>

          <!-- PIE CHART - Customer Distribution -->
          <div class="card" style="margin-top: 24px;">
            <div class="card-header">
              <h3 class="card-title">🥧 Customer Distribution (Pie Chart)</h3>
            </div>
            <div class="card-body" style="padding: 40px; text-align: center;">
              <div style="display: flex; justify-content: center; align-items: center; gap: 60px; flex-wrap: wrap">
                <!-- Pie Chart Visual -->
                <div style="position: relative; width: 250px; height: 250px">
                  <svg width="250" height="250" style="transform: rotate(-90deg)">
                    <!-- Active Customers - 60% (Gold) -->
                    <circle cx="125" cy="125" r="80" fill="none" stroke="#d4af37" stroke-width="50" stroke-dasharray="301.6 503.4"/>
                    <!-- Returning - 30% (Orange) -->
                    <circle cx="125" cy="125" r="80" fill="none" stroke="#f59e0b" stroke-width="50" stroke-dasharray="150.8 503.4" stroke-dashoffset="-301.6"/>
                    <!-- New - 10% (Purple) -->
                    <circle cx="125" cy="125" r="80" fill="none" stroke="#8b5cf6" stroke-width="50" stroke-dasharray="50.3 503.4" stroke-dashoffset="-452.4"/>
                  </svg>
                  <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center">
                    <div style="font-size: 36px; font-weight: bold; color: var(--gold)">{{ totalCustomers }}</div>
                    <div style="font-size: 12px; color: #6f675a">Total</div>
                  </div>
                </div>
                
                <!-- Legend -->
                <div style="text-align: left">
                  <div style="margin-bottom: 20px; padding: 12px; border-radius: 6px; background: rgba(212, 175, 55, 0.1); border-left: 5px solid #d4af37">
                    <div style="display: flex; align-items: center; gap: 10px">
                      <div style="width: 20px; height: 20px; background: #d4af37; border-radius: 3px"></div>
                      <span style="font-weight: 600">Active Customers</span>
                      <span style="color: var(--gold); font-weight: 700">{{ Math.ceil(totalCustomers * 0.6) }} (60%)</span>
                    </div>
                  </div>
                  <div style="margin-bottom: 20px; padding: 12px; border-radius: 6px; background: rgba(245, 158, 11, 0.1); border-left: 5px solid #f59e0b">
                    <div style="display: flex; align-items: center; gap: 10px">
                      <div style="width: 20px; height: 20px; background: #f59e0b; border-radius: 3px"></div>
                      <span style="font-weight: 600">Returning</span>
                      <span style="color: #f59e0b; font-weight: 700">{{ Math.ceil(totalCustomers * 0.3) }} (30%)</span>
                    </div>
                  </div>
                  <div style="padding: 12px; border-radius: 6px; background: rgba(139, 92, 246, 0.1); border-left: 5px solid #8b5cf6">
                    <div style="display: flex; align-items: center; gap: 10px">
                      <div style="width: 20px; height: 20px; background: #8b5cf6; border-radius: 3px"></div>
                      <span style="font-weight: 600">New Visitors</span>
                      <span style="color: #8b5cf6; font-weight: 700">{{ Math.ceil(totalCustomers * 0.1) }} (10%)</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- BAR CHART - Revenue by Day -->
          <div class="card" style="margin-top: 24px;">
            <div class="card-header">
              <h3 class="card-title">📊 Revenue by Day (Bar Chart)</h3>
            </div>
            <div class="card-body" style="padding: 40px">
              <div style="display: flex; align-items: flex-end; gap: 20px; height: 300px; justify-content: center; padding-bottom: 20px">
                <!-- Monday -->
                <div style="display: flex; flex-direction: column; align-items: center; gap: 12px">
                  <div style="width: 60px; height: 150px; background: linear-gradient(180deg, #d4af37 0%, #b89e2c 100%); border-radius: 6px 6px 0 0; box-shadow: 0 8px 16px rgba(212, 175, 55, 0.3); position: relative"
                    @mouseenter="hoveredBar = 'mon'" @mouseleave="hoveredBar = null">
                    <div v-if="hoveredBar === 'mon'" style="position: absolute; top: -35px; left: 50%; transform: translateX(-50%); background: var(--gold); color: var(--text); padding: 8px 16px; border-radius: 4px; font-weight: 700; white-space: nowrap; font-size: 14px">₹500</div>
                  </div>
                  <div style="font-weight: 700">Mon</div>
                  <div style="font-size: 12px; color: #6f675a">₹500</div>
                </div>

                <!-- Tuesday -->
                <div style="display: flex; flex-direction: column; align-items: center; gap: 12px">
                  <div style="width: 60px; height: 200px; background: linear-gradient(180deg, #d4af37 0%, #b89e2c 100%); border-radius: 6px 6px 0 0; box-shadow: 0 8px 16px rgba(212, 175, 55, 0.3); position: relative"
                    @mouseenter="hoveredBar = 'tue'" @mouseleave="hoveredBar = null">
                    <div v-if="hoveredBar === 'tue'" style="position: absolute; top: -35px; left: 50%; transform: translateX(-50%); background: var(--gold); color: var(--text); padding: 8px 16px; border-radius: 4px; font-weight: 700; white-space: nowrap; font-size: 14px">₹750</div>
                  </div>
                  <div style="font-weight: 700">Tue</div>
                  <div style="font-size: 12px; color: #6f675a">₹750</div>
                </div>

                <!-- Wednesday -->
                <div style="display: flex; flex-direction: column; align-items: center; gap: 12px">
                  <div style="width: 60px; height: 180px; background: linear-gradient(180deg, #d4af37 0%, #b89e2c 100%); border-radius: 6px 6px 0 0; box-shadow: 0 8px 16px rgba(212, 175, 55, 0.3); position: relative"
                    @mouseenter="hoveredBar = 'wed'" @mouseleave="hoveredBar = null">
                    <div v-if="hoveredBar === 'wed'" style="position: absolute; top: -35px; left: 50%; transform: translateX(-50%); background: var(--gold); color: var(--text); padding: 8px 16px; border-radius: 4px; font-weight: 700; white-space: nowrap; font-size: 14px">₹600</div>
                  </div>
                  <div style="font-weight: 700">Wed</div>
                  <div style="font-size: 12px; color: #6f675a">₹600</div>
                </div>

                <!-- Thursday -->
                <div style="display: flex; flex-direction: column; align-items: center; gap: 12px">
                  <div style="width: 60px; height: 240px; background: linear-gradient(180deg, #d4af37 0%, #b89e2c 100%); border-radius: 6px 6px 0 0; box-shadow: 0 8px 16px rgba(212, 175, 55, 0.3); position: relative"
                    @mouseenter="hoveredBar = 'thu'" @mouseleave="hoveredBar = null">
                    <div v-if="hoveredBar === 'thu'" style="position: absolute; top: -35px; left: 50%; transform: translateX(-50%); background: var(--gold); color: var(--text); padding: 8px 16px; border-radius: 4px; font-weight: 700; white-space: nowrap; font-size: 14px">₹800</div>
                  </div>
                  <div style="font-weight: 700">Thu</div>
                  <div style="font-size: 12px; color: #6f675a">₹800</div>
                </div>

                <!-- Friday -->
                <div style="display: flex; flex-direction: column; align-items: center; gap: 12px">
                  <div style="width: 60px; height: 190px; background: linear-gradient(180deg, #d4af37 0%, #b89e2c 100%); border-radius: 6px 6px 0 0; box-shadow: 0 8px 16px rgba(212, 175, 55, 0.3); position: relative"
                    @mouseenter="hoveredBar = 'fri'" @mouseleave="hoveredBar = null">
                    <div v-if="hoveredBar === 'fri'" style="position: absolute; top: -35px; left: 50%; transform: translateX(-50%); background: var(--gold); color: var(--text); padding: 8px 16px; border-radius: 4px; font-weight: 700; white-space: nowrap; font-size: 14px">₹650</div>
                  </div>
                  <div style="font-weight: 700">Fri</div>
                  <div style="font-size: 12px; color: #6f675a">₹650</div>
                </div>
              </div>
            </div>
          </div>

          <!-- LARGE Revenue Trend Chart -->
          <div class="card" style="margin-top: 24px; width: 100%;">
            <div class="card-header">
              <h3 class="card-title">📊 Revenue Trend Chart - Weekly Performance</h3>
            </div>
            <div class="card-body" style="padding: 32px">
              <div style="display: flex; align-items: flex-end; gap: 16px; height: 280px; justify-content: space-around">
                <div v-for="(booking, idx) in ownerData.bookings" :key="idx" style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; gap: 12px">
                  <div 
                    :style="{ height: (booking.amount / 800) * 240 + 'px' }"
                    style="width: 100%; background: linear-gradient(180deg, var(--gold) 0%, rgba(212, 175, 55, 0.6) 100%); border-radius: 8px 8px 0 0; transition: all 0.3s ease; cursor: pointer; min-height: 30px; box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3); position: relative"
                    @mouseenter="hoveredBar = idx"
                    @mouseleave="hoveredBar = null"
                  >
                    <div v-if="hoveredBar === idx" style="position: absolute; top: -30px; left: 50%; transform: translateX(-50%); background: var(--gold); color: var(--text); padding: 6px 12px; border-radius: 4px; font-weight: 600; white-space: nowrap; font-size: 14px">₹{{ booking.amount }}</div>
                  </div>
                  <div style="font-weight: 600">Day {{ idx + 1 }}</div>
                  <div class="text-muted" style="font-size: 12px">₹{{ booking.amount }}</div>
                </div>
              </div>
              <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--border); display: flex; justify-content: space-around; text-align: center">
                <div>
                  <div class="text-muted" style="font-size: 12px">Highest Revenue</div>
                  <div style="font-weight: 600; color: var(--gold); font-size: 18px">₹{{ Math.max(...ownerData.bookings.map(b => b.amount)) }}</div>
                </div>
                <div>
                  <div class="text-muted" style="font-size: 12px">Lowest Revenue</div>
                  <div style="font-weight: 600; color: #3b82f6; font-size: 18px">₹{{ Math.min(...ownerData.bookings.map(b => b.amount)) }}</div>
                </div>
                <div>
                  <div class="text-muted" style="font-size: 12px">Average Revenue</div>
                  <div style="font-weight: 600; color: #22c55e; font-size: 18px">₹{{ Math.round(ownerData.bookings.reduce((sum, b) => sum + b.amount, 0) / ownerData.bookings.length) }}</div>
                </div>
              </div>
            </div>
          </div>


          <!-- Performance Analysis Row -->
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 24px">
            <!-- LARGE Customer Distribution Pie Chart -->
            <div class="card">
              <div class="card-header">
                <h3 class="card-title">🥧 Customer Segment Analysis</h3>
              </div>
              <div class="card-body" style="padding: 32px; text-align: center">
                <div style="display: flex; justify-content: center; align-items: center; gap: 32px">
                  <div style="width: 180px; height: 180px; border-radius: 50%; background: conic-gradient(from 0deg, #d4af37 0deg 216deg, #f59e0b 216deg 324deg, #8b5cf6 324deg 360deg); display: flex; align-items: center; justify-content: center; font-weight: bold; color: white; font-size: 32px; box-shadow: 0 8px 24px rgba(0,0,0,0.3)">
                    {{ totalCustomers }}
                  </div>
                  <div style="text-align: left; flex: 1">
                    <div style="margin-bottom: 16px; padding: 12px; background: var(--light-bg); border-radius: 8px; border-left: 5px solid #d4af37">
                      <div style="display: flex; justify-content: space-between; align-items: center">
                        <div><span style="display: inline-block; width: 14px; height: 14px; background: #d4af37; border-radius: 3px; margin-right: 10px"></span> <span style="font-weight: 600">Active</span></div>
                        <div style="font-weight: 600; color: #d4af37">{{ Math.ceil(totalCustomers * 0.6) }} (60%)</div>
                      </div>
                    </div>
                    <div style="margin-bottom: 16px; padding: 12px; background: var(--light-bg); border-radius: 8px; border-left: 5px solid #f59e0b">
                      <div style="display: flex; justify-content: space-between; align-items: center">
                        <div><span style="display: inline-block; width: 14px; height: 14px; background: #f59e0b; border-radius: 3px; margin-right: 10px"></span> <span style="font-weight: 600">Returning</span></div>
                        <div style="font-weight: 600; color: #f59e0b">{{ Math.ceil(totalCustomers * 0.3) }} (30%)</div>
                      </div>
                    </div>
                    <div style="padding: 12px; background: var(--light-bg); border-radius: 8px; border-left: 5px solid #8b5cf6">
                      <div style="display: flex; justify-content: space-between; align-items: center">
                        <div><span style="display: inline-block; width: 14px; height: 14px; background: #8b5cf6; border-radius: 3px; margin-right: 10px"></span> <span style="font-weight: 600">New Visitors</span></div>
                        <div style="font-weight: 600; color: #8b5cf6">{{ Math.ceil(totalCustomers * 0.1) }} (10%)</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Growth Metrics -->
            <div class="card">
              <div class="card-header">
                <h3 class="card-title">📈 Business Performance Metrics</h3>
              </div>
              <div class="card-body" style="padding: 32px">
                <div style="display: flex; flex-direction: column; gap: 20px">
                  <div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 12px; align-items: center">
                      <span style="font-weight: 600">Monthly Growth Rate</span>
                      <span style="color: #22c55e; font-weight: 700; font-size: 18px">↑ 12.5%</span>
                    </div>
                    <div style="height: 12px; background: #444; border-radius: 6px; overflow: hidden">
                      <div style="height: 100%; width: 65%; background: linear-gradient(90deg, #22c55e, #16a34a); border-radius: 6px; box-shadow: 0 0 12px rgba(34, 197, 94, 0.4)"></div>
                    </div>
                  </div>

                  <div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 12px; align-items: center">
                      <span style="font-weight: 600">Customer Satisfaction</span>
                      <span style="color: #3b82f6; font-weight: 700; font-size: 18px">⭐ 4.8/5.0</span>
                    </div>
                    <div style="height: 12px; background: #444; border-radius: 6px; overflow: hidden">
                      <div style="height: 100%; width: 96%; background: linear-gradient(90deg, #3b82f6, #1d4ed8); border-radius: 6px; box-shadow: 0 0 12px rgba(59, 130, 246, 0.4)"></div>
                    </div>
                  </div>

                  <div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 12px; align-items: center">
                      <span style="font-weight: 600">Staff Performance</span>
                      <span style="color: #f59e0b; font-weight: 700; font-size: 18px">⚡ Excellent</span>
                    </div>
                    <div style="height: 12px; background: #444; border-radius: 6px; overflow: hidden">
                      <div style="height: 100%; width: 88%; background: linear-gradient(90deg, #f59e0b, #d97706); border-radius: 6px; box-shadow: 0 0 12px rgba(245, 158, 11, 0.4)"></div>
                    </div>
                  </div>

                  <div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 12px; align-items: center">
                      <span style="font-weight: 600">Booking Pipeline</span>
                      <span style="color: #ec4899; font-weight: 700; font-size: 18px">📅 42</span>
                    </div>
                    <div style="height: 12px; background: #444; border-radius: 6px; overflow: hidden">
                      <div style="height: 100%; width: 78%; background: linear-gradient(90deg, #ec4899, #be185d); border-radius: 6px; box-shadow: 0 0 12px rgba(236, 72, 153, 0.4)"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- LARGE Analytics Row -->
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 24px">
            <!-- LARGE Revenue by Day Chart -->
            <div class="card">
              <div class="card-header">
                <h3 class="card-title">🏆 Daily Revenue Distribution - Weekly Breakdown</h3>
              </div>
              <div class="card-body" style="padding: 32px">
                <div style="display: flex; align-items: flex-end; gap: 12px; height: 220px; justify-content: space-around">
                  <div style="text-align: center; flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; gap: 12px">
                    <div style="height: 120px; width: 90%; background: linear-gradient(180deg, var(--gold), rgba(212, 175, 55, 0.4)); border-radius: 6px 6px 0 0; box-shadow: 0 4px 8px rgba(212, 175, 55, 0.2)"
                      @mouseenter="hoveredBar = 0" @mouseleave="hoveredBar = null">
                      <div v-if="hoveredBar === 0" style="text-align: center; padding-top: 8px; font-weight: 600; color: var(--gold)">₹800</div>
                    </div>
                    <div style="font-weight: 700; font-size: 14px">Monday</div>
                    <div class="text-muted">₹800</div>
                  </div>
                  <div style="text-align: center; flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; gap: 12px">
                    <div style="height: 160px; width: 90%; background: linear-gradient(180deg, var(--gold), rgba(212, 175, 55, 0.4)); border-radius: 6px 6px 0 0; box-shadow: 0 4px 8px rgba(212, 175, 55, 0.2)"
                      @mouseenter="hoveredBar = 1" @mouseleave="hoveredBar = null">
                      <div v-if="hoveredBar === 1" style="text-align: center; padding-top: 8px; font-weight: 600; color: var(--gold)">₹1200</div>
                    </div>
                    <div style="font-weight: 700; font-size: 14px">Tuesday</div>
                    <div class="text-muted">₹1200</div>
                  </div>
                  <div style="text-align: center; flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; gap: 12px">
                    <div style="height: 130px; width: 90%; background: linear-gradient(180deg, var(--gold), rgba(212, 175, 55, 0.4)); border-radius: 6px 6px 0 0; box-shadow: 0 4px 8px rgba(212, 175, 55, 0.2)"
                      @mouseenter="hoveredBar = 2" @mouseleave="hoveredBar = null">
                      <div v-if="hoveredBar === 2" style="text-align: center; padding-top: 8px; font-weight: 600; color: var(--gold)">₹900</div>
                    </div>
                    <div style="font-weight: 700; font-size: 14px">Wednesday</div>
                    <div class="text-muted">₹900</div>
                  </div>
                  <div style="text-align: center; flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; gap: 12px">
                    <div style="height: 180px; width: 90%; background: linear-gradient(180deg, var(--gold), rgba(212, 175, 55, 0.4)); border-radius: 6px 6px 0 0; box-shadow: 0 4px 8px rgba(212, 175, 55, 0.2)"
                      @mouseenter="hoveredBar = 3" @mouseleave="hoveredBar = null">
                      <div v-if="hoveredBar === 3" style="text-align: center; padding-top: 8px; font-weight: 600; color: var(--gold)">₹1400</div>
                    </div>
                    <div style="font-weight: 700; font-size: 14px">Thursday</div>
                    <div class="text-muted">₹1400</div>
                  </div>
                  <div style="text-align: center; flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; gap: 12px">
                    <div style="height: 150px; width: 90%; background: linear-gradient(180deg, var(--gold), rgba(212, 175, 55, 0.4)); border-radius: 6px 6px 0 0; box-shadow: 0 4px 8px rgba(212, 175, 55, 0.2)"
                      @mouseenter="hoveredBar = 4" @mouseleave="hoveredBar = null">
                      <div v-if="hoveredBar === 4" style="text-align: center; padding-top: 8px; font-weight: 600; color: var(--gold)">₹1100</div>
                    </div>
                    <div style="font-weight: 700; font-size: 14px">Friday</div>
                    <div class="text-muted">₹1100</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Key Metrics Summary -->
            <div class="card">
              <div class="card-header">
                <h3 class="card-title">✨ Executive Summary & KPIs</h3>
              </div>
              <div class="card-body" style="padding: 32px">
                <div style="display: flex; flex-direction: column; gap: 14px">
                  <div style="padding: 16px; background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(34, 197, 94, 0.05)); border-radius: 8px; border-left: 5px solid #22c55e">
                    <div style="display: flex; justify-content: space-between; align-items: center">
                      <span>Avg Per-Booking Value</span>
                      <span style="font-weight: 700; font-size: 18px; color: #22c55e">₹{{ avgRevenuePerBooking }}</span>
                    </div>
                    <div class="text-muted" style="font-size: 12px; margin-top: 4px">↑ 8% from last week</div>
                  </div>

                  <div style="padding: 16px; background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(245, 158, 11, 0.05)); border-radius: 8px; border-left: 5px solid #f59e0b">
                    <div style="display: flex; justify-content: space-between; align-items: center">
                      <span>Conversion Rate</span>
                      <span style="font-weight: 700; font-size: 18px; color: #f59e0b">78%</span>
                    </div>
                    <div class="text-muted" style="font-size: 12px; margin-top: 4px">Above industry average</div>
                  </div>
                  <div style="padding: 16px; background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(139, 92, 246, 0.05)); border-radius: 8px; border-left: 5px solid #8b5cf6">
                    <div style="display: flex; justify-content: space-between; align-items: center">
                      <span>Customer Retention</span>
                      <span style="font-weight: 700; font-size: 18px; color: #8b5cf6">82%</span>
                    </div>
                    <div class="text-muted" style="font-size: 12px; margin-top: 4px">Excellent loyalty</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- REPORTS VIEW -->
        <div v-if="currentView === 'reports'" class="fade-in">

          <!-- ── Analytics drill-down panel ─────────────────────────── -->
          <template v-if="ownerAnalyticsView">
            <!-- Header -->
            <div class="card" style="margin-bottom: 16px;">
              <div class="card-body" style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                <button class="btn btn-outline" style="font-size: 13px; padding: 6px 14px;" @click="closeOwnerAnalytics">
                  ← Back
                </button>
                <span style="font-size: 22px;">{{ ownerAnalyticsView.icon }}</span>
                <div>
                  <div style="font-weight: 700; font-size: 16px; color: #2D2D2D;">{{ ownerAnalyticsView.title }}</div>
                  <div style="font-size: 12px; color: #8B7355;">{{ ownerAnalyticsView.periodLabel }}</div>
                </div>
              </div>
            </div>

            <!-- Loading / Error -->
            <div v-if="ownerAnalyticsLoading" style="text-align: center; padding: 48px; color: #8B7355; font-size: 14px;">
              Loading analytics…
            </div>
            <div v-else-if="ownerAnalyticsError" style="text-align: center; padding: 32px; color: #e53e3e; font-size: 14px;">
              ⚠️ {{ ownerAnalyticsError }}
            </div>

            <!-- Charts -->
            <template v-else-if="ownerAnalyticsData">
              <!-- Summary stat -->
              <div class="card" style="margin-bottom: 16px;">
                <div class="card-body" style="display: flex; gap: 24px; flex-wrap: wrap;">
                  <div v-if="ownerAnalyticsData.total !== undefined">
                    <div style="font-size: 11px; color: #8B7355; text-transform: uppercase; letter-spacing: 0.5px;">Total</div>
                    <div style="font-size: 28px; font-weight: 800; color: #2D2D2D;">{{ ownerAnalyticsData.total }}</div>
                  </div>
                  <div v-if="ownerAnalyticsData.total_revenue !== undefined">
                    <div style="font-size: 11px; color: #8B7355; text-transform: uppercase; letter-spacing: 0.5px;">Revenue</div>
                    <div style="font-size: 28px; font-weight: 800; color: #22c55e;">₹{{ ownerAnalyticsData.total_revenue?.toLocaleString('en-IN') }}</div>
                  </div>
                  <div v-if="ownerAnalyticsData.avg_rating !== undefined">
                    <div style="font-size: 11px; color: #8B7355; text-transform: uppercase; letter-spacing: 0.5px;">Avg Rating</div>
                    <div style="font-size: 28px; font-weight: 800; color: #d4af37;">{{ ownerAnalyticsData.avg_rating }} ★</div>
                  </div>
                </div>
              </div>

              <!-- Chart grid -->
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; margin-bottom: 16px;">
                <!-- Appointments -->
                <template v-if="ownerAnalyticsView.type === 'appointments'">
                  <div class="card">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Appointments Over Time</h3></div>
                    <div class="card-body" style="padding: 12px;"><canvas ref="ownerChartLine" style="max-height: 220px;"></canvas></div>
                  </div>
                  <div class="card">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Top Services</h3></div>
                    <div class="card-body" style="padding: 12px;"><canvas ref="ownerChartBar" style="max-height: 220px;"></canvas></div>
                  </div>
                  <div class="card" style="grid-column: 1 / -1;">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Status Breakdown</h3></div>
                    <div class="card-body" style="padding: 12px; display: flex; justify-content: center;"><canvas ref="ownerChartPie" style="max-height: 260px; max-width: 380px;"></canvas></div>
                  </div>
                </template>

                <!-- Sales -->
                <template v-else-if="ownerAnalyticsView.type === 'sales'">
                  <div class="card">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Revenue Over Time (INR)</h3></div>
                    <div class="card-body" style="padding: 12px;"><canvas ref="ownerChartLine" style="max-height: 220px;"></canvas></div>
                  </div>
                  <div class="card">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Revenue by Service</h3></div>
                    <div class="card-body" style="padding: 12px;"><canvas ref="ownerChartBar" style="max-height: 220px;"></canvas></div>
                  </div>
                </template>

                <!-- Staff -->
                <template v-else-if="ownerAnalyticsView.type === 'staff'">
                  <div class="card" style="grid-column: 1 / -1;">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Appointments per Staff</h3></div>
                    <div class="card-body" style="padding: 12px;"><canvas ref="ownerChartBar" style="max-height: 240px;"></canvas></div>
                  </div>
                  <div class="card" style="grid-column: 1 / -1;">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Staff Ratings</h3></div>
                    <div class="card-body" style="padding: 12px;"><canvas ref="ownerChartLine" style="max-height: 200px;"></canvas></div>
                  </div>
                </template>

                <!-- Inventory -->
                <template v-else-if="ownerAnalyticsView.type === 'inventory'">
                  <div class="card" style="grid-column: 1 / -1;">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Stock Levels</h3></div>
                    <div class="card-body" style="padding: 12px;"><canvas ref="ownerChartBar" style="max-height: 260px;"></canvas></div>
                  </div>
                </template>

                <!-- Feedback -->
                <template v-else-if="ownerAnalyticsView.type === 'feedback'">
                  <div class="card">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Ratings Distribution</h3></div>
                    <div class="card-body" style="padding: 12px;"><canvas ref="ownerChartBar" style="max-height: 220px;"></canvas></div>
                  </div>
                  <div class="card">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Sentiment Breakdown</h3></div>
                    <div class="card-body" style="padding: 12px; display: flex; justify-content: center;"><canvas ref="ownerChartPie" style="max-height: 220px; max-width: 280px;"></canvas></div>
                  </div>
                </template>

                <!-- Financial -->
                <template v-else-if="ownerAnalyticsView.type === 'financial'">
                  <div class="card" style="grid-column: 1 / -1;">
                    <div class="card-header"><h3 class="card-title" style="font-size: 14px;">Monthly Revenue vs Profit</h3></div>
                    <div class="card-body" style="padding: 12px;"><canvas ref="ownerChartLine" style="max-height: 240px;"></canvas></div>
                  </div>
                </template>
              </div>

              <!-- Download row -->
              <div class="card">
                <div class="card-body" style="display: flex; gap: 12px; flex-wrap: wrap; align-items: center;">
                  <button v-if="ownerAnalyticsView.hasCsv" class="btn btn-outline" @click="ownerDownloadReport(ownerAnalyticsView.reportId, 'csv')">
                    📥 Download CSV
                  </button>
                  <button v-if="ownerAnalyticsView.hasPdf" class="btn btn-primary" @click="ownerDownloadReport(ownerAnalyticsView.reportId, 'pdf')">
                    📄 Download PDF
                  </button>
                </div>
              </div>
            </template>
          </template>

          <!-- ── Reports list (default) ──────────────────────────────── -->
          <template v-else>
            <div class="card">
              <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
                <h3 class="card-title">📄 Shared Reports from Manager</h3>
                <button class="btn btn-outline" style="font-size: 12px; padding: 5px 14px;" @click="fetchOwnerReports">
                  ↻ Refresh
                </button>
              </div>
              <div class="card-body">
                <!-- Loading -->
                <div v-if="ownerReportsLoading" style="text-align: center; padding: 32px; color: #8B7355;">
                  Loading reports…
                </div>

                <!-- Empty -->
                <div v-else-if="ownerReports.length === 0" style="text-align: center; padding: 32px;">
                  <div style="font-size: 40px; margin-bottom: 12px;">📭</div>
                  <div style="color: #8B7355; font-size: 14px;">No reports shared by the manager yet.</div>
                  <div style="color: #8B7355; font-size: 12px; margin-top: 6px;">Reports appear here when the manager clicks "Send to Owner" in the Reports section.</div>
                </div>

                <!-- Reports list -->
                <div v-else>
                  <div
                    v-for="report in ownerReports"
                    :key="report.id"
                    style="display: flex; align-items: center; gap: 14px; padding: 12px 10px; border-radius: 8px; border: 1px solid #e8e0d5; margin-bottom: 8px; background: white; transition: background 0.15s;"
                    @mouseenter="$event.currentTarget.style.background='#f9f5f0'"
                    @mouseleave="$event.currentTarget.style.background='white'"
                  >
                    <div style="font-size: 26px; flex-shrink: 0;">
                      {{ ownerReportIcons[report.report_type] || '📄' }}
                    </div>
                    <div style="flex: 1; min-width: 0;">
                      <div style="font-weight: 700; font-size: 14px; color: #2D2D2D;">
                        {{ report.report_type.charAt(0).toUpperCase() + report.report_type.slice(1) }} Report
                        <span style="margin-left: 6px; font-size: 10px; background: #e6f4ea; color: #276749; padding: 1px 8px; border-radius: 10px; font-weight: 600;">Shared</span>
                      </div>
                      <div style="font-size: 12px; color: #8B7355; margin-top: 3px;">
                        {{ ownerPeriodLabels[report.time_period] || report.time_period }}
                        &bull;
                        {{ new Date(report.created_at).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }) }}
                      </div>
                    </div>
                    <div style="display: flex; gap: 8px; flex-shrink: 0;">
                      <button
                        class="btn btn-primary"
                        style="font-size: 12px; padding: 5px 12px;"
                        @click="openOwnerAnalytics(report)"
                      >
                        📊 View Analytics
                      </button>
                      <button
                        v-if="report.has_csv"
                        class="btn btn-outline"
                        style="font-size: 12px; padding: 5px 12px;"
                        @click="ownerDownloadReport(report.id, 'csv')"
                      >
                        📥 CSV
                      </button>
                      <button
                        v-if="report.has_pdf"
                        class="btn btn-outline"
                        style="font-size: 12px; padding: 5px 12px;"
                        @click="ownerDownloadReport(report.id, 'pdf')"
                      >
                        📄 PDF
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Error -->
                <div v-if="ownerReportsError" style="color: #e53e3e; font-size: 13px; margin-top: 8px;">
                  ⚠️ {{ ownerReportsError }}
                </div>
              </div>
            </div>
          </template>
        </div>

        <!-- PROFILE VIEW -->
        <div v-if="currentView === 'profile'" class="fade-in">
          <div class="card" style="max-width: 600px; margin: 0 auto">
            <div class="card-header" style="text-align: center">
              <div style="width: 80px; height: 80px; background: linear-gradient(135deg, var(--gold), var(--charcoal)); border-radius: 50%; margin: 0 auto 16px; display: flex; align-items: center; justify-content: center; font-size: 36px">
                👑
              </div>
              <h3 class="card-title">Owner Profile</h3>
            </div>
            <div class="card-body">
              <div style="display: grid; gap: 16px">
                <div class="profile-field">
                  <label class="profile-label">Full Name</label>
                  <input type="text" :value="ownerData.ownerName" readonly class="form-input" style="background: var(--light-bg)"/>
                </div>

                <div class="profile-field">
                  <label class="profile-label">Email Address</label>
                  <input type="email" :value="ownerProfile.email" readonly class="form-input" style="background: var(--light-bg)"/>
                </div>

                <div class="profile-field">
                  <label class="profile-label">Phone Number</label>
                  <input type="tel" :value="ownerProfile.phone" readonly class="form-input" style="background: var(--light-bg)"/>
                </div>

                <div class="profile-field">
                  <label class="profile-label">Date of Birth</label>
                  <input type="date" :value="ownerProfile.dob" readonly class="form-input" style="background: var(--light-bg)"/>
                </div>

                <div class="profile-field">
                  <label class="profile-label">Business Registration Date</label>
                  <input type="date" :value="ownerProfile.registrationDate" readonly class="form-input" style="background: var(--light-bg)"/>
                </div>

                <div class="profile-field">
                  <label class="profile-label">Business Address</label>
                  <textarea readonly class="form-input" style="background: var(--light-bg); height: 80px">{{ ownerProfile.address }}</textarea>
                </div>

                <div class="profile-field">
                  <label class="profile-label">Account Status</label>
                  <div style="display: flex; align-items: center; gap: 8px">
                    <span class="badge badge-success">{{ ownerProfile.status }}</span>
                    <span class="text-muted">Since {{ ownerProfile.registrationDate }}</span>
                  </div>
                </div>

                <hr style="border: none; border-top: 1px solid var(--border); margin: 16px 0"/>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px">
                  <button class="btn btn-secondary" @click="currentView = 'overview'">← Back to Overview</button>
                  <button class="btn btn-primary" @click="showChangePasswordModal = true">🔑 Change Password</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- MANAGERS VIEW -->
        <div v-if="currentView === 'managers'" class="fade-in">
          <!-- Managers Grid View -->
          <div v-if="managers.length > 0" style="margin-bottom: 40px">
            <h3 style="font-size: 20px; font-weight: 600; color: var(--text); margin-bottom: 24px">All Managers</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px">
              <div v-for="manager in managers" :key="manager.id" style="background: var(--surface); border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid var(--border); transition: all 0.3s ease">
                
                <!-- Branch/Manager Header -->
                <div style="margin-bottom: 18px; padding-bottom: 14px; border-bottom: 1px solid var(--divider)">
                  <h4 style="font-family: var(--font-display); font-size: 16px; font-weight: 600; color: var(--gold-deep); margin: 0 0 8px 0">{{ manager.branchName }}</h4>
                  <p style="font-size: 12px; color: var(--text-muted); margin: 0">📍 {{ manager.role }}</p>
                </div>

                <!-- Manager Info -->
                <div style="margin-bottom: 16px">
                  <div style="font-size: 11px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px">Manager</div>
                  <div style="font-size: 14px; font-weight: 500; color: var(--gold-deep)">{{ manager.name }}</div>
                </div>

                <!-- Contact -->
                <div style="margin-bottom: 16px; padding: 12px; background: var(--ivory-warm); border-radius: 8px">
                  <div style="font-size: 11px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px">Contact</div>
                  <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px">
                    <span style="font-size: 12px; color: var(--text)">📞</span>
                    <span style="font-size: 12px; color: var(--text)">{{ manager.phone }}</span>
                  </div>
                  <div style="display: flex; align-items: center; gap: 8px">
                    <span style="font-size: 12px; color: var(--text)">📧</span>
                    <span style="font-size: 12px; color: var(--text-muted)">{{ manager.email }}</span>
                  </div>
                </div>

                <!-- Stats -->
                <div style="margin-bottom: 16px; padding: 12px; background: var(--ivory-warm); border-radius: 8px">
                  <div style="font-size: 11px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px">Stats</div>
                  <div style="display: flex; gap: 12px; flex-wrap: wrap">
                    <div style="display: flex; align-items: center; gap: 6px">
                      <span style="font-size: 12px">👥</span>
                      <span style="font-size: 12px; font-weight: 600; color: var(--text)">{{ getManagerStats(manager.id).customers }} Customers</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 6px">
                      <span style="font-size: 12px">📅</span>
                      <span style="font-size: 12px; font-weight: 600; color: var(--text)">{{ getManagerStats(manager.id).bookings }} Bookings</span>
                    </div>
                  </div>
                  <div style="display: flex; align-items: center; gap: 6px; margin-top: 8px">
                    <span style="font-size: 12px">💰</span>
                    <span style="font-size: 12px; font-weight: 600; color: var(--text)">₹{{ getManagerStats(manager.id).revenue }} Revenue</span>
                  </div>
                </div>

                <!-- Status & Actions -->
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px">
                  <span style="display: inline-block; background: #e8f5e9; color: #2e7d32; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 600">✓ Active</span>
                </div>
                <div style="display: flex; gap: 10px">
                  <button @click="deleteManager(manager.id)" style="flex: 1; padding: 10px 16px; background: #e74c3c; color: white; border: none; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.3s" @mouseenter="$event.target.style.backgroundColor='#c0392b'" @mouseleave="$event.target.style.backgroundColor='#e74c3c'">
                    🗑 Delete
                  </button>
                </div>

              </div>
            </div>
          </div>
          <div v-else style="margin-bottom: 40px; text-align: center; padding: 40px; background: var(--ivory-warm); border-radius: 12px">
            <div style="font-size: 32px; margin-bottom: 8px">👥</div>
            <div style="font-size: 14px; font-weight: 500; color: var(--text)">No Managers Yet</div>
            <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px">Create a manager below to get started</div>
          </div>

          <div class="card" style="margin-bottom: 24px">
            <div class="card-header">
              <h3 class="card-title">Create New Manager</h3>
              <p class="manager-form-subtitle">Fill in manager details and assign the manager to a branch.</p>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleCreateManager" class="manager-form">
                <div class="manager-form-layout">
                  <section class="manager-form-section">
                    <h4 class="manager-section-title">Profile</h4>
                    <div class="manager-form-grid">
                      <div class="manager-form-item">
                        <label class="manager-form-label">Full Name *</label>
                        <input v-model="newManagerForm.name" type="text" placeholder="Enter manager name" class="form-input" required />
                      </div>

                      <div class="manager-form-item">
                        <label class="manager-form-label">Email *</label>
                        <input v-model="newManagerForm.email" type="email" placeholder="Enter email address" class="form-input" required />
                      </div>

                      <div class="manager-form-item">
                        <label class="manager-form-label">Phone *</label>
                        <input v-model="newManagerForm.phone" type="tel" placeholder="Enter phone number" class="form-input" required />
                      </div>

                      <div class="manager-form-item">
                        <label class="manager-form-label">Date of Birth *</label>
                        <input v-model="newManagerForm.dob" type="date" class="form-input" required />
                      </div>
                    </div>
                  </section>

                  <section class="manager-form-section">
                    <h4 class="manager-section-title">Employment</h4>
                    <div class="manager-form-grid">
                      <div class="manager-form-item">
                        <label class="manager-form-label">Role *</label>
                        <input v-model="newManagerForm.role" type="text" placeholder="Enter role" class="form-input" required />
                      </div>

                      <div class="manager-form-item">
                        <label class="manager-form-label">Assign to Branch *</label>
                        <input v-model="newManagerForm.branchName" type="text" placeholder="Enter branch name" class="form-input" required />
                      </div>

                      <div class="manager-form-item manager-form-item-full">
                        <label class="manager-form-label">Skills *</label>
                        <input v-model="newManagerForm.skills" type="text" placeholder="Enter skills (e.g., Hair Styling, Team Management)" class="form-input" required />
                        <span class="manager-form-hint">Use commas to separate multiple skills.</span>
                      </div>

                      <div class="manager-form-item">
                        <label class="manager-form-label">Date of Joining *</label>
                        <input v-model="newManagerForm.doj" type="date" class="form-input" required />
                      </div>
                    </div>
                  </section>

                  <section class="manager-form-section">
                    <h4 class="manager-section-title">Account Access</h4>
                    <div class="manager-form-grid">
                      <div class="manager-form-item">
                        <label class="manager-form-label">Username *</label>
                        <input v-model="newManagerForm.userId" type="text" placeholder="Enter username" class="form-input" required />
                      </div>

                      <div class="manager-form-item">
                        <label class="manager-form-label">Password *</label>
                        <div style="position: relative; display: flex; align-items: center">
                          <input v-model="newManagerForm.password" :type="showManagerPassword ? 'text' : 'password'" placeholder="Enter password" class="form-input" required />
                          <button type="button" @click="showManagerPassword = !showManagerPassword" style="position: absolute; right: 12px; background: none; border: none; cursor: pointer; font-size: 18px; color: var(--text-muted); padding: 4px">
                            {{ showManagerPassword ? '👁️' : '👁️‍🗨️' }}
                          </button>
                        </div>
                        <span class="manager-form-hint">Minimum 8 characters.</span>
                      </div>
                    </div>
                  </section>
                </div>

                <div v-if="managerError" class="manager-form-error">
                  {{ managerError }}
                </div>
                <div v-if="managerSuccess" class="manager-form-success">
                  {{ managerSuccess }}
                </div>

                <div class="manager-form-actions">
                  <button type="submit" class="btn btn-primary manager-form-btn">Create Manager</button>
                  <button type="button" class="btn btn-secondary manager-form-btn" @click="resetManagerForm">Clear Form</button>
                </div>
              </form>
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
</template>

<script>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);
import { useRouter } from 'vue-router';
import { useAppStore } from '@/stores/appStore';

export default {
  name: 'OwnerDashboard',
  setup() {
    const router = useRouter();
    const appStore = useAppStore();
    const API_BASE_URL = 'http://localhost:5000';
    const currentView = ref('overview');

    const ownerData = ref({
      ownerName: appStore.user?.username || "Glow Suite Owner",
      bookings: [
        { id: 1, customerId: 1, amount: 500, date: "2026-03-05" },
        { id: 2, customerId: 2, amount: 750, date: "2026-03-06" },
        { id: 3, customerId: 3, amount: 600, date: "2026-03-07" },
        { id: 4, customerId: 1, amount: 450, date: "2026-03-08" },
        { id: 5, customerId: 4, amount: 800, date: "2026-03-09" }
      ],
      customers: [
        { id: 1, name: "Alice Johnson" },
        { id: 2, name: "Bob Williams" },
        { id: 3, name: "Carol Smith" },
        { id: 4, name: "Diana Prince" }
      ]
    });

    const ownerProfile = ref({
      email: "owner@glowsuite.com",
      phone: "+91-9876543200",
      dob: "1985-08-20",
      registrationDate: "2023-06-01",
      address: "123 Beauty Street, Salon Complex\nCity Center\nState, 560001",
      status: "Active"
    });

    const totalRevenue = computed(() => {
      return ownerData.value.bookings.reduce((sum, booking) => sum + booking.amount, 0);
    });

    const totalBookings = computed(() => {
      return ownerData.value.bookings.length;
    });

    const totalCustomers = computed(() => {
      return ownerData.value.customers.length;
    });

    const hoveredBar = ref(null);

    const avgRevenuePerBooking = computed(() => {
      if (totalBookings.value === 0) return 0;
      return Math.round(totalRevenue.value / totalBookings.value);
    });

    const overallPerformance = computed(() => {
      // Calculate performance based on bookings and revenue
      const bookingScore = Math.min((totalBookings.value / 10) * 100, 100);
      const revenueScore = Math.min((totalRevenue.value / 5000) * 100, 100);
      return Math.round((bookingScore + revenueScore) / 2);
    });

    const businessHealth = computed(() => {
      const score = overallPerformance.value;
      if (score >= 85) return 'Excellent';
      if (score >= 70) return 'Good';
      if (score >= 50) return 'Fair';
      return 'Needs Improvement';
    });

    const businessHealthColor = computed(() => {
      const score = overallPerformance.value;
      if (score >= 85) return '#22c55e';
      if (score >= 70) return '#3b82f6';
      if (score >= 50) return '#f59e0b';
      return '#ef4444';
    });

    const getStatusBadgeClass = (status) => {
      const baseClasses = ['badge'];
      if (status === 'active') {
        baseClasses.push('badge-success');
      } else if (status === 'inactive') {
        baseClasses.push('badge-danger');
      } else {
        baseClasses.push('badge-warning');
      }
      return baseClasses;
    };

    const handleLogout = () => {
      appStore.logout();
      router.push('/');
    };

    // ── Shared Reports ──────────────────────────────────────────────────────
    const ownerReports        = ref([]);
    const ownerReportsLoading = ref(false);
    const ownerReportsError   = ref('');

    const ownerReportIcons = {
      sales: '📊', appointments: '📅', staff: '👥',
      inventory: '📦', financial: '💰', feedback: '⭐',
    };
    const ownerPeriodLabels = {
      daily: 'Today', yesterday: 'Yesterday', weekly: 'This Week',
      monthly: 'This Month', custom: 'Custom Range',
    };

    const fetchOwnerReports = async () => {
      ownerReportsLoading.value = true;
      ownerReportsError.value   = '';
      const token = localStorage.getItem('authToken');
      if (!token) { ownerReportsLoading.value = false; return; }
      try {
        const res = await fetch(`${API_BASE_URL}/reports`, {
          headers: { Authorization: `Bearer ${token}`, 'Authentication-Token': token },
        });
        if (!res.ok) throw new Error('Failed to load reports');
        ownerReports.value = await res.json();
      } catch (err) {
        ownerReportsError.value = err.message || 'Could not load reports.';
      } finally {
        ownerReportsLoading.value = false;
      }
    };

    const ownerDownloadReport = async (reportId, format) => {
      const token = localStorage.getItem('authToken');
      try {
        const res = await fetch(`${API_BASE_URL}/reports/${reportId}/download?format=${format}`, {
          headers: { Authorization: `Bearer ${token}`, 'Authentication-Token': token },
        });
        if (!res.ok) throw new Error('Download failed');
        const blob = await res.blob();
        const url  = URL.createObjectURL(blob);
        const a    = document.createElement('a');
        a.href     = url;
        a.download = `report_${reportId}.${format}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(() => URL.revokeObjectURL(url), 2000);
      } catch (err) {
        ownerReportsError.value = err.message || 'Download failed.';
      }
    };

    // ── Owner Analytics View ────────────────────────────────────────────────
    const ownerAnalyticsView    = ref(null);   // { type, title, icon, periodLabel }
    const ownerAnalyticsData    = ref(null);
    const ownerAnalyticsLoading = ref(false);
    const ownerAnalyticsError   = ref('');

    // Chart.js canvas refs
    const ownerChartLine = ref(null);
    const ownerChartBar  = ref(null);
    const ownerChartPie  = ref(null);
    let _ownerLineInst = null, _ownerBarInst = null, _ownerPieInst = null;

    const OWNER_CHART_COLORS = [
      '#d4af37','#8B6914','#3b82f6','#22c55e','#f59e0b',
      '#ef4444','#a855f7','#06b6d4','#ec4899','#84cc16',
    ];

    const _ownerDestroyCharts = () => {
      if (_ownerLineInst) { _ownerLineInst.destroy(); _ownerLineInst = null; }
      if (_ownerBarInst)  { _ownerBarInst.destroy();  _ownerBarInst  = null; }
      if (_ownerPieInst)  { _ownerPieInst.destroy();  _ownerPieInst  = null; }
    };

    const _ownerRenderCharts = () => {
      _ownerDestroyCharts();
      if (!ownerAnalyticsData.value || !ownerAnalyticsView.value) return;
      const type = ownerAnalyticsView.value.type;
      const data = ownerAnalyticsData.value;
      const def  = { responsive: true, maintainAspectRatio: true, plugins: { legend: { position: 'bottom', labels: { font: { size: 11 } } } } };

      if (type === 'appointments') {
        if (ownerChartLine.value && data.by_day?.length)
          _ownerLineInst = new Chart(ownerChartLine.value, { type: 'line', data: { labels: data.by_day.map(d => d.date), datasets: [{ label: 'Appointments', data: data.by_day.map(d => d.count), borderColor: '#d4af37', backgroundColor: 'rgba(212,175,55,0.15)', tension: 0.35, fill: true, pointRadius: 4 }] }, options: { ...def, scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } } } });
        if (ownerChartBar.value && data.top_services?.length)
          _ownerBarInst = new Chart(ownerChartBar.value, { type: 'bar', data: { labels: data.top_services.map(s => s.name), datasets: [{ label: 'Bookings', data: data.top_services.map(s => s.count), backgroundColor: OWNER_CHART_COLORS }] }, options: { ...def, plugins: { ...def.plugins, legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } } } });
        if (ownerChartPie.value && data.by_status?.length)
          _ownerPieInst = new Chart(ownerChartPie.value, { type: 'pie', data: { labels: data.by_status.map(s => s.name), datasets: [{ data: data.by_status.map(s => s.value), backgroundColor: OWNER_CHART_COLORS }] }, options: def });

      } else if (type === 'sales') {
        if (ownerChartLine.value && data.by_day?.length)
          _ownerLineInst = new Chart(ownerChartLine.value, { type: 'line', data: { labels: data.by_day.map(d => d.date), datasets: [{ label: 'Revenue (INR)', data: data.by_day.map(d => d.revenue), borderColor: '#22c55e', backgroundColor: 'rgba(34,197,94,0.12)', tension: 0.35, fill: true, pointRadius: 4 }] }, options: { ...def, scales: { y: { beginAtZero: true } } } });
        if (ownerChartBar.value && data.by_service?.length)
          _ownerBarInst = new Chart(ownerChartBar.value, { type: 'bar', data: { labels: data.by_service.map(s => s.name), datasets: [{ label: 'Revenue (INR)', data: data.by_service.map(s => s.revenue), backgroundColor: OWNER_CHART_COLORS }] }, options: { ...def, plugins: { ...def.plugins, legend: { display: false } }, scales: { y: { beginAtZero: true } } } });

      } else if (type === 'staff') {
        if (ownerChartBar.value && data.staff?.length)
          _ownerBarInst = new Chart(ownerChartBar.value, { type: 'bar', data: { labels: data.staff.map(s => s.name), datasets: [{ label: 'Total', data: data.staff.map(s => s.total), backgroundColor: 'rgba(212,175,55,0.7)' }, { label: 'Completed', data: data.staff.map(s => s.completed), backgroundColor: 'rgba(34,197,94,0.7)' }] }, options: { ...def, scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } } } });
        if (ownerChartLine.value && data.staff?.length)
          _ownerLineInst = new Chart(ownerChartLine.value, { type: 'bar', data: { labels: data.staff.map(s => s.name), datasets: [{ label: 'Avg Rating', data: data.staff.map(s => s.rating), backgroundColor: OWNER_CHART_COLORS, borderRadius: 6 }] }, options: { ...def, plugins: { ...def.plugins, legend: { display: false } }, scales: { y: { beginAtZero: true, max: 5, ticks: { stepSize: 1 } } } } });

      } else if (type === 'inventory') {
        if (ownerChartBar.value && data.items?.length)
          _ownerBarInst = new Chart(ownerChartBar.value, { type: 'bar', data: { labels: data.items.map(i => i.name), datasets: [{ label: 'Current Stock', data: data.items.map(i => i.current), backgroundColor: 'rgba(59,130,246,0.7)' }, { label: 'Min Required', data: data.items.map(i => i.minimum), backgroundColor: 'rgba(239,68,68,0.6)' }] }, options: { ...def, scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } } } });

      } else if (type === 'feedback') {
        if (ownerChartBar.value && data.by_rating?.length)
          _ownerBarInst = new Chart(ownerChartBar.value, { type: 'bar', data: { labels: data.by_rating.map(r => `${r.rating} Star${r.rating !== 1 ? 's' : ''}`), datasets: [{ label: 'Reviews', data: data.by_rating.map(r => r.count), backgroundColor: ['#ef4444','#f97316','#f59e0b','#84cc16','#22c55e'] }] }, options: { ...def, plugins: { ...def.plugins, legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } } } });
        if (ownerChartPie.value && data.sentiment?.length)
          _ownerPieInst = new Chart(ownerChartPie.value, { type: 'doughnut', data: { labels: data.sentiment.map(s => s.name), datasets: [{ data: data.sentiment.map(s => s.value), backgroundColor: ['#22c55e','#f59e0b','#ef4444'] }] }, options: def });

      } else if (type === 'financial') {
        if (ownerChartLine.value && data.months?.length)
          _ownerLineInst = new Chart(ownerChartLine.value, { type: 'line', data: { labels: data.months.map(m => m.month), datasets: [{ label: 'Revenue', data: data.months.map(m => m.revenue), borderColor: '#22c55e', backgroundColor: 'rgba(34,197,94,0.1)', tension: 0.35, fill: true }, { label: 'Cost', data: data.months.map(m => m.cost), borderColor: '#ef4444', backgroundColor: 'rgba(239,68,68,0.07)', tension: 0.35 }, { label: 'Profit', data: data.months.map(m => m.profit), borderColor: '#d4af37', backgroundColor: 'rgba(212,175,55,0.12)', tension: 0.35, fill: true }] }, options: { ...def, scales: { y: { beginAtZero: true } } } });
      }
    };

    watch(ownerAnalyticsData, () => { nextTick(_ownerRenderCharts); });

    const OWNER_PERIOD_LABELS = {
      daily: 'Today', yesterday: 'Yesterday', weekly: 'This Week',
      monthly: 'This Month', custom: 'Custom Range',
    };

    const openOwnerAnalytics = async (report) => {
      _ownerDestroyCharts();
      ownerAnalyticsView.value = {
        type:        report.report_type,
        title:       report.report_type.charAt(0).toUpperCase() + report.report_type.slice(1) + ' Report',
        icon:        ownerReportIcons[report.report_type] || '📄',
        periodLabel: OWNER_PERIOD_LABELS[report.time_period] || report.time_period,
        reportId:    report.id,
        hasCsv:      report.has_csv,
        hasPdf:      report.has_pdf,
      };
      ownerAnalyticsData.value    = null;
      ownerAnalyticsLoading.value = true;
      ownerAnalyticsError.value   = '';
      const token = localStorage.getItem('authToken');
      try {
        const params = new URLSearchParams({ type: report.report_type, period: report.time_period });
        const res = await fetch(`${API_BASE_URL}/reports/analytics?${params}`, {
          headers: { Authorization: `Bearer ${token}`, 'Authentication-Token': token },
        });
        if (!res.ok) throw new Error('Analytics fetch failed');
        ownerAnalyticsData.value = await res.json();
      } catch (err) {
        ownerAnalyticsError.value = err.message || 'Failed to load analytics.';
      } finally {
        ownerAnalyticsLoading.value = false;
      }
    };

    const closeOwnerAnalytics = () => {
      _ownerDestroyCharts();
      ownerAnalyticsView.value = null;
      ownerAnalyticsData.value = null;
      ownerAnalyticsError.value = '';
    };

    onUnmounted(_ownerDestroyCharts);

    onMounted(() => {
      fetchOwnerReports();
      fetchManagers();
    });

    // Manager management
    const managers = ref([]);
    
    const fetchManagers = async () => {
      const token = localStorage.getItem('authToken');
      if (!token) return;

      try {
        const response = await fetch(`${API_BASE_URL}/api/manager`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': token,
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          // Map API response to component structure
          managers.value = data.map(manager => ({
            id: manager.manager_id,
            name: manager.manager_name,
            email: manager.manager_email,
            phone: manager.manager_contact,
            skills: manager.manager_skills,
            role: manager.manager_role,
            dob: manager.manager_dob,
            doj: manager.manager_doj,
            branchName: manager.branch_name,
          }));
        }
      } catch (error) {
        console.error('Failed to fetch managers:', error);
      }
    };
    const newManagerForm = ref({
      name: '',
      email: '',
      phone: '',
      skills: '',
      role: '',
      dob: '',
      doj: '',
      branchName: '',
      userId: '',
      password: ''
    });

    const managerError = ref('');
    const managerSuccess = ref('');

    const handleCreateManager = async () => {
      managerError.value = '';
      managerSuccess.value = '';

      if (!newManagerForm.value.name || !newManagerForm.value.email || !newManagerForm.value.phone || 
          !newManagerForm.value.skills || !newManagerForm.value.role || !newManagerForm.value.dob || !newManagerForm.value.doj ||
          !newManagerForm.value.branchName || !newManagerForm.value.userId || !newManagerForm.value.password) {
        managerError.value = 'All fields are required';
        return;
      }

      if (newManagerForm.value.password.length < 8) {
        managerError.value = 'Password must be at least 8 characters';
        return;
      }

      const token = localStorage.getItem('authToken');
      if (!token) {
        managerError.value = 'You are not authenticated. Please log in again.';
        return;
      }

      try {
        const response = await fetch(`${API_BASE_URL}/api/create-manager`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': token,
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            fullname: newManagerForm.value.name,
            email: newManagerForm.value.email,
            phone: newManagerForm.value.phone,
            skills: newManagerForm.value.skills,
            role: newManagerForm.value.role,
            dob: newManagerForm.value.dob,
            doj: newManagerForm.value.doj,
            branch_name: newManagerForm.value.branchName,
            username: newManagerForm.value.userId,
            password: newManagerForm.value.password,
          }),
        });

        const data = await response.json();
        if (!response.ok) {
          managerError.value = data.message || 'Failed to create manager';
          return;
        }

        managers.value.push({
          id: managers.value.length + 1,
          name: newManagerForm.value.name,
          email: newManagerForm.value.email,
          phone: newManagerForm.value.phone,
          skills: newManagerForm.value.skills,
          role: newManagerForm.value.role,
          dob: newManagerForm.value.dob,
          doj: newManagerForm.value.doj,
          branchName: newManagerForm.value.branchName,
          userId: newManagerForm.value.userId,
          createdDate: new Date().toISOString().split('T')[0],
        });

        managerSuccess.value = data.message || `Manager "${newManagerForm.value.name}" created successfully!`;
        resetManagerForm();
        fetchManagers(); // Refresh the managers list
        setTimeout(() => { managerSuccess.value = ''; }, 3000);
      } catch (error) {
        managerError.value = 'Unable to connect to server. Please try again.';
      }
    };

    const resetManagerForm = () => {
      newManagerForm.value = {
        name: '',
        email: '',
        phone: '',
        skills: '',
        role: '',
        dob: '',
        doj: '',
        branchName: '',
        userId: '',
        password: ''
      };
    };

    const deleteManager = async (managerId) => {
      if (confirm('Are you sure you want to delete this manager?')) {
        const token = localStorage.getItem('authToken');
        if (!token) {
          alert('You are not authenticated. Please log in again.');
          return;
        }

        try {
          const response = await fetch(`${API_BASE_URL}/api/manager/${managerId}`, {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
              'Authentication-Token': token,
              Authorization: `Bearer ${token}`,
            },
          });

          if (response.ok) {
            managers.value = managers.value.filter(m => m.id !== managerId);
            alert('Manager deleted successfully');
          } else {
            const data = await response.json();
            alert(data.message || 'Failed to delete manager');
          }
        } catch (error) {
          alert('Unable to delete manager. Please try again.');
        }
      }
    };

    const getManagerStats = (managerId) => {
      // Calculate stats for this manager
      // In a real application, you would fetch this from the API
      // For now, return placeholder stats
      return {
        customers: Math.floor(Math.random() * 100) + 10,
        bookings: Math.floor(Math.random() * 200) + 20,
        revenue: Math.floor(Math.random() * 50000) + 5000,
      };
    };

    const getManagerBranch = (branchName) => {
      // Manager branch name is directly available from the manager object
      return branchName || 'Unassigned';
    };

    // Change password
    const showChangePasswordModal = ref(false);
    const showManagerPassword = ref(false);
    const showCurrentPassword = ref(false);
    const showNewPassword = ref(false);
    const showConfirmPassword = ref(false);
    const passwordForm = ref({
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    });
    const passwordError = ref('');
    const passwordSuccess = ref('');

    const handleChangePassword = async () => {
      passwordError.value = '';
      passwordSuccess.value = '';

      if (!passwordForm.value.currentPassword) {
        passwordError.value = 'Current password is required';
        return;
      }

      if (!passwordForm.value.newPassword) {
        passwordError.value = 'New password is required';
        return;
      }

      if (passwordForm.value.newPassword.length < 8) {
        passwordError.value = 'New password must be at least 8 characters';
        return;
      }

      if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
        passwordError.value = 'Passwords do not match';
        return;
      }

      if (passwordForm.value.currentPassword === passwordForm.value.newPassword) {
        passwordError.value = 'New password must be different from current password';
        return;
      }

      const token = localStorage.getItem('authToken');
      if (!token) {
        passwordError.value = 'You are not authenticated. Please log in again.';
        return;
      }

      try {
        const response = await fetch(`${API_BASE_URL}/api/change-password`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
            'Authentication-Token': token,
          },
          body: JSON.stringify({
            current_password: passwordForm.value.currentPassword,
            new_password: passwordForm.value.newPassword,
            confirm_password: passwordForm.value.confirmPassword,
          }),
        });

        const data = await response.json();
        if (!response.ok) {
          passwordError.value = data.message || 'Failed to change password';
          return;
        }

        passwordSuccess.value = data.message || 'Password changed successfully!';
        setTimeout(() => {
          passwordForm.value = {
            currentPassword: '',
            newPassword: '',
            confirmPassword: ''
          };
          passwordSuccess.value = '';
          showChangePasswordModal.value = false;
        }, 1500);
      } catch (error) {
        passwordError.value = 'Unable to connect to server. Please try again.';
      }
    };

    return {
      currentView,
      ownerData,
      ownerProfile,
      totalRevenue,
      totalBookings,
      totalCustomers,
      hoveredBar,
      avgRevenuePerBooking,
      overallPerformance,
      businessHealth,
      businessHealthColor,
      getStatusBadgeClass,
      handleLogout,
      managers,
      newManagerForm,
      managerError,
      managerSuccess,
      handleCreateManager,
      deleteManager,
      getManagerBranch,
      fetchManagers,
      getManagerStats,
      resetManagerForm,
      showChangePasswordModal,
      showManagerPassword,
      showCurrentPassword,
      showNewPassword,
      showConfirmPassword,
      passwordForm,
      passwordError,
      passwordSuccess,
      handleChangePassword,
      ownerReports,
      ownerReportsLoading,
      ownerReportsError,
      ownerReportIcons,
      ownerPeriodLabels,
      fetchOwnerReports,
      ownerDownloadReport,
      ownerAnalyticsView,
      ownerAnalyticsData,
      ownerAnalyticsLoading,
      ownerAnalyticsError,
      ownerChartLine,
      ownerChartBar,
      ownerChartPie,
      openOwnerAnalytics,
      closeOwnerAnalytics,
    };
  }
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

:root {
  --gold: #d4af37;
  --bg: #f6f2e9;
  --card-bg: #fffaf0;
  --text: #2f2a23;
  --border: #d9cfbf;
  --light-bg: #efe7d8;
  --success: #4caf50;
  --danger: #f44336;
  --warning: #ff9800;
  --info: #2196f3;
  --radius: 8px;
}

.dashboard-container {
  display: flex;
  height: 100vh;
  background-color: var(--bg);
  color: var(--text);
}

.dashboard-sidebar {
  width: 280px;
  background-color: var(--card-bg);
  border-right: 1px solid var(--border);
  padding: 20px;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.3);
}

.sidebar-header {
  margin-bottom: 30px;
}

.sidebar-menu {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-item {
  padding: 12px 16px;
  border-radius: var(--radius);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--text);
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
  background-color: transparent;
}

.nav-item:hover {
  background-color: var(--light-bg);
  border-left-color: var(--gold);
}

.nav-item.active {
  background-color: var(--light-bg);
  border-left-color: var(--gold);
  color: var(--gold);
}

.nav-icon {
  font-size: 18px;
}

.sidebar-footer {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.dashboard-main {
  flex: 1;
  overflow-y: auto;
  padding: 30px;
}

.content-wrap {
  max-width: 1200px;
  margin: 0 auto;
}

.fade-in {
  animation: fadeIn 0.3s ease;
}

.change-password-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
}

.change-password-modal {
  background: #f8f6ef;
  color: #2f2f2f;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 400px;
  padding: 24px;
  border: 1px solid #ddd5c6;
}

.change-password-modal .form-input {
  background-color: #fff;
  border-color: #d7d1c2;
  color: #2f2f2f;
}

.change-password-modal .btn-secondary {
  background-color: #f1ece0;
  color: #2f2f2f;
  border-color: #d7d1c2;
}

.change-password-modal .btn-secondary:hover {
  background-color: #e8e1d2;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background-color: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.stat-card:hover {
  border-color: var(--gold);
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.2);
}

.stat-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.stat-label {
  color: #6f675a;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: var(--gold);
}

.card {
  background-color: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.card-header {
  padding: 20px;
  border-bottom: 1px solid var(--border);
  background-color: rgba(212, 175, 55, 0.05);
}

.card-title {
  margin: 0;
  color: var(--gold);
  font-size: 18px;
}

.card-body {
  padding: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 8px;
  color: var(--text);
  font-weight: 500;
}

.form-input {
  padding: 10px 12px;
  background-color: var(--light-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text);
  font-size: 14px;
  transition: all 0.3s ease;
}

.form-input::placeholder {
  color: #746a5c;
  opacity: 1;
}

.form-input:focus {
  outline: none;
  border-color: var(--gold);
  box-shadow: 0 0 8px rgba(212, 175, 55, 0.3);
}

.manager-form-subtitle {
  margin: 8px 0 0;
  color: #6f675a;
  font-size: 13px;
}

.manager-form {
  max-width: 900px;
}

.manager-form-layout {
  display: grid;
  gap: 16px;
}

.manager-form-section {
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 14px;
  background: linear-gradient(180deg, rgba(255, 252, 246, 0.92), rgba(249, 241, 227, 0.96));
}

.manager-section-title {
  margin: 0 0 10px;
  font-size: 14px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: #8a6a1f;
}

.manager-form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px 16px;
}

.manager-form-item {
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(120, 102, 70, 0.18);
  border-radius: 10px;
  padding: 12px;
}

.manager-form-item-full {
  grid-column: span 2;
}

.manager-form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  font-size: 13px;
  color: #3a332a;
}

.manager-form-hint {
  display: block;
  margin-top: 6px;
  font-size: 11px;
  color: #7c7261;
}

.manager-form-error {
  color: #ef4444;
  padding: 12px;
  background: rgba(239, 68, 68, 0.1);
  border-radius: 8px;
  margin-top: 14px;
}

.manager-form-success {
  color: #22c55e;
  padding: 12px;
  background: rgba(34, 197, 94, 0.1);
  border-radius: 8px;
  margin-top: 14px;
}

.manager-form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 14px;
  padding-top: 6px;
}

.manager-form-btn {
  min-width: 150px;
}

.error-message {
  background-color: rgba(244, 67, 54, 0.1);
  border-left: 4px solid var(--danger);
  padding: 12px 16px;
  border-radius: var(--radius);
  color: #ff8a8a;
  margin: 12px 0;
}

.success-message {
  background-color: rgba(76, 175, 80, 0.1);
  border-left: 4px solid var(--success);
  padding: 12px 16px;
  border-radius: var(--radius);
  color: #81c784;
  margin: 12px 0;
}

.btn {
  padding: 10px 16px;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  display: inline-block;
  text-align: center;
}

.btn-primary {
  background-color: var(--gold);
  color: #1a1a1a;
}

.btn-primary:hover {
  background-color: #e0c250;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
}

.btn-secondary {
  background-color: var(--light-bg);
  color: var(--text);
  border: 1px solid var(--border);
}

.btn-secondary:hover {
  background-color: var(--border);
}

.w-full {
  width: 100%;
}

.table-wrap {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

table thead {
  background-color: rgba(212, 175, 55, 0.05);
}

table th {
  padding: 12px;
  text-align: left;
  color: var(--gold);
  font-weight: 600;
  border-bottom: 2px solid var(--border);
}

table td {
  padding: 12px;
  border-bottom: 1px solid var(--border);
}

table tbody tr:hover {
  background-color: var(--light-bg);
}

.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.badge-success {
  background-color: rgba(76, 175, 80, 0.2);
  color: #256b2a;
}

.badge-danger {
  background-color: rgba(244, 67, 54, 0.2);
  color: #a3342b;
}

.badge-warning {
  background-color: rgba(255, 152, 0, 0.2);
  color: #9a5b00;
}

.badge-info {
  background-color: rgba(33, 150, 243, 0.2);
  color: #1f5ea8;
}

.report-item {
  background-color: var(--light-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  text-align: center;
  transition: all 0.3s ease;
}

.report-item:hover {
  border-color: var(--gold);
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.2);
}

.report-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.report-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 8px;
}

.text-muted {
  color: #6f675a;
  font-size: 13px;
}

@media (max-width: 768px) {
  .dashboard-container {
    flex-direction: column;
  }

  .dashboard-sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid var(--border);
  }

  .dashboard-main {
    padding: 20px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .manager-form-grid {
    grid-template-columns: 1fr;
  }

  .manager-form-item-full {
    grid-column: span 1;
  }

  .manager-form-actions {
    flex-direction: column;
  }

  .manager-form-btn {
    width: 100%;
  }
}
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
    border-radius: var(--radius);
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
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: var(--text);
  }

  .modal-close {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    color: var(--text);
    transition: all 0.2s ease;
  }

  .modal-close:hover {
    opacity: 0.7;
  }

  .modal-body {
    padding: 20px;
  }

  .form-group {
    margin-bottom: 16px;
  }

  .form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: 600;
    font-size: 14px;
  }

  .form-hint {
    font-size: 12px;
    color: #6f675a;
    margin-top: 4px;
  }

  .error-message {
    color: #f44336;
    padding: 12px;
    background: rgba(244, 67, 54, 0.1);
    border-radius: 4px;
    font-size: 14px;
    margin: 16px 0;
  }

  .success-message {
    color: #4caf50;
    padding: 12px;
    background: rgba(76, 175, 80, 0.1);
    border-radius: 4px;
    font-size: 14px;
    margin: 16px 0;
  }
</style>