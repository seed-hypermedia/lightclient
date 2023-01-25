# lightclient
Console grpc client to interact with mintter daemon

## Update protobufs
To compile the source protobuf definitions:
```bash
python -m grpc_tools.protoc --proto_path=. ./definition.proto --python_out=. --grpc_python_out=.
```

if there are relative imports in a `.proto` file, make sure the `--proto_path` includes both source and imported protos