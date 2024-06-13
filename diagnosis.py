
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def return_answer(question):
    client = OpenAI()
    assistant = client.beta.assistants.create(
        name="Personal Helper",
        instructions="You are a healthcare professional assisting a doctor in making a diagnosis. You are given a list of symptoms and a file containing medical knowledge on cardiology. Your job is to assist the doctor in making diagnoses.",
        model="gpt-4-turbo",
        tools=[{"type": "file_search"}],
    )

    assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": ['vs_w8PIRwxhcRh1RMlUaklJeKGR']}},
    )

    thread = client.beta.threads.create()

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="You are a healthcare professional assisting a doctor in making a diagnosis. You are given a list of symptoms being" + question + "and a file containing medical knowledge on cardiology. Your job is to assist the doctor in making diagnoses by providing 6 detailed probable diagnoses and how they correlate to the symptoms",
    )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread.id,
            run_id=run.id
        )
        answer = messages.data[0].content[0].text.value
        return answer
    
def get_symptoms():
    symptoms = input("Please enter your symptoms: ")
    return symptoms
    
    
def get_answer(question: str):
    final_answer = return_answer(question)
    return {"answer": final_answer}

symptoms = get_symptoms()
diagnosis = get_answer(symptoms)
print(diagnosis["answer"])
