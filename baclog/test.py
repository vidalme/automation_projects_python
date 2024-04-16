#!/usr/bin/env python

from fabric import Connection

# print('oi')

conn = Connection(host='ubuntu@13.59.66.130')
# print(conn)

conn.run("pwd")
# print(res01)
