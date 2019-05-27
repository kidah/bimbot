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
#python3 -m rasa_core.run -d models/dialogue -u models/default/bimnlu --endpoints endpoints.yml