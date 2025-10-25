import { useState, useEffect } from 'react'
import { 
  Lightbulb,
  TrendingUp, 
  MessageSquare,
  BarChart3,
  ChevronRight
} from 'lucide-react'

const Dashboard = ({ token, user }) => {
  const [stats, setStats] = useState({
    totalEmployees: 0,
    activeEmployees: 0,
    recentQueries: 0,
    subscription: null
  })
  const [recentActivity, setRecentActivity] = useState([])
  const [loading, setLoading] = useState(true)

  const quickActions = [
    {
      id: 1,
      title: 'Reflection time',
      icon: Lightbulb,
      color: 'bg-blue-500',
      value: '2h 30m',
      description: 'This week'
    },
    {
      id: 2,
      title: 'Daily progress',
      icon: TrendingUp,
      color: 'bg-teal-500',
      value: '82%',
      description: 'This week'
    },
    {
      id: 3,
      title: 'FAQ',
      icon: MessageSquare,
      color: 'bg-purple-500',
      value: '12',
      description: 'Questions'
    }
  ]

  useEffect(() => {
    fetchDashboardData()
  }, [token])

  const fetchDashboardData = async () => {
    try {
      // Fetch subscription info
      const subResponse = await fetch(`https://hr-advisor-app.onrender.com/api/subscriptions`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
      
      if (subResponse.ok) {
        const subData = await subResponse.json()
        setStats(prev => ({ ...prev, subscription: subData }))
      }
      
      // Fetch recent activity
      const historyResponse = await fetch(`https://hr-advisor-app.onrender.com/api/history/prompts/recent`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
      
      if (historyResponse.ok) {
        const historyData = await historyResponse.json()
        // Handle both array and object responses
        const activities = Array.isArray(historyData) ? historyData : (historyData.recent_prompts || [])
        setRecentActivity(activities.slice(0, 5))
        setStats(prev => ({ ...prev, recentQueries: activities.length }))
      }

      // Fetch employees (for count)
      const empResponse = await fetch(`https://hr-advisor-app.onrender.com/api/employees?per_page=1`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
      
      if (empResponse.ok) {
        const empData = await empResponse.json()
        setStats(prev => ({ 
          ...prev, 
          totalEmployees: empData.total || 0,
          activeEmployees: empData.total || 0
        }))
      }

    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold text-gray-900">Good morning, {user?.first_name || 'User'}</h1>
        <p className="text-gray-600">Your personal dashboard to manage HR and growth knowledge.</p>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {quickActions.map((action) => {
          const Icon = action.icon
          return (
            <div key={action.id} className={`${action.color} rounded-lg p-6 text-white shadow-md`}>
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm font-medium opacity-90">{action.title}</p>
                  <p className="text-2xl font-bold mt-2">{action.value}</p>
                  <p className="text-xs opacity-75 mt-1">{action.description}</p>
                </div>
                <Icon className="h-8 w-8 opacity-80" />
              </div>
            </div>
          )
        })}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* My Tasks */}
        <div className="lg:col-span-2 bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">My tasks</h2>
          <p className="text-sm text-gray-500 mb-4">2 out of 5 tasks</p>
          
          <div className="space-y-3">
            {[
              { name: 'Interview with developer', date: 'Due today', color: 'text-red-600' },
              { name: 'Reflection time', date: 'Tomorrow', color: 'text-orange-600' },
              { name: 'Sprint questions preparation', date: 'Due today', color: 'text-red-600' }
            ].map((task, idx) => (
              <div key={idx} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-b-0">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center text-sm font-medium text-gray-600">
                    {user?.first_name?.charAt(0) || 'A'}
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">{task.name}</p>
                    <p className={`text-xs ${task.color}`}>{task.date}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          <button className="text-blue-600 text-sm font-medium mt-4 hover:text-blue-700">
            See all tasks →
          </button>
        </div>

        {/* Calendar */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">December 2023</h2>
          
          <div className="grid grid-cols-7 gap-2 mb-4">
            {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
              <div key={day} className="text-center text-xs font-medium text-gray-500 py-2">
                {day}
              </div>
            ))}
            
            {Array.from({ length: 31 }, (_, i) => (
              <div key={i} className="text-center text-sm py-2 text-gray-700 hover:bg-blue-50 rounded cursor-pointer">
                {i + 1}
              </div>
            ))}
          </div>

          <div className="border-t pt-4">
            <h3 className="text-sm font-semibold text-gray-900 mb-3">Upcoming calendar tasks</h3>
            <div className="space-y-2 text-xs">
              {[
                { date: '05', title: 'UI/UX workshop', time: '14:00-14:45' },
                { date: '06', title: 'Interaction design', time: '11:00-14:45' },
                { date: '07', title: 'Team Meeting', time: '12:00-13:35' },
                { date: '08', title: 'User Interview', time: '16:00-17:00' },
                { date: '09', title: 'User Interview', time: '16:00-17:00' }
              ].map((task, idx) => (
                <div key={idx} className="flex justify-between text-gray-600 py-1">
                  <span>{task.date} - {task.title}</span>
                  <span className="text-gray-400">{task.time}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      {recentActivity.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h2>
          <div className="space-y-4">
            {recentActivity.map((activity, idx) => (
              <div key={idx} className="flex items-start gap-4 pb-4 border-b border-gray-100 last:border-b-0">
                <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
                  <MessageSquare className="h-5 w-5 text-blue-600" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {activity.prompt_text?.substring(0, 50)}...
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    {new Date(activity.timestamp).toLocaleDateString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow-sm p-6">
          <p className="text-gray-600 text-sm">Total Employees</p>
          <p className="text-2xl font-bold text-gray-900 mt-2">{stats.totalEmployees}</p>
        </div>
        <div className="bg-white rounded-lg shadow-sm p-6">
          <p className="text-gray-600 text-sm">Active Employees</p>
          <p className="text-2xl font-bold text-gray-900 mt-2">{stats.activeEmployees}</p>
        </div>
        <div className="bg-white rounded-lg shadow-sm p-6">
          <p className="text-gray-600 text-sm">Recent Queries</p>
          <p className="text-2xl font-bold text-gray-900 mt-2">{stats.recentQueries}</p>
        </div>
        <div className="bg-white rounded-lg shadow-sm p-6">
          <p className="text-gray-600 text-sm">Subscription</p>
          <p className="text-lg font-bold text-gray-900 mt-2">{stats.subscription?.plan_type || 'Free'}</p>
        </div>
      </div>
    </div>
  )
}

export default Dashboard

