from django.shortcuts import render
from django.conf import settings
from django.http import StreamingHttpResponse
import openai
import os
import time
import json

openai.api_key = getattr(settings, 'OPEN_API_KEY', None)

# Create your views here.
def get_completion(prompt): 
    print(prompt) 

    start_time = time.time()

    query = openai.ChatCompletion.create( 
        model="gpt-4-turbo",
        messages=[
            {'role':'user','content': prompt}
        ], 
        max_tokens=4096, 
        n=1, 
        stop=None, 
        temperature=0,
        stream=True
    ) 

    for chunk in query:
        chatcompletion_delta = chunk["choices"][0].get("delta", {})
        data = json.dumps(dict(chatcompletion_delta))
        yield f'data: {data}\n\n'

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response['X-Accel-Buffering'] = 'no'  # Disable buffering in nginx
    response['Cache-Control'] = 'no-cache'  # Ensure clients don't cache the data
    
    return response 

def prompt(request):
    if request.method == 'POST': 
        prompt = request.POST.get('prompt') 
        prompt=str(prompt)
        response = get_completion(prompt)
        #return JsonResponse({'response': response})
        return response

    return render(request, 'index.html') 