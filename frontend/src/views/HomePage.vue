<template>
  <div class="homepage">
    <!-- Navigation -->
    <nav class="navbar">
      <div class="navbar-container">
        <div class="navbar-logo">
          <span class="logo-icon">✨</span>
          <span class="logo-text">Glow Suite</span>
        </div>
        <div class="navbar-links">
          <a href="#features" class="nav-link">Features</a>
          <a href="#services" class="nav-link">Services</a>
          <a href="#about" class="nav-link">About</a>
          <router-link to="/login/customer" class="nav-link btn btn-primary">Login</router-link>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-background"></div>
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">Welcome to <span class="highlight">Glow Suite</span></h1>
          <p class="hero-subtitle">Transform Your Beauty Salon with Smart Management</p>
          <p class="hero-description">All-in-one platform designed for modern beauty businesses</p>
          <div class="hero-buttons">
            <router-link to="/login/customer" class="btn btn-primary btn-lg">
              Get Started Now
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features">
      <div class="features-container">
        <div class="section-header">
          <h2 class="section-title">Why Choose Glow Suite?</h2>
          <p class="section-subtitle">Everything you need to run your salon efficiently</p>
        </div>
        <div class="features-grid">
          <div class="feature-card" v-for="(feature, index) in features" :key="index">
            <div class="feature-icon-box" :style="{ backgroundColor: feature.color }">
              <div class="feature-icon">{{ feature.icon }}</div>
            </div>
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-description">{{ feature.description }}</p>
            <div class="feature-tick">✓</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Services Section -->
    <section id="services" class="services">
      <div class="services-container">
        <div class="section-header">
          <h2 class="section-title">Built for Everyone</h2>
          <p class="section-subtitle">Tailored solutions for each role in your salon</p>
        </div>
        <div class="services-grid">
          <div class="service-card" v-for="(service, index) in services" :key="index">
            <div class="service-header">
              <div class="service-icon">{{ service.icon }}</div>
              <h3>{{ service.title }}</h3>
            </div>
            <p class="service-description">{{ service.description }}</p>
            <ul class="service-features">
              <li v-for="(feature, idx) in service.features" :key="idx">
                <span class="check-icon">✓</span>{{ feature }}
              </li>
            </ul>
            <a href="#" class="service-link">Learn more →</a>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta">
      <div class="cta-container">
        <h2 class="cta-title">Ready to Transform Your Salon?</h2>
        <p class="cta-subtitle">Join hundreds of successful salons already using Glow Suite</p>
        <router-link to="/login/customer" class="btn btn-primary btn-lg">
          Start Free Trial Today
        </router-link>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer" id="about">
      <div class="footer-content">
        <div class="footer-section">
          <h4>Glow Suite</h4>
          <p>Professional beauty salon management system designed for modern businesses.</p>
        </div>
        <div class="footer-section">
          <h4>Quick Links</h4>
          <ul>
            <li><a href="#features">Features</a></li>
            <li><a href="#services">Services</a></li>
            <li><a href="#about">About</a></li>
          </ul>
        </div>
        <div class="footer-section">
          <h4>Contact</h4>
          <p>📧 info@glowsuite.com</p>
          <p>📱 +233 123 456 789</p>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 Glow Suite. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const features = [
  {
    icon: '📅',
    title: 'Smart Scheduling',
    description: 'Effortlessly manage appointments, bookings, and staff schedules with our intuitive calendar system.',
    color: '#E8D5B0'
  },
  {
    icon: '👥',
    title: 'Customer Management',
    description: 'Keep detailed customer profiles, track preferences, and maintain loyalty rewards all in one place.',
    color: '#E8C4C4'
  },
  {
    icon: '💰',
    title: 'Financial Tracking',
    description: 'Monitor revenue, expenses, and profitability with comprehensive financial reports and analytics.',
    color: '#A8B5A0'
  },
  {
    icon: '📦',
    title: 'Inventory Management',
    description: 'Track product stock levels, manage suppliers, and never run out of essential beauty products.',
    color: '#D4CDBE'
  },
  {
    icon: '👔',
    title: 'Staff Administration',
    description: 'Manage staff profiles, track attendance, and monitor performance with detailed analytics.',
    color: '#E0D5C7'
  },
  {
    icon: '📊',
    title: 'Advanced Analytics',
    description: 'Get insights into business performance with detailed reports and data-driven recommendations.',
    color: '#E8D5B0'
  }
];

const services = [
  {
    icon: '🏢',
    title: 'For Managers',
    description: 'Complete business management dashboard with analytics, staff coordination, and financial insights.',
    features: ['Full System Control', 'Financial Reports', 'Staff Management', 'Inventory Tracking']
  },
  {
    icon: '👩‍💼',
    title: 'For Staff',
    description: 'Manage your schedule, track orders, and view your performance metrics in real-time.',
    features: ['Schedule Management', 'Appointment Tracking', 'Order Management', 'Attendance Logs']
  },
  {
    icon: '🎀',
    title: 'For Customers',
    description: 'Book appointments, browse services, and manage your beauty journey with ease.',
    features: ['Easy Booking', 'Service Browsing', 'Appointment History', 'Loyalty Rewards']
  }
];

const stats = [
  { icon: '🏆', value: '500+', label: 'Happy Salons' },
  { icon: '👥', value: '10K+', label: 'Active Users' },
  { icon: '⏱️', value: '99.9%', label: 'Uptime' },
  { icon: '🌍', value: '50+', label: 'Countries' }
];

const testimonials = [
  {
    rating: 5,
    text: 'Glow Suite transformed how we manage our salon. The system is intuitive and saves us hours every week!',
    author: 'Sarah Johnson',
    role: 'Salon Owner',
    avatar: '👩‍💼'
  },
  {
    rating: 5,
    text: 'Managing staff attendance and appointments has never been easier. Highly recommended!',
    author: 'Maria Garcia',
    role: 'Manager',
    avatar: '👩‍💻'
  },
  {
    rating: 5,
    text: 'The customer interface is beautiful and easy to use. My clients love booking through the app!',
    author: 'Jessica Lee',
    role: 'Director',
    avatar: '👩‍🦰'
  }
];
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.homepage {
  font-family: 'Segoe UI', 'Roboto', sans-serif;
  color: #333;
  background: #fff;
}

/* Navigation */
.navbar {
  background: rgba(220, 205, 190, 0.98);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.08);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 100%;
}

.navbar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 24px;
  font-weight: 800;
  background: linear-gradient(135deg, #C9A96E, #8B6914);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  flex-shrink: 0;
  white-space: nowrap;
  font-family: var(--font-display);
  margin-right: auto;
}

.logo-icon {
  font-size: 28px;
  animation: sparkle 0.6s ease-in-out infinite;
}

@keyframes sparkle {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}

.navbar-links {
  display: flex;
  gap: 32px;
  align-items: center;
  margin-left: auto;
}

.nav-link {
  color: var(--charcoal);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
  font-family: var(--font-body);
}

.nav-link:not(.btn):hover {
  color: var(--gold);
}

.nav-link:not(.btn)::after {
  content: '';
  position: absolute;
  bottom: -6px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--gold);
  transition: width 0.3s ease;
}

.nav-link:not(.btn):hover::after {
  width: 100%;
}

/* Hero Section */
.hero {
  position: relative;
  overflow: hidden;
  min-height: 600px;
  display: flex;
  align-items: center;
  padding: 60px 24px;
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, var(--ivory) 0%, var(--cream) 50%, var(--ivory) 100%);
  z-index: -1;
}

.hero {
  position: relative;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-text {
  display: flex;
  flex-direction: column;
  gap: 20px;
  z-index: 2;
}

.hero-title {
  font-size: 56px;
  font-weight: 800;
  line-height: 1.2;
  color: var(--charcoal);
  font-family: var(--font-display);
}

.highlight {
  background: linear-gradient(135deg, #C9A96E, #8B6914);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 24px;
  color: var(--charcoal-light);
  font-weight: 600;
  font-family: var(--font-display);
}

.hero-description {
  font-size: 16px;
  color: var(--text-muted);
  line-height: 1.6;
  font-family: var(--font-body);
}

.hero-buttons {
  display: flex;
  gap: 16px;
  margin-top: 24px;
  flex-wrap: wrap;
}

.btn {
  padding: 14px 28px;
  border-radius: 12px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  font-size: 16px;
}

.btn-primary {
  background: linear-gradient(135deg, #C9A96E, #8B6914);
  color: white;
  box-shadow: 0 4px 20px rgba(201, 169, 110, 0.3);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(201, 169, 110, 0.5);
}

.btn-outline {
  border: 2px solid var(--gold);
  color: var(--gold);
  background: transparent;
}

.btn-outline:hover {
  background: var(--gold);
  color: white;
}

.btn-lg {
  padding: 16px 32px;
  font-size: 18px;
}

.btn-icon {
  font-size: 20px;
}

.hero-stats {
  display: flex;
  gap: 40px;
  margin-top: 20px;
}

.stat-item {
  text-align: left;
}

.stat-number {
  font-size: 28px;
  font-weight: 800;
  background: linear-gradient(135deg, #C9A96E, #8B6914);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  font-size: 14px;
  color: var(--text-muted);
  margin-top: 4px;
}

.hero-visual {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
}

.hero-graphic {
  font-size: 200px;
  animation: float 3s ease-in-out infinite;
}

.floating-icons {
  position: absolute;
  width: 100%;
  height: 100%;
}

.float-icon {
  position: absolute;
  font-size: 60px;
  animation: float-around 6s ease-in-out infinite;
}

.float-icon:nth-child(1) {
  top: 20px;
  right: 40px;
  animation-delay: 0s;
}

.float-icon:nth-child(2) {
  bottom: 60px;
  right: 20px;
  animation-delay: 0.5s;
}

.float-icon:nth-child(3) {
  top: 50%;
  left: 30px;
  animation-delay: 1s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

@keyframes float-around {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  25% { transform: translate(20px, -20px) rotate(90deg); }
  50% { transform: translate(0, -40px) rotate(180deg); }
  75% { transform: translate(-20px, -20px) rotate(270deg); }
}

/* Features Section */
.features {
  padding: 100px 24px;
  background: var(--cream);
}

.features-container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 60px;
}

.section-title {
  font-size: 44px;
  font-weight: 800;
  color: var(--charcoal);
  margin-bottom: 12px;
  font-family: var(--font-display);
}

.section-subtitle {
  font-size: 18px;
  color: var(--text-muted);
  font-family: var(--font-body);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 32px;
}

.feature-card {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #C9A96E, #8B6914);
}

.feature-icon-box {
  width: 70px;
  height: 70px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  font-size: 32px;
}

.feature-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--charcoal);
  margin-bottom: 12px;
  font-family: var(--font-display);
}

.feature-description {
  font-size: 14px;
  color: var(--text-muted);
  line-height: 1.6;
  font-family: var(--font-body);
}

.feature-tick {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 30px;
  height: 30px;
  background: linear-gradient(135deg, #C9A96E, #8B6914);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  opacity: 0.8;
}

/* Services Section */
.services {
  padding: 100px 24px;
  background: white;
}

.services-container {
  max-width: 1200px;
  margin: 0 auto;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 32px;
  margin-top: 60px;
}

.service-card {
  background: linear-gradient(135deg, #fff9f5 0%, #fff5e6 100%);
  padding: 40px;
  border-radius: 16px;
  border: 2px solid #ffe5cc;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.service-card:hover {
  border-color: var(--gold);
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(201, 169, 110, 0.2);
}

.service-card::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(201, 169, 110, 0.1), transparent);
  border-radius: 50%;
  animation: pulse 4s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}

.service-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
  position: relative;
  z-index: 1;
}

.service-icon {
  font-size: 48px;
}

.service-card h3 {
  font-size: 24px;
  font-weight: 700;
  color: var(--charcoal);
  font-family: var(--font-display);
}

.service-description {
  font-size: 15px;
  color: var(--text-muted);
  margin: 16px 0;
  line-height: 1.6;
  position: relative;
  z-index: 1;
  font-family: var(--font-body);
}

.service-features {
  list-style: none;
  margin: 24px 0;
  position: relative;
  z-index: 1;
}

.service-features li {
  padding: 10px 0;
  color: var(--charcoal-light);
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-family: var(--font-body);
}

.check-icon {
  color: var(--gold);
  font-weight: bold;
  font-size: 18px;
}

.service-link {
  color: var(--gold);
  text-decoration: none;
  font-weight: 600;
  position: relative;
  z-index: 1;
  display: inline-block;
  transition: all 0.3s ease;
}

.service-link:hover {
  gap: 8px;
}

/* Stats Section */
.stats-section {
  padding: 80px 24px;
  background: linear-gradient(135deg, #d4af37, #f5a623);
  color: white;
}

.stats-container {
  max-width: 1200px;
  margin: 0 auto;
}

.stats-section .section-title {
  color: white;
  margin-bottom: 60px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 40px;
}

.stat-card {
  text-align: center;
}

.stat-icon {
  font-size: 56px;
  margin-bottom: 16px;
}

.stat-value {
  font-size: 48px;
  font-weight: 800;
  margin-bottom: 8px;
}

.stat-text {
  font-size: 16px;
  opacity: 0.9;
}

/* Testimonials Section */
.testimonials {
  padding: 100px 24px;
  background: #fafafa;
}

.testimonials-container {
  max-width: 1200px;
  margin: 0 auto;
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 32px;
  margin-top: 60px;
}

.testimonial-card {
  background: white;
  padding: 32px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.testimonial-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.stars {
  margin-bottom: 16px;
  font-size: 20px;
}

.testimonial-text {
  font-size: 15px;
  color: #666;
  line-height: 1.7;
  margin-bottom: 24px;
  font-style: italic;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 12px;
}

.author-avatar {
  font-size: 40px;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #C9A96E, #8B6914);
  display: flex;
  align-items: center;
  justify-content: center;
}

.author-name {
  font-weight: 600;
  color: var(--charcoal);
  font-family: var(--font-display);
}

.author-role {
  font-size: 13px;
  color: var(--text-muted);
  font-family: var(--font-body);
}

/* CTA Section */
.cta {
  padding: 80px 24px;
  background: linear-gradient(135deg, var(--charcoal), var(--charcoal-mid));
  color: white;
  text-align: center;
}

.cta-container {
  max-width: 600px;
  margin: 0 auto;
}

.cta-title {
  font-size: 44px;
  font-weight: 800;
  margin-bottom: 12px;
  font-family: var(--font-display);
}

.cta-subtitle {
  font-size: 18px;
  margin-bottom: 32px;
  opacity: 0.9;
}

/* Footer */
.footer {
  background: var(--charcoal);
  color: var(--text-muted);
  padding: 60px 24px 24px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px;
  margin-bottom: 40px;
}

.footer-section h4 {
  color: white;
  font-size: 16px;
  font-weight: 700;
  font-family: var(--font-display);
  margin-bottom: 16px;
}

.footer-section p {
  font-size: 14px;
  line-height: 1.7;
  font-family: var(--font-body);
  margin-bottom: 8px;
}

.footer-section ul {
  list-style: none;
}

.footer-section a {
  color: var(--text-muted);
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s;
}

.footer-section a:hover {
  color: var(--gold);
}

.footer-bottom {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
  padding-top: 24px;
  border-top: 1px solid rgba(201, 169, 110, 0.2);
  font-size: 13px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .navbar-container {
    flex-direction: column;
    gap: 16px;
  }

  .navbar-links {
    flex-direction: column;
    width: 100%;
    gap: 12px;
  }

  .hero {
    grid-template-columns: 1fr;
    gap: 30px;
    padding: 40px 24px;
  }

  .hero-title {
    font-size: 36px;
  }

  .hero-subtitle {
    font-size: 18px;
  }

  .hero-buttons {
    flex-direction: column;
  }

  .hero-visual {
    height: 300px;
  }

  .hero-graphic {
    font-size: 120px;
  }

  .section-title {
    font-size: 32px;
  }

  .cta-title {
    font-size: 28px;
  }

  .features-grid,
  .services-grid,
  .testimonials-grid {
    grid-template-columns: 1fr;
  }
}
</style>
