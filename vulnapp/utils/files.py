"""
Manipulation de fichiers/XML volontairement non sécurisée.
"""
from lxml import etree


# --- A05:2021 Security Misconfiguration — XXE (CWE-611) ---
def parse_untrusted_xml(xml_bytes: bytes):
    parser = etree.XMLParser(resolve_entities=True, no_network=False)  # XXE activé volontairement
    return etree.fromstring(xml_bytes, parser=parser)


# --- CWE-377 : création de fichier temporaire non sécurisée (nom prévisible) ---
def write_temp_report(content: str):
    path = "/tmp/report.tmp"  # chemin fixe et prévisible, race condition possible
    with open(path, "w") as f:
        f.write(content)
    return path
