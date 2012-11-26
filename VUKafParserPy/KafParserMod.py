
from lxml import etree
from KafDataObjectsMod import *
import time

class KafParser:
  def __init__(self,filename=None):
    self.tree=None
    self.__pathForToken={}
    
    if filename:
        self.tree = etree.parse(filename,etree.XMLParser(remove_blank_text=True))
        ## Do the text tokenization
        self.__textTokenization()
        
  def __textTokenization(self):
    for wf in self.tree.findall('text/wf'):
      wid = wf.get('wid')
      self.__pathForToken[wid] = self.tree.getpath(wf)
     
  
  def getToken(self,tid):
    path = self.__pathForToken[tid]
    return self.tree.xpath(self.__pathForToken[tid])[0]

  def getTerms(self):
     if self.tree:
       for element in self.tree.find('terms'):
           kafTermObj = KafTerm()
           kafTermObj.setId(element.get('tid'))
           kafTermObj.setLemma(element.get('lemma'))
           kafTermObj.setPos(element.get('pos'))
           
           ## Parsing sentiment
           sentiment = element.find('sentiment')
           if sentiment is not None:
             resource = sentiment.get('resource','')
             polarity = sentiment.get('polarity','')
             strength = sentiment.get('strength','')
             subjectivity = sentiment.get('subjectivity','')
             sentiment_modifier = sentiment.get('sentiment_modifier')
             
             my_sent = KafTermSentiment()
             my_sent.simpleInit(resource,polarity,strength,subjectivity,sentiment_modifier)
             kafTermObj.setSentiment(my_sent)
          
           ## Parsing the span
           span = element.find('span')
           if span is not None:
            list_ids = [target.get('id') for target in span.findall('target')]
            kafTermObj.set_list_span_id(list_ids)
        
             
           yield kafTermObj
     else:
       return
      
      
  def getSentimentTriples(self):
    data = []
    if self.tree:
      for term_element in self.tree.findall('terms/term'):
        lemma = term_element.get('lemma')
        polarity = None
        sentiment_modifier = None
        
        sentiment_element = term_element.find('sentiment')
        if sentiment_element is not None:
            polarity = sentiment_element.get('polarity',None)
            sentiment_modifier = sentiment_element.get('sentiment_modifier')
        data.append( (lemma,polarity,sentiment_modifier))
    return data
      
   
      
  def addPolarityToTerm(self,termid,my_sentiment_attribs,polarity_pos=None):
    if self.tree:
      for element in self.tree.find('terms'):
        if element.get('tid','')==termid:
          
          #In case there is no pos info, we use the polarityPos
          if not element.get('pos') and polarity_pos is not None:
            element.set('pos',polarity_pos)
          sentEle = etree.Element('sentiment',attrib=my_sentiment_attribs)
          element.append(sentEle)  
      
  def saveToFile(self,filename,myencoding='UTF-8'):
    if self.tree:
      self.tree.write(filename,encoding=myencoding,pretty_print=True,xml_declaration=True)
      
  
  def addLinguisticProcessor(self,name,version, layer, time_stamp=True):
    ## Check if there is already element for the layer
    my_lp_ele = None
    
    for element in self.tree.findall('linguisticProcessors'):
      if element.get('layer','')==layer:
        my_lp_ele = element
        break
      
    if time_stamp:  
      my_time = time.strftime('%Y-%m-%dT%H:%M:%S%Z')
    else:
      my_time = '*'
      
    my_lp = etree.Element('lp')
    my_lp.set('timestamp',my_time)
    my_lp.set('version',version)
    my_lp.set('name',name)

    if my_lp_ele is not None: #Already an element for linguisticProcessor with the layer
      my_lp_ele.append(my_lp)
    else:
      # Create a new element for the LP layer
      idx = self.tree.getroot().index(element)
      my_lp_ele = etree.Element('linguisticProcessor')
      my_lp_ele.set('layer',layer)
      my_lp_ele.append(my_lp)
      #my_lp_ele.tail=my_lp_ele.text='\n'
      ## Should be inserted after the last linguisticProcessor element (stored in variable element)
      idx = self.tree.getroot().index(element)
      self.tree.getroot().insert(idx+1,my_lp_ele)
        
      
  def addLayer(self,type,element):
    ## Check if there is already layer for the type
    layer_element = self.tree.find(type)
    
    if layer_element is None:
      layer_element = etree.Element(type)
      self.tree.getroot().append(layer_element)
      ## The id is going to be the first one
      new_id = type[0]+'_1'
    else:
      ## We need to know how many elements there are in the layer
      current_n = len(layer_element.getchildren())
      new_id = type[0]+'_'+str(current_n+1)
      
      
    ## In this point layer_element points to the correct element, wether existing or created
    
    element.set(type[0]+'id',new_id)
    layer_element.append(element)
    
  def addElementToLayer(self,layer, element):
    self.addLayer(layer,element)
    
  


    
    
    
    