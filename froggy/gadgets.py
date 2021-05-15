""""""
"""     _e-e_
      _(-._.-)_
   .-(  `---'  )-. 
  __\ \\\___/// /__
 '-._.'/M\ /M\`._,-
 Froggy's Gadgets or Utility Belt.
"""
import os

def normpath(path):
    """Function to normalize a path. Expand the os.path.normpath to wrap white-spaced words with apostrophes (e.g. /Google Drive -> /'Google Drive').

    :param path: Path to normalize.
    :type path: str
    :return: Returns a normalized path
    :rtype: str
    """
    res = ""
    for directory in path.split('/'):
        try:
            directory.index(' ')
            res += "'" + directory + "'/"
        except ValueError as e: 
            res += directory + "/"
    # 'I want to play a game.'
    return(os.path.normpath(res))

def fprint(message, **kwargs):
    """The worldly know froggy custom print function (not really!).

    :param message: Message to display using the standard print function.
    :type message: str
    :param message: Options
    """
    # TODO: Use inspect.stack to get the function name where fprint was called from.
    function = kwargs.get('function', None) 
    if (function is not None): 
        print("[Froggy] ("+function+"):" + message)
    else:
        print("[Froggy]:"+message)
   

def exists(test_subject, keys):
    """Check if a list of keys exists in an object.

    :param test_subject: A dictionary object.
    :type test_subject: dic
    :param keys: The list of keys to be checked against the 'test_subject'.
    :type keys: list of str
    :return: True if the list of keys is available, false otherwise.
    :rtype: bool
    """    
    #Examples:froggy.gadgets.exists({"id": 1, "name": "Anna"}, {"createdon", "updatedon"})
    for key in keys:
        if key in test_subject:
            # Check if there is a value in the key, if not, return false.
            if (not test_subject[key]): 
                return(False)
        else:
            return(False)
    # 'They call me Mister Tibbs!'
    return(True)
