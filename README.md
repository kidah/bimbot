### Chatbot Models are up to date with the current versions of rasa core & nlu

# Usage
**Replace the rasachat/models folder with your models folder and run django server and bot.py file seperately**

**The data used to train the chatbot is very minimal, you should replace the rasachat/models folder or extend and improve the training data by updating `rasachat/nlu.nd` & `rasachat/stories.md` files.**

Also refer to [Django-Rasa-Sockets](https://github.com/Alexmhack/Django-Rasa-Sockets) for more info on implementing Django and Rasa with Sockets.

# Django-Rasa-Bot
Integrating Rasa Core with Django backend and finally using Webchat for chatbot user interface

In this project we will be using [rasa_core](https://rasa.com/docs/core/quickstart/) 
for our chatbot backend **django** for website backend and [rasa-webchat](https://github.com/mrbot-ai/rasa-webchat) for chatbot **User Interface**

We have to first create a Rasa SocketIO Channel Layer

Create a separate file for this layer in rasachat folder **bot.py**
```
from rasa_core.agent import Agent
from rasa_core.channels.socketio import SocketIOInput
from rasa_core.agent import Agent

# load your trained agent
agent = Agent.load('models/dialogue', interpreter='models/current/nlu')

input_channel = SocketIOInput(
	# event name for messages sent from the user
	user_message_evt="user_uttered",
	# event name for messages sent from the bot
	bot_message_evt="bot_uttered",
	# socket.io namespace to use for the messages
	namespace=None
)

# set serve_forever=False if you want to keep the server running
s = agent.handle_channels([input_channel], 5005, serve_forever=True)
```

Above piece of code comes from Rasa [docs](https://www.rasa.com/docs/core/connectors/#id18)

Then in your html template configure rasa-webchat with following code

```
<body>
          <div class="chatbot">
              <div class="chatscreen">
               <ul class="chat-list" id="messages">
                <!-- chat messages-->
                    
                </ul>
              </div>
              <div class="chatinput">
                <form id="chatform">
                    <div class="form-group">
                        <div class="speech">
                          <input class="form-control" id="user_says" placeholder="Start Speaking..."></input>
                          <img src="../static/img/iconfinder_mic_1055024.png" id="img-listen" class="img img-responsive"/>
                        </div>
                      </div>
                </form>
              </div>
            </div>
      <script>
        $(function () {
    
        var socket = io('http://localhost:5005/', {'path': '/socket.io/', 'pingInterval': 1000, 'pingTimeout': 5000,});
    
        socket.on('connect', function(){
            console.log("connected")
        });
    
        $('#chatform').submit(function(e){
          e.preventDefault(); // prevents page reloading
          socket.emit('user_uttered', {'message': $('#user_says').val() });
          $('<li class="in"><div class="chat-img"><img alt="Avtar" src="http://bootdey.com/img/Content/avatar/avatar2.png"></div><div class="chat-body"><div class="chat-message"><h5>Tim</h5><p></p></div></div></li>').appendTo('#messages').contents().find("p").text($('#user_says').val());
          return false;
        });
        
        socket.on('bot_uttered', (botUttered) => {
          $.each(botUttered, function(msg, text) {
            $('<li class="out"><div class="chat-img"><img alt="Avtar" src="../static/img/bimgirl.jpeg"></div><div class="chat-body"><div class="chat-message"><h5>Sophy</h5><p></p></div></div></li>').appendTo('#messages').contents().find('p').text(botUttered['text']);
           console.log(botUttered['text'])
          });
         
        });
    
        socket.on('disconnect', function(){
            console.log("disconnected")
            if (reason !== 'io client disconnect') {
            this.props.dispatch(disconnectServer());
          }
        });
      });
      </script>
</body>
```

Now run the django server and the socketio server seperately using two terminals,


```
../Django-Rasa-Bot> python manage.py runserver
# then in another command prompt or terminal run
../Django-Rasa-Bot/rasachat> python bot.py
```

Now open the url [127.0.0.1:8000](http://127.0.0.1:8000) and click on the chat widget placed in bottom right and 
enter ```hi there``` and the bot will reply.
