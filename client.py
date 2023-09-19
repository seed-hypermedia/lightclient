#!/usr/bin/env python3
from daemon.v1alpha import daemon_pb2
from daemon.v1alpha import daemon_pb2_grpc
from networking.v1alpha import networking_pb2
from networking.v1alpha import networking_pb2_grpc
from documents.v1alpha import documents_pb2
from documents.v1alpha import documents_pb2_grpc
from p2p.v1alpha import p2p_pb2
from p2p.v1alpha import p2p_pb2_grpc
from accounts.v1alpha import accounts_pb2
from accounts.v1alpha import accounts_pb2_grpc
from groups.v1alpha import groups_pb2
from groups.v1alpha import groups_pb2_grpc
from groups.v1alpha import website_pb2
from groups.v1alpha import website_pb2_grpc
import grpc
import argparse
import sys
from datetime import datetime
class client():
    def __init__(self, server="localhost:55002"):
        self.__channel = grpc.insecure_channel(server)
        self._daemon = daemon_pb2_grpc.DaemonStub(self.__channel)
        self._p2p = p2p_pb2_grpc.P2PStub(self.__channel)
        self._networking = networking_pb2_grpc.NetworkingStub(self.__channel)
        self._accounts = accounts_pb2_grpc.AccountsStub(self.__channel)
        self._publications = documents_pb2_grpc.PublicationsStub(self.__channel)
        self._drafts = documents_pb2_grpc.DraftsStub(self.__channel)
        self._website = website_pb2_grpc.WebsiteStub(self.__channel)
        self._groups= groups_pb2_grpc.GroupsStub(self.__channel)

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
    
    def get_site_info(self, headers=[]):
        metadata = [tuple(h.split("=")) for h in headers if h.count('=') == 1]
        try:
            res = self._remotesite.GetSiteInfo(web_publishing_pb2.GetSiteInfoRequest(), metadata=metadata)
        except Exception as e:
            print("get_site_info error: "+str(e))
            return
        print("Hostname: "+res.hostname)
        print("Title: "+res.title)
        print("Description: "+res.description)
        print("Owner: "+res.owner)

    # Sites
    def init_site(self, secret_link, group_eid):   
        try:
            res = self._website.InitializeServer(website_pb2.InitializeServerRequest(secret=secret_link, group_id=group_eid))
        except Exception as e:
            print("init_site error: "+str(e))
            return
        print(res.id)

    def site_info(self):   
        try:
            res = self._website.GetSiteInfo(website_pb2.GetSiteInfoRequest())
        except Exception as e:
            print("init_site error: "+str(e))
            return
        print("Group EID :"+str(res.group_id))
        print("Group Version :"+str(res.group_version))
        print("Site PeerID:"+str(res.peer_info.peer_id))
        print("Site Address :"+str(res.peer_info.addrs))

    # Groups 
    def create_group(self, title, description = "", url=""):   
        try:
            res = self._groups.CreateGroup(groups_pb2.CreateGroupRequest(title=title, description=description, site_setup_url=url))
        except Exception as e:
            print("create_group error: "+str(e))
            return
        print(res.id)
    
    def list_groups(self):   
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

    # Documents
    def create_document(self, title, body=""):
        try:
            draft = self._drafts.CreateDraft(documents_pb2.CreateDraftRequest())
        except Exception as e:
            print("draft error: "+str(e))
            return
    
        try:
            changes = [documents_pb2.DocumentChange(set_title=title)]
            changes += [documents_pb2.DocumentChange(move_block=documents_pb2.DocumentChange.MoveBlock(block_id="b1"))]
            changes += [documents_pb2.DocumentChange(replace_block=documents_pb2.Block(id="b1",text=body,type="paragraph"))]
            self._drafts.UpdateDraft(documents_pb2.UpdateDraftRequest(document_id=draft.id, changes=changes))
        except Exception as e:
            print("updating document error: "+str(e))
            return

        try:
            publication = self._drafts.PublishDraft(documents_pb2.PublishDraftRequest(document_id=draft.id))
        except Exception as e:
            print("publishing document error: "+str(e))
            return
        print(f"{draft.id}?v={publication.version}")
    
    def get_publication(self, eid, local_only=False, trusted_only=False):
        try:
            cid_list = eid.split("?v=")
            if len(cid_list)==1:
                res = self._publications.GetPublication(documents_pb2.GetPublicationRequest(document_id=eid.split("?v=")[0], local_only=local_only, trusted_only=trusted_only))
            else:    
                res = self._publications.GetPublication(documents_pb2.GetPublicationRequest(document_id=eid.split("?v=")[0], version=eid.split("?v=")[1], local_only=local_only, trusted_only=trusted_only))
        except Exception as e:
            print("get_publication error: "+str(e))
            return
        print("Version :"+str(res.version))
        print("Document :"+str(res.document))

    def list_publications(self, trusted_only=False, list_formatting=True):
        try:
            res = self._publications.ListPublications(documents_pb2.ListPublicationsRequest(trusted_only=trusted_only))
        except Exception as e:
            print("list_publications error: "+str(e))
            return
        if not list_formatting:
            for p in res.publications:
                print("EID :"+str(p.document.id))
                print("Version :"+str(p.version))
                print("Title :"+str(p.document.title))
                print("Creator :"+str(p.document.author))
                print("Updated time :"+str(p.document.update_time))
        else:
            print("{:<29}|{:<10}|{:<12}|{:<10}|{:<19}|".format('EID','Version','Title','Creator','Updated time'))
            print(''.join(["-"]*29+["|"]+["-"]*10+['|']+["-"]*12+["|"]+["-"]*10+["|"]+["-"]*19+["|"]))
            for p in res.publications:
                print("{:<29}|{:<10}|{:<12}|{:<10}|{:<19}|".format(self._trim(p.document.id,29,trim_ending=False),
                                                     self._trim(p.version,10,trim_ending=False),
                                                     self._trim(p.document.title,12,trim_ending=True),
                                                     self._trim(p.document.author,10,trim_ending=False),
                                                     self._trim(p.document.create_time.ToDatetime().strftime("%Y-%m-%d %H:%M:%S"),19,trim_ending=False)))

    def list_drafts(self):
        try:
            drafts = self._drafts.ListDrafts(documents_pb2.ListDraftsRequest())
        except Exception as e:
            print("list_drafts error: "+str(e))
            return
        print("{:<72}|{:<20}|".format('ID','Title'))
        print(''.join(["-"]*72+['|']+["-"]*20+["|"]))
        for d in drafts.documents:
            print("ID :"+str(d.id))
            print("Document :"+str(d.title))

    # Daemon
    def daemon_info(self):
        try:
            res = self._daemon.GetInfo(daemon_pb2.GetInfoRequest())
        except Exception as e:
            print("daemon_info error: "+str(e))
            return
        print("Account ID: "+str(res.account_id))
        print("Device ID:  "+str(res.device_id))
        print("Start time: "+str(res.start_time.ToDatetime())+" UTC")

    def force_sync(self):
        try:
            res = self._daemon.ForceSync(daemon_pb2.ForceSyncRequest())
        except Exception as e:
            print("force_sync error: "+str(e))
            return
        print("force_sync OK:"+str(res))

    def register(self, mnemonics, passphrase = ""):
        try:
            res = self._daemon.Register(daemon_pb2.RegisterRequest(mnemonic=mnemonics, passphrase=passphrase))
        except Exception as e:
            print("register error: "+str(e))
            return
        print("registered account_id :"+str(res.account_id))

    def set_alias(self, alias = ""):
        try:
            account = self._accounts.UpdateProfile(accounts_pb2.Profile(alias=alias))
        except Exception as e:
            print("update profile error: "+str(e))
            return
        print("new alias: "+str(account.profile.alias))

    # Networking
    def list_peers(self):
        try:
            res = self._networking.ListPeers(networking_pb2.ListPeersRequest())
        except Exception as e:
            print("list_peers error: "+str(e))
            return
        print("{:<20}|{:<20}|{:<20}|".format('AccountID','PeerID','Status'))
        print(''.join(["-"]*20+['|']+["-"]*20+["|"]+["-"]*20+["|"]))
        for peer in res.peers:
            print("{:<20}|{:<20}|{:<20}|".format(self._trim(peer.account_id,20,trim_ending=False),
                                                    self._trim(peer.id,20,trim_ending=False),
                                                    self._trim(self._status2string(peer.connection_status),20)))

    def peer_info(self, cid, dict_output=False):
        try:
            res = self._networking.GetPeerInfo(networking_pb2.GetPeerInfoRequest(device_id=cid))
        except Exception as e:
            print("peer_info error: "+str(e))
            return
        if not dict_output:
            print("Addresses :"+str(res.addrs))
            print("Account id :"+str(res.account_id))
            print("Status :"+str(res.connection_status))
        else:
            return {"account id": str(res.account_id), "addresses":str(res.addrs), "connection status": self._status2string(res.connection_status)}
        
    def get_profile(self, acc_id = ""):
        try:
            account = self._accounts.GetAccount(accounts_pb2.GetAccountRequest(id=acc_id))
        except Exception as e:
            print("Getting account error: "+str(e))
            return
        print("Alias: "+str(account.profile.alias))
        print("Bio: "+str(account.profile.bio))
        print("Avatar: "+str(account.profile.avatar))
        
    def connect(self, addrs):
        if type(addrs) != list:
            print("addrs must be a list")
            return
        try:
            res = self._networking.Connect(networking_pb2.ConnectRequest(addrs=addrs))
        except Exception as e:
            print("connect error: "+str(e))
            return
        print("connect response:"+str(res))

    # Accounts
    def account_info(self, acc_id = ""):
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
    
    def list_accounts(self):
        try:
            accounts = self._accounts.ListAccounts(accounts_pb2.ListAccountsRequest())
        except Exception as e:
            print("Getting account error: "+str(e))
            return
        
        print("{:<20}|{:<20}|{:<25}|{:<10}|".format('ID','Alias','Bio','isTrusted'))
        print(''.join(["-"]*20+['|']+["-"]*20+['|']+["-"]*25+["|"]+["-"]*10+["|"]))
        for account in accounts.accounts:
            print("{:<20}|{:<20}|{:<25}|{:<10}|".format(self._trim(account.id,20,trim_ending=False),
                                                        self._trim(account.profile.alias,20,trim_ending=False),
                                                        self._trim(account.profile.bio,25,trim_ending=False), 
                                                        self._trim(str(account.is_trusted).replace("0","Trusted").replace("1","Untrusted"),10)))

def main():
    """basic gRPC client that sends commands to a remote gRPC server

    Returns:
        int: return code 0 on success -1 on error
    """
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

    # Documents
    document_parser = subparsers.add_parser(name = "document", help='Document related functionality (create, drafts, get, ...)')
    document_subparser = document_parser.add_subparsers(title="Manage Documents", required=True, dest="command",
                                                        description= "Everything related to document creation and fetching.", 
                                                        help='documents sub-commands')
    create_document_parser = document_subparser.add_parser(name = "create", help='Create a one-block document.')
    create_document_parser.add_argument('body', type=str, help="document's body. Can contain linebreaks")
    create_document_parser.add_argument('--title', '-t', type=str, help="sets document's title.")
    create_document_parser.set_defaults(func=create_document)

    get_publication_parser = document_subparser.add_parser(name = "get", help='Gets any given publication')
    get_publication_parser.add_argument('EID', type=str, metavar='eid', help='Fully qualified ID')
    get_publication_parser.add_argument('--local-only', '-l', action="store_true",
                        help='find the document only locally')
    get_publication_parser.add_argument('--trusted-only', '-t', action="store_true",
                        help='get the publication from a trusted only source')
    get_publication_parser.set_defaults(func=get_publication)

    list_publications_parser = document_subparser.add_parser(name = "list", help='Lists all known publications.')
    list_publications_parser.add_argument('--trusted-only', '-t', action="store_true",
                        help='list publications from trusted sources only')
    list_publications_parser.set_defaults(func=list_publications)

    print_publications_parser = document_subparser.add_parser(name = "print-all", help='Prints all publications.')
    print_publications_parser.add_argument('--trusted-only', '-t', action="store_true",
                        help='print publications from trusted sources only')
    print_publications_parser.set_defaults(func=print_publications)

    list_drafts_parser = document_subparser.add_parser(name = "list-drafts", help='gets a list of stored drafts.')
    list_drafts_parser.set_defaults(func=list_drafts)
    
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
    daemon_register_parser.set_defaults(func=daemon_register)
    
    # Accounts
    account_parser = subparsers.add_parser(name = "account", help='Account related functionality (Trusted, info,...)')
    account_parser.add_argument('info', type=str, const = "",
                        help='gets information from provided account. Own account if no extra argument is provided', nargs='?')
    account_parser.add_argument('list', action="store_true", 
                        help='gets a list of known accounts (Contacts) without including ourselves.')
    account_parser.add_argument("trust", type=str,
                        help="Trust provided account. Self account is trusted by default.")
    account_parser.add_argument("untrust", type=str,
                        help="Untrust provided account. Cannot untrust self.")
    
    # Network
    network_parser = subparsers.add_parser(name = "network", help='Network related functionality (Connect, Profile, peers,...)')
    network_parser.add_argument('get-profile', type=str, const="", 
                        help='gets profile information from provided account. Own profile if no extra argument is provided.' , nargs='?')
    network_parser.add_argument('connect', type=str, default=[], nargs='+',
                        help='connects to the given multiaddresses')
    network_parser.add_argument('list-peers', action="store_true",
                        help='List peers with connection status STATUS')
    network_parser.add_argument('peer-info', type=str, 
                        help='gets information from given peer encoded EID.')
    network_parser.add_argument('set-alias', type=str,
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


def network(args):
    print("not ready yet")
    return
    my_client = get_client(args.server)
    if args.connect != []:
        my_client.connect(args.connect)
    elif args.peer_info:  
        my_client.peer_info(args.peer_info)
    elif args.get_profile != None:
        my_client.get_profile(acc_id=args.get_profile)
    elif args.list_peers != None:
        my_client.list_peers()
    elif args.set_alias:
        my_client.set_alias(alias=args.set_alias)
    del my_client

def account(args):
    print("not ready yet")
    return
    my_client = get_client(args.server)
    if args.list:
        my_client.list_accounts()
    elif args.info != None:
        my_client.account_info(acc_id=args.info)
    elif args.trust != None:
        my_client.trust_untrust(acc_id=args.trust, is_trusted=True)
    elif args.untrust != None:
        my_client.trust_untrust(acc_id=args.untrust, is_trusted=False)
    del my_client

# Daemon
def daemon_info(args):
    my_client = get_client(args.server)
    my_client.daemon_info()
    del my_client

def daemon_sync(args):
    my_client = get_client(args.server)
    my_client.force_sync()
    del my_client

def daemon_register(args):
    my_client = get_client(args.server)
    my_client.register(args.words)
    del my_client

# Sites
def init_site(args):
    my_client = get_client(args.server)
    my_client.init_site(args.secret_url, args.group_eid)
    del my_client

def site_info(args):
    my_client = get_client(args.server)
    my_client.site_info()
    del my_client

# Groups
def create_group(args):
    my_client = get_client(args.server)
    my_client.create_group(title=args.title, description=args.description, url=args.setup_url)
    del my_client

def list_groups(args):
    my_client = get_client(args.server)
    my_client.list_groups()
    del my_client

# Documents
def create_document(args):
    my_client = get_client(args.server)
    my_client.create_document(title=args.title if args.title != None and args.title != "" else args.body.split(" ")[0], body=args.body)
    del my_client

def get_publication(args):
    my_client = get_client(args.server)
    my_client.get_publication(args.EID, args.local_only, args.trusted_only)
    del my_client

def list_publications(args):
    my_client = get_client(args.server)
    my_client.list_publications(args.trusted_only, list_formatting=True)
    del my_client

def print_publications(args):
    my_client = get_client(args.server)
    my_client.list_publications(args.trusted_only, list_formatting=False)
    del my_client

def list_drafts(args):
    my_client = get_client(args.server)
    my_client.list_drafts()
    del my_client


if __name__ == "__main__":
    main()
