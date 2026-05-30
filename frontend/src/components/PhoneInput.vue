<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'

const props = defineProps<{ modelValue: string }>()
const emit = defineEmits<{ 'update:modelValue': [value: string] }>()

const DIAL_CODES = [
  { code: '+91',  country: 'India',          flag: '🇮🇳', maxLen: 10 },
  { code: '+1',   country: 'USA / Canada',   flag: '🇺🇸', maxLen: 10 },
  { code: '+44',  country: 'United Kingdom', flag: '🇬🇧', maxLen: 10 },
  { code: '+61',  country: 'Australia',      flag: '🇦🇺', maxLen: 9  },
  { code: '+971', country: 'UAE',            flag: '🇦🇪', maxLen: 9  },
  { code: '+65',  country: 'Singapore',      flag: '🇸🇬', maxLen: 8  },
  { code: '+60',  country: 'Malaysia',       flag: '🇲🇾', maxLen: 10 },
  { code: '+64',  country: 'New Zealand',    flag: '🇳🇿', maxLen: 9  },
  { code: '+49',  country: 'Germany',        flag: '🇩🇪', maxLen: 11 },
  { code: '+33',  country: 'France',         flag: '🇫🇷', maxLen: 9  },
  { code: '+81',  country: 'Japan',          flag: '🇯🇵', maxLen: 10 },
  { code: '+86',  country: 'China',          flag: '🇨🇳', maxLen: 11 },
]

const dialCode = ref('+91')
const localNumber = ref('')

const selected = computed(() => DIAL_CODES.find(d => d.code === dialCode.value)!)
const maxLen = computed(() => selected.value.maxLen)
const placeholder = computed(() => '0'.repeat(maxLen.value))

onMounted(() => {
  if (!props.modelValue) return
  const sorted = [...DIAL_CODES].sort((a, b) => b.code.length - a.code.length)
  const match = sorted.find(d => props.modelValue.startsWith(d.code))
  if (match) {
    dialCode.value = match.code
    localNumber.value = props.modelValue.slice(match.code.length)
  } else {
    localNumber.value = props.modelValue
  }
})

// Trim to new country's max when switching dial code
watch(dialCode, () => {
  localNumber.value = localNumber.value.slice(0, maxLen.value)
})

function onInput(e: Event) {
  const raw = (e.target as HTMLInputElement).value.replace(/\D/g, '')
  localNumber.value = raw.slice(0, maxLen.value)
}

const fullPhone = computed(() => dialCode.value + localNumber.value)

watch(fullPhone, val => emit('update:modelValue', val))
</script>

<template>
  <div class="phone-input">
    <select v-model="dialCode" class="dial-select">
      <option v-for="d in DIAL_CODES" :key="d.code" :value="d.code">
        {{ d.flag }} {{ d.code }} — {{ d.country }}
      </option>
    </select>
    <input
      type="tel"
      class="number-input"
      :value="localNumber"
      :maxlength="maxLen"
      :placeholder="placeholder"
      @input="onInput"
    />
  </div>
</template>

<style scoped>
.phone-input {
  display: flex;
  gap: 8px;
}

.dial-select {
  font-family: inherit;
  font-size: 15px;
  padding: 10px 10px;
  border: 1.5px solid #ddd;
  border-radius: 8px;
  outline: none;
  background: #fafafa;
  cursor: pointer;
  flex-shrink: 0;
  width: 210px;
  transition: border-color 0.2s;
}

.dial-select:focus {
  border-color: #c0392b;
  background: #fff;
}

.number-input {
  font-family: inherit;
  font-size: 15px;
  padding: 10px 12px;
  border: 1.5px solid #ddd;
  border-radius: 8px;
  outline: none;
  background: #fafafa;
  flex: 1;
  min-width: 0;
  transition: border-color 0.2s;
}

.number-input:focus {
  border-color: #c0392b;
  background: #fff;
}
</style>
