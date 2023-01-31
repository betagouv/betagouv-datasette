import requests
from sqlite_utils import Database
from datetime import datetime, date

def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}


class Refresher:
    def __init__(self):
        self.startups = []
        self.startup_phases = []
        self.members = []
        self.member_missions = []
        self.startup_members = []
        self.startup_alumnis = []
        pass

    def run(self):
        self.db = Database("app/data.sqlite", recreate=True)
        self.refresh_startups()
        self.db["startups"].insert_all(
            self.startups,
            pk="id",
            columns={"id": str, "name": str, "pitch": str, "stats_url": str, "link": str, "repository": str, "contact": str, "budget_url": str, "accessibility_status": str, "analyse_risques_url": str},
            replace=True
        )
        self.db["startup_phases"].insert_all(
            self.startup_phases,
            pk=("startup_id", "index"),
            replace=True,
            foreign_keys=["startup_id"]
        )
        self.refresh_members()
        self.db["members"].insert_all(self.members, pk="id", replace=True)
        self.db["member_missions"].insert_all(
            self.member_missions,
            pk=("member_id", "index"),
            replace=True,
            foreign_keys=["member_id"]
        )
        self.db["startup_members"].insert_all(
            self.startup_members,
            replace=True,
            foreign_keys=["startup_id", "member_id"]
        )
        self.db["startup_alumnis"].insert_all(
            self.startup_alumnis,
            replace=True,
            foreign_keys=["startup_id", "member_id"]
        )

    def refresh_startups(self):
        json_res = requests.get("https://beta.gouv.fr/api/v2.5/startups.json").json()
        for raw in json_res["data"]:
            if raw["type"] != "startup":
                next
            self.handle_startup(raw)

    def handle_startup(self, raw_startup):
        startup = without_keys(raw_startup["attributes"], ["content_url_encoded_markdown", "events", "phases"])
        startup["id"] = raw_startup["id"]
        raw_phases = raw_startup["attributes"]["phases"]
        startup["current_phase"] = raw_phases[-1]["name"] if len(raw_phases) > 0 else None
        self.startups.append(startup)
        for index, raw_phase in enumerate(raw_phases):
            self.handle_startup_phase(raw_phase, index, startup)

    def handle_startup_phase(self, raw_phase, index, startup):
        phase = {"startup_id": startup["id"], "index": index, "name": raw_phase["name"] }
        phase["start"] = datetime.strptime(raw_phase["start"], "%Y-%m-%d") if raw_phase["start"] != "" else None
        phase["end"] = datetime.strptime(raw_phase["end"], "%Y-%m-%d") if raw_phase["end"] != "" else None
        self.startup_phases.append(phase)

    def refresh_members(self):
        json_res = requests.get("https://beta.gouv.fr/api/v2.5/authors.json").json()
        for raw in json_res:
            self.handle_member(raw)

    def handle_member(self, raw_member):
        member = without_keys(raw_member, ["missions", "startups", "previously"])
        self.members.append(member)
        for index, raw_mission in enumerate(raw_member["missions"]):
            self.handle_mission(raw_mission, index, member)
        for startup_id in raw_member.get("startups", []):
            self.startup_members.append({"member_id": member["id"], "startup_id": startup_id})
        for startup_id in raw_member.get("previously", []):
            self.startup_alumnis.append({"member_id": member["id"], "startup_id": startup_id})

    def handle_mission(self, raw_mission, index, member):
        mission = {"member_id": member["id"], "index": index, "status": raw_mission["status"], "employer": raw_mission["employer"] }
        mission["start"] = datetime.strptime(raw_mission["start"], "%Y-%m-%d") if raw_mission["start"] != "" else None
        mission["end"] = datetime.strptime(raw_mission["end"], "%Y-%m-%d") if raw_mission["end"] != "" else None
        self.member_missions.append(mission)

if __name__ == "__main__":
    Refresher().run()
