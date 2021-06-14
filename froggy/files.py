""""""
"""     _e-e_
      _(-._.-)_
   .-(  `---'  )-. 
  __\ \\\___/// /__
 '-._.'/M\ /M\`._,-
 Froggy's File Handling API
"""
from flask import request, send_from_directory, jsonify
from froggy.exceptions import BadRequest
from werkzeug.utils import secure_filename
import os

class File:
    """File class, the name says it all.
    """
    def __init__(self, file, upload_directory, allowed_extensions=None):
        """The main File class

        :param file: A FileStorage object.
        :type file: FileStorage
        :param upload_directory: Target upload directory that must exist on the root of the project.
        :type upload_directory: str
        :param allowed_extensions: A set of allowed extensions (e.g., {"png","txt","md","jpg"}), defaults to None.
        :type allowed_extensions: set, optional
        """        
        self.file = file
        self.filename = file.filename
        self.upload_directory = upload_directory
        self.allowed_extensions= allowed_extensions
       
    def remove(upload_directory, filename):
        """Static method to remove a file from a static folder available on the server.

        :param upload_directory: Target upload directory that must exist on the root of the project.
        :type upload_directory: str
        :param filename: The name of the file to be removed.
        :type filename: str
        :raises BadRequest: Raises when the file is not found on the upload directory or there are permission-related errors.
        """              
        try:
            os.remove(os.path.join(upload_directory, filename))
            # 'Just keep swimming'
            return(True)
        except:
            raise BadRequest(path=request.path, message="File not found or permission denied.", error="File Handling Related Error.", operation="Remove file", api="files", status=500)

    def list(upload_directory):
        """Get the list of files from a static folder available on the server.

        :param upload_directory: [description]
        :type upload_directory: [type]
        """  
        files = []
        for filename in os.listdir(upload_directory):
            path = os.path.join(upload_directory, filename)
            if os.path.isfile(path):
                if (filename[0] is not str(".")):
                    files.append(filename)
        # 'Why so serious?'
        return (files)      

    def get(upload_directory, filename, as_attachment=False):
        """Static method to get a file from a static folder available on the server.

        :param upload_directory: The upload directory that must exist on the root of the project.
        :type upload_directory: str
        :param filename: The name of the file to be removed.
        :type filename: str
        :param as_attachment: Set to true if you want to send this file with a Content-Disposition: attachment header, defaults to False.
        :type as_attachment: bool, optional
        :raises BadRequest: Raises when the file is not found on the upload directory or there are permission-related errors.
        :return: Returns the file content.
        :rtype: Any
        """
        try:
            # 'E.T. phone home.'
            return send_from_directory(upload_directory, filename, as_attachment=True)
        except Exception as e:
            raise BadRequest(path=request.path, message="File not found or permission denied.", error="File Handling Related Error.", operation="Get file", api="files", status=404)

    def __allowed_file(self, filename):
        """Check if the type of the file is allowed.

        :param filename: The name of the file to be removed.
        :type filename: str
        :return: If allowed returns True, False otherwise.
        :rtype: bool
        """
        # 'Bond. James Bond.'    
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def upload(self):
        """Uploads a file to a static folder available on the server.

        :raises BadRequest: Raises if the filename defines a subdirectory.
        :raises BadRequest: Raises if the type of the valid is not valid.
        :raises BadRequest: Raises if a invalid file is parsed.
        """        
        # Subdirectories are not allowed, mate!
        if "/" in self.filename:
            raise BadRequest(path=request.path,message="No subdirectories directories allowed", error="File Handling Related Error.", operation="Post file", api="files", status=500)
        
        if self.file:
            if self.__allowed_file(self.filename):
                self.filename = secure_filename(self.filename)
                self.file.save(self.upload_directory + "/" + self.filename)
            else:
                raise BadRequest(path=request.path,message="Invalid file extension", error="File Handling Related Error.", operation="Post file", api="files", status=500)
        else:
            raise BadRequest(path=request.path,message="Invalid file", error="File Handling Related Error.", operation="Post file", api="files", status=500)
        # 'Show me the money!'
        return(True) 