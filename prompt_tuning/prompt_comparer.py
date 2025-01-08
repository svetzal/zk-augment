from ollama import Message

from llm.llm_gateway import LLMGateway
from models import EntityTypes

# scenarios = ["prompt1.txt", "prompt1a.txt", "prompt1b.txt", "prompt1c.txt"]
scenarios = ["prompt3.txt", "prompt3a.txt"]
models = ['llama3.1-instruct-8b-32k', 'llama3.3-instruct-70b-32k']

results = {}
for scenario in scenarios:
    prompt = open(f"prompt_tuning/{scenario}", "r").read()
    for model in models:
        llm = LLMGateway(model)
        for temperature in [0.5]:#0, 0.1, 0.5, 1.0]:
            generated_object = llm.generate_object(messages=[Message(role="user", content=prompt)],
                                                   response_model=EntityTypes, temperature=0.5, num_ctx=32768,
                                                   num_predict=8192)

            results[f"{model}_{temperature}"] = generated_object.list

            generated_object.list = sorted(generated_object.list, key=lambda x: x.label)

            with open(f"prompt_tuning/{scenario}_{model}_{temperature}.json", "w") as f:
                f.write(generated_object.model_dump_json(indent=2))

