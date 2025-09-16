import { useState, useEffect } from 'react'
import Layout from './components/Layout'
import Login from './components/Login'
import Dashboard from './components/Dashboard'
import HRAdvisor from './components/HRAdvisor'
import EmployeeTable from './components/EmployeeTable'
import Subscription from './components/Subscription'
import { Alert, AlertDescription } from '@/components/ui/alert'
import './App.css'

function App() {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(null)
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [loading, setLoading] = useState(true)
  const [verificationMessage, setVerificationMessage] = useState(null)
  const [verificationStatus, setVerificationStatus] = useState(null)

  useEffect(() => {
    // Check for verification URL parameters
    const urlParams = new URLSearchParams(window.location.search)
    const verification = urlParams.get('verification')
    
    if (verification) {
      switch (verification) {
        case 'success':
          setVerificationMessage('Email verified successfully! You can now log in to your account.')
          setVerificationStatus('success')
          break
        case 'invalid':
          setVerificationMessage('Invalid verification link. Please check your email for the correct link or request a new verification email.')
          setVerificationStatus('error')
          break
        case 'expired':
          setVerificationMessage('Verification link has expired. Please request a new verification email.')
          setVerificationStatus('error')
          break
        case 'already_verified':
          setVerificationMessage('Your email is already verified. You can log in to your account.')
          setVerificationStatus('info')
          break
        case 'error':
          setVerificationMessage('An error occurred during verification. Please try again or contact support.')
          setVerificationStatus('error')
          break
        default:
          break
      }
      
      // Clear URL parameters after processing
      window.history.replaceState({}, document.title, window.location.pathname)
    }
    
    // Check for existing session
    const savedToken = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')
    
    if (savedToken && savedUser) {
      setToken(savedToken)
      setUser(JSON.parse(savedUser))
    }
    setLoading(false)
  }, [])

  const handleLogin = (userData, accessToken) => {
    setUser(userData)
    setToken(accessToken)
    setCurrentPage('dashboard')
    // Clear verification message after successful login
    setVerificationMessage(null)
    setVerificationStatus(null)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setUser(null)
    setToken(null)
    setCurrentPage('dashboard')
    // Clear verification message on logout
    setVerificationMessage(null)
    setVerificationStatus(null)
  }

  const clearVerificationMessage = () => {
    setVerificationMessage(null)
    setVerificationStatus(null)
  }

  const handleUserUpdate = (updatedUser) => {
    setUser(updatedUser)
    localStorage.setItem('user', JSON.stringify(updatedUser))
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard onPageChange={setCurrentPage} token={token} />
      case 'hr-advisor':
        return <HRAdvisor token={token} />
      case 'employees':
        return <EmployeeTable token={token} />
      case 'history':
        return <div className="text-center py-12">
          <h2 className="text-2xl font-bold text-gray-900">Prompt History</h2>
          <p className="text-gray-600 mt-2">Coming soon...</p>
        </div>
      case 'subscription':
        return <Subscription token={token} user={user} onUserUpdate={handleUserUpdate} />
      case 'settings':
        return <div className="text-center py-12">
          <h2 className="text-2xl font-bold text-gray-900">Settings</h2>
          <p className="text-gray-600 mt-2">Coming soon...</p>
        </div>
      default:
        return <Dashboard onPageChange={setCurrentPage} token={token} />
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (!user || !token) {
    return (
      <div>
        {verificationMessage && (
          <div className="fixed top-4 left-1/2 transform -translate-x-1/2 z-50 w-full max-w-md">
            <Alert variant={verificationStatus === 'error' ? 'destructive' : 'default'} className="mb-4">
              <AlertDescription className={verificationStatus === 'success' ? 'text-green-600' : ''}>
                {verificationMessage}
              </AlertDescription>
              <button 
                onClick={clearVerificationMessage}
                className="absolute top-2 right-2 text-gray-400 hover:text-gray-600"
              >
                ×
              </button>
            </Alert>
          </div>
        )}
        <Login 
          onLogin={handleLogin} 
          verificationMessage={verificationMessage}
          verificationStatus={verificationStatus}
          onClearVerification={clearVerificationMessage}
        />
      </div>
    )
  }

  return (
    <Layout 
      currentPage={currentPage} 
      onPageChange={setCurrentPage}
      user={user}
      onLogout={handleLogout}
    >
      {renderPage()}
    </Layout>
  )
}

export default App


