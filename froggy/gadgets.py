"""     _e-e_
      _(-._.-)_
   .-(  `---'  )-. 
  __\ \\\___/// /__
 '-._.'/M\ /M\`._,-
 Froggy's Gadgets or Utility Belt.
"""
import os

def normpath(path):
    """ Normalize a path.
        Expand the os.path.normpath to wrap white-spaced words with apostrophes (e.g. /Google Drive -> /'Google Drive').
    Args:
        path (string): Path to normalize.
    Returns:
        string: returns a normalized path.
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
    Args:
        message (string): Message to display using the standard print function.
        kwargs: the name of function calling fprint: function=main. 
                Froggy knows that we can use inspect.stack, but this way is better (he thinks!).
    """
    function = kwargs.get('function', None) 
    if (function is not None): 
        print("[Froggy] ("+function+"):" + message)
    else:
        print("[Froggy]:"+message)
   

def exists(test_subject, keys):
    """Check if a list of keys exists in an object.

    Args:
        test_subject (Dictionary): The dictionary object.
        keys (List of strings): The list of keys to be checked against the 'test_subject'.
    Returns:
        bool: True if the list of keys is available, false otherwise.
    Examples:
        froggy.gadgets.exists({"id": 1, "name": "Anna"}, {"createdon", "updatedon"})
    """
    for key in keys:
        if key in test_subject:
            # Check if there is a value in the key, if not, return false.
            if (not test_subject[key]): 
                return(False)
        else:
            return(False)
    # 'They call me Mister Tibbs!'
    return(True)
