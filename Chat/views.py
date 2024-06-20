from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import openai
import os

openai.api_key = getattr(settings, 'OPEN_API_KEY', None)

# Create your views here.
def get_completion(prompt): 
    print(prompt) 
    query = openai.ChatCompletion.create( 
        model="gpt-4-turbo",
        messages=[
            {'role':'user','content': prompt}
        ], 
        max_tokens=4096, 
        n=1, 
        stop=None, 
        temperature=0, 
    ) 
    response = query.choices[0].message["content"]
    print(response) 
    return response 

def prompt(request):
    if request.method == 'POST': 
        prompt = request.POST.get('prompt') 
        prompt=str(prompt)
        response = get_completion(prompt)
        return JsonResponse({'response': response}) 
    return render(request, 'index.html') 