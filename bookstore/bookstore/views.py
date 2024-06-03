# bookstore/views.py

from django.shortcuts import render

import logging

logger = logging.getLogger(__name__)


def home(request):
    logger.debug("Rendering the home page")
    return render(request, 'index.html')
