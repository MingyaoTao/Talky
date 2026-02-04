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
                with the current exchange: user said: {other_1.message} you replied: {other_2.message}
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
        f.write({prompt}+"\n\n")
        f.write({response}+"\n\n\n")

        
# load talks

