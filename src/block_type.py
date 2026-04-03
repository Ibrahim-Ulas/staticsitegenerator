from enum import Enum 

class BlockType(Enum):
    P = "paragraph"
    H = "heading"
    C = "code"
    Q = "quote"
    UL = "unordered_list"
    OL = "ordered_list"