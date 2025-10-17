import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import {
  Home,
  Users,
  MessageSquare,
  FileText,
  Settings,
  LogOut,
  Menu,
  X
} from 'lucide-react'

const Layout = ({ children, onLogout, user }) => {
  const location = useLocation()
  const [isMobileMenuOpen, setIsMobileMenuMenuOpen] = useState(false)

  const navigation = [
    { name: 'Dashboard', href: '/', icon: Home },
    { name: 'Employees', href: '/employees', icon: Users },
    { name: 'HR Advisor', href: '/hr-advisor', icon: MessageSquare },
    { name: 'Reports', href: '/reports', icon: FileText },
    { name: 'Settings', href: '/settings', icon: Settings },
  ]

  const isActive = (path) => {
    if (path === '/') {
      return location.pathname === '/'
    }
    return location.pathname.startsWith(path)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Desktop Sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:z-50 lg:flex lg:w-72 lg:flex-col">
        <div className="flex grow flex-col gap-y-5 overflow-y-auto bg-white px-6 pb-4 shadow-sm">
          <div className="flex h-16 shrink-0 items-center">
            <h1 className="text-2xl font-bold text-gray-900">AnNi AI</h1>
            <p className="ml-2 text-sm text-gray-500">HR made simple</p>
          </div>
          <nav className="flex flex-1 flex-col">
            <ul role="list" className="flex flex-1 flex-col gap-y-7">
              <li>
                <ul role="list" className="-mx-2 space-y-1">
                  {navigation.map((item) => (
                    <li key={item.name}>
                      <Link
                        to={item.href}
                        className={`${
                          isActive(item.href)
                            ? 'bg-gray-50 text-blue-600'
                            : 'text-gray-700 hover:text-blue-600 hover:bg-gray-50'
                        } group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold transition-colors`}
                      >
                        <item.icon
                          className={`${
                            isActive(item.href) ? 'text-blue-600' : 'text-gray-400 group-hover:text-blue-600'
                          } h-6 w-6 shrink-0 transition-colors`}
                          aria-hidden="true"
                        />
                        {item.name}
                      </Link>
                    </li>
                  ))}
                </ul>
              </li>
              <li className="mt-auto">
                <div className="flex items-center gap-x-4 px-2 py-3 text-sm font-semibold leading-6 text-gray-900">
                  <div className="h-8 w-8 rounded-full bg-gray-50 flex items-center justify-center">
                    <span className="text-sm font-medium text-gray-600">
                      {user?.first_name?.charAt(0) || user?.email?.charAt(0) || 'U'}
                    </span>
                  </div>
                  <span className="sr-only">Your profile</span>
                  <span aria-hidden="true">{user?.first_name || user?.email}</span>
                </div>
                <button
                  onClick={onLogout}
                  className="group -mx-2 flex w-full gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold text-gray-700 hover:bg-gray-50 hover:text-red-600 transition-colors"
                >
                  <LogOut
                    className="h-6 w-6 shrink-0 text-gray-400 group-hover:text-red-600 transition-colors"
                    aria-hidden="true"
                  />
                  Sign out
                </button>
              </li>
            </ul>
          </nav>
        </div>
      </div>

      {/* Mobile menu */}
      <div className="lg:hidden">
        <div className="sticky top-0 z-40 flex h-16 shrink-0 items-center gap-x-4 border-b border-gray-200 bg-white px-4 shadow-sm sm:gap-x-6 sm:px-6 lg:px-8">
          <button
            type="button"
            className="-m-2.5 p-2.5 text-gray-700 lg:hidden"
            onClick={() => setIsMobileMenuOpen(true)}
          >
            <span className="sr-only">Open sidebar</span>
            <Menu className="h-6 w-6" aria-hidden="true" />
          </button>

          <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">AnNi AI</h1>
            </div>
          </div>
        </div>

        {/* Mobile sidebar */}
        {isMobileMenuOpen && (
          <div className="relative z-50 lg:hidden">
            <div className="fixed inset-0 bg-gray-900/80" onClick={() => setIsMobileMenuOpen(false)} />
            <div className="fixed inset-0 flex">
              <div className="relative mr-16 flex w-full max-w-xs flex-1">
                <div className="absolute left-full top-0 flex w-16 justify-center pt-5">
                  <button
                    type="button"
                    className="-m-2.5 p-2.5"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    <span className="sr-only">Close sidebar</span>
                    <X className="h-6 w-6 text-white" aria-hidden="true" />
                  </button>
                </div>

                <div className="flex grow flex-col gap-y-5 overflow-y-auto bg-white px-6 pb-4">
                  <div className="flex h-16 shrink-0 items-center">
                    <h1 className="text-2xl font-bold text-gray-900">AnNi AI</h1>
                  </div>
                  <nav className="flex flex-1 flex-col">
                    <ul role="list" className="flex flex-1 flex-col gap-y-7">
                      <li>
                        <ul role="list" className="-mx-2 space-y-1">
                          {navigation.map((item) => (
                            <li key={item.name}>
                              <Link
                                to={item.href}
                                onClick={() => setIsMobileMenuOpen(false)}
                                className={`${
                                  isActive(item.href)
                                    ? 'bg-gray-50 text-blue-600'
                                    : 'text-gray-700 hover:text-blue-600 hover:bg-gray-50'
                                } group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold transition-colors`}
                              >
                                <item.icon
                                  className={`${
                                    isActive(item.href) ? 'text-blue-600' : 'text-gray-400 group-hover:text-blue-600'
                                  } h-6 w-6 shrink-0 transition-colors`}
                                  aria-hidden="true"
                                />
                                {item.name}
                              </Link>
                            </li>
                          ))}
                        </ul>
                      </li>
                      <li className="mt-auto">
                        <button
                          onClick={onLogout}
                          className="group -mx-2 flex w-full gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold text-gray-700 hover:bg-gray-50 hover:text-red-600 transition-colors"
                        >
                          <LogOut
                            className="h-6 w-6 shrink-0 text-gray-400 group-hover:text-red-600 transition-colors"
                            aria-hidden="true"
                          />
                          Sign out
                        </button>
                      </li>
                    </ul>
                  </nav>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Main content */}
      <div className="lg:pl-72">
        <main className="py-10">
          <div className="px-4 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}

export default Layout

