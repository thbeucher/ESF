import os
import pickle



if os.path.isfile('stored_good_tracks'):
  a = pickle.load(open('stored_good_tracks', 'rb'))
  for el in a:
    print('Track: ', el)
