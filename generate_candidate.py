import os
import pickle
import mtranslate

from arg_hp import Args

my_args = Args(text=(str, True))
my_args.resolve_args()


def find_new_candidate(text, candidates, tracks):
  '''

  text - the text from which to generate new candidates
  candidates - the candidates which already exist
  tracks - the translation tracks to use
  '''
  for track in tracks:
    new_text = text
    for i in range(len(track) - 1):
      new_text = mtranslate.translate(new_text, track[i+1], track[i])
    if new_text not in candidates:
      return new_text
  return ''


if os.path.isfile('stored_good_tracks'):
  tracks = pickle.load(open('stored_good_tracks', 'rb'))
  new_text = [my_args.text]
  sizes = [len(new_text)]
  for i in range(100):
    if i > 3:
      if sizes[-1] == sizes[-2] and sizes[-2] == sizes[-3]:
        break
    text = new_text[i]
    added = True
    while added:
      n_text = find_new_candidate(text, new_text, tracks)
      if n_text == '':
        added = False
        break
      print('new: ', n_text)
      new_text.append(n_text)
    sizes.append(len(new_text))
    print('new element added (', sizes, ')')
  for i, el in enumerate(new_text):
    print('Candidate ', i, ': ', el)
else:
  print("No file store_good_tracks find!")
