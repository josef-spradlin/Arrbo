import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import GameCompareView from '../views/GameCompareView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'dashboard', component: DashboardView },
    { path: '/compare/:gameId', name: 'compare', component: GameCompareView, props: true },
  ],
})

export default router
