# 202602
# Main
# Contain talk loop

import ollama
import re
from collections import deque
#from history_manager import HistoryManager
import history_manager
import Prompt_handle


# Take in user input

# send over to Prompt_handle to detect pdf, website, etc


# combine new prompt to history (add to the list)
# it's in the history manager
# call for a check, if >10, use the function perform: old_conv += history(last)



# now the prompt is refined, sned to DS
def chat_main():
    # 5 pairs of back and forth, 1 new, 1 old_conv
    chat_history = deque(maxlen = 12)

    print(f"🤖 Talky Online. (Time: {Prompt_handle.get_current_time_str()})")

    while True:
        user_input_raw = input("\nYou: ")

        if user_input_raw.lower() in ["exit", "quit"]:
            Prompt_handle.save_chat_log(chat_history)
            break

        # handle raw 
        user_input_raw = Prompt_handle.handler(user_input_raw)

        # into history
        user_input = history_manager.Talk(user_input_raw, "user")

        if len(chat_history) >= 12:
            # clean up
            chat_history[9] = history_manager.treat(chat_history[11], chat_history[10], chat_history[9])

        # make to list 
        chat_history.append(user_input)

        # send the prompt for handling




# --- MAIN LOOP ---
def chat_with_secretary():

    
    # Context buffer (so it remembers the previous question)
    conversation_history = HistoryManager(max_exchanges=5)

    while True:



        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]: 
            save_chat_log(conversation_history)
            break

        # 1. PRE-PROCESS: Check for PDFs (File paths)
        # (Simple logic: if input ends in .pdf, treat it as a file)
        context_data = ""
        if user_input.strip().endswith(".pdf"):
            context_data += extract_pdf_text(user_input.strip())
            # We don't replace the input, we just append the content to the context

        # 2. PRE-PROCESS: Check for Links (http/https)
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', user_input)
        for url in urls:
            context_data += fetch_url_content(url)

        # 3. BUILD PROMPT
        # We construct the "System Message" fresh every time to update the clock
        system_msg = f"""
        You are a smart personal secretary.
        CURRENT TIME: {get_current_time_str()}
        
        INSTRUCTIONS:
        - If the user asks about a link or PDF, the content is provided below.
        - Be concise.
        """

        # Combine User Input + Any Scraped Data
        full_prompt = f"{user_input}\n\nDATA:\n{context_data}"
        conversation_history.add_message('user', full_user).     # !!!!! Work in progress

        # 4. SEND TO OLLAMA
        print("Thinking...")
        
        # We append to history for conversational flow
        conversation_history.append({'role': 'user', 'content': full_prompt})
        
        # Note: If history gets too long, M2 Air might slow down. 
        # In V3 we will trim this list.
        response = ollama.chat(
            model='deepseek-r1:8b', # Or 'llama3'
            messages=[{'role': 'system', 'content': system_msg}] + conversation_history
        )

        reply = response['message']['content']
        print(f"Secretary: {reply}")
        
        # Add reply to history
        conversation_history.append({'role': 'assistant', 'content': reply})

if __name__ == "__main__":
    chat_main()