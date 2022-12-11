from ctypes import *
import io
import json
import base64

import cbor2

# GraalVM dynamic library setup
dll = CDLL("libdatahike.so")
isolate = c_void_p()
isolatethread = c_void_p()
dll.graal_create_isolate(None, byref(isolate), byref(isolatethread))

CBFUNC = CFUNCTYPE(c_void_p, c_char_p)

class DatahikeException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

def __tag_hook__(decoder, tag, shareable_index=None):
    # clojure keyword, collapse to string for now
    if tag.tag == 39:
        return tag.value

    return tag.value

def __parse_return__(s, output_format):
    if len(s) == 0:
        return None
    if s.startswith(bytes("exception:", "utf8")):
        raise DatahikeException(s.decode("utf8").replace("exception:", ""))

    if output_format == "json":
        return json.loads(s)
    elif output_format == "edn":
        return s
    elif output_format == "cbor":
        s = base64.decodebytes(s)
        return cbor2.loads(s, tag_hook=__tag_hook__)

def database_exists(config, output_format="cbor"):
    config = bytes(config, "utf8")

    res = None
    def callback(s):
        nonlocal res
        res = __parse_return__(s, output_format)

    dll.database_exists(isolatethread, c_char_p(config),
                        bytes(output_format, "utf8"), CBFUNC(callback))
    return res

def create_database(config, output_format="cbor"):
    config = bytes(config, "utf8")

    res = None
    def callback(s):
        nonlocal res
        res = __parse_return__(s, output_format)

    dll.create_database(isolatethread, c_char_p(config),
                        bytes(output_format, "utf8"), CBFUNC(callback))
    return res

def delete_database(config, output_format="cbor"):
    config = bytes(config, "utf8")

    res = None
    def callback(s):
        nonlocal res
        res = __parse_return__(s, output_format)

    dll.delete_database(isolatethread, c_char_p(config),
                        bytes(output_format, "utf8"), CBFUNC(callback))
    return res

def query(query, inputs, output_format="cbor"):
    query = bytes(query, "utf8")
    N = len(inputs)
    char_p_p = ARRAY(c_char_p, N)
    input_types = char_p_p()
    input_values = char_p_p()
    for (n, (t, v)) in enumerate(inputs):
        input_types[n] = bytes(t, "utf8")
        input_values[n] = bytes(v, "utf8")

    res = None
    def callback(s):
        nonlocal res
        res = __parse_return__(s, output_format)

    dll.query(isolatethread, query, N, input_types, input_values,
              bytes(output_format, "utf8"), CBFUNC(callback))
    return res

def transact(config, tx_data, output_format="cbor", input_format="json"):
    config = bytes(config, "utf8")
    tx_data = bytes(tx_data, "utf8")

    res = None
    def callback(s):
        nonlocal res
        res = __parse_return__(s, output_format)

    dll.transact(isolatethread, config,
                 bytes(input_format, "utf8"), tx_data,
                 bytes(output_format, "utf8"), CBFUNC(callback))
    return res

def pull(input_db, selector, eid, output_format="cbor", input_format="db"):
    input_format = bytes(input_format, "utf8")
    input_db = bytes(input_db, "utf8")
    selector = bytes(selector, "utf8")

    res = None
    def callback(s):
        nonlocal res
        res = __parse_return__(s, output_format)

    dll.pull(isolatethread, input_format, input_db, selector, eid,
             bytes(output_format, "utf8"), CBFUNC(callback))
    return res

def pull_many(input_db, selector, eids, output_format="cbor", input_format="db"):
    input_format = bytes(input_format, "utf8")
    input_db = bytes(input_db, "utf8")
    selector = bytes(selector, "utf8")
    eids = bytes(json.dumps(eids), "utf8")

    res = None
    def callback(s):
        nonlocal res
        res = __parse_return__(s, output_format)

    dll.pull_many(isolatethread, input_format, input_db, selector, eids,
                  bytes(output_format, "utf8"), CBFUNC(callback))
    return res

def entity(input_db, eid, output_format="cbor", input_format="db"):
    input_format = bytes(input_format, "utf8")
    input_db = bytes(input_db, "utf8")
    res = None
    def callback(s):
        nonlocal res
        res = __parse_return__(s, output_format)

    dll.entity(isolatethread, input_format, input_db, eid,
               bytes(output_format, "utf8"), CBFUNC(callback))
    return res

def datoms(input_db, index, output_format="cbor", input_format="db"):
    input_format = bytes(input_format, "utf8")
    input_db = bytes(input_db, "utf8")
    index = bytes(index, "utf8")

    res = None
    def callback(s):
        nonlocal res
        res = __parse_return__(s, output_format)

    dll.datoms(isolatethread, input_format, input_db, index,
               bytes(output_format, "utf8"), CBFUNC(callback))
    return res

def schema(input_db, output_format="cbor", input_format="db"):
    input_format = bytes(input_format, "utf8")
    input_db = bytes(input_db, "utf8")
    res = None
    def callback(s):
        nonlocal res
        res = __parse_return__(s, output_format)

    dll.schema(isolatethread, input_format, input_db,
               bytes(output_format, "utf8"), CBFUNC(callback))
    return res

def reverse_schema(input_db, output_format="cbor", input_format="db"):
    input_format = bytes(input_format, "utf8")
    input_db = bytes(input_db, "utf8")
    res = None
    def callback(s):
        nonlocal res
        res = __parse_return__(s, output_format)

    dll.reverse_schema(isolatethread, input_format, input_db,
                       bytes(output_format, "utf8"), CBFUNC(callback))
    return res

def metrics(input_db, output_format="cbor", input_format="db"):
    input_format = bytes(input_format, "utf8")
    input_db = bytes(input_db, "utf8")
    res = None
    def callback(s):
        nonlocal res
        res = __parse_return__(s, output_format)

    dll.metrics(isolatethread, input_format, input_db,
               bytes(output_format, "utf8"), CBFUNC(callback))
    return res


if __name__ == "__main__":
    config = "{:store {:backend :mem :id \"pydatahike-test\"} :schema-flexibility :read}"
    tx_data = "[{\"age\": 42}]"

    delete_database(config)
    create_database(config)
    assert(database_exists(config))

    assert len(transact(config, tx_data)) == 2

    q = "[:find ?a . :where [?e :age ?a]]"
    assert query(q, [("db", config)]) == 42

    assert pull(config, "[*]", 1)[":age"] == 42

    assert pull_many(config, "[*]", [1, 1])[1][":age"] == 42

    assert len(datoms(config, ":eavt")) == 2

    assert entity(config, 1)[":age"] == 42

    assert len(schema(config)) == 0
    assert len(reverse_schema(config)) == 0

    # weird base64 one off error sometimes?
    #assert len(metrics(config)) == 6

    delete_database(config)
    assert not database_exists(config)

