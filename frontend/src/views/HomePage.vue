<template>
  <div class="homepage" ref="homepage">

    <!-- ─── NAVBAR ─────────────────────────────────────────────── -->
    <nav class="navbar" ref="navbar">
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
        <!-- Sparkles -->
        <div class="sparkle sparkle-1"></div>
        <div class="sparkle sparkle-2"></div>
        <div class="sparkle sparkle-3"></div>
        <div class="sparkle sparkle-4"></div>
      </div>


      <div class="hero-content">
        <div class="hero-eyebrow">
          <span class="hero-eyebrow-line"></span>
          Luxury Beauty Management
          <span class="hero-eyebrow-line"></span>
        </div>

        <h1 class="hero-title">
          <span class="title-word">Where Beauty</span><br>
          <span class="title-word gradient-text">Meets <em>Precision</em></span>
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
          <div class="feature-icon-box glow-icon">{{ feature.icon }}</div>
          <h3 class="feature-title">{{ feature.title }}</h3>
          <p class="feature-description">{{ feature.description }}</p>
          <!-- Shimmer effect -->
          <div class="shimmer"></div>
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
          <span class="service-icon glow-icon">{{ role.icon }}</span>
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
          <!-- Shimmer effect -->
          <div class="shimmer"></div>
        </div>
      </div>
    </section>


    <!-- ─── CTA ────────────────────────────────────────────────── -->
    <section class="cta-section" id="contact">
      <div class="cta-deco-left"></div>
      <div class="cta-deco-right"></div>
      <span class="eyebrow" style="display: block; margin-bottom: 18px">Begin Today</span>
      <h2 class="cta-title">Ready to Elevate<br><em style="font-style: italic">Your Salon?</em></h2>
      <div style="display: flex; gap: 16px; justify-content: center; flex-wrap: wrap">
        <router-link to="/login/customer" class="btn btn-gold btn-lg">Owner Login</router-link>
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
          <p>glowsuite8@gmail.com</p>
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
import { onMounted, onUnmounted, ref } from 'vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const router = useRouter()
const homepage = ref(null)

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

onMounted(() => {
  // Kill any existing ScrollTriggers to prevent conflicts
  ScrollTrigger.getAll().forEach(trigger => trigger.kill())
  
  // ══════════════════════════════════════════════════════════════
  // HERO TITLE - GROWS BIGGER AS YOU SCROLL
  // ══════════════════════════════════════════════════════════════
  const heroTitle = homepage.value?.querySelector('.hero-title')
  if (heroTitle) {
    gsap.fromTo(heroTitle, 
      {
        scale: 0.8,
        opacity: 0,
        y: 60,
      },
      {
        scale: 1.1,
        opacity: 1,
        y: 0,
        duration: 1,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: heroTitle,
          start: 'top 85%',
          end: 'top 35%',
          scrub: 0.8,
          markers: false,
        }
      }
    )
  }

  // ══════════════════════════════════════════════════════════════
  // HERO VISUAL - ZOOM IN EFFECT
  // ══════════════════════════════════════════════════════════════
  const heroVisual = homepage.value?.querySelector('.hero-visual')
  if (heroVisual) {
    gsap.to(heroVisual, {
      scale: 1.3,
      opacity: 0,
      y: 150,
      duration: 1,
      ease: 'power1.inOut',
      scrollTrigger: {
        trigger: '.hero-section',
        start: 'top top',
        end: 'bottom top',
        scrub: 0.6,
        markers: false,
      }
    })
  }

  // ══════════════════════════════════════════════════════════════
  // HERO SUBTITLE - GROWS AND FADES
  // ══════════════════════════════════════════════════════════════
  const heroSubtitle = homepage.value?.querySelector('.hero-subtitle')
  if (heroSubtitle) {
    gsap.fromTo(heroSubtitle,
      {
        scale: 0.85,
        opacity: 0,
        y: 40,
      },
      {
        scale: 1,
        opacity: 1,
        y: 0,
        duration: 0.9,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: heroSubtitle,
          start: 'top 85%',
          end: 'top 40%',
          scrub: 0.8,
          markers: false,
        }
      }
    )
  }

  // ══════════════════════════════════════════════════════════════
  // FEATURE CARDS - ZOOM IN WITH STAGGER
  // ══════════════════════════════════════════════════════════════
  const featureCards = homepage.value?.querySelectorAll('.feature-card')
  if (featureCards && featureCards.length > 0) {
    gsap.fromTo(featureCards,
      {
        opacity: 0,
        scale: 0.75,
        y: 80,
      },
      {
        opacity: 1,
        scale: 1,
        y: 0,
        duration: 0.8,
        stagger: 0.12,
        ease: 'back.out(1.2)',
        scrollTrigger: {
          trigger: '.features-grid',
          start: 'top 70%',
          end: 'top 20%',
          scrub: 1.2,
          markers: false,
        }
      }
    )
  }

  // ══════════════════════════════════════════════════════════════
  // SERVICE CARDS - ZOOM & ROTATE EFFECT
  // ══════════════════════════════════════════════════════════════
  const serviceCards = homepage.value?.querySelectorAll('.service-card-home')
  if (serviceCards && serviceCards.length > 0) {
    serviceCards.forEach((card, index) => {
      gsap.fromTo(card,
        {
          opacity: 0,
          scale: 0.6,
          rotationY: index % 2 === 0 ? -15 : 15,
          y: 100,
        },
        {
          opacity: 1,
          scale: 1,
          rotationY: 0,
          y: 0,
          duration: 0.9,
          delay: index * 0.15,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: '.services-grid-home',
            start: 'top 70%',
            end: 'top 15%',
            scrub: 1,
            markers: false,
          }
        }
      )
    })
  }

  // ══════════════════════════════════════════════════════════════
  // MARQUEE - CONTINUOUS SCROLL (CSS-based, not scroll-triggered)
  // ══════════════════════════════════════════════════════════════
  // Animation is now handled by CSS @keyframes for smooth infinite loop

  // ══════════════════════════════════════════════════════════════
  // SECTION HEADERS - BIG TEXT GROWTH
  // ══════════════════════════════════════════════════════════════
  const sectionHeaders = homepage.value?.querySelectorAll('.section-header')
  if (sectionHeaders && sectionHeaders.length > 0) {
    sectionHeaders.forEach(header => {
      const title = header.querySelector('.section-title')
      if (title) {
        gsap.fromTo(title,
          {
            scale: 0.7,
            opacity: 0,
            y: 50,
          },
          {
            scale: 1,
            opacity: 1,
            y: 0,
            duration: 0.8,
            ease: 'power3.out',
            scrollTrigger: {
              trigger: header,
              start: 'top 75%',
              end: 'top 30%',
              scrub: 1,
              markers: false,
            }
          }
        )
      }

      const eyebrow = header.querySelector('.eyebrow')
      if (eyebrow) {
        gsap.fromTo(eyebrow,
          {
            opacity: 0,
            x: -30,
          },
          {
            opacity: 1,
            x: 0,
            duration: 0.6,
            ease: 'power2.out',
            scrollTrigger: {
              trigger: header,
              start: 'top 75%',
              end: 'top 30%',
              scrub: 1,
              markers: false,
            }
          }
        )
      }
    })
  }

  // ══════════════════════════════════════════════════════════════
  // CTA SECTION - ZOOM IN & GLOW EFFECT
  // ══════════════════════════════════════════════════════════════
  const ctaSection = homepage.value?.querySelector('.cta-section')
  if (ctaSection) {
    gsap.fromTo(ctaSection,
      {
        opacity: 0,
        scale: 0.8,
        y: 60,
      },
      {
        opacity: 1,
        scale: 1,
        y: 0,
        duration: 0.8,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: ctaSection,
          start: 'top 70%',
          end: 'top 20%',
          scrub: 1.2,
          markers: false,
        }
      }
    )

    // Add pulsing glow effect
    gsap.to(ctaSection, {
      boxShadow: '0 0 60px rgba(212, 175, 55, 0.3)',
      duration: 2,
      repeat: -1,
      yoyo: true,
      ease: 'sine.inOut',
    })
  }

  // ══════════════════════════════════════════════════════════════
  // SCROLL INDICATOR - FADE OUT
  // ══════════════════════════════════════════════════════════════
  const scrollIndicator = homepage.value?.querySelector('.hero-scroll')
  if (scrollIndicator) {
    gsap.to(scrollIndicator, {
      opacity: 0,
      pointerEvents: 'none',
      duration: 0.5,
      scrollTrigger: {
        trigger: '.hero-section',
        start: 'top top',
        end: 'center top',
        scrub: 0.5,
        markers: false,
      }
    })
  }

  // ══════════════════════════════════════════════════════════════
  // FEATURE ICONS - BOUNCE & SCALE ON SCROLL
  // ══════════════════════════════════════════════════════════════
  const featureIcons = homepage.value?.querySelectorAll('.feature-icon-box')
  if (featureIcons && featureIcons.length > 0) {
    featureIcons.forEach((icon, index) => {
      gsap.to(icon, {
        scale: 1.2,
        rotation: 360,
        duration: 0.5,
        delay: index * 0.1,
        ease: 'back.out',
        scrollTrigger: {
          trigger: icon,
          start: 'top 70%',
          end: 'top 40%',
          scrub: 0.5,
          markers: false,
        }
      })
    })
  }

  // ══════════════════════════════════════════════════════════════
  // SERVICE ICONS - SCALE & SPIN EFFECT
  // ══════════════════════════════════════════════════════════════
  const serviceIcons = homepage.value?.querySelectorAll('.service-icon')
  if (serviceIcons && serviceIcons.length > 0) {
    serviceIcons.forEach((icon, index) => {
      gsap.to(icon, {
        scale: 1.3,
        rotation: 180,
        duration: 0.7,
        delay: index * 0.15,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: icon,
          start: 'top 65%',
          end: 'top 35%',
          scrub: 0.8,
          markers: false,
        }
      })
    })
  }

  // ══════════════════════════════════════════════════════════════
  // HERO CIRCLES - EXPAND & FADE
  // ══════════════════════════════════════════════════════════════
  const heroCircles = homepage.value?.querySelectorAll('[class*="hero-circle"]')
  if (heroCircles && heroCircles.length > 0) {
    gsap.to(heroCircles, {
      scale: 1.4,
      opacity: 0,
      duration: 1,
      ease: 'power1.inOut',
      scrollTrigger: {
        trigger: '.hero-section',
        start: 'top top',
        end: 'bottom top',
        scrub: 0.7,
        markers: false,
      }
    })
  }
})

onUnmounted(() => {
  // Clean up ScrollTriggers when component unmounts
  ScrollTrigger.getAll().forEach(trigger => trigger.kill())
})
</script>

<style scoped>
/* ════════════════════════════════════════════════════════════════ */
/* PREMIUM HOMEPAGE WITH GSAP SCROLL ANIMATIONS                    */
/* ════════════════════════════════════════════════════════════════ */

:root {
  --gold: #c9a960;
  --gold-pale: #d4af37;
  --obsidian: #0a0e1a;
  --surface: #1a1f3a;
  --ivory: #f5f5f5;
  --text-muted: #9ca3af;
  --border: rgba(201, 169, 110, 0.1);
  --font-display: 'Playfair Display', serif;
}

* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body, .homepage {
  background: var(--obsidian);
  color: var(--ivory);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  overflow-x: hidden;
}

/* ════════════════════════════════════════════════════════════════ */
/* NAVBAR                                                           */
/* ════════════════════════════════════════════════════════════════ */

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 60px;
  background: rgba(10, 14, 26, 0.7);
  backdrop-filter: blur(15px);
  border-bottom: 1px solid var(--border);
  transition: all 0.3s ease;
}

.navbar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.logo-icon {
  font-size: 22px;
}

.navbar-links {
  display: flex;
  gap: 40px;
  align-items: center;
}

.nav-link {
  font-size: 13px;
  color: var(--text-muted);
  text-decoration: none;
  transition: all 0.3s ease;
  font-weight: 500;
}

.nav-link:hover {
  color: var(--gold-pale);
}

.btn.btn-gold {
  background: var(--gold);
  padding: 10px 24px;
  border-radius: 6px;
  transition: all 0.3s ease;
  font-weight: 600;
  font-size: 13px;
  position: relative;
  overflow: hidden;
}

.btn.btn-gold::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.3), transparent);
  animation: button-shine 3s infinite;
}

.btn.btn-gold:hover {
  background: var(--gold-pale);
  color: #000000;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(212, 175, 55, 0.3);
}

@keyframes button-shine {
  0% {
    transform: translate(-50%, -50%) scale(0);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -50%) scale(2);
    opacity: 0;
  }
}

/* ════════════════════════════════════════════════════════════════ */
/* HERO SECTION                                                     */
/* ════════════════════════════════════════════════════════════════ */

.hero-section {
  position: relative;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  overflow: hidden;
  margin-top: 60px;
}

.hero-bg-lines {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 50% 0%, rgba(201, 169, 110, 0.1) 0%, transparent 60%);
  pointer-events: none;
}

.hero-visual {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.hero-visual-inner,
.hero-circle-large,
.hero-circle-small {
  position: absolute;
  border: 1px solid rgba(201, 169, 110, 0.08);
  border-radius: 50%;
}

.hero-visual-inner {
  width: 600px;
  height: 600px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.hero-circle-large {
  width: 800px;
  height: 800px;
  top: 30%;
  right: -200px;
  opacity: 0.5;
}

.hero-circle-small {
  width: 400px;
  height: 400px;
  bottom: -100px;
  left: -100px;
  opacity: 0.3;
}

/* ────────────────────────────────────── */
/* HERO BACKGROUND & SPARKLES            */
/* ────────────────────────────────────── */

.sparkle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.8), transparent);
  border-radius: 50%;
  box-shadow: 0 0 8px rgba(212, 175, 55, 0.6);
  animation: sparkle-float 4s ease-in-out infinite;
  z-index: 2;
}

.sparkle-1 {
  top: 20%;
  right: 15%;
  animation-delay: 0s;
}

.sparkle-2 {
  top: 40%;
  left: 20%;
  width: 3px;
  height: 3px;
  animation-delay: 1s;
}

.sparkle-3 {
  bottom: 25%;
  right: 25%;
  animation-delay: 2s;
}

.sparkle-4 {
  bottom: 30%;
  left: 15%;
  width: 2px;
  height: 2px;
  animation-delay: 1.5s;
}

@keyframes sparkle-float {
  0%, 100% {
    opacity: 0;
    transform: translateY(0) scale(1);
  }
  50% {
    opacity: 1;
    transform: translateY(-30px) scale(1.3);
  }
}

.hero-content {
  position: relative;
  z-index: 10;
  max-width: 800px;
  padding: 0 40px;
}

.hero-eyebrow {
  font-size: 12px;
  letter-spacing: 0.15em;
  color: rgba(201, 169, 110, 0.7);
  margin-bottom: 24px;
  text-transform: uppercase;
  font-weight: 600;
}

.hero-title {
  font-size: clamp(48px, 8vw, 80px);
  line-height: 1.1;
  font-weight: 700;
  letter-spacing: -2px;
  margin-bottom: 24px;
  word-spacing: 0.1em;
}

.title-word {
  display: inline-block;
  animation: word-fade 0.8s ease-out forwards;
}

.title-word:nth-child(2) {
  animation-delay: 0.1s;
}

@keyframes word-fade {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.gradient-text {
  background: linear-gradient(90deg, var(--gold-pale), #d4c5f9, var(--gold-pale));
  background-size: 200% 100%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradient-shift 6s ease infinite;
}

@keyframes gradient-shift {
  0%, 100% {
    background-position: 0% center;
  }
  50% {
    background-position: 100% center;
  }
}

.hero-title em {
  font-style: italic;
  color: var(--gold-pale);
}

.hero-subtitle {
  font-size: 16px;
  line-height: 1.7;
  color: var(--text-muted);
  margin-bottom: 40px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.hero-cta {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 14px 32px;
  border-radius: 6px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
  font-size: 14px;
}

.btn-lg {
  padding: 16px 42px;
  font-size: 15px;
}

.btn-ghost {
  border: 1px solid rgba(201, 169, 110, 0.3);
  background: transparent;
}

.btn-ghost:hover {
  background: rgba(201, 169, 110, 0.08);
  border-color: rgba(201, 169, 110, 0.6);
}

.hero-scroll {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  font-size: 10px;
  letter-spacing: 0.15em;
  color: rgba(255, 255, 255, 0.2);
  text-transform: uppercase;
  opacity: 1;
  z-index: 20;
}

.hero-scroll-line {
  width: 1px;
  height: 40px;
  background: linear-gradient(to bottom, rgba(201, 169, 110, 0.4), transparent);
  animation: pulse-line 2s ease-in-out infinite;
}

@keyframes pulse-line {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* ════════════════════════════════════════════════════════════════ */
/* MARQUEE SECTION                                                  */
/* ════════════════════════════════════════════════════════════════ */

.marquee-strip {
  background: rgba(201, 169, 110, 0.08);
  border-top: 1px solid rgba(201, 169, 110, 0.12);
  border-bottom: 1px solid rgba(201, 169, 110, 0.12);
  padding: 20px 0;
  overflow: hidden;
  position: relative;
}

.marquee-track {
  display: flex;
  width: max-content;
  gap: 20px;
  animation: scroll-marquee 40s linear infinite;
}

@keyframes scroll-marquee {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-50%);
  }
}

.marquee-item {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: rgba(201, 169, 110, 0.55);
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 28px;
}

.marquee-dot {
  color: var(--gold-pale);
  font-size: 8px;
}

/* ════════════════════════════════════════════════════════════════ */
/* SECTIONS                                                         */
/* ════════════════════════════════════════════════════════════════ */

.section {
  max-width: 1280px;
  margin: 0 auto;
  padding: 100px 60px;
}

.section-dark {
  background: var(--obsidian);
}

.section-header {
  text-align: center;
  margin-bottom: 80px;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.eyebrow {
  display: inline-block;
  font-size: 12px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--gold-pale);
  margin-bottom: 16px;
  font-weight: 600;
}

.section-title {
  font-size: clamp(36px, 6vw, 56px);
  line-height: 1.2;
  font-weight: 700;
  letter-spacing: -1px;
  margin-bottom: 24px;
  position: relative;
  animation: title-glow 2s ease-in-out infinite;
}

@keyframes title-glow {
  0%, 100% {
    text-shadow: 0 0 20px rgba(212, 175, 55, 0.1);
  }
  50% {
    text-shadow: 0 0 40px rgba(212, 175, 55, 0.2), 0 0 60px rgba(212, 175, 55, 0.1);
  }
}

.section-title em {
  font-style: italic;
  color: var(--gold-pale);
}

.section-subtitle {
  font-size: 15px;
  line-height: 1.6;
  color: var(--text-muted);
}

.centered {
  max-width: 640px;
  margin: 0 auto 60px;
}

/* ════════════════════════════════════════════════════════════════ */
/* FEATURES SECTION                                                 */
/* ════════════════════════════════════════════════════════════════ */

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 32px;
}

.feature-card {
  padding: 40px;
  background: rgba(45, 60, 90, 0.3);
  border: 1px solid rgba(201, 169, 110, 0.15);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.feature-card:hover {
  border-color: rgba(201, 169, 110, 0.35);
  background: rgba(45, 60, 90, 0.5);
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(212, 175, 55, 0.15), 0 0 40px rgba(212, 175, 55, 0.1);
}

.glow-icon {
  position: relative;
  display: inline-block;
  font-size: 40px;
  margin-bottom: 20px;
  animation: icon-glow 2s ease-in-out infinite;
}

@keyframes icon-glow {
  0%, 100% {
    text-shadow: 0 0 10px rgba(212, 175, 55, 0.3), 0 0 20px rgba(212, 175, 55, 0);
  }
  50% {
    text-shadow: 0 0 20px rgba(212, 175, 55, 0.6), 0 0 40px rgba(212, 175, 55, 0.3);
  }
}

.shimmer {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  animation: shimmer-slide 3s infinite;
  pointer-events: none;
  z-index: 1;
}

@keyframes shimmer-slide {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

@keyframes title-shimmer {
  0%, 100% {
    background-position: 0% center;
  }
  50% {
    background-position: 100% center;
  }
}

.feature-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--ivory);
  animation: title-float 3s ease-in-out infinite;
}

@keyframes title-float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}

.feature-description {
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-muted);
}

/* ════════════════════════════════════════════════════════════════ */
/* SERVICES SECTION                                                 */
/* ════════════════════════════════════════════════════════════════ */

.services-grid-home {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 32px;
  max-width: 1000px;
  margin: 0 auto;
}

.service-card-home {
  padding: 32px 24px;
  background: linear-gradient(135deg, rgba(45, 60, 90, 0.4) 0%, rgba(45, 60, 90, 0.2) 100%);
  border: 1px solid rgba(201, 169, 110, 0.15);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.service-card-home:hover {
  border-color: rgba(201, 169, 110, 0.35);
  background: linear-gradient(135deg, rgba(45, 60, 90, 0.6) 0%, rgba(45, 60, 90, 0.4) 100%);
  transform: translateY(-12px);
  box-shadow: 0 20px 48px rgba(212, 175, 55, 0.15), 0 0 50px rgba(212, 175, 55, 0.08);
}

.service-card-home h3 {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 12px;
  color: var(--ivory);
  background: linear-gradient(90deg, var(--ivory), rgba(212, 175, 55, 0.8));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: title-shimmer 3s ease infinite;
}

.service-description {
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-muted);
  margin-bottom: 24px;
}

.service-features {
  list-style: none;
  margin-bottom: 24px;
}

.service-features li {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.check-icon {
  color: var(--gold-pale);
  font-weight: bold;
}

.btn-outline {
  border: 1px solid rgba(201, 169, 110, 0.3);
  background: transparent;
  color: var(--text-muted);
}

.btn-outline:hover {
  border-color: rgba(201, 169, 110, 0.6);
  color: var(--gold-pale);
}

/* ════════════════════════════════════════════════════════════════ */
/* CTA SECTION                                                      */
/* ════════════════════════════════════════════════════════════════ */

.cta-section {
  position: relative;
  max-width: 1280px;
  margin: 100px auto;
  padding: 80px 60px;
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.08) 0%, rgba(232, 180, 184, 0.04) 100%);
  border: 1px solid rgba(201, 169, 110, 0.15);
  border-radius: 12px;
  text-align: center;
  overflow: hidden;
  box-shadow: inset 0 0 40px rgba(212, 175, 55, 0.05);
  animation: cta-bloom 4s ease-in-out infinite;
}

@keyframes cta-bloom {
  0%, 100% {
    box-shadow: inset 0 0 40px rgba(212, 175, 55, 0.05), 0 0 30px rgba(212, 175, 55, 0.08);
  }
  50% {
    box-shadow: inset 0 0 40px rgba(212, 175, 55, 0.08), 0 0 50px rgba(212, 175, 55, 0.15);
  }
}

.cta-deco-left,
.cta-deco-right {
  position: absolute;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  border: 1px solid rgba(201, 169, 110, 0.08);
  pointer-events: none;
}

.cta-deco-left {
  bottom: -100px;
  left: -100px;
}

.cta-deco-right {
  top: -100px;
  right: -100px;
}

.cta-title {
  font-size: clamp(32px, 5vw, 48px);
  line-height: 1.2;
  font-weight: 700;
  letter-spacing: -1px;
  margin-bottom: 16px;
}

/* ════════════════════════════════════════════════════════════════ */
/* FOOTER                                                           */
/* ════════════════════════════════════════════════════════════════ */

.footer {
  background: rgba(10, 14, 26, 0.8);
  border-top: 1px solid var(--border);
  padding: 60px 40px 30px;
}

.footer-content {
  max-width: 1280px;
  margin: 0 auto 48px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 48px;
}

.footer-section h4 {
  color: var(--gold-pale);
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 24px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  font-family: var(--font-display);
}

.footer-section p {
  font-size: 14px;
  line-height: 1.9;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 400;
}

.footer-section ul {
  list-style: none;
}

.footer-section li {
  margin-bottom: 12px;
}

.footer-section a {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  transition: color 0.3s ease;
  font-weight: 400;
}

.footer-section a:hover {
  color: var(--gold-pale);
}

.footer-social {
  display: flex;
  gap: 14px;
  margin-top: 20px;
  font-size: 18px;
  opacity: 0.4;
  cursor: pointer;
}

.footer-social span:hover {
  opacity: 1;
}

.footer-bottom {
  max-width: 1280px;
  margin: 0 auto;
  padding-top: 24px;
  border-top: 1px solid var(--border);
  text-align: center;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.6;
}

/* ════════════════════════════════════════════════════════════════ */
/* RESPONSIVE DESIGN                                                */
/* ════════════════════════════════════════════════════════════════ */

@media (max-width: 1024px) {
  .navbar {
    padding: 16px 40px;
  }

  .section,
  .cta-section {
    padding: 80px 40px;
  }

  .navbar-links {
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .navbar {
    padding: 14px 24px;
  }

  .navbar-links {
    gap: 16px;
    font-size: 12px;
  }

  .nav-link {
    font-size: 12px;
  }

  .section,
  .cta-section {
    padding: 60px 24px;
  }

  .hero-title {
    font-size: 36px;
  }

  .hero-subtitle {
    font-size: 15px;
  }

  .hero-cta {
    gap: 12px;
  }

  .btn,
  .btn-lg {
    padding: 12px 24px;
    font-size: 13px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .services-grid-home {
    grid-template-columns: 1fr;
  }

  .feature-card,
  .service-card-home {
    padding: 28px 20px;
  }

  .marquee-item {
    padding: 0 16px;
  }

  .section-header {
    margin-bottom: 60px;
  }

  .section-title {
    font-size: 32px;
  }
}

@media (max-width: 480px) {
  .navbar {
    padding: 12px 16px;
  }

  .navbar-logo {
    font-size: 16px;
  }

  .navbar-links {
    gap: 8px;
  }

  .nav-link {
    font-size: 11px;
  }

  .section,
  .cta-section {
    padding: 48px 16px;
  }

  .hero-section {
    margin-top: 100px;
  }

  .hero-title {
    font-size: 28px;
  }

  .hero-subtitle {
    font-size: 14px;
  }

  .hero-cta {
    flex-direction: column;
    gap: 10px;
  }

  .btn,
  .btn-lg {
    width: 100%;
    padding: 12px 20px;
    font-size: 12px;
  }

  .features-grid,
  .services-grid-home {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .feature-card,
  .service-card-home {
    padding: 20px 16px;
  }

  .section-title {
    font-size: 24px;
  }

  .cta-title {
    font-size: 28px;
  }
}
</style>