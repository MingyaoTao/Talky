# 202602
# handles old conversation
import ollama
import datetime
from dataclasses import dataclass


# talk object (class)
# Category: user / machine / old_conv
# Data: One back, or forth, string?


@dataclass
class Talk:
    message: str
    category: str # user / asssitant / old
    
#    def combine(self, other):
#        return Talk(self.message + other.message, "old")


# comnbine the last 2 conversation (back and forth) with the old conv 
# old_conv += last
# send into DS
# take in 2 objects, return 1 with old category
def treat(old_mem, other_1, other_2):
    # self = old 
    prompt = f"""Generalize and combine this distant memory: {old_mem.message} 
                with the current exchange: {other_1.category} said: {other_1.message}. {other_2.category} replied : {other_2.message}
                Summarize this into one concise paragraph. Keep key facts but be brief."""  

    #model_name='deepseek-r1:1.5b'
    model_name = 'qwen3:0.6b'

    response = ollama.chat(
        #model='deepseek-r1:8b', # Or 'llama3'
        messages=[{'role': 'user', 'content': prompt}]
        # log into separate json
    )
    
    summary_text = response['message']['content']
    return Talk(summary_text, "old")


# Operator function?

# save talks
def save_talks(prompt, response):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"history_treatment_log.txt"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"=== {timestamp} ===\n\n")
        f.write(f"{prompt.category}: {prompt.message}\n\n")
        f.write(f"{response.category}: {response.message}\n\n")

        
# load talks


# final combine
def combine_history (history_deque, old):
    currtime = datetime.datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")

    # add old
    messages = [
        {
            "role" : "system",
            "content" :
            f"""
            You are a smart personal secretary.
            CURRENT TIME: {currtime}
            
            INSTRUCTIONS:
            - If the user asks about a link or PDF, the content is provided below.
            - Be concise.
            """
        }
    ]
    
    messages.append({"role" : "system", "content" : f"Previous Conversation Summary:{old.message}"})

    for talk in history_deque:
        if talk.category == "user":
            messages.append({"role": "user", "content": talk.message})
        elif talk.category == "assistant":
            messages.append({"role": "assistant", "content": talk.message})

    #messages.append({"role": "user", "content":{prompt.message}})
    return messages

