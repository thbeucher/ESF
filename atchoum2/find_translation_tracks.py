import mtranslate
import random
import pickle
import os

from arg_hp import Args

my_args = Args(text=(str, False, "Je m'appelle Henri"), langue=(str, False, 'fr'))
my_args.resolve_args()

text = my_args.text
langue = my_args.langue

all_targets = ['af', 'ar', 'zh','hr', 'cs', 'da', 'nl', 'en', 'et', 'fi', 'fr', 'de', 'el', 'iw', 'hi', 'hu', 'is', 'id', 'ga', 'it', 'ja', 'ko', 'la', 'lt', 'lb', 'no', 'pt', 'ro', 'ru', 'sr', 'sk', 'sl', 'es', 'sv', 'th', 'tr', 'uk', 'vi']


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

  text2 = text
  # run the translation track
  for i in range(len(my_track) - 1):
    text2 = mtranslate.translate(text2, my_track[i+1], my_track[i])
  # ask user if the translation is good or not
  print("Text: ", text, "\n==> Rephrase: ", text2)
  rep = input('Is it ok for you? (y/n): ')
  if rep == 'y':
    store_good_tracks.append(my_track) if my_track not in store_good_tracks else 1
  elif rep == 'n':
    store_bad_tracks.append(my_track) if my_track not in store_bad_tracks else 1


#save translation tracks
pickle.dump(store_good_tracks, open("stored_good_tracks", 'wb'))
pickle.dump(store_bad_tracks, open("stored_bad_tracks", "wb"))
# end of translation tracks exploration
# ==================================== #



# target_chinois = 'zh'
# target_anglais = 'en'
# target_allemand = 'al'
# targets = [target_chinois, target_anglais, target_allemand, 'it', 'ar', 'ja', 'la']


# rephrases = []

# for i in range(5):
#   print('text: ', text)
#   l_uses = [langue]
#   for i in range(5):
#     translation = text if i == 0 else text
#     r = random.randint(0, len(targets) - 1)
#     translation = mtranslate.translate(translation, targets[r], l_uses[-1]).lower()
#     l_uses.append(targets[r])
#   text = mtranslate.translate(translation, langue, l_uses[-1]).lower()
#   rephrases.append(text)
#   print("track: ", l_uses)
#   print("==> ", text)


# good_track = ['fr', 'ar', 'zh', 'al', 'ja', 'fr']
# otext = text
# for i in range(len(good_track) - 1):
#   text = mtranslate.translate(text, good_track[i+1], good_track[i])
# print("Text: ", otext, "\n==> New text: ", text)
