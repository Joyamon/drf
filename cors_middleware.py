class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"  # 允许所有源访问
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"  # 允许的请求方法
        response["Access-Control-Allow-Headers"] = "Content-Type" # 允许的请求头
        return response