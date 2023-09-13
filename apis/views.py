import json
import os
from django.middleware.csrf import get_token

from django.http import JsonResponse, HttpResponse
import subprocess


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


def upload_audio(request):
    if request.method == 'POST':
        file_key = request.POST.get('file_key')
        if file_key and file_key in request.FILES:
            audio_file = request.FILES[file_key]
            with open(f'static/{audio_file.name}', 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)
            return JsonResponse({'message': 'File uploaded successfully'})
        else:
            return JsonResponse({'error': 'Invalid file key'})
    else:
        return JsonResponse({'error': 'Invalid request'})


def chathistory(request):
    json_file_path = os.path.abspath('/Users/abhishekab/PycharmProjects/LLMBackend/static/output.json')

    try:
        with open(json_file_path, 'r') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        existing_data = []

    return JsonResponse({
        'result': existing_data,
    })


def callprogram(request, output):
    file_path = os.path.abspath('/Users/abhishekab/PycharmProjects/LLMBackend/static/file')
    json_file_path = os.path.abspath('/Users/abhishekab/PycharmProjects/LLMBackend/static/output.json')

    cmd = [file_path, output]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    try:
        with open(json_file_path, 'r') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        existing_data = []

    new_data = stdout.decode('utf-8')
    existing_data.append({'user': output, 'response': new_data})

    with open(json_file_path, 'w') as f:
        json.dump(existing_data, f, indent=4)

    return_code = process.returncode

    return JsonResponse({
        'result': new_data,
        'error': stderr.decode('utf-8'),
        'return_code': return_code
    })
