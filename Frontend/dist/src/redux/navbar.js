// ** Redux Imports
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'

// ** Axios Imports
import axios from 'axios'

// ✅ Base URL from .env (make sure .env has VITE_API_URL)
const API_URL = import.meta.env.VITE_API_URL

// 🔹 Get bookmarks
export const getBookmarks = createAsyncThunk('layout/getBookmarks', async () => {
  // const response = await axios.get(`${API_URL}/bookmarks/data`)
  return {
    data: response.data.suggestions || [],
    bookmarks: response.data.bookmarks || []
  }
})

// 🔹 Update bookmark
export const updateBookmarked = createAsyncThunk('layout/updateBookmarked', async id => {
  await axios.post(`${API_URL}/bookmarks/update`, { id })
  return id
})

export const layoutSlice = createSlice({
  name: 'layout',
  initialState: {
    query: '',
    bookmarks: [],
    suggestions: []
  },
  reducers: {
    handleSearchQuery: (state, action) => {
      state.query = action.payload
    }
  },
  extraReducers: builder => {
    builder
      .addCase(getBookmarks.fulfilled, (state, action) => {
        state.suggestions = action.payload.data
        state.bookmarks = action.payload.bookmarks
      })
      .addCase(updateBookmarked.fulfilled, (state, action) => {
        let objectToUpdate

        // ** find & update object
        state.suggestions.find(item => {
          if (item.id === action.payload) {
            item.isBookmarked = !item.isBookmarked
            objectToUpdate = item
          }
        })

        // ** Get index to add or remove bookmark from array
        const bookmarkIndex = state.bookmarks.findIndex(x => x.id === action.payload)

        if (bookmarkIndex === -1 && objectToUpdate) {
          state.bookmarks.push(objectToUpdate)
        } else {
          state.bookmarks.splice(bookmarkIndex, 1)
        }
      })
  }
})

export const { handleSearchQuery } = layoutSlice.actions

export default layoutSlice.reducer
