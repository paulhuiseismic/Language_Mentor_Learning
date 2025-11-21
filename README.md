# Language Mentor Learning 🎓

An AI-powered English conversation learning application that provides personalized English practice through interactive conversations and scenario-based training.

## 📋 Overview

Language Mentor Learning is an intelligent English tutoring system built with LangChain and Gradio. It features an AI teacher named **DjangoPeng** who helps students practice English through natural conversations and realistic scenarios like technical interviews, restaurant ordering, and meeting hosting.

## ✨ Features

- **Conversation Practice**: Free-form English conversation practice with an AI tutor
- **Scenario Training**: Practice specific real-world scenarios:
  - 🎯 Technical Interview
  - 🍽️ Restaurant Ordering
  - 👔 Salary Negotiation
  - 🏠 Hotel Check-in & Apartment Rental
- **Intelligent Feedback**: Get real-time corrections and suggestions
- **Conversation History**: Maintains context throughout the conversation
- **Adaptive Learning**: Adjusts difficulty based on student responses
- **Bilingual Support**: Feedback in Chinese with English reference sentences

## 🏗️ Project Structure

```
Language_Mentor_Learning/
├── src/
│   ├── main.py                      # Main application entry point
│   ├── azure_openai.py              # Azure OpenAI configuration
│   ├── agents/
│   │   └── conversation_agent.py    # Conversation agent with history
│   └── utils/
│       └── logger.py                # Logging utility
├── prompts/
│   └── conversation_prompt.txt      # System prompt for the AI tutor
├── logs/
│   └── app.log                      # Application logs
├── images/                          # Image assets
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Azure OpenAI API access
- pip package manager

### Installation

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   cd Language_Mentor_Learning
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Create a `.env` file in the root directory with the following variables:
   ```env
   AZURE_OPENAI_API_KEY=your_api_key_here
   AZURE_OPENAI_ENDPOINT=your_endpoint_here
   AZURE_API_VERSION=2024-02-15-preview
   AZURE_MODEL=your_model_deployment_name
   ```

### Running the Application

1. **Start the application**:
   ```bash
   cd src
   python main.py
   ```

2. **Access the interface**:
   - The Gradio interface will launch automatically
   - Open your browser to the provided URL (typically `http://localhost:7860`)
   - The app will also create a public share link if `share=True`

## 🎯 How to Use

### Conversation Practice Tab

1. Navigate to the "对话练习" (Conversation Practice) tab
2. Start typing in English to begin your conversation
3. The AI tutor will respond and provide feedback
4. Use the "清除历史记录" (Clear History) button to start a new conversation

### Scenario Training Tab

1. Navigate to the "场景训练" (Scenario Training) tab
2. Select a scenario from the dropdown menu:
   - 求职面试 (Job Interview)
   - 酒店入住 (Hotel Check-in)
   - 薪资谈判 (Salary Negotiation)
   - 租房 (Apartment Rental)
3. Follow the AI tutor's guidance through the scenario
4. Practice realistic dialogues and receive feedback

## 🧠 Technology Stack

- **LangChain**: Framework for building AI applications with LLMs
- **Gradio**: Web interface for machine learning applications
- **Azure OpenAI**: GPT-4 powered language model
- **Loguru**: Advanced Python logging
- **Python-dotenv**: Environment variable management

## 📦 Dependencies

```
python-dotenv
langchain==0.2.16
langchain_core==0.2.41
langchain_community==0.2.17
langchain_openai==0.1.25
langchain_ollama==0.1.3
gradio
huggingface-hub==0.22.2
loguru==0.7.2
```

## 🎓 Learning Scenarios

### 1. Technical Interview
Practice common technical interview questions including:
- Personal introductions
- Technical knowledge questions
- Behavioral interview questions
- Project experience discussions

### 2. Restaurant Ordering
Learn to:
- Ask about the menu
- Place orders
- Make special requests
- Handle payment

### 3. Meeting Hosting
Improve your professional skills:
- Opening remarks
- Guiding speakers
- Time management
- Meeting summaries

## 🔧 Configuration

### System Prompt
The AI tutor's behavior is controlled by `prompts/conversation_prompt.txt`. You can customize:
- Teaching style
- Difficulty levels
- Feedback language
- Scenario types

### Session Management
- Conversations are stored in memory with session IDs
- Each session maintains its own chat history
- Default session ID: `abc123`

## 📝 Logging

Application logs are stored in `logs/app.log` and include:
- DEBUG: Chat history and detailed agent responses
- INFO: Bot messages and user interactions
- Timestamps and source information

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Add more practice scenarios
- Implement voice input/output
- Add progress tracking
- Create difficulty level assessments
- Support for more languages

## 📄 License

This project is for educational purposes.

## 👤 Author

Built with ❤️ for English language learners

## 🙏 Acknowledgments

- Azure OpenAI for providing the language model
- LangChain for the excellent LLM framework
- Gradio for the intuitive UI framework

---

**Happy Learning! 📚**

