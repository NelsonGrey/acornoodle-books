#!/usr/bin/env python3
"""Build the age-5-9, non-repeating subject manifest for all twelve books."""
from __future__ import annotations
import csv
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

BOOKS={
"crawling-bugs":("Crawling Bugs","#5B8C35",[
"Harvester Ant","Leafcutter Ant","Seven-Spotted Lady Beetle","Stag Beetle","Rhinoceros Beetle","Dung Beetle","Ground Beetle","Rove Beetle","Woolly Bear Caterpillar","Swallowtail Caterpillar","Monarch Caterpillar","Earthworm","Garden Snail","Garden Slug","House Centipede","Giant Millipede","Pill Bug","Stick Insect","Praying Mantis","Earwig","Silverfish","Mole Cricket","Field Cricket","Jerusalem Cricket","Katydid","Desert Grasshopper"]),
"flying-bugs":("Flying Bugs","#D98B22",[
"Honey Bee","Bumblebee","Carpenter Bee","Mason Bee","Paper Wasp","Cicada","Monarch Butterfly","Swallowtail Butterfly","Painted Lady Butterfly","Blue Morpho Butterfly","Luna Moth","Atlas Moth","Hummingbird Moth","Common Dragonfly","Damselfly","Firefly","Lacewing","Hoverfly","Crane Fly","Mayfly","Caddisfly","Scorpionfly","Robber Fly","Gnat","Mosquito","Flying Lady Beetle"]),
"singing-birds":("Singing Birds","#D95763",[
"American Robin","Northern Cardinal","Eastern Bluebird","House Wren","Meadowlark","American Goldfinch","Mockingbird","Black-Capped Chickadee","Song Sparrow","Yellow Warbler","Wood Thrush","Canary","Indigo Bunting","Baltimore Oriole","Tufted Titmouse","Carolina Wren","Red-Winged Blackbird","White-Throated Sparrow","Rose-Breasted Grosbeak","Purple Finch","Common Nightingale","Skylark","Tree Swallow","Cedar Waxwing","Blue Jay","Brown Thrasher"]),
"soaring-birds":("Soaring Birds","#3B79A8",[
"Bald Eagle","Golden Eagle","Red-Tailed Hawk","Peregrine Falcon","Osprey","Turkey Vulture","California Condor","Barn Owl","Snowy Owl","Great Blue Heron","Sandhill Crane","Brown Pelican","White Pelican","Herring Gull","Albatross","Frigatebird","Canada Goose","Trumpeter Swan","Wood Stork","Roseate Spoonbill","American Kestrel","Mississippi Kite","Northern Harrier","Common Raven","Black Skimmer","Anhinga"]),
"schools-of-fish":("Schools of Fish","#168C9E",[
"Sardines","Anchovies","Herring","Mackerel","Blue Tangs","Yellow Tangs","Clownfish","Cardinalfish","Glassfish","Rainbowfish","Neon Tetras","Zebra Danios","Harlequin Rasboras","Silver Dollars","Scissortail Fish","Goatfish","Fusiliers","Snappers","Grunts","Bream","Mullet","Minnows","Salmon","Moorish Idols","Bannerfish","Jack Fish"]),
"lonely-fish":("Lonely Fish","#496DB3",[
"Pufferfish","Seahorse","Betta Fish","Lionfish","Anglerfish","Butterflyfish","Triggerfish","Parrotfish","Boxfish","Goby","Flounder","Moray Eel","Flying Fish","Swordfish","Pumpkinseed Sunfish","Barracuda","Mandarinfish","Discus Fish","Koi Fish","Goldfish","Trout","Catfish","Stingray","Electric Eel","Leafy Seadragon","Ocean Sunfish"]),
"roaring-dinosaurs":("Roaring Dinosaurs","#6A8F3D",[
"Tyrannosaurus Rex","Triceratops","Allosaurus","Stegosaurus","Spinosaurus","Carnotaurus","Ankylosaurus","Dilophosaurus","Baryonyx","Ceratosaurus","Iguanodon","Parasaurolophus","Giganotosaurus","Albertosaurus","Majungasaurus","Utahraptor","Deinonychus","Megalosaurus","Suchomimus","Acrocanthosaurus","Torvosaurus","Daspletosaurus","Cryolophosaurus","Monolophosaurus","Yangchuanosaurus","Mapusaurus"]),
"sleepy-dinosaurs":("Sleepy Dinosaurs","#7667A8",[
"Apatosaurus","Brachiosaurus","Diplodocus","Brontosaurus","Camarasaurus","Argentinosaurus","Dreadnoughtus","Patagotitan","Saltasaurus","Amargasaurus","Corythosaurus","Lambeosaurus","Maiasaura","Edmontosaurus","Pachycephalosaurus","Protoceratops","Styracosaurus","Euoplocephalus","Kentrosaurus","Plateosaurus","Psittacosaurus","Oviraptor","Gallimimus","Therizinosaurus","Microraptor","Compsognathus"]),
"busy-farm-animals":("Busy Farm Animals","#C47A2C",[
"Border Collie","Australian Shepherd","Belgian Draft Horse","Clydesdale Horse","Jersey Cow","Holstein Cow","Nubian Goat","Alpine Goat","Merino Sheep","Suffolk Sheep","Berkshire Pig","Tamworth Pig","Rhode Island Red Hen","Leghorn Hen","Pekin Duck","Embden Goose","Miniature Donkey","Barn Cat","Farm Rabbit","Llama","Alpaca","Guinea Fowl","Peacock","Turkey","Mule","Farm Rooster"]),
"cuddly-farm-animals":("Cuddly Farm Animals","#B45C7D",[
"Fluffy Lamb","Newborn Calf","Tiny Piglet","Baby Chick","Young Foal","Baby Goat","Duckling","Gosling","Barn Kitten","Baby Rabbit","Alpaca Cria","Llama Cria","Miniature Pony","Highland Calf","Jersey Calf","Merino Lamb","Nubian Kid","Pygmy Goat Kid","Silkie Chick","Turkey Poult","Guinea Keet","Peachick","Donkey Foal","Mule Foal","Baby Yak","Farm Puppy"]),
"working-vehicles":("Working Vehicles","#E0A11B",[
"Excavator","Bulldozer","Fire Engine","Farm Tractor","Dump Truck","Concrete Mixer","Garbage Truck","Tow Truck","Snowplow","Tower Crane","Road Roller","Ambulance","Backhoe Loader","Skid Steer Loader","Forklift","Street Sweeper","Bucket Truck","Logging Truck","Combine Harvester","Crop Sprayer","Rescue Helicopter","Mail Truck","Delivery Van","Utility Tractor","Trencher","Mobile Crane"]),
"racing-vehicles":("Racing Vehicles","#D34A38",[
"Formula Race Car","Stock Car","Rally Car","Go-Kart","Dragster","Motocross Bike","Superbike","BMX Bicycle","Mountain Bike","Soapbox Car","Monster Truck","Dune Buggy","Off-Road Truck","Racing Speedboat","Racing Sailboat","Jet Ski","Racing Kayak","Racing Canoe","Snowmobile","Racing Snowboard","Racing Ski","Small Racing Plane","Air Racing Biplane","Track Bicycle","Racing Wheelchair","Land-Speed Car"]),
}

ENVIRONMENTS=[
"with three simple habitat elements: one broad leaf, two smooth stones, and short grass",
"with three simple habitat elements: a small flower, a curved twig, and two pebbles",
"with three simple habitat elements: one tree trunk, a patch of moss, and a single cloud",
"with three simple habitat elements: a low fence, one plant, and a gently curving path",
"with three simple habitat elements appropriate to the subject, using no more than four background objects",
]

PROMPT="""Use case: illustration-story
Asset type: interior coloring page for children ages 5-9
Primary request: Draw one large, anatomically recognizable {label}, {environment}. The {label} is the only main subject and must occupy about 60 percent of the usable page.
Style/medium: polished black-and-white children's coloring-book line art; realistic enough to identify correctly, friendly and approachable
Composition: portrait 8.5 x 11; centered main subject; simple setting; generous white space; no visual clutter
Line treatment: very bold smooth outer contour; a few medium interior lines; large enclosed colorable shapes suitable for crayons and broad markers
Critical constraints: one main subject only; no other animal or vehicle; no text inside the illustration; no grayscale; no shading; no crosshatching; no solid black regions except tiny pupils; no color; no border; no watermark; no signature; no cropping; no brand; no logo; no fictional character; no artist imitation; maximum four simple environmental elements"""

def main():
    out=ROOT/"prompts"; out.mkdir(exist_ok=True)
    rows=[]
    for slug,(title,color,labels) in BOOKS.items():
        assert len(labels)==26 and len(set(labels))==26, slug
        for i,label in enumerate(labels,1):
            env=ENVIRONMENTS[(i-1)%len(ENVIRONMENTS)]
            rows.append({"book_slug":slug,"book_title":title,"cover_color":color,"page":i,"object_name":label,"prompt":PROMPT.format(label=label,environment=env),"status":"pending","asset_path":"","generator":"OpenAI built-in image generation","reference_images":"none"})
    path=out/"manifest-v2.csv"
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
    print(f"Wrote {len(rows)} non-repeating prompts to {path}")

if __name__=="__main__": main()
