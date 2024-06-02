from filemovement import transfer
from markdown import generate_pages_recursive

def main():
    transfer("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()
