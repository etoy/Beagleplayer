import UserDict

class Conf(UserDict.DictMixin):
    
    _data = {}
    
    def __init__(self, data={}):
        if len(data) > 0:
            self._data.update(data);
    
    def __setattr__(self, key, value):
        if key not in self._data:
            self._keys.append(key)
        self._data[key] = value
        
        
    def __getattr__(self, key):
        return self._data[key]
    
    
    def __delattr__(self, key):
        del self._data[key]
        self._keys.remove(key)

        
    
class ListenerConf(Conf):
    
    def __init__(self, data={}):
        Conf.__init__(self, data)
        self._data.update({'host':'', 'port':22044, 'broadcast':'<broadcast>'})
