<template>
  <div class="login-page">
    <div class="login-bg-pattern"></div>
    <div class="login-card fade-in">
      <div class="login-logo">
        <div class="login-logo-text">Glow Suite</div>
        <div class="login-logo-sub">Beauty Management Platform</div>
      </div>

      <!-- Registration Success Alert -->
      <div v-if="regSuccess" class="alert alert-success">
        Account created! Please log in.
      </div>

      <!-- Login Tab -->
      <template v-if="tab !== 'register'">
        <!-- Tab Buttons -->
        <div class="login-tabs">
          <button
            v-for="t in ['owner', 'manager', 'staff', 'customer']"
            :key="t"
            :class="['login-tab', { active: tab === t }]"
            @click="switchTab(t)"
          >
            {{ t.charAt(0).toUpperCase() + t.slice(1) }}
          </button>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="alert alert-error">{{ error }}</div>

        <!-- User ID or Email Input -->
        <div v-if="tab !== 'customer'" class="form-group">
          <label class="form-label">{{ tab === 'owner' ? 'Owner ID' : 'User ID' }}</label>
          <input
            v-model="form.userId"
            type="text"
            class="form-input"
            :placeholder="tab === 'owner' ? 'owner' : tab === 'manager' ? 'manager' : 'staff user ID'"
          />
        </div>
        <div v-else class="form-group">
          <label class="form-label">Email</label>
          <input
            v-model="form.email"
            type="email"
            class="form-input"
            placeholder="your@email.com"
          />
        </div>

        <!-- Password Input -->
        <div class="form-group">
          <label class="form-label">Password</label>
          <input
            v-model="form.password"
            type="password"
            class="form-input"
            @keydown.enter="login"
          />
        </div>

        <!-- Sign In Button -->
        <button class="btn btn-primary w-full" style="margin-top: 8px; padding: 13px; font-size: 15px" @click="login" :disabled="isLoading">
          {{ isLoading ? "Signing in..." : "Sign In" }}
        </button>

        <!-- Register Link for Customer -->
        <template v-if="tab === 'customer'">
          <div class="login-divider">or</div>
          <button class="btn btn-outline w-full" @click="switchTab('register')">
            Create Account
          </button>
        </template>

      </template>

      <!-- Register Tab -->
      <template v-else>
        <!-- Back Button -->
        <div
          style="margin-bottom: 20px; display: flex; align-items: center; gap: 8px; cursor: pointer; color: var(--gold-dark); font-size: 13px"
          @click="switchTab('customer')"
        >
          ← Back to Login
        </div>

        <!-- Error Message -->
        <div v-if="error" class="alert alert-error">{{ error }}</div>

        <!-- Registration Form -->
        <div class="form-group">
          <label class="form-label">Full Name *</label>
          <input v-model="regForm.name" type="text" class="form-input" />
        </div>
        <div class="form-group">
          <label class="form-label">Email *</label>
          <input v-model="regForm.email" type="email" class="form-input" />
        </div>
        <div class="form-group">
          <label class="form-label">Date of Birth</label>
          <input v-model="regForm.dob" type="date" class="form-input" />
        </div>
        <div class="form-group">
          <label class="form-label">Phone</label>
          <input v-model="regForm.phone" type="text" class="form-input" />
        </div>
        <div class="form-group">
          <label class="form-label">
            Address <span class="text-muted">(optional)</span>
          </label>
          <input v-model="regForm.address" type="text" class="form-input" />
        </div>
        <div class="form-group">
          <label class="form-label">Password *</label>
          <input v-model="regForm.password" type="password" class="form-input" />
        </div>
        <div class="form-group">
          <label class="form-label">Service Preferences</label>
          <div class="preferences-group">
            <label v-for="service in ['Facial', 'Hair Care', 'Massage', 'Manicure', 'Pedicure', 'Threading', 'Waxing']" :key="service" class="preference-checkbox">
              <input v-model="regForm.preferences" type="checkbox" :value="service">
              <span>{{ service }}</span>
            </label>
          </div>
        </div>
        <button class="btn btn-primary w-full" style="margin-top: 8px; padding: 13px; font-size: 15px" @click="register" :disabled="isLoading">
          {{ isLoading ? "Creating Account..." : "Create Account" }}
        </button>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAppStore } from "@/stores/appStore";

const router = useRouter();
const route = useRoute();
const appStore = useAppStore();

const API_BASE_URL = "http://localhost:5000";

const tab = ref("manager");
const form = reactive({ userId: "", email: "", password: "", name: "", phone: "" });
const regForm = reactive({ name: "", email: "", phone: "", password: "", address: "", dob: "", preferences: [] });
const error = ref("");
const regSuccess = ref(false);
const isLoading = ref(false);

const switchTab = (newTab) => {
  tab.value = newTab;
  error.value = "";

  if (newTab !== "register") {
    router.replace(`/login/${newTab}`);
  }
};

watch(
  () => route.path,
  (path) => {
    const role = path.split("/")[2];
    if (["owner", "manager", "staff", "customer"].includes(role)) {
      tab.value = role;
      error.value = "";
    }
  },
  { immediate: true }
);

const login = async () => {
  error.value = "";
  isLoading.value = true;

  try {
    let endpoint = "";
    let payload = {};

    if (tab.value === "owner") {
      endpoint = `${API_BASE_URL}/owner-login`;
      payload = { username: form.userId, password: form.password };
    } else if (tab.value === "manager") {
      endpoint = `${API_BASE_URL}/manager-login`;
      payload = { username: form.userId, password: form.password };
    } else if (tab.value === "staff") {
      endpoint = `${API_BASE_URL}/staff-login`;
      payload = { username: form.userId, password: form.password };
    } else if (tab.value === "customer") {
      endpoint = `${API_BASE_URL}/customer-login`;
      payload = { username: form.email, password: form.password };
    }

    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (response.ok && data.token) {
      const normalizedUser = {
        username: data.username || payload.username,
        role: (data.role || tab.value).toLowerCase(),
      };

      // Store token in localStorage
      localStorage.setItem("authToken", data.token);
      localStorage.setItem("user", JSON.stringify(normalizedUser));
      
      // Update app store
      appStore.login({ token: data.token, ...normalizedUser });
      const dashboardRouteByRole = {
        owner: "/owner-dashboard",
        manager: "/manager-dashboard",
        staff: "/staff-dashboard",
        customer: "/customer-dashboard",
      };
      router.push(dashboardRouteByRole[normalizedUser.role] || "/dashboard");
    } else {
      error.value = data.message || "Login failed. Please try again.";
    }
  } catch (err) {
    console.error("Login error:", err);
    error.value = "Connection error. Make sure the backend is running on http://localhost:5000";
  } finally {
    isLoading.value = false;
  }
};

const genId = (arr) => {
  return arr.length > 0 ? Math.max(...arr.map((item) => item.id || 0)) + 1 : 1;
};

const today = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
};

const register = async () => {
  if (!regForm.name || !regForm.email || !regForm.password) {
    error.value = "Name, email and password are required.";
    return;
  }

  isLoading.value = true;
  
  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/register/customer`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: regForm.name,
        email: regForm.email,
        phone: regForm.phone,
        address: regForm.address,
        password: regForm.password,
        dob: regForm.dob,
        preferences: regForm.preferences
      }),
    });

    const data = await response.json();

    if (data.success) {
      // Store token
      localStorage.setItem("authToken", data.token);
      localStorage.setItem("user", JSON.stringify(data.user));
      
      // Update app store
      appStore.login({ token: data.token, ...data.user });
      
      regSuccess.value = true;
      tab.value = "customer";
      form.email = regForm.email;
      form.password = regForm.password;
      error.value = "";
      
      // Auto-redirect after 2 seconds
      setTimeout(() => {
        router.push("/");
      }, 2000);
    } else {
      error.value = data.message || "Registration failed. Please try again.";
    }
  } catch (err) {
    console.error("Registration error:", err);
    error.value = "Connection error. Make sure the backend is running.";
  } finally {
    isLoading.value = false;
  }
};
</script>
