<script setup lang="ts">
import { useRouter } from 'vue-router'

const props = defineProps<{
  userId: string
  firstName: string
  lastName: string
  age: number
  city: string
  state: string
  occupation: string
  religionName: string
  profilePicUrl: string
  isVerified: boolean
}>()

const router = useRouter()

function open() {
  router.push(`/profile/${props.userId}`)
}
</script>

<template>
  <div class="pcard" @click="open">
    <div class="pcard-photo">
      <img v-if="profilePicUrl" :src="profilePicUrl" :alt="`${firstName} ${lastName}`" />
      <div v-else class="pcard-avatar">{{ firstName.charAt(0) }}</div>
      <span v-if="isVerified" class="verified-badge">✓</span>
    </div>
    <div class="pcard-body">
      <p class="pcard-name">{{ firstName }} {{ lastName }}, {{ age }}</p>
      <p class="pcard-meta" v-if="city || state">📍 {{ [city, state].filter(Boolean).join(', ') }}</p>
      <p class="pcard-meta" v-if="occupation">💼 {{ occupation }}</p>
      <p class="pcard-meta" v-if="religionName">🙏 {{ religionName }}</p>
    </div>
  </div>
</template>

<style scoped>
.pcard {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s;
}
.pcard:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.12);
}
.pcard-photo {
  position: relative;
  width: 100%;
  padding-top: 75%;
  background: #f0e8e8;
  overflow: hidden;
}
.pcard-photo img {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  object-fit: cover;
}
.pcard-avatar {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  font-weight: 700;
  color: #c0392b;
  opacity: 0.4;
}
.verified-badge {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: #27ae60;
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 7px;
  border-radius: 20px;
}
.pcard-body {
  padding: 12px 14px 16px;
}
.pcard-name {
  font-size: 15px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 6px;
}
.pcard-meta {
  font-size: 13px;
  color: #666;
  margin-bottom: 3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
