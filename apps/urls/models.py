from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.utils.transfer_url import get_code
from apps.urls.managers import LinkMapManager, AccessLogManager
from apps.utils.redis.client import redis_cli


class LinkMap(models.Model):
    """
    长网址与短码的映射
    """
    id = models.BigAutoField(primary_key=True)
    url = models.URLField("长网址", max_length=255)
    code = models.CharField("短码", max_length=7, null=True, blank=True, db_index=True)
    hit_count = models.IntegerField("打开次数", default=0)
    init_access_at = models.DateTimeField("初次访问时间", null=True, blank=True)
    created_by = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE, verbose_name="创建人")
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    objects = LinkMapManager()

    def save_code(self):
        self.code = get_code(self.id)
        self.save()
        # 将生成的短码写入过滤器中
        redis_cli.set_bloom(self.code)

    class Meta:
        db_table = "link_map"
        verbose_name = "网址映射"
        verbose_name_plural = verbose_name


@receiver(post_save, sender=LinkMap)
def create_map_cache(sender, instance=None, created=False, **kwargs):
    """
    当LinkMap`写入`时，先保存长网址的短码，再将长网址与对应短码写入redis缓存
    """
    if created:
        instance.save_code()
        redis_cli.set_data(instance.code, instance.url)


class AccessLogs(models.Model):
    """
    访问日志
    """
    code = models.CharField("短码", max_length=16, db_index=True)
    ip = models.GenericIPAddressField("访客IP")
    country = models.CharField("国家", max_length=64, null=True, blank=True)
    province = models.CharField("省份", max_length=64, null=True, blank=True)
    city = models.CharField("城市", max_length=64, null=True, blank=True)
    isp = models.CharField("运营商", max_length=64, null=True, blank=True)
    browser_name = models.CharField("浏览器名称", max_length=128, null=True, blank=True)
    os_name = models.CharField("操作系统名称", max_length=128, null=True, blank=True)
    device = models.CharField("设备名称", max_length=128, null=True, blank=True)
    is_mobile = models.NullBooleanField("是否手机")
    is_pc = models.NullBooleanField("是否电脑")
    is_bot = models.NullBooleanField("是否机器人")
    created_at = models.DateTimeField("访问时间", auto_now_add=True)

    objects = AccessLogManager()

    class Meta:
        db_table = "access_logs"
        verbose_name = "访问日志"
        verbose_name_plural = verbose_name
