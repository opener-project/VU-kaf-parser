class KafTermSentiment:
  def __init__(self):
    self.resource=''
    self.polarity=''
    self.strength=''
    self.subjectivity=''
    
  def simpleInit(self,r,p,st,su):
    self.resource=r
    self.polarity=p
    self.strength=st
    self.subjectivity=su
    
    
  


class KafTerm:
  def __init__(self):
    self.tid = None
    self.lemma = None
    self.pos = None
    self.sentiment = None
    
  def setSentiment(self,my_sent):
    self.sentiment = my_sent
    
  def getSentiment(self):
    return self.sentiment
    
  def getLemma(self): 
      return self.lemma
    
  def setLemma(self,lemma):
      self.lemma = lemma
    
  def getPos(self):
      return self.pos
    
  def setPos(self,pos):
      self.pos = pos
      
  def getId(self):
      return self.tid
      
  def setId(self,id):
      self.tid = id

  def getShortPos(self):
    if self.pos==None:
      return None
    auxpos=self.pos.lower()[0]
    if auxpos == 'g': auxpos='a'
    elif auxpos == 'a': auxpos='r'
    return auxpos
    
  def __str__(self):
    if self.tid and self.lemma and self.pos:
        return self.tid+'\n\t'+self.lemma.encode('utf-8')+'\n\t'+self.pos
    else:
        return 'None'
      
    
    
    
    