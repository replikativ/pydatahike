# Datahike for Python

This repository provides native bindings for [Datahike](https://datahike.io) (see also the [github repository](https://github.com/replikativ/datahike)) for Python 3.

Currently you need to manually provide `libdatahike.so` (or the respective dynamic library format for your platform) from a native image build of Datahike on your linking path (`LD_LIBRARY_PATH` on Linux). The core API of Datahike is then available with:

~~~python
from datahike import *

config = "{:store {:backend :file :path \"/path/to/db\"} :schema-flexibility :read}"
tx_data = "[{\"age\": 42}]"

create_database(config)
transact(config, tx_data)
q = "[:find ?a . :where [?e :age ?a]]"
# provide a query and a list of inputs, here just a single database
query(q, [("db", config)])  # => 42

# cleanup
delete_database(config)
~~~

The API is a fairly direct partial mapping onto [the Clojure API](https://cljdoc.org/d/io.replikativ/datahike/) (click `api`) which contains documentation. If you need help please open an issue and/or join the Clojurians slack.
