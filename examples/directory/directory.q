package directory {

    class Entry {
        String service;
        List<String> endpoints;
    }

    class Directory extends Task { // implements WebHandler, Task

        Runtime runtime;
        WebSocket socket;

        bool initialized = false;
        Map<String,Entry> entries = new Map<String, Entry>();
        float timeout = 60.0;
        List<AsyncLookup> deferred = [];

        Directory(Runtime runtime, String url, String service, String endpoint) {
            self.runtime = runtime;
            self.runtime.acquire(); // would be nice to have a with statement or something
            self.socket = self.runtime.open(url);
            self.socket.setHandler(self);

            JSONObject tetherInfo = new JSONObject()
                .setObjectItem("op", "tether".toJSON())
                .setObjectItem("service", service.toJSON())
                .setObjectItem("endpoint", endpoint.toJSON());
            self.socket.send(tetherInfo.toString());

            JSONObject subscribeInfo = new JSONObject()
                .setObjectItem("op", "subscribe".toJSON());
            self.socket.send(subscribeInfo.toString());

            self.runtime.schedule(self, 3.0); // heartbeat interval

            self.runtime.release();
        }

        void onExecute(Runtime runtime) {
            JSONObject heartbeatInfo = new JSONObject()
                .setObjectItem("op", "heartbeat".toJSON());
            self.socket.send(heartbeatInfo.toString());
            self.runtime.schedule(self, 3.0);
        }

        void onMessage(WebSocket socket, String message) {
            JSONObject jobj = message.parseJSON();
            String op = jobj["op"].getString();
            if (op == "entry") {
                Entry entry = new Entry();
                entry.service = jobj["service"].getString();
                entry.endpoints = new List<String>();
                int i = 0;
                JSONObject endpoints = jobj["endpoints"];
                JSONObject endpoint = endpoints.getListItem(i);

                while (endpoint != endpoints.undefined()) {
                    entry.endpoints.add(endpoint.getString());
                    i = i + 1;
                    endpoint = endpoints.getListItem(i);
                }

                entries[entry.service] = entry;
            } else {
                if (op == "initialized") {
                    self.initialized = true;
                    int idx = 0;
                    while (idx < self.deferred.size()) {
                        self.runtime.schedule(self.deferred[idx], 0.0);
                        idx = idx + 1;
                    }
                } else {
                    print("Got message with unknown op: " + op);
                    print(message);
                }
            }
        }

        Entry lookup(String name) {
            Entry result = null;
            self.runtime.acquire();
            while (self.initialized != true) {
                self.runtime.wait(self.timeout);
            }
            result = entries[name];
            self.runtime.release();
            return result;
        }

        void lookupAsync(String name, LookupCallback callback) {
            self.runtime.acquire();
            AsyncLookup task = new AsyncLookup(self, name, callback);
            if (self.initialized) {
                self.runtime.schedule(task, 0.0);
            } else {
                self.deferred.add(task);
            }
            self.runtime.release();
        }

    }

    interface LookupCallback {
        void run(Entry result);
    }

    class AsyncLookup extends Task {
        Directory directory;
        String name;
        LookupCallback callback;

        AsyncLookup(Directory directory, String name, LookupCallback callback) {
            self.directory = directory;
            self.name = name;
            self.callback = callback;
        }

        void onExecute(Runtime runtime) {
            Entry result = self.directory.entries[self.name];
            self.callback.run(result);
        }
    }

}
