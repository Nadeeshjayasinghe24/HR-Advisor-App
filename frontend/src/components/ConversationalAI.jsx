import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { 
  MessageCircle, 
  Send, 
  Sparkles, 
  User, 
  Bot,
  Loader2,
  ThumbsUp,
  ThumbsDown,
  Copy,
  RefreshCw,
  Lightbulb,
  FileText,
  Users,
  Calendar,
  BarChart3
} from 'lucide-react';

const ConversationalAI = ({ isFullScreen = false, onClose }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'ai',
      content: "Hi! I'm AnNi AI, your intelligent HR assistant. HR made simple! I can help you with employee management, performance reviews, compliance questions, and much more. What would you like to work on today?",
      timestamp: new Date(),
      suggestions: [
        "Show me employees at retention risk",
        "Create a performance review template",
        "Generate team diversity report",
        "Help with onboarding process"
      ]
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isFullScreen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isFullScreen]);

  const handleSendMessage = async (message = inputValue) => {
    if (!message.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: message,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setIsTyping(true);

    try {
      // Simulate AI processing
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Generate AI response based on user input
      const aiResponse = await generateAIResponse(message);
      
      setIsTyping(false);
      
      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: aiResponse.content,
        timestamp: new Date(),
        suggestions: aiResponse.suggestions,
        actions: aiResponse.actions,
        data: aiResponse.data
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      setIsTyping(false);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: "I apologize, but I encountered an error. Please try again or rephrase your question.",
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const generateAIResponse = async (userInput) => {
    const input = userInput.toLowerCase();
    
    // Simulate different types of responses based on user input
    if (input.includes('retention') || input.includes('risk')) {
      return {
        content: "I've analyzed your workforce data and identified 3 employees at retention risk:\n\n• **John Smith** (Engineering) - Low engagement score, no recent promotion\n• **Sarah Johnson** (Marketing) - Poor work-life balance indicators\n• **Mike Chen** (Sales) - Below-average manager relationship score\n\nI recommend scheduling one-on-one meetings with these employees within the next week.",
        suggestions: [
          "Schedule meetings with at-risk employees",
          "Generate detailed retention report",
          "Create retention improvement plan",
          "Show department-wise retention analysis"
        ],
        actions: [
          { type: 'schedule', label: 'Schedule Meetings', icon: Calendar },
          { type: 'report', label: 'Generate Report', icon: FileText }
        ],
        data: {
          type: 'retention_analysis',
          employees: [
            { name: 'John Smith', department: 'Engineering', risk: 'high' },
            { name: 'Sarah Johnson', department: 'Marketing', risk: 'medium' },
            { name: 'Mike Chen', department: 'Sales', risk: 'medium' }
          ]
        }
      };
    }
    
    if (input.includes('performance') || input.includes('review')) {
      return {
        content: "I'll help you create performance reviews! I can generate customized templates based on:\n\n• **Role-specific competencies**\n• **Company values alignment**\n• **Goal achievement metrics**\n• **360-degree feedback integration**\n\nWhich department or specific employees would you like to create reviews for?",
        suggestions: [
          "Create review for Engineering team",
          "Generate manager review template",
          "Set up 360-degree feedback process",
          "Schedule quarterly review cycle"
        ],
        actions: [
          { type: 'template', label: 'Create Template', icon: FileText },
          { type: 'schedule', label: 'Schedule Reviews', icon: Calendar }
        ]
      };
    }
    
    if (input.includes('report') || input.includes('analytics') || input.includes('diversity')) {
      return {
        content: "I can generate comprehensive reports for you:\n\n📊 **Available Reports:**\n• Workforce demographics and diversity\n• Performance distribution analysis\n• Compensation equity review\n• Turnover and retention trends\n• Department-wise insights\n\nWhich type of report would be most helpful right now?",
        suggestions: [
          "Generate diversity report",
          "Create performance analytics",
          "Show compensation analysis",
          "Department comparison report"
        ],
        actions: [
          { type: 'report', label: 'Generate Report', icon: BarChart3 },
          { type: 'export', label: 'Export Data', icon: FileText }
        ]
      };
    }
    
    if (input.includes('onboarding') || input.includes('new hire')) {
      return {
        content: "I'll help you streamline the onboarding process! Here's what I can set up:\n\n✅ **Automated Onboarding Workflow:**\n• Welcome email sequence\n• Document collection checklist\n• Training schedule creation\n• Buddy system assignment\n• 30-60-90 day check-ins\n\nWould you like me to create an onboarding plan for a specific role or department?",
        suggestions: [
          "Create onboarding for Engineering role",
          "Set up general onboarding template",
          "Schedule new hire check-ins",
          "Generate welcome materials"
        ],
        actions: [
          { type: 'workflow', label: 'Create Workflow', icon: Users },
          { type: 'template', label: 'Generate Materials', icon: FileText }
        ]
      };
    }
    
    // Default response for general queries
    return {
      content: "I understand you're looking for help with HR tasks. I can assist you with:\n\n• **Employee Management** - Add, update, analyze employee data\n• **Performance Reviews** - Create templates, schedule reviews\n• **Compliance** - Policy guidance, legal requirements\n• **Analytics** - Generate insights and reports\n• **Workflows** - Automate HR processes\n\nWhat specific area would you like to focus on?",
      suggestions: [
        "Show me team overview",
        "Help with compliance question",
        "Create employee handbook",
        "Analyze team performance"
      ]
    };
  };

  const handleSuggestionClick = (suggestion) => {
    handleSendMessage(suggestion);
  };

  const handleActionClick = (action) => {
    // Handle different action types
    console.log('Action clicked:', action);
    // This would integrate with the appropriate system components
  };

  const copyMessage = (content) => {
    navigator.clipboard.writeText(content);
    // Show toast notification
  };

  const formatTimestamp = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={`flex flex-col ${isFullScreen ? 'h-screen' : 'h-96'} bg-white`}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b bg-gradient-to-r from-blue-50 to-indigo-50">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-blue-100 rounded-full">
            <Bot className="h-5 w-5 text-blue-600" />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900">AnNi AI</h3>
            <p className="text-sm text-gray-600">
              {isTyping ? 'Typing...' : 'HR made simple - Online and ready to help'}
            </p>
          </div>
        </div>
        {isFullScreen && onClose && (
          <Button variant="ghost" size="sm" onClick={onClose}>
            ✕
          </Button>
        )}
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] ${message.type === 'user' ? 'order-2' : 'order-1'}`}>
              
              {/* Message bubble */}
              <div className={`p-3 rounded-lg ${
                message.type === 'user' 
                  ? 'bg-blue-600 text-white' 
                  : message.isError 
                    ? 'bg-red-50 text-red-800 border border-red-200'
                    : 'bg-gray-100 text-gray-900'
              }`}>
                <div className="whitespace-pre-wrap text-sm">{message.content}</div>
                
                {/* Actions */}
                {message.actions && (
                  <div className="flex flex-wrap gap-2 mt-3">
                    {message.actions.map((action, index) => (
                      <Button
                        key={index}
                        variant="outline"
                        size="sm"
                        onClick={() => handleActionClick(action)}
                        className="text-xs"
                      >
                        <action.icon className="h-3 w-3 mr-1" />
                        {action.label}
                      </Button>
                    ))}
                  </div>
                )}
              </div>

              {/* Suggestions */}
              {message.suggestions && (
                <div className="flex flex-wrap gap-2 mt-2">
                  {message.suggestions.map((suggestion, index) => (
                    <Button
                      key={index}
                      variant="ghost"
                      size="sm"
                      onClick={() => handleSuggestionClick(suggestion)}
                      className="text-xs text-blue-600 hover:text-blue-800 hover:bg-blue-50"
                    >
                      {suggestion}
                    </Button>
                  ))}
                </div>
              )}

              {/* Message metadata */}
              <div className={`flex items-center space-x-2 mt-1 ${
                message.type === 'user' ? 'justify-end' : 'justify-start'
              }`}>
                <span className="text-xs text-gray-500">
                  {formatTimestamp(message.timestamp)}
                </span>
                {message.type === 'ai' && !message.isError && (
                  <div className="flex items-center space-x-1">
                    <Button variant="ghost" size="sm" onClick={() => copyMessage(message.content)}>
                      <Copy className="h-3 w-3" />
                    </Button>
                    <Button variant="ghost" size="sm">
                      <ThumbsUp className="h-3 w-3" />
                    </Button>
                    <Button variant="ghost" size="sm">
                      <ThumbsDown className="h-3 w-3" />
                    </Button>
                  </div>
                )}
              </div>
            </div>

            {/* Avatar */}
            <div className={`flex-shrink-0 ${message.type === 'user' ? 'order-1 ml-2' : 'order-2 mr-2'}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                message.type === 'user' 
                  ? 'bg-blue-600' 
                  : 'bg-gradient-to-r from-purple-500 to-blue-500'
              }`}>
                {message.type === 'user' ? (
                  <User className="h-4 w-4 text-white" />
                ) : (
                  <Bot className="h-4 w-4 text-white" />
                )}
              </div>
            </div>
          </div>
        ))}

        {/* Typing indicator */}
        {isTyping && (
          <div className="flex justify-start">
            <div className="flex items-center space-x-2 bg-gray-100 p-3 rounded-lg">
              <Loader2 className="h-4 w-4 animate-spin text-gray-500" />
              <span className="text-sm text-gray-500">AI is thinking...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t bg-gray-50">
        <form onSubmit={(e) => { e.preventDefault(); handleSendMessage(); }} className="flex space-x-2">
          <Input
            ref={inputRef}
            placeholder="Ask me anything about HR... (e.g., 'Show me retention risks')"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            disabled={isLoading}
            className="flex-1"
          />
          <Button type="submit" disabled={isLoading || !inputValue.trim()}>
            {isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </Button>
        </form>

        {/* Quick actions */}
        <div className="flex flex-wrap gap-2 mt-2">
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={() => handleSendMessage("Show me today's priorities")}
            className="text-xs"
          >
            <Lightbulb className="h-3 w-3 mr-1" />
            Today's Priorities
          </Button>
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={() => handleSendMessage("Generate team report")}
            className="text-xs"
          >
            <BarChart3 className="h-3 w-3 mr-1" />
            Team Report
          </Button>
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={() => handleSendMessage("Help with compliance")}
            className="text-xs"
          >
            <FileText className="h-3 w-3 mr-1" />
            Compliance Help
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ConversationalAI;

