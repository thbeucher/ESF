import mtranslate
import random
import pickle
import os

from arg_hp import Args

my_args = Args(text=(str, False, "Je m'appelle Henri"), langue=(str, False, 'fr'))
my_args.resolve_args()

text = my_args.text
langue = my_args.langue

all_targets = ['af', 'ar', 'zh', 'hr', 'cs', 'da', 'nl', 'en', 'et', 'fi', 'fr', 'de', 'el', 'iw', 'hi', 'hu', 'is', 'id', 'ga', 'it', 'ja', 'ko', 'la', 'lt', 'lb', 'no', 'pt', 'ro', 'ru', 'sr', 'sk', 'sl', 'es', 'sv', 'th', 'tr', 'uk', 'vi']


sentences = [el.strip('\n') for el in open('sentences', 'r').readlines()]


# ========================= #
# explore translation tracks
TRACK_MIN_SIZE = 1
TRACK_MAX_SIZE = 10
TARGET_SIZE = len(all_targets)

store_good_tracks = pickle.load(open("stored_good_tracks", "rb")) if os.path.isfile("stored_good_tracks") else []
store_bad_tracks = pickle.load(open("stored_bad_tracks", 'rb')) if os.path.isfile("stored_bad_tracks") else []

for i in range(5):
  finded = False
  limit = 100
  test = 0
  while not finded:
    my_track = [langue]
    # generate the translation track
    [my_track.append(all_targets[random.randint(0, TARGET_SIZE - 1)]) for i in range(random.randint(TRACK_MIN_SIZE, TRACK_MAX_SIZE))]
    my_track.append(langue)
    finded = True if my_track not in store_good_tracks and my_track not in store_bad_tracks else False
    test += 1
    finded = True if test > limit else False

  print('Track = ', my_track)
  for text in sentences:
    text2 = text
    # run the translation track
    for i in range(len(my_track) - 1):
      text2 = mtranslate.translate(text2, my_track[i+1], my_track[i])
    # ask user if the translation is good or not
    print("Text: ", text, " ==> Rephrase: ", text2)
  rep = input('Is it ok for you? (y/n): ')
  if rep == 'y':
    store_good_tracks.append(my_track) if my_track not in store_good_tracks else 1
  elif rep == 'n':
    store_bad_tracks.append(my_track) if my_track not in store_bad_tracks else 1
  print('\n\n')


#save translation tracks
pickle.dump(store_good_tracks, open("stored_good_tracks", 'wb'))
pickle.dump(store_bad_tracks, open("stored_bad_tracks", "wb"))
# end of translation tracks exploration
# ==================================== #
