import re
import markdown
import sys
import os
import codecs

from bs4 import BeautifulSoup

class WikiExporter(object):
    
    def __init__(self, root_doc, options={}):
    
        self.root_doc = root_doc
        self.options = {}

        self.done_links = []
        self.content = ""
        
        
        self.css_media = options.get('css_media', ['themepdf.css'])
        
        
        
    def export_doc(self, output_file):
        self.parse_doc(self.root_doc)
        self.write_file(output_file)
    
    def get_doc_link_name(self, doc):
        
        pieces =  os.path.split(doc)
        doc_link_name =  os.path.splitext(pieces[-1])[0]
        return doc_link_name
        
    def get_doc_link_ext(self, doc):
        
        pieces =  os.path.split(doc)
        doc_link_ext =  os.path.splitext(pieces[-1])[1]
        return doc_link_ext
    
    
    def slugify_name(self, name):
        return name.lower().replace("-", "")
        
        
    def get_anchor_name(self, name):
        return self.slugify_name(name).replace("/", "-")
        
        
    def get_doc_for_link(self, doc, link):
    
        doc_link_name = self.get_doc_link_name(doc) 
        doc_ext = self.get_doc_link_ext(doc)
        
        file_list = []
        for root, subFolders, files in os.walk(os.path.dirname(self.root_doc)):
            if root.find(".git") > -1:
                continue
            for file in files:
                file_list.append(os.path.join(root, file))
                
        files_map = {}
        for f in file_list:
            slug =  self.slugify_name(os.path.split(f)[-1])
            files_map[slug] = f

        link_name = self.get_doc_link_name(link)
        candidate_slug = link_name + doc_ext
        candidate_slug = candidate_slug.lower()
        
        if candidate_slug in files_map:
            return files_map[candidate_slug]
            
        return None
        
            
    def parse_doc(self, doc):
    
        doc_link_name = self.get_doc_link_name(doc) 
    
        f = codecs.open(doc, mode="r", encoding="utf-8")
        content = f.read()
        """
        """
        f.close()
        
        html = markdown.markdown(content, extensions=['extra', 'codehilite', 'semanticwikilinks'])
        soup = BeautifulSoup(html)
        
        links_list = []
        links = soup.findAll("a")
        for l in links:
            #href = l.get("href")
            href = l.string
            links_list.append(href)
            slug_link = self.get_anchor_name(href)
            l["href"] =  "#" + slug_link
        
        self.content += str(soup)
        
        for candidate_link in links_list:
                    
            if candidate_link in self.done_links:
                continue
                
            if self.slugify_name(candidate_link) != self.slugify_name(doc_link_name):
                candidate_doc = self.get_doc_for_link(doc, candidate_link)
                self.done_links.append(candidate_link)

                if candidate_doc:
                    anchor_name = self.get_anchor_name(candidate_link)
                    tag = '<div class="page-breaker"></div><a name="%s">' % anchor_name
                    self.content += str(BeautifulSoup(tag))

                    self.parse_doc(candidate_doc)

    
    
    def generate_css(self):
        tpl = '<style>%s</style>'
        out = ''
        for css_media in self.css_media:
            filename = os.path.join(os.path.dirname(__file__), 'css', css_media)
            filename = os.path.abspath(filename)
            try:
                with open(filename, "rb") as f:
                
                    css_content = f.read()
                    item = tpl % css_content
                    out += item + "\n"
            except Exception, e:
                raise e
        return out
            
    
    
    
    def wrap_content(self):
        
        css = self.generate_css()
        html_doc =  "<html><head><meta charset='utf-8'>%s</head>" % css   + "<body><div class='container'>"+ self.content + "</div></body></html>"
        
        #soup = BeautifulSoup(html_doc)
        return html_doc
        
    
    def write_file(self, output_file):
        out_file = open(output_file, "wb")
        out_file.write(self.wrap_content())
        out_file.close()
        


if __name__ == '__main__':
    
    root_doc = sys.argv[1]
    output_file = sys.argv[2]
    
    if '--bootstrap' in sys.argv:
        worker.css_media.append('bootstrap.min.css')
    
    worker = WikiExporter(root_doc)
    worker.export_doc(output_file)
