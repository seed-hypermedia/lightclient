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
        self._documents = documents_pb2_grpc.PublicationsStub(self.__channel)
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
    
    def get_path(self, path="/", quiet=False, headers=[]):
        metadata = [tuple(h.split("=")) for h in headers if h.count('=') == 1]
        if path =="":path ="/"
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
            print("{:<25}|{:<25}|{:<15}|{:<25}|".format('ID','Version','Hostname','Path'))
            print(''.join(["-"]*25+['|']+["-"]*25+["|"]+["-"]*15+['|']+["-"]*25+["|"]))
            for record in res.publications:
                print("{:<25}|{:<25}|{:<15}|{:<25}|".format(record.document_id,record.version,record.hostname,record.path))
    
    def list_web_publications(self, quiet=False, headers=[]):
        metadata = [tuple(h.split("=")) for h in headers if h.count('=') == 1]
        try:
            res = self._remotesite.ListWebPublications(web_publishing_pb2.ListWebPublicationsRequest(), metadata=metadata)
        except Exception as e:
            print("list_web_publications error: "+str(e))
            return
        if not quiet:
            print("{:<62}|{:<9}|{:<7}|{:<15}|".format('ID','Path', 'Version','Hostname'))
            print(''.join(["-"]*62+['|']+["-"]*9+["|"]+["-"]*7+['|']+["-"]*15+["|"]))
            for record in res.publications:
                print("{:<62}|{:<9}|{:<7}|{:<15}|".format(record.document_id,record.path, record.version,record.hostname))
    
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
            print("{:<25}|{:<10}|".format('Hostname','Role'))
            print(''.join(["-"]*25+['|']+["-"]*10+["|"]))
            for s in ret.sites:
                if s.role == 2:
                    role = "editor"
                elif s.role==1:
                    role = "owner"
                else:
                    role = "unspecified"
                print("{:<25}|{:<10}|".format(s.hostname, role))
    
    def forceSync(self, quiet=False):
        try:
            res = self._daemon.ForceSync(daemon_pb2.ForceSyncRequest())
        except Exception as e:
            print("forceSync error: "+str(e))
            return
        if not quiet:
            print("forceSync OK:"+str(res))

    def peerInfo(self, cid, quiet=False):
        try:
            res = self._networking.GetPeerInfo(networking_pb2.GetPeerInfoRequest(peer_id=cid))
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
                res = self._documents.GetPublication(documents_pb2.GetPublicationRequest(document_id=cid.split("/")[0]))
            else:    
                res = self._documents.GetPublication(documents_pb2.GetPublicationRequest(document_id=cid.split("/")[0], version=cid.split("/")[1]))
        except Exception as e:
            print("get_publication error: "+str(e))
            return
        if not quiet:
            print("Version :"+str(res.version))
            print("Document :"+str(res.document))

    def list_publications(self, quiet=False):
        try:
            res = self._documents.ListPublications(documents_pb2.ListPublicationsRequest())
        except Exception as e:
            print("list_publications error: "+str(e))
            return
        if not quiet:
            for p in res.publications:
                print("Version :"+str(p.version))
                print("Document :"+str(p.document))
                
    def list_members(self, quiet=False, headers=[]):
        metadata = [tuple(h.split("=")) for h in headers if h.count('=') == 1]
        try:
            res = self._remotesite.ListMembers(web_publishing_pb2.ListMembersRequest(), metadata=metadata)
        except Exception as e:
            print("list_members error: "+str(e))
            return
        if not quiet:
            print("{:<72}|{:<10}|".format('AccountID','Role'))
            print(''.join(["-"]*72+['|']+["-"]*10+["|"]))
            for s in res.members:
                print("{:<72}|{:<10}|".format(s.account_id, self._role_to_str(s.role)))


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

    def get_profile(self, quiet=False):
        try:
            account = self._accounts.GetAccount(accounts_pb2.GetAccountRequest())
        except Exception as e:
            print("Getting account error: "+str(e))
            return
        if not quiet:
            print("Alias: "+str(account.profile.alias))
            print("Bio: "+str(account.profile.bio))
            print("Email: "+str(account.profile.email))

    def peer_info(self, id, quiet=False):
        try:
            res = self._networking.GetPeerInfo(networking_pb2.GetPeerInfoRequest(peer_id=id))
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
                        help='Adds key:value header to the gRPC call. Multiple headers can me defined separated by blank space')
    parser.add_argument('--add-site', dest = "add_site", type=str, metavar='HOSTNAME',
                        help='adds a site located in HOSTNAME with an optional invite TOKEN.')
    parser.add_argument('--token', dest = "token", type=str, metavar='TOKEN',
                        help='append an invitational TOKEN to the --add-site call.')
    parser.add_argument('--remove-site', dest = "del_site", type=str, metavar='HOSTNAME',
                        help='removes a site located in HOSTNAME.')
    parser.add_argument('--get-site-info', dest = "get_site_info", action="store_true",
                        help='gets site info.')
    parser.add_argument('--update-site-info', dest = "update_site_info", action="store_true",
                        help='updates site info with TITLE and DESCRIPTION optional flags.')
    parser.add_argument('--title', dest = "title", type=str, metavar='TITLE',
                        help='sets (updates) a title to a given site.')
    parser.add_argument('--description', dest = "description", type=str, metavar='DESCRIPTION',
                        help='sets (updates) a description to a given site.')
    parser.add_argument('--create-token', dest = "create_token", type=str, metavar='ROLE',
                        nargs='?', help='Create an invite token with an optional role editor | owner')
    parser.add_argument('--redeem-token', dest = "redeem_token", type=str, metavar='TOKEN',
                        help='Redeem TOKEN if it is a valid token')
    parser.add_argument('--list-web-publications', dest = "list_web_publications", action="store_true",
                        help='List all available published documents on the site')
    parser.add_argument('--list-document-records', dest = "list_document_records", type=str, metavar='ID',
                        help='List all records (in all known sites) for any given document ID and optional VERSION')
    parser.add_argument('--get-path', dest = "get_path", action="store_true",
                        help='Get a publication with an optional PATH. If not provided --path flag, then root document assumed')
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
    parser.add_argument('--account-info', dest = "get_account", action="store_true", 
                        help='gets information from own account.')
    parser.add_argument('--get-profile', dest = "get_profile", action="store_true", 
                        help='gets profile information.')
    parser.add_argument('--list-publications', dest = "list_publications", action="store_true", 
                        help='gets a list of own publications.')
    parser.add_argument('--set-alias', dest = "alias", type=str, metavar='ALIAS',
                        help='sets alias of the device running in SRV.')
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
    elif args.del_site:
        my_client.remove_site(args.del_site, quiet=args.quiet)
    elif args.list_sites:
        my_client.list_sites(quiet=args.quiet)
    elif args.update_site_info:
        my_client.update_site_info(args.title, args.description, quiet=args.quiet, headers=args.headers)
    elif args.get_site_info:
        my_client.get_site_info(quiet=args.quiet, headers=args.headers)
    elif args.create_token:
        my_client.create_token(args.create_token, quiet=args.quiet, headers=args.headers)
    elif args.redeem_token:
        my_client.redeem_token(args.redeem_token, quiet=args.quiet, headers=args.headers)
    elif args.get_path:
        my_client.get_path(path=args.path, quiet=args.quiet, headers=args.headers)
    elif args.list_document_records:
        my_client.list_document_records(args.list_document_records, args.version, quiet=args.quiet)
    elif args.list_web_publications:
        my_client.list_web_publications(quiet=args.quiet, headers=args.headers)
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
    elif args.get_profile:
        my_client.get_profile(quiet=args.quiet)
    elif args.get_account:
        my_client.account_info(quiet=args.quiet)
    del my_client
    
if __name__ == "__main__":
    main()
