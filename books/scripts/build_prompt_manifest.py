#!/usr/bin/env python3
"""Create the traceable prompt manifest for the realistic coloring-book series."""
from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

THEMES = {
"crawling-bugs": ("Crawling Bugs", [
"ladybug crossing a veined leaf", "ants carrying crumbs beside an anthill", "caterpillar inching along a tomato stem", "beetle exploring beneath a fern", "snail gliding over a smooth garden stone", "centipede weaving through fallen leaves", "pill bug beside a patch of moss", "stick insect hiding among twigs", "praying mantis standing on a sunflower leaf", "earwig beneath a flowerpot", "ground beetle crossing a woodland path", "two ladybugs meeting on a daisy", "caterpillar nibbling a cabbage leaf"]),
"flying-bugs": ("Flying Bugs", [
"monarch butterfly visiting milkweed", "bumblebee gathering pollen from a sunflower", "dragonfly hovering above a pond", "moth flying near moonlit flowers", "ladybug opening its wings on a leaf", "fireflies glowing over tall grass", "damselfly resting on a reed", "honeybee returning to a hive", "swallowtail butterfly above wildflowers", "lacewing flying through a herb garden", "two butterflies over a puddle", "bee flying between apple blossoms", "dragonflies skimming a quiet stream"]),
"singing-birds": ("Singing Birds", [
"robin singing from an apple-tree branch", "cardinal singing beside winter berries", "bluebird calling from a fence post", "wren singing near a tiny nest", "meadowlark singing in tall grass", "finch singing among sunflowers", "mockingbird singing on a garden gate", "chickadee calling from a pine branch", "sparrow singing beneath spring blossoms", "warbler singing beside a woodland stream", "thrush singing on a mossy log", "canary singing near an open window", "two songbirds answering across branches"]),
"soaring-birds": ("Soaring Birds", [
"bald eagle gliding above a mountain valley", "gull soaring over ocean cliffs", "hawk circling above open fields", "owl flying over a moonlit forest", "pelican gliding above coastal waves", "albatross sailing over the open sea", "vulture riding warm air above desert rocks", "falcon flying past a canyon wall", "crane gliding above a wetland", "goose flying over a winding river", "kite bird soaring above grassland", "heron flying toward a lakeshore", "three swans flying above reeds"]),
"schools-of-fish": ("Schools of Fish", [
"school of clownfish weaving through sea anemones", "school of sardines turning above a reef", "young salmon swimming upstream together", "tropical fish circling coral towers", "goldfish swimming together in a garden pond", "angelfish moving through tall water plants", "tiny fish sheltering beneath a sea turtle", "striped fish exploring a rocky cove", "silver fish passing a sunken anchor", "reef fish swimming beneath a coral arch", "minnows gathering around lily-pad roots", "fish following bubbles near a shipwreck", "school of fish forming a spiral in open water"]),
"lonely-fish": ("Lonely Fish", [
"one clownfish exploring a quiet coral garden", "one pufferfish beside a treasure chest", "one seahorse holding a swaying reed", "one angelfish beneath a coral arch", "one goldfish circling a pond lily", "one betta fish among broad water plants", "one trout resting beside river stones", "one flying fish above a gentle wave", "one lanternfish in the deep ocean", "one goby peeking from a sandy burrow", "one butterflyfish beside a sea fan", "one young salmon facing a waterfall", "one tiny fish looking toward a distant school"]),
"roaring-dinosaurs": ("Roaring Dinosaurs", [
"Tyrannosaurus roaring in a fern-filled valley", "Triceratops calling beside a cycads grove", "Allosaurus roaring from a rocky ridge", "Stegosaurus bellowing near a river", "Spinosaurus calling beside a swamp", "Carnotaurus roaring across an open plain", "Ankylosaurus calling among tree ferns", "Dilophosaurus roaring near a fallen log", "Baryonyx calling beside a fish-filled stream", "Ceratosaurus roaring under a volcano", "Iguanodon calling across a herd", "Parasaurolophus trumpeting by a lake", "two young dinosaurs practicing tiny roars"]),
"sleepy-dinosaurs": ("Sleepy Dinosaurs", [
"young Triceratops sleeping beneath broad ferns", "baby Stegosaurus napping beside a warm rock", "small sauropod resting in a leafy nest", "young Tyrannosaurus sleeping under a tree fern", "Parasaurolophus dozing beside a quiet lake", "Ankylosaurus napping in soft moss", "three baby dinosaurs asleep in a nest", "Pteranodon sleeping on a sheltered cliff", "Iguanodon resting beneath a starry sky", "dinosaur curled beside an unhatched egg", "sleepy dinosaur beneath a crescent moon", "two young dinosaurs sharing a leafy bed", "dinosaur family resting at sunset"]),
"busy-farm-animals": ("Busy Farm Animals", [
"border collie guiding sheep through a gate", "hen leading chicks across the barnyard", "horse pulling a small hay wagon", "goat climbing onto a low wooden platform", "piglets rooting beside a garden fence", "ducks walking toward the farm pond", "cow standing beside a milking stool", "rooster greeting sunrise from a fence", "donkey carrying two baskets of apples", "barn cat watching mice near grain sacks", "geese patrolling beside the barn", "sheep walking home from pasture", "farm animals gathering as a tractor arrives"]),
"cuddly-farm-animals": ("Cuddly Farm Animals", [
"fluffy lamb resting in clover", "calf nuzzling its mother in a pasture", "two piglets cuddling in clean straw", "chick tucked beneath a mother hen", "foal resting beside a mare", "baby goat curled in a sunny barn doorway", "ducklings huddled beside a pond", "barn kittens sleeping in a hay basket", "rabbit nestled beside garden vegetables", "two lambs touching noses by a fence", "calf wearing a simple flower garland", "pony greeting a small barn cat", "young farm animals resting together at sunset"]),
"working-vehicles": ("Working Vehicles", [
"excavator digging at a construction site", "bulldozer pushing a mound of soil", "fire engine parked beside a fire station", "tractor plowing neat farm rows", "dump truck carrying gravel", "concrete mixer working beside a new building", "garbage truck collecting bins on a neighborhood street", "tow truck helping a small car", "snowplow clearing a winter road", "crane lifting a steel beam", "road roller flattening fresh pavement", "ambulance waiting outside a hospital", "three construction vehicles building a playground"]),
"racing-vehicles": ("Racing Vehicles", [
"race car rounding a track corner", "go-kart crossing a checkered finish line", "motocross bike climbing a dirt hill", "rally car driving along a forest road", "soapbox car racing down a neighborhood hill", "speedboat turning around a lake buoy", "sailboat racing beneath full sails", "bicycle racer climbing a country road", "monster truck driving over a dirt mound", "small racing plane circling a course marker", "snowmobile racing across a snowy field", "off-road buggy crossing a desert trail", "three friendly race cars lining up at the start"]),
}

BASE = """Use case: illustration-story
Asset type: interior page for a professionally published children's coloring book
Primary request: {scene}.
Audience: children ages 5-9
Style/medium: polished hand-inked black-and-white coloring-book line art; semi-realistic natural proportions; friendly and inviting, not babyish or exaggerated
Composition/framing: portrait 8.5 x 11 page; the named subject is large and unmistakable; believable habitat or working environment; full scene inside generous white margins; clear foreground, midground, and background
Line treatment: bold clean outer contours; medium-weight interior detail; consistent black lines on pure white; closed shapes suitable for coloring; large colorable areas
Constraints: no grayscale, no shading, no crosshatching, no filled black regions, no color, no text, no border, no watermark, no signature, no cropped subject, no frightening features, no brands, no logos, no recognizable fictional characters, no artist imitation, uncluttered composition, printable at high resolution"""

def main():
    ROOT.joinpath("prompts").mkdir(exist_ok=True)
    rows=[]
    for slug,(title,scenes) in THEMES.items():
        expanded=scenes + [s + " in a different natural viewpoint with a few additional habitat details" for s in scenes]
        for number,scene in enumerate(expanded,1):
            rows.append({"book_slug":slug,"book_title":title,"page":number,"scene":scene,"prompt":BASE.format(scene=scene)})
    with ROOT.joinpath("prompts","manifest.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    print(f"Wrote {len(rows)} page prompts")

if __name__ == "__main__": main()
