import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from "../utility/api"; 
import apiList from "../../api.json";


const API_URL = import.meta.env.VITE_API_URL;

// --- PIE CHART ---
export const fetchStudentDistribution = createAsyncThunk(
  'students/fetchDistribution',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get(`${API_URL}${apiList.dashboard.classDistribution}`);
      const payload = response.data;
      if (Array.isArray(payload.data)) {
        const cleaned = payload.data.filter(
          item => item.class && item.number_of_student != null
        );
        return {
          labels: cleaned.map(item => item.class),
          data: cleaned.map(item => item.number_of_student),
        };
      }
      return { labels: [], data: [] };
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch pie chart data');
    }
  }
);

// --- LAST TRANSACTIONS ---
export const fetchLastTransactions = createAsyncThunk(
  'students/fetchLastTransactions',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get(`${API_URL}${apiList.dashboard.lastTransactions}`);
      return Array.isArray(response.data.data) ? response.data.data : [];
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch transactions');
    }
  }
);

// --- USER LOGIN DETAILS ---
export const fetchUserLoginDetails = createAsyncThunk(
  'students/fetchUserLoginDetails',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get(`${API_URL}${apiList.dashboard.LoginDetails}`);
      // Ensure we always return an array
      return Array.isArray(response.data.data) ? response.data.data : [];
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch user login details');
    }
  }
);

const studentSlice = createSlice({
  name: 'students',
  initialState: {
    // Pie chart
    labels: [],
    data: [],
    pieLoading: false,
    pieError: null,

    // Transactions
    transactions: [],
    txnLoading: false,
    txnError: null,

    // User login details
    userLogins: [],
    userLoginLoading: false,
    userLoginError: null,
    fetched:false,
  },
  reducers: {},
  extraReducers: builder => {
    builder
      // --- PIE CHART ---
      .addCase(fetchStudentDistribution.pending, state => {
        state.pieLoading = true;
        state.pieError = null;
      })
      .addCase(fetchStudentDistribution.fulfilled, (state, action) => {
        state.labels = action.payload.labels;
        state.data = action.payload.data;
        state.pieLoading = false;
        state.pieError = null;
      })
      .addCase(fetchStudentDistribution.rejected, (state, action) => {
        state.pieLoading = false;
        state.pieError = action.payload;
      })

      // --- LAST TRANSACTIONS ---
      .addCase(fetchLastTransactions.pending, state => {
        state.txnLoading = true;
        state.txnError = null;
      })
      .addCase(fetchLastTransactions.fulfilled, (state, action) => {
        state.transactions = action.payload;
        state.txnLoading = false;
        state.txnError = null;
      })
      .addCase(fetchLastTransactions.rejected, (state, action) => {
        state.txnLoading = false;
        state.txnError = action.payload;
      })

      // --- USER LOGIN DETAILS ---
      .addCase(fetchUserLoginDetails.pending, state => {
        state.userLoginLoading = true;
        state.userLoginError = null;
      })
      .addCase(fetchUserLoginDetails.fulfilled, (state, action) => {
        state.userLogins = action.payload;
        state.userLoginLoading = false;
        state.userLoginError = null;
        state.fetched = true;
      })
      .addCase(fetchUserLoginDetails.rejected, (state, action) => {
        state.userLoginLoading = false;
        state.userLoginError = action.payload;
        state.fetched = true;
      });
  },
});

export default studentSlice.reducer;
