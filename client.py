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

    def get_publication(self, eid, local_only=False, trusted_only=False, quiet=False):
        try:
            cid_list = eid.split("?v=")
            if len(cid_list)==1:
                res = self._publications.GetPublication(documents_pb2.GetPublicationRequest(document_id=eid.split("?v=")[0], local_only=local_only, trusted_only=trusted_only))
            else:    
                res = self._publications.GetPublication(documents_pb2.GetPublicationRequest(document_id=eid.split("?v=")[0], version=eid.split("?v=")[1], local_only=local_only, trusted_only=trusted_only))
        except Exception as e:
            print("get_publication error: "+str(e))
            return
        if not quiet:
            print("Version :"+str(res.version))
            print("Document :"+str(res.document))

    def list_publications(self, trusted_only=False, quiet=False):
        try:
            res = self._publications.ListPublications(documents_pb2.ListPublicationsRequest(trusted_only=trusted_only))
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
            print("{:<20}|{:<20}|{:<25}|{:<10}|".format('ID','Alias','Bio','isTrusted'))
            print(''.join(["-"]*20+['|']+["-"]*20+['|']+["-"]*25+["|"]+["-"]*10+["|"]))
            for account in accounts.accounts:
                print("{:<20}|{:<20}|{:<25}|{:<10}|".format(self._trim(account.id,20,trim_ending=False),
                                                            self._trim(account.profile.alias,20,trim_ending=False),
                                                            self._trim(account.profile.bio,25,trim_ending=False), 
                                                            self._trim(str(account.is_trusted).replace("0","Trusted").replace("1","Untrusted"),10)))


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
    subparsers = parser.add_subparsers(help='sub-command help', required=True)
    
    document_parser = subparsers.add_parser(name = "document", help='Document related functionality (create, drafts, get, ...)')

    account_parser = subparsers.add_parser(name = "account", help='Account related functionality (Trusted, info,...)')

    site_parser = subparsers.add_parser(name = "site", help='Sites related functionality (Add, list, members, ...)')
    site_subparser = site_parser.add_subparsers(help='sub-commands for members', dest='subparser_name')
    member_parser = site_subparser.add_parser(name = "member", help='Site member related functionality (remove, list, invite, ...)')

    network_parser = subparsers.add_parser(name = "network", help='Network related functionality (Connect, Profile, peers,...)')
    daemon_parser = subparsers.add_parser(name = "daemon", help='Daemon related functionality (Sync, Register, Alias, ...)')

    # General
    parser.add_argument("--quiet", action="store_true",  help="Suppress output")
    
    parser.add_argument('--server', dest='server', type=str, default="localhost:55002", metavar='SRV',
                        help='gRPC server address <IP>:<port>.')
    
    # Site
    site_parser.add_argument('--headers', dest = "headers", type=str, default=[], metavar='KEY=VALUE',nargs='+',
                        help='Adds key:value header to the gRPC call. Multiple headers can be defined separated by blank space')
    site_parser.add_argument('add', type=str,
                        help='adds the given hostname.')
    site_parser.add_argument('--token', type=str,
                        help='append an invitational TOKEN to the add call.')
    site_parser.add_argument('remove', type=str,
                        help='removes a site located in HOSTNAME.')
    #site_parser.add_argument('info', action="store_true",
    #                    help='gets site info.')
    #site_parser.add_argument('update-info', action="store_true",
    #                    help='updates site info with TITLE and DESCRIPTION optional flags.')
    site_parser.add_argument('--title', type=str,
                        help='sets (updates) a title to a given site.')
    site_parser.add_argument('--description', '-d', type=str,
                        help='sets (updates) a description to a given site.')
    #site_parser.add_argument('list-web-publications', action="store_true",
    #                    help='List all available published documents on the site')
    site_parser.add_argument('list-document-records', type=str, metavar='ID',
                        help='List all records (in all known sites) for any given document ID and optional VERSION')
    site_parser.add_argument('get-path', type=str, nargs='?', const="/",
                        help='Get the publication published at the provided path. If not provided, root document is assumed.')
    site_parser.add_argument('publish', type=str,
                        help='Publish a document with ID and optional VERSION and PATH')
    site_parser.add_argument('unpublish', type=str, metavar='ID',
                        help='Remove a published a document with ID and optional VERSION')
    site_parser.add_argument("list",  action="store_true",  help="List added sites")
    site_parser.add_argument('--version', type=str,
                        help='Optional version to publish a document with')
    site_parser.add_argument('--path', type=str,
                        help='Optional pretty path to publish a document with')
    
    member_parser.add_argument('create-token', type=str,
                        nargs='?', help='Create an invite token with an optional role. editor | owner')
    member_parser.add_argument('redeem-token', type=str,
                        help='Redeem the providedtoken')
    member_parser.add_argument("list", action="store_true",  help="List site members")
    member_parser.add_argument("get", type=str,
                        help="Get info about specific site member represented by its accountID")
    member_parser.add_argument("delete", type=str,
                        help="Removes an specific member represented by its accountID")
    
    # Documents
    document_subparser = document_parser.add_subparsers(title="Document commands", required=True,
                                                        description= "Everything related to document creation and fetching", 
                                                        help='documents sub-commands')
    create_parser = document_subparser.add_parser(name = "create", help='Create a one-block document.')
    create_parser.add_argument('body', type=str, help="document's body. Can contain linebreaks")
    create_parser.add_argument('--title', '-t', type=str, help="sets document's title.")
    create_parser.set_defaults(func=create)

    get_publication_parser = document_subparser.add_parser(name = "get-publication", help='gets remote publication')
    get_publication_parser.add_argument('EID', type=str, metavar='eid', help='Fully qualified ID')
    get_publication_parser.add_argument('--local-only', '-l', action="store_true",
                        help='find the document only locally')
    get_publication_parser.add_argument('--trusted-only', '-t', action="store_true",
                        help='get the publication from a trusted only source')
    get_publication_parser.set_defaults(func=get_publication)

    list_publications_parser = document_subparser.add_parser(name = "list-publications", help='gets a list of own publications.')
    list_publications_parser.add_argument('--trusted-only', '-t', action="store_true",
                        help='list publications from trusted sources only')
    list_publications_parser.set_defaults(func=list_publications)

    list_drafts_parser = document_subparser.add_parser(name = "list-drafts", help='gets a list of stored drafts.')
    list_drafts_parser.set_defaults(func=list_drafts)
    
    
    
    # Accounts
    account_parser.add_argument('info', type=str, const = "",
                        help='gets information from provided account. Own account if no extra argument is provided', nargs='?')
    account_parser.add_argument('list', action="store_true", 
                        help='gets a list of known accounts (Contacts) without including ourselves.')
    account_parser.add_argument("trust", type=str,
                        help="Trust provided account. Self account is trusted by default.")
    account_parser.add_argument("untrust", type=str,
                        help="Untrust provided account. Cannot untrust self.")
    
    # Network
    network_parser.add_argument('get-profile', type=str, const="", 
                        help='gets profile information from provided account. Own profile if no extra argument is provided.' , nargs='?')
    network_parser.add_argument('connect', type=str, default=[], nargs='+',
                        help='connects to the given multiaddresses')
    network_parser.add_argument('list-peers', action="store_true",
                        help='List peers with connection status STATUS')
    network_parser.add_argument('peer-info', type=str, 
                        help='gets information from given peer encoded EID.')

    # Daemon
    daemon_parser.add_argument('info', action="store_true", 
                        help='gets useful information of the daemon running on host defined in flag --server.')
    daemon_parser.add_argument("sync", action="store_true",  help="Forces a sync loop on the server")
    daemon_parser.add_argument('register', type=str, default=[], nargs='+',
                        help='registers the device under the account taken from the provided mnemonics.')
    daemon_parser.add_argument('set-alias', type=str,
                        help='sets alias of the device running in SRV.')
    
    args = parser.parse_args()
    args.func(args)

def get_client(server):
    try:
        my_client = client(server)
    except Exception as e:
        print("Could not connect to provided server: "+str(e))
        sys.exit(1)
    return my_client

def daemon(args):
    my_client = get_client(args.server)
    if args.sync:
        my_client.forceSync(quiet=args.quiet)
    elif args.info:
        my_client.daemonInfo(quiet=args.quiet)
    elif args.register != []:
        my_client.register(args.register, quiet=args.quiet)
    elif args.set_alias:
        my_client.set_alias(alias=args.set_alias, quiet=args.quiet)
    del my_client

def network(args):
    my_client = get_client(args.server)
    if args.connect != []:
        my_client.connect(args.connect, quiet=args.quiet)
    elif args.peer_info:  
        my_client.peerInfo(args.peer_info, quiet=args.quiet)
    elif args.get_profile != None:
        my_client.get_profile(acc_id=args.get_profile, quiet=args.quiet)
    elif args.list_peers != None:
        my_client.list_peers(quiet=args.quiet)
    del my_client

def account(args):
    my_client = get_client(args.server)
    if args.list:
        my_client.list_accounts(quiet=args.quiet)
    elif args.info != None:
        my_client.account_info(quiet=args.quiet, acc_id=args.info)
    elif args.trust != None:
        my_client.trust_untrust(quiet=args.quiet, acc_id=args.trust, is_trusted=True)
    elif args.untrust != None:
        my_client.trust_untrust(quiet=args.quiet, acc_id=args.untrust, is_trusted=False)
    del my_client

def create(args):
    my_client = get_client(args.server)
    my_client.create_document(title=args.title if args.title != None and args.title != "" else args.body.split(" ")[0], body=args.body)
    del my_client

def get_publication(args):
    my_client = get_client(args.server)
    my_client.get_publication(args.EID, args.local_only, args.trusted_only, quiet=args.quiet)
    del my_client

def list_publications(args):
    my_client = get_client(args.server)
    my_client.list_publications(args.trusted_only, quiet=args.quiet)
    del my_client

def list_drafts(args):
    my_client = get_client(args.server)
    my_client.list_drafts(quiet=args.quiet)
    del my_client

def site(args):
    my_client = get_client(args.server)
    if args.info:
        my_client.get_site_info(quiet=args.quiet, headers=args.headers)
    elif args.list_publications:
        my_client.list_publications(quiet=args.quiet)
    elif args.add:
        my_client.add_site(args.add, args.token, quiet=args.quiet)
    elif args.remove:
        my_client.remove_site(args.remove, quiet=args.quiet)
    elif args.list:
        my_client.list_sites(quiet=args.quiet)
    elif args.update_info:
        my_client.update_site_info(args.title, args.description, quiet=args.quiet, headers=args.headers)
    elif args.get_path != None:
        my_client.get_path(path=args.get_path, quiet=args.quiet, headers=args.headers)
    elif args.list_document_records:
        my_client.list_document_records(args.list_document_records, args.version, quiet=args.quiet)
    elif args.list_web_publications:
        my_client.list_web_publications(quiet=args.quiet, headers=args.headers)
    elif args.publish:
        my_client.publish(args.publish, args.version, args.path, quiet=args.quiet, headers=args.headers)
    elif args.unpublish:
        my_client.unpublish(args.unpublish, args.version, quiet=args.quiet, headers=args.headers)
    del my_client

def member(args):
    my_client = get_client(args.server)
    if args.list:  
        my_client.list_members(quiet=args.quiet, headers=args.headers)
    elif args.get:  
        my_client.get_member(args.get, quiet=args.quiet, headers=args.headers)
    elif args.delete:  
        my_client.delete_member(args.delete, quiet=args.quiet, headers=args.headers)
    elif args.create_token:
        my_client.create_token(args.create_token, quiet=args.quiet, headers=args.headers)
    elif args.redeem_token:
        my_client.redeem_token(args.redeem_token, quiet=args.quiet, headers=args.headers)
    del my_client
if __name__ == "__main__":
    main()
