class KafTermSentiment:
  def __init__(self):
    self.resource=None
    self.polarity=None
    self.strength=None
    self.subjectivity=None
    
  def simpleInit(self,r,p,st,su,sm=None):
    self.resource=r
    self.polarity=p
    self.strength=st
    self.subjectivity=su
    self.sentiment_modifier = sm
    
  def getPolarity(self):
    return self.polarity
  
  def getSentimentModifier(self):
    return self.sentiment_modifier
    
    
class KafToken:
  def __init__(self,wid, value, sent=None, para=None):
    self.token_id = wid
    self.value = value
    self.sent = sent
    self.para = para
  


class KafTerm:
  def __init__(self):
    self.tid = None
    self.lemma = None
    self.pos = None
    self.sentiment = None
    self.list_span_id = []
    
  def set_list_span_id(self, L):
    self.list_span_id = L
    
  def get_list_span(self):
    return self.list_span_id
    
    
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
      
    
    
    
    