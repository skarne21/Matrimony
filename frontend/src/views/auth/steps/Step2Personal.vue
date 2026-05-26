<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRegistrationStore } from '../../../stores/registration'
import api from '../../../api/index'

const reg = useRegistrationStore()

interface Religion { id: number; name: string }

const religions = ref<Religion[]>([])

async function loadReligions() {
  try {
    const { data } = await api.get('/api/religions/')
    religions.value = data
  } catch { /* non-blocking */ }
}

onMounted(() => {
  loadReligions()
})
</script>

<template>
  <div>
    <p class="card-title">Personal & Religion</p>
    <p class="card-subtitle">Help matches understand your background</p>

    <div class="form-group">
      <label>Mother Tongue</label>
      <input type="text" v-model="reg.mother_tongue" placeholder="e.g. Telugu, Tamil, Hindi" />
    </div>

    <div class="row">
      <div class="form-group">
        <label>Religion</label>
        <select v-model.number="reg.religion_id">
          <option :value="null">Select religion</option>
          <option v-for="r in religions" :key="r.id" :value="r.id">{{ r.name }}</option>
        </select>
      </div>
      <div class="form-group">
        <label>Caste / Community <span class="optional-tag">optional</span></label>
        <input type="text" v-model="reg.caste_name" placeholder="e.g. Reddy, Nair, Iyer, Khatri" />
      </div>
    </div>

    <div class="form-group">
      <label>Sub-caste <span class="optional-tag">optional</span></label>
      <input type="text" v-model="reg.sub_caste" placeholder="e.g. Deshastha, Karhade" />
    </div>

    <hr style="border:none; border-top:1px solid #eee; margin: 16px 0;" />
    <p style="font-size:13px; font-weight:600; color:#888; margin-bottom:14px;">
      Horoscope Details <span class="optional-tag">optional</span>
    </p>

    <div class="row">
      <div class="form-group">
        <label>Nakshatra</label>
        <input type="text" v-model="reg.nakshatra" placeholder="Birth star" />
      </div>
      <div class="form-group">
        <label>Rashi</label>
        <input type="text" v-model="reg.rashi" placeholder="Moon sign" />
      </div>
    </div>

    <div class="form-group">
      <label>Manglik / Dosha</label>
      <div class="radio-group">
        <label v-for="opt in [{ label: 'Yes', val: true }, { label: 'No', val: false }, { label: 'Not sure', val: null }]" :key="String(opt.val)"
          class="radio-option" :class="{ selected: reg.is_manglik === opt.val }"
          @click="reg.is_manglik = opt.val">
          {{ opt.label }}
        </label>
      </div>
    </div>

    <div class="step-actions">
      <button class="btn btn-secondary" @click="reg.prevStep()">← Back</button>
      <button class="btn btn-primary" @click="reg.nextStep()">Next →</button>
    </div>
  </div>
</template>
