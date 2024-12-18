# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: payments/v1alpha/invoices.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fpayments/v1alpha/invoices.proto\x12\x19\x63om.seed.payments.v1alpha\x1a\x1bgoogle/protobuf/empty.proto\"7\n\x0fInvoiceResponse\x12\x0e\n\x06payreq\x18\x01 \x01(\t\x12\x14\n\x0cpayment_hash\x18\x02 \x01(\t\"&\n\x14\x44\x65\x63odeInvoiceRequest\x12\x0e\n\x06payreq\x18\x01 \x01(\t\"Q\n\x14\x43reateInvoiceRequest\x12\x0f\n\x07\x61\x63\x63ount\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0e\n\x06\x61mount\x18\x03 \x01(\x03\x12\x0c\n\x04memo\x18\x04 \x01(\t\"P\n\x11PayInvoiceRequest\x12\x0e\n\x06payreq\x18\x01 \x01(\t\x12\x0f\n\x07\x61\x63\x63ount\x18\x02 \x01(\t\x12\n\n\x02id\x18\x03 \x01(\t\x12\x0e\n\x06\x61mount\x18\x04 \x01(\x03\"T\n\x19RequestLud6InvoiceRequest\x12\x0b\n\x03URL\x18\x01 \x01(\t\x12\x0c\n\x04user\x18\x02 \x01(\t\x12\x0e\n\x06\x61mount\x18\x03 \x01(\x03\x12\x0c\n\x04memo\x18\x04 \x01(\t\"!\n\x13GetLnAddressRequest\x12\n\n\x02id\x18\x01 \x01(\t\"\x1c\n\tLNAddress\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\"6\n\x16UpdateLNAddressRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08nickname\x18\x02 \x01(\t\"!\n\x13ListInvoicesRequest\x12\n\n\x02id\x18\x01 \x01(\t\"\xb2\x02\n\x07Invoice\x12\x14\n\x0cpayment_hash\x18\x01 \x01(\t\x12\x17\n\x0fpayment_request\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x18\n\x10\x64\x65scription_hash\x18\x04 \x01(\t\x12\x18\n\x10payment_preimage\x18\x05 \x01(\t\x12\x13\n\x0b\x64\x65stination\x18\x06 \x01(\t\x12\x0e\n\x06\x61mount\x18\x07 \x01(\x03\x12\x0b\n\x03\x66\x65\x65\x18\x08 \x01(\x03\x12\x0e\n\x06status\x18\t \x01(\t\x12\x0c\n\x04type\x18\n \x01(\t\x12\x15\n\rerror_message\x18\x0b \x01(\t\x12\x12\n\nsettled_at\x18\x0c \x01(\t\x12\x12\n\nexpires_at\x18\r \x01(\t\x12\x0f\n\x07is_paid\x18\x0e \x01(\x08\x12\x0f\n\x07keysend\x18\x0f \x01(\x08\"L\n\x14ListInvoicesResponse\x12\x34\n\x08invoices\x18\x01 \x03(\x0b\x32\".com.seed.payments.v1alpha.Invoice2\xa0\x04\n\x08Invoices\x12l\n\rCreateInvoice\x12/.com.seed.payments.v1alpha.CreateInvoiceRequest\x1a*.com.seed.payments.v1alpha.InvoiceResponse\x12R\n\nPayInvoice\x12,.com.seed.payments.v1alpha.PayInvoiceRequest\x1a\x16.google.protobuf.Empty\x12s\n\x10ListPaidInvoices\x12..com.seed.payments.v1alpha.ListInvoicesRequest\x1a/.com.seed.payments.v1alpha.ListInvoicesResponse\x12\x64\n\rDecodeInvoice\x12/.com.seed.payments.v1alpha.DecodeInvoiceRequest\x1a\".com.seed.payments.v1alpha.Invoice\x12w\n\x14ListReceivedInvoices\x12..com.seed.payments.v1alpha.ListInvoicesRequest\x1a/.com.seed.payments.v1alpha.ListInvoicesResponse2\xd1\x02\n\x05LNURL\x12v\n\x12RequestLud6Invoice\x12\x34.com.seed.payments.v1alpha.RequestLud6InvoiceRequest\x1a*.com.seed.payments.v1alpha.InvoiceResponse\x12\x64\n\x0cGetLnAddress\x12..com.seed.payments.v1alpha.GetLnAddressRequest\x1a$.com.seed.payments.v1alpha.LNAddress\x12j\n\x0fUpdateLNAddress\x12\x31.com.seed.payments.v1alpha.UpdateLNAddressRequest\x1a$.com.seed.payments.v1alpha.LNAddressB1Z/seed/backend/genproto/payments/v1alpha;paymentsb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'payments.v1alpha.invoices_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z/seed/backend/genproto/payments/v1alpha;payments'
  _INVOICERESPONSE._serialized_start=91
  _INVOICERESPONSE._serialized_end=146
  _DECODEINVOICEREQUEST._serialized_start=148
  _DECODEINVOICEREQUEST._serialized_end=186
  _CREATEINVOICEREQUEST._serialized_start=188
  _CREATEINVOICEREQUEST._serialized_end=269
  _PAYINVOICEREQUEST._serialized_start=271
  _PAYINVOICEREQUEST._serialized_end=351
  _REQUESTLUD6INVOICEREQUEST._serialized_start=353
  _REQUESTLUD6INVOICEREQUEST._serialized_end=437
  _GETLNADDRESSREQUEST._serialized_start=439
  _GETLNADDRESSREQUEST._serialized_end=472
  _LNADDRESS._serialized_start=474
  _LNADDRESS._serialized_end=502
  _UPDATELNADDRESSREQUEST._serialized_start=504
  _UPDATELNADDRESSREQUEST._serialized_end=558
  _LISTINVOICESREQUEST._serialized_start=560
  _LISTINVOICESREQUEST._serialized_end=593
  _INVOICE._serialized_start=596
  _INVOICE._serialized_end=902
  _LISTINVOICESRESPONSE._serialized_start=904
  _LISTINVOICESRESPONSE._serialized_end=980
  _INVOICES._serialized_start=983
  _INVOICES._serialized_end=1527
  _LNURL._serialized_start=1530
  _LNURL._serialized_end=1867
# @@protoc_insertion_point(module_scope)
