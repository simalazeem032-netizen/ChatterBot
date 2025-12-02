# Quick Start Guide

## ✅ Success! Your chatbot is working!

The chatbot ran successfully as shown in your terminal. Here are all the ways to run it:

## Ways to Run

### 1. **Standalone Console Mode** (Recommended - No Flask needed!)
```bash
py chatbot_console.py
```
**Perfect for online terminals!** This is what you just ran successfully.

### 2. **Using Batch File** (Windows)
```bash
run.bat --console
```
or double-click `run.bat`

### 3. **Using PowerShell Script**
```powershell
.\run.ps1 --console
```

### 4. **Full API Mode** (Requires Flask)
```bash
py app.py --console    # Console mode
py app.py              # API server mode
py app.py --test       # Test mode
```

## What You Have

### ✅ OOP Features Implemented:
- **Classes**: 8+ classes with clear responsibilities
- **Inheritance**: Base classes (`MatcherStrategy`, `ResponseHandler`) with derived classes
- **Polymorphism**: Same interface (`calculate_score()`, `format_response()`), different implementations
- **Functions**: Utility functions (`validate_input()`, `format_confidence()`, etc.)
- **Comments**: Comprehensive documentation throughout

### ✅ Files Created:
1. `chatbot_console.py` - Standalone console version (NO Flask needed!)
2. `app.py` - Full API version with Flask
3. `run.bat` - Windows batch script
4. `run.ps1` - PowerShell script
5. `iot_chatbot.py` - Original console chatbot

## Usage Examples

### Console Mode (What you just ran):
```
You: What is the flight time?
Bot: The drone offers up to 28–32 minutes of continuous flight time per battery, depending on wind and payload.
(Confidence: 95.0%)

You: help
Available questions:
1. What is the flight time of this drone?
2. What is the maximum range?
...

You: exit
Bot: Thank you for visiting. Goodbye!
```

## For Online Terminals

**Best option**: Use `chatbot_console.py` - it works everywhere!

- ✅ Replit
- ✅ GitHub Codespaces  
- ✅ CodeSandbox
- ✅ Any Python environment

Just run: `python chatbot_console.py` or `py chatbot_console.py`

## OOP Structure Summary

```
MatcherStrategy (Abstract Base Class)
├── SimilarityMatcher (Inherits)
├── KeywordMatcher (Inherits)
└── HybridMatcher (Inherits, uses Composition)

ResponseHandler (Abstract Base Class)
├── ConsoleResponseHandler (Inherits)
└── ErrorResponseHandler (Inherits)

FAQDatabase (Uses Composition with MatcherStrategy)
ChatbotAPI (Uses Composition with FAQDatabase and ResponseHandler)
```

All demonstrating **polymorphism** - same interface, different implementations!

