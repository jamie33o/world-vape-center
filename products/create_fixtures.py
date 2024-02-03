import json

def create_fixture(model_name, pk, fields):
    return {
        "model": f"products.{model_name}",
        "pk": pk,
        "fields": fields
    }

# Categories
vape_categories = [
    ("Vape Kits", "vape-kits"),
    ("E-Liquids", "e-liquids"),
    ("Mods", "mods"),
    ("Coils", "coils"),
    ("Accessories", "accessories"),
    ("Pod Systems", "pod-systems"),
    ("Tanks", "tanks"),
    ("Batteries", "batteries"),
    ("Chargers", "chargers"),
    ("Nicotine Salts", "nicotine-salts"),
    ("Disposable Vapes", "disposable-vapes"),
    ("Starter Kits", "starter-kits"),
    ("Vape Pens", "vape-pens"),
    ("Squonk Mods", "squonk-mods"),
    ("DIY Supplies", "diy-supplies"),
]


categories = []
for i, category in enumerate(vape_categories):
    category_fixture = create_fixture("category", i+1, {"name":  category[0], "slug": category[1]})
    categories.append(category_fixture)

# Brands
vape_brands = [
    ("Vaporesso", "vaporesso"),
    ("SMOK", "smok"),
    ("Innokin", "innokin"),
    ("Aspire", "aspire"),
    ("GeekVape", "geekvape"),
    ("Voopoo", "voopoo"),
    ("Eleaf", "eleaf"),
    ("Joyetech", "joyetech"),
    ("Wismec", "wismec"),
    ("Sigelei", "sigelei"),
    ("Lost Vape", "lost-vape"),
    ("Vandy Vape", "vandy-vape"),
    ("Uwell", "uwell"),
    ("HorizonTech", "horizontech"),
    ("Freemax", "freemax"),
]


brands = []
for i, brand in enumerate(vape_brands):
    brand_fixture = create_fixture("brand", i+1, {"name": brand[0], "slug": brand[1]})
    brands.append(brand_fixture)


vape_options = [
    # 0-4 e-liquids
    ("10ml", "10ml"),
    ("20ml", "20ml"),
    ("30ml", "30ml"),
    ("50ml", "50ml"),
    ("Nicotine Free", "nicotine-free"),
    # coils 5-8
    ("Single Coil", "single-coil"),
    ("Dual Coil", "dual-coil"),
    ("Mesh Coil", "mesh-coil"),
    ("Ceramic Coil", "ceramic-coil"),
    # vape kits 9-12
    ("Variable Wattage", "variable-wattage"),
    ("Temperature Control", "temperature-control"),
    ("Pod System", "pod-system"),
    ("Box Mod", "box-mod"),
]

options = []
for i, option in enumerate(vape_options):
    option_fixture = create_fixture("multioption", i+1, {"name": option[0], "slug": option[1]})
    options.append(option_fixture)




# Products
e_liquid_name = [
    ("Mystic Mint E-liquid", "mystic-mint-e-liquid"),
    ("Tropical Breeze Vape Kit", "tropical-breeze-vape-kit"),
    ("Citrus Splash Nicotine Salt", "citrus-splash-nicotine-salt"),
    ("Sour Apple Vape Juice", "sour-apple-vape-juice"),
    ("Vanilla Dream Pod System", "vanilla-dream-pod-system"),
    ("Blueberry Burst CBD Vape Pen", "blueberry-burst-cbd-vape-pen"),
    ("Cherry Chill Nicotine Pouches", "cherry-chill-nicotine-pouches"),
    ("Mango Tango Disposable Vape", "mango-tango-disposable-vape"),
    ("Caramel Cloud Vape Mod", "caramel-cloud-vape-mod"),
    ("Strawberry Serenity E-hookah", "strawberry-serenity-e-hookah"),
    ("Watermelon Wave Vape Cartridge", "watermelon-wave-vape-cartridge"),
    ("Peppermint Pleasure THC Vape", "peppermint-pleasure-thc-vape"),
    ("Grape Glacier Nicotine Lozenges", "grape-glacier-nicotine-lozenges"),
    ("Cotton Candy Cloud E-liquid", "cotton-candy-cloud-e-liquid"),
    ("Lemon Lime Fizz Vape Pen", "lemon-lime-fizz-vape-pen"),
    ("Chocolate Bliss Nicotine Patch", "chocolate-bliss-nicotine-patch"),
    ("Honeydew Heaven CBD Gummies", "honeydew-heaven-cbd-gummies"),
    ("Pineapple Paradise Vape Stick", "pineapple-paradise-vape-stick"),
    ("Raspberry Rapture Vape Mod", "raspberry-rapture-vape-mod"),
    ("Coffee Craze E-hookah", "coffee-craze-e-hookah"),
    ("Peppermint Bark THC Vape", "peppermint-bark-thc-vape"),
    ("Blue Raspberry Burst Nicotine Pouches", "blue-raspberry-burst-nicotine-pouches"),
    ("Mango Madness Vape Juice", "mango-madness-vape-juice"),
    ("Cherry Cheesecake CBD Vape Pen", "cherry-cheesecake-cbd-vape-pen"),
    ("Pomegranate Punch Disposable Vape", "pomegranate-punch-disposable-vape"),
    ("Cinnamon Swirl Vape Cartridge", "cinnamon-swirl-vape-cartridge"),
    ("Coconut Cream Pie THC Vape", "coconut-cream-pie-thc-vape"),
    ("Orange Creamsicle Nicotine Lozenges", "orange-creamsicle-nicotine-lozenges"),
    ("Gingerbread Delight E-liquid", "gingerbread-delight-e-liquid"),
]



# Reviews
reviews = []
for i in range(1, 11):
    review_fixture = create_fixture("review", i, {
        "product": i % 10 + 1,
        "user": 1,
        "name": f"User {i}",
        "rating": 4 + i % 2,
        "comment": f"Review {i}: Great product!",
        "created_at": f"2022-01-{i:02d}T12:00:00Z"
    })
    reviews.append(review_fixture)



products = []
def create_product_fix(product_id, cat, name_slug_tuple, brand_id, options_name, options_id_list, sku):
    product_fixture = create_fixture("product", product_id, {
                    "category": cat,  
                    "slug": name_slug_tuple[1],
                    "sku": f"SKU{sku}",
                    "name": name_slug_tuple[0],
                    "image": "v3.jpeg",
                    "brand": brand_id,  
                    "description": f"A high-quality product for Product {name_slug_tuple[0]}.",
                    "price": 5.00 + i,
                    "countInStock": 10 - i,
                    "options_name": options_name,
                    "options": options_id_list
                })

    products.append(product_fixture)


for i, _ in enumerate(vape_categories):
    if i == 0:
        # vape kits
        vape_kits = [
            ("SMOK Nord 4", "smok-nord-4"),
            ("Voopoo Drag X Plus", "voopoo-drag-x-plus"),
            ("GeekVape Aegis X", "geekvape-aegis-x"),
            ("Vaporesso Luxe PM40", "vaporesso-luxe-pm40"),
            ("Innokin MVP5", "innokin-mvp5"),
            ("Lost Vape Thelema", "lost-vape-thelema"),
            ("Uwell Caliburn G", "uwell-caliburn-g"),
            ("Vaporesso XROS", "vaporesso-xros"),
            ("Voopoo Argus GT", "voopoo-argus-gt"),
            ("SMOK RPM 80 Pro", "smok-rpm-80-pro"),
            ("Vaporesso Luxe PM80", "vaporesso-luxe-pm80"),
            ("Voopoo Drag S", "voopoo-drag-s"),
            ("GeekVape Aegis X Zeus", "geekvape-aegis-x-zeus"),
            ("Vaporesso Swag PX80", "vaporesso-swag-px80"),
            ("SMOK Stick V9 Max", "smok-stick-v9-max"),
        ]

        for e in range(1, 11):
            create_product_fix(e, i+1, vape_kits[e], e, 'Kit Type', [9,10,11,12], e)

    elif i == 1:
        # e-liquid
        multi_options = [1,2,3,4,5]

        for e in range(1, 12):
            create_product_fix(e+10, i+1, e_liquid_name[e], e, 'Nicotine Strength', multi_options, e*i)


fixtures = categories + brands + options + products + reviews

with open('products/fixtures/product_fixtures.json', 'w', encoding='utf-8') as f:
    json.dump(fixtures, f, indent=2)