import re

from bs4 import BeautifulSoup

global soup


def init():
    global soup
    soup = BeautifulSoup(open("pagina.html", "r", encoding="utf-8"), "html.parser")


def menu_items():
    menu_titles = []
    for item in soup.findAll("li", {"role": "presentation"}):
        menu_titles.append(item.getText(strip=True))
    return menu_titles


def data():
    content = []
    for i, attribute in enumerate(menu_attributes()):
        div_element = soup.find("div", {"id": {attribute}})
        if len(menu_submenus()[i]) >= 1:
            tables = div_element.findAll("div", {"aria-labelledby": re.compile('.')})
            table_data = []
            for table in tables:
                rows = table.findAll(["th", "td"])
                row_data = []
                for row in rows:
                    row_data.append(row.getText(strip=True))

                table_data.append(row_data)
        else:
            table_body = div_element.find("table")
            rows = table_body.findAll(["th", "td"])
            table_data = []
            for row in rows:
                table_data.append(row.getText(strip=True))
        content.append(table_data)
    return content


def data_headcount():
    count = []
    for i, attribute in enumerate(menu_attributes()):
        div_element = soup.find("div", {"id": {attribute}})
        if len(menu_submenus()[i]) >= 1:
            tables = div_element.findAll("div", {"aria-labelledby": re.compile('.')})
            table_data = []
            for table in tables:
                rows = table.find(["tr"])
                num = 0
                for row in rows:
                    if row != "\n":
                        num += 1
                table_data.append(num)
            count.append(table_data)

        else:
            table_body = div_element.find("table")
            row = table_body.find(["tr"])
            num = 0
            for r in row:
                if r != "\n":
                    num += 1
            count.append(num)
    return count


def menu_attributes():
    attributes = []
    for item in soup.findAll("li", {"role": "presentation"}):
        attributes.append(item.findAll("a")[0].attrs['aria-controls'])
    return attributes


def menu_submenus():
    submenus = []
    for attribute in menu_attributes():
        div_element = soup.find("div", {"id": {attribute}})
        button_element = div_element.findAll("a", {"role": "button"})
        button_name = []
        for button in button_element:
            if button:
                button = button.getText(strip=True)
            else:
                button = ""
            button_name.append(button)
        submenus.append(button_name)
    return submenus
