class HTMLNode:
    
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        prop_string = ""
        for item in self.props:
            prop_string += f'{item}="{self.props[item]}" '

        return prop_string.rstrip()

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("all leaf nodes must have a value")
        if not self.tag:
            return self.value
        if self.props:
            prop_str = self.props_to_html()
            return f"<{self.tag} {prop_str}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag is required")
        if not self.children:
            raise ValueError("children are required")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        if self.props:
            prop_str = self.props_to_html()
            return f"<{self.tag} {prop_str}>{children_html}</{self.tag}>"
        return f"<{self.tag}>{children_html}</{self.tag}>"
