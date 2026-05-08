'''
Mousehunt Title Screen
'''

def main():
      title = 'Mousehunt'
      
      logo = '''
       ____()()
      /      @@
`~~~~~\_;m__m._>o'''
      
      author = 'Bassam Batch'

      credits = f'''
Inspired by Mousehunt© Hitgrab
Programmer - {author}
Mice art - Joan Stark and Hayley Jane Wakenshaw
'''

      print(f"{title}\n{logo}\n{credits}")


# Using the following condition so that file is not automatically run when imported
if __name__ == '__main__':
      main()
