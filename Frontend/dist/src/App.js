import React, { Suspense } from 'react'
import './App.css';
// import "./core/scss/base/pages/app-student.scss";



// ** Router Import
import Router from './router/Router'

const App = () => {
  return (
    <Suspense fallback={null}>
      <Router />
    </Suspense>
  );
};

export default App
