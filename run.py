import azapi

artist = raw_input("Insert artist: ")
title = raw_input("Insert title: ")

azapi.generating(artist, title, save=True)
