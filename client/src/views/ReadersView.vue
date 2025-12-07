<script setup>
import axios from 'axios';
import {onBeforeMount, ref} from 'vue';
import {useUserStore} from '@/stores/user_store';
import { useDataStore } from '@/stores/data_store';
import {storeToRefs} from "pinia";
const userStore = useUserStore()
const dataStore = useDataStore();

const readerToAdd = ref({});
const readerPictureRef = ref();
const readerImageUrl = ref();
const readerToEdit = ref({});
const readerEditPictureRef = ref();
const readerEditImageUrl = ref();

const {userInfo} = storeToRefs(userStore)
const {readers } = storeToRefs(dataStore);

onBeforeMount(async () => {
  dataStore.fetchReaders()
})
async function readerAddPictureChange() {
  readerImageUrl.value = URL.createObjectURL(readerPictureRef.value.files[0])
}
async function onReaderAdd() {
  const formData = new FormData();
  formData.set('first_name', readerToAdd.value.first_name);
  formData.set('last_name', readerToAdd.value.last_name);
  formData.set('email', readerToAdd.value.email);
  formData.set('card_number', readerToAdd.value.card_number);
  if (readerPictureRef.value.files[0]) {
     formData.append('picture', readerPictureRef.value.files[0]);
  }
  await axios.post("/api/readers/",formData);
  await dataStore.fetchReaders(); // переподтягиваю
}
async function onRemoveClick(reader) {
  if (userInfo.value.is_staff && !userInfo.value.second) {
        alert('Для редактирования требуется двухфакторная аутентификация. Нажмите кнопку "Войти по второму фактору" на главной странице.');
        return;
    }
  await axios.delete(`/api/readers/${reader.id}/`);
  await dataStore.fetchReaders(); // переподтягиваю
}

async function readerEditPictureChange() {
  if (readerEditPictureRef.value.files[0]) {
    readerEditImageUrl.value = URL.createObjectURL(readerEditPictureRef.value.files[0])
  }
}
async function onReaderEditClick(reader) {
  readerToEdit.value = { ...reader };
  readerEditImageUrl.value = null; 
}
async function onUpdateReader() {
  const formData = new FormData();
  if (readerEditPictureRef.value.files[0]) {
    formData.append('picture', readerEditPictureRef.value.files[0]);
  }
  formData.set('first_name', readerToEdit.value.first_name);
  formData.set('last_name', readerToEdit.value.last_name);
  formData.set('email', readerToEdit.value.email);
  formData.set('card_number', readerToEdit.value.card_number);
  await axios.put(`/api/readers/${readerToEdit.value.id}/`, formData);
  await dataStore.fetchReaders();

}


</script>
<template>
  <div class="border p-5" v-if="userInfo && userInfo.is_authenticated">
        <div class="mb-5" v-if="userInfo && userInfo.is_authenticated && userInfo.is_staff">
          <h3>Добавить читателя</h3>
        <form @submit.prevent.stop="onReaderAdd">
            
            <div class="row">
                <div class="col">
                <div class="form-floating">
                    <!-- ТУТ ПОДКЛЮЧИЛ studentToAdd.name -->
                    <input
                    type="text"
                    class="form-control"
                    v-model="readerToAdd.first_name"
                    required
                    />
                    <label for="floatingInput">Имя</label>
                </div>
                </div>
                <div class="col">
                <div class="form-floating">
                    <!-- ТУТ ПОДКЛЮЧИЛ studentToAdd.name -->
                    <input
                    type="text"
                    class="form-control"
                    v-model="readerToAdd.last_name"
                    required
                    />
                    <label for="floatingInput">Фамилия</label>
                </div>
                </div>
                <div class="col">
                <div class="form-floating">
                    <!-- ТУТ ПОДКЛЮЧИЛ studentToAdd.name -->
                    <input
                    type="email"
                    class="form-control"
                    v-model="readerToAdd.email"
                    required
                    />
                    <label for="floatingInput">Почта</label>
                </div>
                </div>
                <div class="col">
                <div class="form-floating">
                    <!-- ТУТ ПОДКЛЮЧИЛ studentToAdd.name -->
                    <input
                    type="number"
                    class="form-control"
                    v-model="readerToAdd.card_number"
                    required
                    />
                    <label for="floatingInput">Номер билета</label>
                </div>
                </div>
                <div class="col">
                  <div class="form-floating">
                      <input
                      type="file"
                      class="form-control"
                      ref="readerPictureRef"
                      @change="readerAddPictureChange"
                      
                      />
                      <label for="floatingInput">Фотография</label>
                  </div>
                  </div>
                <div class="col-auto">
                <button class="btn btn-primary" style="width: 100%;height: 100%;">
                    Добавить 
                </button>
                </div>
            </div>
            <img :src="readerImageUrl" style="max-width: 300px; margin-top:20px;border-radius:20px;"/>
        </form>
        </div>
        <h4 v-if="userInfo && userInfo.is_authenticated && userInfo.is_staff" >Список читателей</h4>
        <h4 v-else-if="userInfo && userInfo.is_authenticated">Моя информация</h4>
        <div class="row">
            <template v-for="item in readers">
            <div class="col-3 p-3 border d-flex justify-content-between align-items-center flex-wrap">
                    <div v-show="item.picture"><img :src="item.picture" style="max-width: 100%; border-radius: 20px; height: 300px; object-fit: cover; width:300px; margin-bottom:20px"></div>  {{ item.first_name }} 
                
                 <button class="btn btn-danger" @click="onRemoveClick(item)" v-if="userInfo && userInfo.is_authenticated && userInfo.is_staff">
                    <i class="bi bi-x">x</i>
                </button>
                
                <button style="flex:0 0 100%;"
                    class="btn btn-success mt-2"
                    @click="onReaderEditClick(item)"
                    data-bs-toggle="modal"
                    data-bs-target="#editReaderModal">
                    <span>Редактировать</span>
                </button>
            </div>
            </template>
        </div>
        </div>
        <div v-else>
      <h2 class="mt-2">Пожалуйста, <a href="/">авторизуйтесь</a></h2>
    </div>
        <div class="modal fade" id="editReaderModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="exampleModalLabel">
           Редактировать
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
                  v-model="readerToEdit.first_name"
                />
                <label for="floatingInput">Имя</label>
              </div>
            </div>
            <div class="col">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  v-model="readerToEdit.last_name"
                />
                <label for="floatingInput">Фамилия</label>
              </div>
            </div>
            <div class="col">
              <div class="form-floating">
                <input
                  type="email"
                  class="form-control"
                  v-model="readerToEdit.email"
                />
                <label for="floatingInput">Почта</label>
              </div>
            </div>
            <div class="col">
              <div class="form-floating">
                <input
                  type="number"
                  class="form-control"
                  v-model="readerToEdit.card_number"
                />
                <label for="floatingInput">Номер читательского билета</label>
              </div>
            </div>
            <div class="col-12 mt-3" v-if="readerToEdit.picture">
                <p>Текущее фото:</p>
                <img :src="readerToEdit.picture" style="max-width: 300px; border-radius: 10px; height: 200px; object-fit: cover; margin-bottom: 10px">
            </div>
            <div class="col-12 mt-3">
              <div class="form-floating">
                <input
                  type="file"
                  class="form-control"
                  ref="readerEditPictureRef"
                  @change="readerEditPictureChange"
                />
                <label for="floatingInput">Новое фото (оставьте пустым, чтобы не менять)</label>
              </div>
            </div>
          </div>
          <img v-if="authorEditImageUrl" :src="authorEditImageUrl" style="max-width: 200px; border-radius: 10px; height: 200px; object-fit: cover; margin-top: 10px">
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
            @click="onUpdateReader"
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