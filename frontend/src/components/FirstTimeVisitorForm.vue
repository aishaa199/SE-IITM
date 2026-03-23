<template>
  <div v-if="isOpen" class="modal-overlay" @click="closeModal">
    <div class="modal" @click.stop>
      <div class="modal-header">
        <h2>Welcome! 👋</h2>
        <p class="subtitle">Please tell us a bit about yourself</p>
      </div>

      <form @submit.prevent="submitForm" class="form">
        <!-- Date of Birth Section -->
        <div class="form-section">
          <h3>Date of Birth</h3>
          <input 
            v-model="formData.dob" 
            type="date" 
            class="input-field"
          >
        </div>

        <!-- Skin Type Section -->
        <div class="form-section">
          <h3>What's your skin type?</h3>
          <div class="radio-group">
            <label v-for="type in skinTypes" :key="type" class="radio-label">
              <input v-model="formData.skinType" type="radio" :value="type">
              <span>{{ type }}</span>
            </label>
          </div>
        </div>

        <!-- Allergies Section -->
        <div class="form-section">
          <h3>Any allergies we should know about?</h3>
          <textarea 
            v-model="formData.allergies" 
            placeholder="List any allergies or sensitivities (comma-separated)"
            class="textarea"
          ></textarea>
        </div>

        <!-- Service Preferences Section -->
        <div class="form-section">
          <h3>What services interest you?</h3>
          <div class="checkbox-group">
            <label v-for="service in availableServices" :key="service" class="checkbox-label">
              <input v-model="formData.services" type="checkbox" :value="service">
              <span>{{ service }}</span>
            </label>
          </div>
        </div>

        <!-- Past Treatments Section -->
        <div class="form-section">
          <h3>Any past treatments or experiences?</h3>
          <textarea 
            v-model="formData.pastTreatments" 
            placeholder="Tell us about any previous treatments or experiences"
            class="textarea"
          ></textarea>
        </div>

        <!-- Special Requests Section -->
        <div class="form-section">
          <h3>Anything special we should know?</h3>
          <textarea 
            v-model="formData.specialRequests" 
            placeholder="Special requests or preferences (optional)"
            class="textarea"
          ></textarea>
        </div>

        <!-- Customer Preferences Section -->
        <div class="form-section">
          <h3>Preferred Services</h3>
          <div class="checkbox-group">
            <label v-for="pref in customerPreferences" :key="pref" class="checkbox-label">
              <input v-model="formData.preferences" type="checkbox" :value="pref">
              <span>{{ pref }}</span>
            </label>
          </div>
        </div>

        <!-- Form Actions -->
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">Complete Questionnaire</button>
          <button type="button" class="btn btn-secondary" @click="closeModal">Skip</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'submit'])

const skinTypes = ['Oily', 'Dry', 'Combination', 'Sensitive', 'Normal']
const availableServices = [
  'Facial',
  'Hair Care',
  'Massage',
  'Manicure',
  'Pedicure',
  'Threading',
  'Waxing'
]
const customerPreferences = [
  'Facial',
  'Hair Care',
  'Massage',
  'Manicure',
  'Pedicure',
  'Threading',
  'Waxing'
]

const formData = ref({
  dob: '',
  skinType: '',
  allergies: '',
  services: [],
  pastTreatments: '',
  specialRequests: '',
  preferences: []
})

const closeModal = () => {
  emit('close')
}

const submitForm = () => {
  // Emit the form data
  emit('submit', {
    dob: formData.value.dob,
    skinType: formData.value.skinType,
    allergies: formData.value.allergies.split(',').map(a => a.trim()).filter(a => a),
    services: formData.value.services,
    pastTreatments: formData.value.pastTreatments,
    specialRequests: formData.value.specialRequests,
    preferences: formData.value.preferences
  })
  
  // Close modal
  closeModal()
}
</script>

<style scoped>
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
  padding: 20px;
}

.modal {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.modal-header {
  background: linear-gradient(135deg, var(--gold), #d4a956);
  color: white;
  padding: 32px 24px;
  text-align: center;
}

.modal-header h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
}

.subtitle {
  margin: 0;
  font-size: 14px;
  opacity: 0.9;
}

.form {
  padding: 32px 24px;
}

.form-section {
  margin-bottom: 24px;
}

.form-section h3 {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #333;
}

.radio-label input[type="radio"] {
  cursor: pointer;
  width: 18px;
  height: 18px;
}

.input-field {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-family: inherit;
  font-size: 13px;
}

.input-field:focus {
  outline: none;
  border-color: var(--gold);
  box-shadow: 0 0 0 3px rgba(212, 169, 84, 0.1);
}

.checkbox-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 13px;
  color: #333;
}

.checkbox-label input[type="checkbox"] {
  cursor: pointer;
  width: 16px;
  height: 16px;
}

.textarea {
  width: 100%;
  min-height: 80px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-family: inherit;
  font-size: 13px;
  resize: vertical;
}

.textarea:focus {
  outline: none;
  border-color: var(--gold);
  box-shadow: 0 0 0 3px rgba(212, 169, 84, 0.1);
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 32px;
}

.btn {
  flex: 1;
  padding: 12px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: var(--gold);
  color: var(--charcoal);
}

.btn-primary:hover {
  background: #d4a956;
  transform: translateY(-2px);
}

.btn-secondary {
  background: #f0f0f0;
  color: #333;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

@media (max-width: 600px) {
  .checkbox-group {
    grid-template-columns: 1fr;
  }

  .modal-header {
    padding: 24px 16px;
  }

  .form {
    padding: 24px 16px;
  }
}
</style>
