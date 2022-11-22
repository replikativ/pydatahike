from ctypes import *
import json

# GraalVM dynamic library setup
dll = CDLL("../libdatahike.so")
isolate = c_void_p()
isolatethread = c_void_p()
dll.graal_create_isolate(None, byref(isolate), byref(isolatethread))

# set result types for functions that return JSON
dll.database_exists.restype = c_char_p
dll.transact_json.restype = c_char_p
dll.q_json.restype = c_char_p

def database_exists(config):
    config = bytes(config, "utf8")
    return json.loads(dll.database_exists(isolatethread, c_char_p(config)))

def create_database(config):
    config = bytes(config, "utf8")
    dll.create_database(isolatethread, c_char_p(config))

def delete_database(config):
    config = bytes(config, "utf8")
    dll.delete_database(isolatethread, c_char_p(config))

def transact(config, tx_data):
    config = bytes(config, "utf8")
    tx_data = bytes(tx_data, "utf8")
    return json.loads(dll.transact_json(isolatethread, config, tx_data))

def query(query, config):
    query = bytes(query, "utf8")
    config = bytes(config, "utf8")
    return json.loads(dll.q_json(isolatethread, query, config))


if __name__ == "__main__":
    config = "{:store {:backend :mem :id \"foo\"} :schema-flexibility :read}"
    tx_data = "[{\"age\": 42}]"

    create_database(config)
    assert database_exists(config)

    transact(config, tx_data)
    q = "[:find ?a . :where [?e :age ?a]]"
    assert query(q, config) == 42

    delete_database(config)
    assert not database_exists(config)
