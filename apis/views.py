import json
import os
import signal
from django.middleware.csrf import get_token
from django.http import StreamingHttpResponse
from django.http import JsonResponse
import subprocess

global process
process = None


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


def stream_output(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    for line in process.stdout:
        yield line


def abort_code(request):
    global process
    if process is not None:
        process.send_signal(signal.SIGINT)  # Send interrupt signal to the process
        process = None  # Reset the process variable
        return JsonResponse({'message': 'Code execution aborted'})
    else:
        return JsonResponse({'message': 'No running process to abort'})

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


def save_log(request):
    json_file_path = os.path.abspath('/Users/abhishekab/PycharmProjects/LLMBackend/static/output.json')
    try:
        with open(json_file_path, 'r') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        existing_data = []

    global process

    if process is not None:
        process.send_signal(signal.SIGINT)
        process = None

    with open(json_file_path, 'w') as f:
        json.dump(existing_data, f, indent=4)

    return JsonResponse({'message': 'Current log saved to output.json'})


def callprogram(request, output):
    file_path = os.path.abspath('/Users/abhishekab/PycharmProjects/LLMBackend/static/file')
    json_file_path = os.path.abspath('/Users/abhishekab/PycharmProjects/LLMBackend/static/output.json')

    cmd = [file_path, output]

    response = StreamingHttpResponse(stream_output(cmd), content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{output}.log"'

    return response


