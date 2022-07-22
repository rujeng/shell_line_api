class Config:
  __conf = {
    "open_time": "",
    "close_time": "",
    "distance_price_ratio": "",
  
  }
  __setters = ["username", "password"]

  @staticmethod
  def config(name):
    return Config.__conf[name]

  @staticmethod
  def set(name, value):
    if name in Config.__setters:
      Config.__conf[name] = value
    else:
      raise NameError("Name not accepted in set() method")