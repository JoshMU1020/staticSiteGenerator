class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = ""
        if self.props is not None:
            for key, val in self.props.items():
                result += f" {key}=\"{val}\""
        return result

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, None, None, props)
        self.value = value

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes require a value.")
        elif self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return (self.tag == other.tag and
                self.value == other.value and
                self.props == other.props)


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, None, props)
        self.children = children

    def to_html(self):
        if self.tag == None:
            raise ValueError("A tag must be provided for parent nodes.")
        elif self.children == None or self.children == []:
            raise ValueError("Parent nodes MUST have children.")
        else:
            childStr = ""
            for child in self.children:
                childStr += child.to_html()
            
            return f"<{self.tag}{self.props_to_html()}>{childStr}</{self.tag}>"
        
        
