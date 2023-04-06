import json

import openai

with open('source.json') as file:
    source = json.load(file)
    api_key = source['chatGPT'][0]['API_key']

openai.api_key = api_key


async def chat(ctx, *question):
    search = ""
    for i in question:
        search = str(search) + i + " "
    prompt = search
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt,
                                        temperature=0,
                                        max_tokens=500,
                                        top_p=1.0,
                                        frequency_penalty=0.0,
                                        presence_penalty=0.0)
    message = response.choices[0].text.strip()
    await ctx.send(message)
