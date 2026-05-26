<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRegistrationStore } from '../../../stores/registration'

const reg = useRegistrationStore()

const confirmPassword = ref('')

const isValid = computed(() =>
  reg.phone_number.trim() &&
  reg.email.trim() &&
  reg.password.length >= 8 &&
  reg.password === confirmPassword.value &&
  reg.first_name.trim() &&
  reg.last_name.trim() &&
  reg.gender &&
  reg.dob &&
  reg.marital_status
)

function setGender(v: string) { reg.gender = v }
function setCreatedBy(v: string) { reg.profile_created_by = v }
</script>

<template>
  <div>
    <p class="card-title">Basic Details</p>
    <p class="card-subtitle">Let's start with your basic information</p>

    <div class="row">
      <div class="form-group">
        <label>First Name *</label>
        <input type="text" v-model="reg.first_name" placeholder="First name" />
      </div>
      <div class="form-group">
        <label>Last Name *</label>
        <input type="text" v-model="reg.last_name" placeholder="Last name" />
      </div>
    </div>

    <div class="form-group">
      <label>Gender *</label>
      <div class="radio-group">
        <label v-for="opt in ['male','female','other']" :key="opt"
          class="radio-option" :class="{ selected: reg.gender === opt }"
          @click="setGender(opt)">
          {{ opt.charAt(0).toUpperCase() + opt.slice(1) }}
        </label>
      </div>
    </div>

    <div class="row">
      <div class="form-group">
        <label>Date of Birth *</label>
        <input type="date" v-model="reg.dob" />
      </div>
      <div class="form-group">
        <label>Marital Status *</label>
        <select v-model="reg.marital_status">
          <option value="">Select</option>
          <option value="never_married">Never Married</option>
          <option value="divorced">Divorced</option>
          <option value="widowed">Widowed</option>
        </select>
      </div>
    </div>

    <div class="row">
      <div class="form-group">
        <label>Height (cm) <span class="optional-tag">optional</span></label>
        <input type="number" v-model.number="reg.height_cm" placeholder="e.g. 170" min="100" max="250" />
      </div>
      <div class="form-group">
        <label>Weight (kg) <span class="optional-tag">optional</span></label>
        <input type="number" v-model.number="reg.weight_kg" placeholder="e.g. 65" min="30" max="200" />
      </div>
    </div>

    <div class="form-group">
      <label>Profile Created By</label>
      <div class="radio-group">
        <label v-for="opt in ['self','parent','relative','friend']" :key="opt"
          class="radio-option" :class="{ selected: reg.profile_created_by === opt }"
          @click="setCreatedBy(opt)">
          {{ opt.charAt(0).toUpperCase() + opt.slice(1) }}
        </label>
      </div>
    </div>

    <hr style="border:none; border-top:1px solid #eee; margin: 20px 0;" />
    <p class="card-subtitle" style="margin-bottom:16px;">Contact & Login Details</p>

    <div class="form-group">
      <label>Mobile Number *</label>
      <input type="tel" v-model="reg.phone_number" placeholder="+91 98765 43210" />
    </div>

    <div class="form-group">
      <label>Email Address *</label>
      <input type="email" v-model="reg.email" placeholder="you@example.com" />
    </div>

    <div class="row">
      <div class="form-group">
        <label>Password *</label>
        <input type="password" v-model="reg.password" placeholder="Min. 8 characters" />
      </div>
      <div class="form-group">
        <label>Confirm Password *</label>
        <input type="password" v-model="confirmPassword" placeholder="Repeat password" />
        <span v-if="confirmPassword && reg.password !== confirmPassword" class="error-text">Passwords do not match</span>
      </div>
    </div>

    <div class="step-actions">
      <span />
      <button class="btn btn-primary" :disabled="!isValid" @click="reg.nextStep()">
        Next →
      </button>
    </div>
  </div>
</template>
