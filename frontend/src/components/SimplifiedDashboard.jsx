import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { 
  MessageCircle, 
  Users, 
  TrendingUp, 
  Calendar, 
  Bell, 
  Search,
  Plus,
  BarChart3,
  CheckCircle,
  AlertCircle,
  Clock,
  Sparkles,
  ArrowRight,
  User,
  FileText,
  Settings
} from 'lucide-react';

const SimplifiedDashboard = () => {
  const [user, setUser] = useState({ name: 'Sarah', role: 'HR Manager' });
  const [chatInput, setChatInput] = useState('');
  const [quickStats, setQuickStats] = useState({
    totalEmployees: 125,
    satisfactionScore: 95,
    openPositions: 3,
    reviewsDue: 7
  });
  const [todaysFocus, setTodaysFocus] = useState([
    { id: 1, text: '3 employees need check-ins', type: 'action', priority: 'medium' },
    { id: 2, text: 'Performance reviews due next week', type: 'deadline', priority: 'high' },
    { id: 3, text: 'New hire onboarding ready', type: 'process', priority: 'low' }
  ]);
  const [smartInsights, setSmartInsights] = useState([
    { id: 1, text: '3 employees at retention risk in Engineering', type: 'warning' },
    { id: 2, text: 'Marketing team satisfaction up 12% this month', type: 'success' },
    { id: 3, text: 'Recommended: Schedule team building for Sales', type: 'suggestion' }
  ]);
  const [recentActivity, setRecentActivity] = useState([
    { id: 1, action: 'John Smith completed onboarding', time: '2 hours ago', type: 'completion' },
    { id: 2, action: 'Performance review scheduled for Engineering team', time: '4 hours ago', type: 'scheduled' },
    { id: 3, action: 'New policy document generated', time: '1 day ago', type: 'document' }
  ]);

  const handleChatSubmit = (e) => {
    e.preventDefault();
    if (chatInput.trim()) {
      // This would integrate with the AI assistant
      console.log('User query:', chatInput);
      setChatInput('');
      // Show loading state and then AI response
    }
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 17) return 'Good afternoon';
    return 'Good evening';
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800 border-red-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getInsightIcon = (type) => {
    switch (type) {
      case 'warning': return <AlertCircle className="h-4 w-4 text-amber-500" />;
      case 'success': return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'suggestion': return <Sparkles className="h-4 w-4 text-blue-500" />;
      default: return <Bell className="h-4 w-4 text-gray-500" />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-gray-900">
              {getGreeting()}, {user.name}! 👋
            </h1>
            <p className="text-gray-600 mt-1">Ready to make HR simple and effective</p>
          </div>
          <div className="flex items-center space-x-3 mt-4 md:mt-0">
            <Button variant="outline" size="sm">
              <Settings className="h-4 w-4 mr-2" />
              Settings
            </Button>
            <Button variant="outline" size="sm">
              <Bell className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* AI Assistant Chat */}
        <Card className="border-2 border-blue-200 bg-gradient-to-r from-blue-50 to-indigo-50">
          <CardContent className="p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="p-2 bg-blue-100 rounded-full">
                <MessageCircle className="h-5 w-5 text-blue-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">AI Assistant</h3>
                <p className="text-sm text-gray-600">Ask me anything about HR</p>
              </div>
            </div>
            
            <form onSubmit={handleChatSubmit} className="flex space-x-3">
              <Input
                placeholder="How can I help you today? (e.g., 'Schedule performance reviews for engineering team')"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                className="flex-1 text-base"
              />
              <Button type="submit" className="px-6">
                <ArrowRight className="h-4 w-4" />
              </Button>
            </form>
            
            <div className="flex flex-wrap gap-2 mt-4">
              <Button variant="outline" size="sm" onClick={() => setChatInput('Show me employees at retention risk')}>
                Retention Risk
              </Button>
              <Button variant="outline" size="sm" onClick={() => setChatInput('Create performance review template')}>
                Performance Reviews
              </Button>
              <Button variant="outline" size="sm" onClick={() => setChatInput('Generate team report')}>
                Team Reports
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Quick Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-blue-100 rounded-full">
                  <Users className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900">{quickStats.totalEmployees}</p>
                  <p className="text-sm text-gray-600">Employees</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-green-100 rounded-full">
                  <TrendingUp className="h-5 w-5 text-green-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900">{quickStats.satisfactionScore}%</p>
                  <p className="text-sm text-gray-600">Satisfaction</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-purple-100 rounded-full">
                  <Calendar className="h-5 w-5 text-purple-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900">{quickStats.reviewsDue}</p>
                  <p className="text-sm text-gray-600">Reviews Due</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-amber-100 rounded-full">
                  <Plus className="h-5 w-5 text-amber-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900">{quickStats.openPositions}</p>
                  <p className="text-sm text-gray-600">Open Roles</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          
          {/* Today's Focus */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Clock className="h-5 w-5 text-blue-600" />
                <span>Today's Focus</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {todaysFocus.map((item) => (
                <div key={item.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className={`w-3 h-3 rounded-full ${
                      item.priority === 'high' ? 'bg-red-500' :
                      item.priority === 'medium' ? 'bg-yellow-500' : 'bg-green-500'
                    }`}></div>
                    <span className="text-sm font-medium text-gray-900">{item.text}</span>
                  </div>
                  <Button variant="ghost" size="sm">
                    <ArrowRight className="h-4 w-4" />
                  </Button>
                </div>
              ))}
              
              <Button variant="outline" className="w-full mt-4">
                <Plus className="h-4 w-4 mr-2" />
                Add Task
              </Button>
            </CardContent>
          </Card>

          {/* Smart Insights */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Sparkles className="h-5 w-5 text-purple-600" />
                <span>AI Insights</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {smartInsights.map((insight) => (
                <div key={insight.id} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                  {getInsightIcon(insight.type)}
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">{insight.text}</p>
                  </div>
                  <Button variant="ghost" size="sm">
                    <ArrowRight className="h-4 w-4" />
                  </Button>
                </div>
              ))}
              
              <Button variant="outline" className="w-full mt-4">
                <BarChart3 className="h-4 w-4 mr-2" />
                View All Insights
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Button variant="outline" className="h-20 flex-col space-y-2">
                <User className="h-6 w-6" />
                <span className="text-sm">Add Employee</span>
              </Button>
              
              <Button variant="outline" className="h-20 flex-col space-y-2">
                <FileText className="h-6 w-6" />
                <span className="text-sm">Generate Report</span>
              </Button>
              
              <Button variant="outline" className="h-20 flex-col space-y-2">
                <Calendar className="h-6 w-6" />
                <span className="text-sm">Schedule Review</span>
              </Button>
              
              <Button variant="outline" className="h-20 flex-col space-y-2">
                <Search className="h-6 w-6" />
                <span className="text-sm">Find Employee</span>
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>Recent Activity</span>
              <Button variant="ghost" size="sm">View All</Button>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {recentActivity.map((activity) => (
                <div key={activity.id} className="flex items-center space-x-3 p-3 hover:bg-gray-50 rounded-lg transition-colors">
                  <div className={`w-2 h-2 rounded-full ${
                    activity.type === 'completion' ? 'bg-green-500' :
                    activity.type === 'scheduled' ? 'bg-blue-500' : 'bg-purple-500'
                  }`}></div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">{activity.action}</p>
                    <p className="text-xs text-gray-500">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

      </div>
    </div>
  );
};

export default SimplifiedDashboard;

