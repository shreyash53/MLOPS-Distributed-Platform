import random
class rng:
  def preprocess(self,a):
    return (a)
  def predict(self,arg):
    random.seed(arg)
    return random.random()
  def postprocess(self,a):
    return a
