python3 -m grpc_tools.protoc -I wataame-rpc/compute --python_out=. --grpc_python_out=. compute.proto
python3 -m grpc_tools.protoc -I wataame-rpc/network --python_out=. --grpc_python_out=. network.proto
python3 -m grpc_tools.protoc -I wataame-rpc/container --python_out=. --grpc_python_out=. container.proto
python3 -m grpc_tools.protoc -I wataame-rpc/storage --python_out=. --grpc_python_out=. storage.proto
python3 -m grpc_tools.protoc -I wataame-rpc/serverless --python_out=. --grpc_python_out=. serverless.proto