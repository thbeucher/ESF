import os
import pickle
import mtranslate

NAME = 'stored_good_tracks_but_duplicate'

datasets = [
    "Mon nom est Henri",
    "Je voudrais commander une pizza",
    "Comment je peux gagner de nouveau point fidélité?"
    ]

if os.path.isfile('stored_good_tracks'):
  tracks = pickle.load(open('stored_good_tracks', 'rb'))
  tracks_cleared = []
  for i in range(len(tracks) - 1):
    new_data1, new_data2 = [], []
    track1, track2 = tracks[i], tracks[i+1]
    for sentence in datasets:
      new_text = sentence
      for i in range(len(track1) - 1):
        new_text = mtranslate.translate(new_text, track1[i+1], track1[i])
      new_data1.append(new_text)

      new_text = sentence
      for i in range(len(track2) - 1):
        new_text = mtranslate.translate(new_text, track2[i+1], track2[i])
      new_data2.append(new_text)

    if new_data1 == new_data2:
      print("this two tracks give the same candidate: ", track1, " || ", track2)
      if track1 not in tracks_cleared:
        tracks_cleared.append(track1)
    else:
      if track1 not in tracks_cleared:
        tracks_cleared.append(track1)
      if track2 not in tracks_cleared:
        tracks_cleared.append(track2)
  print(len(tracks), len(tracks_cleared))
else:
  print("no stored_good_tracks file finded!")
