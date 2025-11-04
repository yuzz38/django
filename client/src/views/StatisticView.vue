<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import {useUserStore} from '@/stores/user_store';
import {storeToRefs} from "pinia";
const bookStats = ref(null)
const authorStats = ref(null)
const genreStats = ref(null)
const loading = ref(false)
const error = ref(null)

async function loadBookStats() {
    const response = await axios.get('/api/books/stats/')
    bookStats.value = response.data
}

async function loadAuthorStats() {
    const response = await axios.get('/api/authors/stats/')
    authorStats.value = response.data
}

async function loadGenreStats() {
    const response = await axios.get('/api/genres/stats/')
    genreStats.value = response.data
}

async function loadAllStats() {
  await Promise.all([
      loadBookStats(),
      loadAuthorStats(),
      loadGenreStats()
    ])
}

onMounted(() => {
  loadAllStats()
})
const userStore = useUserStore()

const {
    userInfo,
} = storeToRefs(userStore)

</script>
<template>
  <div class="container mt-4" v-if="userInfo && userInfo.is_authenticated && userInfo.is_staff">
    <h2 class="text-center mb-4">Статистика библиотеки</h2>

 
    <div class="card mb-4" v-if="bookStats">
      <div class="card-header bg-primary text-white">
        <h4> Статистика книг</h4>
      </div>
      <div class="card-body">
        <div class="row text-center">
          <div class="col-md-3 mb-3">
            <div class="stat-card">
              <h3 class="text-primary">{{ bookStats.total_books }}</h3>
              <p class="text-muted">Всего книг</p>
            </div>
          </div>
          <div class="col-md-3 mb-3">
            <div class="stat-card">
              <h3 class="text-success">{{ bookStats.avg_publication_year }}</h3>
              <p class="text-muted">Средний год издания</p>
            </div>
          </div>
          <div class="col-md-3 mb-3">
            <div class="stat-card">
              <h3 class="text-warning">{{ bookStats.oldest_book_year }}</h3>
              <p class="text-muted">Самая старая книга</p>
            </div>
          </div>
          <div class="col-md-3 mb-3">
            <div class="stat-card">
              <h3 class="text-info">{{ bookStats.newest_book_year }}</h3>
              <p class="text-muted">Самая новая книга</p>
            </div>
          </div>
        </div>
       
      </div>
    </div>

   
    <div class="card mb-4" v-if="authorStats">
      <div class="card-header bg-success text-white">
        <h4>Статистика авторов</h4>
      </div>
      <div class="card-body">
        <div class="row text-center">
          <div class="col-md-3 mb-3">
            <div class="stat-card">
              <h3 class="text-primary">{{ authorStats.count }}</h3>
              <p class="text-muted">Всего авторов</p>
            </div>
          </div>
          <div class="col-md-3 mb-3">
            <div class="stat-card">
              <h3 class="text-success">{{ authorStats.avg_books?.toFixed(1) }}</h3>
              <p class="text-muted">Среднее книг на автора</p>
            </div>
          </div>
          <div class="col-md-3 mb-3">
            <div class="stat-card">
              <h3 class="text-warning">{{ authorStats.max_books }}</h3>
              <p class="text-muted">Максимум книг у автора</p>
            </div>
          </div>
          <div class="col-md-3 mb-3">
            <div class="stat-card">
              <h3 class="text-info">{{ authorStats.min_books }}</h3>
              <p class="text-muted">Минимум книг у автора</p>
            </div>
          </div>
        </div>
        <div class="row mt-3">
          <div class="col">
            <div class="alert alert-info">
              <strong>Самый продуктивный автор:</strong><br>
              {{ bookStats.most_popular_author }} ({{ bookStats.books_by_popular_author }} книг)
            </div>
          </div>
        </div>
      
      </div>
    </div>

    <div class="card mb-4" v-if="genreStats">
      <div class="card-header bg-warning text-dark">
        <h4>Статистика жанров</h4>
      </div>
      <div class="card-body">
        <div class="row text-center">
          <div class="col-md-4 mb-3">
            <div class="stat-card">
              <h3 class="text-primary">{{ genreStats.total_genres }}</h3>
              <p class="text-muted">Всего жанров</p>
            </div>
          </div>
          <div class="col-md-4 mb-3">
            <div class="stat-card">
              <h3 class="text-success">{{ genreStats.total_books }}</h3>
              <p class="text-muted">Всего книг</p>
            </div>
          </div>
          <div class="col-md-4 mb-3">
            <div class="stat-card">
              <h3 class="text-danger">{{ genreStats.books_in_popular_genre }}</h3>
              <p class="text-muted">Книг в популярном жанре</p>
            </div>
          </div>
        </div>
        
        <div class="alert alert-info mt-3">
          <strong>Самый популярный жанр:</strong> {{ genreStats.most_popular_genre }}
        </div>
      </div>
    </div>

    

    
  </div>
  <div v-else-if="userInfo && userInfo.is_authenticated">
      <h2 class="mt-2">Это информация для администраторов</h2>
    </div>
    <div v-else>
      <h2 class="mt-2">Пожалуйста, <a href="/">авторизуйтесь</a></h2>
    </div>
</template>
<style scoped> 
</style>