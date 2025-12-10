import { createRouter, createWebHistory } from 'vue-router'
import ResourceView from '../views/ResourceView.vue'
import QuotationView from '../views/QuotationView.vue'

const routes = [
  {
    path: '/',
    name: 'resource',
    component: ResourceView
  },
  {
    path: '/quotation',
    name: 'quotation',
    component: QuotationView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
