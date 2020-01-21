from enum import Enum

class FromType(Enum):
    youku = 'youku'
    custom = 'custom'
    bilibili = 'bilibili'


FromType.youku.label = '优酷'
FromType.custom.label = '自制'
FromType.bilibili.label = 'B站'

print(FromType('custom'))