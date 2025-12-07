<script setup>
import axios from 'axios';
import {computed, onBeforeMount, ref} from 'vue';
import {useUserStore} from '@/stores/user_store';
import { useDataStore } from '@/stores/data_store';
import {storeToRefs} from "pinia";
const userStore = useUserStore()
const dataStore = useDataStore()

const selectedReader = ref(null); 
const booksToAddItem = ref({});
const bookToEditItem = ref({});

const {userInfo} = storeToRefs(userStore)
const { books , readers , bookItem } = storeToRefs(dataStore);

onBeforeMount(async () => {
  dataStore.fetchReaders()
  dataStore.fetchBooks()
  dataStore.fetchBookItem()
})

const filteredBookItems = computed(() => {
  if (!selectedReader.value) {
    return bookItem.value;
  }
  return bookItem.value.filter(item => item.borrower === parseInt(selectedReader.value));
});
async function onBookAddItem() {
  await axios.post("/api/bookinstances/", {
    ...booksToAddItem.value,
  });
  await dataStore.fetchBookItem(); // переподтягиваю
}
async function onRemoveClickBookItem(bookItem) {
  if (userInfo.value.is_staff && !userInfo.value.second) {
        alert('Для редактирования требуется двухфакторная аутентификация. Нажмите кнопку "Войти по второму фактору" на главной странице.');
        return;
    }
  await axios.delete(`/api/bookinstances/${bookItem.id}/`);
  await dataStore.fetchBookItem(); // переподтягиваю
}
async function onBookEditClickItem(book) {
  bookToEditItem.value = { ...book };
}
async function onUpdateBookItem() {
  await axios.put(`/api/bookinstances/${bookToEditItem.value.id}/`, {
    ...bookToEditItem.value,
  });
  await dataStore.fetchBookItem();
}
</script>
<template>
        <div class="border p-5" v-if="userInfo && userInfo.is_authenticated">
          <div>
            <h3 v-if="userInfo && userInfo.is_authenticated && userInfo.is_staff">Выдать книгу</h3>
            <h3 v-else-if="userInfo && userInfo.is_authenticated">Взять книгу</h3>
            <form @submit.prevent.stop="onBookAddItem">
                <div class="row">
            <div class="col-3">
                <div class="form-floating">
                  <select class="form-select" v-model="booksToAddItem.book" required>
                    <option :value="b.id" v-for="b in books" :key="b.id">
                      {{ b.name }}
                    </option>
                  </select>
                  <label for="floatingInput">Книга</label>
                </div>
            </div>
            <div class="col-2">
                      <div class="form-floating">
                        <select class="form-select" v-model="booksToAddItem.status"> 
                        
                          <option value="borrowed">Выдана</option>
                        </select>
                        <label for="floatingInput">Статус</label>
                      </div>
            </div>
            <div class="col-2">
                  <div class="form-floating">
                      <input
                      type="date"
                      class="form-control"
                      v-model="booksToAddItem.due_back"
                      required
                      />
                      <label for="floatingInput">Дата возврата</label>
                  </div>
            </div>
            <div class="col-3">
                <div class="form-floating">
                  <select class="form-select" v-model="booksToAddItem.borrower" required>
                    <option :value="b.id" v-for="b in readers">
                      {{ b.first_name }}  {{ b.last_name }}
                    </option>
                  </select>
                  <label for="floatingInput">Читатель</label>
                </div>
            </div>
          
                 <div class="col-2" v-if="userInfo && userInfo.is_authenticated && userInfo.is_staff">
                  <button class="btn btn-primary"  style="width: 100%;height: 100%;">
                      Выдать 
                  </button>
                  </div>
                     <div class="col-2" v-else-if="userInfo && userInfo.is_authenticated">
                  <button class="btn btn-primary"  style="width: 100%;height: 100%;">
                      Взять 
                  </button>
                  </div>
          </div>
           
          </form>
          </div>

         
          <div class="mt-4" v-if="userInfo && userInfo.is_authenticated && userInfo.is_staff">
            <h4>Фильтр по читателю</h4>
            <div class="row">
              <div class="col-6">
                <div class="form-floating">
                  <select class="form-select" v-model="selectedReader">
                    <option value="">Все читатели</option>
                    <option :value="reader.id" v-for="reader in readers" :key="reader.id">
                      {{ reader.first_name }} {{ reader.last_name }}
                    </option>
                  </select>
                  <label for="floatingInput">Выберите читателя</label>
                </div>
              </div>
            
            </div>
          </div>

          <h4 class="mt-5" v-if="userInfo && userInfo.is_authenticated && userInfo.is_staff">Состояние книг</h4>
          <h4 class="mt-5" v-else-if="userInfo && userInfo.is_authenticated">Мои книги</h4>
          
          
          <div v-if="selectedReader && userInfo && userInfo.is_authenticated && userInfo.is_staff" class="alert alert-info">
            Показаны книги читателя: 
            <strong>
              {{ readers.find(r => r.id === parseInt(selectedReader))?.first_name }} 
              {{ readers.find(r => r.id === parseInt(selectedReader))?.last_name }}
            </strong>
          </div>

            <div class="row">
                <template v-for="item in filteredBookItems">
                <div class="col-3 p-3 border d-flex justify-content-between align-items-center flex-wrap">{{ books.find(b => b.id === item.book)?.name || 'Книга' }}  <br> <hr>
                
                    
                    <button v-if="userInfo && userInfo.is_authenticated && userInfo.is_staff"class="btn btn-danger" @click="onRemoveClickBookItem(item)">
                        <i class="bi bi-x">x</i>
                    </button>
                    <div style="width:100%;">
                          <span v-if="item.status === 'available'">На полке</span>
                    <span v-else-if="item.status === 'borrowed'">Выдана</span>
                    <span v-else-if="item.status === 'maintenance'">В ремонте</span>
                    <span v-else>{{ item.status }}</span>
                    </div>
                    <div class="mt-2 mb-2" style="width:100%;">
                      Читатель - {{ readers.find(r => r.id === item.borrower)?.first_name }} {{ readers.find(r => r.id === item.borrower)?.last_name }}
                    </div>
                    <button style="flex:0 0 100%;" v-if="userInfo && userInfo.is_authenticated && userInfo.is_staff"
                        class="btn btn-success mt-2"
                        @click="onBookEditClickItem(item)"
                        data-bs-toggle="modal"
                        data-bs-target="#editBookModalItem">
                        <span>Редактировать</span>
                    </button>
                     
                </div>
                
                </template>
            </div>

         
         
        </div>
        <div v-else>
          <h2 class="mt-2">Пожалуйста, <a href="/">авторизуйтесь</a></h2>
        </div>  
         <div class="modal fade" id="editBookModalItem" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="exampleModalLabel">
           Редактировать состояние книги
          </h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col-6 mb-2">
                <div class="form-floating">
                  <select class="form-select" v-model="bookToEditItem.book" required>
                    <option :value="b.id" v-for="b in books" :key="b.id">
                      {{ b.name }}
                    </option>
                  </select>
                  <label for="floatingInput">Книга</label>
                </div>
            </div>
            <div class="col-6 mb-2">
                      <div class="form-floating">
                        <select class="form-select" v-model="bookToEditItem.status"> 
                          <option value="available">На полке</option>
                          <option value="borrowed">Выдана</option>
                          <option value="maintenance">В ремонте</option>
                        </select>
                        <label for="floatingInput">Статус</label>
                      </div>
            </div>
            <div class="col-6 mb-2">
                  <div class="form-floating">
                      <input
                      type="date"
                      class="form-control"
                      v-model="bookToEditItem.due_back"
                      required
                      />
                      <label for="floatingInput">Дата возврата</label>
                  </div>
            </div>
             <div class="col-6 mb-2">
                <div class="form-floating">
                  <select class="form-select" v-model="bookToEditItem.borrower" required>
                    <option :value="b.id" v-for="b in readers" :key="b.id">
                      {{ b.first_name }}  {{ b.last_name }}
                    </option>
                  </select>
                  <label for="floatingInput">Читатель</label>
                </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button
            data-bs-dismiss="modal"
            type="button"
            class="btn btn-primary"
            @click="onUpdateBookItem"
          >
            Сохранить
          </button>
        </div>
      </div>
    </div>
</div>
</template>
<style scoped>
</style>