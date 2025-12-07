import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";

export const useDataStore = defineStore("dataStore", () => {
    const authors = ref([]);
    const books = ref([]);
    const genres = ref([]);
    const readers = ref([]);
    const bookItem = ref([]);

    async function fetchAuthors() {
        const response = await axios.get("/api/authors");
        authors.value = response.data;
        return response.data;
    }

    async function fetchBooks() {
        const response = await axios.get("/api/books");
        books.value = response.data;
        return response.data;
    }

    async function fetchGenres() {
        const response = await axios.get("/api/genres");
        genres.value = response.data;
        return response.data;
    }

    async function fetchReaders() {
        const response = await axios.get("/api/readers");
        readers.value = response.data;
        return response.data;
    }

    async function fetchBookItem() {
        const response = await axios.get("/api/bookinstances");
        bookItem.value = response.data;
        return response.data;
    }

    return {
        authors,
        books,
        genres,
        readers,
        bookItem,
        fetchAuthors,
        fetchBooks,
        fetchGenres,
        fetchReaders,
        fetchBookItem
    };
});