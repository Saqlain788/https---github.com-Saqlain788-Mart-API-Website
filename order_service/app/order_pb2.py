# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: order.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0border.proto\x12\x05order\"R\n\tOrderItem\x12\x10\n\x08order_id\x18\x01 \x01(\x05\x12\x12\n\nproduct_id\x18\x02 \x01(\x05\x12\x10\n\x08quantity\x18\x03 \x01(\x05\x12\r\n\x05price\x18\x04 \x01(\x02\"\x92\x01\n\x05Order\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0f\n\x07user_id\x18\x02 \x01(\x05\x12\x13\n\x0btotal_price\x18\x03 \x01(\x02\x12\x0e\n\x06status\x18\x04 \x01(\t\x12\x12\n\ncreated_at\x18\x05 \x01(\t\x12\x12\n\nupdated_at\x18\x06 \x01(\t\x12\x1f\n\x05items\x18\x07 \x03(\x0b\x32\x10.order.OrderItem\")\n\tOrderList\x12\x1c\n\x06orders\x18\x01 \x03(\x0b\x32\x0c.order.Orderb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'order_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ORDERITEM._serialized_start=22
  _ORDERITEM._serialized_end=104
  _ORDER._serialized_start=107
  _ORDER._serialized_end=253
  _ORDERLIST._serialized_start=255
  _ORDERLIST._serialized_end=296
# @@protoc_insertion_point(module_scope)
