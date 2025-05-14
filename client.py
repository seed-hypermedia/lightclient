#!/usr/bin/env python3
from daemon.v1alpha import daemon_pb2, daemon_pb2_grpc
from networking.v1alpha import networking_pb2, networking_pb2_grpc
from documents.v1alpha import documents_pb2, documents_pb2_grpc
from documents.v3alpha import documents_pb2 as documents_v3_pb2
from documents.v3alpha import documents_pb2_grpc as documents_v3_pb2_grpc 
from payments.v1alpha import wallets_pb2, invoices_pb2
from payments.v1alpha import wallets_pb2_grpc, invoices_pb2_grpc
from p2p.v1alpha import p2p_pb2, p2p_pb2_grpc
from entities.v1alpha import entities_pb2, entities_pb2_grpc
from activity.v1alpha import activity_pb2, activity_pb2_grpc, subscriptions_pb2, subscriptions_pb2_grpc
from accounts.v1alpha import accounts_pb2, accounts_pb2_grpc
from groups.v1alpha import groups_pb2, groups_pb2_grpc, website_pb2, website_pb2_grpc
from datetime import datetime
import requests

import re
import json
import grpc
import argparse
import sys
import time
import random
import string

class client():
    def __init__(self, server="localhost:55002"):
        # Initialize the gRPC client with various service stubs
        options = [('grpc.max_receive_message_length', 100 * 1024 * 1024),
                   ('grpc.max_send_message_length', 100 * 1024 * 1024)]
        self.__channel = grpc.insecure_channel(server, options=options)
        self._daemon = daemon_pb2_grpc.DaemonStub(self.__channel)
        self._p2p = p2p_pb2_grpc.P2PStub(self.__channel)
        self._networking = networking_pb2_grpc.NetworkingStub(self.__channel)
        self._entities = entities_pb2_grpc.EntitiesStub(self.__channel)
        self._activity = activity_pb2_grpc.ActivityFeedStub(self.__channel)
        self._subscriptions = subscriptions_pb2_grpc.SubscriptionsStub(self.__channel)
        self._accounts = accounts_pb2_grpc.AccountsStub(self.__channel)
        self._documents = documents_v3_pb2_grpc.DocumentsStub(self.__channel)
        self._publications = documents_pb2_grpc.PublicationsStub(self.__channel)
        self._drafts = documents_pb2_grpc.DraftsStub(self.__channel)
        self._website = website_pb2_grpc.WebsiteStub(self.__channel)
        self._groups = groups_pb2_grpc.GroupsStub(self.__channel)
        self._wallets = wallets_pb2_grpc.WalletsStub(self.__channel)
        self._invoices = invoices_pb2_grpc.InvoicesStub(self.__channel)
        split_server=server.split(":")
        self._port = int(split_server[1])
        self._host = str(split_server[0])

    def get_port(self):
        # Return the port number of the server
        return self._port
    def get_host(self):
        # Return the host address of the server
        return self._host
    def __del__(self):
        # Close the gRPC channel when the client is deleted
        self.__channel.close()
    def _role_to_str(self, role):
        # Convert role integer to string representation
        if role == 2:
            return "editor"
        elif role==1:
            return "owner"
        else:
            return "unspecified"

    def _str_to_role(self, role):
        # Convert role string to integer representation
        if "editor" in role.lower():
            return 2
        elif "owner" in role.lower():
            return 1
        else:
            return 0
    def _status2string(self, status):
        # Convert status integer to string representation
        if status == 0:
            return "NOT_CONNECTED"
        elif status == 1:
            return "CONNECTED"
        elif status == 2:
            return "CAN_CONNECT"
        elif status == 3:
            return "CANNOT_CONNECT"
        elif status == 4:
            return "LIMITED"
        else:
            return "UNKNOWN"
    def _trim(self, string, length=24, trim_ending=True):
        # Trim a string to a specified length, optionally adding ellipsis
        if len(string) <= length or length < 3:
            return string
        else:
            if trim_ending:
                return string[:length-3] + '...'
            else:
                return '...' + string[-length+3:]

    def _upload_file(self, path):
        # Upload a file to the server and return the response text
        port = self.get_port()
        host = self.get_host()
        if "http" not in host:
            host = "http://"+host
        url= host+":"+str(port-1)+"/ipfs/file-upload"
        res = requests.post(url, files={'file': open(path,'rb')})
        if res.status_code <200 or res.status_code >299:
            raise ValueError("Could not upload file ["+str(res.status_code)+"]: "+res.reason)
        return res.text

    # Sites
    def init_site(self, secret_link, group_eid):   
        # Initialize the server to become a website for a specific group
        try:
            res = self._website.InitializeServer(website_pb2.InitializeServerRequest(secret=secret_link, group_id=group_eid))
        except Exception as e:
            print("init_site error: "+str(e))
            return
        print(res.id)

    def site_info(self):   
        # Get public information about the website
        try:
            res = self._website.GetSiteInfo(website_pb2.GetSiteInfoRequest())
        except Exception as e:
            print("init_site error: "+str(e))
            return
        print("Group EID :"+str(res.group_id))
        print("Group Version :"+str(res.group_version))
        print("Site PeerID:"+str(res.peer_info.peer_id))
        print("Site Address :"+str(res.peer_info.addrs))

    # Activity 
    def get_feed(self, page_size=30, page_token="", trusted_only=False, accounts = [], event_types=[], resources=[], links=[]):   
        # Retrieve the activity feed with various filters
        try:
            start = time.time()
            res = self._activity.ListEvents(activity_pb2.ListEventsRequest(page_size=page_size, 
                                                                           page_token=page_token, 
                                                                           trusted_only=trusted_only,
                                                                           filter_users=accounts,
                                                                           filter_event_type=event_types,
                                                                           filter_resource=resources,
                                                                           add_linked_resource=links))
            end = time.time()
        except Exception as e:
            print("get_feed error: "+str(e))
            return
        
        print("{:<30}|{:<13}|{:<48}|{:<24}|{:<24}|".format('Resource','Type','Author','event_ts','observed_ts'))
        print(''.join(["-"]*30+["|"]+["-"]*13+['|']+["-"]*48+['|']+["-"]*24+["|"]+["-"]*24+['|']))
        for event in res.events:
            dt = datetime.fromtimestamp(event.event_time.seconds*1000)
            event_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            if event.event_time.nanos != "":
                event_time += '.'+str(int(event.event_time.nanos)).zfill(9)

            dt = datetime.fromtimestamp(event.observe_time.seconds)
            observe_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            if event.observe_time.nanos != "":
                observe_time += '.'+str(int(event.observe_time.nanos)).zfill(9)
            print("{:<30}|{:<13}|{:<48}|{:<24}|{:<24}|".format(self._trim(event.new_blob.resource,30,trim_ending=True),
                                                    self._trim(event.new_blob.blob_type,13,trim_ending=True),
                                                    self._trim(event.new_blob.author,48,trim_ending=True),
                                                    self._trim(event_time,24,trim_ending=True),
                                                    self._trim(observe_time,24,trim_ending=True)))
        
        print("Next Page Token: ["+res.next_page_token+"]")
        print("Elapsed time: "+str(end-start))
    def search(self, query, include_body=False):   
        # Search for entities matching the query string
        try:
            res = self._entities.SearchEntities(entities_pb2.SearchEntitiesRequest(query=query, include_body=include_body))
        except Exception as e:
            print("search error: "+str(e))
            return
        
        print("{:<72}|{:<26}|{:<8}|{:<8}|{:<24}|{:<48}|{:<10}|".format('Resource','Content','Type','Blob ID','Version Time','Parent Titles','Owner'))
        print(''.join(["-"]*72+["|"]+["-"]*26+['|']+["-"]*8+['|']+["-"]*8+['|']+["-"]*24+['|']+["-"]*48+['|']+["-"]*10+['|']))
        for entitiy in res.entities:
            dt = datetime.fromtimestamp(entitiy.version_time.seconds)
            version_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            if entitiy.version_time.nanos != "":
                version_time += '.'+str(int(entitiy.version_time.nanos)).zfill(9)
            print("{:<72}|{:<26}|{:<8}|{:<8}|{:<24}|{:<48}|{:<10}|".format(self._trim(entitiy.id,72,trim_ending=False),
                                                    self._trim(entitiy.content,26,trim_ending=True),
                                                    self._trim(entitiy.type,8,trim_ending=True),
                                                    self._trim(entitiy.blob_id,8,trim_ending=False),
                                                    self._trim(version_time,24,trim_ending=True),
                                                    self._trim(">".join(entitiy.parent_names),48,trim_ending=False),
                                                    self._trim(entitiy.owner,10,trim_ending=False)))
    
    def subscribe(self, account, path = "", recursive=False):   
        # Subscribe to a document, fetching it first if not found locally
        try:
            self._subscriptions.Subscribe(subscriptions_pb2.SubscribeRequest(account= account, path=path, recursive=recursive))
        except Exception as e:
            print("subscribe error: "+str(e))
            return
        print("Successfully subscribed to hm://"+account+path)
    
    def mentions(self, id):   
        # List all mentions
        try:
            mentions = self._entities.ListEntityMentions(entities_pb2.ListEntityMentionsRequest(id= id, page_size = 10000))
        except Exception as e:
            print("mentions error: "+str(e))
            return
        
        print("{:<69}|{:<24}|{:<24}|{:<12}|{:<24}|{:<24}|{:<26}|".format('Source IRI', 'Blob Source CID', 'Source Document', 'Source Type', 'Target Version', 'Author', 'Create Time'))
        print(''.join(["-"]*69+["|"]+["-"]*24+['|']+["-"]*24+['|']+["-"]*12+['|']+["-"]*24+['|']+["-"]*24+['|']+["-"]*26+['|']))
        for mention in mentions.mentions:
            dt = datetime.fromtimestamp(mention.source_blob.create_time.seconds)
            create_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            if mention.source_blob.create_time.nanos != "":
                create_time += '.'+str(int(mention.source_blob.create_time.nanos)).zfill(9)
            print("{:<69}|{:<24}|{:<24}|{:<12}|{:<24}|{:<24}|{:<26}|".format(self._trim(mention.source,69,trim_ending=True),
                                                    self._trim(mention.source_blob.cid,24,trim_ending=True),
                                                    self._trim(mention.source_document,24,trim_ending=False),
                                                    self._trim(mention.source_type,12,trim_ending=True),
                                                    self._trim(mention.target_version,24,trim_ending=False),
                                                    self._trim(mention.source_blob.author,24,trim_ending=True),
                                                    self._trim(create_time,26,trim_ending=True)))

            
    # Groups 
    def list_group_content(self,id):   
        # List the content of a specified group
        try:
            res = self._groups.ListContent(groups_pb2.ListContentRequest(id=id))
        except Exception as e:
            print("list_group_content error: "+str(e))
            return
        print("{:<43}|{:<35}|".format('EID','Title'))
        print(''.join(["-"]*43+["|"]+["-"]*35+['|']+["|"]))
        str_dict = str(res.content).replace("'",'"')
        d = json.loads(str_dict)
        for title, eid in d.items():
            print("{:<43}|{:<35}|".format(self._trim(eid,43,trim_ending=True),
                                                    self._trim(title,35,trim_ending=True)))
    def create_group(self, title, description = "", url=""):   
        # Create a new P2P group with the given title, description, and setup URL
        try:
            res = self._groups.CreateGroup(groups_pb2.CreateGroupRequest(title=title, description=description, site_setup_url=url))
        except Exception as e:
            print("create_group error: "+str(e))
            return
        print(res.id)

    def list_group_content(self,id):   
        # List the content of a specified group
        try:
            res = self._groups.ListContent(groups_pb2.ListContentRequest(id=id))
        except Exception as e:
            print("list_group_content error: "+str(e))
            return
        print("{:<43}|{:<35}|".format('EID','Title'))
        print(''.join(["-"]*43+["|"]+["-"]*35+['|']+["|"]))
        str_dict = str(res.content).replace("'",'"')
        d = json.loads(str_dict)
        for title, eid in d.items():
            print("{:<43}|{:<35}|".format(self._trim(eid,43,trim_ending=True),
                                                    self._trim(title,35,trim_ending=True)))

    def list_groups(self):   
        # List all known P2P groups
        try:
            res = self._groups.ListGroups(groups_pb2.ListGroupsRequest())
        except Exception as e:
            print("list_groups error: "+str(e))
            return
        print("{:<29}|{:<12}|{:<10}|{:<10}|{:<19}|".format('EID','Title','Version','Owner','Site'))
        print(''.join(["-"]*29+["|"]+["-"]*12+['|']+["-"]*10+["|"]+["-"]*10+["|"]+["-"]*19+["|"]))
        for g in res.groups:
            print("{:<29}|{:<12}|{:<10}|{:<10}|{:<19}|".format(self._trim(g.id,29,trim_ending=False),
                                                    self._trim(g.title,12,trim_ending=True),
                                                    self._trim(g.version,10,trim_ending=False),
                                                    self._trim(g.owner_account_id,10,trim_ending=False),
                                                    self._trim(g.site_info.base_url,19,trim_ending=True)))

    # Payments 
    def create_wallet(self, account, name = ""):   
        # Create a new wallet for the specified account
        if name =="":
            name = account
        try:
            res = self._wallets.CreateWallet(wallets_pb2.CreateWalletRequest(account=account, name=name))
        except Exception as e:
            print("create_wallet error: "+str(e))
            return
        print("ID :"+str(res.id))
        print("Account :"+str(res.account))
        print("Address :"+str(res.address))
        print("Name :"+str(res.name))
        print("Type :"+str(res.type))

    def remove_wallet(self,id):
        # Remove a wallet by its ID
        try:
            self._wallets.RemoveWallet(wallets_pb2.WalletRequest(id=id))
        except Exception as e:
            print("remove_wallet error: "+str(e))
            return
        print("Wallet successfully removed")

    def export_wallet(self,id):
        # Export the credentials of a wallet by its ID
        try:
            res = self._wallets.ExportWallet(wallets_pb2.WalletRequest(id=id))
        except Exception as e:
            print("export_wallet error: "+str(e))
            return
        print(res.credentials)

    def receive_wallet(self,id, amount = 0, memo=""):
        # Create an invoice to receive money on a wallet
        try:
            res = self._invoices.CreateInvoice(invoices_pb2.CreateInvoiceRequest(id=id, amount = amount, memo=memo))
        except Exception as e:
            print("receive_wallet error: "+str(e))
            return
        print(res.payreq)

    def pay_wallet(self, id, payreq, amount = 0):
        # Pay an invoice with a specified wallet
        try:
            self._invoices.PayInvoice(invoices_pb2.PayInvoiceRequest(id=id, amount=amount, payreq=payreq))
        except Exception as e:
            print("pay_wallet error: "+str(e))
            return
        print("Payment succeeded")

    def list_wallets(self, account=""):   
        # List all wallets for a specified account
        try:
            res = self._wallets.ListWallets(wallets_pb2.ListWalletsRequest(account=account))
        except Exception as e:
            print("list_wallets error: "+str(e))
            return
        print("{:<64}|{:<10}|{:<12}|{:<30}|{:<10}|".format('id','Name','Account','Address','Type'))
        print(''.join(["-"]*64+["|"]+["-"]*10+['|']+["-"]*12+["|"]+["-"]*30+["|"]+["-"]*10+["|"]))
        for w in res.wallets:
            print("{:<64}|{:<10}|{:<12}|{:<30}|{:<10}|".format(self._trim(w.id,64,trim_ending=False),
                                                    self._trim(w.name,10,trim_ending=False),
                                                    self._trim(w.account,12,trim_ending=False),
                                                    self._trim(w.address,30,trim_ending=True),
                                                    self._trim(w.type,10,trim_ending=True)))
            
    # Documents
    def create_or_update_draft(self, title="", body=[], draft_id= "", append="", parent="", heading=False, is_image=False, quiet=True):
        # Create or update a draft document with the specified parameters
        try:
            ref = ""
            changes = []
            if title is not None and title != "" and draft_id != "":
                changes = [documents_pb2.DocumentChange(set_title=title)]

            if draft_id is None or draft_id == "":
                if title == "":
                    raise ValueError("New drafts must contain a title")
                draft = self._drafts.CreateDraft(documents_pb2.CreateDraftRequest())
                
            else:
                draft = self._drafts.GetDraft(documents_pb2.GetDraftRequest(document_id=draft_id))
            
        except Exception as e:
            print("draft error: "+str(e))
            return
        try:
            if heading and len(body) > 1:
                raise ValueError("Headings must not contain line breaks")
            elif heading and is_image:
                raise ValueError("Cannot insert an image as a heading")
            elif heading:
                block_type = "heading"
            elif is_image:
                if len(body) != 1:
                    raise ValueError("Text must be the path to the image with no line breaks")
                block_type = "image"
                ref = "ipfs://"+self._upload_file(body[0])
            else:
                block_type = "paragraph"
            for line in body:
                block_id=''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))
                changes += [documents_pb2.DocumentChange(move_block=documents_pb2.DocumentChange.MoveBlock(block_id=block_id, parent=parent, left_sibling=append))]
                changes += [documents_pb2.DocumentChange(replace_block=documents_pb2.Block(id=block_id,text=line,type=block_type, ref=ref))]
                append = block_id
            self._drafts.UpdateDraft(documents_pb2.UpdateDraftRequest(document_id=draft.id, changes=changes))
        except Exception as e:
            print("draft error: "+str(e))
            return
        if not quiet:
            if draft_id is None or draft_id == "":
                print(draft.id)
            else:
                print(block_id)
        return draft

    def create_document_v1(self, title, body=[]):
        # Create a version 1 document with the specified title and body
        draft = self.create_or_update_draft(title, body)
        if draft is None:
            print("Could not create a draft in the first place: "+str(e))
            return
        try:
            publication = self._drafts.PublishDraft(documents_pb2.PublishDraftRequest(document_id=draft.id))
        except Exception as e:
            print("publishing document error: "+str(e))
            return
        print(f"{draft.id}?v={publication.version}")
    
    def create_document_change(self, account, title, version = "", body=[], path="",key_name="main"):
        # Create a document change with the specified parameters
        try:
            ref = ""
            changes = []
            if title is not None and title != "":
                new_title = documents_v3_pb2.DocumentChange.SetMetadata(key="name", value=title)
                changes = [documents_v3_pb2.DocumentChange(set_metadata=new_title)]
            
        except Exception as e:
            print("create_document_change error: "+str(e))
            return
        try:
            block_type = "paragraph"
            for line in body:
                block_id=''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))
                changes += [documents_v3_pb2.DocumentChange(move_block=documents_v3_pb2.DocumentChange.MoveBlock(block_id=block_id))]
                changes += [documents_v3_pb2.DocumentChange(replace_block=documents_v3_pb2.Block(id=block_id,text=line,type=block_type, ref=ref))]
            doc = self._documents.CreateDocumentChange(documents_v3_pb2.CreateDocumentChangeRequest(path=path, account=account, changes=changes, signing_key_name=key_name, base_version=version))
        except Exception as e:
            print("create_document_change error: "+str(e))
            return
        
        print(f"{doc.account}{doc.path}?v={doc.version}")

    def get_document(self, eid):
        # Retrieve a document by its EID
        try:
            pattern = r"^hm://(?P<account>[^/?]+)(?P<path>/[^?]*)?(?:\?v=(?P<version>[^&]*))?"
            match = re.match(pattern, eid)
            if match:
                result = match.groupdict()
                account = result['account']
                path = result.get('path', "")
                version = result.get('version', "")
            else:
                raise ValueError("Invalid eid format: "+ eid)
            doc = self._documents.GetDocument(documents_v3_pb2.GetDocumentRequest(account=account, path=path, version= version))
        except Exception as e:
            print("get_document error: "+str(e))
            return
        print(doc)

    def delete_publication(self, eid, reason=""):
        # Delete a publication by its EID with an optional reason
        try:
            self._entities.DeleteEntity(entities_pb2.DeleteEntityRequest(id=eid.split("?v=")[0], reason = reason))
        except Exception as e:
            print("remove_publication error: "+str(e))
            return
        print("Entity: ["+str(eid) + "] removed successfully")

    def restore_publication(self, eid):
        # Restore a previously deleted publication by its EID
        try:
            self._entities.RestoreEntity(entities_pb2.RestoreEntityRequest(id=eid.split("?v=")[0]))
            self._entities.DiscoverEntity(entities_pb2.DiscoverEntityRequest(id=eid.split("?v=")[0]))
        except Exception as e:
            print("restore_publication error: "+str(e))
            return
        print("Entity: ["+str(eid) + "] restored successfully")

    
    def list_documents(self, account="", page_size=30, page_token="", list_formatting=True):
        # List documents for a specified account with pagination
        try:
            if account == "":
                account_path_str = "Account"
                res = self._documents.ListRootDocuments(documents_v3_pb2.ListRootDocumentsRequest(page_token=page_token, page_size=page_size))
            else:
                res = self._documents.ListDocuments(documents_v3_pb2.ListDocumentsRequest(account=account, page_token=page_token, page_size=page_size))
                account_path_str = "Path"
        except Exception as e:
            print("list_documents error: "+str(e))
            return
        
        
        if not list_formatting:
            for p in res.publications:
                print(account_path_str+" :"+str(p.path))
                print("Version :"+str(p.version))
                print("Meta :"+str(p.metadata))
                print("Creators :"+str(p.authors))
                print("Updated time :"+str(p.update_time))
        else:
            print("{:<19}|{:<20}|{:<28}|{:<20}|{:<19}|".format(account_path_str,'Version','Title','Creators','Updated time'))
            print(''.join(["-"]*19+["|"]+["-"]*20+['|']+["-"]*28+["|"]+["-"]*20+["|"]+["-"]*19+["|"]))
            for p in res.documents:
                if account == "":
                    account_path_data = p.account
                else:
                    account_path_data = p.path
                print("{:<19}|{:<20}|{:<28}|{:<20}|{:<19}|".format(self._trim(str(account_path_data),19,trim_ending=False),
                                                     self._trim(str(p.version),20,trim_ending=False),
                                                     self._trim(str(p.metadata),28,trim_ending=False),
                                                     self._trim(str(p.authors),20,trim_ending=False),
                                                     self._trim(p.update_time.ToDatetime().strftime("%Y-%m-%d %H:%M:%S"),19,trim_ending=False)))
        print("Next Page Token: ["+res.next_page_token+"]")
    def remove_draft(self, id, quiet=False):
        # Remove a draft by its ID
        try:
            self._drafts.DeleteDraft(documents_pb2.DeleteDraftRequest(document_id=id))
        except Exception as e:
            print("remove_draft error: "+str(e))
            return
        if not quiet:
            print("Draft Removed")

    def remove_all_drafts(self):
        # Remove all drafts
        try:
            drafts = self.list_drafts(quiet=True)
            if drafts is None:
                raise ValueError("Error listing drafts")
            for d in drafts.documents:
                self.remove_draft(d.id, quiet=True)
        except Exception as e:
            print("remove_all_drafts error: "+str(e))
            return
        print("All Drafts Removed")

    def list_drafts(self, page_size=30, page_token="", quiet=False):
        # List all drafts with pagination
        try:
            drafts = self._drafts.ListDrafts(documents_pb2.ListDraftsRequest(page_size=page_size,page_token=page_token))
        except Exception as e:
            print("list_drafts error: "+str(e))
            return
        print("{:<29}|{:<20}|".format('ID','Title'))
        print(''.join(["-"]*29+['|']+["-"]*20+["|"]))
        if not quiet:
            for d in drafts.documents:
                print("{:<29}|{:<20}|".format(self._trim(str(d.id),29,trim_ending=False),
                                                        self._trim(str(d.title),20,trim_ending=False)))
        print("Next Page Token: ["+drafts.next_page_token+"]")
        return drafts

    # Daemon
    def daemon_info(self):
        # Get information about the daemon running on the host
        try:
            res = self._daemon.GetInfo(daemon_pb2.GetInfoRequest())
        except Exception as e:
            print("daemon_info error: "+str(e))
            return
        print("Peer ID: "+str(res.peer_id))
        print("Start time: "+str(res.start_time.ToDatetime())+" UTC")
        print("Protocol ID: "+str(res.protocol_id))

    def force_sync(self):
        # Force a sync loop on the server
        try:
            res = self._daemon.ForceSync(daemon_pb2.ForceSyncRequest())
        except Exception as e:
            print("force_sync error: "+str(e))
            return
        print("force_sync OK:"+str(res))

    def register(self, name, mnemonics, passphrase = ""):
        # Register the device under the account using mnemonics
        try:
            res = self._daemon.RegisterKey(daemon_pb2.RegisterKeyRequest(name=name, mnemonic=mnemonics, passphrase=passphrase))
        except Exception as e:
            print("register error: "+str(e))
            return
        print("registered account_id :"+str(res.account_id))

    # Networking
    def list_peers(self):
        # List all known peers
        try:
            res = self._networking.ListPeers(networking_pb2.ListPeersRequest(page_size=5000))
        except Exception as e:
            print("list_peers error: "+str(e))
            return
        print("{:<52}|{:<18}|{:<6}|{:<13}|{:<19}|{:<19}|".format('PeerID','Protocol','Direct','Status', 'Created At', 'Updated At'))
        print(''.join(["-"]*52+['|']+["-"]*18+["|"]+["-"]*6+["|"]+["-"]*13+["|"]+["-"]*19+["|"]+["-"]*19+["|"]))
        for peer in res.peers:
            print("{:<52}|{:<18}|{:<6}|{:<13}|{:<19}|{:<19}|".format(
                                                    self._trim(peer.id,52,trim_ending=False),
                                                    self._trim(str(peer.protocol),18,trim_ending=False),
                                                    self._trim(str(peer.is_direct),6,trim_ending=True),
                                                    self._trim(self._status2string(peer.connection_status),13,trim_ending=True),
                                                    self._trim(str(datetime.fromtimestamp(peer.created_at.seconds)),19),
                                                    self._trim(str(datetime.fromtimestamp(peer.updated_at.seconds)),19)))

    def peer_info(self, cid, dict_output=False):
        # Get information about a peer by its CID
        try:
            res = self._networking.GetPeerInfo(networking_pb2.GetPeerInfoRequest(device_id=cid))
        except Exception as e:
            print("peer_info error: "+str(e))
            return
        if not dict_output:
            addrs_list = [_ for _ in res.addrs]
            print("Addresses :"+','.join(addrs_list))
            print("Account id :"+str(res.account_id))
            print("Status :"+str(res.connection_status))
        else:
            return {"account id": str(res.account_id), "addresses":str(res.addrs), "connection status": self._status2string(res.connection_status)}
        
    def connect(self, addrs):
        # Connect to remote peers using their addresses
        if type(addrs) != list:
            print("addrs must be a list")
            return
        space_separated=[]
        for addr in addrs:
            space_separated+=addr.replace('"','').replace("'","").split(",")
        try:
            res = self._networking.Connect(networking_pb2.ConnectRequest(addrs=space_separated))
        except Exception as e:
            print("connect error: "+str(e))
            return
        print("connect response:"+str(res))

    def discover(self, eid, recursive=False):
        # Discover an object in the P2P network by its EID
        iri = eid.replace("hm://","")
        account = iri.split("/")[0]
        path = iri.split("?v=")[0].replace(account,"")
        if len(iri.split("?v="))==1:
            version = ""
        else:
            version = iri.split("?v=")[1]
        try:
            print("version", version)
            ret = self._entities.DiscoverEntity(entities_pb2.DiscoverEntityRequest(account=account, path=path, version=version, recursive=recursive))
        except Exception as e:
            print("discover error: "+str(e))
            return
        print("Discovered With version: "+ ret.version)
    
    # Accounts
    def account_info(self, acc_id = ""):
        # Get information about a specified account
        try:
            res = self._accounts.GetAccount(accounts_pb2.GetAccountRequest(id=acc_id))
        except Exception as e:
            print("account info error: "+str(e))
            return
        
        if len(res.devices)>0:
            devices={}
            for d in res.devices:
                address = self.peer_info(d, dict_output=True)
                devices[d]=address
        else:
            devices = "No devices under the account"
        
        print(devices)
    
    def get_profile(self, acc_id = ""):
        # Get the profile information of a specified account
        try:
            account = self._accounts.GetAccount(accounts_pb2.GetAccountRequest(id=acc_id))
        except Exception as e:
            print("Getting account error: "+str(e))
            return
        print("Alias: "+str(account.profile.alias))
        print("Bio: "+str(account.profile.bio))
        print("Avatar: "+str(account.profile.avatar))

    def set_alias(self, alias = ""):
        # Set the alias of the device running on the server
        try:
            account = self._accounts.UpdateProfile(accounts_pb2.Profile(alias=alias))
        except Exception as e:
            print("update profile error: "+str(e))
            return
        print("new alias: "+str(account.profile.alias))

    def list_accounts(self):
        # List all known accounts (contacts) excluding the self account
        try:
            accounts = self._documents.ListAccounts(documents_v3_pb2.ListAccountsRequest())
        except Exception as e:
            print("Getting account error: "+str(e))
            return
        
        print("{:<20}|{:<8}|{:<24}|{:<10}|".format('ID','Comments','Latest Change','Subscribed'))
        print(''.join(["-"]*20+['|']+["-"]*8+['|']+["-"]*24+["|"]+["-"]*10+["|"]))
        for account in accounts.accounts:
            latest_change = account.activity_summary.latest_change_time.ToDatetime().strftime('%Y-%m-%d %H:%M:%S')
            print("{:<20}|{:<8}|{:<24}|{:<10}|".format(self._trim(account.id,20,trim_ending=False),
                                                        self._trim(str(account.activity_summary.comment_count),8,trim_ending=False),
                                                        self._trim(latest_change,24,trim_ending=False), 
                                                        self._trim(str(account.is_subscribed).replace("0","Subscribed").replace("1","Unsubscribed"),10)))

def main():
    """basic gRPC client that sends commands to a remote gRPC server

    Returns:
        int: return code 0 on success -1 on error
    """
    # Main function to parse arguments and execute commands
    # General
    parser = argparse.ArgumentParser(description='Basic gRPC client that sends commands to a remote gRPC server',
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(help='sub-command help', required=True, dest="command",)
    
    parser.add_argument('--server', dest='server', type=str, default="localhost:55002", metavar='SRV',
                        help='gRPC server address <IP>:<port>.')
    
    # Groups
    group_parser = subparsers.add_parser(name = "group", help='Groups related functionality (Create, list, update, members...)')
    group_subparser = group_parser.add_subparsers(title="Manage Groups", required=True, dest="command",
                                                        description= "Everything related to groups creation/update and listing.", 
                                                        help='groups sub-commands')
    create_group_parser = group_subparser.add_parser(name = "create", help='Create a new P2P group.')
    create_group_parser.add_argument('title', type=str, help="Group's Title")
    create_group_parser.add_argument('--description', '-d', type=str, help="Brief description of the new group.")
    create_group_parser.add_argument('--setup-url', '-u', type=str, help="Secret setup URL that is provided during site server deployment. If present, the group will instantly be published as a site after creating. It can also be provided later with `InitializeServer` call under Sites management.")
    create_group_parser.set_defaults(func=create_group)

    list_group_parser = group_subparser.add_parser(name = "list", help='List all known P2P groups.')
    list_group_parser.set_defaults(func=list_groups)

    get_group_parser = group_subparser.add_parser(name = "get", help='Get the content of a group.')
    get_group_parser.add_argument('id', type=str, help="Group's ID")
    get_group_parser.set_defaults(func=list_group_content)
    
    # Activity
    activity_parser = subparsers.add_parser(name = "activity", help='Activity related functionality (Feed, Subscriptions, ...)')
    activity_subparser = activity_parser.add_subparsers(title="Manage Activity", required=True, dest="command",
                                                        description= "Everything related to activity.", 
                                                        help='activity sub-commands')
    feed_parser = activity_subparser.add_parser(name = "feed", help='List the activity feed of the local node.')
    feed_parser.add_argument('--trusted-only', '-T', action="store_true", help="Only events from trusted peers")
    feed_parser.add_argument('--accounts', '-a', nargs='+', type=str, help="Events from specific accounts.")
    feed_parser.add_argument('--event-types', '-e', nargs='+', type=str, help="Only specific event types KeyDelegation | Change | Comment | DagPB.")
    feed_parser.add_argument('--resources', '-r', nargs='+', type=str, help="Events from specific resources")
    feed_parser.add_argument('--add-links', '-l', nargs='+', type=str, help="Add linked iris to the list.")
    
    feed_parser.add_argument('--page-size', '-s', type=int, help="Number of events per request")
    feed_parser.add_argument('--page-token', '-t', type=str, help="Pagination token")
    feed_parser.set_defaults(func=feed)

    search_parser = activity_subparser.add_parser(name = "search", help='Search a resource. Responds a list of matching resources.')
    search_parser.add_argument('query', type=str, help="The query string to perform the fuzzy search.")
    search_parser.add_argument('--include-body', '-b', action="store_true", help='Search also in the body of the documents and comments.')
    search_parser.set_defaults(func=search)

    subscribe_parser = activity_subparser.add_parser(name = "subscribe", help='Subscribe to a document. If not found locally, it tries to fetch it first.')
    subscribe_parser.add_argument('account', type=str, help="The account the document to subscribe belongs to.")
    subscribe_parser.add_argument('--path', '-p', type=str, const="", help='The path under the document is located. Blank for root document', nargs='?', default="")
    subscribe_parser.add_argument('--recursive', '-r', action="store_true", help='Subscribe also to all paths under the one provided in eid')
    subscribe_parser.set_defaults(func=subscribe)
    
    mentions_parser = activity_subparser.add_parser(name = "mentions", help='List the entity mentions')
    mentions_parser.add_argument('id', type=str, help="ID of the entity to list mentions for.")
    mentions_parser.set_defaults(func=mentions)
    # Sites
    site_parser = subparsers.add_parser(name = "site", help='Sites related functionality (Init, info, publish, ...)')
    site_subparser = site_parser.add_subparsers(title="Manage Sites", required=True, dest="command",
                                                        description= "Everything related to sites updates.", 
                                                        help='sites sub-commands')
    init_site_parser = site_subparser.add_parser(name = "init", help='Initializes the server to become a website for a specific group.')
    init_site_parser.add_argument('secret_url', type=str, help="The secret provided during the site deployment process.")
    init_site_parser.add_argument('group_eid', type=str, help="The group EID that should be served on this site.")
    init_site_parser.set_defaults(func=init_site)

    site_info_parser = site_subparser.add_parser(name = "info", help='Gets the public information about the website.')
    site_info_parser.set_defaults(func=site_info)

    # Payments
    wallet_parser = subparsers.add_parser(name = "wallet", help='Payment related stuff (Create wallet, pay, receive, ...)')
    wallet_subparser = wallet_parser.add_subparsers(title="Manage wallets", required=True, dest="command",
                                                        description= "Everything related to wallet management and payments.", 
                                                        help='wallets sub-commands')
    create_wallet_parser = wallet_subparser.add_parser(name = "create", help='Create a seed wallet.')
    create_wallet_parser.add_argument('account', type=str, help="Account ID where the new wallet will belong to.")
    create_wallet_parser.set_defaults(func=create_wallet)

    import_wallet_parser = wallet_subparser.add_parser(name = "import", help='Imports a compatible wallet.')
    import_wallet_parser.add_argument('account', type=str, help="Account ID where the new wallet will belong to.")
    import_wallet_parser.add_argument('credentials', type=str, help="URI in the format <wallet_type>://<alphanumeric_login>:<alphanumeric_password>@https://<domain>.")
    import_wallet_parser.set_defaults(func=import_wallet)

    export_wallet_parser = wallet_subparser.add_parser(name = "export", help='Export an already registered walled.')
    export_wallet_parser.add_argument('id', type=str, help="Wallet ID to export.")
    export_wallet_parser.set_defaults(func=export_wallet)

    list_wallet_parser = wallet_subparser.add_parser(name = "list", help='List available wallets.')
    list_wallet_parser.add_argument('--account', '-a', type=str, help="If we want wallets from specific account only")
    list_wallet_parser.set_defaults(func=list_wallets)

    remove_wallet_parser = wallet_subparser.add_parser(name = "remove", help='Remove a specific wallet.')
    remove_wallet_parser.add_argument('id', type=str, help="Wallet ID to remove.")
    remove_wallet_parser.set_defaults(func=remove_wallet)

    pay_wallet_parser = wallet_subparser.add_parser(name = "pay", help='Pay an invoice with a wallet.')
    pay_wallet_parser.add_argument('id', type=str, help="Wallet ID to pay with.")
    pay_wallet_parser.add_argument('payreq', type=str, help="BOLT-11 invoice to pay.")
    pay_wallet_parser.add_argument('--amount', '-a', type=int, default=0, help="Amount to pay")
    pay_wallet_parser.set_defaults(func=pay_wallet)

    receive_wallet_parser = wallet_subparser.add_parser(name = "receive", help='Creating an invoice to receive money on a wallet.')
    receive_wallet_parser.add_argument('id', type=str, help="Wallet ID to receive money to.")
    receive_wallet_parser.add_argument('--amount', '-a', type=int, default=0, help="Amount in Satoshis to be received. O if not provided")
    receive_wallet_parser.add_argument('--memo', '-m', type=str, help="Optional memo to be included in the invoice")
    receive_wallet_parser.set_defaults(func=receive_wallet)

    # Documents
    document_parser = subparsers.add_parser(name = "document", help='Document related functionality (create, drafts, get, ...)')
    document_subparser = document_parser.add_subparsers(title="Manage Documents", required=True, dest="command",
                                                        description= "Everything related to document creation and fetching.", 
                                                        help='documents sub-commands')
    create_document_v1_parser = document_subparser.add_parser(name = "create-v1-doc", help='SOON TO BE DEPRECATED USE create INSTEAD. Create a version 1 document (HM-23)')
    create_document_v1_parser.add_argument('body', type=str, help="document's body. Can contain linebreaks.")
    create_document_v1_parser.add_argument('--title', '-t', type=str, help="sets document's title.")
    create_document_v1_parser.set_defaults(func=create_document_v1)

    create_document_parser = document_subparser.add_parser(name = "create", help='Creates a document')
    create_document_parser.add_argument('body', type=str, help="document's body. Can contain linebreaks.")
    create_document_parser.add_argument('--title', '-t', type=str, help="sets document's title.")
    create_document_parser.add_argument('--account', '-a', type=str, help="account to publish this document to.")
    create_document_parser.add_argument('--path', '-p', type=str, const="", help="Path to publish the document to. It defaults to empty which is a root document." , nargs='?', default="")
    create_document_parser.add_argument('--version', '-v', type=str, const="", help="UPDATES ONLY. Base version of the document to update." , nargs='?', default="")
    create_document_parser.add_argument('--key-name', '-k', type=str, const="main", help="name of the key used to sign the document Default to 'main'." , nargs='?', default="main")
    create_document_parser.set_defaults(func=create_document)

    create_or_update_draft_parser = document_subparser.add_parser(name = "create-draft", help='Create a Draft or update it if it exists.')
    create_or_update_draft_parser.add_argument('body', type=str, help="document's body. Can contain linebreaks. Can be piped from other commands", nargs='?')
    create_or_update_draft_parser.add_argument('--id', type=str, help="provide an already existing draft to update it")
    create_or_update_draft_parser.add_argument('--heading', action="store_true", help="Insert data as a heading")
    create_or_update_draft_parser.add_argument('--append','-a', metavar='blkID', help="append content after provided block ID")
    create_or_update_draft_parser.add_argument('--parent','-p', metavar='blkID', help="insert content under provided block ID")
    create_or_update_draft_parser.add_argument('--image','-i', action="store_true", help="path to an image to insert")
    create_or_update_draft_parser.add_argument('--title', '-t', type=str, help="sets drafts's title.")
    create_or_update_draft_parser.set_defaults(func=create_draft)

    get_document_parser = document_subparser.add_parser(name = "get", help='Gets any given publication')
    get_document_parser.add_argument('EID', type=str, metavar='eid', help='Fully qualified ID. hm://<account>/path?v=<version>')
    get_document_parser.set_defaults(func=get_document)

    delete_publication_parser = document_subparser.add_parser(name = "delete", help='Locally deletes a publication')
    delete_publication_parser.add_argument('EID', type=str, metavar='eid', help='Fully qualified ID')
    delete_publication_parser.add_argument('--reason', '-r', type=str, help='Reason to delete')
    delete_publication_parser.set_defaults(func=delete_publication)

    delete_publication_parser = document_subparser.add_parser(name = "restore", help='Tries to restore a previously deleted document')
    delete_publication_parser.add_argument('EID', type=str, metavar='eid', help='Fully qualified ID')
    delete_publication_parser.set_defaults(func=restore_publication)

    list_documents_parser = document_subparser.add_parser(name = "list", help='Lists all known documents for an account.')
    list_documents_parser.add_argument('--page-size', '-s', type=int, help="Number of documents per request")
    list_documents_parser.add_argument('--page-token', '-t', type=str, help="Pagination token")
    list_documents_parser.add_argument('account', type=str, help="Account to retrieve documents from")
    list_documents_parser.set_defaults(func=list_documents)

    list_root_documents_parser = document_subparser.add_parser(name = "list-root", help='Lists all root documents.')
    list_root_documents_parser.add_argument('--page-size', '-s', type=int, help="Number of documents per request")
    list_root_documents_parser.add_argument('--page-token', '-t', type=str, help="Pagination token")
    list_root_documents_parser.set_defaults(func=list_root_documents)

    print_publications_parser = document_subparser.add_parser(name = "print-all", help='Prints all publications.')
    print_publications_parser.add_argument('--page-size', '-s', type=int, help="Number of documents per request")
    print_publications_parser.add_argument('--page-token', '-t', type=str, help="Pagination token")
    print_publications_parser.add_argument('--trusted-only', '-T', action="store_true",
                        help='print publications from trusted sources only')
    print_publications_parser.set_defaults(func=print_publications)

    list_drafts_parser = document_subparser.add_parser(name = "list-drafts", help='gets a list of stored drafts.')
    list_drafts_parser.add_argument('--page-size', '-s', type=int, help="Number of drafts per request")
    list_drafts_parser.add_argument('--page-token', '-t', type=str, help="Pagination token")
    list_drafts_parser.set_defaults(func=list_drafts)

    remove_draft_parser = document_subparser.add_parser(name = "remove-draft", help='Delete a draft with provided ID.')
    remove_draft_parser.add_argument('id', type=str, help="Drafts id to remove")
    remove_draft_parser.set_defaults(func=remove_draft)

    remove_all_drafts_parser = document_subparser.add_parser(name = "remove-all-drafts", help='Delete all drafts. Requires confirmation.')
    remove_all_drafts_parser.set_defaults(func=remove_all_drafts)

    # Daemon
    daemon_parser = subparsers.add_parser(name = "daemon", help='Daemon related functionality (Sync, Register, Alias, ...)')
    daemon_subparser = daemon_parser.add_subparsers(title="Manage daemon", required=True, dest="command",
                                                        description= "Everything related to daemon.", 
                                                        help='daemon sub-commands')
    
    daemon_info_parser = daemon_subparser.add_parser(name = "info", help='Gets useful information of the daemon running on host.')
    daemon_info_parser.set_defaults(func=daemon_info)

    daemon_sync_parser = daemon_subparser.add_parser(name = "sync", help='Forces a sync loop on the server.')
    daemon_sync_parser.set_defaults(func=daemon_sync)

    daemon_register_parser = daemon_subparser.add_parser(name = "register", help='Registers the device under the account taken from the provided mnemonics.')
    daemon_register_parser.add_argument('words', type=str, default=[], nargs='+', help="12|15|18|21|24 BIP-39 mnemonic words.")
    daemon_register_parser.add_argument('--name', '-n', type=str, const="main", help='name of the new key. Default as "main"' , nargs='?', default="main")
    daemon_register_parser.set_defaults(func=daemon_register)
    
    # Accounts
    account_parser = subparsers.add_parser(name = "account", help='Account related functionality (Trusted, info,...)')
    account_subparser = account_parser.add_subparsers(title="Manage accounts", required=True, dest="command",
                                                        description= "Everything related to accounts.", 
                                                        help='account sub-commands')
    
    account_info_parser = account_subparser.add_parser(name = "info", help='gets information from provided account. Own account if no account flag is provided')
    account_info_parser.add_argument('account', type=str, const="", 
                        help='Account ID to get info from. Own account if not provided' , nargs='?')
    account_info_parser.set_defaults(func=account_info)

    account_profile_parser = account_subparser.add_parser(name = "get-profile", help='Gets profile information from provided account.')
    account_profile_parser.add_argument('account', type=str, const="", 
                        help='Account ID to get profile. Own profile if not provided' , nargs='?')
    account_profile_parser.set_defaults(func=account_profile)

    account_alias_parser = account_subparser.add_parser(name = "set-alias", help='Sets alias of the device running in SRV.')
    account_alias_parser.add_argument('alias', type=str, help='New alias of the account')
    account_profile_parser.set_defaults(func=account_alias)

    account_info_parser = account_subparser.add_parser(name = "list", help='gets a list of known accounts (Contacts) without including ourselves.')
    account_info_parser.set_defaults(func=account_list)


    account_info_parser = account_subparser.add_parser(name = "trust", help='Trust provided account.')
    account_info_parser.add_argument('account', type=str, help="The Account ID we want to trust. Self account is trusted by default.")
    account_info_parser.set_defaults(func=account_trust)

    account_info_parser = account_subparser.add_parser(name = "untrust", help='Untrust provided account.')
    account_info_parser.add_argument('account', type=str, help="The Account ID we want to untrust. Cannot untrust self.")
    account_info_parser.set_defaults(func=account_untrust)
    
    # Network
    network_parser = subparsers.add_parser(name = "network", help='Network related functionality (Connect, Info, peers,...)')
    network_subparser = network_parser.add_subparsers(title="Manage network", required=True, dest="command",
                                                        description= "Everything related to networking.", 
                                                        help='network sub-commands')

    network_connect_parser = network_subparser.add_parser(name = "connect", help='Connects to remote peer.')
    network_connect_parser.add_argument('addrs', type=str, default=[], nargs='+',
                        help='peer multiaddresses. Comma separator')
    network_connect_parser.set_defaults(func=network_connect)

    network_list_parser = network_subparser.add_parser(name = "list-peers", help='List all known peers.')
    network_list_parser.set_defaults(func=network_list)

    network_info_parser = network_subparser.add_parser(name = "info", help='Gets info about a peer.')
    network_info_parser.add_argument('peer', type=str, help='peer ID')
    network_info_parser.set_defaults(func=network_info)

    network_discover_parser = network_subparser.add_parser(name = "discover", help='Discovers an object in the p2p network.')
    network_discover_parser.add_argument('eid', type=str, help='Entity ID of the entity to discover in the format hm://<account>/<the-path>?v=<version>')
    network_discover_parser.add_argument('--recursive', '-r', action="store_true", help='Discover also to all paths under the one provided in eid')
    network_discover_parser.set_defaults(func=network_discover)
    
    args = parser.parse_args()
    args.func(args)

def get_client(server):
    # Create and return a client instance connected to the specified server
    try:
        my_client = client(server)
    except Exception as e:
        print("Could not connect to provided server: "+str(e))
        sys.exit(1)
    return my_client

# Network
def network_connect(args):
    # Connect to remote peers using their addresses
    my_client = get_client(args.server)
    my_client.connect(args.addrs)
    del my_client

def network_list(args):
    # List all known peers
    my_client = get_client(args.server)
    my_client.list_peers()
    del my_client

def network_info(args):
    # Get information about a peer by its ID
    my_client = get_client(args.server)
    my_client.peer_info(cid=args.peer)
    del my_client

def network_discover(args):
    # Discover an object in the P2P network by its EID
    my_client = get_client(args.server)
    my_client.discover(eid=args.eid, recursive=args.recursive)
    del my_client

# Payments
def create_wallet(args):
    # Create a new wallet for the specified account
    my_client = get_client(args.server)
    my_client.create_wallet(account=args.account)
    del my_client

def import_wallet(args):
    # Import a compatible wallet for the specified account
    my_client = get_client(args.server)
    my_client.import_wallet(account=args.account, credentials=args.credentials)
    del my_client

def export_wallet(args):
    # Export the credentials of a wallet by its ID
    my_client = get_client(args.server)
    my_client.export_wallet(id=args.id)
    del my_client

def remove_wallet(args):
    # Remove a wallet by its ID
    my_client = get_client(args.server)
    my_client.remove_wallet(id=args.id)
    del my_client

def list_wallets(args):
    # List all wallets for a specified account
    my_client = get_client(args.server)
    my_client.list_wallets(account=args.account)
    del my_client

def pay_wallet(args):
    # Pay an invoice with a specified wallet
    my_client = get_client(args.server)
    my_client.pay_wallet(id=args.id, payreq=args.payreq, amount=args.amount)
    del my_client

def receive_wallet(args):
    # Create an invoice to receive money on a wallet
    my_client = get_client(args.server)
    my_client.receive_wallet(id=args.id, amount=args.amount, memo=args.memo)
    del my_client

# Account
def account_info(args):
    # Get information about a specified account
    my_client = get_client(args.server)
    my_client.account_info(acc_id=args.account)
    del my_client

def account_profile(args):
    # Get the profile information of a specified account
    my_client = get_client(args.server)
    my_client.get_profile(acc_id=args.account)
    del my_client

def account_alias(args):
    # Set the alias of the device running on the server
    my_client = get_client(args.server)
    my_client.set_alias(alias=args.alias)
    del my_client

def account_list(args):
    # List all known accounts (contacts) excluding the self account
    my_client = get_client(args.server)
    my_client.list_accounts()
    del my_client

def account_trust(args):
    # Trust a specified account
    my_client = get_client(args.server)
    my_client.trust_untrust(acc_id=args.account, is_trusted=True)
    del my_client

def account_untrust(args):
    # Untrust a specified account
    my_client = get_client(args.server)
    my_client.trust_untrust(acc_id=args.account, is_trusted=False)
    del my_client

# Daemon
def daemon_info(args):
    # Get information about the daemon running on the host
    my_client = get_client(args.server)
    my_client.daemon_info()
    del my_client

def daemon_sync(args):
    # Force a sync loop on the server
    my_client = get_client(args.server)
    my_client.force_sync()
    del my_client

def daemon_register(args):
    # Register the device under the account using mnemonics
    my_client = get_client(args.server)
    my_client.register(args.name, args.words)
    del my_client

# Sites
def init_site(args):
    # Initialize the server to become a website for a specific group
    my_client = get_client(args.server)
    my_client.init_site(args.secret_url, args.group_eid)
    del my_client

def site_info(args):
    # Get public information about the website
    my_client = get_client(args.server)
    my_client.site_info()
    del my_client

# Groups
def create_group(args):
    # Create a new P2P group with the given title, description, and setup URL
    my_client = get_client(args.server)
    my_client.create_group(title=args.title, description=args.description, url=args.setup_url)
    del my_client

def list_groups(args):
    # List all known P2P groups
    my_client = get_client(args.server)
    my_client.list_groups()
    del my_client

def list_group_content(args):
    # List the content of a specified group
    my_client = get_client(args.server)
    my_client.list_group_content(args.id)
    del my_client

# Activity
def feed(args):
    # Retrieve the activity feed with various filters
    my_client = get_client(args.server)
    my_client.get_feed(args.page_size, args.page_token, args.trusted_only, args.accounts, args.event_types, args.resources, args.add_links)
    del my_client

def subscribe(args):
    # Subscribe to a document, fetching it first if not found locally
    my_client = get_client(args.server)
    my_client.subscribe(args.account, args.path, args.recursive)
    del my_client

def search(args):
    # Search for entities matching the query string
    my_client = get_client(args.server)
    my_client.search(args.query, args.include_body)
    del my_client 
    
def mentions(args):
    # Search for entities matching the query string
    my_client = get_client(args.server)
    my_client.mentions(args.id)
    del my_client 
    
# Documents
def create_document_v1(args):
    # Create a version 1 document with the specified title and body
    my_client = get_client(args.server)
    my_client.create_document_v1(title=args.title if args.title != None and args.title != "" else args.body.split(" ")[0], body=args.body.splitlines())
    del my_client

def create_document(args):
    # Create a document change with the specified parameters
    my_client = get_client(args.server)
    my_client.create_document_change(path=args.path, key_name=args.key_name, account=args.account, version=args.version, title=args.title if args.title != None and args.title != "" else args.body.split(" ")[0], body=args.body.splitlines())
    del my_client

def create_draft(args):
    # Create or update a draft document with the specified parameters
    my_client = get_client(args.server)
    if not sys.stdin.isatty():
        body = sys.stdin.read().splitlines()
    else:
        if args.body is None or len(args.body)==0:
            body = []
        else:
            body = args.body.splitlines()

    my_client.create_or_update_draft(title=args.title if args.title != None and args.title != "" else args.body.split(" ")[0], body=body, draft_id = args.id, append=args.append, parent=args.parent, heading=args.heading, is_image=args.image, quiet = False)
    del my_client

def get_document(args):
    # Retrieve a document by its EID
    my_client = get_client(args.server)
    my_client.get_document(args.EID)
    del my_client

def delete_publication(args):
    # Delete a publication by its EID with an optional reason
    my_client = get_client(args.server)
    my_client.delete_publication(args.EID, args.reason)
    del my_client

def restore_publication(args):
    # Restore a previously deleted publication by its EID
    my_client = get_client(args.server)
    my_client.restore_publication(args.EID)
    del my_client

def list_documents(args):
    # List documents for a specified account with pagination
    my_client = get_client(args.server)
    my_client.list_documents(args.account, args.page_size, args.page_token, list_formatting=True)
    del my_client

def list_root_documents(args):
    # List all root documents with pagination
    my_client = get_client(args.server)
    my_client.list_documents(page_size=args.page_size, page_token=args.page_token, list_formatting=True)
    del my_client

def print_publications(args):
    # Print all publications with optional filters
    my_client = get_client(args.server)
    my_client.list_publications(args.trusted_only, args.page_size, args.page_token, list_formatting=False)
    del my_client

def list_drafts(args):
    # List all drafts with pagination
    my_client = get_client(args.server)
    my_client.list_drafts(args.page_size, args.page_token)
    del my_client

def remove_draft(args):
    # Remove a draft by its ID
    my_client = get_client(args.server)
    my_client.remove_draft(args.id)
    del my_client

def remove_all_drafts(args):
    # Remove all drafts after confirmation
    res = input('This will remove all drafts, do you really continue (Y/n)?.\n')
    if str(res).lower() == "y" or str(res).lower() == "yes":
        my_client = get_client(args.server)
        my_client.remove_all_drafts()
        del my_client

if __name__ == "__main__":
    main()