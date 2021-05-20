import os


def update_site():
      print("running command")
      cmd = r'C:\Users\colin\\anaconda3\condabin\conda.bat activate squish_site &' \
            r'cd C:\Users\colin\PycharmProjects\squish_site &' \
            r'python bulk_update.py '

      os.system(cmd)
