import os
import pickle
import mtranslate
import language_check

from arg_hp import Args

my_args = Args(text=(str, True))
my_args.resolve_args()

langue = 'fr-FR'


def find_new_candidate(text, candidates, tracks):
  '''
  Explore translation tracks and return the new sentence
  when a new one is find.

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


def main():
  '''
  Find rephrase from the one given and then explore in
  order to find new sentence from the ones which are
  generated.

  '''
  if os.path.isfile('stored_good_tracks'):
    tool = language_check.LanguageTool(langue)
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
        if len(tool.check(n_text)) == 0:
          print('--> Correct sentence generated: ', n_text)
          new_text.append(n_text)
        else:
          print('--> Incorrect sentence generated: ', n_text)
      sizes.append(len(new_text))
      print('new element added (', sizes, ')')
    for i, el in enumerate(new_text):
      print('Candidate ', i, ': ', el)
  else:
    print("No file store_good_tracks find!")

main()
