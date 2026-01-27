class HTMLNode():
    def __init__(self,tag, value, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        # We join with quotes around the value to ensure valid HTML
        return "".join([f' {key}="{value}"' for key, value in self.props.items()])
    
    def __repr__(self):
        return (f"Tag: {self.tag}"
                f"Value: {self.value}"
                f"Children: {self.children}"
                f"Props: {self.props}")


