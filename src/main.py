import os
from pathlib import Path
import gradio as gr
from agents.conversation_agent import ConversationAgent
from agents.scenario_agent import ScenarioAgent
from utils.logger import LOG

# Get the project root directory (parent of src)
PROJECT_ROOT = Path(__file__).parent.parent
os.chdir(PROJECT_ROOT)

conversation_agent = ConversationAgent()

agents = {
    "job_interview": ScenarioAgent("job_interview"),
    "hotel_checkin": ScenarioAgent("hotel_checkin"),
    "renting_house": ScenarioAgent("renting_house"),
    "airport_checkin": ScenarioAgent("airport_checkin"),
}

def handle_conversation(user_input, chat_history):
    LOG.debug(f"[聊天记录]: {chat_history}")
    bot_message = conversation_agent.chat_with_history(user_input)
    LOG.info(f"[ChatBot]: {bot_message}")
    return bot_message

def get_scenario_intro(scenario):
    with open(f"content/page/{scenario}.md", "r", encoding="utf-8") as file:
        scenario_intro = file.read().strip()
    return scenario_intro


def handle_scenario(user_input, chat_history, scenario):
    bot_message = agents[scenario].chat_with_history(user_input)
    LOG.info(f"[{scenario} ChatBot]: {bot_message}")
    return bot_message


with gr.Blocks(title="LanguageMentor 英语私教") as language_mentor_app:
    with gr.Tab("对话练习"):
        gr.Markdown("## 练习英语对话 ")
        conversation_chatbot = gr.Chatbot(
            placeholder="<strong>您的英语私教 Paul</strong><br><br>想和我聊什么话题都可以，记得用英语哦！",
            height=600,
        )

        gr.ChatInterface(
            fn=handle_conversation,
            chatbot=conversation_chatbot,
        )

    with gr.Tab("场景训练"):
        gr.Markdown("## 选择一个场景完成目标和挑战")

        scenario_radio = gr.Radio(
            choices=[
                ("酒店入住", "hotel_checkin"),
                ("求职面试", "job_interview"),
                ("租赁房屋", "renting_house"),
                ("机场值机", "airport_checkin"),
                #("薪资谈判", "salary_negotiation"),
            ],
            label="场景"
        )
        scenario_intro = gr.Markdown()
        scenario_chatbot = gr.Chatbot(
            placeholder="<strong>您的英语私教 Paul</strong><br><br>选择场景后开始对话吧！",
            height=600,
        )

        def start_new_scenario_chatbot(scenario):
            initial_ai_message = agents[scenario].start_new_session()
            return [{"role": "assistant", "content": initial_ai_message}]

        scenario_radio.change(
            fn=lambda s: (get_scenario_intro(s), start_new_scenario_chatbot(s)),
            inputs=scenario_radio,
            outputs=[scenario_intro, scenario_chatbot],
        )

        gr.ChatInterface(
            fn=handle_scenario,
            chatbot=scenario_chatbot,
            additional_inputs=scenario_radio,
        )


if __name__ == "__main__":
    language_mentor_app.launch(share=True, server_name="0.0.0.0")