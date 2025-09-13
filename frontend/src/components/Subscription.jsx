import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { CheckCircle, DollarSign, RefreshCw } from 'lucide-react'
import { Alert, AlertDescription } from '@/components/ui/alert'

const Subscription = ({ token, user, onUserUpdate }) => {
  const [subscriptionData, setSubscriptionData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [upgradeMessage, setUpgradeMessage] = useState('')

  useEffect(() => {
    fetchSubscriptionData()
  }, [token, user])

  const fetchSubscriptionData = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await fetch(`https://hr-advisor-app.onrender.com/api/subscriptions`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
      const data = await response.json()
      if (response.ok) {
        setSubscriptionData(data)
      } else {
        setError(data.error || 'Failed to fetch subscription data')
      }
    } catch (err) {
      setError('Network error. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleUpgrade = async (planName) => {
    setLoading(true)
    setError('')
    setUpgradeMessage('')
    try {
      const response = await fetch(`https://hr-advisor-app.onrender.com/api/subscriptions/upgrade`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ plan_name: planName }),
      })
      const data = await response.json()
      if (response.ok) {
        setUpgradeMessage(data.message)
        // Update user context with new coins and plan
        onUserUpdate({ ...user, coins: data.new_coins_balance, subscription_plan: data.new_plan })
        fetchSubscriptionData() // Refresh subscription data
      } else {
        setError(data.error || 'Failed to upgrade subscription')
      }
    } catch (err) {
      setError('Network error. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="h-64 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  const plans = [
    { name: 'Free', cost: 0, coins: 100, features: ['Basic HR Advice', 'Country-specific guidance', 'Template generation'] },
    { name: 'Premium', cost: 29.99, coins: 1000, features: ['All Free features', 'Advanced HR Advice', 'Workflow creation', 'Priority support'] },
    { name: 'Enterprise', cost: 99.99, coins: 5000, features: ['All Premium features', 'Dedicated account manager', 'Custom integrations', 'On-site training'] },
  ]

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Subscription Management</h1>
        <Button onClick={fetchSubscriptionData} variant="outline">
          <RefreshCw className="mr-2 h-4 w-4" />
          Refresh
        </Button>
      </div>

      {error && (
        <Alert variant="destructive" className="mb-4">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
      {upgradeMessage && (
        <Alert className="mb-4">
          <AlertDescription>{upgradeMessage}</AlertDescription>
        </Alert>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Your Current Plan</CardTitle>
          <CardDescription>Details of your active subscription</CardDescription>
        </CardHeader>
        <CardContent>
          {subscriptionData ? (
            <div className="space-y-4">
              <p className="text-2xl font-bold capitalize">
                {subscriptionData.plan_type.replace('_', ' ')}
              </p>
              <p className="text-lg">
                Coins Balance: <Badge>{subscriptionData.coins_balance}</Badge> / {subscriptionData.total_coins_allocated}
              </p>
              <div className="space-y-2">
                <h3 className="text-md font-semibold">Features:</h3>
                <ul className="list-disc list-inside space-y-1">
                  {subscriptionData.features.map((feature, index) => (
                    <li key={index} className="flex items-center text-sm text-gray-700">
                      <CheckCircle className="mr-2 h-4 w-4 text-green-500" /> {feature}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ) : (
            <p>No subscription data available.</p>
          )}
        </CardContent>
      </Card>

      <h2 className="text-2xl font-bold text-gray-900 mt-8">Available Plans</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {plans.map((plan) => (
          <Card key={plan.name} className={subscriptionData?.plan_type === plan.name.toLowerCase() ? 'border-blue-500 border-2' : ''}>
            <CardHeader>
              <CardTitle className="flex justify-between items-center">
                {plan.name}
                {subscriptionData?.plan_type === plan.name.toLowerCase() && (
                  <Badge className="bg-blue-500">Current Plan</Badge>
                )}
              </CardTitle>
              <CardDescription>${plan.cost} / month</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-lg font-semibold">{plan.coins} Coins</p>
              <ul className="list-disc list-inside space-y-1">
                {plan.features.map((feature, index) => (
                  <li key={index} className="flex items-center text-sm text-gray-700">
                    <CheckCircle className="mr-2 h-4 w-4 text-green-500" /> {feature}
                  </li>
                ))}
              </ul>
              <Button 
                className="w-full"
                onClick={() => handleUpgrade(plan.name)}
                disabled={loading || subscriptionData?.plan_type === plan.name.toLowerCase()}
              >
                {subscriptionData?.plan_type === plan.name.toLowerCase() ? 'Current Plan' : 'Upgrade'}
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

export default Subscription


