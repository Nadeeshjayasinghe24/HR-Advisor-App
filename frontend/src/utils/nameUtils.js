// Creative name extraction and welcome message utilities

/**
 * Extracts the first name from various username formats
 * Handles: "John Doe", "john.doe", "john_doe", "johnDoe", "john", etc.
 */
export const extractFirstName = (username) => {
  if (!username) return 'Friend'
  
  // Remove common email domains if present
  const cleanUsername = username.split('@')[0]
  
  // Handle different separators and formats
  let firstName = cleanUsername
    .split(/[\s._-]+/)[0] // Split by space, dot, underscore, or dash
    .replace(/([a-z])([A-Z])/g, '$1 $2') // Handle camelCase
    .split(' ')[0] // Take first word
    .toLowerCase()
  
  // Capitalize first letter
  firstName = firstName.charAt(0).toUpperCase() + firstName.slice(1)
  
  // Handle edge cases
  if (firstName.length < 2) return 'Friend'
  if (firstName.length > 15) return firstName.substring(0, 15) // Truncate very long names
  
  return firstName
}

/**
 * Gets a creative welcome message based on time of day and user's first name
 */
export const getWelcomeMessage = (username) => {
  const firstName = extractFirstName(username)
  const hour = new Date().getHours()
  
  const timeBasedGreetings = {
    morning: [
      `Good morning, ${firstName}! ☀️`,
      `Rise and shine, ${firstName}! 🌅`,
      `Morning, ${firstName}! Ready to conquer the day? 💪`,
      `Hello ${firstName}! Hope you're having a great morning! 🌞`
    ],
    afternoon: [
      `Good afternoon, ${firstName}! 🌤️`,
      `Hey ${firstName}! How's your day going? 😊`,
      `Afternoon, ${firstName}! Keep up the great work! 🚀`,
      `Hi ${firstName}! Hope your day is productive! ⭐`
    ],
    evening: [
      `Good evening, ${firstName}! 🌆`,
      `Evening, ${firstName}! Wrapping up the day? 🌙`,
      `Hey ${firstName}! Hope you had a wonderful day! ✨`,
      `Hi ${firstName}! Time to wind down? 🌃`
    ],
    night: [
      `Working late, ${firstName}? 🌙`,
      `Good evening, ${firstName}! Burning the midnight oil? 💡`,
      `Hey ${firstName}! Don't forget to rest! 😴`,
      `Hi ${firstName}! Hope you're not working too hard! 🌟`
    ]
  }
  
  let timeOfDay
  if (hour >= 5 && hour < 12) timeOfDay = 'morning'
  else if (hour >= 12 && hour < 17) timeOfDay = 'afternoon'
  else if (hour >= 17 && hour < 21) timeOfDay = 'evening'
  else timeOfDay = 'night'
  
  const greetings = timeBasedGreetings[timeOfDay]
  return greetings[Math.floor(Math.random() * greetings.length)]
}

/**
 * Gets a motivational message with the user's first name
 */
export const getMotivationalMessage = (username) => {
  const firstName = extractFirstName(username)
  
  const messages = [
    `You're doing great, ${firstName}! 🌟`,
    `Keep it up, ${firstName}! 💪`,
    `${firstName}, you're making a difference! ✨`,
    `Awesome work, ${firstName}! 🚀`,
    `${firstName}, you're on fire today! 🔥`,
    `Way to go, ${firstName}! 🎉`,
    `${firstName}, you're crushing it! 💎`,
    `Fantastic job, ${firstName}! 🌈`,
    `${firstName}, you're a star! ⭐`,
    `Keep shining, ${firstName}! ✨`
  ]
  
  return messages[Math.floor(Math.random() * messages.length)]
}

/**
 * Gets a context-specific welcome message
 */
export const getContextualWelcome = (username, context = 'general') => {
  const firstName = extractFirstName(username)
  
  const contextMessages = {
    dashboard: [
      `Welcome back, ${firstName}! 🏠`,
      `Hey ${firstName}! Ready to dive in? 🌊`,
      `${firstName}, your dashboard awaits! 📊`,
      `Welcome home, ${firstName}! 🏡`
    ],
    employees: [
      `Managing your team, ${firstName}? 👥`,
      `${firstName}, let's check on your employees! 👨‍💼`,
      `Time for some people management, ${firstName}! 🤝`,
      `${firstName}, your team is lucky to have you! 💼`
    ],
    hr_advisor: [
      `Need some HR wisdom, ${firstName}? 🧠`,
      `${firstName}, I'm here to help with HR questions! 💡`,
      `Let's solve some HR challenges, ${firstName}! 🎯`,
      `${firstName}, ready for some expert HR advice? 📚`
    ],
    subscription: [
      `Checking your plan, ${firstName}? 💳`,
      `${firstName}, let's review your subscription! 📋`,
      `Time to manage your account, ${firstName}! ⚙️`,
      `${firstName}, your subscription details are here! 📊`
    ],
    general: [
      `Hello ${firstName}! 👋`,
      `Hey there, ${firstName}! 😊`,
      `Welcome, ${firstName}! 🎉`,
      `Hi ${firstName}! Great to see you! ✨`
    ]
  }
  
  const messages = contextMessages[context] || contextMessages.general
  return messages[Math.floor(Math.random() * messages.length)]
}

/**
 * Gets the user's initials for avatar display
 */
export const getUserInitials = (username) => {
  if (!username) return 'U'
  
  const firstName = extractFirstName(username)
  const parts = username.split(/[\s._-]+/)
  
  if (parts.length >= 2) {
    // First name + Last name initials
    const lastName = parts[1].charAt(0).toUpperCase()
    return firstName.charAt(0) + lastName
  }
  
  // Just first name initial
  return firstName.charAt(0)
}

/**
 * Gets a personalized page title
 */
export const getPageTitle = (username, pageName) => {
  const firstName = extractFirstName(username)
  
  const pageTitles = {
    dashboard: `${firstName}'s Dashboard`,
    employees: `${firstName}'s Team`,
    'hr-advisor': `HR Advisor for ${firstName}`,
    history: `${firstName}'s History`,
    subscription: `${firstName}'s Subscription`,
    settings: `${firstName}'s Settings`
  }
  
  return pageTitles[pageName] || `${firstName}'s ${pageName}`
}

