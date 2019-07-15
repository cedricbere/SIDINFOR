#!/usr/bin/env python
# -*- coding: utf8 -*-


'''
Created on 28 déc. 2018

@author: parice02
'''

from threading import current_thread
_requests = {}


class RequestMiddleware(object):
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    
    def __call__(self, request):
        reponse = self.get_response(request)
        self.process_resquest(request)
        return reponse
    
    def process_resquest(self, request):
        global _requests
        _requests[current_thread()] = request
        #_requests['user'] = request
    
    
        
def get_user():
    t = current_thread()
    global _requests
    if t not in _requests:
        return None
    return _requests[t].user