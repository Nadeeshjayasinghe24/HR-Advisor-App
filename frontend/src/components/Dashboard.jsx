import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { getContextualWelcome, getMotivationalMessage, extractFirstName } from '../utils/nameUtils'
import { 
  Users, 
  MessageSquare, 
  TrendingUp, 
  Clock,
  Plus,
  ArrowRight,
  Coins,
  ChevronDown,
  ChevronUp,
  Lightbulb,
  Target,
  Calendar
} from 'lucide-react'
import '../App.css'

const Dashboard = ({ onPageChange, token, user }) => {
  const [stats, setStats] = useState({
    totalEmployees: 0,
    activeEmployees: 0,
    recentQueries: 0,
    subscription: null
  })
  const [recentActivity, setRecentActivity] = useState([])
  const [loading, setLoading] = useState(true)
  const [tipsCollapsed, setTipsCollapsed] = useState(false)
  const [currentTip, setCurrentTip] = useState(0)

  // Daily HR Tips
  const dailyTips = [
    {
      title: "Employee Recognition",
      content: "Recognize achievements within 24 hours for maximum impact. A simple 'thank you' can boost productivity by 31%.",
      category: "Best Practice"
    },
    {
      title: "One-on-One Meetings",
      content: "Schedule regular 1:1s with direct reports. Aim for 30 minutes monthly to discuss goals, challenges, and career development.",
      category: "Management"
    },
    {
      title: "Team Building Activity",
      content: "Try a 'Two Truths and a Lie' session during your next team meeting to help colleagues learn about each other.",
      category: "Team Building"
    },
    {
      title: "Performance Reviews",
      content: "Use the STAR method (Situation, Task, Action, Result) when documenting performance examples for more effective reviews.",
      category: "Performance"
    },
    {
      title: "Workplace Wellness",
      content: "Encourage micro-breaks every 90 minutes. Even a 2-minute walk can improve focus and reduce stress.",
      category: "Wellness"
    }
  ]

  useEffect(() => {
    fetchDashboardData()
    // Rotate tips daily
    const today = new Date().getDate()
    setCurrentTip(today % dailyTips.length)
  }, [])

  const fetchDashboardData = async () => {
    try {
      // Fetch subscription info
      const subResponse = await fetch(`https://hr-advisor-app.onrender.com/api/subscriptions`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      } )
      
      if (subResponse.ok) {
        const subData = await subResponse.json()
        setStats(prev => ({ ...prev, subscription: subData }))
      }
      
      // Fetch recent activity
      const historyResponse = await fetch(`https://hr-advisor-app.onrender.com/api/history/prompts/recent`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      } )
      
      if (historyResponse.ok) {
        const historyData = await historyResponse.json()
        setRecentActivity(historyData.slice(0, 5))
        setStats(prev => ({ ...prev, recentQueries: historyData.length }))
      }

      // Fetch employees (for count)
      const empResponse = await fetch(`https://hr-advisor-app.onrender.com/api/employees?per_page=1`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      } )
      
      if (empResponse.ok) {
        const empData = await empResponse.json()
        setStats(prev => ({ 
          ...prev, 
          totalEmployees: empData.total || 0,
          activeEmployees: empData.total || 0 // Simplified for now
        }))
      }

    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-32 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header with User Info */}
      <div className="flex justify-between items-start">
        <div className="flex-1">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-orange-600 to-orange-500 bg-clip-text text-transparent">
            {getContextualWelcome(user?.username, 'dashboard')}
          </h1>
          <p className="text-gray-600 mt-1">{getMotivationalMessage(user?.username)}</p>
        </div>
        
        {/* User Profile Area with Subscription */}
        <div className="flex items-center space-x-4">
          <div className="text-right">
            <p className="text-sm font-medium text-gray-900">
              {user?.first_name || extractFirstName(user?.username) || 'User'}
            </p>
            <p className="text-xs text-gray-500">
              {stats.subscription?.subscription_type || 'Free'} Plan
            </p>
          </div>
          <Button onClick={() => onPageChange('hr-advisor')} className="bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white shadow-lg">
            <MessageSquare className="mr-2 h-4 w-4" />
            Ask HR Advisor
          </Button>
        </div>
      </div>

      {/* Daily Tips Section - Collapsible */}
      {!tipsCollapsed && (
        <Card className="border-l-4 border-l-blue-500 bg-gradient-to-r from-blue-50 to-indigo-50">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Lightbulb className="h-5 w-5 text-blue-600" />
                <CardTitle className="text-lg text-blue-900">Daily HR Tip</CardTitle>
                <Badge variant="secondary" className="text-xs">
                  {dailyTips[currentTip].category}
                </Badge>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setTipsCollapsed(true)}
                className="text-blue-600 hover:text-blue-800"
              >
                <ChevronUp className="h-4 w-4" />
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <h4 className="font-medium text-blue-900 mb-2">{dailyTips[currentTip].title}</h4>
            <p className="text-blue-800 text-sm">{dailyTips[currentTip].content}</p>
          </CardContent>
        </Card>
      )}

      {/* Collapsed Tips Button */}
      {tipsCollapsed && (
        <Button
          variant="outline"
          onClick={() => setTipsCollapsed(false)}
          className="w-full border-blue-200 text-blue-600 hover:bg-blue-50"
        >
          <Lightbulb className="mr-2 h-4 w-4" />
          Show Daily HR Tip
          <ChevronDown className="ml-2 h-4 w-4" />
        </Button>
      )}

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Employees</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalEmployees}</div>
            <p className="text-xs text-muted-foreground">
              {stats.activeEmployees} active
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Recent Queries</CardTitle>
            <MessageSquare className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.recentQueries}</div>
            <p className="text-xs text-muted-foreground">
              Last 10 interactions
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">AI Coins</CardTitle>
            <Coins className="h-4 w-4 text-yellow-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-yellow-600">
              {stats.subscription?.coins_balance || 0}
            </div>
            <p className="text-xs text-muted-foreground">
              HR Advisor queries remaining
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Quick Actions</CardTitle>
            <Plus className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <Button 
                variant="outline" 
                size="sm" 
                className="w-full justify-start"
                onClick={() => onPageChange('employees')}
              >
                <Users className="mr-2 h-3 w-3" />
                Add Employee
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Activity - Takes 2 columns */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Recent HR Queries</CardTitle>
              <CardDescription>
                Your latest interactions with the HR Advisor
              </CardDescription>
            </CardHeader>
            <CardContent>
              {recentActivity.length > 0 ? (
                <div className="space-y-4">
                  {recentActivity.map((activity) => (
                    <div key={activity.prompt_id} className="flex items-start space-x-3">
                      <div className="flex-shrink-0">
                        <MessageSquare className="h-5 w-5 text-blue-500" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm text-gray-900 truncate">
                          {activity.prompt_text}
                        </p>
                        <div className="flex items-center mt-1 space-x-2">
                          <Badge variant="secondary" className="text-xs">
                            {activity.country_context || 'General'}
                          </Badge>
                          <span className="text-xs text-gray-500">
                            {formatDate(activity.timestamp)}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                  <Button 
                    variant="outline" 
                    className="w-full"
                    onClick={() => onPageChange('history')}
                  >
                    View All History
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </div>
              ) : (
                <div className="text-center py-6">
                  <MessageSquare className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">No queries yet</h3>
                  <p className="mt-1 text-sm text-gray-500">
                    Start by asking the HR Advisor a question
                  </p>
                  <Button 
                    className="mt-4"
                    onClick={() => onPageChange('hr-advisor')}
                  >
                    Ask a Question
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Getting Started Guide - Single column */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Target className="mr-2 h-5 w-5" />
              Getting Started
            </CardTitle>
            <CardDescription>
              Quick tips to make the most of your HR platform
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0">
                  <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center">
                    <span className="text-xs font-medium text-blue-600">1</span>
                  </div>
                </div>
                <div>
                  <h4 className="text-sm font-medium">Add your team</h4>
                  <p className="text-sm text-gray-500">
                    Start by adding employee information to get personalized advice
                  </p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0">
                  <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center">
                    <span className="text-xs font-medium text-blue-600">2</span>
                  </div>
                </div>
                <div>
                  <h4 className="text-sm font-medium">Ask HR questions</h4>
                  <p className="text-sm text-gray-500">
                    Get instant answers to HR policies, compliance, and best practices
                  </p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0">
                  <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center">
                    <span className="text-xs font-medium text-blue-600">3</span>
                  </div>
                </div>
                <div>
                  <h4 className="text-sm font-medium">Manage workflows</h4>
                  <p className="text-sm text-gray-500">
                    Create and track HR processes and compliance
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default Dashboard
