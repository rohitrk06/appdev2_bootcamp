import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/logout',
      name: 'logout',
      component: () => import('../views/LogoutView.vue')
    },
    {
      path:'/add_product',
      name: 'add_product',
      component: () => import('../views/AddProduct.vue')
    },
    {
      path:'/add_category',
      name: 'add_category',
      component: () => import('../views/AddCategory.vue')
    }, 
    {
      path:'/update_product/:id',
      name: 'update_product',
      component: () => import('../views/EditProduct.vue')
    }
  ]
})

export default router
