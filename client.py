#!/usr/bin/env python3
from daemon.v1alpha import daemon_pb2
from daemon.v1alpha import daemon_pb2_grpc
from networking.v1alpha import networking_pb2
from networking.v1alpha import networking_pb2_grpc
from documents.v1alpha import documents_pb2
from documents.v1alpha import documents_pb2_grpc
from documents.v1alpha import web_publishing_pb2
from documents.v1alpha import web_publishing_pb2_grpc
from p2p.v1alpha import p2p_pb2
from p2p.v1alpha import p2p_pb2_grpc
from accounts.v1alpha import accounts_pb2
from accounts.v1alpha import accounts_pb2_grpc
import grpc
import argparse
import sys
import os 

class client():
    def __init__(self, server="localhost:55002"):
        self.__channel = grpc.insecure_channel(server)
        self._daemon = daemon_pb2_grpc.DaemonStub(self.__channel)
        self._p2p = p2p_pb2_grpc.P2PStub(self.__channel)
        self._networking = networking_pb2_grpc.NetworkingStub(self.__channel)
        self._accounts = accounts_pb2_grpc.AccountsStub(self.__channel)
        self._publications = documents_pb2_grpc.PublicationsStub(self.__channel)
        self._drafts = documents_pb2_grpc.DraftsStub(self.__channel)
        self._remotesite = web_publishing_pb2_grpc.WebSiteStub(self.__channel)
        self._localsites = web_publishing_pb2_grpc.WebPublishingStub(self.__channel)

    def __del__(self):
        self.__channel.close()
    def _role_to_str(self, role):
        if role == 2:
            return "editor"
        elif role==1:
            return "owner"
        else:
            return "unspecified"

    def _str_to_role(self, role):
        if "editor" in role.lower():
            return 2
        elif "owner" in role.lower():
            return 1
        else:
            return 0
    def _status2string(self, status):
        if status == 0:
            return "NOT_CONNECTED"
        elif status == 1:
            return "CONNECTED"
        elif status == 2:
            return "CAN_CONNECT"
        elif status == 3:
            return "CANNOT_CONNECT"
        else:
            return "UNKNOWN"
    def _trim(self, string, length=24, trim_ending=True):
        if len(string) <= length or length < 3:
            return string
        else:
            if trim_ending:
                return string[:length-3] + '...'
            else:
                return '...' + string[-length+3:]
    def update_site_info(self, title="", description="", quiet=False, headers=[]):
        metadata = [tuple(h.split("=")) for h in headers if h.count('=') == 1]
        try:
            res = self._remotesite.UpdateSiteInfo(web_publishing_pb2.UpdateSiteInfoRequest(title=title, description=description), metadata=metadata)
        except Exception as e:
            print("update_site_info error: "+str(e))
            return
        if not quiet:
            print("Hostname: "+res.hostname)
            print("Title: "+res.title)
            print("Description: "+res.description)
            print("Owner: "+res.owner)

    def get_site_info(self, quiet=False, headers=[]):
        metadata = [tuple(h.split("=")) for h in headers if h.count('=') == 1]
        try:
            res = self._remotesite.GetSiteInfo(web_publishing_pb2.GetSiteInfoRequest(), metadata=metadata)
        except Exception as e:
            print("get_site_info error: "+str(e))
            return
        if not quiet:
            print("Hostname: "+res.hostname)
            print("Title: "+res.title)
            print("Description: "+res.description)
            print("Owner: "+res.owner)
    
    def create_document(self, title, body=""):
        try:
            draft = self._drafts.CreateDraft(documents_pb2.CreateDraftRequest())
        except Exception as e:
            print("draft error: "+str(e))
            return
        
        # Set Title
        try:
            changes = [documents_pb2.DocumentChange(set_title=title)]
            changes += [documents_pb2.DocumentChange(move_block=documents_pb2.DocumentChange.MoveBlock(block_id="b1"))]
            changes += [documents_pb2.DocumentChange(replace_block=documents_pb2.Block(id="b1",text=body,type="paragraph"))]
            self._drafts.UpdateDraft(documents_pb2.UpdateDraftRequest(document_id=draft.id, changes=changes))
        except Exception as e:
            print("updating document error: "+str(e))
            return
        #publish
        try:
            publication = self._drafts.PublishDraft(documents_pb2.PublishDraftRequest(document_id=draft.id))
        except Exception as e:
            print("publishing document error: "+str(e))
            return
        print(f"{draft.id}?v={publication.version}")

    def create_token(self, role="", quiet=False, headers=[]):
        metadata = [tuple(h.split("=")) for h in headers if h.count('=') == 1]
        if role=="":
            role="editor"
        try:
            res = self._remotesite.CreateInviteToken(web_publishing_pb2.CreateInviteTokenRequest(role=self._str_to_role(role)), metadata=metadata)
        except Exception as e:
            print("create_token error: "+str(e))
            return
        if not quiet:
            print(str(res.token))

    def redeem_token(self, token, quiet=False, headers=[]):
        metadata = [tuple(h.split("=")) for h in headers if h.count('=') == 1]
        try:
            res = self._remotesite.RedeemInviteToken(web_publishing_pb2.RedeemInviteTokenRequest(token=token), metadata=metadata)
        except Exception as e:
            print("redeem_token error: "+str(e))
            return
        if not quiet:
            print("Token redeemed. New role: "+self._role_to_str(res.role))
    
    def get_path(self, path, quiet=False, headers=[]):
        metadata = [tuple(h.split("=")) for h in headers if h.count('=') == 1]
        try:
            res = self._remotesite.GetPath(web_publishing_pb2.GetPathRequest(path=path), metadata=metadata)
        except Exception as e:
            print("get_path error: "+str(e))
            return
        if not quiet:
            print("Version :"+str(res.publication.version))
            print("Document :"+str(res.publication.document))

    def publish(self, ID, version="", path="", quiet=False, headers=[]):
        metadata = [tuple(h.split("=")) for h in headers if h.count('=') == 1]
        try:
            self._remotesite.PublishDocument(web_publishing_pb2.PublishDocumentRequest(document_id=ID, version=version, path=path), metadata=metadata)
        except Exception as e:
            print("publish error: "+str(e))
            return
        if not quiet:
            print("Document "+ID+" successfully published!")

    def unpublish(self, ID, version="", quiet=False, headers=[]):
        metadata = [tuple(h.split("=")) for h in headers if h.count('=') == 1]
        try:
            self._remotesite.UnpublishDocument(web_publishing_pb2.UnpublishDocumentRequest(document_id=ID, version=version), metadata=metadata)
        except Exception as e:
            print("unpublish error: "+str(e))
            return
        if not quiet:
            print("Document "+ID+" successfully removed")

    def list_document_records(self, document_id, version = "", quiet=False):
        try:
            res = self._localsites.ListWebPublicationRecords(web_publishing_pb2.ListWebPublicationRecordsRequest(document_id=document_id, version=version))
        except Exception as e:
            print("list_document_records error: "+str(e))
            return
        if not quiet:
            print("{:<22}|{:<18}|{:<18}|{:<22}|".format('ID','Path','Version','Hostname',))
            print(''.join(["-"]*22+['|']+["-"]*18+["|"]+["-"]*18+['|']+["-"]*22+["|"]))
            for record in res.publications:
                print("{:<22}|{:<18}|{:<18}|{:<22}|".format(self._trim(record.document_id, 22),
                                                            self._trim(record.path,18,trim_ending=False),
                                                            self._trim(record.version,18,trim_ending=False),
                                                            self._trim(record.hostname,22,trim_ending=False)))
    
    def list_web_publications(self, quiet=False, headers=[]):
        metadata = [tuple(h.split("=")) for h in headers if h.count('=') == 1]
        try:
            res = self._remotesite.ListWebPublications(web_publishing_pb2.ListWebPublicationsRequest(), metadata=metadata)
        except Exception as e:
            print("list_web_publications error: "+str(e))
            return
        if not quiet:
            print("{:<22}|{:<18}|{:<18}|{:<22}|".format('ID','Path', 'Version','Hostname'))
            print(''.join(["-"]*22+['|']+["-"]*18+["|"]+["-"]*18+['|']+["-"]*22+["|"]))
            for record in res.publications:
                print("{:<22}|{:<18}|{:<18}|{:<22}|".format(self._trim(record.document_id,22),
                                                            self._trim(record.path,18,trim_ending=False),
                                                            self._trim(record.version,18,trim_ending=False),
                                                            self._trim(record.hostname,22,trim_ending=False)))
    
    def add_site(self, hostname, token = "", quiet=False):
        try:
            res = self._localsites.AddSite(web_publishing_pb2.AddSiteRequest(hostname=hostname, invite_token=token))
        except Exception as e:
            print("add_site error: "+str(e))
            return
        if not quiet:
            print("Site "+str(res.hostname)+ " successfully added with role: "+self._role_to_str(res.role))

    def remove_site(self, hostname, quiet=False):
        try:
            self._localsites.RemoveSite(web_publishing_pb2.RemoveSiteRequest(hostname=hostname))
        except Exception as e:
            print("remove_site error: "+str(e))
            return
        if not quiet:
            print("Site "+str(hostname) + " successfully removed")

    def list_sites(self, quiet=False):
        try:
            ret = self._localsites.ListSites(web_publishing_pb2.ListSitesRequest())
        except Exception as e:
            print("list_sites error: "+str(e))
            return
        if not quiet:
            print("{:<35}|{:<11}|".format('Hostname','Role'))
            print(''.join(["-"]*35+['|']+["-"]*11+["|"]))
            for s in ret.sites:
                if s.role == 2:
                    role = "editor"
                elif s.role==1:
                    role = "owner"
                else:
                    role = "unspecified"
                print("{:<35}|{:<11}|".format(s.hostname, role))
    
    def forceSync(self, quiet=False):
        try:
            res = self._daemon.ForceSync(daemon_pb2.ForceSyncRequest())
        except Exception as e:
            print("forceSync error: "+str(e))
            return
        if not quiet:
            print("forceSync OK:"+str(res))

    def list_peers(self, quiet=False):
        try:
            res = self._networking.ListPeers(networking_pb2.ListPeersRequest())
        except Exception as e:
            print("list_peers error: "+str(e))
            return
        if not quiet:
            print("{:<20}|{:<20}|{:<20}|".format('AccountID','PeerID','Status'))
            print(''.join(["-"]*20+['|']+["-"]*20+["|"]+["-"]*20+["|"]))
            for peer in res.peers:
                print("{:<20}|{:<20}|{:<20}|".format(self._trim(peer.account_id,20,trim_ending=False),
                                                     self._trim(peer.id,20,trim_ending=False),
                                                     self._trim(self._status2string(peer.connection_status),20)))

    def daemonInfo(self, quiet=False):
        try:
            res = self._daemon.GetInfo(daemon_pb2.GetInfoRequest())
        except Exception as e:
            print("daemonInfo error: "+str(e))
            return
        if not quiet:
            print("Account ID :"+str(res.account_id))
            print("Device ID :"+str(res.device_id))
            print("Start time :"+str(res.start_time.ToDatetime())+" UTC")
    def trust_untrust(self, quiet, acc_id, is_trusted):
        print(acc_id)
        try:
            res = self._accounts.SetAccountTrust(accounts_pb2.SetAccountTrustRequest(id=acc_id, is_trusted=is_trusted))
        except Exception as e:
            print("trust_untrust error: "+str(e))
            return
        if not quiet:
            print(f"Account { acc_id } is now {'trusted' if is_trusted else 'untrusted'}")
    def peerInfo(self, cid, quiet=False):
        try:
            res = self._networking.GetPeerInfo(networking_pb2.GetPeerInfoRequest(device_id=cid))
        except Exception as e:
            print("peerInfo error: "+str(e))
            return
        if not quiet:
            print("Addresses :"+str(res.addrs))
            print("Account id :"+str(res.account_id))
            print("Status :"+str(res.connection_status))

    def get_publication(self, cid, quiet=False):
        try:
            cid_list = cid.split("/")
            if len(cid_list)==1:
                res = self._publications.GetPublication(documents_pb2.GetPublicationRequest(document_id=cid.split("/")[0]))
            else:    
                res = self._publications.GetPublication(documents_pb2.GetPublicationRequest(document_id=cid.split("/")[0], version=cid.split("/")[1]))
        except Exception as e:
            print("get_publication error: "+str(e))
            return
        if not quiet:
            print("Version :"+str(res.version))
            print("Document :"+str(res.document))

    def list_publications(self, quiet=False):
        try:
            res = self._publications.ListPublications(documents_pb2.ListPublicationsRequest())
        except Exception as e:
            print("list_publications error: "+str(e))
            return
        if not quiet:
            for p in res.publications:
                print("Version :"+str(p.version))
                print("Document :"+str(p.document))

    def list_drafts(self, quiet=False):
        try:
            drafts = self._drafts.ListDrafts(documents_pb2.ListDraftsRequest())
        except Exception as e:
            print("list_drafts error: "+str(e))
            return
        if not quiet:
            print("{:<72}|{:<20}|".format('ID','Title'))
            print(''.join(["-"]*72+['|']+["-"]*20+["|"]))
            for d in drafts.documents:
                print("ID :"+str(d.id))
                print("Document :"+str(d.title))

    def list_members(self, quiet=False, headers=[]):
        metadata = [tuple(h.split("=")) for h in headers if h.count('=') == 1]
        try:
            res = self._remotesite.ListMembers(web_publishing_pb2.ListMembersRequest(), metadata=metadata)
        except Exception as e:
            print("list_members error: "+str(e))
            return
        if not quiet:
            print("{:<72}|{:<11}|".format('AccountID','Role'))
            print(''.join(["-"]*72+['|']+["-"]*11+["|"]))
            for s in res.members:
                print("{:<72}|{:<11}|".format(s.account_id, self._role_to_str(s.role)))


    def delete_member(self, account_id, quiet=False, headers=[]):
        metadata = [tuple(h.split("=")) for h in headers if h.count('=') == 1]
        try:
            self._remotesite.DeleteMember(web_publishing_pb2.DeleteMemberRequest(account_id=account_id), metadata=metadata)
        except Exception as e:
            print("list_members error: "+str(e))
            return
        if not quiet:
            print("Member successfully removed")

    def get_member(self, account_id, quiet=False, headers=[]):
        metadata = [tuple(h.split("=")) for h in headers if h.count('=') == 1]
        try:
            res = self._remotesite.GetMember(web_publishing_pb2.GetMemberRequest(account_id=account_id), metadata=metadata)
        except Exception as e:
            print("list_members error: "+str(e))
            return
        if not quiet:
            print("Account ID: " + res.account_id)
            print("Role: " + self._role_to_str(res.role))

    def register(self, mnemonics, passphrase = "", quiet=False):
        try:
            res = self._daemon.Register(daemon_pb2.RegisterRequest(mnemonic=mnemonics, passphrase=passphrase))
        except Exception as e:
            print("register error: "+str(e))
            return
        if not quiet:
            print("registered account_id :"+str(res.account_id))

    def connect(self, addrs, quiet=False):
        if type(addrs) != list:
            print("addrs must be a list")
            return
        try:
            res = self._networking.Connect(networking_pb2.ConnectRequest(addrs=addrs))
        except Exception as e:
            print("connect error: "+str(e))
            return
        if not quiet:
            print("connect response:"+str(res))

    def account_info(self, acc_id = "", quiet=False):
        try:
            res = self._accounts.GetAccount(accounts_pb2.GetAccountRequest(id=acc_id))
        except Exception as e:
            print("account info error: "+str(e))
            return
        if not quiet:
            if len(res.devices)>0:
                devices={}
                for d in res.devices:
                    address = self.peer_info(d, quiet=True)
                    devices[d]=address
            else:
                devices = "No devices under the account"
            
            print(devices)
    
    def set_alias(self, alias = "",  quiet=False):
        try:
            account = self._accounts.UpdateProfile(accounts_pb2.Profile(alias=alias))
        except Exception as e:
            print("update profile error: "+str(e))
            return
        if not quiet:
            print("new alias: "+str(account.profile.alias))

    def list_accounts(self, quiet=False):
        try:
            accounts = self._accounts.ListAccounts(accounts_pb2.ListAccountsRequest())
        except Exception as e:
            print("Getting account error: "+str(e))
            return
        if not quiet:
            terminal_width = os.get_terminal_size().columns
            acc_space = min([terminal_width-20-25-10-4,48])
            print(f"{'ID':<{acc_space}}|{'Alias':<20}|{'Bio':<25}|{'isTrusted':<10}|")
            print(''.join(["-"]*acc_space+['|']+["-"]*20+['|']+["-"]*25+["|"]+["-"]*10+["|"]))
            for account in accounts.accounts:
                print(f"{self._trim(account.id,acc_space,trim_ending=False):<{acc_space}}|{self._trim(account.profile.alias,20,trim_ending=False):<20}|{self._trim(account.profile.bio,25,trim_ending=False):<25}|{self._trim(str(account.is_trusted).replace('0','Trusted').replace('1','Untrusted'),10):<10}|")


    def get_profile(self, acc_id = "", quiet=False):
        try:
            account = self._accounts.GetAccount(accounts_pb2.GetAccountRequest(id=acc_id))
        except Exception as e:
            print("Getting account error: "+str(e))
            return
        if not quiet:
            print("Alias: "+str(account.profile.alias))
            print("Bio: "+str(account.profile.bio))
            print("Avatar: "+str(account.profile.avatar))

    def peer_info(self, id, quiet=False):
        try:
            res = self._networking.GetPeerInfo(networking_pb2.GetPeerInfoRequest(device_id=id))
        except Exception as e:
            print("peer_info error: "+str(e))
            return
        if not quiet:
            print("peer account_id :%s addrs: %s status: %s"%(str(res.account_id), str(res.addrs), str(res.connection_status)))
        else:
            return {"account id": str(res.account_id), "addresses":str(res.addrs), "connection status": str(res.connection_status)}

def main():
    """basic gRPC client that sends commands to a remote gRPC server

    Returns:
        int: return code 0 on success -1 on error
    """
    parser = argparse.ArgumentParser(description='Basic gRPC client that sends commands to a remote gRPC server',
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--headers', dest = "headers", type=str, default=[], metavar='KEY=VALUE',nargs='+',
                        help='Adds key:value header to the gRPC call. Multiple headers can be defined separated by blank space')
    parser.add_argument('--add-site', dest = "add_site", type=str, metavar='HOSTNAME',
                        help='adds a site located in HOSTNAME with an optional invite TOKEN.')
    parser.add_argument('--token', dest = "token", type=str, metavar='TOKEN',
                        help='append an invitational TOKEN to the --add-site call.')
    parser.add_argument('--trust', dest = "trust_account", type=str, metavar='CID',
                        help='trust the provided account.')
    parser.add_argument('--untrust', dest = "untrust_account", type=str, metavar='CID',
                        help='untrust the provided account.')
    parser.add_argument('--remove-site', dest = "del_site", type=str, metavar='HOSTNAME',
                        help='removes a site located in HOSTNAME.')
    parser.add_argument('--get-site-info', dest = "get_site_info", action="store_true",
                        help='gets site info.')
    parser.add_argument('--update-site-info', dest = "update_site_info", action="store_true",
                        help='updates site info with TITLE and DESCRIPTION optional flags.')
    parser.add_argument('--title', dest = "title", type=str, metavar='TITLE',
                        help='sets (updates) a title to a given site/document.')
    parser.add_argument('--description', dest = "description", type=str, metavar='DESCRIPTION',
                        help='sets (updates) a description to a given site.')
    parser.add_argument('--create-token', dest = "create_token", type=str, metavar='ROLE',
                        nargs='?', help='Create an invite token with an optional role editor | owner')
    parser.add_argument('--create-document', dest = "create_document", type=str, metavar='TITLE',
                        help='Create a document with a short title')
    parser.add_argument('--redeem-token', dest = "redeem_token", type=str, metavar='TOKEN',
                        help='Redeem TOKEN if it is a valid token')
    parser.add_argument('--list-web-publications', dest = "list_web_publications", action="store_true",
                        help='List all available published documents on the site')
    parser.add_argument('--list-document-records', dest = "list_document_records", type=str, metavar='ID',
                        help='List all records (in all known sites) for any given document ID and optional VERSION')
    parser.add_argument('--get-path', dest = "get_path", type=str,  metavar='PATH', nargs='?', const="/",
                        help='Get a publication in path PATH. In PATH not provided, root document is assumed.')
    parser.add_argument('--publish', dest = "publish", type=str, metavar='ID',
                        help='Publish a document with ID and optional VERSION and PATH')
    parser.add_argument('--unpublish', dest = "unpublish", type=str, metavar='ID',
                        help='Remove a published a document with ID and optional VERSION')
    parser.add_argument('--version', dest = "version", type=str, metavar='VERSION',
                        help='Optional version to publish a document with')
    parser.add_argument('--path', dest = "path", type=str, metavar='PATH',
                        help='Optional pretty path to publish a document with')
    parser.add_argument("--list-members", dest = "list_members", action="store_true",  help="List site members")
    parser.add_argument("--get-member", dest = "get_member", type=str, metavar='ACCOUNTID',
                        help="Get info about specific site member")
    parser.add_argument("--delete-member", dest = "delete_member", type=str, metavar='ACCOUNTID',
                        help="Removes an specific member")
    parser.add_argument("--list-sites", dest = "list_sites", action="store_true",  help="List added sites")
    parser.add_argument("--sync", action="store_true",  help="Forces a sync loop on the server")
    parser.add_argument("--quiet", action="store_true",  help="Suppress output")
    parser.add_argument('--connect', dest='peer_connect', type=str, default=[], metavar='ADDRS', nargs='+',
                        help='connects to the given multiaddresses')
    parser.add_argument('--register', dest='mnemonics', type=str, default=[], metavar='WORDS', nargs='+',
                        help='registers the device under the account taken from the provided mnemonics.')
    parser.add_argument('--account-info', dest = "get_account", type=str, metavar='CID', const="", 
                        help='gets information from own account [CID]. Own account if not provided', nargs='?')
    parser.add_argument('--get-profile', dest = "get_profile", type=str, metavar='CID', const="", 
                        help='gets profile information from account [CID]. Own profile if not provided' , nargs='?')
    parser.add_argument('--list-publications', dest = "list_publications", action="store_true", 
                        help='gets a list of own publications.')
    parser.add_argument('--list-accounts', dest = "list_accounts", action="store_true", 
                        help='gets a list of known accounts (Contacts).')
    parser.add_argument('--list-drafts', dest = "list_drafts", action="store_true", 
                        help='gets a list of stored drafts.')
    parser.add_argument('--daemon-info', dest = "daemon_info", action="store_true", 
                        help='gets useful information of the daemon running on host defined in flag --server.')
    parser.add_argument('--set-alias', dest = "alias", type=str, metavar='ALIAS',
                        help='sets alias of the device running in SRV.')
    parser.add_argument('--list-peers', dest = "list_peers", action="store_true",
                        help='List peers with connection status STATUS')
    parser.add_argument('--peer-info', dest = "peer_info", type=str, metavar='CID',
                        help='gets information from given peer encoded CID.')
    parser.add_argument('--get-publication', dest = "publication_id", type=str, metavar='CID',
                        help='gets remote publication given its <docuemntID>/<version>')
    parser.add_argument('--server', dest='server', type=str, default="localhost:55002", metavar='SRV',
                        help='gRPC server address in the format <IP>:<port>.')
    
    args = parser.parse_args()
    try:
        my_client = client(args.server)
    except Exception as e:
        print("Could not connect to provided server: "+str(e))
        sys.exit(1)
    if args.sync:
        my_client.forceSync(quiet=args.quiet)
    elif args.peer_connect != []:
        my_client.connect(args.peer_connect, quiet=args.quiet)
    elif args.peer_info:  
        my_client.peerInfo(args.peer_info, quiet=args.quiet)
    elif args.list_publications:
        my_client.list_publications(quiet=args.quiet)
    elif args.list_members:  
        my_client.list_members(quiet=args.quiet, headers=args.headers)
    elif args.get_member:  
        my_client.get_member(args.get_member, quiet=args.quiet, headers=args.headers)
    elif args.delete_member:  
        my_client.delete_member(args.delete_member, quiet=args.quiet, headers=args.headers)
    elif args.add_site:
        my_client.add_site(args.add_site, args.token, quiet=args.quiet)
    elif args.list_accounts:
        my_client.list_accounts(quiet=args.quiet)
    elif args.del_site:
        my_client.remove_site(args.del_site, quiet=args.quiet)
    elif args.list_sites:
        my_client.list_sites(quiet=args.quiet)
    elif args.list_drafts:
        my_client.list_drafts(quiet=args.quiet)
    elif args.update_site_info:
        my_client.update_site_info(args.title, args.description, quiet=args.quiet, headers=args.headers)
    elif args.get_site_info:
        my_client.get_site_info(quiet=args.quiet, headers=args.headers)
    elif args.create_document:
        my_client.create_document(title=args.title if args.title != None and args.title != "" else args.create_document, body=args.create_document)
    elif args.create_token:
        my_client.create_token(args.create_token, quiet=args.quiet, headers=args.headers)
    elif args.redeem_token:
        my_client.redeem_token(args.redeem_token, quiet=args.quiet, headers=args.headers)
    elif args.get_path != None:
        my_client.get_path(path=args.get_path, quiet=args.quiet, headers=args.headers)
    elif args.list_document_records:
        my_client.list_document_records(args.list_document_records, args.version, quiet=args.quiet)
    elif args.list_web_publications:
        my_client.list_web_publications(quiet=args.quiet, headers=args.headers)
    elif args.trust_account:
        my_client.trust_untrust(quiet=args.quiet, acc_id = args.trust_account, is_trusted=True)
    elif args.untrust_account:
        my_client.trust_untrust(quiet=args.quiet, acc_id = args.untrust_account, is_trusted=False)
    elif args.daemon_info:
        my_client.daemonInfo(quiet=args.quiet)
    elif args.publish:
        my_client.publish(args.publish, args.version, args.path, quiet=args.quiet, headers=args.headers)
    elif args.unpublish:
        my_client.unpublish(args.unpublish, args.version, quiet=args.quiet, headers=args.headers)
    elif args.publication_id:  
        my_client.get_publication(args.publication_id, quiet=args.quiet)
    elif args.mnemonics != []:
        my_client.register(args.mnemonics, quiet=args.quiet)
    elif args.alias:
        my_client.set_alias(alias=args.alias, quiet=args.quiet)
    elif args.get_profile != None:
        my_client.get_profile(acc_id=args.get_profile, quiet=args.quiet)
    elif args.get_account != None:
        my_client.account_info(quiet=args.quiet, acc_id=args.get_account)
    elif args.list_peers != None:
        my_client.list_peers(quiet=args.quiet)
    del my_client
    
if __name__ == "__main__":
    main()
