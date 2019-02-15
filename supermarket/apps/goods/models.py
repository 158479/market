from django.db import models

# Create your models here.
from db.base_model import BaseModel
from ckeditor_uploader.fields import RichTextUploadingField


# 商品分类表
class Classification(BaseModel):
    classification_name = models.CharField(max_length=100,
                                           verbose_name='分类名')
    introduction = models.TextField(null=True,
                                    blank=True,
                                    verbose_name='简介')
    order = models.SmallIntegerField(default=0,
                                     verbose_name="排序")

    def __str__(self):
        return self.classification_name

    class Meta:
        verbose_name = '商品分类管理'
        verbose_name_plural = verbose_name


# 商品单位表
class Conversion(BaseModel):
    conversion_name = models.CharField(max_length=100, verbose_name='单位名')

    def __str__(self):
        return self.conversion_name

    class Meta:
        verbose_name = '商品单位管理'
        verbose_name_plural = verbose_name


# 商品SKU表
class GoodsSKU(BaseModel):
    is_on_sale_choices = (
        (False, "下架"),
        (True, "上架"),
    )
    sku_name = models.CharField(max_length=150,
                                verbose_name='商品SKU名')
    introduce = models.TextField(null=True,
                                 blank=True,
                                 verbose_name='简介')
    price = models.DecimalField(max_digits=9,
                                decimal_places=2,
                                default=0,
                                verbose_name='价格')
    conversion = models.ForeignKey(to='Conversion',
                                   verbose_name='单位')
    tock = models.CharField(max_length=150,
                            default=0,
                            verbose_name='库存')
    sale = models.CharField(max_length=160,
                            default=0,
                            verbose_name='销量')
    logo = models.ImageField(upload_to='goods/%Y%m%d',
                             verbose_name='封面图片')
    is_on_sale = models.BooleanField(verbose_name="是否上架",
                                     choices=is_on_sale_choices,
                                     default=False)
    classification = models.ForeignKey(to='Classification',
                                       verbose_name='商品分类')
    goods_spu = models.ForeignKey(to='GoodsSPU',
                                  verbose_name='商品SPU')

    def __str__(self):
        return self.sku_name

    class Meta:
        verbose_name = '商品SKU管理'
        verbose_name_plural = verbose_name


# 商品SPU表
class GoodsSPU(BaseModel):
    spu_name = models.CharField(max_length=100,
                                verbose_name='商品SPU名')
    details = RichTextUploadingField(verbose_name='详情')

    def __str__(self):
        return self.spu_name

    class Meta:
        verbose_name = '商品SPU管理'
        verbose_name_plural = verbose_name


# 商品图片表
class GoodsPicture(BaseModel):
    picture_address = models.ImageField(verbose_name='相册图片地址',
                                        upload_to='goods_gallery/%Y%m/%d')
    commodity = models.ForeignKey(to='GoodsSKU',
                                  verbose_name='商品SKU')

    def __str__(self):
        return "商品相册:{}".format(self.picture_address.name)

    class Meta:
        verbose_name = '商品图片管理'
        verbose_name_plural = verbose_name


# 首页轮播
class Banner(BaseModel):
    name = models.CharField(verbose_name="轮播活动名",
                            max_length=150,
                            )
    img_url = models.ImageField(verbose_name='轮播图片地址',
                                upload_to='banner/%Y%m/%d'
                                )
    order = models.SmallIntegerField(verbose_name="排序",
                                     default=0,
                                     )

    goods_sku = models.ForeignKey(to="GoodsSKU", verbose_name="商品SKU")

    class Meta:
        verbose_name = "轮播管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 首页活动
class Activity(BaseModel):
    title = models.CharField(verbose_name='活动名称', max_length=150)
    img_url = models.ImageField(verbose_name='活动图片地址',
                                upload_to='activity/%Y%m/%d'
                                )
    url_site = models.URLField(verbose_name='活动的url地址', max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "活动管理"
        verbose_name_plural = verbose_name


# 首页活动专区
class ActivityZone(BaseModel):
    is_on_sale_choices = (
        (False, "下架"),
        (True, "上架"),
    )
    title = models.CharField(verbose_name='活动专区名称', max_length=150)
    brief = models.CharField(verbose_name="活动专区的简介",
                             max_length=200,
                             null=True,
                             blank=True,
                             )
    order = models.SmallIntegerField(verbose_name="排序",
                                     default=0,
                                     )
    is_on_sale = models.BooleanField(verbose_name="上否上线",
                                     choices=is_on_sale_choices,
                                     default=0,
                                     )
    goods_sku = models.ManyToManyField(to="GoodsSKU", verbose_name="商品")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "活动专区管理"
        verbose_name_plural = verbose_name
