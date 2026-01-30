<template>
  <div style="padding: 16px;">
    <header style="display:flex; align-items:center; gap:12px; margin-bottom: 16px;">
      <strong>Arrbo</strong>
      <nav style="display:flex; gap:10px;">
        <RouterLink to="/">Dashboard</RouterLink>
        <RouterLink to="/league-leaders">League Leaders</RouterLink>
      </nav>
    </header>

    <RouterView />
  </div>
</template>

<script setup lang="ts"></script>
