import os
import json
from django.utils.text import slugify

vape_brands = [
    "maryliq",
    "elfliq",
    "avct-avictor",
    "across-vape",
    "advken",
    "air-factory",
    "airistech",
    "airmez",
    "al-fakher",
    "aleader",
    "aleaf",
    "aloha-sun",
    "alt-zero",
    "armageddon",
    "aspire",
    "astro-eight",
    "asvape",
    "augvape",
    "auxo",
    "asmodus",
    "barz",
    "blvk-unicorn",
    "bmic-tech",
    "bp-mods",
    "bad-drip-labs",
    "baked-hhc",
    "bam-bam's-cannoli",
    "bantam-vape",
    "bar-juice",
    "beach-club-vapor",
    "beard-vape-co.",
    "binoid",
    "blank-bar",
    "blitz-enterprises",
    "bluegrass-cannabis-co.",
    "boulder-vape",
    "boundless",
    "bugatti",
    "cbdfx",
    "ccell",
    "crazyace",
    "cake-vapors",
    "cali-extrax",
    "candy-king",
    "carats",
    "cartisan",
    "chapo-extrax",
    "charlie's-chalk-dust",
    "cheech",
    "chillax",
    "chromium-crusher",
    "chubby-gorilla",
    "cloud-nurdz",
    "coastal-clouds",
    "coil-master",
    "coilology",
    "cookies",
    "craving-vapor",
    "crooked-creations",
    "cutleaf",
    "cuttwood",
    "czar",
    "dogg-lbs",
    "dovpo-technology",
    "dozo",
    "davinci-vaporizers",
    "damn-vape",
    "daywalker",
    "dazzleaf",
    "death-row",
    "delta-extrax",
    "delta-king",
    "delta-muchies",
    "desire-vape",
    "diamond-shruumz",
    "diamond-supply-co.",
    "digiflavor",
    "dimo-hemp",
    "dotmod",
    "dr-dabber",
    "dummy-vapes",
    "dripmore",
    "elf-thc",
    "elyxr",
    "eyce",
    "echo",
    "efest",
    "eighty-six",
    "eleaf",
    "elf-bar",
    "elysian-labs",
    "exodus",
    "feela",
    "flerbar",
    "flo",
    "fryd",
    "fume-vape",
    "fifty-bar",
    "firerose",
    "flayvorz",
    "flum-float",
    "flying-monkey",
    "focus-v",
    "foger",
    "food-fighter-juice",
    "four-seasons",
    "freemax",
    "fresh-farms-e-liquid",
    "frozen-fields",
    "frutia",
    "fume-extracts",
    "funky-republic",
    "grav-labs",
    "gumi",
    "galaxy-treats",
    "geek-vape",
    "geek'd-extracts",
    "ghost-hemp",
    "glamee",
    "glas-vapor",
    "goo'd-extracts",
    "good-vibez",
    "grenco-science",
    "göst-vapor",
    "hqd-technology",
    "half-bak'd",
    "hamilton-devices",
    "hangsen",
    "happi",
    "haze",
    "hellvape",
    "hemper",
    "hi-fog",
    "hidrip",
    "hixotic",
    "hidden-hills",
    "hideseek",
    "high-garden",
    "high-times",
    "hohm-tech",
    "honeyroot-wellness",
    "horizon-tech",
    "hugo-vapor",
    "hulk-hogan",
    "humble-juice-co.",
    "huni-badger",
    "icewave",
    "indacloud",
    "iykyk",
    "innevape",
    "innokin",
    "instabar",
    "ijoy",
    "imini",
    "jus-vape",
    "justfog",
    "jam-monster",
    "ivg",
    "jeeter",
    "jimmy-the-juiceman",
    "joyetech",
    "jubi",
    "juice-head",
    "juice-roll-upz",
    "just-cbd",
    "kilo",
    "kros",
    "kado",
    "kangertech",
    "kangvape",
    "keep-it-100",
    "king-van-vapes",
    "koi-cbd",
    "kush-burst",
    "kuz",
    "kynn-labs",
    "lg",
    "litto",
    "lokey",
    "lucid",
    "luffbar",
    "lve",
    "leaf-buddi",
    "lil-baby",
    "limitless-mod-co.",
    "logic",
    "lookah",
    "looper",
    "losst",
    "lost-mary",
    "lost-vape",
    "lykcan",
    "mj-arsenal",
    "mnke-bars",
    "mrkt",
    "mad-hatter",
    "nasty",
    "voopoo",
    "yeti",
    "pod-salt"
]


def create_fixture(model_name, pk, fields):
    return {
        "model": f"products.{model_name}",
        "pk": pk,
        "fields": fields
    }

def format_category_name(original_string):
    # Replace underscores with spaces
    formatted_string = original_string.replace('_', ' ')

    # Convert to slug
    slug = slugify(formatted_string)

    # Create a tuple with both formatted and slug
    name_n_slug = (formatted_string, slug)
    return name_n_slug
    
def find_brand(input_string):
    for brand in vape_brands:
        if brand in input_string:
            return brand
    return False

products = []
categories = []
brands = []
def create_product_fix(product_id, cat, name_slug_tuple, brand_id, sku, image_url):
    product_fixture = create_fixture("product", product_id, {
                    "category": cat,  
                    "slug": name_slug_tuple[1],
                    "sku": f"SKU{sku}",
                    "name": name_slug_tuple[0],
                    "image": image_url,
                    "brand": brand_id,  
                    "description": f"A high-quality product for Product {name_slug_tuple[0]}.",
                })

    products.append(product_fixture)

def add_extension_to_files_in_folder():
    product_id = 1
    category_id = 1
    brand_id = 1
    brand_pk = None

    for folder in os.listdir('media'):
        full_path = os.path.join('media', folder)

        if folder != 'jumbotron_images' and os.path.isdir(full_path):

            category_name_n_slug = format_category_name(folder)
            category_fixture = create_fixture("category", category_id,
                                            {"name":  category_name_n_slug[0],
                                            "slug": category_name_n_slug[1]})
            categories.append(category_fixture)

            if os.path.exists(full_path) and len(os.listdir(full_path)) > 0:
                for filename in os.listdir(full_path):
                    brand = find_brand(filename)

                    if brand:
                        brand_pk = next((fixture['pk'] for fixture in \
                                         brands if brand in fixture['fields']['slug']), None)
                        match = brand.replace('-', ' ')

                       
                        if brand_pk is None:
                            brand_fixture = create_fixture("brand",
                                                           brand_id,
                                                           {"name": match, "slug": brand})
                            brands.append(brand_fixture)
                            brand_pk = brand_id
                            brand_id += 1
                           
                    # Remove file extension
                    file_name_without_ext = filename.rsplit('.', 1)[0]

                    # Replace underscores with spaces
                    name = file_name_without_ext.replace('-', ' ')
                    slug = filename.rsplit('.', 1)[0]
                    product_name_n_slug = (name, slug)
                    sku = f"-{category_name_n_slug[0]}_{brand_id}{product_id}{category_id}"

                    create_product_fix(product_id, category_id,
                                       product_name_n_slug,
                                       brand_pk,
                                       sku,
                                       folder + '/' + filename)
                    product_id += 1

                    brand_pk = None


            category_id += 1


add_extension_to_files_in_folder()

fixtures = categories + brands + products


with open('products/fixtures/product_fixtures.json', 'w', encoding='utf-8') as f:
    json.dump(fixtures, f, indent=2)