import { lazy } from 'react'

const Contentupload = lazy(() => import('../../views/contentupload'))

const CalculatorRoutes = [
  {
    path: '/contentupload',
    element: <Contentupload/>
  }
]

export default CalculatorRoutes;