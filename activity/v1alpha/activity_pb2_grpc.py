# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from activity.v1alpha import activity_pb2 as activity_dot_v1alpha_dot_activity__pb2


class ActivityFeedStub(object):
    """ActivityFeed service provides information about the recent activity events happened in the system.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListEvents = channel.unary_unary(
                '/com.seed.activity.v1alpha.ActivityFeed/ListEvents',
                request_serializer=activity_dot_v1alpha_dot_activity__pb2.ListEventsRequest.SerializeToString,
                response_deserializer=activity_dot_v1alpha_dot_activity__pb2.ListEventsResponse.FromString,
                )


class ActivityFeedServicer(object):
    """ActivityFeed service provides information about the recent activity events happened in the system.
    """

    def ListEvents(self, request, context):
        """Lists the recent activity events,
        sorted by locally observed time (newest first).
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ActivityFeedServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListEvents': grpc.unary_unary_rpc_method_handler(
                    servicer.ListEvents,
                    request_deserializer=activity_dot_v1alpha_dot_activity__pb2.ListEventsRequest.FromString,
                    response_serializer=activity_dot_v1alpha_dot_activity__pb2.ListEventsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.seed.activity.v1alpha.ActivityFeed', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ActivityFeed(object):
    """ActivityFeed service provides information about the recent activity events happened in the system.
    """

    @staticmethod
    def ListEvents(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.seed.activity.v1alpha.ActivityFeed/ListEvents',
            activity_dot_v1alpha_dot_activity__pb2.ListEventsRequest.SerializeToString,
            activity_dot_v1alpha_dot_activity__pb2.ListEventsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
