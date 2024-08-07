# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: entities/v1alpha/entities.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1f\x65ntities/v1alpha/entities.proto\x12\x19\x63om.seed.entities.v1alpha\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1bgoogle/protobuf/empty.proto\"\x1e\n\x10GetChangeRequest\x12\n\n\x02id\x18\x01 \x01(\t\">\n\x18GetEntityTimelineRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x16\n\x0einclude_drafts\x18\x02 \x01(\x08\"4\n\x15\x44iscoverEntityRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\"\x18\n\x16\x44iscoverEntityResponse\"\x9b\x01\n\x06\x43hange\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x02 \x01(\t\x12/\n\x0b\x63reate_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0c\n\x04\x64\x65ps\x18\x04 \x03(\t\x12\x10\n\x08\x63hildren\x18\x06 \x03(\t\x12\x12\n\nis_trusted\x18\x05 \x01(\x08\x12\x10\n\x08is_draft\x18\x07 \x01(\x08\"\xc1\x02\n\x0e\x45ntityTimeline\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05owner\x18\x02 \x01(\t\x12G\n\x07\x63hanges\x18\x03 \x03(\x0b\x32\x36.com.seed.entities.v1alpha.EntityTimeline.ChangesEntry\x12\x17\n\x0f\x63hanges_by_time\x18\x04 \x03(\t\x12\r\n\x05roots\x18\x05 \x03(\t\x12\r\n\x05heads\x18\x06 \x03(\t\x12\x41\n\x0f\x61uthor_versions\x18\x07 \x03(\x0b\x32(.com.seed.entities.v1alpha.AuthorVersion\x1aQ\n\x0c\x43hangesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x30\n\x05value\x18\x02 \x01(\x0b\x32!.com.seed.entities.v1alpha.Change:\x02\x38\x01\"q\n\rAuthorVersion\x12\x0e\n\x06\x61uthor\x18\x01 \x01(\t\x12\r\n\x05heads\x18\x02 \x03(\t\x12\x0f\n\x07version\x18\x03 \x01(\t\x12\x30\n\x0cversion_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"2\n\x06\x45ntity\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\r\n\x05owner\x18\x03 \x01(\t\"v\n\rDeletedEntity\x12\n\n\x02id\x18\x01 \x01(\t\x12/\n\x0b\x64\x65lete_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x16\n\x0e\x64\x65leted_reason\x18\x03 \x01(\t\x12\x10\n\x08metadata\x18\x04 \x01(\t\"&\n\x15SearchEntitiesRequest\x12\r\n\x05query\x18\x01 \x01(\t\"f\n\x16SearchEntitiesResponse\x12\x33\n\x08\x65ntities\x18\x01 \x03(\x0b\x32!.com.seed.entities.v1alpha.Entity\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"1\n\x13\x44\x65leteEntityRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06reason\x18\x02 \x01(\t\"C\n\x1aListDeletedEntitiesRequest\x12\x11\n\tpage_size\x18\x01 \x01(\x05\x12\x12\n\npage_token\x18\x02 \x01(\t\"z\n\x1bListDeletedEntitiesResponse\x12\x42\n\x10\x64\x65leted_entities\x18\x01 \x03(\x0b\x32(.com.seed.entities.v1alpha.DeletedEntity\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"#\n\x15UndeleteEntityRequest\x12\n\n\x02id\x18\x01 \x01(\t\"e\n\x19ListEntityMentionsRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x11\n\tpage_size\x18\x02 \x01(\x05\x12\x12\n\npage_token\x18\x03 \x01(\t\x12\x15\n\rreverse_order\x18\x04 \x01(\x08\"k\n\x1aListEntityMentionsResponse\x12\x34\n\x08mentions\x18\x01 \x03(\x0b\x32\".com.seed.entities.v1alpha.Mention\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"\xaa\x02\n\x07Mention\x12\x0e\n\x06source\x18\x01 \x01(\t\x12\x16\n\x0esource_context\x18\x02 \x01(\t\x12@\n\x0bsource_blob\x18\x03 \x01(\x0b\x32+.com.seed.entities.v1alpha.Mention.BlobInfo\x12\x16\n\x0etarget_version\x18\x04 \x01(\t\x12\x18\n\x10is_exact_version\x18\x05 \x01(\x08\x12\x17\n\x0ftarget_fragment\x18\x06 \x01(\t\x1aj\n\x08\x42lobInfo\x12\x0b\n\x03\x63id\x18\x01 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x02 \x01(\t\x12/\n\x0b\x63reate_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x10\n\x08is_draft\x18\x04 \x01(\x08\x32\x89\x07\n\x08\x45ntities\x12[\n\tGetChange\x12+.com.seed.entities.v1alpha.GetChangeRequest\x1a!.com.seed.entities.v1alpha.Change\x12s\n\x11GetEntityTimeline\x12\x33.com.seed.entities.v1alpha.GetEntityTimelineRequest\x1a).com.seed.entities.v1alpha.EntityTimeline\x12u\n\x0e\x44iscoverEntity\x12\x30.com.seed.entities.v1alpha.DiscoverEntityRequest\x1a\x31.com.seed.entities.v1alpha.DiscoverEntityResponse\x12u\n\x0eSearchEntities\x12\x30.com.seed.entities.v1alpha.SearchEntitiesRequest\x1a\x31.com.seed.entities.v1alpha.SearchEntitiesResponse\x12V\n\x0c\x44\x65leteEntity\x12..com.seed.entities.v1alpha.DeleteEntityRequest\x1a\x16.google.protobuf.Empty\x12\x84\x01\n\x13ListDeletedEntities\x12\x35.com.seed.entities.v1alpha.ListDeletedEntitiesRequest\x1a\x36.com.seed.entities.v1alpha.ListDeletedEntitiesResponse\x12Z\n\x0eUndeleteEntity\x12\x30.com.seed.entities.v1alpha.UndeleteEntityRequest\x1a\x16.google.protobuf.Empty\x12\x81\x01\n\x12ListEntityMentions\x12\x34.com.seed.entities.v1alpha.ListEntityMentionsRequest\x1a\x35.com.seed.entities.v1alpha.ListEntityMentionsResponseB1Z/seed/backend/genproto/entities/v1alpha;entitiesb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'entities.v1alpha.entities_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z/seed/backend/genproto/entities/v1alpha;entities'
  _ENTITYTIMELINE_CHANGESENTRY._options = None
  _ENTITYTIMELINE_CHANGESENTRY._serialized_options = b'8\001'
  _GETCHANGEREQUEST._serialized_start=124
  _GETCHANGEREQUEST._serialized_end=154
  _GETENTITYTIMELINEREQUEST._serialized_start=156
  _GETENTITYTIMELINEREQUEST._serialized_end=218
  _DISCOVERENTITYREQUEST._serialized_start=220
  _DISCOVERENTITYREQUEST._serialized_end=272
  _DISCOVERENTITYRESPONSE._serialized_start=274
  _DISCOVERENTITYRESPONSE._serialized_end=298
  _CHANGE._serialized_start=301
  _CHANGE._serialized_end=456
  _ENTITYTIMELINE._serialized_start=459
  _ENTITYTIMELINE._serialized_end=780
  _ENTITYTIMELINE_CHANGESENTRY._serialized_start=699
  _ENTITYTIMELINE_CHANGESENTRY._serialized_end=780
  _AUTHORVERSION._serialized_start=782
  _AUTHORVERSION._serialized_end=895
  _ENTITY._serialized_start=897
  _ENTITY._serialized_end=947
  _DELETEDENTITY._serialized_start=949
  _DELETEDENTITY._serialized_end=1067
  _SEARCHENTITIESREQUEST._serialized_start=1069
  _SEARCHENTITIESREQUEST._serialized_end=1107
  _SEARCHENTITIESRESPONSE._serialized_start=1109
  _SEARCHENTITIESRESPONSE._serialized_end=1211
  _DELETEENTITYREQUEST._serialized_start=1213
  _DELETEENTITYREQUEST._serialized_end=1262
  _LISTDELETEDENTITIESREQUEST._serialized_start=1264
  _LISTDELETEDENTITIESREQUEST._serialized_end=1331
  _LISTDELETEDENTITIESRESPONSE._serialized_start=1333
  _LISTDELETEDENTITIESRESPONSE._serialized_end=1455
  _UNDELETEENTITYREQUEST._serialized_start=1457
  _UNDELETEENTITYREQUEST._serialized_end=1492
  _LISTENTITYMENTIONSREQUEST._serialized_start=1494
  _LISTENTITYMENTIONSREQUEST._serialized_end=1595
  _LISTENTITYMENTIONSRESPONSE._serialized_start=1597
  _LISTENTITYMENTIONSRESPONSE._serialized_end=1704
  _MENTION._serialized_start=1707
  _MENTION._serialized_end=2005
  _MENTION_BLOBINFO._serialized_start=1899
  _MENTION_BLOBINFO._serialized_end=2005
  _ENTITIES._serialized_start=2008
  _ENTITIES._serialized_end=2913
# @@protoc_insertion_point(module_scope)
