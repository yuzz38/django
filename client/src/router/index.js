
import AuthorsView from '@/views/AuthorsView.vue'
import BookinstancesView from '@/views/BookinstancesView.vue'
import BooksView from '@/views/BooksView.vue'
import GenresView from '@/views/GenresView.vue'
import LibraryView from '@/views/LibraryView.vue'
import ReadersView from '@/views/ReadersView.vue'
import StatisticView from '@/views/StatisticView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: LibraryView
  },
    {
      path: '/authors',
      component: AuthorsView
  },
    {
      path: '/books',
      component: BooksView
  },
    {
      path: '/readers',
      component: ReadersView
  },
    {
      path: '/genres',
      component: GenresView
  },
    {
      path: '/bookinstances',
      component: BookinstancesView
  },{
      path: '/statistic',
      component: StatisticView
  }],
  
})

export default router
