from django.contrib import admin

# Register your models here.
from goods.models import Classification, GoodsSPU, Conversion, GoodsPicture, GoodsSKU, Banner, Activity, ActivityZone


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    # 自定义后台
    list_display = ['id', 'classification_name', 'introduction', 'order', 'update_time']
    list_display_links = ['id', 'classification_name', 'introduction']


admin.site.register(Conversion)

admin.site.register(GoodsSPU)


class GalleryInline(admin.TabularInline):
    model = GoodsPicture
    extra = 2



@admin.register(GoodsSKU)
class GoodsSKUAdmin(admin.ModelAdmin):
    list_display = ["id", 'sku_name', 'price', 'conversion', 'tock', 'sale', 'is_on_sale', 'classification']
    list_display_links = ["id", 'sku_name', 'price']

    search_fields = ['sku_name', 'price', 'sale']
    inlines = [
        GalleryInline,
    ]

# 首页管理
admin.site.register(Banner)
admin.site.register(Activity)


@admin.register(ActivityZone)
class ActivityZoneAdmin(admin.ModelAdmin):
    pass