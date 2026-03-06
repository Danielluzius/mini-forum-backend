from rest_framework.throttling import UserRateThrottle


class PostThrottle(UserRateThrottle):
    scope = 'posts'
