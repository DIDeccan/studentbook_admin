import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import api from "../utility/api"; 
import apiList from "../../api.json";

const API_URL = import.meta.env.VITE_API_URL;

// --- Fetch Class List ---
export const fetchClassList = createAsyncThunk(
  "calculator/fetchClassList",
  async (_, { rejectWithValue }) => {
    try {
      const url = `${API_URL}${apiList.calculator.classList}`; 
      const response = await api.get(url);
      return response.data.data || []; 
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || error.message);
    }
  }
);

// --- Submit Calculation ---
export const fetchCalculatePrice = createAsyncThunk(
  "calculator/fetchCalculatePrice",
  async ({ class_id, original_price, discount_percentage, final_price }, { rejectWithValue }) => {
    try {
      const url = `${API_URL}${apiList.calculator.PriceCalculator}`; 
      const response = await api.post(url, {
        class_id,
        original_price,
        discount_percentage,
        final_price,
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || error.message);
    }
  }
);

const calculatorSlice = createSlice({
  name: "calculator",
  initialState: {
    classLevel: null,
    classList: [],
    originalPrice: "",
    discount: "",
    finalPrice: null,
    loading: false,
    error: null,
    success: null,
  },
  reducers: {
    setClassLevel: (state, action) => {
      state.classLevel = action.payload;
    },
    setOriginalPrice: (state, action) => {
      state.originalPrice = action.payload;
    },
    setDiscount: (state, action) => {
      state.discount = action.payload;
    },
    reset: (state) => {
      state.classLevel = "";
      state.originalPrice = "";
      state.discount = "";
      state.finalPrice = null;
      state.error = null;
      state.success = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // --- class list ---
      .addCase(fetchClassList.fulfilled, (state, action) => {
        state.classList = action.payload || [];
      })
      // --- price calc ---
      .addCase(fetchCalculatePrice.pending, (state) => {
        state.loading = true;
        state.error = null;
        state.success = null;
      })
      .addCase(fetchCalculatePrice.fulfilled, (state, action) => {
        state.loading = false;
        state.finalPrice = action.meta.arg.final_price;
        state.success = action.payload.message || "Price calculated successfully!";
      })
      .addCase(fetchCalculatePrice.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { setClassLevel, setOriginalPrice, setDiscount, reset } =
  calculatorSlice.actions;

export default calculatorSlice.reducer;
