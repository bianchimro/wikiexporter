import re
import markdown
import sys
import os
import codecs

from BeautifulSoup import BeautifulSoup

class WikiExporter(object):
    
    def __init__(self, root_doc):
    
        self.root_doc = root_doc
        self.done_links = []
        
        self.content = ""
        
        
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
        
        html = markdown.markdown(content, extensions=['extra', 'codehilite'])
        
        soup = BeautifulSoup(html)
        
        links_list = []
        links = soup.findAll("a")
        for l in links:
            href = l.get("href")
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
                    tag = '<hr/><a name="%s">' % anchor_name
                    self.content += str(BeautifulSoup(tag))

                    self.parse_doc(candidate_doc)

    
    
    def wrap_content(self):
        return "<html><head><meta charset='utf-8'> </head><body>" + self.content + "</body></html>"
        
    
    def write_file(self, output_file):
        out_file = open(output_file, "wb")
        out_file.write(self.wrap_content())
        out_file.close()
        


if __name__ == '__main__':
    
    root_doc = sys.argv[1]
    output_file = sys.argv[2]
    
    worker = WikiExporter(root_doc)
    worker.export_doc(output_file)
