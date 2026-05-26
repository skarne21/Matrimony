<script setup lang="ts">
import { useRegistrationStore } from '../../../stores/registration'
const reg = useRegistrationStore()

const educationOptions = [
  'High School', 'Diploma', "Bachelor's Degree", "Master's Degree",
  'MBA', 'PhD / Doctorate', 'MBBS / MD', 'CA / CS', 'Other',
]
</script>

<template>
  <div>
    <p class="card-title">Education & Career</p>
    <p class="card-subtitle">Tell matches about your professional background</p>

    <div class="form-group">
      <label>Highest Education</label>
      <select v-model="reg.education_level">
        <option value="">Select qualification</option>
        <option v-for="e in educationOptions" :key="e" :value="e">{{ e }}</option>
      </select>
    </div>

    <div class="form-group">
      <label>College / University <span class="optional-tag">optional</span></label>
      <input type="text" v-model="reg.college" placeholder="e.g. IIT Delhi, Osmania University" />
    </div>

    <div class="row">
      <div class="form-group">
        <label>Occupation</label>
        <input type="text" v-model="reg.occupation" placeholder="e.g. Software Engineer" />
      </div>
      <div class="form-group">
        <label>Company <span class="optional-tag">optional</span></label>
        <input type="text" v-model="reg.company" placeholder="e.g. TCS, Infosys" />
      </div>
    </div>

    <div class="row">
      <div class="form-group">
        <label>Annual Income (₹) <span class="optional-tag">optional</span></label>
        <input type="number" v-model.number="reg.annual_income" placeholder="e.g. 800000" min="0" />
      </div>
      <div class="form-group">
        <label>Work Location <span class="optional-tag">optional</span></label>
        <input type="text" v-model="reg.work_location" placeholder="e.g. Hyderabad, Bengaluru" />
      </div>
    </div>

    <div class="step-actions">
      <button class="btn btn-secondary" @click="reg.prevStep()">← Back</button>
      <button class="btn btn-primary" @click="reg.nextStep()">Next →</button>
    </div>
  </div>
</template>
