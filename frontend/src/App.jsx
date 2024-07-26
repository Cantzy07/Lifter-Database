import {BrowserRouter, Routes, Route} from 'react-router-dom'
import AllLifters from './pages/AllLifters'
import MatchingLifter from './pages/MatchingLifter'
import Resources from './pages/Resources'
import NoPage from './pages/NoPage'

export default function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route index element={<AllLifters />} />
          <Route path="/AllLifters" element={<AllLifters />} />
          <Route path="/MatchingLifter" element={<MatchingLifter />} />
          <Route path="/Resources" element={<Resources />} />
          <Route path="*" element={<NoPage />} />
        </Routes>
      </BrowserRouter>
    </div>
  )
}