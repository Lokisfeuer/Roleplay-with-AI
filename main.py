import os
import openai

# Load your API key from an environment variable or secret management service
openai.api_key = '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'




def main():
    response = openai.Completion.create(model="text-davinci-002",
                                        prompt="Say this is a test",
                                        temperature=0,
                                        max_tokens=6)
    response = response['choices'][0]['text']
    print(response)


if __name__ == '__main__':
    main()
