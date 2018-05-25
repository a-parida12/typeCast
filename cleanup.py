import textract
import os

DEFAULT_LANGUAGE = 'deu'
DEFAULT_INPUT_DIR = "inputdocuments"
DEFAULT_OUTPUT_DIR = "finaldocuments" 


cwd = os.getcwd()
list = []
def getFileName( path ):

  for subdir, dirs, files in os.walk(path):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file
        hidden_file = filepath
        if file != '.DS_Store':
          list.append(filepath)
  return list

getFileName(cwd + "/" + DEFAULT_INPUT_DIR)
# print(list)
for l in list:
  # print(l)
  file_name = os.path.splitext(l)[0] + '.txt'
  file_ext = os.path.splitext(l)[1]  
  print(file_name)
  if (file_ext != '.txt') and (l != file_name):
    parsed_text = textract.process(l)
#   # print(parsed_text)
    doc_path = DEFAULT_OUTPUT_DIR + "/"
#   # Create directory if not exists
    try: 
      os.makedirs(doc_path)
    except OSError:
        if not os.path.isdir(doc_path):
            raise
    file = open(file_name, 'w+')
    file.write(parsed_text)
    file.close()
