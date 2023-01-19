import openai

openai.api_key = "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"

def generate_response(prompt):
  completions = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=2048,
    n=1,
    stop=None,
    temperature=0.5,
  )

  message = completions.choices[0].text
  return message

