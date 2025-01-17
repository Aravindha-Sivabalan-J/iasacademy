class NavigationHistoryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the current response
        response = self.get_response(request)

        # Skip if it's an AJAX request or API call
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.path.startswith('/api/'):
            return response

        # Current URL (the page being visited)
        current_url = request.path

        # Initialize session history if not already set
        if 'history' not in request.session:
            request.session['history'] = []

        # Get the history stack
        history = request.session['history']

        # Avoid pushing the same URL consecutively to prevent loops
        if history and history[-1] != current_url:
            history.append(current_url)
            request.session['history'] = history

        return response
