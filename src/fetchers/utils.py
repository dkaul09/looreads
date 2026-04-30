from urllib.parse import urlparse, urlencode, parse_qsl

_UTM_PARAMS = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
               "trk", "sc_channel", "st"}


def clean_url(url: str) -> str:
    try:
        parsed = urlparse(url)
        kept = [(k, v) for k, v in parse_qsl(parsed.query) if k not in _UTM_PARAMS]
        clean = parsed._replace(query=urlencode(kept))
        return clean.geturl()
    except Exception:
        return url
