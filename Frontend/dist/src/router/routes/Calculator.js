import { lazy } from 'react'

const PriceCalculator = lazy(() => import('../../views/calculator'))

const CalculatorRoutes = [
  {
    path: '/pricecalculator',
    element: <PriceCalculator/>
  }
]

export default CalculatorRoutes;