# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: documents/v1alpha/changes.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1f\x64ocuments/v1alpha/changes.proto\x12\x1d\x63om.mintter.documents.v1alpha\x1a\x1fgoogle/protobuf/timestamp.proto\"\"\n\x14GetChangeInfoRequest\x12\n\n\x02id\x18\x01 \x01(\t\"N\n\x12ListChangesRequest\x12\x11\n\tobject_id\x18\x01 \x01(\t\x12\x11\n\tpage_size\x18\x02 \x01(\x05\x12\x12\n\npage_token\x18\x03 \x01(\t\"j\n\x13ListChangesResponse\x12:\n\x07\x63hanges\x18\x01 \x03(\x0b\x32).com.mintter.documents.v1alpha.ChangeInfo\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"Y\n\nChangeInfo\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x02 \x01(\t\x12/\n\x0b\x63reate_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp2\xf0\x01\n\x07\x43hanges\x12o\n\rGetChangeInfo\x12\x33.com.mintter.documents.v1alpha.GetChangeInfoRequest\x1a).com.mintter.documents.v1alpha.ChangeInfo\x12t\n\x0bListChanges\x12\x31.com.mintter.documents.v1alpha.ListChangesRequest\x1a\x32.com.mintter.documents.v1alpha.ListChangesResponseB6Z4mintter/backend/genproto/documents/v1alpha;documentsb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'documents.v1alpha.changes_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z4mintter/backend/genproto/documents/v1alpha;documents'
  _GETCHANGEINFOREQUEST._serialized_start=99
  _GETCHANGEINFOREQUEST._serialized_end=133
  _LISTCHANGESREQUEST._serialized_start=135
  _LISTCHANGESREQUEST._serialized_end=213
  _LISTCHANGESRESPONSE._serialized_start=215
  _LISTCHANGESRESPONSE._serialized_end=321
  _CHANGEINFO._serialized_start=323
  _CHANGEINFO._serialized_end=412
  _CHANGES._serialized_start=415
  _CHANGES._serialized_end=655
# @@protoc_insertion_point(module_scope)
