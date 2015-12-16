# Hello RPC Example

HelloRPC demonstrates how Quark can implement cross-language RPC.

## Hello Service Contract

The Hello Service contract is expressed in hello.q. There are two
value classes (Request and Response) and a service interface
(Hello). The Quark file also defines the names of the client class
(HelloClient) and the server stub class (HelloServer).

### Writing a client

The client code files (pyclient.py, HelloRPCClient.java) follow the
same basic pattern. A client instance can be constructed by passing in
to the client constructor the runtime integration and the URL of the
server. The only defined function (hello) requires an argument, an
instance of Request, and returns an instance of Response. The code
`response = client.hello(request)` is what causes the remote procedure
call to take place.

### Writing a server

The server code files (pyserver.py, jsserver.js, HelloRPCServer.java)
also follow the same basic pattern. A server instance can be
constructed by passing in to the server constructor the runtime
integration and the implementation of the contract interface. Then the
integration can serve the service on the given URL.

## Running this example

The clients expect to find the service on http://127.0.0.1:8910/hello
and each server runs there. Thus you may run a single server at a
time, as well as any number of clients.

### Python

Make sure the python-threaded runtime integration is installed (`pip
install -U datawire-quark-threaded`).

Compile and install the Service Contract in hello.q:

        quark --python package hello.q
        pip install hello/py/dist/hello-0.1.0-py2-none-any.whl

Run the Python server with

        python pyserver.py

Run the Python client with

        python pyclient.py

### Java

Compile and install the Service Contract in hello.q:

        quark --java package hello.q
        (cd hello/java && mvn install)

Compile the Java server and client with 

        mvn compile

Run the Java server with

        mvn exec:java -Dexec.mainClass=helloRPC.HelloRPCServer

Run the Java client with

        mvn exec:java -Dexec.mainClass=helloRPC.HelloRPCClient

### JavaScript

Make sure the JS/Node setup has been completed:

        npm install ws
        npm install datawire-quark-core
        npm install datawire-quark-node

Compile and install the RPC Contract in hello.q:

        quark --javascript package hello.q
        npm install helloRPC/js/hello.tgz

Run the Javascript server with

        node jsserver.js

JavaScript client support is coming soon!

# FIXME

- Better answer for JS clients.
- Any answer for failures. Right now client code hangs forever if the
  server is unavailable.
- `mvn` stuff does not work for everybody.