import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Navbar from './components/Navbar'
import OverviewPage from './pages/OverviewPage'
import TemporalPage from './pages/TemporalPage'
import ClusteringPage from './pages/ClusteringPage'
import ComparisonPage from './pages/ComparisonPage'
import './index.css'

function App() {
  return (
    <BrowserRouter>
      <div className="layout">
        <Navbar />
        <main className="main">
          <Routes>
            <Route path="/" element={<Navigate to="/overview" replace />} />
            <Route path="/overview" element={<OverviewPage />} />
            <Route path="/temporal" element={<TemporalPage />} />
            <Route path="/clustering" element={<ClusteringPage />} />
            <Route path="/comparison" element={<ComparisonPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
