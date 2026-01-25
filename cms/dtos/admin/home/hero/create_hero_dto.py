from typing import Optional


class CreateHeroDTO:
    
    def __init__(
        self, 
        imageUrl: str,
        imageAlt: str,
        textCta: str,
        urlCta: str,
        headline: Optional[str] = None, 
        highlight_word: Optional[str] = None,
        subheadline: Optional[str] = None
    ):
        self.headline = headline
        self.imageUrl = imageUrl
        self.imageAlt = imageAlt
        self.textCta = textCta
        self.urlCta = urlCta  
        self.highlight_word = highlight_word
        self.subheadline = subheadline
        
        
    @classmethod
    def from_dict(cls, data:dict) -> "CreateHeroDTO":
        
        if not isinstance(data, dict):
            raise ValueError("Invalid payload")
        
        required_fields = {
            "imageUrl": str,
            "imageAlt": str,
            "textCta": str,
            "urlCta": str,
        }
        
        for field, field_type in required_fields.items():
             if field not in data:
                 raise ValueError(f"{field} is required")
             
             if not isinstance(data[field], field_type):
                 raise ValueError(f"{field} must be {field_type.__name__}")
             
        
        
        return cls(
            imageUrl=data.get("imageUrl", ""),
            imageAlt=data.get("imageAlt", ""),
            textCta=data.get("textCta", ""),
            urlCta=data.get("urlCta", ""),
            headline=data.get("headline", ""),
            highlight_word=data.get("highlight_word", ""),
            subheadline=data.get("subheadline", ""),
        )
        