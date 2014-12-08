# test.py
def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return ["Coming December 2014: The Lee Family College Bowl Series"]
