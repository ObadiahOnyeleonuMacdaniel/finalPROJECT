from django.shortcuts import render

# Create your views here.
# sentapp/views.py
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

# import the pipeline we loaded once
from .model_store import sent_pipeline

@csrf_exempt
def predict(request):
    # accept POST with raw JSON like: {"text": "I love this!"}
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")

    try:
        data = json.loads(request.body.decode("utf-8"))
        text = data.get("text", "")
        if not text:
            return HttpResponseBadRequest("Send {'text': 'your sentence'}")
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    # Run the pipeline
    result = sent_pipeline(text)

    # result is a list like [{"label": "5 stars", "score": 0.8}] for this model
    return JsonResponse({"input": text, "prediction": result})
