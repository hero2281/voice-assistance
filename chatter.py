import json
import requests

API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"

headers = {"Authorization": f"Bearer {API_TOKEN}"}
def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))

if __name__ == "__main__":
    print("Ask me anything or press q to quit...")
    print()
    username = input("Hi! Please enter your username: ")
    print()
    print(f"Hi! {username}. I am ChatFriend! Go ahead and ask me something...")
    print()

    while True:
        user = input(f"{username} > ")
        data = query(user)
        # print(data)
        print("ChatFriend > ", data['generated_text'])
        print()

        if user == "q":
            print("ChatFriend > ", "Nice chatting with you. Bye")
            print()
            break


