from ollama import ChatResponse, chat, Options
from openai import OpenAI

from tools.date_resolver import resolve_date_tool
from utility.logger import log


class LLMProviderAdapter:
    def complete(self, model, messages, temperature, num_ctx, num_predict):
        raise NotImplementedError

    def complete_with_object(self, model, messages, response_model, temperature, num_ctx, num_predict):
        raise NotImplementedError


available_functions = [
    resolve_date_tool
]


class OllamaAdapter(LLMProviderAdapter):
    def complete(self, model, messages, temperature, num_ctx, num_predict):
        log.info("Delegating to Ollama for completion")
        response: ChatResponse = chat(
            model=model,
            messages=messages,
            options=Options(temperature=temperature, num_ctx=num_ctx, num_predict=num_predict),
            tools=[t['descriptor'] for t in available_functions]
        )
        if response.message.tool_calls:
            log.info("Tool call requested")
            for requested_tool in response.message.tool_calls:
                if function_descriptor := next((t for t in available_functions if
                                                t['descriptor']['function']['name'] == requested_tool.function.name),
                                               None):
                    log.info('Calling function', function=requested_tool.function.name)
                    log.info('Arguments:', arguments=requested_tool.function.arguments)
                    python_function = function_descriptor["python_function"]
                    output = python_function(**requested_tool.function.arguments)
                    log.info('Function output', output=output)
                    messages.append(response.message)
                    messages.append({'role': 'tool', 'content': str(output), 'name': requested_tool.function.name})
                    return self.complete(model, messages, temperature, num_ctx, num_predict)
                else:
                    log.warn('Function not found', function=requested_tool.function.name)
                    log.info('Expected usage of missing function', expected_usage=requested_tool)
                    raise Exception('Unknown tool function requested:', requested_tool.function.name)

        return response.message.content

    def complete_with_object(self, model, messages, response_model, temperature, num_ctx, num_predict):
        response: ChatResponse = chat(
            model=model,
            messages=messages,
            options=Options(temperature=temperature, num_ctx=num_ctx, num_predict=num_predict),
            format=response_model.model_json_schema()
        )
        return response_model.model_validate_json(response.message.content)


class OpenAIAdapter(LLMProviderAdapter):
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def complete(self, model, messages, temperature, num_ctx, num_predict):
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            # max_tokens=num_predict,
        )
        return response.choices[0].message.content

    def complete_with_object(self, model, messages, response_model, temperature, num_ctx, num_predict):
        response = self.client.beta.chat.completions.parse(
            model=model,
            messages=messages,
            # max_tokens=num_predict,
            response_format=response_model,
        )

        return response.choices[0].message.parsed
