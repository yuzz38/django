<script setup>
import axios from 'axios';
import Cookies from 'js-cookie';
import {computed, onBeforeMount, ref} from 'vue';
import {useUserStore} from '@/stores/user_store';
import {storeToRefs} from "pinia";
const userStore = useUserStore()

const {
    userInfo,
} = storeToRefs(userStore)

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


const authorToAdd = ref({});

const authorPictureRef = ref();
const authorImageUrl = ref();
async function authorAddPictureChange() {
  authorImageUrl.value = URL.createObjectURL(authorPictureRef.value.files[0])
}
async function onAuthorAdd() {
  const formData = new FormData();
  formData.append('picture', authorPictureRef.value.files[0]);
  formData.set('nameAuthor', authorToAdd.value.nameAuthor);
  formData.set('bio', authorToAdd.value.bio)
  await axios.post("/api/authors/",formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  
  await fetchAuthor(); // переподтягиваю
}
const authorToEdit = ref({});



async function onRemoveClickAuthor(author) {
  if (!userInfo.value.is_doublefaq) {
        alert('Для редактирования требуется двухфакторная аутентификация. Нажмите кнопку "Войти по второму фактору" на главной странице.');
        return;
    }
  else {
    await axios.delete(`/api/authors/${author.id}/`);
  await fetchAuthor(); // переподтягиваю
  }
}

const authorEditPictureRef = ref();
const authorEditImageUrl = ref();


async function authorEditPictureChange() {
  if (authorEditPictureRef.value.files[0]) {
    authorEditImageUrl.value = URL.createObjectURL(authorEditPictureRef.value.files[0])
  }
}


async function onAuthorEditClick(author) {
  authorToEdit.value = { ...author };
  authorEditImageUrl.value = null; 
}


async function onUpdateAuthor() {
  const formData = new FormData();
  
  
  if (authorEditPictureRef.value.files[0]) {
    formData.append('picture', authorEditPictureRef.value.files[0]);
  }
  
  formData.set('nameAuthor', authorToEdit.value.nameAuthor);
  formData.set('bio', authorToEdit.value.bio);
  
  await axios.put(`/api/authors/${authorToEdit.value.id}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  
  await fetchAuthor();
}


</script>
<template>
  
    <div v-if="userInfo && userInfo.is_authenticated">
        <div class="border p-5">
          <div class="mb-5" v-if="userInfo && userInfo.is_authenticated && userInfo.is_staff">
            <h3>Добавить автора</h3>
          <form @submit="onAuthorAdd">
              
              <div class="row">
                  <div class="col">
                  <div class="form-floating">
                      <!-- ТУТ ПОДКЛЮЧИЛ studentToAdd.name -->
                      <input
                      type="text"
                      class="form-control"
                      v-model="authorToAdd.nameAuthor"
                      required
                      />
                      <label for="floatingInput">Имя автора</label>
                  </div>
                  </div>
                  <div class="col">
                  <div class="form-floating">
                      <input
                      type="text"
                      class="form-control"
                      v-model="authorToAdd.bio"
                      required
                      />
                      <label for="floatingInput">Биография</label>
                  </div>
                  </div>
                  <div class="col">
                  <div class="form-floating">
                      <input
                      type="file"
                      class="form-control"
                      ref="authorPictureRef"
                      @change="authorAddPictureChange"
                      required
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
              
              <img :src="authorImageUrl" style="max-width: 300px; margin-top:20px;border-radius:20px;"/>
          </form>
          </div>
          <div v-if="userInfo && userInfo.is_authenticated">
            <h4>Список авторов</h4>
        <div class="row">
            <template v-for="item in authors">
            <div class="col-3 p-3 border d-flex justify-content-between align-items-center flex-wrap">
              <div v-show="item.picture"><img :src="item.picture" style="max-width: 100%; border-radius: 20px; height: 300px; object-fit: cover; width:300px; margin-bottom:20px"></div>
              {{ item.nameAuthor }} 

                 <button v-if="userInfo && userInfo.is_authenticated && userInfo.is_staff" class="btn btn-danger" @click="onRemoveClickAuthor(item)">
                    <i class="bi bi-x">x</i>
                </button>
                
                <button style="flex:0 0 100%;" v-if="userInfo && userInfo.is_authenticated && userInfo.is_staff"
                    class="btn btn-success mt-2"
                    @click="onAuthorEditClick(item)"
                    data-bs-toggle="modal"
                    data-bs-target="#editAuthorModal">
                    <span>Редактировать</span>
                </button>
            </div>
            </template>
        </div>
          </div>
        </div>
    </div>
    <div v-else>
      <h2 class="mt-2">Пожалуйста, <a href="/">авторизуйтесь</a></h2>
    </div>
    <div class="modal fade" id="editAuthorModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="exampleModalLabel">
           Редактировать автора
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
            <div class="col-6">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  v-model="authorToEdit.nameAuthor"
                />
                <label for="floatingInput">Имя</label>
              </div>
            </div>
            <div class="col-6">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  v-model="authorToEdit.bio"
                />
                <label for="floatingInput">Биография</label>
              </div>
            </div>
            <div class="col-6 mt-3" v-if="authorToEdit.picture">
                <p>Текущее изображение:</p>
                <img :src="authorToEdit.picture" style="max-width: 300px; border-radius: 10px; height: 200px; object-fit: cover; margin-bottom: 10px">
            </div>
            <div class="col-12 mt-3">
              <div class="form-floating">
                <input
                  type="file"
                  class="form-control"
                  ref="authorEditPictureRef"
                  @change="authorEditPictureChange"
                />
                <label for="floatingInput">Новое изображение (оставьте пустым, чтобы не менять)</label>
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
            @click="onUpdateAuthor"
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