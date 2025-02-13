from tqdm import tqdm


def create_prompt(prompts_file, prompt_name):
    sheet_data = prompts_file[prompt_name]
    prompt = []
    for message in sheet_data.index:
        dict_entry = {
            "role": sheet_data.loc[message, "role"],
            "content": sheet_data.loc[message, "content"],
        }
        prompt.append(dict_entry)
    return prompt


def get_responses(prompt, texts, model, client):
    responses = []
    for text in tqdm(texts):
        messages = prompt + [{"role": "user", "content": text}]

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.00,
        )
        # clean and append response
        cleaned_response = response.choices[0].message.content
        responses.append(cleaned_response.lower())
    return responses
