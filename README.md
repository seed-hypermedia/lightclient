# lightclient
Command line grpc client to interact with mintter daemon

## Run the program
First Install the dependencies running:
```bash
pip install -r requirements.txt
```

Then you can check you can run the program by typing
```bash
python client.py -h
```

## Update protobufs
To compile the source protobuf definitions:
```bash
python -m grpc_tools.protoc --proto_path=. ./definition.proto --python_out=. --grpc_python_out=.
```

example:
```bash
python -m grpc_tools.protoc --proto_path=/home/julio/Documents/mintter/proto /home/julio/Documents/mintter/proto/accounts/v1alpha/accounts.proto --python_out=. --grpc_python_out=.
```

if there are relative imports in a `.proto` file, make sure the `--proto_path` includes both source and imported protos