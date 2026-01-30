import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/DashboardView.vue'
import GameCompareView from '@/views/GameCompareView.vue'
import LeagueLeadersView from '@/views/LeagueLeadersView.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'dashboard', component: DashboardView },
    {
      path: '/game/:gameId',
      name: 'gameCompare',
      component: GameCompareView,
      props: route => ({
        gameId: route.params.gameId,
        home: route.query.home,
        away: route.query.away,
        date: route.query.date,
      }),
    },
    { path: '/league-leaders', name: 'leagueLeaders', component: LeagueLeadersView },
  ],
})
