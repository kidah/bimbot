from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
#import socketio
from .forms import ChatForm
from rasa_core.channels.socketio import socketio

# from .bot import agent


#@socketio.on('connect')
def home_view(request):
	return render(request, 'chatbot.html')

def chatview(request):
	form = ChatForm()
	return render(request, 'chatbot.html', {'form': form} )

@csrf_exempt
def webhook(request):
	print(request.POST)
	return JsonResponse({"status": "OK"})

# @csrf_exempt 
def handle_response(request, *args, **kwargs):
	if request.method == "POST":
		try:
			print(request)
			print(request.POST.get('user_input'))
			message = request.POST.get('user_input')
			responses = agent.handle_message(message)
			print(responses)
			bot_data = {
				'status': 'OK',
				'responses': responses[0]['text']
			}
			return JsonResponse(bot_data)
		except Exception as e:
			return JsonResponse({'status': 'FAILED', 'responses': 'default'})

