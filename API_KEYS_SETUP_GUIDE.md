# API Keys Setup Guide for Multi-LLM Orchestration

## Overview

To fully activate the Multi-LLM Orchestration system, you'll need API keys from the LLM providers. Here's a complete guide on how to get them, what they cost, and how to set them up.

## 🆓 **Free Tiers Available!**

**Good News**: All major providers offer free tiers or credits to get started. You can test the system without any upfront payment!

---

## 1. OpenAI API Key

### **How to Get It:**
1. **Go to**: https://platform.openai.com/
2. **Sign up** for an OpenAI account (free)
3. **Navigate to**: API Keys section
4. **Click**: "Create new secret key"
5. **Copy** the key (starts with `sk-`)

### **Costs:**
- **Free Tier**: $5 in free credits for new accounts
- **GPT-3.5-turbo**: $0.0015 per 1K tokens (~750 words)
- **GPT-4**: $0.03 per 1K tokens (~750 words)
- **Typical HR Query**: ~$0.01-0.05 per response

### **Monthly Estimate for HR Advisor:**
- **Light Usage** (100 queries/month): $1-5
- **Medium Usage** (500 queries/month): $5-25
- **Heavy Usage** (2000 queries/month): $20-100

---

## 2. Google AI API Key (Gemini)

### **How to Get It:**
1. **Go to**: https://aistudio.google.com/
2. **Sign in** with Google account
3. **Click**: "Get API Key"
4. **Create** new project or select existing
5. **Generate** API key
6. **Copy** the key

### **Costs:**
- **Free Tier**: 15 requests per minute, 1,500 requests per day
- **Gemini Pro**: $0.0005 per 1K tokens (very affordable!)
- **Gemini Flash**: $0.00025 per 1K tokens (even cheaper!)

### **Monthly Estimate:**
- **Light Usage**: FREE (within limits)
- **Medium Usage**: $1-3
- **Heavy Usage**: $5-15

---

## 3. Anthropic API Key (Claude)

### **How to Get It:**
1. **Go to**: https://console.anthropic.com/
2. **Sign up** for Anthropic account
3. **Navigate to**: API Keys
4. **Create** new key
5. **Copy** the key (starts with `sk-ant-`)

### **Costs:**
- **Free Tier**: $5 in free credits for new accounts
- **Claude-3 Haiku**: $0.00025 per 1K tokens (cheapest)
- **Claude-3 Sonnet**: $0.003 per 1K tokens
- **Claude-3 Opus**: $0.015 per 1K tokens

### **Monthly Estimate:**
- **Light Usage**: $1-3
- **Medium Usage**: $3-10
- **Heavy Usage**: $10-30

---

## 💡 **Smart Strategy: Start Free!**

### **Phase 1: Free Testing (Recommended)**
1. **Start with just OpenAI** (use $5 free credits)
2. **Test the system** with real HR queries
3. **Monitor usage** and costs
4. **Add other providers** as needed

### **Phase 2: Gradual Expansion**
1. **Add Google Gemini** (free tier is generous)
2. **Add Anthropic Claude** when ready for premium features
3. **Monitor which providers work best** for your use cases

---

## 🔧 **How to Add API Keys to Your System**

### **Option 1: Environment Variables (Recommended for Production)**

1. **In your hosting platform** (Render), go to Environment Variables
2. **Add these variables**:
   ```
   OPENAI_API_KEY=sk-your-openai-key-here
   GOOGLE_API_KEY=your-google-key-here
   ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
   ```

### **Option 2: Local Testing**

1. **Create** `.env` file in your backend folder:
   ```bash
   OPENAI_API_KEY=sk-your-openai-key-here
   GOOGLE_API_KEY=your-google-key-here
   ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
   ```

2. **Never commit** this file to GitHub (already in .gitignore)

---

## 📊 **Cost Optimization Tips**

### **1. Start Small**
- Begin with **OpenAI only** using free credits
- **Monitor usage** patterns
- **Scale up** based on actual needs

### **2. Use Cheaper Models First**
- **Gemini Flash** for speed and low cost
- **Claude Haiku** for balanced performance
- **GPT-3.5** instead of GPT-4 for basic queries

### **3. Smart Orchestration**
- System automatically **selects best provider** based on query type
- **Fallback mechanisms** prevent unnecessary API calls
- **Caching** reduces duplicate requests

### **4. Monitor and Control**
- Set **usage alerts** in provider dashboards
- **Monitor costs** weekly
- **Adjust provider priorities** based on performance/cost

---

## 🎯 **Recommended Starting Approach**

### **Week 1: OpenAI Only**
```bash
# Add only this to start
OPENAI_API_KEY=sk-your-openai-key-here
```
- **Cost**: $0 (using free credits)
- **Capability**: Full HR advisor functionality
- **Goal**: Test system and understand usage patterns

### **Week 2: Add Google Gemini**
```bash
OPENAI_API_KEY=sk-your-openai-key-here
GOOGLE_API_KEY=your-google-key-here
```
- **Cost**: Still mostly free
- **Capability**: Multi-LLM comparison and validation
- **Goal**: See quality improvements from multiple providers

### **Week 3+: Full Orchestration**
```bash
OPENAI_API_KEY=sk-your-openai-key-here
GOOGLE_API_KEY=your-google-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
```
- **Cost**: $5-20/month for typical usage
- **Capability**: Full enterprise-grade AI orchestration
- **Goal**: Maximum accuracy and reliability

---

## 🔒 **Security Best Practices**

### **API Key Security:**
1. **Never share** API keys publicly
2. **Use environment variables** (not hardcoded)
3. **Rotate keys** regularly
4. **Monitor usage** for unusual activity
5. **Set spending limits** in provider dashboards

### **Usage Monitoring:**
1. **Check dashboards** weekly
2. **Set up alerts** for high usage
3. **Review costs** monthly
4. **Optimize** based on performance data

---

## 🚀 **System Behavior with Different Configurations**

### **No API Keys:**
- ✅ System works with **fallback responses**
- ✅ Basic HR guidance provided
- ❌ No real-time AI processing
- ❌ No source integration

### **OpenAI Only:**
- ✅ **Full AI-powered responses**
- ✅ High-quality HR advice
- ❌ No multi-LLM validation
- ❌ Single point of failure

### **Multiple Providers:**
- ✅ **Multi-LLM orchestration**
- ✅ **Response validation and voting**
- ✅ **Higher accuracy and reliability**
- ✅ **Redundancy and fallbacks**

---

## 📞 **Support and Troubleshooting**

### **Common Issues:**
1. **"Invalid API Key"**: Check key format and permissions
2. **"Rate Limit Exceeded"**: Wait or upgrade plan
3. **"Insufficient Credits"**: Add payment method or wait for reset

### **Testing Your Setup:**
1. **Add one API key** at a time
2. **Test with simple HR query**
3. **Check response metadata** for provider used
4. **Monitor costs** in provider dashboard

---

## 💰 **Total Cost Summary**

### **Monthly Estimates:**

| Usage Level | OpenAI | Google | Anthropic | **Total** |
|-------------|--------|--------|-----------|-----------|
| **Free Tier** | $0 | $0 | $0 | **$0** |
| **Light (100 queries)** | $1-5 | $0-1 | $1-3 | **$2-9** |
| **Medium (500 queries)** | $5-25 | $1-3 | $3-10 | **$9-38** |
| **Heavy (2000 queries)** | $20-100 | $5-15 | $10-30 | **$35-145** |

### **ROI Consideration:**
- **Enterprise HR consulting**: $200-500/hour
- **AI HR Advisor**: $10-50/month
- **Cost savings**: 90-99% compared to human consultants
- **24/7 availability**: Priceless for global operations

---

## 🎯 **Recommendation**

**Start with OpenAI's free $5 credits** to test the system. This will give you 100-500 high-quality HR responses to evaluate the system's value. Once you see the benefits, gradually add other providers for enhanced accuracy and reliability.

The Multi-LLM orchestration system is designed to provide enterprise-grade HR advisory services at a fraction of traditional consulting costs!

