<script setup>
import axios from 'axios';
import {onBeforeMount, ref} from 'vue';
import {useUserStore} from '@/stores/user_store';
import { useDataStore } from '@/stores/data_store';
import {storeToRefs} from "pinia";
const userStore = useUserStore()
const dataStore = useDataStore();

const genreToAdd = ref({});
const genreToEdit = ref({});

const {userInfo} = storeToRefs(userStore)
const { genres } = storeToRefs(dataStore);
onBeforeMount(async () => {
  dataStore.fetchGenres()
})

async function onGenreAdd() {
  await axios.post("/api/genres/", {
    ...genreToAdd.value,
  });
  await dataStore.fetchGenres(); // переподтягиваю
}

async function onRemoveClickGenre(genre) {
  if (userInfo.value.is_staff && !userInfo.value.second) {
        alert('Для редактирования требуется двухфакторная аутентификация. Нажмите кнопку "Войти по второму фактору" на главной странице.');
        return;
    }
   await axios.delete(`/api/genres/${genre.id}/`);
    await dataStore.fetchGenres(); // переподтягиваю
}

async function onGenreEditClick(genre) {
  genreToEdit.value = { ...genre };
}
async function onUpdateGenre() {
  await axios.put(`/api/genres/${genreToEdit.value.id}/`, {
    ...genreToEdit.value,
  });
  await dataStore.fetchGenres();
}
</script>
<template>
  <div class="border p-5" v-if="userInfo && userInfo.is_authenticated">
         <div class="mb-5" v-if="userInfo && userInfo.is_authenticated && userInfo.is_staff">
           <h3>Добавить жанр</h3>
          <form @submit.prevent.stop="onGenreAdd">
              
              <div class="row">
                  <div class="col-5">
                  <div class="form-floating">
                      <!-- ТУТ ПОДКЛЮЧИЛ studentToAdd.name -->
                      <input
                      type="text"
                      class="form-control"
                      v-model="genreToAdd.name"
                      required
                      />
                      <label for="floatingInput">Название жанра</label>
                  </div>
                  </div>
                  <div class="col-5">
                  <div class="form-floating">
                      <input
                      type="text"
                      class="form-control"
                      v-model="genreToAdd.description"
                      required
                      />
                      <label for="floatingInput">Описание</label>
                  </div>
                  </div>
                
                  <div class="col-2">
                  <button class="btn btn-primary" style="width: 100%;height: 100%;">
                      Добавить 
                  </button>
                  </div>
              </div>
          </form>
         </div>
          <h4>Список жанров</h4>
        <div class="row">
            <template v-for="item in genres">
            <div class="col-3 p-3 border d-flex justify-content-between align-items-center flex-wrap">{{ item.name }} 
                
                 <button v-if="userInfo && userInfo.is_authenticated && userInfo.is_staff" class="btn btn-danger" @click="onRemoveClickGenre(item)">
                    <i class="bi bi-x">x</i>
                </button>
                <div style="width: 100%;">
                  Описание:
                  {{ item.description }}
                </div>
                <button style="flex:0 0 100%;"v-if="userInfo && userInfo.is_authenticated && userInfo.is_staff"
                    class="btn btn-success mt-2"
                    @click="onGenreEditClick(item)"
                    data-bs-toggle="modal"
                    data-bs-target="#editGenreModal">
                    <span>Редактировать</span>
                </button>
            </div>
            </template>
        </div>
         </div>
         <div v-else>
      <h2 class="mt-2">Пожалуйста, <a href="/">авторизуйтесь</a></h2>
    </div>
         <div class="modal fade" id="editGenreModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="exampleModalLabel">
           Редактировать жанр
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
            <div class="col">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  v-model="genreToEdit.name"
                />
                <label for="floatingInput">Название жанра</label>
              </div>
            </div>
            <div class="col">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  v-model="genreToEdit.description"
                />
                <label for="floatingInput">Описание жанра</label>
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
            @click="onUpdateGenre"
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