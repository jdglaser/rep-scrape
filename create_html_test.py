import lambda_function

test_json = lambda_function.lambda_handler("","")

with open("template.html", "r") as f:
    template = f.read()

single_item_row_template = """
            <tr>
                <td class="border"><img src={img}></td>
                <td class="border"><a href={url}>{name}</a></td>
                <td class="border">{in_stock}</td>
            </tr>
"""

multi_item_row_template = """
            <tr>
                <td class="border"><img src={img}></td>
                <td class="border" colspan=2><a href={url}>{name}</a></td>
            </tr>
"""

sub_item_row_template = """
            <tr>
                <td class="no-border"></td>
                <td class="border">{name}</td>
                <td class="border">{in_stock}</td>
            </tr>
"""

def generate_html(json):
    final_str = ""
    for j in json:
        if j["in_stock"] == False:
            continue
        if j["sub_items"]:
            row = multi_item_row_template.format(img=j["img"], url=j["url"], name=j["name"])
            for si in j["sub_items"]:
                if si["in_stock"]:
                    row += sub_item_row_template.format(name=si["name"], in_stock="In Stock")
            final_str += row
        elif not j["sub_items"]:
            row = single_item_row_template.format(img=j["img"], url=j["url"], name=j["name"], in_stock="In Stock")
            final_str += row
    if final_str == "":
        return "<h2>No In Stock Items \U0001f614</h2>"
    else:
        return final_str

insert = generate_html(test_json)
with open("output.html", "w", encoding='utf-8') as f:
    f.write(template.replace("{rows}",insert))
'''html = inject_html(test_json)
with open("output_test.html", "w") as f:
    f.write(html)'''
