# 🤖 GPT-Powered Chatbot Setup Guide

## Overview

Your dashboard now supports **TWO chatbot modes**:

1. **Rule-Based (Fast, Free)** - Pattern matching, no API key needed
2. **GPT-Powered (Smart, Requires API Key)** - OpenAI GPT for natural language understanding

## 🚀 Quick Start

### Step 1: Install OpenAI Package

```bash
pip install openai
```

### Step 2: Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the API key (starts with `sk-...`)
5. **Important**: Save it securely - you won't see it again!

### Step 3: Launch Dashboard with GPT Support

```bash
python -m streamlit run dashboard_with_gpt.py
```

### Step 4: Configure in Dashboard

1. In the left sidebar, check **"Enable Chatbot"**
2. Select **"GPT-Powered (Smart, Requires API Key)"**
3. Enter your OpenAI API key in the password field
4. You'll see "✓ API Key configured" when successful
5. Start asking questions!

---

## 💡 Chatbot Comparison

### Rule-Based Mode (Free)
✅ **Pros:**
- Completely free
- Fast responses
- Works offline
- No API key needed
- Deterministic answers

❌ **Cons:**
- Limited to pre-defined question patterns
- Less flexible
- Can't understand complex phrasing
- Must match keywords

### GPT-Powered Mode (Paid but Smart)
✅ **Pros:**
- Understands natural language
- Very flexible - ask in any way
- Can handle complex questions
- Contextual understanding
- Better at follow-up questions

❌ **Cons:**
- Requires OpenAI API key
- Costs money (but very cheap)
- Needs internet connection
- Slightly slower responses

---

## 💰 Cost Breakdown

The dashboard uses **GPT-4o-mini**, which is extremely cost-effective:

| Metric | Cost |
|--------|------|
| Input | $0.150 per 1M tokens |
| Output | $0.600 per 1M tokens |
| Typical Question | ~$0.001 (0.1 cents) |
| 100 Questions | ~$0.10 |
| 1000 Questions | ~$1.00 |

**Translation**: You can ask hundreds of questions for just pennies! 💰

---

## 📝 Example Questions

### Questions GPT Handles Better

**Complex/Conversational:**
```
"Can you explain why our clothing sales are higher than technology?"
"What insights can you give me about customer behavior?"
"If I want to increase revenue, which category should I focus on?"
"Compare Q1 vs Q2 performance and tell me what changed"
"Why might Saturday sales be higher than weekdays?"
```

**Follow-up Questions:**
```
You: "What's our top category?"
GPT: "Clothing is your top category..."

You: "Why do you think that is?"
GPT: "Clothing likely performs well because..."

You: "What about the second best?"
GPT: "Technology is your second-best category..."
```

### Questions Rule-Based Handles Well

**Direct/Factual:**
```
"What is my total revenue?"
"Which mall performs best?"
"What are customer demographics?"
"Which day has most sales?"
"Tell me about Technology category"
```

---

## 🔒 Security & Privacy

### API Key Storage
- **Never hardcode** your API key in files
- **Never commit** API keys to git
- The dashboard stores it temporarily in session only
- Key is cleared when you close the browser

### Best Practices
1. Use separate API keys for different projects
2. Set spending limits in OpenAI dashboard
3. Rotate keys periodically
4. Monitor usage at https://platform.openai.com/usage

### Data Privacy
- Your sales data is sent to OpenAI with each question
- Only summary statistics are shared (not raw transactions)
- OpenAI's data usage policy applies
- If concerned, use Rule-Based mode instead

---

## 🛠️ How GPT Integration Works

### Architecture

```python
User Question
    ↓
[Extract Data Summary]
    ↓
    {
      "total_revenue": 68532976,
      "top_categories": {...},
      "customer_demographics": {...}
    }
    ↓
[Send to GPT with Context]
    ↓
OpenAI GPT-4o-mini
    ↓
[Natural Language Response]
    ↓
Display to User
```

### What Gets Sent to OpenAI

**System Prompt (Context):**
```
You are a retail sales data analyst. 
Here's the data summary:
- Total revenue: $68,532,976
- Top categories: Clothing ($28M), Shoes ($15M)...
- Customer demographics: Avg age 43, 50/50 gender split...
...
```

**User Question:**
```
"Why is clothing our best category?"
```

**GPT Response:**
```
Clothing is your top category with $28M revenue (41% of total). 
This is likely due to:
1. High purchase frequency
2. Broad customer appeal across demographics
3. Average transaction value of $689...
```

---

## 🔧 Troubleshooting

### Error: "OpenAI library not installed"
```bash
pip install openai
```

### Error: "Invalid API key"
- Check you copied the full key (starts with `sk-`)
- Ensure no extra spaces
- Generate a new key if needed
- Check your OpenAI account is active

### Error: "Rate limit exceeded"
- You're sending too many requests too fast
- Wait a few seconds between questions
- Upgrade your OpenAI plan if needed

### Error: "Insufficient quota"
- Add payment method to OpenAI account
- Your free credits may be expired
- Add funds at https://platform.openai.com/billing

### Responses Are Generic
- GPT can only see the data summary, not individual transactions
- Use filters to narrow data for more specific insights
- Ask more specific questions

---

## 🎯 Tips for Best Results

### 1. Be Specific
❌ Bad: "Tell me about sales"
✅ Good: "What were the top 3 categories by revenue last quarter?"

### 2. Use Filters First
1. Apply sidebar filters (date, category, mall)
2. Then ask GPT about the filtered data
3. Get insights for specific segments

### 3. Ask Follow-up Questions
GPT maintains context within a conversation!
```
"What's our revenue?" → "Which category is best?" → "Why?"
```

### 4. Request Analysis
Don't just ask for facts - ask for insights!
```
"What insights can you provide about customer behavior?"
"What recommendations do you have to increase revenue?"
"What patterns do you see in our sales data?"
```

### 5. Combine Modes
- Use Rule-Based for quick facts
- Switch to GPT for complex analysis
- Compare responses to validate insights

---

## 📊 Comparison Example

**Question**: "What's happening with our clothing sales?"

### Rule-Based Response:
```
🏷️ Clothing Analysis:
- Total Revenue: $28,423,745.00 (41.5% of total)
- Transactions: 15,234
- Average Sale: $1,865.23
- Most Popular Mall: Kanyon
```

### GPT-Powered Response:
```
Clothing is your strongest performing category, accounting for 
41.5% of total revenue ($28.4M). This success is driven by:

1. **High transaction volume** (15,234 sales) - more than any 
   other category
   
2. **Strong average sale value** ($1,865) - indicating customers 
   buy multiple items or premium products
   
3. **Kanyon mall dominance** - this location seems particularly 
   well-suited for clothing sales

The data suggests clothing has broad appeal across your customer 
base. Consider expanding clothing inventory, especially at 
Kanyon, and analyzing which specific items drive these high 
transaction values.
```

**Winner**: GPT provides context, insights, and recommendations! 🏆

---

## 🔄 Switching Between Modes

You can switch anytime:

1. **Left Sidebar** → Chatbot Mode radio buttons
2. Select your preferred mode
3. Chat history is preserved when switching
4. No need to restart dashboard

---

## 💡 Advanced Usage

### Custom GPT Instructions

Want to customize how GPT responds? Edit `dashboard_with_gpt.py`:

```python
system_prompt = f"""You are a retail sales data analyst assistant.
You speak in a friendly, conversational tone.
Always provide actionable recommendations.
Keep responses under 200 words.
...
"""
```

### Using Different Models

In `dashboard_with_gpt.py`, change:

```python
model="gpt-4o-mini",  # Fast & cheap
# model="gpt-4o",     # More powerful, more expensive
# model="gpt-4",      # Most powerful, most expensive
```

### Adjusting Response Length

```python
max_tokens=500,  # Increase for longer responses
temperature=0.7, # Lower (0.3) for factual, higher (0.9) for creative
```

---

## 📚 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [OpenAI Pricing](https://openai.com/pricing)
- [OpenAI Usage Dashboard](https://platform.openai.com/usage)
- [API Best Practices](https://platform.openai.com/docs/guides/production-best-practices)

---

## ✅ Quick Checklist

- [ ] Installed `openai` package
- [ ] Created OpenAI account
- [ ] Generated API key
- [ ] Added payment method (for paid usage)
- [ ] Launched `dashboard_with_gpt.py`
- [ ] Entered API key in sidebar
- [ ] Selected GPT mode
- [ ] Asked first question
- [ ] Got amazing insights! 🎉

---

**Ready to chat with GPT?** Fire up the dashboard and ask away! 🚀🤖

