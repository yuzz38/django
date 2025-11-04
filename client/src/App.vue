<script setup>
import axios from 'axios';
import Cookies from 'js-cookie';

import {computed, onBeforeMount, ref} from 'vue';
import {useUserStore} from '@/stores/user_store';
import {storeToRefs} from "pinia";

const readers = ref([]);
const books = ref([]);
const genre = ref([]);
const authors = ref([]);
const bookItem = ref([]);

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})
async function fetchReaders() {
    const l = await axios.get("/api/readers");
    readers.value = l.data    
}
async function fetchBooks() {
    const l = await axios.get("/api/books");
    books.value = l.data    
}
async function fetchGenre() {
    const l = await axios.get("/api/genres");
    genre.value = l.data    
}
async function fetchAuthor() {
    const l = await axios.get("/api/authors");
    authors.value = l.data    
}
async function fetchBookItem() {
    const l = await axios.get("/api/bookinstances");
    bookItem.value = l.data    
}
onBeforeMount(async () => {
    await fetchReaders()
    await fetchBooks()
    await fetchGenre()
    await fetchAuthor()
    await fetchBookItem()
})
const userStore = useUserStore()

const username = ref();
const password = ref();
const {
    userInfo,
} = storeToRefs(userStore)
async function onFormSend() {
    userStore.login(username.value, password.value)
}
async function handleLogout() {
    await userStore.logout();
}

</script>
<template>

  <nav class="navbar navbar-expand-lg bg-body-tertiary">

  <div class="container">
    
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link class="nav-link" to="/">Главная</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/authors">Авторы</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/books">Книги</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/genres">Жанры</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/readers">Читатели</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/bookinstances">Экземпляры книг</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/statistic">Статистика</router-link>
        </li>
        
      </ul>
      <ul class="navbar-nav">
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Пользователь</a>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="/admin">Админка</a></li>
            <li><a class="dropdown-item" href="#" @click="handleLogout">Выйти</a></li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
  
</nav>

    

  <div class="container">
    
    <router-view/>
  </div>

</template>
<style scoped>
</style>