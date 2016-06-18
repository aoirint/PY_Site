# coding: utf-8

import sys
import io
import os
import json
import codecs
import tempfile
import subprocess

if __name__ == "__main__":
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    def arg_check(length, msg=None):
        result = len(sys.argv) < length+1 # filename arg1 arg2 -> len() == 3
        if (result): exit(msg if msg != None else 'Invalid args. Required ' + str(length))
        return result
    
    arg_check(1)

    SITE_FILE_VERSION = 1
    SITE_FILE = 'site.json'

    cmd = sys.argv[1]
    
    def exists_site():
        return os.path.isfile(SITE_FILE)
    
    def read_site():
        f = codecs.open(SITE_FILE, 'r', 'utf-8')
        data = json.loads(f.read())
        f.close()
        
        return data
    
    def write_site(data):
        f = codecs.open(SITE_FILE, 'w', 'utf-8')
        f.write(json.dumps(data))
        f.close()
    
    def read_page(name):
        f = codecs.open('pages/' + name + '.txt', 'r', 'utf-8')
        text = f.read()
        f.close()
        
        return text
    
    def write_page(name, text):
        f = codecs.open('pages/' + name + '.txt', 'w', 'utf-8')
        f.write(text)
        f.close()
    
    def success():
        print('Success: ' + cmd)

    def vim(file=None):
        
        if not file == None:
            fp = codecs.open(file, 'r', 'utf-8')
        else:
            fp = tempfile.NamedTemporaryFile(suffix='.tmp', delete=False)
        
        cmdList = ['vim', fp.name, '-n', '-c', '"set encoding=utf-8"', '-c', '"set fileencoding=utf-8"']
        
        subprocess.call(cmdList, shell=True)
        
        if not file == None:
            text = fp.read()
        else:
            text = fp.read().decode('utf-8')
        
        fp.close()
        
        # print(text)
        return text
    

    if cmd == 'init': # init %NAME
        arg_check(2)
        
        if exists_site():
            exit('Can\'t initialize a new site. Already exists')
        
        write_site(
        {
            '_version': SITE_FILE_VERSION,
            'name': sys.argv[2]
        })
        
        success()
            
    elif cmd == 'rename': # rename %NEW_NAME
        arg_check(2)
        
        if not exists_site():
            exit('Can\'t rename the site. Site is not found')

        data = read_site()
        data['name'] = sys.argv[2]
        
        write_site(data)
        success()

    elif cmd == 'page': # page %NAME %OPTION  (none -> create|edit / -d -> delete)
        arg_check(2)
        
        if not exists_site():
            exit('Can\'t edit a page. Site is not found')
        
        if not os.path.isdir('pages'):
            if os.path.exists('pages'):
                exit('Can\'t create a directory "pages". Already exists the same name file')
            else:
                os.mkdir('pages')
        
        data = read_site()
        if not 'pages' in data: data['pages'] = []
        
        name = sys.argv[2]
        
        if '-d' in sys.argv:
            if not name in data['pages']:
                exit('I can\'t delete the page "' + name + '". Not found')
            
            data['pages'].remove(name)

        else:
            if not name in data['pages']:
                data['pages'].append(name)
                
                text = vim()
                
                if not text == None:
                    f = codecs.open('pages/' + name + '.txt', 'w', 'utf-8')
                    f.write(text)
                    
                    f.close()
                else:
                    exit('Cannot create page with no char')
                
            else:
                vim('pages/' + name + '.txt')
            
        write_site(data)
        
        success()
    
    elif cmd == 'list':
        arg_check(2)
        
        if not exists_site():
            exit('Can\'t create a new page. Site is not found')
        
        data = read_site()
        
        what = sys.argv[2]
        
        if what == 'page':
            if not 'pages' in data or len(data['pages']) == 0:
                exit('No page was found');
            
            for name in data['pages']:
                print(name)
        
    elif cmd == 'vim':
        print(vim())
        
    else:
        exit('I don\'t know such a command: ' + cmd)

