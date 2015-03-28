#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) SHS-AV s.r.l. (<http://www.zeroincombenze.it>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
"""

List Odoo databases  V1.00

This code contains sample to access Odoo database

 There are 3 methods:
 1) Via oerplib
 2) Via postgres python driver
 3) Via xmlrpc

oerplib -> Require oerlib python module (pip install oerplib).
     It is the most simple method. All code is encapsulated in library.
     oerplib is e LGPL licensed module.

python driver -> No module are required; code can run inside Odoo application.
     May be dangerous because code access directly to database.
     Require a lot of code and database schema.
     It is possibile do anything, even suicide.

xmlrpc -> Same as web service; no module are required; code can run inside Odoo application.
     Require more code than oerlib.
     Call Odoo methos, so it is safe.


                                    oerplib        python driver     xmlrpc
Require supplemental addons         Yes            No                No
Programming complexity              Simple         Complex           Complex
Odoo future version adaptability    Yes            No guarantee      Should be yes
Source integration                  Low            High              High
Safe                                Yes            No                Yes
Can be evolved                      see oerlib     Yes, anything     just xmlrpc methods
Server side                         Yes            Yes               Yes
Web side                            ?              ?                 Yes
Require Odoo server running         No             Yes               Yes

"""

import pdb


# Method selection (1=oerplib, 2=psycopg2, 3=xmlrpclib)
method = 3
#Username and password are stored in separate sample file
fd=open("sample_db_list.conf", 'r')
uu=fd.readline().strip()
pw=fd.readline().strip()
fd.close()


if method == 1:
    import oerplib
    
    oerp = oerplib.OERP(server='localhost', protocol='xmlrpc', port=8069)
    print oerp.db.list()
    print "DB list by oerplib"

elif method == 2:
    import psycopg2

    db_user = uu
    db_passwd = pw
    db_host = "localhost"
    db_port = 5432
    db_name = "demo"
    db = psycopg2.connect(user=db_user, 
                            password=db_passwd,
                            host=    db_host,
                            port=    db_port,
                            database=db_name)
    cr = db.cursor()
    cr.execute("select datname from pg_database")
    dblist = [str(name) for (name,) in cr.fetchall()]
    print dblist
    print "DB list by psycopg2"


elif method == 3:
    import xmlrpclib

    user = uu
    password = pw
    host = "localhost:8069"
    db = "postgres"
    db_serv_url = 'http://{0}/xmlrpc/db'.format(host)
    sock = xmlrpclib.ServerProxy(db_serv_url)
    #uid = sock.login(db, user, password)
    dblist = sock.list()
    print dblist
    print "DB list by xmlrpc"
 

else:
    raise "Invalid method. Use (1=oerplib, 2=psycopg2, 3=xmlrpclib)!"



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
