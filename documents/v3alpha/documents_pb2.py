# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: documents/v3alpha/documents.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!documents/v3alpha/documents.proto\x12\x1a\x63om.seed.documents.v3alpha\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1bgoogle/protobuf/empty.proto\"D\n\x12GetDocumentRequest\x12\x0f\n\x07\x61\x63\x63ount\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t\"\x93\x01\n\x1b\x43reateDocumentChangeRequest\x12\x0f\n\x07\x61\x63\x63ount\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12;\n\x07\x63hanges\x18\x03 \x03(\x0b\x32*.com.seed.documents.v3alpha.DocumentChange\x12\x18\n\x10signing_key_name\x18\x04 \x01(\t\"6\n\x15\x44\x65leteDocumentRequest\x12\x0f\n\x07\x61\x63\x63ount\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\"A\n\x18ListRootDocumentsRequest\x12\x11\n\tpage_size\x18\x01 \x01(\x05\x12\x12\n\npage_token\x18\x02 \x01(\t\"u\n\x19ListRootDocumentsResponse\x12?\n\tdocuments\x18\x01 \x03(\x0b\x32,.com.seed.documents.v3alpha.DocumentListItem\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"N\n\x14ListDocumentsRequest\x12\x0f\n\x07\x61\x63\x63ount\x18\x01 \x01(\t\x12\x11\n\tpage_size\x18\x02 \x01(\x05\x12\x12\n\npage_token\x18\x03 \x01(\t\"q\n\x15ListDocumentsResponse\x12?\n\tdocuments\x18\x01 \x03(\x0b\x32,.com.seed.documents.v3alpha.DocumentListItem\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"\xb4\x02\n\x10\x44ocumentListItem\x12\x0f\n\x07\x61\x63\x63ount\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12L\n\x08metadata\x18\x03 \x03(\x0b\x32:.com.seed.documents.v3alpha.DocumentListItem.MetadataEntry\x12\x0f\n\x07\x61uthors\x18\x04 \x03(\t\x12/\n\x0b\x63reate_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0bupdate_time\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0f\n\x07version\x18\x08 \x01(\t\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xf6\x02\n\x08\x44ocument\x12\x0f\n\x07\x61\x63\x63ount\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x44\n\x08metadata\x18\x03 \x03(\x0b\x32\x32.com.seed.documents.v3alpha.Document.MetadataEntry\x12\x0f\n\x07\x61uthors\x18\x05 \x03(\t\x12\x36\n\x07\x63ontent\x18\x06 \x03(\x0b\x32%.com.seed.documents.v3alpha.BlockNode\x12/\n\x0b\x63reate_time\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0bupdate_time\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0f\n\x07version\x18\t \x01(\t\x12\x18\n\x10previous_version\x18\n \x01(\t\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"v\n\tBlockNode\x12\x30\n\x05\x62lock\x18\x01 \x01(\x0b\x32!.com.seed.documents.v3alpha.Block\x12\x37\n\x08\x63hildren\x18\x02 \x03(\x0b\x32%.com.seed.documents.v3alpha.BlockNode\"\x85\x02\n\x05\x42lock\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x0c\n\x04text\x18\x03 \x01(\t\x12\x0b\n\x03ref\x18\x07 \x01(\t\x12\x45\n\nattributes\x18\x04 \x03(\x0b\x32\x31.com.seed.documents.v3alpha.Block.AttributesEntry\x12;\n\x0b\x61nnotations\x18\x05 \x03(\x0b\x32&.com.seed.documents.v3alpha.Annotation\x12\x10\n\x08revision\x18\x06 \x01(\t\x1a\x31\n\x0f\x41ttributesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xc4\x01\n\nAnnotation\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x0b\n\x03ref\x18\x05 \x01(\t\x12J\n\nattributes\x18\x02 \x03(\x0b\x32\x36.com.seed.documents.v3alpha.Annotation.AttributesEntry\x12\x0e\n\x06starts\x18\x03 \x03(\x05\x12\x0c\n\x04\x65nds\x18\x04 \x03(\x05\x1a\x31\n\x0f\x41ttributesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xf6\x02\n\x0e\x44ocumentChange\x12N\n\x0cset_metadata\x18\x01 \x01(\x0b\x32\x36.com.seed.documents.v3alpha.DocumentChange.SetMetadataH\x00\x12J\n\nmove_block\x18\x02 \x01(\x0b\x32\x34.com.seed.documents.v3alpha.DocumentChange.MoveBlockH\x00\x12:\n\rreplace_block\x18\x03 \x01(\x0b\x32!.com.seed.documents.v3alpha.BlockH\x00\x12\x16\n\x0c\x64\x65lete_block\x18\x04 \x01(\tH\x00\x1a\x43\n\tMoveBlock\x12\x10\n\x08\x62lock_id\x18\x01 \x01(\t\x12\x0e\n\x06parent\x18\x02 \x01(\t\x12\x14\n\x0cleft_sibling\x18\x03 \x01(\t\x1a)\n\x0bSetMetadata\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\tB\x04\n\x02op2\xbd\x04\n\tDocuments\x12\x63\n\x0bGetDocument\x12..com.seed.documents.v3alpha.GetDocumentRequest\x1a$.com.seed.documents.v3alpha.Document\x12u\n\x14\x43reateDocumentChange\x12\x37.com.seed.documents.v3alpha.CreateDocumentChangeRequest\x1a$.com.seed.documents.v3alpha.Document\x12[\n\x0e\x44\x65leteDocument\x12\x31.com.seed.documents.v3alpha.DeleteDocumentRequest\x1a\x16.google.protobuf.Empty\x12t\n\rListDocuments\x12\x30.com.seed.documents.v3alpha.ListDocumentsRequest\x1a\x31.com.seed.documents.v3alpha.ListDocumentsResponse\x12\x80\x01\n\x11ListRootDocuments\x12\x34.com.seed.documents.v3alpha.ListRootDocumentsRequest\x1a\x35.com.seed.documents.v3alpha.ListRootDocumentsResponseB3Z1seed/backend/genproto/documents/v3alpha;documentsb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'documents.v3alpha.documents_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z1seed/backend/genproto/documents/v3alpha;documents'
  _DOCUMENTLISTITEM_METADATAENTRY._options = None
  _DOCUMENTLISTITEM_METADATAENTRY._serialized_options = b'8\001'
  _DOCUMENT_METADATAENTRY._options = None
  _DOCUMENT_METADATAENTRY._serialized_options = b'8\001'
  _BLOCK_ATTRIBUTESENTRY._options = None
  _BLOCK_ATTRIBUTESENTRY._serialized_options = b'8\001'
  _ANNOTATION_ATTRIBUTESENTRY._options = None
  _ANNOTATION_ATTRIBUTESENTRY._serialized_options = b'8\001'
  _GETDOCUMENTREQUEST._serialized_start=127
  _GETDOCUMENTREQUEST._serialized_end=195
  _CREATEDOCUMENTCHANGEREQUEST._serialized_start=198
  _CREATEDOCUMENTCHANGEREQUEST._serialized_end=345
  _DELETEDOCUMENTREQUEST._serialized_start=347
  _DELETEDOCUMENTREQUEST._serialized_end=401
  _LISTROOTDOCUMENTSREQUEST._serialized_start=403
  _LISTROOTDOCUMENTSREQUEST._serialized_end=468
  _LISTROOTDOCUMENTSRESPONSE._serialized_start=470
  _LISTROOTDOCUMENTSRESPONSE._serialized_end=587
  _LISTDOCUMENTSREQUEST._serialized_start=589
  _LISTDOCUMENTSREQUEST._serialized_end=667
  _LISTDOCUMENTSRESPONSE._serialized_start=669
  _LISTDOCUMENTSRESPONSE._serialized_end=782
  _DOCUMENTLISTITEM._serialized_start=785
  _DOCUMENTLISTITEM._serialized_end=1093
  _DOCUMENTLISTITEM_METADATAENTRY._serialized_start=1046
  _DOCUMENTLISTITEM_METADATAENTRY._serialized_end=1093
  _DOCUMENT._serialized_start=1096
  _DOCUMENT._serialized_end=1470
  _DOCUMENT_METADATAENTRY._serialized_start=1046
  _DOCUMENT_METADATAENTRY._serialized_end=1093
  _BLOCKNODE._serialized_start=1472
  _BLOCKNODE._serialized_end=1590
  _BLOCK._serialized_start=1593
  _BLOCK._serialized_end=1854
  _BLOCK_ATTRIBUTESENTRY._serialized_start=1805
  _BLOCK_ATTRIBUTESENTRY._serialized_end=1854
  _ANNOTATION._serialized_start=1857
  _ANNOTATION._serialized_end=2053
  _ANNOTATION_ATTRIBUTESENTRY._serialized_start=1805
  _ANNOTATION_ATTRIBUTESENTRY._serialized_end=1854
  _DOCUMENTCHANGE._serialized_start=2056
  _DOCUMENTCHANGE._serialized_end=2430
  _DOCUMENTCHANGE_MOVEBLOCK._serialized_start=2314
  _DOCUMENTCHANGE_MOVEBLOCK._serialized_end=2381
  _DOCUMENTCHANGE_SETMETADATA._serialized_start=2383
  _DOCUMENTCHANGE_SETMETADATA._serialized_end=2424
  _DOCUMENTS._serialized_start=2433
  _DOCUMENTS._serialized_end=3006
# @@protoc_insertion_point(module_scope)