from typing import Optional


class UpdateHeroDTO:
    
    def __init__(
        self, 
        imageUrl: Optional[str] = None,
        imageAlt: Optional[str] = None,
        textCta: Optional[str] = None,
        urlCta: Optional[str] = None,
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
    def from_dict(cls, data:dict) -> "UpdateHeroDTO":
        
        if not isinstance(data, dict):
            raise ValueError("Invalid payload")
        
        
             
        
        
        return cls(
            imageUrl=data.get("imageUrl", None),
            imageAlt=data.get("imageAlt", None),
            textCta=data.get("textCta", None),
            urlCta=data.get("urlCta", None),
            headline=data.get("headline", None),
            highlight_word=data.get("highlight_word", None),
            subheadline=data.get("subheadline", None),
        )
        