# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from entities.v1alpha import entities_pb2 as entities_dot_v1alpha_dot_entities__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class EntitiesStub(object):
    """Provides functionality to query information about Hypermedia Entities.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetChange = channel.unary_unary(
                '/com.mintter.entities.v1alpha.Entities/GetChange',
                request_serializer=entities_dot_v1alpha_dot_entities__pb2.GetChangeRequest.SerializeToString,
                response_deserializer=entities_dot_v1alpha_dot_entities__pb2.Change.FromString,
                )
        self.GetEntityTimeline = channel.unary_unary(
                '/com.mintter.entities.v1alpha.Entities/GetEntityTimeline',
                request_serializer=entities_dot_v1alpha_dot_entities__pb2.GetEntityTimelineRequest.SerializeToString,
                response_deserializer=entities_dot_v1alpha_dot_entities__pb2.EntityTimeline.FromString,
                )
        self.DiscoverEntity = channel.unary_unary(
                '/com.mintter.entities.v1alpha.Entities/DiscoverEntity',
                request_serializer=entities_dot_v1alpha_dot_entities__pb2.DiscoverEntityRequest.SerializeToString,
                response_deserializer=entities_dot_v1alpha_dot_entities__pb2.DiscoverEntityResponse.FromString,
                )
        self.SearchEntities = channel.unary_unary(
                '/com.mintter.entities.v1alpha.Entities/SearchEntities',
                request_serializer=entities_dot_v1alpha_dot_entities__pb2.SearchEntitiesRequest.SerializeToString,
                response_deserializer=entities_dot_v1alpha_dot_entities__pb2.SearchEntitiesResponse.FromString,
                )
        self.DeleteEntity = channel.unary_unary(
                '/com.mintter.entities.v1alpha.Entities/DeleteEntity',
                request_serializer=entities_dot_v1alpha_dot_entities__pb2.DeleteEntityRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.ListDeletedEntities = channel.unary_unary(
                '/com.mintter.entities.v1alpha.Entities/ListDeletedEntities',
                request_serializer=entities_dot_v1alpha_dot_entities__pb2.ListDeletedEntitiesRequest.SerializeToString,
                response_deserializer=entities_dot_v1alpha_dot_entities__pb2.ListDeletedEntitiesResponse.FromString,
                )
        self.UndeleteEntity = channel.unary_unary(
                '/com.mintter.entities.v1alpha.Entities/UndeleteEntity',
                request_serializer=entities_dot_v1alpha_dot_entities__pb2.UndeleteEntityRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.ListEntityMentions = channel.unary_unary(
                '/com.mintter.entities.v1alpha.Entities/ListEntityMentions',
                request_serializer=entities_dot_v1alpha_dot_entities__pb2.ListEntityMentionsRequest.SerializeToString,
                response_deserializer=entities_dot_v1alpha_dot_entities__pb2.ListEntityMentionsResponse.FromString,
                )


class EntitiesServicer(object):
    """Provides functionality to query information about Hypermedia Entities.
    """

    def GetChange(self, request, context):
        """Gets a change by ID.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetEntityTimeline(self, request, context):
        """Gets the DAG of changes for an entity.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DiscoverEntity(self, request, context):
        """Triggers a best-effort discovery of an entity.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SearchEntities(self, request, context):
        """Finds the list of local entities whose titles match the input string.
        A fuzzy search is performed among documents, groups and accounts.
        For groups and documents, we match the title, while we match alias in accounts.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteEntity(self, request, context):
        """Deletes an entity from the local node. It removes all the patches corresponding to it, including comments.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListDeletedEntities(self, request, context):
        """Lists deleted entities.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UndeleteEntity(self, request, context):
        """Undo the entity delition by removing the entity from the deleted list. That entity, if available
        will be synced back in the next syncing round (or manually discovered).
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListEntityMentions(self, request, context):
        """List mentions of a given Entity across the locally-available content.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_EntitiesServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetChange': grpc.unary_unary_rpc_method_handler(
                    servicer.GetChange,
                    request_deserializer=entities_dot_v1alpha_dot_entities__pb2.GetChangeRequest.FromString,
                    response_serializer=entities_dot_v1alpha_dot_entities__pb2.Change.SerializeToString,
            ),
            'GetEntityTimeline': grpc.unary_unary_rpc_method_handler(
                    servicer.GetEntityTimeline,
                    request_deserializer=entities_dot_v1alpha_dot_entities__pb2.GetEntityTimelineRequest.FromString,
                    response_serializer=entities_dot_v1alpha_dot_entities__pb2.EntityTimeline.SerializeToString,
            ),
            'DiscoverEntity': grpc.unary_unary_rpc_method_handler(
                    servicer.DiscoverEntity,
                    request_deserializer=entities_dot_v1alpha_dot_entities__pb2.DiscoverEntityRequest.FromString,
                    response_serializer=entities_dot_v1alpha_dot_entities__pb2.DiscoverEntityResponse.SerializeToString,
            ),
            'SearchEntities': grpc.unary_unary_rpc_method_handler(
                    servicer.SearchEntities,
                    request_deserializer=entities_dot_v1alpha_dot_entities__pb2.SearchEntitiesRequest.FromString,
                    response_serializer=entities_dot_v1alpha_dot_entities__pb2.SearchEntitiesResponse.SerializeToString,
            ),
            'DeleteEntity': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteEntity,
                    request_deserializer=entities_dot_v1alpha_dot_entities__pb2.DeleteEntityRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'ListDeletedEntities': grpc.unary_unary_rpc_method_handler(
                    servicer.ListDeletedEntities,
                    request_deserializer=entities_dot_v1alpha_dot_entities__pb2.ListDeletedEntitiesRequest.FromString,
                    response_serializer=entities_dot_v1alpha_dot_entities__pb2.ListDeletedEntitiesResponse.SerializeToString,
            ),
            'UndeleteEntity': grpc.unary_unary_rpc_method_handler(
                    servicer.UndeleteEntity,
                    request_deserializer=entities_dot_v1alpha_dot_entities__pb2.UndeleteEntityRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'ListEntityMentions': grpc.unary_unary_rpc_method_handler(
                    servicer.ListEntityMentions,
                    request_deserializer=entities_dot_v1alpha_dot_entities__pb2.ListEntityMentionsRequest.FromString,
                    response_serializer=entities_dot_v1alpha_dot_entities__pb2.ListEntityMentionsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.mintter.entities.v1alpha.Entities', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Entities(object):
    """Provides functionality to query information about Hypermedia Entities.
    """

    @staticmethod
    def GetChange(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.mintter.entities.v1alpha.Entities/GetChange',
            entities_dot_v1alpha_dot_entities__pb2.GetChangeRequest.SerializeToString,
            entities_dot_v1alpha_dot_entities__pb2.Change.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetEntityTimeline(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.mintter.entities.v1alpha.Entities/GetEntityTimeline',
            entities_dot_v1alpha_dot_entities__pb2.GetEntityTimelineRequest.SerializeToString,
            entities_dot_v1alpha_dot_entities__pb2.EntityTimeline.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DiscoverEntity(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.mintter.entities.v1alpha.Entities/DiscoverEntity',
            entities_dot_v1alpha_dot_entities__pb2.DiscoverEntityRequest.SerializeToString,
            entities_dot_v1alpha_dot_entities__pb2.DiscoverEntityResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SearchEntities(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.mintter.entities.v1alpha.Entities/SearchEntities',
            entities_dot_v1alpha_dot_entities__pb2.SearchEntitiesRequest.SerializeToString,
            entities_dot_v1alpha_dot_entities__pb2.SearchEntitiesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteEntity(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.mintter.entities.v1alpha.Entities/DeleteEntity',
            entities_dot_v1alpha_dot_entities__pb2.DeleteEntityRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListDeletedEntities(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.mintter.entities.v1alpha.Entities/ListDeletedEntities',
            entities_dot_v1alpha_dot_entities__pb2.ListDeletedEntitiesRequest.SerializeToString,
            entities_dot_v1alpha_dot_entities__pb2.ListDeletedEntitiesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UndeleteEntity(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.mintter.entities.v1alpha.Entities/UndeleteEntity',
            entities_dot_v1alpha_dot_entities__pb2.UndeleteEntityRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListEntityMentions(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.mintter.entities.v1alpha.Entities/ListEntityMentions',
            entities_dot_v1alpha_dot_entities__pb2.ListEntityMentionsRequest.SerializeToString,
            entities_dot_v1alpha_dot_entities__pb2.ListEntityMentionsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
