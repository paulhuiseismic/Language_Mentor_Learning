import gradio as gr
from agents.conversation_agent import ConversationAgent
from utils.logger import LOG

conversation_agent = ConversationAgent()

def handle_conversation(user_input, chat_history):
    bot_message = conversation_agent.chat_with_history(user_input)
    LOG.info(f"[Conversation ChatBot]: {bot_message}")
    return bot_message

def create_conversation_tab():
    with gr.Tab("对话练习"):
        gr.Markdown("## 练习英语对话 ")
        conversation_chatbot = gr.Chatbot(
            placeholder="<strong>您的英语私教 Paul</strong><br><br>想和我聊什么话题都可以，记得用英语哦！",
            height=600,
        )

        def handle_conversation(user_input, chat_history):
            bot_message = conversation_agent.chat_with_history(user_input)
            LOG.info(f"[ChatBot]: {bot_message}")
            return bot_message

        gr.ChatInterface(
            fn=handle_conversation,
            chatbot=conversation_chatbot,
        )