<script setup>
import { defineProps } from 'vue';
import formatTimestamp from '../../js/TimeFormat';

const props = defineProps({
  channel: Object,
  selected: Boolean
});
</script>

<template>
  <li :class="{ 'active': selected }" class="channel-item list-group-item list-group-item-action py-3 lh-sm"
    @click="$emit('selected')">
    <div class="d-flex w-100 justify-content-between align-items-center">
      <h1 class="mb-1 fs-5">{{ channel.name }}</h1>
    </div>
    <div class="d-flex justify-content-between align-items-center">
      <small>{{ formatTimestamp(channel.updated_at) }}</small>
    </div>
  </li>
</template>

<style scoped>
.channel-item {
  cursor: pointer;
}
</style>
