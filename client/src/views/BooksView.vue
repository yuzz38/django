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
           <h3>Добавить книгу</h3>
          <form @submit.prevent.stop="onBookAdd">
              
              <div class="row" style="row-gap: 20px;">
                  <div class="col-4">
                  <div class="form-floating">
                      <!-- ТУТ ПОДКЛЮЧИЛ studentToAdd.name -->
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
                        <select class="form-select" v-model="booksToAdd.genres" multiple> 
                          <option :value="g.id" v-for="g in genre">
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
          <h4 class="mt-5">Список книг</h4>
        <div class="row">
            <template v-for="item in books">
            <div class="col-3 p-3 border d-flex justify-content-between align-items-center flex-wrap">{{ item.name }} 
                
                 <button class="btn btn-danger" @click="onRemoveClickBook(item)">
                    <i class="bi bi-x">x</i>
                </button>
                
                <button style="flex:0 0 100%;"
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
                        <select class="form-select" v-model="bookToEdit.genres" multiple> 
                          <option :value="g.id" v-for="g in genre">
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
</style>