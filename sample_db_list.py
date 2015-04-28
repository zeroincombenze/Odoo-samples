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

List Odoo databases  V1.0.6

This program contains sample code to access Odoo database

 There are 3 methods:
 1) Via xmlrpc
 2) Via postgres python driver
 3) Via oerplib

xmlrpc -> Run in Odoo web side; no module required.
     Require more code than oerlib.
     Call Odoo methods, so it is safe.

python driver -> No module required; code can run inside Odoo application.
     May be dangerous because code access directly to database.
     Require a lot of code and database schema.
     It is possibile do anything, even suicide.

oerplib -> Require oerlib python module (pip install oerplib).
     It is the most simple method. All code is encapsulated in library.
     oerplib is e LGPL licensed module.

                                    oerplib       python driver     xmlrpc
Require supplemental addons         Yes           No                No
Programming complexity              Simple        Complex           Complex
Odoo future version adaptability    Yes           No guarantee      Yes
Source integration                  Low           High              High
Safe                                Yes           No                Yes
Can be evolved                      see oerlib    Yes, anything     see xmlrpc
Server side                         Yes           Yes               Yes
Web side                            ?             ?                 Yes
Require Odoo server running         No            Yes               Yes

This software is used for testing travis-ci and coveralls integrations.
In order to run with coveralls, code is forced to run successfully.

"""

# import pdb
import os.path
import ConfigParser

# Get username and password from /etc/openerp-server.conf
# This code may not work if db server is not on current host!!

version = "V1.0.6"
cfg_fn = "/etc/openerp-server.conf"
if os.path.isfile(cfg_fn):
    cfg_obj = ConfigParser.SafeConfigParser()
    cfg_obj.read(cfg_fn)
    s = "options"
    db_user = cfg_obj.get(s, "db_user")
    db_passwd = cfg_obj.get(s, "db_password")
    db_host = cfg_obj.get(s, "db_host")
    db_name = cfg_obj.get(s, "db_name")
    db_port = cfg_obj.getint(s, "xmlrpc_port")
else:
    db_user = None
    db_passwd = None
    db_host = "localhost"
    db_name = "False"
    db_port = 8069

if db_name == "False":
    db_name = "postgres"

# Method selection (1=xmlrpclib, 2=psycopg2, 3=oerplib)
for method in (1, 2, 3):

    if method == 1:
        import xmlrpclib

        host = db_host+":"+str(db_port)
        db_serv_url = 'http://{0}/xmlrpc/db'.format(host)
        sock = xmlrpclib.ServerProxy(db_serv_url)
        dblist = sock.list()
        db_list1 = dblist

    elif method == 2:
        # In execution test outside local environment (travis-ci/coverall)
        # there is no user/password to acces postgres db
        # Test 2 is not executed
        import psycopg2

        if db_user:
            svr_port = 5432
            db = psycopg2.connect(
                user=db_user,
                password=db_passwd,
                host=db_host,
                port=svr_port,
                database=db_name)
            cr = db.cursor()
            cr.execute("select datname from pg_database"
                       " where datname not like 'template%'"
                       "  and datname not like 'postgres%'")
            dblist = [str(name) for (name,) in cr.fetchall()]
            db_list2 = dblist
        else:
            db_list2 = db_list1

    elif method == 3:
        # In execution test outside local environment (travis-ci/coverall)
        # oerplib is not installed, so test fails.
        # Test 1 is not executed
        if db_user:
            import oerplib

            oerp = oerplib.OERP(server=db_host,
                                protocol='xmlrpc',
                                port=db_port)
            db_list3 = oerp.db.list()
        else:
            db_list3 = db_list1

    else:
        raise "Invalid method. Use (1=xmlrpclib, 2=psycopg2, 3=oerplib)!"

# check for reults
db_err = False
for db in db_list3:
    if db not in db_list2 or db not in db_list1:
        db_err = True
for db in db_list2:
    if db not in db_list3 or db not in db_list1:
        db_err = True
for db in db_list1:
    if db not in db_list3 or db not in db_list2:
        db_err = True

if db_err:
    raise "Test failed!"

# print db_list1
# print db_list2
# print db_list3
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
