from ..sections.about import IntroService, HistoryService, VisionService, DiferenciatorService, TeamService


class AboutPageService:
    
    @staticmethod
    def get_data(website):
        return {
            "intro": IntroService.get(website),
            "history": HistoryService.get(website),
            "vision": VisionService.get(website),
            "diferenciators": DiferenciatorService.get(website),
            "team": TeamService.get(website),
        }