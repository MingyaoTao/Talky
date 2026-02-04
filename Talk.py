# 202602
# Main
# Contain talk loop

import ollama
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
    chat_history = deque(maxlen = 10)
    distant_mem = history_manager.Talk("This is the start of a new conversation with the User.", "old")

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

        # currently only old back and forth 11

        if len(chat_history) >= 10:
            # clean up
            # distant_mem += old 2 conv
            distant_mem = history_manager.treat(distant_mem, chat_history[8], chat_history[9])

        # make to list 
        chat_history.append(user_input)

        # add context, time, and others
        system_msg = f"""
            You are a smart personal secretary.
            CURRENT TIME: {Prompt_handle.get_current_time_str()}
            
            INSTRUCTIONS:
            - If the user asks about a link or PDF, the content is provided below.
            - Be concise.
            """
        
        # put things together
        final_input = history_manager.combine_history(chat_history, distant_mem)

        # full send
        print("thinking...\n")
        response = ollama.chat(
            model = 'deepseek-r1:8b',
            messages = final_input
        )

        # collect response, put in deque
        print(response['message']['content'])

        chat_history.append(history_manager.Talk(response['message']['content'], "assistant"))

        # record
        history_manager.save_talks(chat_history[0], chat_history[1])




if __name__ == "__main__":
    chat_main()