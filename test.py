import pypub
my_first_epub = pypub.Epub('My First Epub')
my_first_chapter = pypub.create_chapter_from_url('https://en.wikipedia.org/wiki/EPUB')
my_first_epub.add_chapter(my_first_chapter)
my_first_epub.create_epub('OUTPUT_DIRECTORY')