import os

class FileManager:
    def __init__(self, directory_name):
        self.directory_name = directory_name

    def create_directory(self):
        try:
            os.makedirs(self.directory_name, exist_ok=True)
            print(f"Directory '{self.directory_name}' created successfully!")
        except Exception as e:
            print(f"Error: {e}")

    def files_in_dir(self):
        try:
            filenames = [f for f in os.listdir(self.directory_name) if os.path.isfile(os.path.join(self.directory_name, f))]
            return filenames
        except Exception as e:
            print(f"Error: {e}")
            return []

    def text_to_file(self, file_name, text):
        with open(f"{self.directory_name}/{file_name}", 'w') as file:
            file.write(text)
        print(f"Text has been written to {file_name}")

    def file_to_text(self, file_name):
        try:
            with open(f"{self.directory_name}/{file_name}", 'r') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            print(f"The file {file_name} does not exist.")
            return None



python = FileManager('python')
python.create_directory()
python.text_to_file('L1.txt', 'We talk about data types')
python.text_to_file('L2.txt', 'Lets learn about int and string')

# File data
for i in python.files_in_dir():
    print(i, python.file_to_text(f"{i}"))

