<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRegistrationStore } from '../../../stores/registration'
import api from '../../../api/index'

const reg = useRegistrationStore()

interface Religion { id: number; name: string }
interface Caste    { id: number; name: string }

const religions = ref<Religion[]>([])
const castes    = ref<Caste[]>([])

onMounted(async () => {
  try {
    const [rRes, cRes] = await Promise.all([
      api.get('/api/religions/'),
      api.get('/api/castes/'),
    ])
    religions.value = rRes.data
    castes.value = cRes.data
  } catch { /* non-blocking */ }
})

function toggleReligion(id: number) {
  const arr = reg.partner_preferences.acceptable_religions
  const idx = arr.indexOf(id)
  idx === -1 ? arr.push(id) : arr.splice(idx, 1)
}

function toggleCaste(id: number) {
  const arr = reg.partner_preferences.acceptable_castes
  const idx = arr.indexOf(id)
  idx === -1 ? arr.push(id) : arr.splice(idx, 1)
}
</script>

<template>
  <div>
    <p class="card-title">Partner Preferences</p>
    <p class="card-subtitle">Who are you looking for?</p>

    <div class="row">
      <div class="form-group">
        <label>Preferred Age — Min</label>
        <input type="number" v-model.number="reg.partner_preferences.age_min" min="18" max="80" />
      </div>
      <div class="form-group">
        <label>Preferred Age — Max</label>
        <input type="number" v-model.number="reg.partner_preferences.age_max" min="18" max="80" />
      </div>
    </div>

    <div class="row">
      <div class="form-group">
        <label>Min Height (cm) <span class="optional-tag">optional</span></label>
        <input type="number" v-model.number="reg.partner_preferences.height_min_cm" min="100" max="250" />
      </div>
      <div class="form-group">
        <label>Max Height (cm) <span class="optional-tag">optional</span></label>
        <input type="number" v-model.number="reg.partner_preferences.height_max_cm" min="100" max="250" />
      </div>
    </div>

    <div class="form-group" v-if="religions.length">
      <label>Acceptable Religions <span class="optional-tag">select all that apply</span></label>
      <div class="radio-group">
        <label v-for="r in religions" :key="r.id"
          class="radio-option"
          :class="{ selected: reg.partner_preferences.acceptable_religions.includes(r.id) }"
          @click="toggleReligion(r.id)">
          {{ r.name }}
        </label>
      </div>
    </div>

    <div class="form-group" v-if="castes.length">
      <label>Acceptable Castes <span class="optional-tag">select all that apply</span></label>
      <div class="radio-group" style="max-height:160px; overflow-y:auto; padding:4px;">
        <label v-for="c in castes" :key="c.id"
          class="radio-option"
          :class="{ selected: reg.partner_preferences.acceptable_castes.includes(c.id) }"
          @click="toggleCaste(c.id)">
          {{ c.name }}
        </label>
      </div>
    </div>

    <div class="row">
      <div class="form-group">
        <label>Preferred Education <span class="optional-tag">optional</span></label>
        <input type="text" v-model="reg.partner_preferences.preferred_education" placeholder="e.g. Bachelor's or above" />
      </div>
      <div class="form-group">
        <label>Preferred Profession <span class="optional-tag">optional</span></label>
        <input type="text" v-model="reg.partner_preferences.preferred_profession" placeholder="e.g. Software Engineer" />
      </div>
    </div>

    <div class="form-group">
      <label>Preferred Location <span class="optional-tag">optional</span></label>
      <input type="text" v-model="reg.partner_preferences.preferred_location" placeholder="e.g. Hyderabad, Any city in India" />
    </div>

    <div class="step-actions">
      <button class="btn btn-secondary" @click="reg.prevStep()">← Back</button>
      <button class="btn btn-primary" @click="reg.nextStep()">Next →</button>
    </div>
  </div>
</template>
