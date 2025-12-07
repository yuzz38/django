<script setup>
import axios from 'axios';
import {computed, onBeforeMount, ref,watch} from 'vue';
import {useUserStore} from '@/stores/user_store';
import { useDataStore } from '@/stores/data_store';
import QRCode from 'qrcode';
import {storeToRefs} from "pinia";
const userStore = useUserStore()
const dataStore = useDataStore();

const showImageModal = ref(false);
const currentImageUrl = ref('');
const username = ref();
const password = ref();
const showAllAuthorsModal = ref(false);
const showAllBooksModal = ref(false);

const key = ref('');
const show2FAModal = ref(false);
const qrcodeUrl = ref();
const totpUrl = ref();

const { books, genres, authors, bookItem, readers } = storeToRefs(dataStore);
const {userInfo} = storeToRefs(userStore)


onBeforeMount(async () => {
    dataStore.fetchReaders()
    dataStore.fetchBooks()
    dataStore.fetchGenres()
    dataStore.fetchAuthors()
    dataStore.fetchBookItem()
})
function openImageModal(imageUrl) {
  currentImageUrl.value = imageUrl;
  showImageModal.value = true;
}

async function onFormSend() {
    userStore.login(username.value, password.value)
}


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
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'library_books.xlsx');
        document.body.appendChild(link);
        link.click();  
        link.remove();
        window.URL.revokeObjectURL(url);   
}

function open2FAModal() {
  show2FAModal.value = true;
}
async function onActivate() {
    await axios.post("/api/user/second-login/", {
        key: key.value  
    })
    await userStore.checkLogin();  
    if (userInfo.value.second) {
        show2FAModal.value = false;
    }
}
async function getTotpKey() {
    let r = await axios.get('/api/user/get-totp/')
    totpUrl.value = r.data.url;
}
watch(totpUrl, async () => {
    qrcodeUrl.value = await QRCode.toDataURL(totpUrl.value);
})

</script>
<template>


   <div class="container mt-5">
        <div v-if="userInfo && userInfo.is_authenticated" class="container mt-5">
            <h3>Здравствуй, {{userInfo.username}}</h3>
            <div v-if="userInfo.second" class="alert alert-success mt-2">
                Двухфакторная аутентификация активна
            </div>
            <div v-if="userInfo.is_staff && !userInfo.second" class="alert alert-warning mt-2 d-flex justify-content-between align-items-center">
                <span>Для редактирования данных требуется двухфакторная аутентификация</span>
                <button @click="open2FAModal" class="btn btn-primary btn-sm">
                    Войти по второму фактору
                </button>
            </div>
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
                    <template v-for="genre in genres" :key="genre.id">
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
                                        <strong>Автор:</strong> 
                                        {{ (authors || []).find(a => a.id === book.author)?.nameAuthor || 'Не указан' }} 
                                        <br>
                                        
                                        <strong>Год:</strong> {{ book.publication_year }}<br>
                                        
                                        <strong>Жанр:</strong> 
                                        {{ (genres || []).find(g => g.id === book.genres)?.name || 'Не указан' }}
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
                                        <strong>Автор:</strong> 
                                        {{ (authors || []).find(a => a.id === book.author)?.nameAuthor || 'Не указан' }} 
                                        <br>
                                        
                                        <strong>Год:</strong> {{ book.publication_year }}<br>
                                        
                                        <strong>Жанр:</strong> 
                                        {{ (genres || []).find(g => g.id === book.genres)?.name || 'Не указан' }}
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
<div v-if="show2FAModal" class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.5)">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Двухфакторная аутентификация</h5>
                <button
                    type="button"
                    class="btn-close"
                    @click="show2FAModal = false"
                    aria-label="Close"
                ></button>
            </div>
            <div class="modal-body">
                <input type="text" v-model="key" class="form-control mb-2" placeholder="Введите 6-значный код">
                <button @click="onActivate" class="btn btn-primary mb-2">Активировать второй фактор</button>
                
               
            </div>
            <button @click="getTotpKey">Запросить ключ</button>
            <br>
            <div style="padding: 1rem  0">{{ totpUrl  }}</div>
            <br>
            <img :src="qrcodeUrl" alt="">
            <div class="modal-footer">
                <button
                    type="button"
                    class="btn btn-secondary"
                    @click="show2FAModal = false"
                >
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