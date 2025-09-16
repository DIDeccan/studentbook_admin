import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";
import api from '../../api.json';

const API_URL = import.meta.env.VITE_API_URL;

export const fetchPaymentDetails = createAsyncThunk(
  "payments/fetchPaymentDetails",
  async (filters, { rejectWithValue }) => {
    try {
      // Convert filters to URL query params (handles empty values gracefully)
      const params = new URLSearchParams();
      Object.entries(filters).forEach(([key, value]) => {
        if (value) {  // Only add non-empty params
          params.append(key, value);
        }
      });

      const queryString = params.toString();
      const url = `${API_URL}${api.payment.payDetails}${queryString ? '?' + queryString : ''}`;

      const response = await axios.get(url);
      return response.data.data; 
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || error.message);
    }
  }
);

const paymentSlice = createSlice({
  name: "payments",
  initialState: {
    summary: null,
    payments: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(fetchPaymentDetails.pending, state => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPaymentDetails.fulfilled, (state, action) => {
        state.loading = false;
        state.summary = action.payload.summary;
        state.payments = action.payload.payments;
      })
      .addCase(fetchPaymentDetails.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export default paymentSlice.reducer; 