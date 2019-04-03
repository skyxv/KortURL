from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import CreateLinkMapSerializer
from apps.utils.get_configs import config


class ShortUrlsView(APIView):
    """
    批量缩短网址API
    """
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def serialize(link_maps, invalid_urls):
        results = []
        for instance in link_maps:
            results.append({"long_url": instance.url,
                            "short_url": config.get_short_url_(instance.code)})
        return {"results": results, "invalid_urls": invalid_urls}

    def post(self, request):
        form = CreateLinkMapSerializer(data=request.data, context={'request': request})
        if form.is_valid(raise_exception=True):
            link_maps, invalid_urls = form.save()
            return Response(self.serialize(link_maps, invalid_urls), status=status.HTTP_201_CREATED)
