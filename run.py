import argparse
from zotero2readwise.zt2rw import Zotero2Readwise

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("readwise_token", help="Readwise API token")
    parser.add_argument("zotero_key", help="Zotero API key")
    parser.add_argument("zotero_library_id", help="Zotero library ID")
    parser.add_argument("--library_type", default="user", choices=["user", "group"], help="Zotero library type")
    parser.add_argument("--include_annotations", default=True, type=bool, help="Include Zotero annotations")
    parser.add_argument("--include_notes", default=False, type=bool, help="Include Zotero notes")
    args = parser.parse_args()

    sync = Zotero2Readwise(
        readwise_token=args.readwise_token,
        zotero_key=args.zotero_key,
        zotero_library_id=args.zotero_library_id,
        zotero_library_type=args.library_type,
        include_annotations=args.include_annotations,
        include_notes=args.include_notes,
    )

    sync.run()

if __name__ == "__main__":
    main()
