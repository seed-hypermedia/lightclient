# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from documents.v1alpha import comments_pb2 as documents_dot_v1alpha_dot_comments__pb2


class CommentsStub(object):
    """Comments service allows users to add comments to documents.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateComment = channel.unary_unary(
                '/com.seed.documents.v1alpha.Comments/CreateComment',
                request_serializer=documents_dot_v1alpha_dot_comments__pb2.CreateCommentRequest.SerializeToString,
                response_deserializer=documents_dot_v1alpha_dot_comments__pb2.Comment.FromString,
                )
        self.GetComment = channel.unary_unary(
                '/com.seed.documents.v1alpha.Comments/GetComment',
                request_serializer=documents_dot_v1alpha_dot_comments__pb2.GetCommentRequest.SerializeToString,
                response_deserializer=documents_dot_v1alpha_dot_comments__pb2.Comment.FromString,
                )
        self.ListComments = channel.unary_unary(
                '/com.seed.documents.v1alpha.Comments/ListComments',
                request_serializer=documents_dot_v1alpha_dot_comments__pb2.ListCommentsRequest.SerializeToString,
                response_deserializer=documents_dot_v1alpha_dot_comments__pb2.ListCommentsResponse.FromString,
                )


class CommentsServicer(object):
    """Comments service allows users to add comments to documents.
    """

    def CreateComment(self, request, context):
        """Creates a new comment.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetComment(self, request, context):
        """Gets a single comment by ID.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListComments(self, request, context):
        """Lists comments for a given target.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CommentsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateComment': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateComment,
                    request_deserializer=documents_dot_v1alpha_dot_comments__pb2.CreateCommentRequest.FromString,
                    response_serializer=documents_dot_v1alpha_dot_comments__pb2.Comment.SerializeToString,
            ),
            'GetComment': grpc.unary_unary_rpc_method_handler(
                    servicer.GetComment,
                    request_deserializer=documents_dot_v1alpha_dot_comments__pb2.GetCommentRequest.FromString,
                    response_serializer=documents_dot_v1alpha_dot_comments__pb2.Comment.SerializeToString,
            ),
            'ListComments': grpc.unary_unary_rpc_method_handler(
                    servicer.ListComments,
                    request_deserializer=documents_dot_v1alpha_dot_comments__pb2.ListCommentsRequest.FromString,
                    response_serializer=documents_dot_v1alpha_dot_comments__pb2.ListCommentsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.seed.documents.v1alpha.Comments', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Comments(object):
    """Comments service allows users to add comments to documents.
    """

    @staticmethod
    def CreateComment(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.seed.documents.v1alpha.Comments/CreateComment',
            documents_dot_v1alpha_dot_comments__pb2.CreateCommentRequest.SerializeToString,
            documents_dot_v1alpha_dot_comments__pb2.Comment.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetComment(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.seed.documents.v1alpha.Comments/GetComment',
            documents_dot_v1alpha_dot_comments__pb2.GetCommentRequest.SerializeToString,
            documents_dot_v1alpha_dot_comments__pb2.Comment.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListComments(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.seed.documents.v1alpha.Comments/ListComments',
            documents_dot_v1alpha_dot_comments__pb2.ListCommentsRequest.SerializeToString,
            documents_dot_v1alpha_dot_comments__pb2.ListCommentsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
