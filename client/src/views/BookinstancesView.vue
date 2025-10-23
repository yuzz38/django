<script setup>
import axios from 'axios';
import Cookies from 'js-cookie';
import {computed, onBeforeMount, ref} from 'vue';

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

const readerToAdd = ref({});
const genreToAdd = ref({});
const authorToAdd = ref({});
const booksToAdd = ref({});
const booksToAddItem = ref({});
async function onReaderAdd() {
  await axios.post("/api/readers/", {
    ...readerToAdd.value,
  });
  await fetchReaders(); // переподтягиваю
}
async function onGenreAdd() {
  await axios.post("/api/genres/", {
    ...genreToAdd.value,
  });
  await fetchGenre(); // переподтягиваю
}
async function onAuthorAdd() {
  await axios.post("/api/authors/", {
    ...authorToAdd.value,
  });
  await fetchAuthor(); // переподтягиваю
}
async function onBookAdd() {
  await axios.post("/api/books/", {
    ...booksToAdd.value,
  });
  await fetchBooks(); // переподтягиваю
}
async function onBookAddItem() {
  await axios.post("/api/bookinstances/", {
    ...booksToAddItem.value,
  });
  await fetchBookItem(); // переподтягиваю
}
async function onRemoveClick(reader) {
  await axios.delete(`/api/readers/${reader.id}/`);
  await fetchReaders(); // переподтягиваю
}
async function onRemoveClickGenre(genre) {
  await axios.delete(`/api/genres/${genre.id}/`);
  await fetchGenre(); // переподтягиваю
}
async function onRemoveClickAuthor(author) {
  await axios.delete(`/api/authors/${author.id}/`);
  await fetchAuthor(); // переподтягиваю
}
async function onRemoveClickBook(book) {
  await axios.delete(`/api/books/${book.id}/`);
  await fetchBooks(); // переподтягиваю
}
async function onRemoveClickBookItem(bookItem) {
  await axios.delete(`/api/bookinstances/${bookItem.id}/`);
  await fetchBookItem(); // переподтягиваю
}
const readerToEdit = ref({});
async function onReaderEditClick(reader) {
  readerToEdit.value = { ...reader };
}
async function onUpdateReader() {
  await axios.put(`/api/readers/${readerToEdit.value.id}/`, {
    ...readerToEdit.value,
  });
  await fetchReaders();
}

const genreToEdit = ref({});
async function onGenreEditClick(genre) {
  genreToEdit.value = { ...genre };
}
async function onUpdateGenre() {
  await axios.put(`/api/genres/${genreToEdit.value.id}/`, {
    ...genreToEdit.value,
  });
  await fetchGenre();
}


const authorToEdit = ref({});
async function onAuthorEditClick(author) {
  authorToEdit.value = { ...author };
}
async function onUpdateAuthor() {
  await axios.put(`/api/authors/${authorToEdit.value.id}/`, {
    ...authorToEdit.value,
  });
  await fetchAuthor();
}

const bookToEdit = ref({});
async function onBookEditClick(book) {
  bookToEdit.value = { ...book };
}
async function onUpdateBook() {
  await axios.put(`/api/books/${bookToEdit.value.id}/`, {
    ...bookToEdit.value,
  });
  await fetchBooks();
}

const bookToEditItem = ref({});
async function onBookEditClickItem(book) {
  bookToEditItem.value = { ...book };
}
async function onUpdateBookItem() {
  await axios.put(`/api/bookinstances/${bookToEditItem.value.id}/`, {
    ...bookToEditItem.value,
  });
  await fetchBookItem();
}
</script>
<template>
 <div class="border p-5">
           <h3>Выдать книгу</h3>
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
                 <div class="col-2">
                  <button class="btn btn-primary"  style="width: 100%;height: 100%;">
                      Выдать 
                  </button>
                  </div>
          </div>
           
          </form>
          <h4 class="mt-5">Состояние книг</h4>
            <div class="row">
                <template v-for="item in bookItem">
                <div class="col-3 p-3 border d-flex justify-content-between align-items-center flex-wrap">{{ books.find(b => b.id === item.book)?.name || 'Книга' }}  <br> <hr>
                    <span v-if="item.status === 'available'">На полке</span>
                    <span v-else-if="item.status === 'borrowed'">Выдана</span>
                    <span v-else-if="item.status === 'maintenance'">В ремонте</span>
                    <span v-else>{{ item.status }}</span>
                    
                    <button class="btn btn-danger" @click="onRemoveClickBookItem(item)">
                        <i class="bi bi-x">x</i>
                    </button>
                    <div class="mt-2 mb-2" style="width:100%;">
                      Читатель - {{ readers.find(r => r.id === item.borrower)?.first_name }} {{ readers.find(r => r.id === item.borrower)?.last_name }}
                    </div>
                    <button style="flex:0 0 100%;"
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