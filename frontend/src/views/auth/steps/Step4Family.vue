<script setup lang="ts">
import { useRegistrationStore } from '../../../stores/registration'
const reg = useRegistrationStore()
</script>

<template>
  <div>
    <p class="card-title">Family Details</p>
    <p class="card-subtitle">Share your family background</p>

    <div class="row">
      <div class="form-group">
        <label>Father's Name</label>
        <input type="text" v-model="reg.father_name" placeholder="Father's full name" />
      </div>
      <div class="form-group">
        <label>Father's Occupation</label>
        <input type="text" v-model="reg.father_occupation" placeholder="e.g. Business, Retired" />
      </div>
    </div>

    <div class="row">
      <div class="form-group">
        <label>Mother's Name</label>
        <input type="text" v-model="reg.mother_name" placeholder="Mother's full name" />
      </div>
      <div class="form-group">
        <label>Mother's Occupation</label>
        <input type="text" v-model="reg.mother_occupation" placeholder="e.g. Homemaker, Teacher" />
      </div>
    </div>

    <div class="row">
      <div class="form-group">
        <label>Brothers</label>
        <input type="number" v-model.number="reg.brothers_count" min="0" max="10" />
      </div>
      <div class="form-group">
        <label>Sisters</label>
        <input type="number" v-model.number="reg.sisters_count" min="0" max="10" />
      </div>
    </div>

    <div class="row">
      <div class="form-group">
        <label>Family Type</label>
        <div class="radio-group">
          <label v-for="opt in ['joint','nuclear']" :key="opt"
            class="radio-option" :class="{ selected: reg.family_type === opt }"
            @click="reg.family_type = opt">
            {{ opt.charAt(0).toUpperCase() + opt.slice(1) }}
          </label>
        </div>
      </div>
      <div class="form-group">
        <label>Family Status <span class="optional-tag">optional</span></label>
        <input type="text" v-model="reg.family_status" placeholder="e.g. Middle Class, Affluent" />
      </div>
    </div>

    <div class="step-actions">
      <button class="btn btn-secondary" @click="reg.prevStep()">← Back</button>
      <button class="btn btn-primary" @click="reg.nextStep()">Next →</button>
    </div>
  </div>
</template>
