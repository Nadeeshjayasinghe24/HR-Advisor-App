import { useState, useRef, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { 
  Send, 
  Bot, 
  User, 
  Loader2, 
  FileText, 
  Workflow
} from 'lucide-react'
import '../App.css'

const HRAdvisor = ({ token }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: "Hello! I'm your AI HR Advisor. I can help you with country-specific labor laws, HR templates, workflows, and best practices. What would you like to know?",
      timestamp: new Date().toISOString()
    }
  ])
  const [inputValue, setInputValue] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const messagesEndRef = useRef(null)

  // Quick questions for easy access
  const quickQuestions = [
    "What is the maternity leave policy in Singapore?",
    "How many vacation days are required by law in the US?",
    "What are the overtime regulations in the UK?",
    "How to handle employee termination properly?",
    "What documents are needed for new employee onboarding?",
    "How to conduct performance reviews effectively?",
    "What are the requirements for workplace safety training?",
    "How to handle employee complaints and grievances?"
  ]

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  const handleSendMessage = async (message = inputValue) => {
    if (!message.trim()) return

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: message,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setLoading(true)
    setError('')

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'https://hr-advisor-app.onrender.com'}/api/hr_advisor/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          query: message
        }),
      })

      const data = await response.json()

      if (response.ok) {
        const botMessage = {
          id: Date.now() + 1,
          type: 'bot',
          content: data.response,
          timestamp: new Date().toISOString(),
          country: data.country_context,
          coinsConsumed: data.coins_consumed,
          resources: data.resources || []
        }
        setMessages(prev => [...prev, botMessage])
      } else {
        setError(data.error || 'Failed to get response')
      }
    } catch (err) {
      setError('Network error. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateTemplate = async (templateType) => {
    setLoading(true)
    setError('')

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: `Generate a ${templateType} template`,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'https://hr-advisor-app.onrender.com'}/api/hr_advisor/template`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          type: templateType,
          details: {}
        }),
      })

      const data = await response.json()

      if (response.ok) {
        const botMessage = {
          id: Date.now() + 1,
          type: 'bot',
          content: data.template_content,
          timestamp: new Date().toISOString(),
          country: data.country_context,
          coinsConsumed: data.coins_consumed,
          templateType: data.template_type
        }
        setMessages(prev => [...prev, botMessage])
      } else {
        setError(data.error || 'Failed to generate template')
      }
    } catch (err) {
      setError('Network error. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="h-full flex flex-col">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">HR Advisor</h1>
      </div>

      {error && (
        <Alert variant="destructive" className="mb-4">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <div className="flex-1 flex gap-6">
        {/* Chat Area */}
        <div className="flex-1 flex flex-col">
          <Card className="flex-1 flex flex-col">
            <CardHeader>
              <CardTitle className="text-lg">Chat with HR Advisor</CardTitle>
            </CardHeader>
            <CardContent className="flex-1 flex flex-col">
              {/* Messages */}
              <div className="flex-1 overflow-y-auto space-y-4 mb-4 max-h-96">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                        message.type === 'user'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-900'
                      }`}
                    >
                      <div className="flex items-start space-x-2">
                        {message.type === 'bot' && <Bot className="h-4 w-4 mt-1 flex-shrink-0" />}
                        {message.type === 'user' && <User className="h-4 w-4 mt-1 flex-shrink-0" />}
                        <div className="flex-1">
                          <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                          <div className="flex items-center justify-between mt-2">
                            <span className="text-xs opacity-75">
                              {formatTimestamp(message.timestamp)}
                            </span>
                            {message.country && (
                              <Badge variant="secondary" className="text-xs">
                                {message.country}
                              </Badge>
                            )}
                          </div>
                          {message.coinsConsumed && (
                            <p className="text-xs opacity-75 mt-1">
                              Coins used: {message.coinsConsumed}
                            </p>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 text-gray-900 max-w-xs lg:max-w-md px-4 py-2 rounded-lg">
                      <div className="flex items-center space-x-2">
                        <Bot className="h-4 w-4" />
                        <Loader2 className="h-4 w-4 animate-spin" />
                        <span className="text-sm">Thinking...</span>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Input */}
              <div className="flex space-x-2">
                <Input
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Ask me anything about HR..."
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  disabled={loading}
                />
                <Button 
                  onClick={() => handleSendMessage()} 
                  disabled={loading || !inputValue.trim()}
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="w-80 space-y-6">
          {/* Quick Questions */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Quick Questions</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {quickQuestions.map((question, index) => (
                  <Button
                    key={index}
                    variant="outline"
                    size="sm"
                    className="w-full text-left justify-start h-auto py-2 px-3"
                    onClick={() => handleSendMessage(question)}
                    disabled={loading}
                  >
                    <span className="text-xs">{question}</span>
                  </Button>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Template Generator */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center">
                <FileText className="mr-2 h-5 w-5" />
                Generate Templates
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {[
                  'hiring_communication',
                  'performance_review',
                  'onboarding_checklist',
                  'termination_letter',
                  'policy_document'
                ].map((template) => (
                  <Button
                    key={template}
                    variant="outline"
                    size="sm"
                    className="w-full justify-start"
                    onClick={() => handleGenerateTemplate(template)}
                    disabled={loading}
                  >
                    <FileText className="mr-2 h-3 w-3" />
                    {template.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </Button>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Workflow Generator */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center">
                <Workflow className="mr-2 h-5 w-5" />
                Create Workflows
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {[
                  'onboarding',
                  'performance_review_process',
                  'leave_approval',
                  'disciplinary_action',
                  'exit_process'
                ].map((workflow) => (
                  <Button
                    key={workflow}
                    variant="outline"
                    size="sm"
                    className="w-full justify-start"
                    onClick={() => handleSendMessage(`Create a ${workflow.replace('_', ' ')} workflow`)}
                    disabled={loading}
                  >
                    <Workflow className="mr-2 h-3 w-3" />
                    {workflow.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </Button>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default HRAdvisor

