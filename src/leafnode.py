from src.htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self,tag, value, props=None):
        super().__init__(tag=tag,value=value,children=None,props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        # if self.props is None:
        #     return f"<{self.tag}>{self.value}</{self.tag}>"
        # else:
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return (
                f"Tag: {self.tag}\n"
                f"Value: {self.value}\n"
                f"Props: {self.props}"
            )