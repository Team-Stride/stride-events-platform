import { Routes, Route } from 'react-router-dom'
import EventLanding from './pages/EventLanding'
import AdminDashboard from './pages/admin/Dashboard'
import TermsAndConditions from './pages/TermsAndConditions'
import PrivacyPolicy from './pages/PrivacyPolicy'
import './App.css'

function App() {
  return (
    <Routes>
      <Route path="/" element={<EventLanding />} />
      <Route path="/events/:slug" element={<EventLanding />} />
      <Route path="/terms" element={<TermsAndConditions />} />
      <Route path="/privacy" element={<PrivacyPolicy />} />
      <Route path="/admin" element={<AdminDashboard />} />
    </Routes>
  )
}

export default App
