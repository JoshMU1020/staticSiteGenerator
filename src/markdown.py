import re
from textnode import TextNode
from htmlnode import LeafNode
from converter import *
from filemovement import transfer
import os

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    headPrefixes = ["# ", "## ", "### ", "#### ", "##### ", "###### "]
    if block.startswith(tuple(headPrefixes)):
        return block_type_heading
    elif block.startswith("```") and block.endswith("```"):
        return block_type_code
    elif all(block.startswith(">") for line in block.split('\n')):
        return block_type_quote
    elif all(block.startswith("* ") or block.startswith("- ") for line in block.split('\n')):
        return block_type_unordered_list
    elif re.search(r'(^\d+\.\s)', block):
        pos = re.search(r'(^\d+\.\s)', block)
        past = int(block[0])
        subblocks = block.split('\n')
        for i in subblocks:
            pos = re.search(r'(^\d+\.\s)', i)
            if pos:
                if int(i[0]) == (past):
                    past += 1
                else:
                    return block_type_paragraph # not an ordered list
        return block_type_ordered_list
    else:
        return block_type_paragraph
    

def inline_format(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)  # Italic
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)  # Inline code
    return text


def convert_paragraph(block):
    list_of_textNodes = text_to_textnodes(block.replace('\n', ' '))
    htmlNode_list = []
    for text_node in list_of_textNodes:
        curr_html_node = text_node_to_html_node(text_node)
        htmlNode_list.append(curr_html_node)
    return ParentNode("p", htmlNode_list)


def convert_heading(block):
    headPrefixes = ["# ", "## ", "### ", "#### ", "##### ", "###### "]
    for i in headPrefixes:
        if block.startswith(i):
            return LeafNode(f"h{(headPrefixes.index(i)+1)}", block.lstrip(i))


def convert_quote(block):
    lines = block.split('\n')
    cleaned_lines = [line.lstrip("> ").strip() for line in lines]
    final_text = " ".join(cleaned_lines)
    formatted_content = inline_format(final_text)
    return LeafNode("blockquote", formatted_content)


def convert_code(block):
    left_backticks_pattern = re.compile(r'^```[a-z]*\n', re.IGNORECASE)
    return ParentNode("pre", [LeafNode("code", left_backticks_pattern.sub('', block).rstrip("```"))])


def convert_unordered_list(block):
    li_list = []
    for item in block.split("\n"):
        cleaned_item = item.lstrip("*- ").strip()
        formatted_item = inline_format(cleaned_item)
        li_list.append(LeafNode("li", formatted_item))
    
    return ParentNode("ul", li_list)


def convert_ordered_list(block):
    li_list = []
    for item in block.split("\n"):
        cleaned_item = item.lstrip("1234567890. ").strip()
        formatted_item = inline_format(cleaned_item)
        li_list.append(LeafNode("li", formatted_item))
    return ParentNode("ol", li_list)


def block_to_html(block):
    block_type = block_to_block_type(block)
    if block_type == "paragraph":
        return convert_paragraph(block)
    elif block_type == "heading":
        return convert_heading(block)
    elif block_type == "quote":
        return convert_quote(block)
    elif block_type == "code":
        return convert_code(block)
    elif block_type == "unordered_list":
        return convert_unordered_list(block)
    elif block_type == "ordered_list":
        return convert_ordered_list(block)
    else:
        raise Exception("Block type not supported.")


def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    leaf_list = []
    for block in block_list:
        leaf_list.append(block_to_html(block))
    return ParentNode("div", leaf_list, None)


def extract_title(markdown):
    mark_list = markdown.split("\n")
    for line in mark_list:
        if line.startswith("# "):
            return line.lstrip("# ")
    raise Exception("All pages need a single h1 header.")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown = f.read()
        f.close()
    with open(template_path) as f:
        starterHTML = f.read()
        f.close()
    
    html_node = markdown_to_html_node(markdown)
    html_string = html_node.to_html()
    title = extract_title(markdown)

    finalHTML = starterHTML.replace("{{ Title }}", title).replace("{{ Content }}", html_string)

    with open(os.path.join(dest_path, "index.html"), "w") as f:
        f.write(finalHTML)
        f.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
    for item in os.listdir(dir_path_content):
        if os.path.isfile(os.path.join(dir_path_content, item)):
            generate_page(os.path.join(dir_path_content, item), template_path, dest_dir_path)
        else:
            new_dir = os.path.join(dest_dir_path, item)
            os.mkdir(new_dir)
            generate_pages_recursive(os.path.join(dir_path_content, item), template_path, new_dir)
    return