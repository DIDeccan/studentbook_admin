import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
import apiList from '../../api.json'
import api from "../utility/api"

const API_URL = import.meta.env.VITE_API_URL;

// Thunks
export const loginUser = createAsyncThunk(
  'auth/loginUser',
  async (credentials, { rejectWithValue }) => {
    try {
      const url = `${API_URL}${apiList.auth.login}`;
      console.log('[auth/loginUser] URL:', url);
      console.log('[auth/loginUser] Credentials sent:', credentials);

      const response = await api.post(url, credentials);
      console.log('[auth/loginUser] Raw response:', response);

      return response.data;
    } catch (err) {
      console.error('[auth/loginUser] Error response:', err.response?.data || err.message);
      return rejectWithValue(err.response?.data || err.message);
    }
  }
);

// logout API 
export const logoutUser = createAsyncThunk(
  'auth/logoutUser',
  async (_, { rejectWithValue, getState }) => {
    try {
      const { auth } = getState();
      const refreshToken = auth.refreshToken;
      const accessToken = auth.token;

      const response = await api.post(
        apiList.auth.logout,
        { refresh: refreshToken },
        {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );

      return response.data;
    } catch (err) {
      return rejectWithValue(err.response?.data || err.message);
    }
  }
);

// refresh token api
export const refreshTokenThunk = createAsyncThunk(
  'auth/refreshToken',
  async (_, { rejectWithValue, getState }) => {
    try {
      const { auth } = getState();
      const refreshToken = auth.refreshToken;

      if (!refreshToken) {
        return rejectWithValue('No refresh token found');
      }

      const response = await axios.post(
        `${API_URL}${apiList.auth.refreshToken}`,
        { refresh: refreshToken },
        { headers: { 'Content-Type': 'application/json' } }
      );

      return response.data.data;
    } catch (err) {
      return rejectWithValue(err.response?.data || err.message);
    }
  }
);

const authSlice = createSlice({
  name: 'auth',
  initialState: {
    user: JSON.parse(localStorage.getItem('userData')) || null,
    token: localStorage.getItem('access') || null,
    refreshToken: localStorage.getItem('refresh') || null,
    loading: false,
    error: null,
    success: false,
  },
  reducers: {
    logout: (state) => {
      state.user = null;
      state.token = null;
      state.refreshToken = null;
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      localStorage.removeItem('userData');
    },
  },
  extraReducers: (builder) => {

    // Login
    builder.addCase(loginUser.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(loginUser.fulfilled, (state, action) => {
      console.log('[authSlice] Fulfilled payload:', action.payload);

      const payload = action.payload;

      state.loading = false;
      state.token = payload.access;
      state.refreshToken = payload.refresh;
      state.user = {
        role: payload.user_type,
        is_active: payload.is_active
      };

      localStorage.setItem('access', payload.access);
      localStorage.setItem('refresh', payload.refresh);
      localStorage.setItem('userData', JSON.stringify(state.user));
    });


    builder.addCase(loginUser.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload;
    });

    // log out 
    builder.addCase(logoutUser.pending, (state) => {
      state.loading = true
      state.error = null
      state.user = null
      state.token = null
      state.refreshToken = null
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      localStorage.removeItem('userData')
    })

    builder.addCase(logoutUser.fulfilled, (state) => {
      state.loading = false;
      state.user = null;
      state.token = null;
      state.refreshToken = null;

      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      localStorage.removeItem('userData');
    });
    builder.addCase(logoutUser.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload;
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      localStorage.removeItem('userData');
    });

    // // refresh token api 
    builder.addCase(refreshTokenThunk.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(refreshTokenThunk.fulfilled, (state, action) => {
      state.loading = false;
      state.token = action.payload.access;
      state.refreshToken = action.payload.refresh;
      localStorage.setItem('access', action.payload.access);
      localStorage.setItem('refresh', action.payload.refresh);
    });

    builder.addCase(refreshTokenThunk.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload;
      state.user = null;
      state.token = null;
      state.refreshToken = null;
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      localStorage.removeItem('userData');
    });



  },

});

export const { logout } = authSlice.actions;
export default authSlice.reducer;
