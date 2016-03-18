# -*- coding: utf-8 -*-
# Rundong Li, UESTC
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors
import evernote.edam.notestore.ttypes as UserStoreTypes
import time
import socket

# standard makeNote method:
def makeNote(authToken, noteStore, noteTitle, noteBody, parentNotebook=None):

	nBody = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
	nBody += "<!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\">"
	nBody += "<en-note>%s</en-note>" % noteBody

	## Create note object
	ourNote = Types.Note()
	ourNote.title = noteTitle
	ourNote.content = nBody

	## parentNotebook is optional; if omitted, default notebook is used
	if parentNotebook and hasattr(parentNotebook, 'guid'):
		ourNote.notebookGuid = parentNotebook.guid

	## Attempt to create note in Evernote account
	try:
		note = noteStore.createNote(authToken, ourNote)
	except Errors.EDAMUserException, edue:
		## Something was wrong with the note data
		## See EDAMErrorCode enumeration for error code explanation
		## http://dev.evernote.com/documentation/reference/Errors.html#Enum_EDAMErrorCode
		print "EDAMUserException:", edue
		return None
	except Errors.EDAMNotFoundException, ednfe:
		## Parent Notebook GUID doesn't correspond to an actual notebook
		print "EDAMNotFoundException: Invalid parent notebook GUID"
		return None
	## Return created note object
	return note

# standard updateNote methods:
def updateNote(authToken, noteStore, oldNote, noteBody, cacheOldIP = False):
	# get Note with content:
	try:
		existNote = noteStore.getNote(authToken, oldNote.guid, True, False, False, False)
	except Errors.EDAMUserException, edue:
		## Something was wrong with the note data
		## See EDAMErrorCode enumeration for error code explanation
		## http://dev.evernote.com/documentation/reference/Errors.html#Enum_EDAMErrorCode
		print "EDAMUserException:", edue
		return None
	except Errors.EDAMNotFoundException, ednfe:
		## Parent Notebook GUID doesn't correspond to an actual notebook
		print "EDAMNotFoundException: Invalid parent notebook GUID"
		return None
	except Errors.EDAMSystemException, edue:
		print 'EDAMSystemException:', edue
		return None

	# you can determine cache old IP log via argument cacheOldIP
	if cacheOldIP:
		# update IP Note content:
		# delete exist '</en-note>' and append new noteBody:
		existNote.content = existNote.content[:-10] + noteBody + '</en-note>'
	else:
		# don't cache IP log as default:
		existNote.content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
		existNote.content += "<!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\">"
		existNote.content += "<en-note>%s</en-note>" % noteBody

	# update IP Note and return it:
	try:
		existNote = noteStore.updateNote(authToken, existNote)
	except Errors.EDAMUserException, edue:
		## Something was wrong with the note data
		## See EDAMErrorCode enumeration for error code explanation
		## http://dev.evernote.com/documentation/reference/Errors.html#Enum_EDAMErrorCode
		print "EDAMUserException:", edue
		return None
	except Errors.EDAMNotFoundException, ednfe:
		## Parent Notebook GUID doesn't correspond to an actual notebook
		print "EDAMNotFoundException: Invalid parent notebook GUID"
		return None
	except Errors.EDAMSystemException, edue:
		print 'EDAMSystemException:', edue
		return None
	return existNote

# Search a note in a specific notebook:
def searchNote(authToken, noteStore, keyWord, noteBook):
	IPfilter = UserStoreTypes.NoteFilter()
	IPfilter.words = keyWord
	IPfilter.notebookGuid = noteBook.guid

	# Error shoot:
	try:
		noteFindList = noteStore.findNotes(authToken, IPfilter, 0, 10)
	except Errors.EDAMUserException, edue:
		## Something was wrong with the note data
		## See EDAMErrorCode enumeration for error code explanation
		## http://dev.evernote.com/documentation/reference/Errors.html#Enum_EDAMErrorCode
		print "EDAMUserException:", edue
		return None
	except Errors.EDAMNotFoundException, ednfe:
		## Parent Notebook GUID doesn't correspond to an actual notebook
		print "EDAMNotFoundException: Invalid parent notebook GUID"
		return None
	except Errors.EDAMSystemException, edue:
		print 'EDAMSystemException:', edue
		return None
	return noteFindList

# Function to get current time:
def getCurrentTime():
	return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

# Function to get IPv4 and current PC name:
def getIPandName():
	# name of current PC
	pcName = socket.getfqdn(socket.gethostname())
	# get IPv4
	localIPv4 = socket.gethostbyname(socket.gethostname())
	# get IPv6
	IPv6Info = socket.getaddrinfo(pcName, 80, socket.AF_INET6)
	# ! I tried these idx very HARD!
	localIPv6 = IPv6Info[1][4][0]

	return localIPv4, localIPv6, pcName