from typing import List

class Character:
    def __init__(self, name: str, link: str, stands: List[str]=[]):
        self.name = name
        self.link = link
        self.stands = stands
    
    def __str__(self):
        return f"Name: {self.name}: \n Link: ({self.link}) \n Stands: {self.stands}"
    
    def get_stands(self):
        return self.stands
    
    def get_name(self):
        return self.name
    
    def get_link(self):
        return self.link
