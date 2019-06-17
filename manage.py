#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatsite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


# python3 -m rasa_nlu.train -c nlu_config.yml --fixed_model_name current        --data ./data/nlu.md --path ./models/nlu
# python3 -m rasa_core.train -s data/stories.md -d domain.yml -o models/dialogue --endpoints endpoints.yml

#python3 -m rasa_nlu.train -c nlu_config.yml --fixed_model_name bimnlu        --data ./data/training_dataset.json --path ./models 
# python3 -m rasa_core_sdk.endpoint --actions actions
#python3 -m rasa_core.run -d models/dialogsue -u models/current/bimnlu --endpoints endpoints.yml
''' 
docker run \
  -v $(pwd)/models:/app/models \
  rasa/rasa:latest-full \
  --endpoints endpoints.yml
  run

  docker run -p 5055:5055 --mount type=bind,source=$(pwd)/actions,target=/app/actions \
	rasa/rasa-sdk:latest 
  
  lsof -i 5055 kill pid

docker run 
-v $(pwd):/app/project
-v $(pwd)/models/rasa_core:/app/models 
rasa/rasa_core:latest
run python -m rasa_core.train
interactive
-o models 
-d domain.yml
-s /app/project/data/stories.md 
--nlu /app/models 
--endpoints /app/project/config/endpoints.yml

docker run \
  -v $(pwd):/app \
  -v $(pwd)/models/rasa_core:/app/models \
  rasa/rasa:latest-full \
  train \
    --domain domain.yml \
    --data data \
    --out models \
    --endpoints /app/project/config/endpoints.yml

docker run \
  -v $(pwd):/app \
  rasa/rasa:latest-full \
  train \
    --domain domain.yml \
    --data data \
    --out models 
'''
