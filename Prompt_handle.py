# 202602
# Prompt modifying functions
# handles PDF, website, and (wip) pictures
import datetime
import re
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import os

# main handler
# take in raw prompt, detect 
# return refined + time stamp
def handler(prompt):

    # check for pdf
    # (File paths)
    # (Simple logic: if input ends in .pdf, treat it as a file)
    # can only check for end
    context_data = ""
    if prompt.strip().endswith(".pdf"):
        context_data += extract_pdf_text(prompt.strip())
        # We don't replace the input, we just append the content to the context

    # check for website
    # Check for Links (http/https)
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', prompt)
    for url in urls:
        context_data += fetch_url_content(url)


    # combine everything
    full = f"{prompt}\nDATA:{context_data}"


    # get refined
    # time and prompt context in main
    
    return full


# Turn PDF into text
def extract_pdf_text(file_path):
    try:
        print(f"📄 Reading PDF: {file_path}...")
        doc = fitz.open(file_path)
        text = ""
        # Read first 10 pages only (to save context window)
        for page in doc[:10]: 
            text += page.get_text()
        return f"\n[START PDF CONTENT: {file_path}]\n{text[:10000]}\n[END PDF CONTENT]\n"
    except Exception as e:
        return f"[Error reading PDF: {e}]"

# Turn website into text
# take in web link
# if able to access, return text
# if unable , state error, let DS be honest
def fetch_url_content(url):
    try:
        print(f"🌐 Fetching link: {url}...")
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Kill script and style elements (CSS/JS)
        for script in soup(["script", "style"]):
            script.extract()
            
        # Get text and clean it up
        text = soup.get_text()
        clean_text = " ".join(text.split())[:8000] # Limit to 8k characters to save RAM
        return f"\n[START WEBPAGE CONTENT: {url}]\n{clean_text}\n[END WEBPAGE CONTENT]\n"
    except Exception as e:
        return f"[Error fetching link: {e}]"

# Add time
def get_current_time_str():
    return datetime.datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")


# logger
def save_chat_log(prmt, rspo, timestamp):
    # Take in raw input and raw output
    # Generate a filename with a timestamp
    #timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    folder_name = "Log"
    os.makedirs(folder_name, exist_ok=True)

    filename = os.path.join(folder_name, f"chat_log_{timestamp}.txt") 
    
    #print(f"\n💾 Saving full chat log to '{filename}'...")
    
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"=== ASSIST-O-MATIC SESSION LOG: {timestamp} ===\n\n")
        
        f.write(f"User:\n {prmt}\n\n")
        f.write("-" * 50 + "\n")
        f.write(f"Assistant:\n {rspo}" + "\n")
        f.write("-" * 50 + "\n\n")
            
    #print("✅ Log saved successfully.")



    



