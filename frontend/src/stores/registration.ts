import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useRegistrationStore = defineStore('registration', () => {
  const step = ref(1)

  // Step 1 — Basic & Contact
  const phone_number = ref('')
  const email = ref('')
  const password = ref('')
  const first_name = ref('')
  const last_name = ref('')
  const gender = ref('')
  const dob = ref('')
  const marital_status = ref('')
  const height_cm = ref<number | null>(null)
  const weight_kg = ref<number | null>(null)
  const profile_created_by = ref('self')

  // Step 2 — Personal & Religion
  const mother_tongue = ref('')
  const religion_id = ref<number | null>(null)
  const caste_id = ref<number | null>(null)
  const caste_name = ref('')
  const sub_caste = ref('')
  const nakshatra = ref('')
  const rashi = ref('')
  const is_manglik = ref<boolean | null>(null)

  // Step 3 — Education & Career
  const education_level = ref('')
  const college = ref('')
  const occupation = ref('')
  const company = ref('')
  const annual_income = ref<number | null>(null)
  const work_location = ref('')

  // Step 4 — Family
  const father_name = ref('')
  const father_occupation = ref('')
  const mother_name = ref('')
  const mother_occupation = ref('')
  const brothers_count = ref(0)
  const sisters_count = ref(0)
  const family_type = ref('')
  const family_status = ref('')

  // Step 5 — Partner Preferences
  const partner_preferences = ref({
    age_min: 18,
    age_max: 40,
    height_min_cm: null as number | null,
    height_max_cm: null as number | null,
    acceptable_religions: [] as number[],
    acceptable_castes: [] as number[],
    preferred_education: '',
    preferred_profession: '',
    preferred_location: '',
  })

  // Step 6 — Lifestyle, Photos & Location
  const eating_habit = ref('')
  const smoking_habit = ref('')
  const drinking_habit = ref('')
  const hobbies = ref<string[]>([])
  const bio = ref('')
  const photo_privacy = ref('public')
  const profile_pic_url = ref('')
  const city = ref('')
  const state = ref('')
  const country = ref('India')
  const postal_code = ref('')

  function nextStep() { step.value++ }
  function prevStep() { step.value-- }
  function goToStep(n: number) { step.value = n }

  function toPayload() {
    return {
      phone_number: phone_number.value,
      email: email.value,
      password: password.value,
      first_name: first_name.value,
      last_name: last_name.value,
      gender: gender.value,
      dob: dob.value,
      marital_status: marital_status.value,
      height_cm: height_cm.value,
      weight_kg: weight_kg.value,
      profile_created_by: profile_created_by.value,
      mother_tongue: mother_tongue.value,
      religion_id: religion_id.value,
      caste_id: caste_id.value,
      caste_name: caste_name.value,
      sub_caste: sub_caste.value,
      nakshatra: nakshatra.value,
      rashi: rashi.value,
      is_manglik: is_manglik.value,
      education_level: education_level.value,
      college: college.value,
      occupation: occupation.value,
      company: company.value,
      annual_income: annual_income.value,
      work_location: work_location.value,
      father_name: father_name.value,
      father_occupation: father_occupation.value,
      mother_name: mother_name.value,
      mother_occupation: mother_occupation.value,
      brothers_count: brothers_count.value,
      sisters_count: sisters_count.value,
      family_type: family_type.value,
      family_status: family_status.value,
      partner_preferences: partner_preferences.value,
      eating_habit: eating_habit.value,
      smoking_habit: smoking_habit.value,
      drinking_habit: drinking_habit.value,
      hobbies: hobbies.value,
      bio: bio.value,
      photo_privacy: photo_privacy.value,
      city: city.value,
      state: state.value,
      country: country.value,
      postal_code: postal_code.value,
    }
  }

  function reset() {
    step.value = 1
    phone_number.value = ''
    email.value = ''
    password.value = ''
    first_name.value = ''
    last_name.value = ''
    gender.value = ''
    dob.value = ''
    marital_status.value = ''
    height_cm.value = null
    weight_kg.value = null
    profile_created_by.value = 'self'
    mother_tongue.value = ''
    religion_id.value = null
    caste_id.value = null
    caste_name.value = ''
    sub_caste.value = ''
    nakshatra.value = ''
    rashi.value = ''
    is_manglik.value = null
    education_level.value = ''
    college.value = ''
    occupation.value = ''
    company.value = ''
    annual_income.value = null
    work_location.value = ''
    father_name.value = ''
    father_occupation.value = ''
    mother_name.value = ''
    mother_occupation.value = ''
    brothers_count.value = 0
    sisters_count.value = 0
    family_type.value = ''
    family_status.value = ''
    partner_preferences.value = { age_min: 18, age_max: 40, height_min_cm: null, height_max_cm: null, acceptable_religions: [], acceptable_castes: [], preferred_education: '', preferred_profession: '', preferred_location: '' }
    eating_habit.value = ''
    smoking_habit.value = ''
    drinking_habit.value = ''
    hobbies.value = []
    bio.value = ''
    photo_privacy.value = 'public'
    profile_pic_url.value = ''
    city.value = ''
    state.value = ''
    country.value = 'India'
    postal_code.value = ''
  }

  return {
    step, phone_number, email, password, first_name, last_name, gender, dob,
    marital_status, height_cm, weight_kg, profile_created_by, mother_tongue,
    religion_id, caste_id, caste_name, sub_caste, nakshatra, rashi, is_manglik,
    education_level, college, occupation, company, annual_income, work_location,
    father_name, father_occupation, mother_name, mother_occupation,
    brothers_count, sisters_count, family_type, family_status,
    partner_preferences, eating_habit, smoking_habit, drinking_habit, hobbies,
    bio, photo_privacy, profile_pic_url, city, state, country, postal_code,
    nextStep, prevStep, goToStep, toPayload, reset,
  }
}, {
  persist: { storage: sessionStorage },
})
