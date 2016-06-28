#coding: utf-8
from django.db import models

CLOUD_TYPES = (u"金山云", u"腾讯云", u"木犀园", u"阿里云")
PJNAME_TYPES = (u"天龙3D", u"仙剑五", u"风云", u"仙剑五卡牌", u"苍之骑士团", u"大大大乱斗")

class Pj_host(models.Model):
    idc_type = models.CharField(u"机房", max_length=40, choices=((i, i) for i in CLOUD_TYPES), default=u'金山云')
    #op_addr = models.IPAddressField(u"公网IP(多个IP用","分割)")
    op_addr = models.TextField(u"公网IP", max_length=255, default=u'多个IP用\",\"分割')
    pj_led = models.CharField(u"负责人", max_length=40, default=u'洪珑玮')
    pj_name = models.CharField(u"所属项目", max_length=40, choices=((i, i) for i in PJNAME_TYPES), default=u'天龙3D')
    pj_cmd = models.CharField(u"需要执行的命令", max_length=100, blank=True, null=True)
    pj_disk = models.CharField(u"分区盘符", max_length=100, blank=True, null=True)
    pj_status = models.CharField(u"备注", max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.idc_type

    class Meta:
        verbose_name = u"主机管理"
        verbose_name_plural = verbose_name
