#!/usr/bin/env python3
# pylint: disable=missing-module-docstring

import typing
import json
from scoping import scoping


class Draw:
    """ handles json for settings regarding default values for drawing """

    settings_data: typing.Dict
    is_initialized: bool = False

    @staticmethod
    def init() -> 'Draw':
        if Draw.is_initialized == True:
            return

        # read settings data from json
        Draw.settings_data = None
        with open("draw_settings.json") as json_file:
            Draw.settings_data = json.load(json_file)
            #print(json.dumps(settings_data, sort_keys = True, indent = 4, ensure_ascii=False))

        Draw.check_values(Draw.settings_data)
        Draw.is_initialized = True

    @staticmethod
    def check_values(dictionary, prev=""):
        for key, value in dictionary.items():
            if type(value) is dict:
                if prev == "":
                    Draw.check_values(value, key)
                else:
                    Draw.check_values(value, prev + ":" + key)
            if value == "?":
                print("warning: unknown value in DrawSettings:", prev + ":" + key, "=", value)

    @staticmethod
    def __getitem__(item):
        Draw.init()
        return Draw.settings_data[item]

    @staticmethod
    def write_draw_settings() -> None:
        Draw.init()
        with open("draw_settings.json", "w") as outfile:
            json.dump(Draw.settings_data, outfile, sort_keys=True, indent=4)
        Draw.is_initialized = False

    @staticmethod
    def set_default_settings() -> None:
        # set non-existent data in json

        Draw.init()

        gehweg = Draw.settings_data.setdefault("gehweg", {})
        with scoping():
            breite = gehweg.setdefault("breite", {})
            with scoping():
                breite.setdefault("old", 1.5)
                breite.setdefault("min", 2.5)

        strasse = Draw.settings_data.setdefault("strasse", {})
        with scoping():
            spurbreite = strasse.setdefault("spurbreite", 3)

            bordstein = strasse.setdefault("bordstein", {})
            with scoping():
                bordstein.setdefault("breite", 0.165)
                bordstein.setdefault("laenge", 1)
                bordstein.setdefault("abstand", 0.01)

            linie = strasse.setdefault("linie", {})
            with scoping():
                breitstrich = linie.setdefault("breitstrich", 0.25)
                schmalstrich = linie.setdefault("schmalstrich", 0.12)

                leitlinie = linie.setdefault("leitlinie", {})
                with scoping():
                    # verhaeltnis laenge:luecke ist 1:2
                    abstand = leitlinie.setdefault("abstand", 6)
                    laenge = leitlinie.setdefault("laenge", 3)  # innerorts, ist variabel
                    breite = leitlinie.setdefault("breite", "schmalstrich")

                seitenlinie = linie.setdefault("seitenlinie", {})  # name ausgedacht
                with scoping():
                    abstand = seitenlinie.setdefault("abstand", 0)  # durchgezogen
                    laenge = seitenlinie.setdefault("laenge", 1)
                    breite = seitenlinie.setdefault("breite", "schmalstrich")

        cycleway = Draw.settings_data.setdefault("cycleway", {})
        with scoping():
            ausgeschildert = cycleway.setdefault("ausgeschildert", {})
            with scoping():
                hochbord = ausgeschildert.setdefault("hochbord", {})
                with scoping():
                    breite = hochbord.setdefault("breite", {})
                    with scoping():
                        breite.setdefault("min", 1.5)
                        breite.setdefault("opt", 2)

                    # linksseitig bedeutet meist, dass dieser geteilt, also in beide richtungen benutzt werden kann/muss
                    links = hochbord.setdefault("links", {})
                    with scoping():
                        breite = links.setdefault("breite", {})
                        with scoping():
                            breite.setdefault("min", 2)
                            breite.setdefault("opt", 2.4)

                    geh_rad = hochbord.setdefault("geh_rad", {})
                    with scoping():
                        breite = geh_rad.setdefault("breite", {})
                        with scoping():
                            breite.setdefault("min", 2.5)
                            breite.setdefault("opt", "?")

                radfahrstreifen = ausgeschildert.setdefault("radfahrstreifen", {})
                with scoping():
                    breite = radfahrstreifen.setdefault("breite", {})
                    with scoping():
                        breite.setdefault("min", 1.6)
                        breite.setdefault("opt", "?")

                    links = radfahrstreifen.setdefault("links", {})
                    with scoping():
                        breite = links.setdefault("breite", {})
                        with scoping():
                            breite.setdefault("min", "?")
                            breite.setdefault("opt", "?")

            # nicht ausgeschildert, also optional
            hochbord = cycleway.setdefault("hochbord", {})
            with scoping():
                breite = hochbord.setdefault("breite", {})
                with scoping():
                    breite.setdefault("min", "?")
                    breite.setdefault("opt", "?")

                geh_rad = hochbord.setdefault("geh_rad", {})
                with scoping():
                    breite = geh_rad.setdefault("breite", {})
                    with scoping():
                        breite.setdefault("min", "?")
                        breite.setdefault("opt", "?")

            schutzstreifen = cycleway.setdefault("schutzstreifen", {})
            with scoping():
                breite = schutzstreifen.setdefault("breite", {})
                with scoping():
                    breite.setdefault("min", 1.25)
                    breite.setdefault("opt", 1.50)

                seitenlinie = schutzstreifen.setdefault("seitenlinie", {})
                with scoping():
                    links = seitenlinie.setdefault("links", {})  # name ausgedacht
                    with scoping():
                        abstand = links.setdefault("abstand", 1)
                        laenge = links.setdefault("laenge", 1)
                        breite = links.setdefault("breite", "schmalstrich")

                    rechts = seitenlinie.setdefault("rechts", {})  # name ausgedacht
                    with scoping():
                        abstand = rechts.setdefault("abstand", 0)  # durchgezogen
                        laenge = rechts.setdefault("laenge", 1)
                        breite = rechts.setdefault("breite", "schmalstrich")

                kernfahrbahn = schutzstreifen.setdefault("kernfahrbahn", {})
                with scoping():
                    breite = kernfahrbahn.setdefault("breite", {})
                    with scoping():
                        breite.setdefault("min", 2.25)
                        breite.setdefault("opt", 3)

        pixel_pro_meter = Draw.settings_data.setdefault("pixel_pro_meter", 160)
        draw_height_meter = Draw.settings_data.setdefault("draw_height_meter", 10)

        schild = Draw.settings_data.setdefault("schild", {})
        with scoping():
            # um die schilder besser erkennen zu koennen im bild, stelle sie
            # nicht massstabsgetreu dar, sondern um diesen faktor vergroessert
            groessenfaktor = schild.setdefault("groessenfaktor", 5)

            rund = schild.setdefault("rund", {})
            with scoping():
                breite = schild.setdefault("breite", {})  # = durchmesser
                with scoping():
                    gross = breite.setdefault("gross", 0.6)
                    klein = breite.setdefault("klein", 0.42)

            zusatz = schild.setdefault("zusatz", {})
            with scoping():
                # hoehe egal, da seitenverhaeltnis beizubehalten ist
                breite = zusatz.setdefault("breite", {})
                with scoping():
                    gross = breite.setdefault("gross", 0.6)
                    klein = breite.setdefault("klein", 0.42)

        gruenstreifen = Draw.settings_data.setdefault("gruenstreifen", {})
        with scoping():
            breite = gruenstreifen.setdefault("breite", {})
            with scoping():
                breite.setdefault("min", 0)
                breite.setdefault("max", 1.5)  # quelle?
