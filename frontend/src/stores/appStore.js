import { defineStore } from "pinia";
import { ref, reactive } from "vue";

const INITIAL_DATA = {
  staff: [
    { id: 1, name: "Amara Osei", role: "Senior Stylist", skills: "Hair Cutting, Styling, Coloring, Balayage", email: "amara@glowsuite.com", phone: "050-111-2222", doj: "2022-03-15", userId: "amara01", password: "pass123", status: "active", registrationDate: "2022-03-15", salary: 2000, rating: 4.8 },
    { id: 2, name: "Priya Nair", role: "Nail Technician", skills: "Gel Manicure, Pedicure, Nail Art, Extensions", email: "priya@glowsuite.com", phone: "024-333-4444", doj: "2023-01-20", userId: "priya02", password: "pass123", status: "active", registrationDate: "2023-01-20", salary: 1500, rating: 4.7 },
    { id: 3, name: "Kwame Mensah", role: "Barber", skills: "Hair Cutting, Beard Grooming, Fades, Shaping", email: "kwame@glowsuite.com", phone: "020-555-6666", doj: "2021-07-10", userId: "kwame03", password: "pass123", status: "active", registrationDate: "2021-07-10", salary: 1800, rating: 4.9 },
  ],
  serviceCategories: [
    { id: 1, name: "Hair", description: "All hair services" },
    { id: 2, name: "Nails", description: "Manicure, pedicure" },
    { id: 3, name: "Skin", description: "Facials, treatments" },
  ],
  services: [
    { id: 1, categoryId: 1, name: "Hair Cut & Style", price: 85, duration: 60, description: "Professional cut and styling" },
    { id: 2, categoryId: 1, name: "Balayage", price: 220, duration: 180, description: "Hand-painted highlights" },
    { id: 3, categoryId: 2, name: "Gel Manicure", price: 55, duration: 60, description: "Long-lasting gel polish" },
    { id: 4, categoryId: 3, name: "Hydra Facial", price: 120, duration: 75, description: "Deep cleansing facial" },
    { id: 5, categoryId: 1, name: "Bridal Package", price: 500, duration: 240, description: "Complete bridal makeup and styling" },
  ],
  appointments: [
    { id: 1, customerId: 1, serviceId: 1, staffId: 1, date: "2026-03-05", status: "confirmed", notes: "Trim only", invoiceStatus: "pending" },
    { id: 2, customerId: 2, serviceId: 3, staffId: 2, date: "2026-03-05", status: "in-progress", notes: "", invoiceStatus: "pending" },
    { id: 3, customerId: 3, serviceId: 4, staffId: null, date: "2026-03-06", status: "pending", notes: "First time client", invoiceStatus: "pending" },
    { id: 4, customerId: 1, serviceId: 2, staffId: 1, date: "2026-03-04", status: "completed", notes: "", invoiceStatus: "invoiced" },
  ],
  customers: [
    { id: 1, name: "Sofia Mensah", email: "sofia@email.com", phone: "030-111-2222", address: "14 Cantonments Rd", dob: "1992-06-15", preferences: "Prefers Amara, sensitive scalp", registrationDate: "2025-01-10", password: "pass123", customerType: "VIP", totalSpent: 5500, pointsBalance: 550, pointsEarned: 550, lastPointsUpdate: "2026-03-04" },
    { id: 2, name: "Akosua Darko", email: "akosua@email.com", phone: "024-333-5555", address: "", dob: "1988-11-20", preferences: "Gel nails only, nude shades", registrationDate: "2025-03-22", password: "pass123", customerType: "Normal", totalSpent: 55, pointsBalance: 5.5, pointsEarned: 5.5, lastPointsUpdate: "2026-03-03" },
    { id: 3, name: "James Otieno", email: "james@email.com", phone: "020-777-8888", address: "7 Airport Hills", dob: "1995-04-05", preferences: "No fragrance products", registrationDate: "2025-06-14", password: "pass123", customerType: "Normal", totalSpent: 120, pointsBalance: 12, pointsEarned: 12, lastPointsUpdate: "2026-03-04" },
  ],
  products: [
    { id: 1, name: "L'Oreal Serum", categoryName: "Hair Care", stock: 8, unit: "bottle", costPrice: 45, sellPrice: 85, supplier: "BeautyPro Ltd", supplierContact: "0302-111-222", minStock: 5, description: "Hydrating hair serum" },
    { id: 2, name: "OPI Gel Polish", categoryName: "Nails", stock: 2, unit: "bottle", costPrice: 22, sellPrice: 38, supplier: "Nail World", supplierContact: "0244-333-444", minStock: 10, description: "Long-wear gel polish" },
    { id: 3, name: "Bleach Powder", categoryName: "Hair Colour", stock: 15, unit: "pack", costPrice: 18, sellPrice: 30, supplier: "BeautyPro Ltd", supplierContact: "0302-111-222", minStock: 8, description: "Professional bleach" },
    { id: 4, name: "Cetaphil Cleanser", categoryName: "Skin Care", stock: 3, unit: "tube", costPrice: 35, sellPrice: 60, supplier: "MedBeauty", supplierContact: "0555-666-777", minStock: 6, description: "Gentle face cleanser" },
  ],
  orders: [
    { id: 1, productId: 2, qty: 20, requestedBy: "priya02", status: "pending", date: "2026-03-03", notes: "Urgent restock" },
  ],
  feedbacks: [
    { id: 1, customerId: 1, serviceId: 1, staffId: 1, rating: 5, comment: "Amazing service! Amara is wonderful.", date: "2026-03-04" },
    { id: 2, customerId: 2, serviceId: 3, staffId: 2, rating: 4, comment: "Great nails, will come again.", date: "2026-03-03" },
  ],
  inventoryTransactions: [
    { id: 1, productId: 1, type: "taken", staffId: 1, qty: 1, date: "2026-03-04", notes: "Used for client" },
    { id: 2, productId: 3, type: "replenished", staffId: null, qty: 5, date: "2026-03-03", notes: "Manager restock" },
  ],
  attendance: [
    { id: 1, staffId: 1, date: "2026-03-04", status: "present" },
    { id: 2, staffId: 2, date: "2026-03-04", status: "present" },
    { id: 3, staffId: 3, date: "2026-03-04", status: "absent" },
    { id: 4, staffId: 1, date: "2026-03-20", status: "present" },
    { id: 5, staffId: 2, date: "2026-03-20", status: "present" },
    { id: 6, staffId: 3, date: "2026-03-20", status: "present" },
  ],
  rewards: {
    pointsPerRupee: 0.1, // 10 points per 100 rupees
    pointsForRedemption: 500, // 500 points for redemption
    redemptionValue: 25, // 25 rupees discount
    vipThreshold: 5000, // 5000 rupees spent to become VIP
    firstVisitPoints: 20, // Bonus points for first visit
    birthdayPoints: 50, // Bonus points on birthday
    vipDiscount: 15, // 15% discount for VIP
    pointsExpiryMonths: 6 // Points expire after 6 months
  },
};

export const useAppStore = defineStore("app", () => {
  const data = reactive({ ...INITIAL_DATA });
  const user = ref(null);
  const token = ref(null);
  const isAuthenticated = ref(false);

  // Load auth from localStorage on store creation
  const initializeAuth = () => {
    const savedToken = localStorage.getItem("authToken");
    const savedUser = localStorage.getItem("user");
    
    if (savedToken && savedUser) {
      try {
        token.value = savedToken;
        user.value = JSON.parse(savedUser);
        isAuthenticated.value = true;
      } catch (e) {
        console.error("Failed to restore auth:", e);
        clearAuth();
      }
    }
  };

  const login = (userData) => {
    user.value = userData;
    token.value = userData.token;
    isAuthenticated.value = true;
  };

  const logout = () => {
    user.value = null;
    token.value = null;
    isAuthenticated.value = false;
    localStorage.removeItem("authToken");
    localStorage.removeItem("user");
  };

  const clearAuth = () => {
    user.value = null;
    token.value = null;
    isAuthenticated.value = false;
    localStorage.removeItem("authToken");
    localStorage.removeItem("user");
  };

  const addCustomer = (customer) => {
    data.customers.push(customer);
  };

  const updateData = (newData) => {
    Object.assign(data, newData);
  };

  // Initialize on store creation
  initializeAuth();

  return {
    data,
    user,
    token,
    isAuthenticated,
    login,
    logout,
    clearAuth,
    addCustomer,
    updateData,
    initializeAuth,
  };
});
