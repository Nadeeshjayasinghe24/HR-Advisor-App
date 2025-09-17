import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { 
  Users, 
  MessageSquare, 
  Settings, 
  LogOut, 
  Menu,
  X,
  Home,
  FileText,
  CreditCard,
  Sparkles
} from 'lucide-react'
import { getWelcomeMessage, getUserInitials, extractFirstName } from '../utils/nameUtils'
import '../App.css'

const Layout = ({ children, currentPage, onPageChange, user, onLogout }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const navigation = [
    { name: 'Dashboard', icon: Home, id: 'dashboard', color: 'text-orange-600' },
    { name: 'Employees', icon: Users, id: 'employees', color: 'text-blue-600' },
    { name: 'HR Advisor', icon: MessageSquare, id: 'hr-advisor', color: 'text-green-600' },
    { name: 'History', icon: FileText, id: 'history', color: 'text-purple-600' },
    { name: 'Subscription', icon: CreditCard, id: 'subscription', color: 'text-pink-600' },
    { name: 'Settings', icon: Settings, id: 'settings', color: 'text-gray-600' },
  ]

  const firstName = extractFirstName(user)
  const welcomeMessage = getWelcomeMessage(firstName)

  return (
    <div className="min-h-screen bg-background">
      {/* Desktop Sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col">
        <div className="flex flex-col flex-grow bg-white border-r border-border overflow-y-auto">
          {/* Logo */}
          <div className="flex items-center justify-center px-6 py-6 border-b border-border">
            <div className="anni-logo">
              <img 
                src="/assets/logo-icon.png" 
                alt="AnNi Logo" 
                className="h-10 w-10"
              />
              <img 
                src="/assets/logo-text.png" 
                alt="AnNi AI" 
                className="h-8"
              />
            </div>
          </div>
          
          {/* User Welcome */}
          <div className="px-6 py-4 border-b border-border">
            <div className="anni-welcome text-lg font-semibold">
              {welcomeMessage}
            </div>
            <div className="text-sm text-muted-foreground mt-1">
              {user?.email}
            </div>
          </div>
          
          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-2">
            {navigation.map((item) => (
              <button
                key={item.id}
                onClick={() => onPageChange(item.id)}
                className={`anni-nav-item w-full ${currentPage === item.id ? 'active' : ''}`}
              >
                <item.icon className="h-5 w-5 mr-3" />
                {item.name}
              </button>
            ))}
          </nav>
          
          {/* Logout */}
          <div className="px-4 py-4 border-t border-border">
            <button
              onClick={onLogout}
              className="anni-nav-item w-full text-destructive hover:bg-destructive/10"
            >
              <LogOut className="h-5 w-5 mr-3" />
              Sign out
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Header */}
      <div className="lg:hidden">
        <div className="flex items-center justify-between px-4 py-3 bg-white border-b border-border">
          <div className="anni-logo">
            <img 
              src="/assets/logo-icon.png" 
              alt="AnNi Logo" 
              className="h-8 w-8"
            />
            <img 
              src="/assets/logo-text.png" 
              alt="AnNi AI" 
              className="h-6"
            />
          </div>
          <button
            onClick={() => setSidebarOpen(true)}
            className="p-2 rounded-md text-foreground hover:bg-muted"
          >
            <Menu className="h-6 w-6" />
          </button>
        </div>
      </div>

      {/* Mobile Sidebar */}
      {sidebarOpen && (
        <div className="lg:hidden">
          <div className="fixed inset-0 z-50 flex">
            <div className="fixed inset-0 bg-black/50" onClick={() => setSidebarOpen(false)} />
            <div className="relative flex flex-col w-64 bg-white border-r border-border">
              {/* Mobile Header */}
              <div className="flex items-center justify-between px-6 py-4 border-b border-border">
                <div className="anni-logo">
                  <img 
                    src="/assets/logo-icon.png" 
                    alt="AnNi Logo" 
                    className="h-8 w-8"
                  />
                  <img 
                    src="/assets/logo-text.png" 
                    alt="AnNi AI" 
                    className="h-6"
                  />
                </div>
                <button
                  onClick={() => setSidebarOpen(false)}
                  className="p-2 rounded-md text-foreground hover:bg-muted"
                >
                  <X className="h-6 w-6" />
                </button>
              </div>
              
              {/* User Welcome */}
              <div className="px-6 py-4 border-b border-border">
                <div className="anni-welcome text-lg font-semibold">
                  {welcomeMessage}
                </div>
                <div className="text-sm text-muted-foreground mt-1">
                  {user?.email}
                </div>
              </div>
              
              {/* Navigation */}
              <nav className="flex-1 px-4 py-6 space-y-2">
                {navigation.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => {
                      onPageChange(item.id)
                      setSidebarOpen(false)
                    }}
                    className={`anni-nav-item w-full ${currentPage === item.id ? 'active' : ''}`}
                  >
                    <item.icon className="h-5 w-5 mr-3" />
                    {item.name}
                  </button>
                ))}
              </nav>
              
              {/* Logout */}
              <div className="px-4 py-4 border-t border-border">
                <button
                  onClick={() => {
                    onLogout()
                    setSidebarOpen(false)
                  }}
                  className="anni-nav-item w-full text-destructive hover:bg-destructive/10"
                >
                  <LogOut className="h-5 w-5 mr-3" />
                  Sign out
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="lg:pl-64">
        <main className="py-6">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}

export default Layout

