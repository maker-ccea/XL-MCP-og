import { createRouter, createWebHashHistory } from 'vue-router'
import WorkspacePage from '@/pages/WorkspacePage.vue'
import HistoryPage from '@/pages/HistoryPage.vue'
import SettingsPage from '@/pages/SettingsPage.vue'
import ErrorPage from '@/pages/ErrorPage.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', name: 'workspace', component: WorkspacePage },
    { path: '/history', name: 'history', component: HistoryPage },
    { path: '/settings', name: 'settings', component: SettingsPage },
    { path: '/error', name: 'error', component: ErrorPage },
    { path: '/:pathMatch(.*)*', redirect: '/' }
  ]
})

export default router

