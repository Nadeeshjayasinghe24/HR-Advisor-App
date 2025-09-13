import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Lightbulb, 
  Users, 
  Heart, 
  Target, 
  Coffee, 
  Zap,
  RefreshCw,
  Calendar,
  Star
} from 'lucide-react'

const DailyTips = () => {
  const [currentTip, setCurrentTip] = useState(null)
  const [tipIndex, setTipIndex] = useState(0)

  const hrTips = [
    {
      category: "Best Practice",
      icon: <Star className="h-5 w-5" />,
      title: "The 1-on-1 Rule",
      content: "Schedule regular 1-on-1 meetings with your team members. Even 15 minutes monthly can dramatically improve engagement and catch issues early.",
      actionable: "Block 30 minutes this week to schedule recurring 1-on-1s with your direct reports.",
      color: "bg-blue-50 border-blue-200 text-blue-800"
    },
    {
      category: "Team Building",
      icon: <Users className="h-5 w-5" />,
      title: "Virtual Coffee Chats",
      content: "Create informal 'coffee chat' slots where team members can book 15-minute casual conversations with colleagues from other departments.",
      actionable: "Set up a shared calendar link for voluntary cross-department coffee chats this month.",
      color: "bg-green-50 border-green-200 text-green-800"
    },
    {
      category: "Wellness",
      icon: <Heart className="h-5 w-5" />,
      title: "Mental Health Check-ins",
      content: "Include a simple 'How are you feeling today?' question in team meetings. It normalizes mental health discussions and shows you care.",
      actionable: "Add a 2-minute wellness check-in to your next team meeting agenda.",
      color: "bg-pink-50 border-pink-200 text-pink-800"
    },
    {
      category: "Performance",
      icon: <Target className="h-5 w-5" />,
      title: "Micro-Recognition",
      content: "Acknowledge small wins immediately. A quick 'Great job on that email response' can be more impactful than formal quarterly reviews.",
      actionable: "Send one specific recognition message to a team member today.",
      color: "bg-purple-50 border-purple-200 text-purple-800"
    },
    {
      category: "Culture",
      icon: <Coffee className="h-5 w-5" />,
      title: "Learning Lunch Sessions",
      content: "Host monthly 'Lunch & Learn' sessions where employees share skills, hobbies, or industry insights with colleagues.",
      actionable: "Ask your team what skills they'd like to share or learn about in a casual lunch setting.",
      color: "bg-orange-50 border-orange-200 text-orange-800"
    },
    {
      category: "Productivity",
      icon: <Zap className="h-5 w-5" />,
      title: "No-Meeting Mornings",
      content: "Protect the first 2 hours of Tuesday and Thursday for deep work. No meetings, no interruptions - just focused productivity time.",
      actionable: "Block 8-10 AM on Tuesdays and Thursdays as 'Focus Time' for your team.",
      color: "bg-yellow-50 border-yellow-200 text-yellow-800"
    },
    {
      category: "Communication",
      icon: <Lightbulb className="h-5 w-5" />,
      title: "The 24-Hour Rule",
      content: "For sensitive emails or feedback, write it, save as draft, and review after 24 hours. This prevents reactive communication.",
      actionable: "Practice the 24-hour rule on your next challenging email or feedback conversation.",
      color: "bg-indigo-50 border-indigo-200 text-indigo-800"
    },
    {
      category: "Development",
      icon: <Target className="h-5 w-5" />,
      title: "Skill Swap Program",
      content: "Pair employees to teach each other skills - marketing teaches sales about campaigns, IT teaches everyone about security.",
      actionable: "Identify 2-3 skill-sharing pairs in your organization and facilitate introductions.",
      color: "bg-teal-50 border-teal-200 text-teal-800"
    },
    {
      category: "Engagement",
      icon: <Users className="h-5 w-5" />,
      title: "Reverse Mentoring",
      content: "Have junior employees mentor senior staff on new technologies, social media, or generational perspectives. Everyone learns.",
      actionable: "Identify one junior-senior pairing for reverse mentoring this quarter.",
      color: "bg-cyan-50 border-cyan-200 text-cyan-800"
    },
    {
      category: "Innovation",
      icon: <Lightbulb className="h-5 w-5" />,
      title: "15% Time",
      content: "Allow employees to spend 15% of their time on passion projects or process improvements. Google's Gmail came from 20% time!",
      actionable: "Discuss with leadership about implementing a monthly 'innovation day' for your team.",
      color: "bg-emerald-50 border-emerald-200 text-emerald-800"
    },
    {
      category: "Feedback",
      icon: <Heart className="h-5 w-5" />,
      title: "Start-Stop-Continue",
      content: "Use this simple feedback framework: What should we start doing? Stop doing? Continue doing? It's less intimidating than formal reviews.",
      actionable: "Try the Start-Stop-Continue format in your next team retrospective or 1-on-1.",
      color: "bg-rose-50 border-rose-200 text-rose-800"
    },
    {
      category: "Onboarding",
      icon: <Users className="h-5 w-5" />,
      title: "Buddy System Plus",
      content: "Assign new hires a buddy for their first month, plus a 'culture guide' from a different department to broaden their network.",
      actionable: "Create a list of potential buddies and culture guides for your next new hire.",
      color: "bg-violet-50 border-violet-200 text-violet-800"
    },
    {
      category: "Recognition",
      icon: <Star className="h-5 w-5" />,
      title: "Peer Nomination System",
      content: "Let employees nominate colleagues for monthly recognition. Peer recognition often means more than top-down praise.",
      actionable: "Set up a simple peer nomination system using a shared form or Slack channel.",
      color: "bg-amber-50 border-amber-200 text-amber-800"
    },
    {
      category: "Work-Life Balance",
      icon: <Heart className="h-5 w-5" />,
      title: "Meeting-Free Fridays",
      content: "Protect Friday afternoons from meetings. Use this time for planning next week, learning, or wrapping up loose ends.",
      actionable: "Propose 'Meeting-Free Friday Afternoons' to your leadership team.",
      color: "bg-lime-50 border-lime-200 text-lime-800"
    },
    {
      category: "Diversity",
      icon: <Users className="h-5 w-5" />,
      title: "Inclusive Language Check",
      content: "Review your job postings and internal communications for inclusive language. Tools like Textio can help identify biased phrasing.",
      actionable: "Audit your last 3 job postings for inclusive language and make improvements.",
      color: "bg-sky-50 border-sky-200 text-sky-800"
    }
  ]

  useEffect(() => {
    // Get today's tip based on date to ensure consistency
    const today = new Date()
    const dayOfYear = Math.floor((today - new Date(today.getFullYear(), 0, 0)) / 1000 / 60 / 60 / 24)
    const todaysTipIndex = dayOfYear % hrTips.length
    setTipIndex(todaysTipIndex)
    setCurrentTip(hrTips[todaysTipIndex])
  }, [])

  const getNextTip = () => {
    const nextIndex = (tipIndex + 1) % hrTips.length
    setTipIndex(nextIndex)
    setCurrentTip(hrTips[nextIndex])
  }

  const formatDate = () => {
    return new Date().toLocaleDateString('en-US', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    })
  }

  if (!currentTip) return null

  return (
    <Card className="w-full">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg">
              <Lightbulb className="h-5 w-5 text-white" />
            </div>
            <div>
              <CardTitle className="text-lg">Daily HR Tip</CardTitle>
              <CardDescription className="flex items-center space-x-2">
                <Calendar className="h-4 w-4" />
                <span>{formatDate()}</span>
              </CardDescription>
            </div>
          </div>
          <Button 
            variant="outline" 
            size="sm" 
            onClick={getNextTip}
            className="flex items-center space-x-1"
          >
            <RefreshCw className="h-4 w-4" />
            <span>Next Tip</span>
          </Button>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        <div className="flex items-center space-x-2">
          <Badge className={`${currentTip.color} flex items-center space-x-1`}>
            {currentTip.icon}
            <span>{currentTip.category}</span>
          </Badge>
        </div>
        
        <div>
          <h3 className="font-semibold text-gray-900 mb-2">{currentTip.title}</h3>
          <p className="text-gray-700 leading-relaxed mb-3">{currentTip.content}</p>
        </div>
        
        <div className="bg-gray-50 rounded-lg p-4 border-l-4 border-blue-500">
          <div className="flex items-start space-x-2">
            <Target className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
            <div>
              <h4 className="font-medium text-gray-900 mb-1">Action Item</h4>
              <p className="text-gray-700 text-sm">{currentTip.actionable}</p>
            </div>
          </div>
        </div>
        
        <div className="flex items-center justify-between text-sm text-gray-500 pt-2 border-t">
          <span>Tip {tipIndex + 1} of {hrTips.length}</span>
          <span>💡 Building better workplaces, one tip at a time</span>
        </div>
      </CardContent>
    </Card>
  )
}

export default DailyTips

