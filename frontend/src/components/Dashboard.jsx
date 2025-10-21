import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Search,
  Bell,
  Users, 
  MessageSquare, 
  TrendingUp, 
  Clock,
  Plus,
  Lightbulb,
  BarChart3,
  Calendar,
  ChevronRight,
  Settings
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
  const [currentMonth, setCurrentMonth] = useState(new Date())

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

  const upcomingTasks = [
    {
      id: 1,
      date: '05',
      title: 'UI/UX workshop',
      time: '8:00-12:00 sessions, Mrs. Wilson',
      fullTime: '14:00-14:45'
    },
    {
      id: 2,
      date: '06',
      title: 'Interaction design',
      time: '8:00-12:00 sessions, Mrs. Wilson',
      fullTime: '11:00-14:45'
    },
    {
      id: 3,
      date: '07',
      title: 'Team Meeting',
      time: '8:00-12:00 meetings, Design team',
      fullTime: '12:00-13:35'
    },
    {
      id: 4,
      date: '08',
      title: 'User Interview',
      time: '8:00-12:00 sessions, Design team',
      fullTime: '16:00-17:00'
    },
    {
      id: 5,
      date: '09',
      title: 'User Interview',
      time: '8:00-12:00 sessions, Design team',
      fullTime: '16:00-17:00'
    }
  ]

  useEffect(() => {
    fetchDashboardData()
  }, [])

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
        const activities = Array.isArray(historyData) ? historyData : (historyData.data || [])
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

  const getDaysInMonth = (date) => {
    return new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate()
  }

  const getFirstDayOfMonth = (date) => {
    return new Date(date.getFullYear(), date.getMonth(), 1).getDay()
  }

  const renderCalendar = () => {
    const daysInMonth = getDaysInMonth(currentMonth)
    const firstDay = getFirstDayOfMonth(currentMonth)
    const days = []
    
    // Empty cells for days before month starts
    for (let i = 0; i < firstDay; i++) {
      days.push(<div key={`empty-${i}`} className="text-center py-2"></div>)
    }
    
    // Days of the month
    for (let day = 1; day <= daysInMonth; day++) {
      days.push(
        <div key={day} className="text-center py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded cursor-pointer">
          {day}
        </div>
      )
    }
    
    return days
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="h-32 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Good morning, {user?.first_name || 'User'}
          </h1>
          <p className="text-gray-600 mt-1">
            Your personal dashboard to manage HR and growth knowledge.
          </p>
        </div>
        <Button variant="outline" className="border-blue-500 text-blue-600 hover:bg-blue-50">
          Account settings
        </Button>
      </div>

      {/* Quick Actions Section */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick action</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {quickActions.map((action) => {
            const Icon = action.icon
            return (
              <div key={action.id} className={`${action.color} rounded-lg p-6 text-white cursor-pointer hover:shadow-lg transition-shadow`}>
                <div className="flex items-start justify-between mb-8">
                  <div className="bg-white bg-opacity-20 p-3 rounded-lg">
                    <Icon className="h-6 w-6" />
                  </div>
                </div>
                <div>
                  <p className="text-2xl font-bold mb-1">{action.value}</p>
                  <p className="text-sm text-white text-opacity-90">{action.description}</p>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* My Tasks Section */}
        <div className="lg:col-span-1">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">My tasks</CardTitle>
              <CardDescription>2 out of 5 tasks</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {[
                { name: 'Admira', task: 'Interview with developer', status: 'Due today' },
                { name: 'Admira', task: 'Reflection time', status: 'Tomorrow' },
                { name: 'Admira', task: 'Sprint questions preparation', status: 'Due today' }
              ].map((item, idx) => (
                <div key={idx} className="flex items-start space-x-3 pb-3 border-b last:border-b-0">
                  <div className="w-8 h-8 rounded-full bg-gray-300 flex-shrink-0"></div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900">{item.name}</p>
                    <p className="text-xs text-gray-600">{item.task}</p>
                    <p className={`text-xs mt-1 ${item.status === 'Due today' ? 'text-red-600' : 'text-orange-600'}`}>
                      {item.status}
                    </p>
                  </div>
                </div>
              ))}
              <button className="text-blue-600 text-sm font-medium mt-2 hover:text-blue-700">
                See all tasks
              </button>
            </CardContent>
          </Card>
        </div>

        {/* Calendar and Upcoming Tasks */}
        <div className="lg:col-span-2 space-y-6">
          {/* Calendar */}
          <Card>
            <CardHeader>
              <div className="flex justify-between items-center">
                <CardTitle>December 2023</CardTitle>
                <div className="flex space-x-2">
                  <button className="text-gray-400 hover:text-gray-600">←</button>
                  <button className="text-gray-400 hover:text-gray-600">→</button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-7 gap-2 mb-4">
                {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
                  <div key={day} className="text-center text-xs font-semibold text-gray-600 py-2">
                    {day}
                  </div>
                ))}
                {renderCalendar()}
              </div>
            </CardContent>
          </Card>

          {/* Upcoming Calendar Tasks */}
          <Card>
            <CardHeader>
              <CardTitle>Upcoming calendar tasks</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {upcomingTasks.map((task) => (
                <div key={task.id} className="flex items-start space-x-4 pb-3 border-b last:border-b-0">
                  <div className="text-center">
                    <div className="w-10 h-10 bg-blue-100 rounded flex items-center justify-center">
                      <span className="text-sm font-semibold text-blue-600">{task.date}</span>
                    </div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900">{task.title}</p>
                    <p className="text-xs text-gray-600 mt-1">{task.time}</p>
                  </div>
                  <div className="text-right text-xs text-gray-500 flex-shrink-0">
                    {task.fullTime}
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Bottom Section - Next Retrospective, Sprint, and Chart */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Next Retrospective */}
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Next retrospective</CardTitle>
            <CardDescription>Week 2</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex space-x-2">
              {[1, 2, 3].map(i => (
                <div key={i} className="w-8 h-8 rounded-full bg-gray-300"></div>
              ))}
              <div className="text-xs text-gray-600 flex items-center ml-2">Design team</div>
            </div>
          </CardContent>
        </Card>

        {/* Next Sprint */}
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Next sprint</CardTitle>
            <CardDescription>Week 3</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex space-x-2">
              {[1, 2, 3].map(i => (
                <div key={i} className="w-8 h-8 rounded-full bg-gray-300"></div>
              ))}
              <div className="text-xs text-gray-600 flex items-center ml-2">Design team</div>
            </div>
          </CardContent>
        </Card>

        {/* Calendar Button */}
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Calendar</CardTitle>
          </CardHeader>
          <CardContent>
            <Button className="w-full bg-blue-500 hover:bg-blue-600 text-white">
              <Calendar className="mr-2 h-4 w-4" />
              View Calendar
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Total Working Hours Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Total working hours</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-end justify-between h-48 space-x-2">
            {[8, 6, 7, 5, 8, 6, 7, 8].map((hours, idx) => (
              <div key={idx} className="flex-1 flex flex-col items-center">
                <div className="w-full bg-gray-200 rounded-t" style={{ height: `${(hours / 8) * 100}%` }}>
                  <div className="w-full h-1/2 bg-blue-500 rounded-t"></div>
                </div>
                <span className="text-xs text-gray-600 mt-2">Day {idx + 1}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Dashboard

