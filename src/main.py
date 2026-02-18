from textnode import TextNode, TextType

def main():
    dummy = TextNode("dumb dummy, dumb dumb", TextType.TEXT)
    print(dummy.__repr__())

if __name__ == "__main__":
    main()