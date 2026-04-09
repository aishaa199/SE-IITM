<template>
  <div class="homepage">

    <!-- ─── NAVBAR ─────────────────────────────────────────────── -->
    <nav class="navbar">
      <div class="navbar-logo">
        <span class="logo-icon">✦</span>
        <span class="logo-text">Glow Suite</span>
      </div>
      <div class="navbar-links">
        <a href="#features" class="nav-link">Services</a>
        <a href="#about"    class="nav-link">About</a>
        <a href="#contact"  class="nav-link">Contact</a>
        <router-link to="/login/customer" class="nav-link btn btn-gold" style="color: #000000;">
          Start Now
        </router-link>
      </div>
    </nav>

    <!-- ─── HERO ───────────────────────────────────────────────── -->
    <section class="hero-section">
      <div class="hero-bg-lines"></div>

      <!-- Decorative circles -->
      <div class="hero-visual">
        <div class="hero-visual-inner"></div>
        <div class="hero-circle-large"></div>
        <div class="hero-circle-small"></div>
      </div>


      <div class="hero-content">
        <div class="hero-eyebrow">
          <span class="hero-eyebrow-line"></span>
          Luxury Beauty Management
          <span class="hero-eyebrow-line"></span>
        </div>

        <h1 class="hero-title">
          Where Beauty<br>
          Meets <em>Precision</em>
        </h1>

        <p class="hero-subtitle">
          A complete salon management experience crafted for discerning 
          beauty professionals. Elegant, intuitive, and effortlessly powerful.
        </p>

        <div class="hero-cta">
          <router-link to="/login/customer" class="btn btn-gold btn-lg">
            Begin Your Journey
          </router-link>
          <a href="#features" class="btn btn-ghost" style="color: rgba(255,255,255,0.5); font-size: 12px; letter-spacing: 0.12em">
            Discover More ↓
          </a>
        </div>
      </div>


      <div class="hero-scroll">
        <span>Scroll</span>
        <div class="hero-scroll-line"></div>
      </div>
    </section>

    <!-- ─── MARQUEE ────────────────────────────────────────────── -->
    <div class="marquee-strip">
      <div class="marquee-track">
        <span v-for="item in marqueeItems" :key="item" class="marquee-item">
          {{ item }} <span class="marquee-dot">✦</span>
        </span>
        <!-- Duplicate for seamless loop -->
        <span v-for="item in marqueeItems" :key="'dup-'+item" class="marquee-item" aria-hidden="true">
          {{ item }} <span class="marquee-dot">✦</span>
        </span>
      </div>
    </div>

    <!-- ─── FEATURES ───────────────────────────────────────────── -->
    <section id="features" class="section section-dark">
      <div class="section-header">
        <span class="eyebrow">Why Choose Glow Suite</span>
        <h2 class="section-title" style="color: var(--ivory)">
          Everything Your Salon<br><em style="font-style:italic; color: var(--gold-pale)">Deserves</em>
        </h2>
        <p class="section-subtitle" style="color: rgba(255,255,255,0.4)">
          From appointment booking to financial analytics — a complete ecosystem 
          designed with the precision of a master craftsperson.
        </p>
      </div>

      <div class="features-grid">
        <div
          v-for="(feature, i) in features"
          :key="feature.title"
          class="feature-card"
          :style="{ animationDelay: i * 80 + 'ms' }"
        >
          <div class="feature-icon-box">{{ feature.icon }}</div>
          <h3 class="feature-title">{{ feature.title }}</h3>
          <p class="feature-description">{{ feature.description }}</p>
        </div>
      </div>
    </section>

    <!-- ─── ROLES ──────────────────────────────────────────────── -->
    <section id="about" class="section" style="background: var(--obsidian); padding-top: 80px; padding-bottom: 100px">
      <div class="section-header centered" style="max-width: 640px; margin: 0 auto 60px">
        <span class="eyebrow">Built for Every Role</span>
        <h2 class="section-title" style="color: var(--ivory)">
          One Platform,<br><em style="font-style:italic; color: var(--gold-pale)">Infinite Possibility</em>
        </h2>
      </div>

      <div class="services-grid-home">
        <div
          v-for="(role, i) in roles"
          :key="role.title"
          class="service-card-home"
          :style="{ animationDelay: i * 120 + 'ms' }"
        >
          <span class="service-icon">{{ role.icon }}</span>
          <h3>{{ role.title }}</h3>
          <p class="service-description">{{ role.description }}</p>
          <ul class="service-features">
            <li v-for="f in role.features" :key="f">
              <span class="check-icon">✦</span> {{ f }}
            </li>
          </ul>
          <router-link :to="role.link" class="btn btn-outline" style="font-size: 10px; border-color: rgba(201,169,110,0.3); color: rgba(255,255,255,0.5); width: 100%; margin-top: auto">
            Enter Portal →
          </router-link>
        </div>
      </div>
    </section>


    <!-- ─── CTA ────────────────────────────────────────────────── -->
    <section class="cta-section" id="contact">
      <div class="cta-deco-left"></div>
      <div class="cta-deco-right"></div>
      <span class="eyebrow" style="display: block; margin-bottom: 18px">Begin Today</span>
      <h2 class="cta-title">Ready to Elevate<br><em style="font-style: italic">Your Salon?</em></h2>
      <p class="cta-subtitle">Join hundreds of luxury salons already running on Glow Suite.</p>
      <div style="display: flex; gap: 16px; justify-content: center; flex-wrap: wrap">
        <router-link to="/login/customer" class="btn btn-gold btn-lg">Start Free Trial</router-link>
        <router-link to="/login/manager"  class="btn btn-outline" style="border-color: rgba(201,169,110,0.35); color: rgba(255,255,255,0.55); padding: 15px 36px; font-size: 13px">
          Manager Login
        </router-link>
      </div>
    </section>

    <!-- ─── FOOTER ──────────────────────────────────────────────── -->
    <footer class="footer" id="contact">
      <div class="footer-content">
        <div class="footer-section">
          <div style="font-family: var(--font-display); font-size: 26px; font-style: italic; color: var(--gold-pale); margin-bottom: 14px">
            Glow Suite
          </div>
          <p>
            Professional beauty salon management crafted for those who demand 
            more than the ordinary.
          </p>
          <div class="footer-social">
            <span>📸</span><span>💼</span><span>🐦</span>
          </div>
        </div>

        <div class="footer-section">
          <h4>Navigate</h4>
          <ul>
            <li><a href="#features">Features</a></li>
            <li><a href="#about">About</a></li>
            <li><router-link to="/login/customer">Customer Portal</router-link></li>
            <li><router-link to="/login/manager">Manager Portal</router-link></li>
            <li><router-link to="/login/staff">Staff Portal</router-link></li>
            <li><router-link to="/login/owner">Owner Portal</router-link></li>
          </ul>
        </div>

        <div class="footer-section">
          <h4>Contact</h4>
          <p>Email</p>
          <p>Phone Number</p>
        </div>
      </div>

      <div class="footer-bottom">
        <p>© 2026 Glow Suite. Crafted with intention. All rights reserved.</p>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const marqueeItems = [
  'Smart Scheduling', 'Luxury Experience', 'AI Insights',
  'Customer Loyalty', 'Staff Management', 'Financial Analytics',
  'Inventory Control', 'Premium Design',
]

const features = [
  { icon: '◐', title: 'Smart Scheduling',     description: 'Effortlessly manage appointments with an intelligent calendar that anticipates your needs.' },
  { icon: '◆', title: 'Customer Loyalty',     description: 'Reward your most valued clients with our sophisticated points and VIP membership system.' },
  { icon: '◎', title: 'AI-Powered Insights',  description: 'Your personal AI briefing each morning — recommendations, alerts, and daily priorities.' },
  { icon: '◈', title: 'Financial Clarity',    description: 'Real-time revenue tracking, expense management, and profit analytics in one elegant view.' },
  { icon: '▢', title: 'Inventory Mastery',    description: 'Never run short of your finest products with automated stock alerts and supplier management.' },
  { icon: '◉', title: 'Team Excellence',      description: 'Curate your staff, track performance, and cultivate an exceptional service culture.' },
]

const roles = [
  {
    icon: '◆',
    title: 'For Owners',
    description: 'A birds-eye view of your empire. Track KPIs, review manager reports, and steer your vision.',
    link: '/login/owner',
    features: ['Business Analytics', 'Manager Oversight', 'Shared Reports', 'Revenue Trends'],
  },
  {
    icon: '◐',
    title: 'For Managers',
    description: 'The command center. Coordinate staff, serve customers, and run operations with precision.',
    link: '/login/manager',
    features: ['Full Appointment Control', 'Staff Scheduling', 'Inventory & Orders', 'AI Daily Briefing'],
  },
  {
    icon: '◈',
    title: 'For Staff',
    description: 'Streamlined tools to deliver exceptional service and track your daily performance.',
    link: '/login/staff',
    features: ['View Appointments', 'Track Performance', 'Service Notes', 'Attendance Management'],
  },
  {
    icon: '◉',
    title: 'For Customers',
    description: 'A seamless, luxurious booking experience that keeps clients coming back.',
    link: '/login/customer',
    features: ['Easy Online Booking', 'Service Discovery', 'Loyalty Rewards', 'AI Beauty Assistant'],
  },
]
</script>

<style scoped>
/* ─── SCROLL ─── */
.hero-scroll {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  position: absolute;
  bottom: 40px;
  left: 60px;
  color: rgba(255,255,255,0.2);
  font-size: 8.5px;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  animation: float 2.5s ease-in-out infinite;
}

.hero-scroll-line {
  width: 1px;
  height: 48px;
  background: linear-gradient(to bottom, rgba(201,169,110,0.4), transparent);
}

/* ─── MARQUEE ─── */
.marquee-strip {
  background: rgba(201,169,110,0.08);
  border-top: 1px solid rgba(201,169,110,0.12);
  border-bottom: 1px solid rgba(201,169,110,0.12);
  padding: 16px 0;
  overflow: hidden;
}

.marquee-track {
  display: flex;
  width: max-content;
  animation: marquee 28s linear infinite;
}

@keyframes marquee {
  from { transform: translateX(0); }
  to   { transform: translateX(-50%); }
}

.marquee-item {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: rgba(201,169,110,0.55);
  padding: 0 28px;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 8px;
}

.marquee-dot { color: var(--gold); font-size: 8px; }

/* ─── CTA DECORATIVE ─── */
.cta-deco-left, .cta-deco-right {
  position: absolute;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  border: 1px solid rgba(201,169,110,0.08);
}

.cta-deco-left  { bottom: -100px; left: -100px; }
.cta-deco-right { top: -100px;   right: -100px; }

/* ─── FOOTER SOCIAL ─── */
.footer-social {
  display: flex;
  gap: 14px;
  margin-top: 20px;
  font-size: 18px;
  opacity: 0.4;
  cursor: pointer;
}

.footer-social span:hover { opacity: 1; }

/* ─── RESPONSIVE ─── */
@media (max-width: 768px) {
  .hero-stats { gap: 20px; }
  .testimonial-section { padding: 60px 24px; }
  .marquee-item { padding: 0 20px; }
}
</style>