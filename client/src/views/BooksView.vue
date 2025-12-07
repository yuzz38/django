<script setup>
import axios from 'axios';
import {computed, onBeforeMount, ref} from 'vue';
import {useUserStore} from '@/stores/user_store';
import { useDataStore } from '@/stores/data_store';
import {storeToRefs} from "pinia";
const userStore = useUserStore()
const dataStore = useDataStore();

const booksToAdd = ref({});
const bookToEdit = ref({});

const { books, genres, authors } = storeToRefs(dataStore);
const {userInfo} = storeToRefs(userStore)
onBeforeMount(async () => {
    dataStore.fetchBooks();
    dataStore.fetchGenres();
    dataStore.fetchAuthors();
})
async function onBookAdd() {
  await axios.post("/api/books/", {
    ...booksToAdd.value,
  });
  await dataStore.fetchBooks(); // переподтягиваю
}
async function onRemoveClickBook(book) {
  if (userInfo.value.is_staff && !userInfo.value.second) {
        alert('Для редактирования требуется двухфакторная аутентификация. Нажмите кнопку "Войти по второму фактору" на главной странице.');
        return;
    }
   await axios.delete(`/api/books/${book.id}/`);
    await dataStore.fetchBooks(); // переподтягиваю
}
async function onBookEditClick(book) {
  bookToEdit.value = { ...book };
}
async function onUpdateBook() {
  await axios.put(`/api/books/${bookToEdit.value.id}/`, {
    ...bookToEdit.value,
  });
  await dataStore.fetchBooks();
}

</script>

<template>
    <div class="border p-5" v-if="userInfo && userInfo.is_authenticated">
          <div class="mb-5" v-if="userInfo && userInfo.is_authenticated && userInfo.is_staff">
            <h3>Добавить книгу</h3>
          <form @submit.prevent.stop="onBookAdd">
              
              <div class="row" style="row-gap: 20px;">
                  <div class="col-4">
                  <div class="form-floating">
                     
                      <input
                      type="text"
                      class="form-control"
                      v-model="booksToAdd.name"
                      required
                      />
                      <label for="floatingInput">Название книги</label>
                  </div>
                  </div>
                  <div class="col-4">
                      <div class="form-floating">
                        <select class="form-select" v-model="booksToAdd.author">
                          <option :value="a.id" v-for="a in authors">
                            {{ a.nameAuthor }}
                          </option>
                        </select>
                        <label for="floatingInput">Автор</label>
                      </div>
                  </div>
                 <div class="col-4">
                    <div class="form-floating">
                      <select class="form-select" v-model="booksToAdd.genres"> 
                        <option :value="g.id" v-for="g in genres" :key="g.id">
                          {{ g.name }}
                        </option>
                      </select>
                      <label for="floatingInput">Жанр</label>
                    </div>
                  </div>
                  <div class="col-4">
                  <div class="form-floating">
                      <input
                      type="number"
                      class="form-control"
                      v-model="booksToAdd.publication_year"
                      required
                      />
                      <label for="floatingInput">Год</label>
                  </div>
                  </div>
                  <div class="col-4">
                  <div class="form-floating">
                      <input
                      type="text"
                      class="form-control"
                      v-model="booksToAdd.description"
                      required
                      />
                      <label for="floatingInput">Описание книги</label>
                  </div>
                  </div>
                  <div class="col-4">
                  <button class="btn btn-primary" style="width: 100%;height: 100%;">
                      Добавить 
                  </button>
                  </div>
              </div>
          </form>
          </div>
          
          <div>
            <h4>Список книг</h4>
            <div class="row">
            <template v-for="item in books">
            <div class="col-3 p-3 border d-flex justify-content-between align-items-center flex-wrap" style="position: relative;">
              <div style="display:block; width:100%;"><h5>Название: </h5></div><div>{{ item.name }}</div>
            
             
                 <button v-if="userInfo && userInfo.is_authenticated && userInfo.is_staff" class="btn btn-danger" @click="onRemoveClickBook(item)">
                    <i class="bi bi-x">x</i>
                </button>
                <div>
                  <h5>Описание: </h5>
                  <ul>
                    <li>{{ item.description }} </li>
                  </ul>
                </div>
                
                <button style="flex:0 0 100%;"v-if="userInfo && userInfo.is_authenticated && userInfo.is_staff"
                    class="btn btn-success mt-2"
                    @click="onBookEditClick(item)"
                    data-bs-toggle="modal"
                    data-bs-target="#editBookModal">
                    <span>Редактировать</span>
                </button>
            </div>
            </template>
        </div>
          </div>
          </div>
          <div v-else>
          <h2 class="mt-2">Пожалуйста, <a href="/">авторизуйтесь</a></h2>
          </div>
          <div class="modal fade" id="editBookModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">
            Редактировать книгу
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
                        <input
                          type="text"
                          class="form-control"
                          v-model="bookToEdit.name"
                        />
                        <label for="floatingInput">Название</label>
                      </div>
              </div>
              <div class="col-6 mb-2">
                        <div class="form-floating">
                          <select class="form-select" v-model="bookToEdit.author">
                            <option :value="a.id" v-for="a in authors">
                              {{ a.nameAuthor }}
                            </option>
                          </select>
                          <label for="floatingInput">Автор</label>
                        </div>
              </div>
              <div class="col-6 mb-2">
                        <div class="form-floating">
                          <select class="form-select" v-model="bookToEdit.genres"> 
                          <option :value="g.id" v-for="g in genre" :key="g.id">
                            {{ g.name }}
                          </option>
                        </select>
                          <label for="floatingInput">Жанр</label>
                        </div>
              </div>
              <div class="col-6 mb-2">
                    <div class="form-floating">
                        <input
                        type="number"
                        class="form-control"
                        v-model="bookToEdit.publication_year"
                        required
                        />
                        <label for="floatingInput">Год</label>
                    </div>
              </div>
              <div class="col-6 mb-2">
                    <div class="form-floating">
                        <input
                        type="text"
                        class="form-control"
                        v-model="bookToEdit.description"
                        required
                        />
                        <label for="floatingInput">Описание книги</label>
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
              @click="onUpdateBook"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
          </div>   
</template>
<style scoped>
.btn-danger {
  position: absolute;
  right: 10px;
  top: 10px;
}
</style>