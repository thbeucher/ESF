import os
import pickle
import mtranslate
import language_check
import difflib
import regex
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance as sd
from cask_client import CaskClient

from arg_hp import Args
from wmd import wmd
from pareto import pareto_iterative_peeling

my_args = Args(text=(str, True), name=(str, True))
my_args.resolve_args()

langue = 'fr-FR'
NB_CANDIDATE_TO_GENERATE = 20


def get_pos_tags(sentence):
  cask_client = CaskClient()
  response = cask_client.postag(sentence)

  if response['tokens']:
    return response['tokens'][0]
  else:
    return []


def compute_sd(data, seed):
  '''
  Computes the syntactic distance SD

  data - list - the list of sentences
  seed - string - the source sentence
  '''
  pos_tags = [get_pos_tags(s) for s in data]

  input_sentence = regex.sub('\s+', ' ', seed)
  seed_pos_tags = get_pos_tags(input_sentence)

  return [sd(seed_pos_tags, el) for el in pos_tags]


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


def find_candidates(text, tracks):
  '''
  Explore all tracks and return all new candidates finded

  text - string - the original sentence
  tracks - list - the translation tracks
  '''
  candidates = []
  for track in tracks:
    new_text = text
    for i in range(len(track) - 1):
      new_text = mtranslate.translate(new_text, track[i+1], track[i])

    # check sentence
    if check_candidate(new_text):
      candidates.append(new_text)
  return candidates


def check_candidate(candidate):
  '''
  Checks grammatical validity of the candidate

  candidate - string - the sentence for which you want to check the validity

  return True if no language error,  False otherwise
  '''
  tool = language_check.LanguageTool(langue)

  if len(tool.check(candidate)) == 0:
    print('--> Correct sentence generated: ', candidate)
    return True
  else:
    print('--> Incorrect sentence generated: ', candidate)
    return False


def find_new_candidates(text, tracks):
  '''
  Finds all candidates from the source then from
  the first, second and third generation

  return a list of candidates
  '''
  # find all candidates from source
  print('======> first generation <=======')
  first_gen_candidates = find_candidates(text, tracks)
  # clear doublon
  # first_gen_candidates = list(set(first_gen_candidates))

  # find all n+1 candidates ie find candidates from
  # the first generation
  print('======> second generation <=======')
  second_gen_candidates = []
  for cand in first_gen_candidates:
    second_gen = find_candidates(cand, tracks)
    second_gen_candidates.extend(second_gen)
  # clear doublon
  # second_gen_candidates = list(set(second_gen_candidates))

  # find all n+2 candidates
  print('======> third generation <=======')
  third_gen_candidates = []
  for cand in second_gen_candidates:
    third_gen = find_candidates(cand, tracks)
    third_gen_candidates.extend(third_gen)

  # merge and clear doublon
  tmp_candidates = first_gen_candidates + second_gen_candidates + third_gen_candidates
  final_candidates = list(set(tmp_candidates))

  return final_candidates


def main():
  '''
  Find rephrase from the one given and then explore in
  order to find new sentence from the ones which are
  generated.

  '''
  if os.path.isfile('stored_good_tracks'):
    sm = difflib.SequenceMatcher()
    tracks = pickle.load(open('stored_good_tracks', 'rb'))

    # find candidates
    new_text = find_new_candidates(my_args.text, tracks)

    text = my_args.text
    wmd_score = [round(wmd(text, el), 3) for el in new_text]

    sm.set_seq2(text)
    sm_score = []
    for el in new_text:
      sm.set_seq1(el)
      sm_score.append(round(sm.ratio(), 3))
    for_ordering = [(sentence, score) for sentence, score in zip(new_text, wmd_score)]
    for_ordering2 = [(sentence, score) for sentence, score in zip(new_text, sm_score)]
    for_ordering12 = [(sentence, wmd, sm) for sentence, wmd, sm in zip(new_text, wmd_score, sm_score)]
    candidates_ordered = sorted(for_ordering, key=lambda x: x[1])
    candidates_ordered2 = sorted(for_ordering2, key=lambda x: x[1])
    candidates_ordered12 = sorted(for_ordering12, key=lambda x: (x[1], x[2]))

    # compute syntactic distances SD
    all_sd = compute_sd(new_text, text)
    # pareto to get best tradeoff between high syntactic diversity and low semantic divergence
    candidates = [(wmd, sd, sentence) for wmd, sd, sentence in zip(wmd_score, all_sd, new_text)]
    final_candidates = pareto_iterative_peeling(candidates)
    final_candidates.sort(key=lambda tu: tu[0], reverse=True)

    with open(my_args.name, 'w') as f:
      print("Original sentence: ", text)
      f.write("Original sentence: " + text + "\n")
      for i, el in enumerate(candidates_ordered):
        print('Candidate ', i, ' (wmd = ', el[1], ' ) : ', el[0])
        f.write('Candidate ' + str(i) + ' (wmd = ' + str(el[1]) + ' ) : ' + el[0] + '\n')
      for i, el in enumerate(candidates_ordered2):
        print('Candidate ', i, ' (sm = ', el[1], ' ) : ', el[0])
        f.write('Candidate ' + str(i) + ' (sm = ' + str(el[1]) + ' ) : ' + el[0] + '\n')
      for i, el in enumerate(candidates_ordered12):
        print('Candidate ', i, ' (wmd | sm  = ', el[1], ' | ', el[2],' ) : ', el[0])
        f.write('Candidate ' + str(i) + ' (wmd | sm = ' + str(el[1]) + ' | ' + str(el[2]) + ' ) : ' + el[0] + '\n')
      for i, el in enumerate(final_candidates):
        print('Candidate ', i, ' (wmd | sd = ', el[0], ' | ', el[1], ' )', ' : ', el[2])
        f.write('Candidate ' + str(i) + ' (wmd | sd = ' + str(el[0]) + ' | ' + str(el[1]) + ' )' + ' : ' + str(el[2]))
  else:
    print("No file store_good_tracks find!")

main()
