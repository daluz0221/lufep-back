from ..sections.contact.form import FormService
from ..sections.contact.info import InfoService


class ContactPageService:

    @staticmethod
    def get_data(website):
        return {
            "form": FormService.get(website),
            "info": InfoService.get(website),
        }
