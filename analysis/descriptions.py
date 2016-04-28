import nltk
from nltk.sem import relextract

descriptions = [
  'Vote by the best logo',
  'CATS CATS CATS',
  'Which pupper is cutest?',
  'quality of cat',
  'best art',
  'Cutest dog',
  'Best CIS professor',
  'Most representative picture of Penn',
  'Most enjoy spending time with students from which school?',
  'Favorite college w/ heavy sports culture',
  'Favorite phone',
  'best casual outfit for a date',
  'Which is the prettiest button?',
  'Which is the better designed marketing poster?',
  'Which rowing picture is coolest?',
  'Which cookie looks the best?',
  'What is Jennifer Aniston\'s best look?',
  'What is the prettiest sunset?',
  'What is the healthiest?',
  'Who is your favorite Friends character?',
  'What\'s the best coffee?',
  'Which puppy is the cutest?',
  'Which is the hottest pic of our hottest prez?',
  'Which school delivers the best quality of education?',
  'Which lipstick color is the most trendy?',
  'Which Penn baseball cap is the coolest?',
  'Which Harry Potter book is the best?',
  'Which social media platforms are the most helpful for everyday life?',
  'Which Monet is the prettiest?',
  'Which presidential candidate would you most like to see in a dunk tank?',
  'sort by how beautiful you think the photo is',
  'I want my photos to be sorted by most exciting to least exciting',
  'which is a better background'
]

grammar = "RELEVANT: {<DT|JJP|JJC>*<.*>*<NN>+}"

nltk.help.upenn_tagset()

for description in descriptions:
  tokens = nltk.word_tokenize(description)
  tagged = nltk.pos_tag(tokens)
  entities = nltk.chunk.ne_chunk(tagged)
  cp = nltk.RegexpParser(grammar)
  result = cp.parse(entities)
  print result