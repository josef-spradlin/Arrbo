<template>
  <div>
    <h2>Game Compare</h2>
    <p>Game ID: <code>{{ gameId }}</code></p>
    <p>Next: call <code>/api/games/{{ gameId }}/compare</code> (or similar) to render matchups.</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{ gameId: string }>()
</script>
