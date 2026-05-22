from groq import Groq

client = Groq(
    api_key="ur_api_key"
)
messages = [
    {
        "role": "system",
        "content": "You are a very motivating person.Motivate and inspire like a pyschologist."
    }
]

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=200
    )

    
    ai_response = chat_completion.choices[0].message.content

    
    print("AI:", ai_response)

    messages.append(
        {
            "role": "assistant",
            "content": ai_response
        }
    )