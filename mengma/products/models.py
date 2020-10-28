from peewee import *
from datetime import datetime


db = PostgresqlDatabase("spider", user="suthree", host="localhost", password="Password")


class BaseModel(Model):
    """model 基类

    Arguments:
        Model {[type]} -- [description]
    """

    state = IntegerField(default=1, verbose_name="是否有效")
    is_valid = BooleanField(default=True, verbose_name="是否为有效数据")
    created_at = DateTimeField(default=datetime.now(), verbose_name="创建时间")
    updated_at = DateTimeField(default=datetime.now(), verbose_name="更新时间")


class VirtualForeignKey(ForeignKeyField):
    on_delete = False
    on_update = False
    deferrable = False


class Region(BaseModel):
    """
    region model

    Arguments:
        BaseModel {[type]} -- [description]
    """

    name = CharField(max_length=32, verbose_name="区域名称")
    parent = IntegerField(verbose_name="父级id")
    province = IntegerField(verbose_name="省级id")


class Brand(BaseModel):
    """门店品牌

    Arguments:
        BaseModel {[type]} -- [description]
    """

    name = CharField(max_length=32, verbose_name="品牌名")
    name_cn = CharField(max_length=32, verbose_name="品牌名")
    code = CharField(max_length=32, unique=True, verbose_name="爬虫平台唯一代号")
    platform = CharField(max_length=32, null=False, verbose_name="爬虫平台")


class Store(BaseModel):
    """门店

    Arguments:
        BaseModel {[type]} -- [description]
    """

    name = CharField(max_length=32, verbose_name="门店名")
    brand = VirtualForeignKey(Brand, verbose_name="品牌")
    region = VirtualForeignKey(Region, verbose_name="区域")
    code = CharField(max_length=32, verbose_name="第三方平台id")
    address = CharField(max_length=255, verbose_name="地址")
    phone = CharField(max_length=32, erbose_name="联系方式")
    desc = CharField(max_length=32, erbose_name="门店介绍")
    longitude = CharField(max_length=32, erbose_name="经度")
    longitude = CharField(max_length=32, erbose_name="维度")


class Task(BaseModel):
    """任务

    Arguments:
        BaseModel {[type]} -- [description]
    """

    name = CharField(max_length=32, verbose_name="任务名")
    store = VirtualForeignKey(Store, verbose_name="任务执行门店")


class Product(BaseModel):
    """产品详细信息

    Arguments:
        BaseModel {[type]} -- [description]
    """

    task = VirtualForeignKey(Task, verbose_name="任务执行id")
    store = VirtualForeignKey(Store, verbose_name="任务执行门店")
    name = CharField(max_length=32, verbose_name="商品名")
    desc = CharField(max_length=64, verbose_name="商品描述")
    barcode = CharField(max_length=16, verbose_name="商品标准条码")
    code = CharField(max_length=16, verbose_name="商品所在平台的id")
    category = CharField(max_length=32, verbose_name="分类")
    cate_id = CharField(max_lenght=32, verbose_name="分类id")
    spec = CharField(max_length=16, verbose_name="规格")
    unit = CharField(max_length=16, verbose_name="单位")
    price = CharField(max_length=16, verbose_name="现价")
    price_origin = CharField(max_length=16, verbose_name="原价")
    price_detail = TextField(verbose_name="价格详情")
    sales = CharField(max_length=16, verbose_name="销量")
    stock = CharField(max_length=16, verbose_name="库存")


class Promotion(BaseModel):
    """商品促销信息

    Arguments:
        BaseModel {[type]} -- [description]
    """

    product = VirtualForeignKey(Product)
    name = CharField(max_length=32, verbose_name="促销名")
    desc = CharField(max_length=32, verbose_name="促销详情")
    condition = CharField()
    discount = CharField()
    form = CharField(verbose_name="促销类型")
    detail = TextField()
    start_time = DateTimeField()
    end_time = DateTimeField()


class ProductMap:
    """产品映射表：
            一对一
            一对多
    """

    brand = IntegerField()
    store = IntegerField()
    name = CharField()
    barcode = CharField()
    code = CharField
