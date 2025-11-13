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
const showImageModal = ref(false);
const currentImageUrl = ref('');
function openImageModal(imageUrl) {
  currentImageUrl.value = imageUrl;
  showImageModal.value = true;
}

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

const uniqueGenres = computed(() => {
  const seen = new Set();
  return genre.value.filter(item => {
    if (seen.has(item.name)) {
      return false;
    }
    seen.add(item.name);
    return true;
  });
});

const showAllAuthorsModal = ref(false);
const showAllBooksModal = ref(false);


const paginatedAuthors = computed(() => {
  return authors.value.slice(0, 10);
});
const paginatedBooks = computed(() => {
  return books.value.slice(0, 10);
});



function openAllAuthorsModal() {
  showAllAuthorsModal.value = true;
}
function openAllBooksModal() {
  showAllBooksModal.value = true;
}


async function exportBooksToExcel() {
        const response = await axios.get('/api/books/export-excel/', {
            responseType: 'blob' 
        });
        
        // Создаем ссылку для скачивания
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'library_books.xlsx');
        document.body.appendChild(link);
        link.click();
        
        link.remove();
        window.URL.revokeObjectURL(url);
        
    
}
</script>
<template>

 
   <div class="container mt-5">
        <div v-if="userInfo && userInfo.is_authenticated" class="container mt-5">
            <h3>Здравствуй, {{userInfo.username}}</h3>
        </div>
     <h1 class="text-center"> Библиотечка </h1>
    
        <div class="card mb-4" v-if="userInfo && userInfo.is_authenticated">
            <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
                <h2>Авторы</h2>
                <button @click="openAllAuthorsModal" class="btn btn-light btn-sm">
                    Показать всех ({{ authors.length }})
                </button>
            </div>
            <div class="card-body">
                <div class="row">
                    <template v-for="author in paginatedAuthors" :key="author.id">
                         <div class="col-md-6 mb-3">
                            <div class="card">
                                <div class="card-body">
                                    <div class="row">
                                      <div class="col-8">
                                        <h5 class="card-title">{{ author.nameAuthor }}</h5>
                                        <p class="card-text">{{ author.bio }}</p>
                                      </div>
                                      <div class="col-4" style="text-align: right;">
                                       <img :src="author.picture" @click="openImageModal(author.picture)" style="max-width:100px; border-radius:20px; max-height:100px;height:100px;  cursor: pointer; "/>
                                      </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>
                
             
            </div>
        </div>
        
        <div class="card mb-4" v-if="userInfo && userInfo.is_authenticated">
            <div class="card-header bg-success text-white">
                <h2>Жанры</h2>
            </div>
            <div class="card-body">
                <div class="row">
                    <template v-for="genre in uniqueGenres" :key="genre.id">
                          <div class="col-md-4 mb-3">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">{{ genre.name }}</h5>
                                <p class="card-text">{{ genre.description }}</p>
                            </div>
                        </div>
                    </div>
                    </template>
                </div>
            </div>
        </div>
        <div class="card mb-4" v-if="userInfo && userInfo.is_authenticated">
            <div class="card-header bg-warning d-flex justify-content-between align-items-center">
                <h2>Книги</h2>
                <div>
                    <button @click="openAllBooksModal" class="btn btn-light btn-sm">
                    Показать все ({{ books.length }})
                </button>
                <button @click="exportBooksToExcel" class="btn btn-success btn-sm me-2" style="margin-left:20px">
                    <i class="bi bi-file-earmark-excel"></i> Экспорт в Excel
                </button>
                </div>
            </div>
            <div class="card-body">
                <div class="row">
                    <template v-for="book in paginatedBooks">
                        <div class="col-md-6 mb-3">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">{{ book.name }}</h5>
                                <p class="card-text">
                                    <strong>Автор:</strong>   {{ authors.find(a => a.id === book.author)?.nameAuthor }} <br>

                                    <strong>Год:</strong> {{ book.publication_year }}<br>
                                   <strong>Жанр: </strong> 
                                    {{ genre.find(g => g.id === book.genres)?.name || 'Не указан' }}
                                 
                                           
                                       
                                    <br>
                                    <strong>Описание:</strong> {{ book.description }}
                                </p>
                            </div>
                        </div>
                    </div>
                    </template>
                </div>
            </div>
        </div>
          <div class="card mb-4"  v-if="userInfo && userInfo.is_authenticated && userInfo.is_staff">
            <div class="card-header bg-info text-white">
                <h2>Читатели</h2>
            </div>
            <div class="card-body">
                <div class="row">
                    <template v-for="reader in readers" >
                         <div class="col-md-4 mb-3">
                        <div class="card">
                            <div class="card-body">
                                
                                <div class="row">
                                    <div class="col-4" style="text-align: left;">
                                    <img :src="reader.picture" @click="openImageModal(reader.picture)" style="max-width:100px; border-radius:20px; max-height:100px;height:100px; cursor: pointer; "/>
                                  </div>
                                    <div class="col-8">
                                        <h5 class="card-title">{{ reader.first_name }} {{ reader.last_name }}</h5>
                                        <p class="card-text">
                                            <strong>Email:</strong> {{ reader.email }}<br>
                                            <strong>Номер билета:</strong> {{ reader.card_number }}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    </template>
                </div>
            </div>
        </div>
         <div class="card mb-4"  v-if="userInfo && userInfo.is_authenticated  && userInfo.is_staff" > 
            <div class="card-header bg-secondary text-white">
                <h2>Состояния книг</h2>
            </div>
            <div class="card-body">
                <div class="row">
                    <template v-for="instance in bookItem">
                        <div class="col-md-6 mb-3">
                        <div class="card">
                          <div class="card-body">
                                <h5 class="card-title">{{ books.find(b => b.id === instance.book)?.name }}</h5>
                                <p class="card-text">
                                    <strong>Статус: </strong> 
                                    <span>
                                        {{ 
                                            instance.status === 'available' ? 'На полке' :
                                            instance.status === 'borrowed' ? 'Выдана' :
                                            instance.status === 'maintenance' ? 'В ремонте' :
                                            instance.status
                                        }}
                                    </span><br>
                                    <strong>Дата возврата: </strong> 
                                    <span>
                                        {{ instance.due_back || 'Не указана' }}
                                    </span><br>
                                    <strong>Читатель: </strong> 
                                    <span>
                                        {{ readers.find(r => r.id === instance.borrower) ? `${readers.find(r => r.id === instance.borrower).first_name} ${readers.find(r => r.id === instance.borrower).last_name}` : 'Не выдана' }}
                                    </span>
                                </p>
                            </div>
                        </div>
                    </div>
                    </template>
               
                </div>
            </div>
        </div>
   </div>

<div v-if="showImageModal" class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.5)">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Просмотр изображения</h5>
          <button
            type="button"
            class="btn-close"
            @click="showImageModal = false"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body text-center">
          <img :src="currentImageUrl" style="max-width: 100%; border-radius: 10px; max-height: 80vh; object-fit: contain;"/>
        </div>
      </div>
    </div>
</div>
 <div v-if="showAllAuthorsModal" class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.5)">
        <div class="modal-dialog modal-xl">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Все авторы ({{ authors.length }})</h5>
              <button
                type="button"
                class="btn-close"
                @click="showAllAuthorsModal = false"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
                <div class="row">
                    <template v-for="author in authors" :key="author.id">
                         <div class="col-md-6 mb-3">
                            <div class="card">
                                <div class="card-body">
                                    <div class="row">
                                      <div class="col-8">
                                        <h6 class="card-title">{{ author.nameAuthor }}</h6>
                                        <p class="card-text small">{{ author.bio }}</p>
                                      </div>
                                      <div class="col-4" style="text-align: right;">
                                       <img :src="author.picture" style="max-width:80px; border-radius:15px; max-height:80px;height:80px; cursor: pointer; "/>
                                      </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="showAllAuthorsModal = false">
                    Закрыть
                </button>
            </div>
          </div>
        </div>
   </div>
 <div v-if="showAllBooksModal" class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.5)">
        <div class="modal-dialog modal-xl">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Все книги ({{ books.length }})</h5>
              <button
                type="button"
                class="btn-close"
                @click="showAllBooksModal = false"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
                <div class="row">
                    <template v-for="book in books" :key="book.id">
                         <div class="col-md-6 mb-3">
                            <div class="card">
                               <div class="card-body">
                                    <h5 class="card-title">{{ book.name }}</h5>
                                    <p class="card-text">
                                        <strong>Автор:</strong>   {{ authors.find(a => a.id === book.author)?.nameAuthor }} <br>

                                        <strong>Год:</strong> {{ book.publication_year }}<br>
                                    <strong>Жанр: </strong> 
                                        {{ genre.find(g => g.id === book.genres)?.name || 'Не указан' }}
                                    
                                            
                                        
                                        <br>
                                        <strong>Описание:</strong> {{ book.description }}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="showAllBooksModal = false">
                    Закрыть
                </button>
            </div>
          </div>
        </div>
   </div>

<div v-if="userInfo && !userInfo.is_authenticated" class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.5)">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Пожалуйста, авторизуйтесь как администратор или читатель</h5>
         
        </div>
        <div class="modal-body text-center">
         <div v-if="userInfo && !userInfo.is_authenticated" class="container">
        <form
            @submit.stop.prevent="onFormSend"
            style="display: flex; gap: 8px; align-items: center; justify-content: center; padding: 8px; width: 100%">

            <input v-model="username" type="text" placeholder="username" required class="input-group-text" style="flex: auto;">
            <input v-model="password" type="password" placeholder="password" required class="input-group-text"  style="flex: auto;">

            <button type="submit" class="btn btn-primary">Отправить</button>
        </form>
    </div>
        </div>
      </div>
    </div>
</div>
   

  

  
</template>
<style scoped>
</style>