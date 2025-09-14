import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Loader2, CheckCircle, XCircle } from 'lucide-react'

const ResetPassword = () => {
  const [loading, setLoading] = useState(false)
  const [validating, setValidating] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [tokenValid, setTokenValid] = useState(false)
  const [userEmail, setUserEmail] = useState('')
  const [formData, setFormData] = useState({
    password: '',
    confirmPassword: ''
  })

  // Get token from URL parameters
  const urlParams = new URLSearchParams(window.location.search)
  const token = urlParams.get('token')

  useEffect(() => {
    if (token) {
      validateToken()
    } else {
      setError('Invalid reset link. Please request a new password reset.')
      setValidating(false)
    }
  }, [token])

  const validateToken = async () => {
    try {
      const response = await fetch(`https://hr-advisor-app.onrender.com/api/auth/validate-reset-token/${token}`)
      const data = await response.json()

      if (response.ok && data.valid) {
        setTokenValid(true)
        setUserEmail(data.email)
      } else {
        setError(data.error || 'Invalid or expired reset token')
      }
    } catch (err) {
      setError('Network error. Please try again.')
    } finally {
      setValidating(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setSuccess('')

    // Validate passwords
    if (!formData.password || !formData.confirmPassword) {
      setError('Please fill in all fields')
      setLoading(false)
      return
    }

    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters long')
      setLoading(false)
      return
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match')
      setLoading(false)
      return
    }

    try {
      const response = await fetch('https://hr-advisor-app.onrender.com/api/auth/reset-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          token: token,
          password: formData.password
        }),
      })

      const data = await response.json()

      if (response.ok) {
        setSuccess(data.message)
        setFormData({ password: '', confirmPassword: '' })
        
        // Redirect to login after 3 seconds
        setTimeout(() => {
          window.location.href = '/'
        }, 3000)
      } else {
        setError(data.error || 'Failed to reset password')
      }
    } catch (err) {
      setError('Network error. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  if (validating) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Card className="w-full max-w-md">
          <CardContent className="pt-6">
            <div className="flex items-center justify-center space-x-2">
              <Loader2 className="h-6 w-6 animate-spin" />
              <span>Validating reset link...</span>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-bold text-blue-600">AnNi AI</CardTitle>
          <CardDescription>HR made simple - Your intelligent HR assistant</CardDescription>
          
          {tokenValid ? (
            <div className="mt-4">
              <CheckCircle className="h-8 w-8 text-green-500 mx-auto mb-2" />
              <h2 className="text-xl font-semibold">Reset Your Password</h2>
              <p className="text-sm text-gray-600 mt-1">
                Enter a new password for: <strong>{userEmail}</strong>
              </p>
            </div>
          ) : (
            <div className="mt-4">
              <XCircle className="h-8 w-8 text-red-500 mx-auto mb-2" />
              <h2 className="text-xl font-semibold">Invalid Reset Link</h2>
            </div>
          )}
        </CardHeader>

        <CardContent>
          {tokenValid ? (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label htmlFor="password">New Password</Label>
                <Input
                  id="password"
                  name="password"
                  type="password"
                  required
                  value={formData.password}
                  onChange={handleInputChange}
                  placeholder="Enter your new password"
                  minLength={6}
                />
              </div>

              <div>
                <Label htmlFor="confirmPassword">Confirm New Password</Label>
                <Input
                  id="confirmPassword"
                  name="confirmPassword"
                  type="password"
                  required
                  value={formData.confirmPassword}
                  onChange={handleInputChange}
                  placeholder="Confirm your new password"
                  minLength={6}
                />
              </div>

              {error && (
                <Alert variant="destructive">
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              {success && (
                <Alert>
                  <AlertDescription className="text-green-600">
                    {success}
                    <br />
                    <span className="text-sm">Redirecting to login page...</span>
                  </AlertDescription>
                </Alert>
              )}

              <Button type="submit" className="w-full" disabled={loading}>
                {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                Reset Password
              </Button>
            </form>
          ) : (
            <div className="text-center space-y-4">
              {error && (
                <Alert variant="destructive">
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}
              
              <Button 
                onClick={() => window.location.href = '/'}
                className="w-full"
              >
                Back to Login
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

export default ResetPassword

