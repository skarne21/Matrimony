<script setup lang="ts">
import { computed } from 'vue'
import { useRegistrationStore } from '../../stores/registration'
import Step1Basic from './steps/Step1Basic.vue'
import Step2Personal from './steps/Step2Personal.vue'
import Step3Education from './steps/Step3Education.vue'
import Step4Family from './steps/Step4Family.vue'
import Step5Preferences from './steps/Step5Preferences.vue'
import Step6Photos from './steps/Step6Photos.vue'

const reg = useRegistrationStore()

const stepLabels = ['Basic Info', 'Religion', 'Career', 'Family', 'Partner', 'Photos']

const currentComponent = computed(() => {
  return [Step1Basic, Step2Personal, Step3Education, Step4Family, Step5Preferences, Step6Photos][reg.step - 1]
})
</script>

<template>
  <div class="page-center">
    <div class="card">
      <!-- Header -->
      <div style="text-align:center; margin-bottom: 24px;">
        <h1 style="font-size:26px; font-weight:800; color:#c0392b; margin-bottom:4px;">Veerabhadra Matrimony</h1>
        <p style="font-size:14px; color:#888;">Create your profile — Step {{ reg.step }} of {{ stepLabels.length }}</p>
      </div>

      <!-- Step progress bar -->
      <div style="display:flex; gap:6px; margin-bottom:28px;">
        <div
          v-for="(_, i) in stepLabels"
          :key="i"
          :style="{
            flex: '1',
            height: '4px',
            borderRadius: '4px',
            background: i < reg.step ? '#c0392b' : '#eee',
            transition: 'background 0.3s',
          }"
        />
      </div>

      <!-- Step label -->
      <p style="font-size:12px; font-weight:700; color:#c0392b; text-transform:uppercase; letter-spacing:1px; margin-bottom:16px;">
        {{ stepLabels[reg.step - 1] }}
      </p>

      <!-- Active step component -->
      <component :is="currentComponent" />
    </div>
  </div>
</template>
