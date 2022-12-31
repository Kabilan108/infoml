:py:mod:`bmes`
==============

.. py:module:: bmes


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   bmes.bmes



Functions
~~~~~~~~~

.. autoapisummary::

   bmes.ispc
   bmes.computername
   bmes.iscomputername
   bmes.iscomputernameprefix
   bmes.mkdirif
   bmes.isfile
   bmes.isfileandnotempty
   bmes.isfolder
   bmes.tempdir
   bmes.selfdir
   bmes.datadir
   bmes.trycustomdatadirs
   bmes.dbfile
   bmes.trycustomdbfiles
   bmes.binpath
   bmes.trycustompath
   bmes.testdb
   bmes.gettempfile
   bmes.sanitizefilename
   bmes.downloadurl
   bmes.downloadfile
   bmes.isdbtable
   bmes.system_redirecttofile
   bmes.system
   bmes.tryimportingpackage
   bmes.ispackageinstalled
   bmes.pipinstall
   bmes.pipuninstall
   bmes.condainstall
   bmes.unziptofolder
   bmes.bwaexe
   bmes.printsettings



Attributes
~~~~~~~~~~

.. autoapisummary::

   bmes.ret


.. py:class:: bmes

   .. py:attribute:: PROJECTNAME
      

      

   .. py:attribute:: CUSTOMDATADIR
      

      

   .. py:attribute:: CUSTOMDBFILE
      

      

   .. py:attribute:: CUSTOMTEMPDIR
      

      

   .. py:attribute:: CUSTOMPATH
      

      

   .. py:attribute:: db
      

      


.. py:function:: ispc()


.. py:function:: computername()


.. py:function:: iscomputername(name)


.. py:function:: iscomputernameprefix(name)


.. py:function:: mkdirif(dir)


.. py:function:: isfile(file)


.. py:function:: isfileandnotempty(file)


.. py:function:: isfolder(file)


.. py:function:: tempdir()


.. py:function:: selfdir()


.. py:data:: ret
   

   

.. py:function:: datadir()


.. py:function:: trycustomdatadirs(dirs)


.. py:function:: dbfile()


.. py:function:: trycustomdbfiles(dirs)


.. py:function:: binpath()


.. py:function:: trycustompath(dirs)


.. py:function:: testdb()


.. py:function:: gettempfile(filename=None)


.. py:function:: sanitizefilename(file)


.. py:function:: downloadurl(url, file='', overwrite=False)


.. py:function:: downloadfile(path)


.. py:function:: isdbtable(cur, tablename)


.. py:function:: system_redirecttofile(cmd, stdoutfile=None, stderrfile=None)


.. py:function:: system(cmd, doprint=True)


.. py:function:: tryimportingpackage(importname)


.. py:function:: ispackageinstalled(importname)


.. py:function:: pipinstall(importname, packagename=None, reinstall=False)


.. py:function:: pipuninstall(packagename, importname=None)


.. py:function:: condainstall(importname, packagename=None, reinstall=False, condaargs=[])


.. py:function:: unziptofolder(file, folder, createsubfolder=False)


.. py:function:: bwaexe()


.. py:function:: printsettings()


