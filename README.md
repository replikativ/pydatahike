# Datahike from Python

This repository provides native bindings for [Datahike](https://datahike.io) (see also the [github repository](https://github.com/replikativ/datahike)) for Python 3.

Currently you need to manually provide `libdatahike.so` (or the respective dynamic library format for your platform) from a native image build of Datahike in this folder. The core API of Datahike is then available with:

~~~python
from datahike import *

config = "{:store {:backend :mem :id \"foo\"} :schema-flexibility :read}"
tx_data = "[{\"age\": 42}]"

create_database(config)
transact(config, tx_data)
q = "[:find ?a . :where [?e :age ?a]]"
query(q, config)  # 42

delete_database(config)
~~~

Note that currently any errors still SEGFAULT the Python process, so proper error handling is needed.
