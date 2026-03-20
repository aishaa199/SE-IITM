<template>
  <div class="dashboard-container">
    <!-- Sidebar Navigation -->
    <div class="dashboard-sidebar">
      <div class="sidebar-header">
        <h2 style="color: var(--gold); font-size: 24px; margin: 0">👑 Owner Hub</h2>
        <p style="color: #999; margin: 8px 0 0 0; font-size: 12px">{{ ownerData.ownerName }}</p>
      </div>

      <div class="sidebar-menu">
        <div
          :class="['nav-item', { active: currentView === 'overview' }]"
          @click="currentView = 'overview'"
        >
          <span class="nav-icon">📊</span> Overview
        </div>

        <div
          :class="['nav-item', { active: currentView === 'branches' }]"
          @click="currentView = 'branches'"
        >
          <span class="nav-icon">🏢</span> Branches ({{ ownerData.branches.length }})
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
          <span class="nav-icon">📄</span> Download Reports
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
              <div class="stat-icon">🏢</div>
              <div class="stat-label">Total Branches</div>
              <div class="stat-value">{{ ownerData.branches.length }}</div>
            </div>
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
            </div>
            <div class="stat-card">
              <div class="stat-icon">📈</div>
              <div class="stat-label">Avg Customers/Branch</div>
              <div class="stat-value">{{ avgCustomersPerBranch }}</div>
            </div>
            <div class="stat-card">
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
                    <div style="font-size: 12px; color: #999">Total</div>
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
                    <div v-if="hoveredBar === 'mon'" style="position: absolute; top: -35px; left: 50%; transform: translateX(-50%); background: var(--gold); color: var(--bg); padding: 8px 16px; border-radius: 4px; font-weight: 700; white-space: nowrap; font-size: 14px">₹500</div>
                  </div>
                  <div style="font-weight: 700">Mon</div>
                  <div style="font-size: 12px; color: #999">₹500</div>
                </div>

                <!-- Tuesday -->
                <div style="display: flex; flex-direction: column; align-items: center; gap: 12px">
                  <div style="width: 60px; height: 200px; background: linear-gradient(180deg, #d4af37 0%, #b89e2c 100%); border-radius: 6px 6px 0 0; box-shadow: 0 8px 16px rgba(212, 175, 55, 0.3); position: relative"
                    @mouseenter="hoveredBar = 'tue'" @mouseleave="hoveredBar = null">
                    <div v-if="hoveredBar === 'tue'" style="position: absolute; top: -35px; left: 50%; transform: translateX(-50%); background: var(--gold); color: var(--bg); padding: 8px 16px; border-radius: 4px; font-weight: 700; white-space: nowrap; font-size: 14px">₹750</div>
                  </div>
                  <div style="font-weight: 700">Tue</div>
                  <div style="font-size: 12px; color: #999">₹750</div>
                </div>

                <!-- Wednesday -->
                <div style="display: flex; flex-direction: column; align-items: center; gap: 12px">
                  <div style="width: 60px; height: 180px; background: linear-gradient(180deg, #d4af37 0%, #b89e2c 100%); border-radius: 6px 6px 0 0; box-shadow: 0 8px 16px rgba(212, 175, 55, 0.3); position: relative"
                    @mouseenter="hoveredBar = 'wed'" @mouseleave="hoveredBar = null">
                    <div v-if="hoveredBar === 'wed'" style="position: absolute; top: -35px; left: 50%; transform: translateX(-50%); background: var(--gold); color: var(--bg); padding: 8px 16px; border-radius: 4px; font-weight: 700; white-space: nowrap; font-size: 14px">₹600</div>
                  </div>
                  <div style="font-weight: 700">Wed</div>
                  <div style="font-size: 12px; color: #999">₹600</div>
                </div>

                <!-- Thursday -->
                <div style="display: flex; flex-direction: column; align-items: center; gap: 12px">
                  <div style="width: 60px; height: 240px; background: linear-gradient(180deg, #d4af37 0%, #b89e2c 100%); border-radius: 6px 6px 0 0; box-shadow: 0 8px 16px rgba(212, 175, 55, 0.3); position: relative"
                    @mouseenter="hoveredBar = 'thu'" @mouseleave="hoveredBar = null">
                    <div v-if="hoveredBar === 'thu'" style="position: absolute; top: -35px; left: 50%; transform: translateX(-50%); background: var(--gold); color: var(--bg); padding: 8px 16px; border-radius: 4px; font-weight: 700; white-space: nowrap; font-size: 14px">₹800</div>
                  </div>
                  <div style="font-weight: 700">Thu</div>
                  <div style="font-size: 12px; color: #999">₹800</div>
                </div>

                <!-- Friday -->
                <div style="display: flex; flex-direction: column; align-items: center; gap: 12px">
                  <div style="width: 60px; height: 190px; background: linear-gradient(180deg, #d4af37 0%, #b89e2c 100%); border-radius: 6px 6px 0 0; box-shadow: 0 8px 16px rgba(212, 175, 55, 0.3); position: relative"
                    @mouseenter="hoveredBar = 'fri'" @mouseleave="hoveredBar = null">
                    <div v-if="hoveredBar === 'fri'" style="position: absolute; top: -35px; left: 50%; transform: translateX(-50%); background: var(--gold); color: var(--bg); padding: 8px 16px; border-radius: 4px; font-weight: 700; white-space: nowrap; font-size: 14px">₹650</div>
                  </div>
                  <div style="font-weight: 700">Fri</div>
                  <div style="font-size: 12px; color: #999">₹650</div>
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
                    <div v-if="hoveredBar === idx" style="position: absolute; top: -30px; left: 50%; transform: translateX(-50%); background: var(--gold); color: var(--bg); padding: 6px 12px; border-radius: 4px; font-weight: 600; white-space: nowrap; font-size: 14px">₹{{ booking.amount }}</div>
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
                  <div style="padding: 16px; background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.05)); border-radius: 8px; border-left: 5px solid #3b82f6">
                    <div style="display: flex; justify-content: space-between; align-items: center">
                      <span>Customers Per Branch</span>
                      <span style="font-weight: 700; font-size: 18px; color: #3b82f6">{{ avgCustomersPerBranch }}</span>
                    </div>
                    <div class="text-muted" style="font-size: 12px; margin-top: 4px">Optimal distribution</div>
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

        <!-- BRANCHES VIEW -->
        <div v-if="currentView === 'branches'" class="fade-in">
          <!-- Create New Branch Form -->
          <div class="card" style="margin-bottom: 24px; border-left: 5px solid var(--gold)">
            <div class="card-header">
              <h3 class="card-title">➕ Create New Branch</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleCreateBranch">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px">
                  <div>
                    <label style="display: block; margin-bottom: 8px; font-weight: 600">Branch Name *</label>
                    <input 
                      v-model="newBranchForm.name"
                      type="text"
                      placeholder="Enter branch name"
                      class="form-input"
                      required
                    />
                  </div>

                  <div>
                    <label style="display: block; margin-bottom: 8px; font-weight: 600">Location *</label>
                    <input 
                      v-model="newBranchForm.location"
                      type="text"
                      placeholder="Enter branch location"
                      class="form-input"
                      required
                    />
                  </div>

                  <div>
                    <label style="display: block; margin-bottom: 8px; font-weight: 600">Manager Name *</label>
                    <input 
                      v-model="newBranchForm.manager"
                      type="text"
                      placeholder="Enter manager name"
                      class="form-input"
                      required
                    />
                  </div>

                  <div>
                    <label style="display: block; margin-bottom: 8px; font-weight: 600">Phone *</label>
                    <input 
                      v-model="newBranchForm.phone"
                      type="tel"
                      placeholder="Enter phone number"
                      class="form-input"
                      required
                    />
                  </div>

                  <div>
                    <label style="display: block; margin-bottom: 8px; font-weight: 600">Email *</label>
                    <input 
                      v-model="newBranchForm.email"
                      type="email"
                      placeholder="Enter email"
                      class="form-input"
                      required
                    />
                  </div>

                  <div>
                    <label style="display: block; margin-bottom: 8px; font-weight: 600">Status *</label>
                    <select 
                      v-model="newBranchForm.status"
                      class="form-input"
                      required
                    >
                      <option value="active">Active</option>
                      <option value="inactive">Inactive</option>
                    </select>
                  </div>
                </div>

                <div v-if="branchError" style="color: #ef4444; padding: 12px; background: rgba(239, 68, 68, 0.1); border-radius: 8px; margin-top: 16px">
                  {{ branchError }}
                </div>
                <div v-if="branchSuccess" style="color: #22c55e; padding: 12px; background: rgba(34, 197, 94, 0.1); border-radius: 8px; margin-top: 16px">
                  {{ branchSuccess }}
                </div>

                <div style="display: flex; gap: 12px; margin-top: 16px">
                  <button type="submit" class="btn btn-primary">✅ Create Branch</button>
                  <button type="button" class="btn btn-secondary" @click="resetBranchForm">Clear Form</button>
                </div>
              </form>
            </div>
          </div>

          <!-- Edit Branch Form -->
          <div v-if="showEditForm" class="card" style="margin-bottom: 24px; border-left: 5px solid var(--gold)">
            <div class="card-header">
              <h3 class="card-title">✏️ Edit Branch</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleSaveBranch">
                <div class="form-grid">
                  <div class="form-group">
                    <label for="edit-branch-name">Branch Name *</label>
                    <input 
                      id="edit-branch-name"
                      v-model="editForm.name"
                      type="text"
                      placeholder="Enter branch name"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="edit-branch-location">Location *</label>
                    <input 
                      id="edit-branch-location"
                      v-model="editForm.location"
                      type="text"
                      placeholder="Enter branch location"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="edit-branch-manager">Manager Name *</label>
                    <input 
                      id="edit-branch-manager"
                      v-model="editForm.manager"
                      type="text"
                      placeholder="Enter manager name"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="edit-branch-phone">Phone *</label>
                    <input 
                      id="edit-branch-phone"
                      v-model="editForm.phone"
                      type="tel"
                      placeholder="Enter phone number"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="edit-branch-email">Email *</label>
                    <input 
                      id="edit-branch-email"
                      v-model="editForm.email"
                      type="email"
                      placeholder="Enter email"
                      class="form-input"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="edit-branch-status">Status *</label>
                    <select 
                      id="edit-branch-status"
                      v-model="editForm.status"
                      class="form-input"
                      required
                    >
                      <option value="active">Active</option>
                      <option value="inactive">Inactive</option>
                    </select>
                  </div>
                </div>

                <div style="display: flex; gap: 12px; margin-top: 16px">
                  <button type="submit" class="btn btn-primary">💾 Save Changes</button>
                  <button type="button" class="btn btn-secondary" @click="showEditForm = false">Cancel</button>
                </div>
              </form>
            </div>
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px">
            <div v-for="branch in ownerData.branches" :key="branch.id" class="card">
              <div class="card-header" style="display: flex; justify-content: space-between; align-items: center">
                <div>
                  <h3 class="card-title" style="margin: 0">{{ branch.name }}</h3>
                  <p style="margin: 4px 0 0 0; color: #999; font-size: 12px">📍 {{ branch.location }}</p>
                </div>
              </div>
              <div class="card-body">
                <div style="margin-bottom: 16px; padding: 12px; background: var(--light-bg); border-radius: 6px">
                  <div style="font-size: 12px; color: #999; margin-bottom: 4px">Manager</div>
                  <div style="font-weight: 600; color: var(--gold)">{{ branch.manager }}</div>
                </div>

                <div style="margin-bottom: 16px; padding: 12px; background: var(--light-bg); border-radius: 6px">
                  <div style="font-size: 12px; color: #999; margin-bottom: 4px">Contact</div>
                  <div style="font-size: 13px">📞 {{ branch.phone }}</div>
                  <div style="font-size: 13px">✉️ {{ branch.email }}</div>
                </div>

                <div style="margin-bottom: 16px; padding: 12px; background: var(--light-bg); border-radius: 6px">
                  <div style="font-size: 12px; color: #999; margin-bottom: 4px">Stats</div>
                  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 13px">
                    <div>👥 {{ branch.customers }} Customers</div>
                    <div>📅 {{ branch.bookings }} Bookings</div>
                    <div style="grid-column: 1 / -1">💰 ₹{{ branch.revenue }} Revenue</div>
                  </div>
                </div>

                <div style="padding: 12px; background: var(--light-bg); border-radius: 6px; margin-bottom: 12px">
                  <div style="font-size: 12px; color: #999; margin-bottom: 4px">Status</div>
                  <span :class="['badge', branch.status === 'active' ? 'badge-success' : 'badge-danger']">{{ branch.status }}</span>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px">
                  <button class="btn btn-primary" @click="handleEditBranch(branch)" style="font-size: 12px; padding: 8px">✏️ Edit</button>
                  <button class="btn btn-danger" @click="handleDeleteBranch(branch.id)" style="font-size: 12px; padding: 8px">🗑️ Delete</button>
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
              <!-- Branch Selection -->
              <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 24px">
                <label style="font-weight: 600">Select Branch:</label>
                <select v-model.number="selectedBranchId" class="form-input" style="flex: 1; max-width: 300px">
                  <option v-for="branch in ownerData.branches" :key="branch.id" :value="branch.id">
                    {{ branch.name }}
                  </option>
                </select>
              </div>

              <!-- Branch Reports Grid -->
              <div v-if="selectedBranch" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px">
                <div class="report-item">
                  <div class="report-icon">📊</div>
                  <div class="report-title">Sales Report</div>
                  <div class="text-muted" style="margin: 8px 0">Total sales and revenue summary</div>
                  <button class="btn btn-primary w-full">📥 Download CSV</button>
                </div>

                <div class="report-item">
                  <div class="report-icon">📅</div>
                  <div class="report-title">Bookings Report</div>
                  <div class="text-muted" style="margin: 8px 0">All appointments and bookings</div>
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
          <div class="card" style="margin-bottom: 24px">
            <div class="card-header">
              <h3 class="card-title">Create New Manager</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleCreateManager" style="max-width: 600px">
                <div style="display: grid; gap: 16px">
                  <div>
                    <label style="display: block; margin-bottom: 8px; font-weight: 600">Full Name *</label>
                    <input v-model="newManagerForm.name" type="text" placeholder="Enter manager name" class="form-input" required />
                  </div>

                  <div>
                    <label style="display: block; margin-bottom: 8px; font-weight: 600">Email *</label>
                    <input v-model="newManagerForm.email" type="email" placeholder="Enter email address" class="form-input" required />
                  </div>

                  <div>
                    <label style="display: block; margin-bottom: 8px; font-weight: 600">Phone *</label>
                    <input v-model="newManagerForm.phone" type="tel" placeholder="Enter phone number" class="form-input" required />
                  </div>

                  <div>
                    <label style="display: block; margin-bottom: 8px; font-weight: 600">Assign to Branch *</label>
                    <select v-model.number="newManagerForm.branchId" class="form-input" required>
                      <option value="">Select a branch</option>
                      <option v-for="branch in ownerData.branches" :key="branch.id" :value="branch.id">
                        {{ branch.name }}
                      </option>
                    </select>
                  </div>

                  <div>
                    <label style="display: block; margin-bottom: 8px; font-weight: 600">Username *</label>
                    <input v-model="newManagerForm.userId" type="text" placeholder="Enter username" class="form-input" required />
                  </div>

                  <div>
                    <label style="display: block; margin-bottom: 8px; font-weight: 600">Password *</label>
                    <input v-model="newManagerForm.password" type="password" placeholder="Enter password" class="form-input" required />
                  </div>

                  <div v-if="managerError" style="color: #ef4444; padding: 12px; background: rgba(239, 68, 68, 0.1); border-radius: 8px">
                    {{ managerError }}
                  </div>
                  <div v-if="managerSuccess" style="color: #22c55e; padding: 12px; background: rgba(34, 197, 94, 0.1); border-radius: 8px">
                    {{ managerSuccess }}
                  </div>

                  <div style="display: flex; gap: 12px; margin-top: 12px">
                    <button type="submit" class="btn btn-primary">✅ Create Manager</button>
                    <button type="button" class="btn btn-secondary" @click="resetManagerForm">Clear Form</button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Change Password Modal -->
  <div v-if="showChangePasswordModal" style="position: fixed; inset: 0; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 1000; backdrop-filter: blur(4px)" @click="showChangePasswordModal = false">
    <div style="background: var(--card-bg); border-radius: 12px; box-shadow: 0 20px 60px rgba(0,0,0,0.5); width: 100%; max-width: 400px; padding: 24px; border: 1px solid var(--border)" @click.stop>
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px">
        <h3 style="margin: 0; font-size: 20px; font-weight: 600">🔑 Change Password</h3>
        <button @click="showChangePasswordModal = false" style="background: none; border: none; color: var(--text); cursor: pointer; font-size: 24px">✕</button>
      </div>

      <form @submit.prevent="handleChangePassword" style="display: grid; gap: 16px">
        <div>
          <label style="display: block; margin-bottom: 8px; font-weight: 600; font-size: 14px">Current Password</label>
          <input v-model="passwordForm.currentPassword" type="password" placeholder="Enter current password" class="form-input" required />
        </div>

        <div>
          <label style="display: block; margin-bottom: 8px; font-weight: 600; font-size: 14px">New Password</label>
          <input v-model="passwordForm.newPassword" type="password" placeholder="Enter new password" class="form-input" required />
          <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px">At least 8 characters</div>
        </div>

        <div>
          <label style="display: block; margin-bottom: 8px; font-weight: 600; font-size: 14px">Confirm Password</label>
          <input v-model="passwordForm.confirmPassword" type="password" placeholder="Confirm new password" class="form-input" required />
        </div>

        <div v-if="passwordError" style="color: #ef4444; padding: 12px; background: rgba(239, 68, 68, 0.1); border-radius: 8px; font-size: 14px">
          {{ passwordError }}
        </div>

        <div style="display: flex; gap: 12px; margin-top: 12px">
          <button type="submit" class="btn btn-primary" style="flex: 1">Update Password</button>
          <button type="button" class="btn btn-secondary" style="flex: 1" @click="showChangePasswordModal = false">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAppStore } from '@/stores/appStore';

export default {
  name: 'OwnerDashboard',
  setup() {
    const router = useRouter();
    const appStore = useAppStore();
    const currentView = ref('overview');
    const selectedBranchId = ref(1);

    const ownerData = ref({
      ownerName: "Glow Suite Owner",
      branches: [
        {
          id: 1,
          name: "Downtown Branch",
          location: "City Center",
          manager: "Rajesh Kumar",
          phone: "+91-9876543210",
          email: "downtown@glowsuite.com",
          customers: 45,
          bookings: 120,
          revenue: 28500,
          status: "active"
        },
        {
          id: 2,
          name: "Westside Branch",
          location: "Mall Road",
          manager: "Priya Sharma",
          phone: "+91-9876543211",
          email: "westside@glowsuite.com",
          customers: 38,
          bookings: 95,
          revenue: 22500,
          status: "active"
        },
        {
          id: 3,
          name: "North Branch",
          location: "Corporate Plaza",
          manager: "Amit Patel",
          phone: "+91-9876543212",
          email: "north@glowsuite.com",
          customers: 32,
          bookings: 78,
          revenue: 18750,
          status: "active"
        }
      ],
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

    const avgCustomersPerBranch = computed(() => {
      if (ownerData.value.branches.length === 0) return 0;
      return Math.round(totalCustomers.value / ownerData.value.branches.length);
    });

    const overallPerformance = computed(() => {
      const baseScore = 65;
      const revenueBonus = Math.min((totalRevenue.value / 5000) * 20, 20);
      const bookingBonus = Math.min((totalBookings.value / 10) * 10, 10);
      const score = Math.min(baseScore + revenueBonus + bookingBonus, 100);
      return Math.round(score);
    });

    const businessHealth = computed(() => {
      const score = overallPerformance.value;
      if (score >= 85) return '🚀 Excellent';
      if (score >= 70) return '📈 Good';
      if (score >= 50) return '⚖️ Average';
      return '⚠️ Needs Work';
    });

    const businessHealthColor = computed(() => {
      const score = overallPerformance.value;
      if (score >= 85) return '#22c55e';
      if (score >= 70) return '#3b82f6';
      if (score >= 50) return '#f59e0b';
      return '#ef4444';
    });

    // Branch-specific report data
    const selectedBranch = computed(() => {
      return ownerData.value.branches.find(b => b.id === selectedBranchId.value);
    });

    const branchSalesReport = computed(() => {
      if (!selectedBranch.value) return null;
      return {
        totalSales: selectedBranch.value.revenue,
        transactionCount: selectedBranch.value.bookings,
        avgTransactionValue: Math.round(selectedBranch.value.revenue / selectedBranch.value.bookings),
        topService: 'Hair Styling'
      };
    });

    const branchBookingsReport = computed(() => {
      if (!selectedBranch.value) return null;
      return {
        totalBookings: selectedBranch.value.bookings,
        completedBookings: Math.round(selectedBranch.value.bookings * 0.85),
        pendingBookings: Math.round(selectedBranch.value.bookings * 0.1),
        cancelledBookings: Math.round(selectedBranch.value.bookings * 0.05),
        avgBookingValue: Math.round(selectedBranch.value.revenue / selectedBranch.value.bookings)
      };
    });

    const branchStaffReport = computed(() => {
      if (!selectedBranch.value) return null;
      const staffCount = Math.ceil(selectedBranch.value.bookings / 25);
      return {
        totalStaff: staffCount,
        presentToday: Math.round(staffCount * 0.9),
        absentToday: Math.round(staffCount * 0.1),
        avgPerformance: '4.7/5.0',
        topPerformer: 'Amara Osei'
      };
    });

    const branchInventoryReport = computed(() => {
      if (!selectedBranch.value) return null;
      return {
        totalProducts: Math.floor(selectedBranch.value.bookings / 20),
        lowStockItems: Math.floor(selectedBranch.value.bookings / 80),
        totalValue: selectedBranch.value.revenue * 0.15,
        lastUpdated: '2026-03-20'
      };
    });

    const branchFinancialReport = computed(() => {
      if (!selectedBranch.value) return null;
      const revenue = selectedBranch.value.revenue;
      const expenses = revenue * 0.35;
      const profit = revenue - expenses;
      return {
        revenue: revenue,
        expenses: expenses,
        profit: profit,
        profitMargin: Math.round((profit / revenue) * 100),
        growth: '12.5%'
      };
    });

    const branchFeedbackReport = computed(() => {
      if (!selectedBranch.value) return null;
      const totalFeedback = Math.floor(selectedBranch.value.customers * 0.6);
      return {
        totalFeedback: totalFeedback,
        avgRating: '4.8/5.0',
        positiveReviews: Math.round(totalFeedback * 0.85),
        negativeReviews: Math.round(totalFeedback * 0.05),
        neutralReviews: Math.round(totalFeedback * 0.1)
      };
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

    const showEditForm = ref(false);
    const editingBranchId = ref(null);
    const editForm = ref({
      name: "",
      location: "",
      manager: "",
      phone: "",
      email: "",
      status: "active"
    });

    const newBranchForm = ref({
      name: "",
      location: "",
      manager: "",
      phone: "",
      email: "",
      status: "active"
    });

    const branchError = ref('');
    const branchSuccess = ref('');

    const handleCreateBranch = () => {
      branchError.value = '';
      branchSuccess.value = '';

      if (!newBranchForm.value.name || !newBranchForm.value.location || !newBranchForm.value.manager || 
          !newBranchForm.value.phone || !newBranchForm.value.email) {
        branchError.value = 'All fields are required';
        return;
      }

      const newBranch = {
        id: Math.max(...ownerData.value.branches.map(b => b.id), 0) + 1,
        name: newBranchForm.value.name,
        location: newBranchForm.value.location,
        manager: newBranchForm.value.manager,
        phone: newBranchForm.value.phone,
        email: newBranchForm.value.email,
        customers: 0,
        bookings: 0,
        revenue: 0,
        status: newBranchForm.value.status
      };

      ownerData.value.branches.push(newBranch);
      branchSuccess.value = `Branch "${newBranchForm.value.name}" created successfully!`;
      resetBranchForm();
      setTimeout(() => { branchSuccess.value = ''; }, 3000);
    };

    const resetBranchForm = () => {
      newBranchForm.value = {
        name: "",
        location: "",
        manager: "",
        phone: "",
        email: "",
        status: "active"
      };
    };

    const handleEditBranch = (branch) => {
      editingBranchId.value = branch.id;
      editForm.value = {
        name: branch.name,
        location: branch.location,
        manager: branch.manager,
        phone: branch.phone,
        email: branch.email,
        status: branch.status
      };
      showEditForm.value = true;
    };

    const handleSaveBranch = () => {
      if (editingBranchId.value) {
        const branchIndex = ownerData.value.branches.findIndex(b => b.id === editingBranchId.value);
        if (branchIndex !== -1) {
          ownerData.value.branches[branchIndex] = {
            ...ownerData.value.branches[branchIndex],
            name: editForm.value.name,
            location: editForm.value.location,
            manager: editForm.value.manager,
            phone: editForm.value.phone,
            email: editForm.value.email,
            status: editForm.value.status
          };
          showEditForm.value = false;
          editingBranchId.value = null;
        }
      }
    };

    const handleDeleteBranch = (branchId) => {
      if (confirm('Are you sure you want to delete this branch? This action cannot be undone.')) {
        ownerData.value.branches = ownerData.value.branches.filter(b => b.id !== branchId);
      }
    };

    const handleLogout = () => {
      appStore.logout();
      router.push('/');
    };

    // Manager management
    const managers = ref([]);
    const newManagerForm = ref({
      name: '',
      email: '',
      phone: '',
      branchId: '',
      userId: '',
      password: ''
    });

    const managerError = ref('');
    const managerSuccess = ref('');

    const handleCreateManager = () => {
      managerError.value = '';
      managerSuccess.value = '';

      if (!newManagerForm.value.name || !newManagerForm.value.email || !newManagerForm.value.phone || 
          !newManagerForm.value.branchId || !newManagerForm.value.userId || !newManagerForm.value.password) {
        managerError.value = 'All fields are required';
        return;
      }

      if (newManagerForm.value.password.length < 8) {
        managerError.value = 'Password must be at least 8 characters';
        return;
      }

      const newManager = {
        id: managers.value.length + 1,
        name: newManagerForm.value.name,
        email: newManagerForm.value.email,
        phone: newManagerForm.value.phone,
        branchId: newManagerForm.value.branchId,
        userId: newManagerForm.value.userId,
        password: newManagerForm.value.password,
        createdDate: new Date().toISOString().split('T')[0]
      };

      managers.value.push(newManager);
      managerSuccess.value = `Manager "${newManagerForm.value.name}" created successfully!`;
      resetManagerForm();
      setTimeout(() => { managerSuccess.value = ''; }, 3000);
    };

    const resetManagerForm = () => {
      newManagerForm.value = {
        name: '',
        email: '',
        phone: '',
        branchId: '',
        userId: '',
        password: ''
      };
    };

    const deleteManager = (managerId) => {
      if (confirm('Are you sure you want to delete this manager?')) {
        managers.value = managers.value.filter(m => m.id !== managerId);
      }
    };

    const getManagerBranch = (branchId) => {
      const branch = ownerData.value.branches.find(b => b.id === branchId);
      return branch ? branch.name : 'Unknown Branch';
    };

    // Change password
    const showChangePasswordModal = ref(false);
    const passwordForm = ref({
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    });
    const passwordError = ref('');

    const handleChangePassword = () => {
      passwordError.value = '';

      if (!passwordForm.value.currentPassword || !passwordForm.value.newPassword || !passwordForm.value.confirmPassword) {
        passwordError.value = 'All fields are required';
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

      // TODO: Validate current password with backend
      // For now, just show success and close
      alert('Password changed successfully!');
      showChangePasswordModal.value = false;
      passwordForm.value = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      };
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
      avgCustomersPerBranch,
      overallPerformance,
      businessHealth,
      businessHealthColor,
      getStatusBadgeClass,
      showEditForm,
      editForm,
      editingBranchId,
      handleEditBranch,
      handleSaveBranch,
      handleDeleteBranch,
      handleLogout,
      selectedBranchId,
      selectedBranch,
      branchSalesReport,
      branchBookingsReport,
      branchStaffReport,
      branchInventoryReport,
      branchFinancialReport,
      branchFeedbackReport,
      managers,
      newManagerForm,
      managerError,
      managerSuccess,
      handleCreateManager,
      deleteManager,
      getManagerBranch,
      resetManagerForm,
      showChangePasswordModal,
      passwordForm,
      passwordError,
      handleChangePassword,
      newBranchForm,
      branchError,
      branchSuccess,
      handleCreateBranch,
      resetBranchForm
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
  --bg: #1a1a1a;
  --card-bg: #2a2a2a;
  --text: #e0e0e0;
  --border: #444;
  --light-bg: #3a3a3a;
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
  color: #999;
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

.form-input:focus {
  outline: none;
  border-color: var(--gold);
  box-shadow: 0 0 8px rgba(212, 175, 55, 0.3);
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
  color: #81c784;
}

.badge-danger {
  background-color: rgba(244, 67, 54, 0.2);
  color: #ff8a8a;
}

.badge-warning {
  background-color: rgba(255, 152, 0, 0.2);
  color: #ffb74d;
}

.badge-info {
  background-color: rgba(33, 150, 243, 0.2);
  color: #64b5f6;
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
  color: #999;
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
}
</style>
