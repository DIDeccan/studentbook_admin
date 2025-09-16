// src/redux/rootReducer.js
import navbar from './navbar';
import layout from './layout';
import auth from './authentication';
import students from './studentSlice'; 
import user from './userSlice';
import payments from './paymentSlice';

const rootReducer = {
  auth,
  navbar,
  layout,
  students, 
  user,
  payments,
};

export default rootReducer;
