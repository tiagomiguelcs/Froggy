"""     _e-e_
      _(-._.-)_
   .-(  `---'  )-. 
  __\ \\\___/// /__
 '-._.'/M\ /M\`._,-
 Froggy's Gadgets or Utility Belt.
"""
import os

# if a path has white spaces for example /Google Drive/ then this method will added ' -> /'Google Drive'
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
    if (function is not None): function = "("+function+")"
    print("[Froggy] " + function + ":" + message)

