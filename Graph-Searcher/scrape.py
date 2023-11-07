# project: p3
# submitter: abkazan
# partner: none
# hours: 5

from collections import deque
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import pandas as pd
import time
import requests

class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []

    def visit_and_get_children(self, node):
        """ Record the node value in self.order, and return its children
        param: node
        return: children of the given node
        """
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        # 1. clear out visited set and order list
        self.visited.clear()
        self.order.clear()
        # 2. start recursive search by calling dfs_visit
        self.dfs_visit(node)

    def dfs_visit(self, node):
        # 1. if this node has already been visited, just `return` (no value necessary)
        if node in self.visited:
            return
        # 2. mark node as visited by adding it to the set
        self.visited.add(node)
        # 3. call self.visit_and_get_children(node) to get the children
        children = self.visit_and_get_children(node)
        # 4. in a loop, call dfs_visit on each of the children
        for child in children:
            self.dfs_visit(child)
    
    def bfs_search(self, node):
        todo = deque([node])
        discovered = {node}
        graph = {}
        while len(todo) > 0 and len(discovered) < 30:
            node = todo.popleft()
            #self.order.append(node)
            children = self.visit_and_get_children(node)
            graph[node] = children
            for child in children:
                if not child in discovered:
                    todo.append(child)
                    discovered.add(child)
        
class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__() # call constructor method of parent class
        self.df = df

    def visit_and_get_children(self, node):
        # TODO: Record the node value in self.order
        self.order.append(node)
        children = []
        # TODO: use `self.df` to determine what children the node has and append them
        for child, has_edge in self.df.loc[node].items():
            if has_edge == 1:
                children.append(child)
        return children
    
class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__()
    
    #The visit_and_get_children method should read a node file, 
    #record its vlaue in self.order and return a list of children. 
    def visit_and_get_children(self, filename):
        filename = "file_nodes/" + filename
        with open(filename, 'r') as f:
            data = f.read()
            self.order.append(data.strip()[0])
            return data.strip()[2:].split(",")
            #print("end of data")

    #The concat_order method should return all the values concatenated together.
    def concat_order(self):
        ret = ""
        for c in self.order:
            ret += c
        return ret

class WebSearcher(GraphSearcher):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.tables = []
        #self.tables_dict = {}
        
    def visit_and_get_children(self, url):
        #print("we are in visit_and_get_children")
        self.order.append(url)
        self.driver.get(url)
        links = self.driver.find_elements_by_tag_name("a")
        html = self.driver.page_source
        # Use Pandas read_html to extract table fragments from the HTML content
        #print("pd.read_html:\n")
        self.tables.append(pd.read_html(html)[0].dropna(axis=1))
        #self.tables.append()
        # Store the tables in an attribute (for example, a dictionary)
        #print(f"self.tables:\n {self.tables}")
        hrefs = [link.get_attribute("href") for link in links]
        return hrefs
    
    def table(self):
        #print(self.order)
        return pd.concat(self.tables, ignore_index=True)

    

def reveal_secrets(driver, url, travellog):
    
    #generate a password from the "clues" column of the travellog DataFrame
    password = travellog['clue'].astype(str).str.cat()
    
    #visit url with the driver
    driver.get(url)
    
    #automate typing the password in the box and clicking "GO"
    pw = driver.find_element_by_id("password")
    pw.send_keys(password)
    go = driver.find_element_by_id("attempt-button")
    go.click()
    
    #wait until the pages is loaded (perhaps with time.sleep)
    time.sleep(5)
    
    #click the "View Location" button and wait until the result finishes loading
    view_loc = driver.find_element_by_tag_name("button")
    view_loc.click()
    
    #save the image that appears to a file named 'Current_Location.jpg' (use the requests module to do the download, once you get the URL from selenium)
    time.sleep(5)
    img_url = driver.find_element_by_tag_name("img").get_attribute("src")
    file_name = "Current_Location.jpg"
    img_bytes = requests.get(img_url)
    with open(file_name, "wb") as f:
        f.write(img_bytes.content)
    
    #return the current location that appears on the page (should be "BASCOM HALL")
    return driver.find_element_by_id("location").text

    
    