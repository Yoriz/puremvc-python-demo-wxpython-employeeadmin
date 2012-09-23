'''
Created on 23 Sep 2012

@author: Dave Wilson
'''

from pubsub import pub

AUTO_TOPIC = pub.AUTO_TOPIC

class ObsClassAttr(object):
    __storage = {}
    def __init__(self, attribute_name):
        self.attribute_name = attribute_name
        
    def __set__(self, instance, value):
        ObsClassAttr.__storage[self.store_id(instance)] = value
        pub.sendMessage(self.store_id(instance), value=value)

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return ObsClassAttr.__storage[self.store_id(instance)]
    
    def store_id(self, instance):
        return "S%s.%s" % (id(instance), self.attribute_name)
    
        
def obs_attr(instance, attr_name, callback):
    pub.subscribe(callback, "S%s.%s" % (id(instance), attr_name))
    callback(getattr(instance, attr_name))
    
def obs_any(instance, callback):
    pub.subscribe(callback, "S%s" % (id(instance)))


if __name__ == '__main__':
    
    def call_back1(value):
        """callback must receive value"""
        print "Call_back1: %s" % value
        
    def call_back2(value):
        print "Call_back2: %s" % value
        
    def call_back_any(value, topic=AUTO_TOPIC):
        """callback can receive optional topic=AUTO_TOPIC to find out
        what the received topic is"""
        print "call_back_any: %s - %s" %(value, topic.getNameTuple()[1])
        
    class TestModel(object):
        
        obs_field1 = ObsClassAttr("obs_field1")
        obs_field2 = ObsClassAttr("obs_field2")
        
        def __init__(self, obs_field1= "", obs_field2= ""):
            self.obs_field1 = obs_field1
            self.obs_field2 = obs_field2
            
    test_model = TestModel("field1 start value", "field2 start value")
    obs_attr(test_model, "obs_field1", call_back1)
    obs_attr(test_model, "obs_field2", call_back2)
    obs_any(test_model, call_back_any)
    
    test_model.obs_field1 = "field1 new value"
    test_model.obs_field2 = "field2 new value"
    
    
        