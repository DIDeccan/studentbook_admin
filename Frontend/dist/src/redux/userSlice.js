import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";
import api from "../../api.json";

const API_URL = import.meta.env.VITE_API_URL;

// --- USER DETAILS ---
export const fetchUserDetails = createAsyncThunk(
  "user/fetchUserDetails",
  async (_, { rejectWithValue }) => {
    try {
      const response = await axios.get(`${API_URL}${api.users.details}`);
      // Backend returns { data: [...] }, so we extract it
      return Array.isArray(response.data.data) ? response.data.data : [];
    } catch (error) {
      return rejectWithValue(
        error.response?.data || "Failed to fetch user details"
      );
    }
  }
);

const studentSlice = createSlice({
  name: "user",
  initialState: {
    users: [],
    userLoading: false,
    userError: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchUserDetails.pending, (state) => {
        state.userLoading = true;
        state.userError = null;
      })
      .addCase(fetchUserDetails.fulfilled, (state, action) => {
        state.users = action.payload;
        state.userLoading = false;
        state.userError = null;
      })
      .addCase(fetchUserDetails.rejected, (state, action) => {
        state.userLoading = false;
        state.userError = action.payload;
      });
  },
});

export default studentSlice.reducer;
