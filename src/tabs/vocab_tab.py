import gradio as gr
from agents.vocab_agent import VocabAgent
from utils.logger import LOG


vocab_agent = VocabAgent()

feature = "vocab_study"

def get_page_desc(feature):
    try:
        with open(f"../content/page/{feature}.md", "r", encoding="utf-8") as file:
            scenario_intro = file.read().strip()
        return scenario_intro
    except FileNotFoundError:
        LOG.error(f"File not found: {feature}.md")
        return "vocab study page not found"

def restart_vocab_study_chatbot():
    vocab_agent.restart_session()
    _next_round = "Let's do it"
    bot_message = vocab_agent.chat_with_history(_next_round)
    return [{"role": "assistant", "content": bot_message}]

def handle_vocab(user_input, chat_history):
    bot_message = vocab_agent.chat_with_history(user_input)
    LOG.info(f"[Vocab ChatBot]: {bot_message}")
    return bot_message

def create_vocab_tab():
    with gr.Tab("单词"):
        gr.Markdown("## 闯关背单词")

        gr.Markdown(get_page_desc(feature))

        vocab_study_chatbot = gr.Chatbot(
            placeholder="<strong>您的英语私教 Paul</strong><br><br>开始学习新单词吧！",
            height=600,
        )

        restart_btn = gr.ClearButton(value="下一关")
        restart_btn.click(
            fn=restart_vocab_study_chatbot,
            inputs=None,
            outputs=vocab_study_chatbot,
        )

        gr.ChatInterface(
            fn=handle_vocab,
            chatbot=vocab_study_chatbot,
        )