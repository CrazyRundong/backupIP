# -*- coding: utf-8 -*-
# Rundong Li, UESTC

# import library
import evernote.edam.userstore.constants as UserStoreConstants
from evernote.api.client import EvernoteClient
from backupMethods import *


# dev token for Evernote:
auth_token = "S=s1:U=9237e:E=15ac1b0fe1b:C=15369ffd030:P=1cd:A=en-devtoken:V=2:H=5387bfabe015c47c53b9f8bea6cfa92e"
localIPv4, localIPv6, pcName = getIPandName()

# initial my sandbox user:
client = EvernoteClient(token=auth_token, sandbox=True)
user_store = client.get_user_store()
version_ok = user_store.checkVersion(
    "Evernote EDAMTest (Python)",
    UserStoreConstants.EDAM_VERSION_MAJOR,
    UserStoreConstants.EDAM_VERSION_MINOR
)
if not version_ok: exit(1)
note_store = client.get_note_store()

# create a notebook -- IP if no such a notebook exsists
ipGUID = 'IP address'; IPNotebook = None
for element in note_store.listNotebooks():
	if element.name == ipGUID:
		IPNotebook = element
		print 'Find exist IP Notebook: %s' % IPNotebook.guid
# if ipGUID not in notebookNames:
if not IPNotebook:
	IPNotebook = Types.Notebook()
	IPNotebook.name = ipGUID
	IPNotebook = note_store.createNotebook(IPNotebook)
	print 'Created a new notebook with GUID: %s\n' % IPNotebook.guid

# create a new note:
noteTitle = "IP address in %s" % pcName
noteBody = 'Backup time: %s;<br/>' % getCurrentTime()
noteBody += 'IPv4: %s;<br/>' % localIPv4
noteBody += 'IPv6: %s;<br/><br/>' % localIPv6

# Search if IPNote already exist:
noteFindList = searchNote(auth_token, note_store, ipGUID, IPNotebook)
ipNote = Types.Note()
for element in noteFindList.notes:
	if element.title == noteTitle:
		ipNote = element
		print 'Find a IPNote: %s\nGUID: %s' % (ipNote.title, ipNote.guid)
if not ipNote.title:
	# no exist IP Note: create a new Note
	ipNote = makeNote(auth_token, note_store, noteTitle, noteBody, IPNotebook)
	if ipNote:
		print 'Successfully backup your IP in a new Note:\n %s' % ipNote.guid
	else:
		print 'Backup failed'
else:
	# do exist a IP Note: update its content
	# don't cache IP log as default:
	if updateNote(auth_token, note_store, ipNote, noteBody, cacheOldIP = False):
		print 'Successfully update your IP'
	else:
		print 'Update failed'