import { useState } from 'react'
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-orange-50">
      {/* Mobile sidebar */}
      <div className={`fixed inset-0 z-50 lg:hidden ${sidebarOpen ? 'block' : 'hidden'}`}>
        <div className="fixed inset-0 bg-gray-900/50 backdrop-blur-sm" onClick={() => setSidebarOpen(false)} />
        <div className="fixed inset-y-0 left-0 flex w-72 flex-col bg-white/95 backdrop-blur-xl border-r border-orange-200/50 shadow-2xl">
          <div className="flex h-16 items-center justify-between px-6 bg-gradient-to-r from-orange-500 to-orange-600">
            <div className="flex items-center space-x-2">
              <Sparkles className="h-6 w-6 text-white" />
              <h1 className="text-xl font-bold text-white">AnNi AI</h1>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setSidebarOpen(false)}
              className="text-white hover:bg-white/20"
            >
              <X className="h-5 w-5" />
            </Button>
          </div>
          <nav className="flex-1 space-y-2 px-4 py-6">
            {navigation.map((item) => (
              <Button
                key={item.id}
                variant="ghost"
                className={`w-full justify-start h-12 rounded-xl transition-all duration-200 ${
                  currentPage === item.id 
                    ? 'bg-gradient-to-r from-orange-100 to-orange-50 text-orange-700 shadow-lg shadow-orange-200/50 border border-orange-200' 
                    : 'hover:bg-gray-50 hover:shadow-md text-gray-700'
                }`}
                onClick={() => {
                  onPageChange(item.id)
                  setSidebarOpen(false)
                }}
              >
                <item.icon className={`mr-3 h-5 w-5 ${currentPage === item.id ? 'text-orange-600' : item.color}`} />
                <span className="font-medium">{item.name}</span>
              </Button>
            ))}
          </nav>
          <div className="border-t border-gray-200/50 p-4 bg-gradient-to-r from-gray-50 to-blue-50">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                <span className="text-white font-semibold text-sm">{user?.username?.charAt(0)?.toUpperCase()}</span>
              </div>
              <div className="flex-1">
                <p className="text-sm font-semibold text-gray-900">{user?.username}</p>
                <p className="text-xs text-gray-500">{user?.email}</p>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={onLogout}
                className="text-gray-500 hover:text-red-600 hover:bg-red-50"
              >
                <LogOut className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Desktop sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-72 lg:flex-col">
        <div className="flex flex-col flex-grow bg-white/95 backdrop-blur-xl border-r border-orange-200/50 shadow-xl">
          <div className="flex h-16 items-center px-6 bg-gradient-to-r from-orange-500 to-orange-600">
            <div className="flex items-center space-x-2">
              <Sparkles className="h-6 w-6 text-white" />
              <h1 className="text-xl font-bold text-white">AnNi AI</h1>
            </div>
          </div>
          <nav className="flex-1 space-y-2 px-4 py-6">
            {navigation.map((item) => (
              <Button
                key={item.id}
                variant="ghost"
                className={`w-full justify-start h-12 rounded-xl transition-all duration-200 ${
                  currentPage === item.id 
                    ? 'bg-gradient-to-r from-orange-100 to-orange-50 text-orange-700 shadow-lg shadow-orange-200/50 border border-orange-200' 
                    : 'hover:bg-gray-50 hover:shadow-md text-gray-700'
                }`}
                onClick={() => onPageChange(item.id)}
              >
                <item.icon className={`mr-3 h-5 w-5 ${currentPage === item.id ? 'text-orange-600' : item.color}`} />
                <span className="font-medium">{item.name}</span>
              </Button>
            ))}
          </nav>
          <div className="border-t border-gray-200/50 p-4 bg-gradient-to-r from-gray-50 to-blue-50">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                <span className="text-white font-semibold text-sm">{user?.username?.charAt(0)?.toUpperCase()}</span>
              </div>
              <div className="flex-1">
                <p className="text-sm font-semibold text-gray-900">{user?.username}</p>
                <p className="text-xs text-gray-500">{user?.email}</p>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={onLogout}
                className="text-gray-500 hover:text-red-600 hover:bg-red-50"
              >
                <LogOut className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-72">
        {/* Top bar */}
        <div className="sticky top-0 z-40 flex h-16 shrink-0 items-center gap-x-4 border-b border-orange-200/50 bg-white/95 backdrop-blur-xl px-4 shadow-lg sm:gap-x-6 sm:px-6 lg:px-8">
          <Button
            variant="ghost"
            size="sm"
            className="lg:hidden text-orange-600 hover:bg-orange-50"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu className="h-5 w-5" />
          </Button>
          
          <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
            <div className="flex flex-1"></div>
            <div className="flex items-center gap-x-4 lg:gap-x-6">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-r from-green-400 to-blue-500 rounded-full flex items-center justify-center">
                  <span className="text-white font-semibold text-xs">{user?.username?.charAt(0)?.toUpperCase()}</span>
                </div>
                <span className="text-sm font-medium text-gray-700">
                  Welcome back, <span className="text-orange-600">{user?.username}</span>
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Page content */}
        <main className="py-8">
          <div className="px-4 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}

export default Layout

