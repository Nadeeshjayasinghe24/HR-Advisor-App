import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { 
  Users, 
  TrendingUp, 
  TrendingDown, 
  Clock, 
  Heart, 
  UserMinus, 
  UserPlus,
  Building,
  MapPin,
  Calendar,
  Target,
  AlertTriangle,
  CheckCircle,
  BarChart3,
  PieChart,
  Activity
} from 'lucide-react'

const HRAnalyticsDashboard = ({ token }) => {
  const [analytics, setAnalytics] = useState({
    headcount: {
      total: 0,
      byDepartment: {},
      byLocation: {},
      byEmploymentType: {},
      byWorkArrangement: {}
    },
    turnover: {
      rate: 0,
      voluntary: 0,
      involuntary: 0,
      trend: []
    },
    hiring: {
      newHires: 0,
      exits: 0,
      netGrowth: 0,
      timeToHire: 0,
      trend: []
    },
    engagement: {
      averageScore: 0,
      distribution: {},
      lastSurveyDate: null,
      responseRate: 0
    },
    absenteeism: {
      rate: 0,
      unplannedAbsences: 0,
      trend: []
    },
    diversity: {
      gender: {},
      age: {},
      ethnicity: {}
    }
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    try {
      const response = await fetch('https://hr-advisor-app.onrender.com/api/employees/analytics', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        setAnalytics(data)
      } else {
        setError('Failed to fetch analytics data')
      }
    } catch (err) {
      setError('Error fetching analytics: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const formatPercentage = (value) => {
    return `${(value || 0).toFixed(1)}%`
  }

  const formatNumber = (value) => {
    return (value || 0).toLocaleString()
  }

  const getStatusColor = (value, threshold = 5) => {
    if (value > threshold) return 'text-red-600'
    if (value > threshold / 2) return 'text-yellow-600'
    return 'text-green-600'
  }

  const getTrendIcon = (trend) => {
    if (trend > 0) return <TrendingUp className="h-4 w-4 text-green-600" />
    if (trend < 0) return <TrendingDown className="h-4 w-4 text-red-600" />
    return <Activity className="h-4 w-4 text-gray-400" />
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-2 text-gray-600">Loading analytics...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">HR Analytics Dashboard</h2>
          <p className="text-gray-600">Real-time insights into your workforce</p>
        </div>
        <Badge variant="outline" className="flex items-center space-x-1">
          <Activity className="h-3 w-3" />
          <span>Live Data</span>
        </Badge>
      </div>

      {error && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="p-4">
            <div className="flex items-center space-x-2 text-red-800">
              <AlertTriangle className="h-4 w-4" />
              <span>{error}</span>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Key Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Headcount</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatNumber(analytics.headcount.total)}</div>
            <p className="text-xs text-muted-foreground">
              Active employees
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Turnover Rate</CardTitle>
            <UserMinus className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className={`text-2xl font-bold ${getStatusColor(analytics.turnover.rate)}`}>
              {formatPercentage(analytics.turnover.rate)}
            </div>
            <p className="text-xs text-muted-foreground">
              {formatPercentage(analytics.turnover.voluntary)} voluntary
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Net Growth</CardTitle>
            <div className="flex items-center space-x-1">
              {getTrendIcon(analytics.hiring.netGrowth)}
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {analytics.hiring.netGrowth > 0 ? '+' : ''}{formatNumber(analytics.hiring.netGrowth)}
            </div>
            <p className="text-xs text-muted-foreground">
              {formatNumber(analytics.hiring.newHires)} hires, {formatNumber(analytics.hiring.exits)} exits
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Engagement Score</CardTitle>
            <Heart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {analytics.engagement.averageScore ? analytics.engagement.averageScore.toFixed(1) : 'N/A'}
            </div>
            <p className="text-xs text-muted-foreground">
              Out of 10.0
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Analytics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Headcount Breakdown */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Building className="h-5 w-5" />
              <span>Headcount Breakdown</span>
            </CardTitle>
            <CardDescription>Distribution across departments and locations</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h4 className="font-medium mb-2">By Department</h4>
              <div className="space-y-2">
                {Object.entries(analytics.headcount.byDepartment).map(([dept, count]) => (
                  <div key={dept} className="flex justify-between items-center">
                    <span className="text-sm">{dept}</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-20 bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full" 
                          style={{ width: `${(count / analytics.headcount.total) * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-sm font-medium w-8">{count}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h4 className="font-medium mb-2">By Employment Type</h4>
              <div className="space-y-2">
                {Object.entries(analytics.headcount.byEmploymentType).map(([type, count]) => (
                  <div key={type} className="flex justify-between items-center">
                    <span className="text-sm">{type}</span>
                    <Badge variant="outline">{count}</Badge>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Turnover Analysis */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <UserMinus className="h-5 w-5" />
              <span>Turnover Analysis</span>
            </CardTitle>
            <CardDescription>Voluntary vs involuntary departures</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center p-4 bg-red-50 rounded-lg">
                <div className="text-2xl font-bold text-red-600">
                  {formatPercentage(analytics.turnover.voluntary)}
                </div>
                <div className="text-sm text-red-700">Voluntary</div>
              </div>
              <div className="text-center p-4 bg-orange-50 rounded-lg">
                <div className="text-2xl font-bold text-orange-600">
                  {formatPercentage(analytics.turnover.involuntary)}
                </div>
                <div className="text-sm text-orange-700">Involuntary</div>
              </div>
            </div>
            
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium">Overall Turnover Rate</span>
                <span className={`text-sm font-bold ${getStatusColor(analytics.turnover.rate)}`}>
                  {formatPercentage(analytics.turnover.rate)}
                </span>
              </div>
              <Progress 
                value={analytics.turnover.rate} 
                className="h-2"
                max={20}
              />
              <p className="text-xs text-gray-500 mt-1">
                Industry benchmark: 10-15%
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Time to Hire & Recruitment */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Clock className="h-5 w-5" />
              <span>Recruitment Metrics</span>
            </CardTitle>
            <CardDescription>Hiring efficiency and trends</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <div className="text-2xl font-bold">{analytics.hiring.timeToHire || 'N/A'}</div>
                <div className="text-sm text-gray-600">Days to hire</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-green-600">
                  {formatNumber(analytics.hiring.newHires)}
                </div>
                <div className="text-sm text-gray-600">New hires (30d)</div>
              </div>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-2">
                <UserPlus className="h-4 w-4 text-green-600" />
                <span className="text-sm">Hiring Trend</span>
              </div>
              <div className="flex items-center space-x-1">
                {getTrendIcon(analytics.hiring.netGrowth)}
                <span className="text-sm font-medium">
                  {analytics.hiring.netGrowth > 0 ? 'Growing' : analytics.hiring.netGrowth < 0 ? 'Declining' : 'Stable'}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Absenteeism & Wellness */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <AlertTriangle className="h-5 w-5" />
              <span>Absenteeism & Wellness</span>
            </CardTitle>
            <CardDescription>Unplanned leave and wellness indicators</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium">Absenteeism Rate</span>
                <span className={`text-lg font-bold ${getStatusColor(analytics.absenteeism.rate, 3)}`}>
                  {formatPercentage(analytics.absenteeism.rate)}
                </span>
              </div>
              <Progress 
                value={analytics.absenteeism.rate} 
                className="h-2"
                max={10}
              />
              <p className="text-xs text-gray-500 mt-1">
                Target: &lt;3%
              </p>
            </div>
            
            <div className="p-3 bg-yellow-50 rounded-lg">
              <div className="flex items-center space-x-2 mb-1">
                <AlertTriangle className="h-4 w-4 text-yellow-600" />
                <span className="text-sm font-medium">Unplanned Absences</span>
              </div>
              <div className="text-lg font-bold text-yellow-700">
                {formatNumber(analytics.absenteeism.unplannedAbsences)}
              </div>
              <div className="text-xs text-yellow-600">This month</div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Diversity & Inclusion */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Users className="h-5 w-5" />
            <span>Diversity & Inclusion</span>
          </CardTitle>
          <CardDescription>Workforce demographics and representation</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <h4 className="font-medium mb-3">Gender Distribution</h4>
              <div className="space-y-2">
                {Object.entries(analytics.diversity.gender).map(([gender, count]) => (
                  <div key={gender} className="flex justify-between items-center">
                    <span className="text-sm capitalize">{gender}</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-16 bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-purple-600 h-2 rounded-full" 
                          style={{ width: `${(count / analytics.headcount.total) * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-sm font-medium">{formatPercentage((count / analytics.headcount.total) * 100)}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h4 className="font-medium mb-3">Age Groups</h4>
              <div className="space-y-2">
                {Object.entries(analytics.diversity.age).map(([ageGroup, count]) => (
                  <div key={ageGroup} className="flex justify-between items-center">
                    <span className="text-sm">{ageGroup}</span>
                    <Badge variant="outline">{count}</Badge>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h4 className="font-medium mb-3">Work Arrangements</h4>
              <div className="space-y-2">
                {Object.entries(analytics.headcount.byWorkArrangement).map(([arrangement, count]) => (
                  <div key={arrangement} className="flex justify-between items-center">
                    <span className="text-sm">{arrangement}</span>
                    <Badge variant="outline">{count}</Badge>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default HRAnalyticsDashboard

