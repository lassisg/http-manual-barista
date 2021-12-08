import os
import requests as req
from bs4 import BeautifulSoup
from fpdf import FPDF


def make_link_list(site_url: str) -> None:
    # set_status(1)
    # get_link(site_url)
    for i in range(1, 49):
        set_status(i)
        get_link(f"{site_url}?p={i}")


def get_link(url: str) -> None:
    r = req.get(url)
    img_link = ""
    if r.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
        for link in soup.find_all('source', type="image/png"):
            img_link = base_url + link.get('srcset')
            save_file(img_link)

    else:
        print(r.status_code)


def save_file(img_link: str) -> None:
    img_path = os.path.join(os.getcwd(), 'img')
    file_name = os.path.join(img_link.split('/')[-1])
    print(f"{file_name}...")

    file_path = os.path.join(img_path, file_name)
    myfile = req.get(f'{img_link}', allow_redirects=True)
    open(f'{file_path}', 'wb').write(myfile.content)
    pdf.add_page()
    pdf.image(file_path, 0, 0, 210, 297)


def set_status(file: int):
    print(f"Downloading image {file}: ", end="")


# TODO: Check image quality (currently getting wrong content)
img_path = os.path.join(os.getcwd(), 'img')
base_url = "https://www.manualpdf.pt"
product_url = "/caffitaly/cafe-expresso-pingo-doce-barista/manual"
site_url = base_url + product_url

pdf = FPDF()
make_link_list(site_url)
print("Saving file...")
pdf.output("manual_barista.pdf", "F")
