single_item_row_template = """
            <tr>
                <td><img src={img} style="width: 150px; height: 150px;"></td>
                <td><a href={url}>{name}</a></td>
            </tr>
"""

multi_item_row_template = """
            <tr>
                <td><img src={img} style="width: 150px; height: 150px;"></td>
                <td colspan=2><a href={url}>{name}</a></td>
            </tr>
"""

sub_item_row_template = """
            <tr>
                <td></td>
                <td>{name}</td>
            </tr>
"""

def generate_html(json):
    with open("template.html","r") as f:
        template = f.read()
    final_str = ""
    for j in json:
        if j["in_stock"] == False:
            continue
        if j["sub_items"]:
            row = multi_item_row_template.format(img=j["img"], url=j["url"], name=j["name"])
            for si in j["sub_items"]:
                if si["in_stock"]:
                    row += sub_item_row_template.format(name=si["name"])
            final_str += row
        elif not j["sub_items"]:
            row = single_item_row_template.format(img=j["img"], url=j["url"], name=j["name"])
            final_str += row
    if final_str == "":
        return template.replace("{rows}","<h2>No In Stock Items \U0001f614</h2>")
    else:
        return template.replace("{rows}",final_str)
