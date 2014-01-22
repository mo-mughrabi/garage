# -*- coding: utf-8 -*-
from models import ModelLookup, Car, Image, Lookup, ModelLookUpI18n
from forms import CarAdminForm, ImageInlineForm, CarForm
from django.contrib import admin
from hvad.admin import TranslatableAdmin


class LookupAdmin(TranslatableAdmin):
    model = Lookup
    list_display = ('group', '__unicode__', 'created_at', 'created_by')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super(LookupAdmin, self).save_model(request, obj, form, change)


class ImageInline(admin.TabularInline):
    model = Image
    form = ImageInlineForm


class CarAdmin(admin.ModelAdmin):
    list_filter = ('created_by',)
    readonly_fields = ['created_by', 'model']
    list_display = ['model', 'status', 'condition', 'view_count', 'asking_price', 'created_at', 'created_by']
    date_hierarchy = 'created_at'  # drill down by dates
    exclude = ['updated_by',  'approved_by', 'approved_at',  'model', 'primary_image']

    inlines = [ImageInline, ]
    # form = CarForm

    def lookup_year(self, obj):
        return '%s' % obj.model.year


class ModelLookUpI18nInline(admin.TabularInline):
    model = ModelLookUpI18n
    extra = 1


class ModelLookupAdmin(admin.ModelAdmin):
    list_display = (
        'make', 'model', 'trim', 'year', 'status', 'created_by', 'created_at')
    list_display_links = ('model',)
    search_fields = ('make', 'model')
    inlines = [ModelLookUpI18nInline, ]

admin.site.register(Car, CarAdmin)
admin.site.register(ModelLookup, ModelLookupAdmin)
admin.site.register(Lookup, LookupAdmin)
