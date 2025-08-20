from gtts import gTTS
import io
import base64
import base64
import re

class TTSService:
    def __init__(self, lang: str = "ar", tld: str = "com.sa", slow: bool = False):
        self.lang = lang
        self.tld = tld
        self.slow = slow


    def _strip_emojis(self,text: str) -> str:
        # Broad emoji ranges (no external deps)
        _EMOJI_RE = re.compile(
            r"["
            r"\U0001F600-\U0001F64F"  # Emoticons 🙂
            r"\U0001F300-\U0001F5FF"  # Symbols & pictographs
            r"\U0001F680-\U0001F6FF"  # Transport & map
            r"\U0001F1E0-\U0001F1FF"  # Flags
            r"\U00002700-\U000027BF"  # Dingbats
            r"\U0001F900-\U0001F9FF"  # Supplemental Symbols & Pictographs
            r"\U00002600-\U000026FF"  # Misc symbols
            r"\U00002B00-\U00002BFF"  # Arrows etc.
            r"\U0001FA70-\U0001FAFF"  # Symbols & Pictographs Extended-A
            r"]+",
            flags=re.UNICODE,
        )
        # Common ASCII emoticons like :) :-D :(
        _ASCII_EMOTICON_RE = re.compile(r"(?:(?:[:;=8][\-^']?[\)D\(\]PpOo/\\])|<3)")

        # Zero-width joiner & variation selectors used in emoji sequences
        _ZWJ_OR_VARIATION = re.compile(r"[\u200D\uFE0F]")

        # Collapse extra whitespace
        _WS_RE = re.compile(r"\s+")

        text = _EMOJI_RE.sub("", text)
        text = _ASCII_EMOTICON_RE.sub("", text)
        text = _ZWJ_OR_VARIATION.sub("", text)
        text = _WS_RE.sub(" ", text).strip()
        return text

    def _prosody_hints(self,text: str, lang: str) -> str:
        """
        Tiny heuristics to encourage pauses (works for ar/en reasonably):
        - turn some ' - ' into commas,
        - add a space after Arabic comma '،' if missing,
        - add an ellipsis after exclamation for a micro pause,
        - normalize multiple punctuation.
        """
        s = text

        # Ensure space after Arabic comma
        s = re.sub(r"،(?!\s)", "، ", s)

        # Replace mid-sentence dashes with commas (gentle pause)
        s = re.sub(r"\s[-–—]\s", ", ", s)

        # Exclamation often spoken too fast; add a small pause via ellipsis
        s = re.sub(r"!+", "!…", s)

        # Normalize runs of punctuation
        s = re.sub(r"[.]{3,}", "…", s)
        s = re.sub(r"[!]{2,}", "!", s)
        s = re.sub(r"[?]{2,}", "?", s)

        # Optional: insert commas between numbered steps 1) 2) etc.
        s = re.sub(r"(\d+\))", r"\1،", s) if lang.startswith("ar") else s
        return s

    def speech(self, text: str, *, skip_emojis: bool = True, prosody: bool = True) -> str:
        # 1) Clean up emojis/emoticons so they’re not read aloud
        s = self._strip_emojis(text) if skip_emojis else text

        # 2) Lightweight prosody nudges via punctuation
        if prosody:
            s = self._prosody_hints(s, self.lang)

        # 3) Generate MP3
        tts = gTTS(text=s, lang=self.lang, tld=self.tld, slow=self.slow)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        data = buf.read()
        return base64.b64encode(data).decode("utf-8")

    # def speech(self, text:str) -> str:
    #     tts = gTTS(text=text, lang=self.lang)
    #     buf = io.BytesIO()
    #     tts.write_to_fp(buf)
    #     buf.seek(0)
    #     data = buf.read()
    #     return base64.b64encode(data).decode()