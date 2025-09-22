// src/redux/rootReducer.js
import navbar from './navbar';
import layout from './layout';
import auth from './authentication';
import students from './studentSlice'; 
import user from './userSlice';
import payments from './paymentSlice';
import calculator from './calculatorSlice';

const rootReducer = {
  auth,
  navbar,
  layout,
  students, 
  user,
  payments,
  calculator,
};

export default rootReducer;
